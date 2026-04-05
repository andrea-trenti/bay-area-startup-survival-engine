"""
Build a Bay Area startup foundation panel from the processed public-data layer.

The script is designed for modular replication and explicit coverage diagnostics.
In particular, Bay Area QCEW wage/employment data may be absent even if QCEW files
from other states are present. The script therefore produces:
    1. Bay Area county business-application panel
    2. Latest California/U.S. monthly BFS snapshot
    3. QCEW coverage diagnostics for Bay Area counties
    4. A compact JSON summary for downstream Markdown or chart generation
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, List

import pandas as pd

from config import BAY_AREA_COUNTIES


LOGGER = logging.getLogger("build_bay_area_foundation_panel")

def configure_logging(verbose: bool = False) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Required processed file not found: {path}")
    return pd.read_csv(path)


def ensure_output_dir(repo_root: Path) -> Path:
    output_dir = repo_root / "outputs" / "bay_area_foundation"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def build_application_panel(bfs_county: pd.DataFrame) -> pd.DataFrame:
    df = bfs_county.copy()
    df["county_code"] = df["county_code"].astype(str).str.zfill(5)
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["business_applications"] = pd.to_numeric(df["business_applications"], errors="coerce")

    bay = df[df["county_code"].isin(BAY_AREA_COUNTIES)].copy()
    bay["county_name"] = bay["county_code"].map(BAY_AREA_COUNTIES)
    bay = bay.sort_values(["county_name", "year"]).reset_index(drop=True)
    bay["applications_yoy_abs"] = bay.groupby("county_code")["business_applications"].diff()
    bay["applications_yoy_pct"] = bay.groupby("county_code")["business_applications"].pct_change() * 100.0

    regional = (
        bay.groupby("year", as_index=False)["business_applications"]
        .sum()
        .rename(columns={"business_applications": "bay_area_total_business_applications"})
        .sort_values("year")
        .reset_index(drop=True)
    )
    regional["bay_area_yoy_abs"] = regional["bay_area_total_business_applications"].diff()
    regional["bay_area_yoy_pct"] = regional["bay_area_total_business_applications"].pct_change() * 100.0

    merged = bay.merge(regional, on="year", how="left")
    merged["county_share_of_bay_area_pct"] = (
        merged["business_applications"] / merged["bay_area_total_business_applications"] * 100.0
    )
    return merged


def build_monthly_snapshot(bfs_monthly: pd.DataFrame) -> pd.DataFrame:
    df = bfs_monthly.copy()
    df["period"] = pd.to_datetime(df["period"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    filtered = df[
        (df["naics_sector"] == "TOTAL")
        & (df["seasonal_adjustment"] == "seasonally_adjusted")
        & (df["series"].isin(["BA_BA", "BF_PBF4Q", "BF_PBF8Q"]))
        & (df["geo"].isin(["US", "CA"]))
    ].copy()

    non_null = filtered.dropna(subset=["value"]).copy()
    latest_period = non_null["period"].max()
    snapshot = non_null[non_null["period"] == latest_period].copy()
    snapshot = snapshot.sort_values(["geo", "series"]).reset_index(drop=True)
    snapshot["latest_period"] = latest_period
    return snapshot


def build_qcew_coverage(qcew: pd.DataFrame, area_titles: pd.DataFrame) -> pd.DataFrame:
    area_titles = area_titles.copy()
    area_titles["area_fips"] = area_titles["area_fips"].astype(str).str.zfill(5)

    qcew = qcew.copy()
    if qcew.empty:
        observed = set()
    else:
        qcew["area_fips"] = qcew["area_fips"].astype(str).str.zfill(5)
        observed = set(qcew["area_fips"].dropna().unique())

    coverage_rows: List[Dict[str, object]] = []
    for county_code, county_name in BAY_AREA_COUNTIES.items():
        matched_title = area_titles.loc[area_titles["area_fips"] == county_code, "area_title"]
        coverage_rows.append(
            {
                "area_fips": county_code,
                "county_name": county_name,
                "area_title_from_crosswalk": matched_title.iloc[0] if not matched_title.empty else county_name,
                "qcew_file_present_for_area": county_code in observed,
            }
        )

    coverage = pd.DataFrame(coverage_rows).sort_values("area_fips").reset_index(drop=True)
    return coverage


def build_summary(application_panel: pd.DataFrame, monthly_snapshot: pd.DataFrame, qcew_coverage: pd.DataFrame) -> Dict[str, object]:
    latest_year = int(application_panel["year"].dropna().max())
    latest = application_panel[application_panel["year"] == latest_year].copy().sort_values("business_applications", ascending=False)

    bay_total = float(latest["bay_area_total_business_applications"].iloc[0])
    summary = {
        "latest_application_year": latest_year,
        "bay_area_total_business_applications": int(round(bay_total)),
        "top_counties_latest_year": [
            {"county_name": row["county_name"], "business_applications": int(row["business_applications"])}
            for _, row in latest.head(5).iterrows()
        ],
        "top_two_county_share_pct": round(float(latest.head(2)["business_applications"].sum() / bay_total * 100.0), 2),
        "qcew_bay_area_area_files_present": int(qcew_coverage["qcew_file_present_for_area"].sum()),
        "qcew_bay_area_area_files_missing": int((~qcew_coverage["qcew_file_present_for_area"]).sum()),
        "monthly_snapshot": [
            {
                "geo": row["geo"],
                "series": row["series"],
                "period": str(pd.Timestamp(row["latest_period"]).date()),
                "value": None if pd.isna(row["value"]) else int(row["value"]),
            }
            for _, row in monthly_snapshot.iterrows()
        ],
    }
    return summary


def write_outputs(repo_root: Path, application_panel: pd.DataFrame, monthly_snapshot: pd.DataFrame, qcew_coverage: pd.DataFrame, summary: Dict[str, object]) -> None:
    output_dir = ensure_output_dir(repo_root)

    application_panel.to_csv(output_dir / "bay_area_county_business_applications.csv", index=False)
    monthly_snapshot.to_csv(output_dir / "california_us_latest_bfs_snapshot.csv", index=False)
    qcew_coverage.to_csv(output_dir / "bay_area_qcew_coverage.csv", index=False)
    (output_dir / "bay_area_foundation_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    LOGGER.info("Output directory: %s", output_dir)
    LOGGER.info("Wrote Bay Area foundation outputs successfully.")


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Bay Area startup foundation panel from processed data.")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1], help="Repository root path.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging.")
    return parser


def main() -> None:
    parser = build_argument_parser()
    args = parser.parse_args()
    configure_logging(verbose=args.verbose)

    processed_dir = args.repo_root / "data" / "processed"
    bfs_county = load_csv(processed_dir / "bfs_county_annual_long.csv")
    bfs_monthly = load_csv(processed_dir / "bfs_monthly_long.csv")
    qcew = load_csv(processed_dir / "qcew_area_panel.csv")
    area_titles = load_csv(processed_dir / "area_titles_clean.csv")

    application_panel = build_application_panel(bfs_county)
    monthly_snapshot = build_monthly_snapshot(bfs_monthly)
    qcew_coverage = build_qcew_coverage(qcew, area_titles)
    summary = build_summary(application_panel, monthly_snapshot, qcew_coverage)

    write_outputs(args.repo_root, application_panel, monthly_snapshot, qcew_coverage, summary)

    if summary["qcew_bay_area_area_files_present"] == 0:
        LOGGER.warning(
            "No Bay Area QCEW area files detected in the acquisition layer. "
            "The foundation layer was built successfully and the labor-context layer remains conditional on the corresponding Bay Area QCEW source family."
        )


if __name__ == "__main__":
    main()
