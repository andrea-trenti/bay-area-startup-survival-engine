#!/usr/bin/env python3
"""
Validate the source-acquisition inventory required by the Bay Area startup repository.

The validator is intentionally strict about canonical source-file naming for the
core Census and BLS artifacts and intentionally flexible about QCEW area
coverage, because independent replications may assemble different subsets of
area files while preserving the same public-data architecture.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from config import BAY_AREA_COUNTIES, SOURCE_MANIFEST


@dataclass
class ValidationReport:
    raw_dir: str
    core_files_present: dict[str, bool]
    bfs_monthly: dict[str, Any]
    bfs_county_annual: dict[str, Any]
    geography: dict[str, Any]
    qcew_inventory: dict[str, Any]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--raw-dir",
        default="data/raw",
        help="Directory containing source files acquired from the issuing institutions.",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs/validation",
        help="Directory where validation artifacts will be written.",
    )
    return parser.parse_args()


def ensure_core_files(raw_dir: Path) -> dict[str, bool]:
    return {name: (raw_dir / name).exists() for name in SOURCE_MANIFEST}


def summarize_bfs_monthly(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"present": False}
    df = pd.read_csv(path)
    month_cols = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    long_df = df.melt(
        id_vars=["sa", "naics_sector", "series", "geo", "year"],
        value_vars=month_cols,
        var_name="month",
        value_name="value",
    )
    long_df["value"] = pd.to_numeric(long_df["value"], errors="coerce")
    long_df = long_df.dropna(subset=["value"])
    return {
        "present": True,
        "rows": int(df.shape[0]),
        "geographies": int(df["geo"].nunique()),
        "series": sorted(df["series"].dropna().unique().tolist()),
        "years": [int(df["year"].min()), int(df["year"].max())],
        "latest_adjusted_ca_ba_ba": float(
            long_df.loc[
                (long_df["sa"] == "A")
                & (long_df["geo"] == "CA")
                & (long_df["series"] == "BA_BA")
                & (long_df["naics_sector"] == "TOTAL")
            ].sort_values(["year", "month"]).iloc[-1]["value"]
        ),
    }


def summarize_bfs_county_annual(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"present": False}
    df = pd.read_excel(path, sheet_name="County Data", header=2)
    df = df.rename(
        columns={
            df.columns[0]: "state_abbr",
            df.columns[1]: "county_name",
            df.columns[2]: "county_code",
            df.columns[3]: "state_fips",
            df.columns[4]: "county_fips",
        }
    )
    year_cols = [col for col in df.columns if isinstance(col, str) and col.startswith("BA")]
    for col in year_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["state_fips"] = pd.to_numeric(df["state_fips"], errors="coerce").astype("Int64").astype(str).str.zfill(2)
    df["county_fips"] = pd.to_numeric(df["county_fips"], errors="coerce").astype("Int64").astype(str).str.zfill(3)
    df["county_geoid"] = df["state_fips"] + df["county_fips"]

    bay_df = df[df["county_geoid"].isin(BAY_AREA_COUNTIES)].copy()
    return {
        "present": True,
        "rows": int(df.shape[0]),
        "year_range": [int(year_cols[0].replace("BA", "")), int(year_cols[-1].replace("BA", ""))],
        "bay_area_counties_found": sorted(bay_df["county_geoid"].unique().tolist()),
        "bay_area_total_2024": float(bay_df["BA2024"].sum()) if "BA2024" in bay_df else None,
        "bay_area_total_2023": float(bay_df["BA2023"].sum()) if "BA2023" in bay_df else None,
    }


def summarize_geography(list1_path: Path, area_titles_path: Path) -> dict[str, Any]:
    report: dict[str, Any] = {"list1_present": list1_path.exists(), "area_titles_present": area_titles_path.exists()}
    if list1_path.exists():
        list1 = pd.read_excel(list1_path, header=2)
        list1 = list1.rename(
            columns={
                "CBSA Code": "cbsa_code",
                "CSA Code": "csa_code",
                "CBSA Title": "cbsa_title",
                "County/County Equivalent": "county_name",
                "State Name": "state_name",
                "FIPS State Code": "state_fips",
                "FIPS County Code": "county_fips",
            }
        )
        if {"state_fips", "county_fips"}.issubset(list1.columns):
            list1["state_fips"] = pd.to_numeric(list1["state_fips"], errors="coerce").astype("Int64").astype(str).str.zfill(2)
            list1["county_fips"] = pd.to_numeric(list1["county_fips"], errors="coerce").astype("Int64").astype(str).str.zfill(3)
            list1["county_geoid"] = list1["state_fips"] + list1["county_fips"]
            bay = list1[list1["county_geoid"].isin(BAY_AREA_COUNTIES)]
            report["bay_area_cbsa_rows"] = int(bay.shape[0])
            report["bay_area_cbsa_titles"] = sorted(bay["cbsa_title"].dropna().astype(str).unique().tolist())
            report["bay_area_csa_codes"] = sorted(bay["csa_code"].dropna().astype(str).unique().tolist())
    if area_titles_path.exists():
        area = pd.read_csv(area_titles_path, dtype=str)
        bay_area_codes = ["C4186", "C4194", "CS488", "06001", "06013", "06041", "06055", "06075", "06081", "06085", "06095", "06097"]
        subset = area[area["area_fips"].isin(bay_area_codes)]
        report["area_titles_matches"] = subset.to_dict(orient="records")
    return report


def summarize_qcew_inventory(raw_dir: Path) -> dict[str, Any]:
    pattern = re.compile(r"^20\d{2}\.annual .*\.csv$")
    files = sorted([path for path in raw_dir.iterdir() if path.is_file() and pattern.match(path.name)])
    summary: dict[str, Any] = {
        "files_found": len(files),
        "years_present": sorted({path.name[:4] for path in files}),
        "bay_area_county_files_present": [],
        "bay_area_county_files_missing": sorted(BAY_AREA_COUNTIES),
    }
    if not files:
        return summary

    discovered_codes: set[str] = set()
    samples: list[dict[str, Any]] = []
    for path in files:
        try:
            frame = pd.read_csv(path, nrows=3, dtype={"area_fips": str})
            area_code = str(frame.iloc[0]["area_fips"]).zfill(5)
            discovered_codes.add(area_code)
            if len(samples) < 8:
                samples.append(
                    {
                        "file": path.name,
                        "area_fips": area_code,
                        "area_title": str(frame.iloc[0].get("area_title", "")),
                        "year": int(frame.iloc[0].get("year", path.name[:4])),
                    }
                )
        except Exception as exc:  # pragma: no cover
            if len(samples) < 8:
                samples.append({"file": path.name, "read_error": str(exc)})

    present = sorted(code for code in BAY_AREA_COUNTIES if code in discovered_codes)
    missing = sorted(code for code in BAY_AREA_COUNTIES if code not in discovered_codes)
    summary["bay_area_county_files_present"] = present
    summary["bay_area_county_files_missing"] = missing
    summary["sample_inventory"] = samples
    return summary


def main() -> None:
    args = parse_args()
    raw_dir = Path(args.raw_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = ValidationReport(
        raw_dir=str(raw_dir.resolve()),
        core_files_present=ensure_core_files(raw_dir),
        bfs_monthly=summarize_bfs_monthly(raw_dir / "bfs_monthly.csv"),
        bfs_county_annual=summarize_bfs_county_annual(raw_dir / "bfs_county_apps_annual.xlsx"),
        geography=summarize_geography(raw_dir / "list1_2023.xlsx", raw_dir / "area-titles-csv.csv"),
        qcew_inventory=summarize_qcew_inventory(raw_dir),
    )

    json_path = output_dir / "public_data_validation_report.json"
    json_path.write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")

    print(f"[ok] wrote validation report to {json_path}")


if __name__ == "__main__":
    main()
