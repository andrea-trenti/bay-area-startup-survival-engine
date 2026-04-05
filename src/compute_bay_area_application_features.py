#!/usr/bin/env python3
"""
Compute Bay Area business-application features from public Census/BLS inputs.

Outputs
-------
- bay_area_county_application_features.csv
- bay_area_region_annual_summary.csv
- california_monthly_bfs_benchmark.csv
- bay_area_feature_build_metadata.json

The script is designed to run even when Bay Area QCEW county files are not included.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from config import BAY_AREA_COUNTIES

MONTH_ORDER = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", default="data/raw", help="Directory containing raw source files.")
    parser.add_argument("--output-dir", default="outputs/research_ready", help="Directory for derived analytical outputs.")
    return parser.parse_args()


def load_bfs_county_annual(path: Path) -> pd.DataFrame:
    frame = pd.read_excel(path, sheet_name="County Data", header=2)
    frame = frame.rename(
        columns={
            frame.columns[0]: "state_abbr",
            frame.columns[1]: "county_name",
            frame.columns[2]: "county_code",
            frame.columns[3]: "state_fips",
            frame.columns[4]: "county_fips",
        }
    )
    year_cols = [col for col in frame.columns if isinstance(col, str) and col.startswith("BA")]
    for col in year_cols:
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    frame["state_fips"] = frame["state_fips"].astype(str).str.zfill(2)
    frame["county_fips"] = frame["county_fips"].astype(str).str.zfill(3)
    frame["county_geoid"] = frame["state_fips"] + frame["county_fips"]
    return frame


def build_county_feature_table(frame: pd.DataFrame) -> pd.DataFrame:
    bay = frame[frame["county_geoid"].isin(BAY_AREA_COUNTIES)].copy()
    year_cols = sorted([col for col in bay.columns if isinstance(col, str) and col.startswith("BA")], key=lambda x: int(x.replace("BA", "")))

    long = bay.melt(
        id_vars=["county_geoid", "county_name"],
        value_vars=year_cols,
        var_name="series_year",
        value_name="business_applications",
    )
    long["year"] = long["series_year"].str.replace("BA", "", regex=False).astype(int)
    long = long.drop(columns=["series_year"]).sort_values(["county_geoid", "year"]).reset_index(drop=True)

    long["business_applications"] = pd.to_numeric(long["business_applications"], errors="coerce")
    regional_total = long.groupby("year", as_index=False)["business_applications"].sum().rename(columns={"business_applications": "bay_area_total"})
    long = long.merge(regional_total, on="year", how="left")
    long["county_share"] = long["business_applications"] / long["bay_area_total"]
    long["yoy_growth"] = long.groupby("county_geoid")["business_applications"].pct_change()
    long["three_year_cagr"] = (
        long.groupby("county_geoid")["business_applications"].transform(lambda s: (s / s.shift(3)) ** (1 / 3) - 1)
    )
    long["five_year_cagr"] = (
        long.groupby("county_geoid")["business_applications"].transform(lambda s: (s / s.shift(5)) ** (1 / 5) - 1)
    )

    base_2005 = long.loc[long["year"] == 2005, ["county_geoid", "business_applications"]].rename(columns={"business_applications": "base_2005"})
    long = long.merge(base_2005, on="county_geoid", how="left")
    long["growth_vs_2005"] = long["business_applications"] / long["base_2005"] - 1.0

    share_2005 = long.loc[long["year"] == 2005, ["county_geoid", "county_share"]].rename(columns={"county_share": "county_share_2005"})
    long = long.merge(share_2005, on="county_geoid", how="left")
    long["share_change_vs_2005_pp"] = (long["county_share"] - long["county_share_2005"]) * 100

    return long


def build_region_summary(frame: pd.DataFrame) -> pd.DataFrame:
    bay = frame[frame["county_geoid"].isin(BAY_AREA_COUNTIES)].copy()
    ca = frame[frame["state_abbr"] == "CA"].copy()
    year_cols = sorted([col for col in bay.columns if isinstance(col, str) and col.startswith("BA")], key=lambda x: int(x.replace("BA", "")))

    rows: list[dict[str, Any]] = []
    for col in year_cols:
        year = int(col.replace("BA", ""))
        county_values = bay[["county_geoid", "county_name", col]].rename(columns={col: "value"}).dropna()
        bay_total = float(county_values["value"].sum())
        ca_total = float(pd.to_numeric(ca[col], errors="coerce").sum())
        shares = county_values["value"] / bay_total if bay_total else np.nan
        hhi = float((shares**2).sum()) if bay_total else np.nan
        top3_share = float(shares.sort_values(ascending=False).head(3).sum()) if bay_total else np.nan
        rows.append(
            {
                "year": year,
                "bay_area_total_business_applications": bay_total,
                "california_total_business_applications": ca_total,
                "bay_area_share_of_california": bay_total / ca_total if ca_total else np.nan,
                "county_hhi": hhi,
                "effective_county_count": (1.0 / hhi) if hhi else np.nan,
                "top3_county_share": top3_share,
            }
        )

    summary = pd.DataFrame(rows).sort_values("year").reset_index(drop=True)
    summary["yoy_growth"] = summary["bay_area_total_business_applications"].pct_change()
    summary["three_year_cagr"] = (summary["bay_area_total_business_applications"] / summary["bay_area_total_business_applications"].shift(3)) ** (1 / 3) - 1
    summary["five_year_cagr"] = (summary["bay_area_total_business_applications"] / summary["bay_area_total_business_applications"].shift(5)) ** (1 / 5) - 1
    summary["bay_area_share_change_pp"] = summary["bay_area_share_of_california"].diff() * 100
    return summary


def build_monthly_benchmark(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    month_cols = list(MONTH_ORDER)
    long = frame.melt(
        id_vars=["sa", "naics_sector", "series", "geo", "year"],
        value_vars=month_cols,
        var_name="month",
        value_name="value",
    )
    long["value"] = pd.to_numeric(long["value"], errors="coerce")
    long = long.dropna(subset=["value"])
    long["month_num"] = long["month"].map(MONTH_ORDER)
    long["date"] = pd.to_datetime(dict(year=long["year"], month=long["month_num"], day=1))

    subset = long[
        (long["sa"] == "A")
        & (long["naics_sector"] == "TOTAL")
        & (long["series"] == "BA_BA")
        & (long["geo"].isin(["CA", "US"]))
    ].copy()

    pivot = subset.pivot_table(index="date", columns="geo", values="value", aggfunc="first").reset_index()
    pivot = pivot.rename(columns={"CA": "california_adjusted_business_applications", "US": "us_adjusted_business_applications"})
    pivot["california_share_of_us"] = pivot["california_adjusted_business_applications"] / pivot["us_adjusted_business_applications"]
    pivot["california_yoy_growth"] = pivot["california_adjusted_business_applications"].pct_change(12)
    pivot["us_yoy_growth"] = pivot["us_adjusted_business_applications"].pct_change(12)
    pivot["year"] = pivot["date"].dt.year
    pivot["month"] = pivot["date"].dt.month
    return pivot.sort_values("date").reset_index(drop=True)


def main() -> None:
    args = parse_args()
    raw_dir = Path(args.raw_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    county_frame = load_bfs_county_annual(raw_dir / "bfs_county_apps_annual.xlsx")
    county_features = build_county_feature_table(county_frame)
    region_summary = build_region_summary(county_frame)
    monthly_benchmark = build_monthly_benchmark(raw_dir / "bfs_monthly.csv")

    county_path = output_dir / "bay_area_county_application_features.csv"
    region_path = output_dir / "bay_area_region_annual_summary.csv"
    monthly_path = output_dir / "california_monthly_bfs_benchmark.csv"

    county_features.to_csv(county_path, index=False)
    region_summary.to_csv(region_path, index=False)
    monthly_benchmark.to_csv(monthly_path, index=False)

    metadata = {
        "raw_dir": str(raw_dir.resolve()),
        "files_written": [str(county_path), str(region_path), str(monthly_path)],
        "bay_area_counties": BAY_AREA_COUNTIES,
        "latest_region_year": int(region_summary["year"].max()),
        "latest_region_total": float(region_summary.iloc[-1]["bay_area_total_business_applications"]),
        "latest_region_share_of_california": float(region_summary.iloc[-1]["bay_area_share_of_california"]),
        "latest_ca_month": str(monthly_benchmark.iloc[-1]["date"].date()),
        "latest_ca_adjusted_business_applications": float(monthly_benchmark.iloc[-1]["california_adjusted_business_applications"]),
    }

    metadata_path = output_dir / "bay_area_feature_build_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"[ok] wrote {county_path}")
    print(f"[ok] wrote {region_path}")
    print(f"[ok] wrote {monthly_path}")
    print(f"[ok] wrote {metadata_path}")


if __name__ == "__main__":
    main()
