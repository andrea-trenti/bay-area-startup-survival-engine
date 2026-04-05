"""
Backtest annual Bay Area startup-pipeline nowcasts using public U.S. Census data.

The script combines:
1. California monthly Business Formation Statistics (BFS) totals; and
2. Bay Area annual county business-applications totals.

It produces a pseudo-real-time rolling backtest for March, June, and September
cutoffs under a transparent bridge model:
- infer California annual total from year-to-date observations and historical
  completion fractions;
- infer Bay Area annual total from the estimated California annual total and
  a lagged Bay Area share of California applications.

The script is intentionally narrow. It estimates an annual formation proxy, not
startup survival, employer births, or venture outcomes.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from config import BAY_AREA_COUNTIES, REPO_ROOT

MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bfs-monthly-file",
        type=Path,
        default=REPO_ROOT / "data" / "raw" / "bfs_monthly.csv",
        help="Path to the public BFS monthly CSV file.",
    )
    parser.add_argument(
        "--bfs-county-file",
        type=Path,
        default=REPO_ROOT / "data" / "raw" / "bfs_county_apps_annual.xlsx",
        help="Path to the public annual county business-applications file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "outputs" / "validation_outputs",
        help="Directory where derived backtest outputs will be written.",
    )
    parser.add_argument(
        "--share-window",
        type=int,
        default=3,
        help="Trailing window length for Bay Area share estimation.",
    )
    parser.add_argument(
        "--fraction-window",
        type=int,
        default=5,
        help="Trailing window length for California completion-fraction estimation.",
    )
    parser.add_argument(
        "--minimum-evaluation-year",
        type=int,
        default=2010,
        help="Earliest target year included in the reported backtest.",
    )
    return parser.parse_args()


def load_bay_area_annual(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Annual county file not found: {path}")

    df = pd.read_excel(path, header=2, dtype=str)
    required = {"state_fips", "county_fips"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Annual county file is missing required columns: {sorted(missing)}")

    df["state_fips"] = df["state_fips"].astype(str).str.zfill(2)
    df["county_fips"] = df["county_fips"].astype(str).str.zfill(3)
    df["full_fips"] = df["state_fips"] + df["county_fips"]

    ba_columns = [str(col) for col in df.columns if str(col).startswith("BA")]
    if not ba_columns:
        raise ValueError("No BA annual columns found in county file.")

    bay = df[df["full_fips"].isin(BAY_AREA_COUNTIES)].copy()
    if bay.empty:
        raise ValueError("No Bay Area counties found in annual county file.")

    for col in ba_columns:
        bay[col] = pd.to_numeric(bay[col], errors="coerce")

    annual = (
        bay[["full_fips"] + ba_columns]
        .set_index("full_fips")
        .sum(axis=0)
        .rename("bay_area_applications")
        .reset_index()
        .rename(columns={"index": "year_col"})
    )
    annual["year"] = annual["year_col"].str[2:].astype(int)
    annual = annual[["year", "bay_area_applications"]].sort_values("year").reset_index(drop=True)
    return annual


def load_california_monthly(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    if not path.exists():
        raise FileNotFoundError(f"BFS monthly file not found: {path}")

    df = pd.read_csv(path)
    required = {"sa", "naics_sector", "series", "geo", "year"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"BFS monthly file is missing required columns: {sorted(missing)}")

    ca = df[
        (df["geo"] == "CA")
        & (df["series"] == "BA_BA")
        & (df["naics_sector"] == "TOTAL")
        & (df["sa"] == "U")
    ].copy()

    if ca.empty:
        raise ValueError("No California total BA_BA rows found in monthly BFS file.")

    for month in MONTHS:
        ca[month] = pd.to_numeric(ca[month], errors="coerce")

    long_rows: list[dict[str, float | int]] = []
    for _, row in ca.iterrows():
        year = int(row["year"])
        cumulative = 0.0
        for month_index, month in enumerate(MONTHS, start=1):
            value = row[month]
            if pd.notna(value):
                cumulative += float(value)
                long_rows.append(
                    {
                        "year": year,
                        "month": month_index,
                        "monthly_value": float(value),
                        "ytd_value": cumulative,
                    }
                )
    long_df = pd.DataFrame(long_rows).sort_values(["year", "month"]).reset_index(drop=True)
    annual_df = (
        long_df.groupby("year", as_index=False)["monthly_value"]
        .sum()
        .rename(columns={"monthly_value": "california_annual_applications"})
        .sort_values("year")
        .reset_index(drop=True)
    )
    return long_df, annual_df


def build_backtest_frame(
    bay_area_annual: pd.DataFrame,
    california_monthly_long: pd.DataFrame,
    california_annual: pd.DataFrame,
    share_window: int,
    fraction_window: int,
    minimum_evaluation_year: int,
) -> pd.DataFrame:
    merged = bay_area_annual.merge(california_annual, on="year", how="inner")
    merged["bay_area_share_of_ca"] = (
        merged["bay_area_applications"] / merged["california_annual_applications"]
    )

    fractions = california_monthly_long.merge(california_annual, on="year", how="left")
    fractions["completion_fraction"] = (
        fractions["ytd_value"] / fractions["california_annual_applications"]
    )

    rows: list[dict[str, float | int]] = []
    valid_years = sorted(set(merged["year"]))

    for year in valid_years:
        if year > merged["year"].max() or year < minimum_evaluation_year:
            continue

        for cutoff in (3, 6, 9):
            ytd_match = fractions[(fractions["year"] == year) & (fractions["month"] == cutoff)]
            hist_frac = fractions[
                (fractions["month"] == cutoff)
                & (fractions["year"] < year)
                & (fractions["year"] >= year - fraction_window)
            ]
            hist_share = merged[
                (merged["year"] < year) & (merged["year"] >= year - share_window)
            ]

            if ytd_match.empty or hist_frac.empty or hist_share.empty:
                continue
            if len(hist_frac) < fraction_window or len(hist_share) < share_window:
                continue

            ytd = float(ytd_match["ytd_value"].iloc[0])
            avg_completion_fraction = float(hist_frac["completion_fraction"].mean())
            avg_bay_share = float(hist_share["bay_area_share_of_ca"].mean())

            if avg_completion_fraction <= 0:
                continue

            forecast_ca = ytd / avg_completion_fraction
            forecast_bay = forecast_ca * avg_bay_share

            actual_row = merged[merged["year"] == year].iloc[0]
            actual_bay = float(actual_row["bay_area_applications"])
            actual_yoy = float(
                actual_bay
                - merged.loc[merged["year"] == year - 1, "bay_area_applications"].iloc[0]
            ) if year - 1 in set(merged["year"]) else np.nan

            forecast_yoy = float(
                forecast_bay
                - merged.loc[merged["year"] == year - 1, "bay_area_applications"].iloc[0]
            ) if year - 1 in set(merged["year"]) else np.nan

            rows.append(
                {
                    "year": int(year),
                    "cutoff_month": int(cutoff),
                    "california_ytd_value": ytd,
                    "estimated_completion_fraction": avg_completion_fraction,
                    "estimated_bay_share": avg_bay_share,
                    "forecast_california_annual": forecast_ca,
                    "forecast_bay_area_annual": forecast_bay,
                    "actual_bay_area_annual": actual_bay,
                    "forecast_error": forecast_bay - actual_bay,
                    "absolute_percentage_error": abs(forecast_bay - actual_bay) / actual_bay * 100.0,
                    "captured_yoy_direction": (
                        np.sign(forecast_yoy) == np.sign(actual_yoy)
                        if pd.notna(actual_yoy) and pd.notna(forecast_yoy)
                        else np.nan
                    ),
                }
            )

    return pd.DataFrame(rows).sort_values(["cutoff_month", "year"]).reset_index(drop=True)


def summarize_backtest(backtest: pd.DataFrame) -> pd.DataFrame:
    def rmse(series: pd.Series) -> float:
        return float(np.sqrt(np.mean(np.square(series.astype(float)))))

    summary = (
        backtest.groupby("cutoff_month")
        .agg(
            observations=("year", "count"),
            mape_pct=("absolute_percentage_error", "mean"),
            median_ape_pct=("absolute_percentage_error", "median"),
            rmse=("forecast_error", rmse),
            mean_error=("forecast_error", "mean"),
            directional_accuracy=("captured_yoy_direction", "mean"),
        )
        .reset_index()
        .sort_values("cutoff_month")
        .reset_index(drop=True)
    )
    return summary


def write_outputs(backtest: pd.DataFrame, summary: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    backtest.to_csv(output_dir / "bay_area_nowcast_backtest_by_year.csv", index=False)
    summary.to_csv(output_dir / "bay_area_nowcast_backtest_summary.csv", index=False)

    backtest_summary = {
        "years_evaluated": sorted(backtest["year"].unique().tolist()),
        "cutoffs": sorted(backtest["cutoff_month"].unique().tolist()),
        "summary_records": summary.to_dict(orient="records"),
    }
    with (output_dir / "bay_area_nowcast_backtest_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(backtest_summary, handle, indent=2)


def main() -> None:
    args = parse_args()
    bay_area_annual = load_bay_area_annual(args.bfs_county_file)
    california_monthly_long, california_annual = load_california_monthly(args.bfs_monthly_file)
    backtest = build_backtest_frame(
        bay_area_annual=bay_area_annual,
        california_monthly_long=california_monthly_long,
        california_annual=california_annual,
        share_window=args.share_window,
        fraction_window=args.fraction_window,
        minimum_evaluation_year=args.minimum_evaluation_year,
    )
    if backtest.empty:
        raise ValueError("Backtest produced no rows. Check input files and window lengths.")
    summary = summarize_backtest(backtest)
    write_outputs(backtest, summary, args.output_dir)
    print(f"Wrote backtest outputs to: {args.output_dir}")


if __name__ == "__main__":
    main()
