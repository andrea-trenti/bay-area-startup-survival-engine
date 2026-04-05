"""
Detect regional turning points and county rank transitions in the Bay Area
annual business-applications series.

The script uses a threshold rule on the change in annual growth to identify
large regime breaks. It is intended for analytical diagnostics, not formal
structural-break econometrics.
"""

from __future__ import annotations

import argparse
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
        help="Directory where regime-shift outputs will be written.",
    )
    parser.add_argument(
        "--threshold-pp",
        type=float,
        default=10.0,
        help="Absolute percentage-point change in YoY growth required to flag a regime break.",
    )
    return parser.parse_args()


def get_ba_columns(columns: Iterable[str]) -> list[str]:
    return [str(col) for col in columns if str(col).startswith("BA")]


def load_long_panel(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"BFS county file not found: {path}")

    df = pd.read_excel(path, header=2, dtype=str)
    required = {"County", "state_fips", "county_fips"}
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
    return long_df


def build_regional_series(long_df: pd.DataFrame) -> pd.DataFrame:
    regional = (
        long_df.groupby("year", as_index=False)["applications"]
        .sum()
        .rename(columns={"applications": "bay_area_applications"})
        .sort_values("year")
        .reset_index(drop=True)
    )
    regional["yoy_abs"] = regional["bay_area_applications"].diff()
    regional["yoy_pct"] = regional["bay_area_applications"].pct_change() * 100.0
    regional["yoy_change_pp"] = regional["yoy_pct"].diff()
    regional["running_peak"] = regional["bay_area_applications"].cummax()
    regional["drawdown_pct"] = (
        regional["bay_area_applications"] / regional["running_peak"] - 1.0
    ) * 100.0
    return regional


def build_regime_shift_table(regional: pd.DataFrame, threshold_pp: float) -> pd.DataFrame:
    flagged = regional[regional["yoy_change_pp"].abs() >= threshold_pp].copy()
    flagged["direction"] = np.where(flagged["yoy_change_pp"] >= 0, "positive_break", "negative_break")
    flagged["severity"] = pd.cut(
        flagged["yoy_change_pp"].abs(),
        bins=[threshold_pp, 15.0, 25.0, np.inf],
        labels=["material", "strong", "extreme"],
        include_lowest=True,
        right=False,
    )
    return flagged.reset_index(drop=True)


def build_cycle_segments(regional: pd.DataFrame) -> pd.DataFrame:
    segments = regional[["year", "bay_area_applications", "yoy_pct", "drawdown_pct"]].copy()
    segments["cycle_state"] = np.select(
        [segments["yoy_pct"] > 0, segments["yoy_pct"] < 0],
        ["expansion", "contraction"],
        default="base_year",
    )
    segments["peak_status"] = np.where(segments["drawdown_pct"] < 0, "below_peak", "at_peak")
    return segments


def build_rank_transition_table(long_df: pd.DataFrame) -> pd.DataFrame:
    first_year = int(long_df["year"].min())
    latest_year = int(long_df["year"].max())

    first = (
        long_df[long_df["year"] == first_year][["full_fips", "county_name", "applications"]]
        .sort_values("applications", ascending=False)
        .reset_index(drop=True)
    )
    first["rank_first_year"] = first.index + 1
    first = first.rename(columns={"applications": f"applications_{first_year}"})

    latest = (
        long_df[long_df["year"] == latest_year][["full_fips", "applications"]]
        .sort_values("applications", ascending=False)
        .reset_index(drop=True)
    )
    latest["rank_latest_year"] = latest.index + 1
    latest = latest.rename(columns={"applications": f"applications_{latest_year}"})

    merged = first.merge(latest, on="full_fips", how="left")
    merged["rank_change"] = merged["rank_first_year"] - merged["rank_latest_year"]
    return merged.sort_values(["rank_latest_year", f"applications_{latest_year}"], ascending=[True, False])


def write_outputs(
    regional: pd.DataFrame,
    regime_shifts: pd.DataFrame,
    cycle_segments: pd.DataFrame,
    rank_transitions: pd.DataFrame,
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    regional.to_csv(output_dir / "bay_area_regional_cycle_series.csv", index=False)
    regime_shifts.to_csv(output_dir / "bay_area_regime_shift_events.csv", index=False)
    cycle_segments.to_csv(output_dir / "bay_area_cycle_segments.csv", index=False)
    rank_transitions.to_csv(output_dir / "bay_area_county_rank_transitions.csv", index=False)


def main() -> None:
    args = parse_args()
    long_df = load_long_panel(args.bfs_county_file)
    regional = build_regional_series(long_df)
    regime_shifts = build_regime_shift_table(regional, threshold_pp=args.threshold_pp)
    cycle_segments = build_cycle_segments(regional)
    rank_transitions = build_rank_transition_table(long_df)
    write_outputs(regional, regime_shifts, cycle_segments, rank_transitions, args.output_dir)
    print(f"Wrote regime-shift outputs to: {args.output_dir}")


if __name__ == "__main__":
    main()
