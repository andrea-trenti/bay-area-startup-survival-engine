"""Shared repository configuration for geographic scope, paths, and source manifest."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = REPO_ROOT / "outputs"

BAY_AREA_COUNTIES: dict[str, str] = {
    "06001": "Alameda County",
    "06013": "Contra Costa County",
    "06041": "Marin County",
    "06055": "Napa County",
    "06075": "San Francisco County",
    "06081": "San Mateo County",
    "06085": "Santa Clara County",
    "06095": "Solano County",
    "06097": "Sonoma County",
}

SOURCE_MANIFEST: dict[str, dict[str, str | bool]] = {
    "bfs_monthly.csv": {
        "required": True,
        "institution": "U.S. Census Bureau",
        "role": "Monthly Business Formation Statistics time series",
        "source_url": "https://www.census.gov/econ/bfs/present/index.html",
        "expected_parser": "ingest_bfs_monthly",
    },
    "bfs_county_apps_annual.xlsx": {
        "required": True,
        "institution": "U.S. Census Bureau",
        "role": "Annual county business applications workbook",
        "source_url": "https://www.census.gov/econ/bfs/data/county.html",
        "expected_parser": "ingest_bfs_county_annual",
    },
    "list1_2023.xlsx": {
        "required": True,
        "institution": "U.S. Census Bureau",
        "role": "CBSA/CSA delineation crosswalk",
        "source_url": "https://www2.census.gov/programs-surveys/metro-micro/geographies/reference-files/2023/delineation-files/list1_2023.xlsx",
        "expected_parser": "ingest_cbsa_delineation",
    },
    "area-titles-csv.csv": {
        "required": True,
        "institution": "U.S. Bureau of Labor Statistics",
        "role": "QCEW area-title lookup",
        "source_url": "https://www.bls.gov/cew/classifications/areas/qcew-area-titles.htm",
        "expected_parser": "ingest_area_titles",
    },
}
