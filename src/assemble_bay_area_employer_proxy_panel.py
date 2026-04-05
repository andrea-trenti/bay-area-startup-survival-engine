#!/usr/bin/env python3
"""
Assemble a Bay Area employer-formation proxy panel from public Census files.

This script bridges county-level annual business applications to a state-level
employer-formation environment using California's monthly Business Formation
Statistics (BFS). The key output is *not* an official startup count. It is a
research-grade proxy intended for comparative analysis, scenario design, and
documentation.

Required raw inputs
-------------------
- bfs_county_apps_annual.xlsx
- bfs_monthly.csv

Optional supporting inputs
--------------------------
- list1_2023.xlsx
- area-titles-csv.csv

Outputs
-------
- outputs/modeling/bay_area_county_employer_proxy_panel.csv
- outputs/modeling/bay_area_region_employer_proxy_summary.csv
- outputs/modeling/california_bfs_conversion_bridge.csv
- outputs/modeling/bay_area_employer_proxy_metadata.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable

import numpy as np
import pandas as pd

from config import BAY_AREA_COUNTIES

MONTH_ORDER: Dict[str, int] = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a Bay Area employer proxy panel.")
    parser.add_argument("--raw-dir", default="data/raw", help="Directory containing raw input files.")
    parser.add_argument("--output-dir", default="outputs/modeling", help="Directory for derived outputs.")
    return parser.parse_args()


def _normalize_fips(value: object, width: int) -> str:
    text = "" if pd.isna(value) else str(value).strip()
    text = text.replace(".0", "")
    digits = "".join(ch for ch in text if ch.isdigit())
    return digits.zfill(width)


def load_county_business_applications(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing required annual county workbook: {path}")

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
    frame["state_fips"] = frame["state_fips"].apply(lambda x: _normalize_fips(x, 2))
    frame["county_fips"] = frame["county_fips"].apply(lambda x: _normalize_fips(x, 3))
    frame["county_geoid"] = frame["state_fips"] + frame["county_fips"]

    year_cols = sorted(
        [col for col in frame.columns if isinstance(col, str) and col.startswith("BA")],
        key=lambda x: int(x.replace("BA", "")),
    )
    for col in year_cols:
        frame[col] = pd.to_numeric(frame[col], errors="coerce")

    long = frame[frame["county_geoid"].isin(BAY_AREA_COUNTIES)].melt(
        id_vars=["state_abbr", "county_name", "county_geoid"],
        value_vars=year_cols,
        var_name="series_year",
        value_name="business_applications_obs",
    )
    long["year"] = long["series_year"].str.replace("BA", "", regex=False).astype(int)
    long = long.drop(columns=["series_year"]).sort_values(["county_geoid", "year"]).reset_index(drop=True)

    long["county_share_obs"] = (
        long["business_applications_obs"]
        / long.groupby("year")["business_applications_obs"].transform("sum")
    )
    long["county_yoy_growth"] = long.groupby("county_geoid")["business_applications_obs"].pct_change()
    long["county_three_year_cagr"] = (
        long.groupby("county_geoid")["business_applications_obs"]
        .transform(lambda s: (s / s.shift(3)) ** (1 / 3) - 1)
    )
    return long


def load_california_conversion_bridge(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing required monthly BFS file: {path}")

    frame = pd.read_csv(path)
    long = frame.melt(
        id_vars=["sa", "naics_sector", "series", "geo", "year"],
        value_vars=list(MONTH_ORDER),
        var_name="month_name",
        value_name="value",
    )
    long["value"] = pd.to_numeric(long["value"], errors="coerce")
    long = long.dropna(subset=["value"]).copy()
    long["month"] = long["month_name"].map(MONTH_ORDER)
    long["date"] = pd.to_datetime(dict(year=long["year"], month=long["month"], day=1))

    subset = long[
        (long["sa"] == "A")
        & (long["naics_sector"] == "TOTAL")
        & (long["geo"] == "CA")
        & (long["series"].isin(["BA_BA", "BF_BF4Q", "BF_PBF4Q", "BF_SBF4Q"]))
    ].copy()

    pivot = subset.pivot_table(index="date", columns="series", values="value", aggfunc="first").reset_index()
    required_cols = {"BA_BA", "BF_SBF4Q"}
    missing = required_cols.difference(pivot.columns)
    if missing:
        raise ValueError(f"Monthly BFS file does not contain required series: {sorted(missing)}")

    pivot["year"] = pivot["date"].dt.year
    pivot["conversion_ratio_spliced"] = pivot["BF_SBF4Q"] / pivot["BA_BA"]
    pivot["conversion_ratio_actual"] = pivot.get("BF_BF4Q", pd.Series(index=pivot.index, dtype=float)) / pivot["BA_BA"]
    pivot["conversion_ratio_projected"] = pivot.get("BF_PBF4Q", pd.Series(index=pivot.index, dtype=float)) / pivot["BA_BA"]

    annual = (
        pivot.groupby("year", as_index=False)
        .agg(
            california_monthly_ba_avg=("BA_BA", "mean"),
            california_monthly_sbf4q_avg=("BF_SBF4Q", "mean"),
            california_monthly_bf4q_avg=("BF_BF4Q", "mean"),
            california_monthly_pbf4q_avg=("BF_PBF4Q", "mean"),
            california_conversion_ratio_spliced=("conversion_ratio_spliced", "mean"),
            california_conversion_ratio_spliced_std=("conversion_ratio_spliced", "std"),
            california_conversion_ratio_actual=("conversion_ratio_actual", "mean"),
            california_conversion_ratio_projected=("conversion_ratio_projected", "mean"),
            months_observed=("date", "count"),
        )
        .sort_values("year")
        .reset_index(drop=True)
    )

    annual["conversion_ratio_lower_band"] = (
        annual["california_conversion_ratio_spliced"]
        - annual["california_conversion_ratio_spliced_std"].fillna(0.0)
    ).clip(lower=0.0)
    annual["conversion_ratio_upper_band"] = (
        annual["california_conversion_ratio_spliced"]
        + annual["california_conversion_ratio_spliced_std"].fillna(0.0)
    ).clip(lower=0.0)
    annual["conversion_ratio_yoy_change_bp"] = (
        annual["california_conversion_ratio_spliced"].diff() * 10000.0
    )
    return annual


def build_proxy_panel(
    county_applications: pd.DataFrame,
    california_bridge: pd.DataFrame,
) -> pd.DataFrame:
    panel = county_applications.merge(california_bridge, on="year", how="left", validate="many_to_one")
    panel["employer_formations_proxy"] = (
        panel["business_applications_obs"] * panel["california_conversion_ratio_spliced"]
    )
    panel["employer_formations_proxy_lower"] = (
        panel["business_applications_obs"] * panel["conversion_ratio_lower_band"]
    )
    panel["employer_formations_proxy_upper"] = (
        panel["business_applications_obs"] * panel["conversion_ratio_upper_band"]
    )
    panel["proxy_per_100_applications"] = panel["california_conversion_ratio_spliced"] * 100.0
    panel["regional_proxy_share"] = (
        panel["employer_formations_proxy"]
        / panel.groupby("year")["employer_formations_proxy"].transform("sum")
    )
    panel["regional_proxy_share_change_pp"] = (
        panel.groupby("county_geoid")["regional_proxy_share"].diff() * 100.0
    )
    panel["county_share_change_pp"] = (
        panel.groupby("county_geoid")["county_share_obs"].diff() * 100.0
    )
    panel["business_applications_vs_2005"] = (
        panel["business_applications_obs"]
        / panel.groupby("county_geoid")["business_applications_obs"].transform("first")
        - 1.0
    )
    return panel.sort_values(["county_geoid", "year"]).reset_index(drop=True)


def build_region_summary(panel: pd.DataFrame) -> pd.DataFrame:
    def _hhi(values: Iterable[float]) -> float:
        arr = np.asarray(list(values), dtype=float)
        return float(np.square(arr).sum()) if len(arr) else np.nan

    grouped = (
        panel.groupby("year", as_index=False)
        .agg(
            bay_area_business_applications_obs=("business_applications_obs", "sum"),
            bay_area_employer_formations_proxy=("employer_formations_proxy", "sum"),
            bay_area_employer_formations_proxy_lower=("employer_formations_proxy_lower", "sum"),
            bay_area_employer_formations_proxy_upper=("employer_formations_proxy_upper", "sum"),
            california_conversion_ratio_spliced=("california_conversion_ratio_spliced", "first"),
        )
        .sort_values("year")
        .reset_index(drop=True)
    )

    hhi_rows = []
    for year, frame in panel.groupby("year"):
        shares = frame["county_share_obs"].fillna(0.0)
        proxy_shares = frame["regional_proxy_share"].fillna(0.0)
        hhi_rows.append(
            {
                "year": int(year),
                "county_hhi_obs": _hhi(shares),
                "county_effective_count_obs": 1.0 / _hhi(shares) if _hhi(shares) > 0 else np.nan,
                "proxy_hhi": _hhi(proxy_shares),
                "proxy_effective_count": 1.0 / _hhi(proxy_shares) if _hhi(proxy_shares) > 0 else np.nan,
                "top3_county_share_obs": float(np.sort(shares.to_numpy())[::-1][:3].sum()),
                "top3_proxy_share": float(np.sort(proxy_shares.to_numpy())[::-1][:3].sum()),
            }
        )

    hhi = pd.DataFrame(hhi_rows)
    summary = grouped.merge(hhi, on="year", how="left", validate="one_to_one")
    summary["applications_yoy_growth"] = summary["bay_area_business_applications_obs"].pct_change()
    summary["proxy_yoy_growth"] = summary["bay_area_employer_formations_proxy"].pct_change()
    summary["applications_vs_2005"] = (
        summary["bay_area_business_applications_obs"] / summary.loc[summary["year"] == summary["year"].min(), "bay_area_business_applications_obs"].iloc[0] - 1.0
    )
    summary["proxy_vs_2005"] = (
        summary["bay_area_employer_formations_proxy"] / summary.loc[summary["year"] == summary["year"].min(), "bay_area_employer_formations_proxy"].iloc[0] - 1.0
    )
    return summary.sort_values("year").reset_index(drop=True)


def main() -> None:
    args = parse_args()
    raw_dir = Path(args.raw_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    county_applications = load_county_business_applications(raw_dir / "bfs_county_apps_annual.xlsx")
    california_bridge = load_california_conversion_bridge(raw_dir / "bfs_monthly.csv")
    proxy_panel = build_proxy_panel(county_applications, california_bridge)
    region_summary = build_region_summary(proxy_panel)

    county_path = output_dir / "bay_area_county_employer_proxy_panel.csv"
    region_path = output_dir / "bay_area_region_employer_proxy_summary.csv"
    bridge_path = output_dir / "california_bfs_conversion_bridge.csv"
    metadata_path = output_dir / "bay_area_employer_proxy_metadata.json"

    proxy_panel.to_csv(county_path, index=False)
    region_summary.to_csv(region_path, index=False)
    california_bridge.to_csv(bridge_path, index=False)

    latest_year = int(region_summary["year"].max())
    latest_region = region_summary.loc[region_summary["year"] == latest_year].iloc[0]
    latest_counties = (
        proxy_panel.loc[proxy_panel["year"] == latest_year, ["county_name", "employer_formations_proxy"]]
        .sort_values("employer_formations_proxy", ascending=False)
        .head(3)
    )

    metadata = {
        "raw_dir": str(raw_dir.resolve()),
        "output_dir": str(output_dir.resolve()),
        "latest_year": latest_year,
        "latest_bay_area_applications_obs": float(latest_region["bay_area_business_applications_obs"]),
        "latest_bay_area_employer_formations_proxy": float(latest_region["bay_area_employer_formations_proxy"]),
        "latest_california_conversion_ratio_spliced": float(latest_region["california_conversion_ratio_spliced"]),
        "latest_top3_counties_by_proxy": latest_counties.to_dict(orient="records"),
        "county_count": len(BAY_AREA_COUNTIES),
        "note": "Employer formations are estimated proxies derived from county applications and California monthly BFS conversion ratios.",
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"[ok] wrote {county_path}")
    print(f"[ok] wrote {region_path}")
    print(f"[ok] wrote {bridge_path}")
    print(f"[ok] wrote {metadata_path}")


if __name__ == "__main__":
    main()
