"""
Build a Bay Area county resilience scorecard from annual county business-application data.

The scorecard is a transparent composite designed for monitoring the startup
application pipeline. It does not estimate startup quality, startup survival,
or venture funding outcomes.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from config import BAY_AREA_COUNTIES, REPO_ROOT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bfs-county-file",
        type=Path,
        default=REPO_ROOT / "data" / "raw" / "bfs_county_apps_annual.xlsx",
        help="Path to the annual county business-applications file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "outputs" / "validation_outputs",
        help="Directory where scorecard outputs will be written.",
    )
    parser.add_argument(
        "--volatility-start-year",
        type=int,
        default=2015,
        help="Start year for the volatility calculation window.",
    )
    parser.add_argument(
        "--base-year",
        type=int,
        default=2019,
        help="Base year for medium-run growth calculations.",
    )
    parser.add_argument(
        "--reference-year",
        type=int,
        default=2022,
        help="Reference year for rebound calculations.",
    )
    parser.add_argument(
        "--latest-year",
        type=int,
        default=2024,
        help="Latest year used in the scorecard.",
    )
    return parser.parse_args()


def load_long_panel(path: Path) -> pd.DataFrame:
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

    long_df = bay[["full_fips"] + ba_columns].melt(
        id_vars=["full_fips"],
        var_name="year_col",
        value_name="applications",
    )
    long_df["year"] = long_df["year_col"].str[2:].astype(int)
    long_df["applications"] = pd.to_numeric(long_df["applications"], errors="coerce")
    long_df["county_name"] = long_df["full_fips"].map(BAY_AREA_COUNTIES)
    long_df = long_df.sort_values(["full_fips", "year"]).reset_index(drop=True)
    long_df["yoy_pct"] = long_df.groupby("full_fips")["applications"].pct_change() * 100.0
    long_df["running_peak"] = long_df.groupby("full_fips")["applications"].cummax()
    long_df["drawdown_pct"] = (
        long_df["applications"] / long_df["running_peak"] - 1.0
    ) * 100.0
    return long_df


def compute_cagr(first: float, last: float, years: int) -> float:
    if pd.isna(first) or pd.isna(last) or first <= 0 or last <= 0 or years <= 0:
        return np.nan
    return (last / first) ** (1.0 / years) - 1.0


def min_max(series: pd.Series) -> pd.Series:
    minimum = series.min()
    maximum = series.max()
    if pd.isna(minimum) or pd.isna(maximum) or maximum == minimum:
        return pd.Series(0.0, index=series.index)
    return (series - minimum) / (maximum - minimum)


def build_scorecard(
    long_df: pd.DataFrame,
    volatility_start_year: int,
    base_year: int,
    reference_year: int,
    latest_year: int,
) -> pd.DataFrame:
    if latest_year not in set(long_df["year"]):
        raise ValueError(f"Latest year {latest_year} not found in panel.")

    latest_cross_section = long_df[long_df["year"] == latest_year].copy()
    regional_total = float(latest_cross_section["applications"].sum())

    rows: list[dict[str, float | int | str]] = []
    for full_fips, group in long_df.groupby("full_fips"):
        group = group.sort_values("year").reset_index(drop=True)

        latest = group[group["year"] == latest_year]
        base = group[group["year"] == base_year]
        ref = group[group["year"] == reference_year]
        previous = group[group["year"] == latest_year - 1]

        if latest.empty or base.empty or ref.empty or previous.empty:
            continue

        latest_value = float(latest["applications"].iloc[0])
        previous_value = float(previous["applications"].iloc[0])
        base_value = float(base["applications"].iloc[0])
        ref_value = float(ref["applications"].iloc[0])

        volatility_window = group[group["year"] >= volatility_start_year]
        yoy_volatility = float(volatility_window["yoy_pct"].dropna().std())

        medium_cagr = compute_cagr(
            first=base_value,
            last=latest_value,
            years=int(latest_year - base_year),
        ) * 100.0

        rows.append(
            {
                "full_fips": full_fips,
                "county_name": BAY_AREA_COUNTIES[full_fips],
                "applications_latest": latest_value,
                "share_latest_pct": latest_value / regional_total * 100.0,
                "yoy_latest_pct": (latest_value / previous_value - 1.0) * 100.0,
                "cagr_base_to_latest_pct": medium_cagr,
                "rebound_reference_to_latest_pct": (latest_value / ref_value - 1.0) * 100.0,
                "yoy_volatility_pct_pts": yoy_volatility,
                "max_drawdown_pct": float(group["drawdown_pct"].min()),
            }
        )

    scorecard = pd.DataFrame(rows)
    if scorecard.empty:
        raise ValueError("Scorecard produced no county rows.")

    scorecard["scale_component"] = np.log(scorecard["applications_latest"])
    scorecard["momentum_component"] = scorecard["yoy_latest_pct"]
    scorecard["medium_growth_component"] = scorecard["cagr_base_to_latest_pct"]
    scorecard["rebound_component"] = scorecard["rebound_reference_to_latest_pct"]
    scorecard["stability_component"] = -scorecard["yoy_volatility_pct_pts"]
    scorecard["drawdown_resilience_component"] = scorecard["max_drawdown_pct"]

    normalized_columns = []
    for raw_column in [
        "scale_component",
        "momentum_component",
        "medium_growth_component",
        "rebound_component",
        "stability_component",
        "drawdown_resilience_component",
    ]:
        normalized_column = f"norm_{raw_column}"
        scorecard[normalized_column] = min_max(scorecard[raw_column])
        normalized_columns.append(normalized_column)

    scorecard["resilience_score_0_100"] = scorecard[normalized_columns].mean(axis=1) * 100.0
    scorecard["resilience_rank"] = scorecard["resilience_score_0_100"].rank(
        method="first", ascending=False
    ).astype(int)

    change_driver = scorecard["applications_latest"] * scorecard["yoy_latest_pct"] / 100.0
    total_change_driver = float(change_driver.sum())
    if total_change_driver != 0:
        scorecard["contribution_to_latest_change_pct"] = change_driver / total_change_driver * 100.0
    else:
        scorecard["contribution_to_latest_change_pct"] = 0.0

    return scorecard.sort_values(
        ["resilience_score_0_100", "applications_latest"],
        ascending=[False, False],
    ).reset_index(drop=True)


def build_summary(scorecard: pd.DataFrame, latest_year: int) -> dict:
    top = scorecard.iloc[0]
    bottom = scorecard.iloc[-1]
    return {
        "latest_year": latest_year,
        "regional_total_latest": float(scorecard["applications_latest"].sum()),
        "top_county": {
            "county_name": top["county_name"],
            "resilience_score_0_100": float(top["resilience_score_0_100"]),
            "share_latest_pct": float(top["share_latest_pct"]),
        },
        "bottom_county": {
            "county_name": bottom["county_name"],
            "resilience_score_0_100": float(bottom["resilience_score_0_100"]),
            "share_latest_pct": float(bottom["share_latest_pct"]),
        },
        "top_three_share_pct": float(scorecard["share_latest_pct"].nlargest(3).sum()),
        "median_resilience_score": float(scorecard["resilience_score_0_100"].median()),
    }


def write_outputs(scorecard: pd.DataFrame, summary: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    scorecard.to_csv(output_dir / "bay_area_county_resilience_scorecard.csv", index=False)
    with (output_dir / "bay_area_county_resilience_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)


def main() -> None:
    args = parse_args()
    long_df = load_long_panel(args.bfs_county_file)
    scorecard = build_scorecard(
        long_df=long_df,
        volatility_start_year=args.volatility_start_year,
        base_year=args.base_year,
        reference_year=args.reference_year,
        latest_year=args.latest_year,
    )
    summary = build_summary(scorecard, latest_year=args.latest_year)
    write_outputs(scorecard, summary, output_dir=args.output_dir)
    print(f"Wrote resilience scorecard outputs to: {args.output_dir}")


if __name__ == "__main__":
    main()
