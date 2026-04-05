"""
Compute Bay Area county hazard proxies from the annual county business-applications file.

The script intentionally produces diagnostic proxies rather than failure probabilities.
It is designed to work from a public source file held in the acquisition layer and not redistributed
in the public repository.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

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
        default=REPO_ROOT / "outputs" / "risk_diagnostics",
        help="Directory where derived outputs will be written.",
    )
    return parser.parse_args()


def get_ba_columns(columns: Iterable[str]) -> list[str]:
    return [str(col) for col in columns if str(col).startswith("BA")]


def load_bay_area_panel(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"BFS county file not found: {path}")

    df = pd.read_excel(path, header=2, dtype=str)
    required = {"State", "County", "state_fips", "county_fips"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    ba_columns = get_ba_columns(df.columns)
    if not ba_columns:
        raise ValueError("No annual BA columns were found in the BFS county file.")

    df["state_fips"] = df["state_fips"].astype(str).str.zfill(2)
    df["county_fips"] = df["county_fips"].astype(str).str.zfill(3)
    df["full_fips"] = df["state_fips"] + df["county_fips"]
    df = df[df["full_fips"].isin(BAY_AREA_COUNTIES)].copy()

    if df.empty:
        raise ValueError("No Bay Area counties were found in the supplied BFS file.")

    for col in ba_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    long_df = df[["full_fips", "County"] + ba_columns].melt(
        id_vars=["full_fips", "County"],
        var_name="year_col",
        value_name="applications",
    )
    long_df["year"] = long_df["year_col"].str[2:].astype(int)
    long_df["applications"] = pd.to_numeric(long_df["applications"], errors="coerce")
    long_df["county_name"] = long_df["full_fips"].map(BAY_AREA_COUNTIES)
    long_df = long_df.sort_values(["full_fips", "year"]).reset_index(drop=True)
    long_df["yoy_abs"] = long_df.groupby("full_fips")["applications"].diff()
    long_df["yoy_pct"] = long_df.groupby("full_fips")["applications"].pct_change() * 100.0
    long_df["regional_total"] = long_df.groupby("year")["applications"].transform("sum")
    long_df["share_pct"] = long_df["applications"] / long_df["regional_total"] * 100.0
    long_df["running_peak"] = long_df.groupby("full_fips")["applications"].cummax()
    long_df["drawdown_pct"] = (long_df["applications"] / long_df["running_peak"] - 1.0) * 100.0

    return long_df


def compute_cagr(first: float, last: float, years: int) -> float:
    if pd.isna(first) or pd.isna(last) or first <= 0 or last <= 0 or years <= 0:
        return np.nan
    return (last / first) ** (1.0 / years) - 1.0


def build_county_hazard_table(long_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for full_fips, group in long_df.groupby("full_fips"):
        group = group.sort_values("year").reset_index(drop=True)
        latest = group[group["year"] == group["year"].max()].iloc[0]
        medium_window = group[group["year"] >= latest["year"] - 5]
        cagr_5y = compute_cagr(
            medium_window.iloc[0]["applications"],
            medium_window.iloc[-1]["applications"],
            int(medium_window.iloc[-1]["year"] - medium_window.iloc[0]["year"]),
        )
        rows.append(
            {
                "full_fips": full_fips,
                "county_name": latest["county_name"],
                "latest_year": int(latest["year"]),
                "applications_latest": float(latest["applications"]),
                "share_latest_pct": float(latest["share_pct"]),
                "yoy_latest_abs": float(latest["yoy_abs"]),
                "yoy_latest_pct": float(latest["yoy_pct"]),
                "cagr_5y_pct": float(cagr_5y * 100.0),
                "yoy_volatility_pct_pts": float(group["yoy_pct"].dropna().std()),
                "max_drawdown_pct": float(group["drawdown_pct"].min()),
            }
        )

    result = pd.DataFrame(rows)
    result["drawdown_depth_pct"] = -result["max_drawdown_pct"]
    result["risk_recent_momentum"] = -result["yoy_latest_pct"]
    result["risk_medium_growth"] = -result["cagr_5y_pct"]
    result["risk_volatility"] = result["yoy_volatility_pct_pts"]
    result["risk_drawdown"] = result["drawdown_depth_pct"]

    risk_columns = [
        "risk_recent_momentum",
        "risk_medium_growth",
        "risk_volatility",
        "risk_drawdown",
    ]
    for column in risk_columns:
        std = result[column].std(ddof=0)
        if std == 0 or pd.isna(std):
            result[f"z_{column}"] = 0.0
        else:
            result[f"z_{column}"] = (result[column] - result[column].mean()) / std

    z_columns = [f"z_{column}" for column in risk_columns]
    result["hazard_proxy_raw"] = result[z_columns].mean(axis=1)
    minimum = result["hazard_proxy_raw"].min()
    maximum = result["hazard_proxy_raw"].max()
    if maximum == minimum:
        result["hazard_proxy_score_0_100"] = 0.0
    else:
        result["hazard_proxy_score_0_100"] = (
            (result["hazard_proxy_raw"] - minimum) / (maximum - minimum) * 100.0
        )

    return result.sort_values(
        ["hazard_proxy_score_0_100", "applications_latest"],
        ascending=[False, False],
    ).reset_index(drop=True)


def build_regional_diagnostics(long_df: pd.DataFrame) -> dict:
    regional = (
        long_df.groupby("year", as_index=False)["applications"]
        .sum()
        .rename(columns={"applications": "bay_area_applications"})
        .sort_values("year")
        .reset_index(drop=True)
    )
    regional["yoy_pct"] = regional["bay_area_applications"].pct_change() * 100.0
    regional["running_peak"] = regional["bay_area_applications"].cummax()
    regional["drawdown_pct"] = (
        regional["bay_area_applications"] / regional["running_peak"] - 1.0
    ) * 100.0

    latest_year = int(regional["year"].max())
    latest = regional[regional["year"] == latest_year].iloc[0]
    first = regional.iloc[0]
    year_span = int(latest["year"] - first["year"])
    cagr = compute_cagr(first["bay_area_applications"], latest["bay_area_applications"], year_span)

    latest_cross_section = long_df[long_df["year"] == latest_year].copy()
    shares = latest_cross_section["share_pct"] / 100.0

    return {
        "latest_year": latest_year,
        "bay_area_applications_latest": float(latest["bay_area_applications"]),
        "bay_area_yoy_latest_pct": float(latest["yoy_pct"]),
        "bay_area_cagr_full_sample": float(cagr * 100.0),
        "top3_share_latest_pct": float(latest_cross_section["share_pct"].nlargest(3).sum()),
        "hhi_latest": float((shares.pow(2).sum()) * 10000.0),
        "worst_drawdown_pct": float(regional["drawdown_pct"].min()),
    }


def write_outputs(hazard_table: pd.DataFrame, regional_diagnostics: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    hazard_table.to_csv(output_dir / "bay_area_hazard_proxy_table.csv", index=False)
    with (output_dir / "bay_area_hazard_proxy_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(regional_diagnostics, handle, indent=2)


def main() -> None:
    args = parse_args()
    long_df = load_bay_area_panel(args.bfs_county_file)
    hazard_table = build_county_hazard_table(long_df)
    regional_diagnostics = build_regional_diagnostics(long_df)
    write_outputs(hazard_table, regional_diagnostics, args.output_dir)
    print(f"Wrote hazard outputs to: {args.output_dir}")


if __name__ == "__main__":
    main()
