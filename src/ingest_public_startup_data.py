"""
Public-data ingestion pipeline for the Bay Area Startup Survival Engine.

This script assumes that source files exist in the non-versioned acquisition layer and are *not* tracked in Git. It standardizes official public data extracts into reusable CSV outputs under ``data/processed/``.

Supported source families
-------------------------
1. Business Formation Statistics monthly extract (BFS)
2. Annual county business applications workbook
3. Area title crosswalk for QCEW area FIPS labels
4. CBSA delineation workbook
5. QCEW annual area CSV files

The pipeline is built for modular replication. Missing optional files do
not hard-fail the ingestion step unless they are explicitly required.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import pandas as pd

from config import BAY_AREA_COUNTIES


LOGGER = logging.getLogger("ingest_public_startup_data")

@dataclass
class IngestionPaths:
    repo_root: Path
    raw_dir: Path
    processed_dir: Path


def configure_logging(verbose: bool = False) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def normalize_fips(value: object, width: int = 5) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip()
    text = text.replace(".0", "")
    digits = re.sub(r"\D", "", text)
    return digits.zfill(width)


def discover_paths(repo_root: Path, raw_dir: Optional[Path]) -> IngestionPaths:
    if raw_dir is None:
        raw_dir = repo_root / "data" / "raw"
    processed_dir = repo_root / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    return IngestionPaths(repo_root=repo_root, raw_dir=raw_dir, processed_dir=processed_dir)


def resolve_file(raw_dir: Path, candidates: Iterable[str]) -> Optional[Path]:
    for candidate in candidates:
        path = raw_dir / candidate
        if path.exists():
            return path
    return None


def ingest_bfs_monthly(path: Path) -> pd.DataFrame:
    LOGGER.info("Reading BFS monthly file: %s", path.name)
    df = pd.read_csv(path)

    month_columns = [
        column
        for column in ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
        if column in df.columns
    ]
    month_lookup = {name: i for i, name in enumerate(month_columns, start=1)}

    long_df = df.melt(
        id_vars=["sa", "naics_sector", "series", "geo", "year"],
        value_vars=month_columns,
        var_name="month_name",
        value_name="value",
    )
    long_df["month"] = long_df["month_name"].map(month_lookup)
    long_df["period"] = pd.to_datetime(
        dict(year=long_df["year"].astype(int), month=long_df["month"].astype(int), day=1),
        errors="coerce",
    )
    long_df["seasonal_adjustment"] = long_df["sa"].map({"A": "seasonally_adjusted", "U": "unadjusted"}).fillna("unknown")
    long_df["value"] = pd.to_numeric(long_df["value"], errors="coerce")
    long_df = long_df.sort_values(["geo", "naics_sector", "series", "seasonal_adjustment", "period"]).reset_index(drop=True)

    LOGGER.info("BFS monthly standardized rows: %s", f"{len(long_df):,}")
    return long_df


def ingest_bfs_county_annual(path: Path) -> pd.DataFrame:
    LOGGER.info("Reading annual county BFS workbook: %s", path.name)
    df = pd.read_excel(path, header=2)
    df = df.rename(columns={df.columns[0]: "state_abbrev", df.columns[1]: "county_name"})
    df["state_fips"] = df["state_fips"].apply(lambda x: normalize_fips(x, width=2))
    df["county_fips"] = df["county_fips"].apply(lambda x: normalize_fips(x, width=3))
    df["county_code"] = df["County Code"].apply(lambda x: normalize_fips(x, width=5))
    df["county_name"] = df["county_name"].astype(str).str.strip()

    value_columns = [column for column in df.columns if re.fullmatch(r"BA\d{4}", str(column))]
    long_df = df.melt(
        id_vars=["state_abbrev", "county_name", "county_code", "state_fips", "county_fips"],
        value_vars=value_columns,
        var_name="series_year",
        value_name="business_applications",
    )
    long_df["year"] = long_df["series_year"].str.extract(r"(\d{4})").astype(int)
    long_df["business_applications"] = pd.to_numeric(long_df["business_applications"], errors="coerce")
    long_df["is_bay_area_county"] = long_df["county_code"].isin(BAY_AREA_COUNTIES)
    long_df["bay_area_county_name"] = long_df["county_code"].map(BAY_AREA_COUNTIES)
    long_df = long_df.sort_values(["county_code", "year"]).reset_index(drop=True)

    LOGGER.info("BFS county annual standardized rows: %s", f"{len(long_df):,}")
    return long_df


def ingest_area_titles(path: Path) -> pd.DataFrame:
    LOGGER.info("Reading area titles file: %s", path.name)
    df = pd.read_csv(path)
    df["area_fips"] = df["area_fips"].astype(str).str.replace(r"\.0$", "", regex=True).str.zfill(5)
    df["area_title"] = df["area_title"].astype(str).str.strip()
    return df.sort_values("area_fips").reset_index(drop=True)


def ingest_cbsa_delineation(path: Path) -> pd.DataFrame:
    LOGGER.info("Reading CBSA delineation workbook: %s", path.name)
    df = pd.read_excel(path, header=2)
    df["cbsa_code"] = df["CBSA Code"].apply(lambda x: normalize_fips(x, width=5))
    df["state_fips"] = df["FIPS State Code"].apply(lambda x: normalize_fips(x, width=2))
    df["county_fips"] = df["FIPS County Code"].apply(lambda x: normalize_fips(x, width=3))
    df["county_code"] = df["state_fips"] + df["county_fips"]
    df["county_name"] = df["County/County Equivalent"].astype(str).str.strip()
    df["state_name"] = df["State Name"].astype(str).str.strip()
    df["cbsa_title"] = df["CBSA Title"].astype(str).str.strip()
    df["metro_micro_status"] = df["Metropolitan/Micropolitan Statistical Area"].astype(str).str.strip()
    df["central_outlying_status"] = df["Central/Outlying County"].astype(str).str.strip()

    bay_mask = (
        (df["state_name"] == "California")
        & df["county_code"].isin(BAY_AREA_COUNTIES)
    )
    bay_df = df.loc[bay_mask, [
        "cbsa_code",
        "cbsa_title",
        "county_code",
        "county_name",
        "state_name",
        "metro_micro_status",
        "central_outlying_status",
    ]].copy()
    bay_df["is_bay_area_county"] = True
    return bay_df.sort_values(["cbsa_code", "county_code"]).reset_index(drop=True)


def discover_qcew_files(raw_dir: Path) -> List[Path]:
    pattern = re.compile(r"^20\d{2}\.annual .*\.csv$")
    files = [path for path in raw_dir.iterdir() if path.is_file() and pattern.match(path.name)]
    return sorted(files)


def ingest_qcew_area_files(paths: List[Path]) -> pd.DataFrame:
    LOGGER.info("Reading %d QCEW annual area file(s)", len(paths))
    frames: List[pd.DataFrame] = []

    keep_columns = [
        "area_fips",
        "area_title",
        "own_code",
        "own_title",
        "industry_code",
        "industry_title",
        "agglvl_code",
        "agglvl_title",
        "size_code",
        "size_title",
        "year",
        "annual_avg_estabs_count",
        "annual_avg_emplvl",
        "total_annual_wages",
        "annual_avg_wkly_wage",
        "avg_annual_pay",
        "oty_annual_avg_estabs_count_pct_chg",
        "oty_annual_avg_emplvl_pct_chg",
        "oty_total_annual_wages_pct_chg",
        "oty_annual_avg_wkly_wage_pct_chg",
        "oty_avg_annual_pay_pct_chg",
    ]

    for path in paths:
        try:
            frame = pd.read_csv(path)
            frame["source_file"] = path.name
            frame["area_fips"] = frame["area_fips"].apply(lambda x: normalize_fips(x, width=5))
            available_columns = [column for column in keep_columns if column in frame.columns]
            frame = frame[available_columns + ["source_file"]].copy()
            frames.append(frame)
        except Exception as exc:  # pragma: no cover - logged for operational visibility
            LOGGER.warning("Failed to parse %s: %s", path.name, exc)

    if not frames:
        return pd.DataFrame(columns=keep_columns + ["source_file"])

    df = pd.concat(frames, ignore_index=True)
    numeric_columns = [
        "year",
        "annual_avg_estabs_count",
        "annual_avg_emplvl",
        "total_annual_wages",
        "annual_avg_wkly_wage",
        "avg_annual_pay",
        "oty_annual_avg_estabs_count_pct_chg",
        "oty_annual_avg_emplvl_pct_chg",
        "oty_total_annual_wages_pct_chg",
        "oty_annual_avg_wkly_wage_pct_chg",
        "oty_avg_annual_pay_pct_chg",
    ]
    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    LOGGER.info("QCEW standardized rows: %s", f"{len(df):,}")
    return df


def write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def run_ingestion(paths: IngestionPaths) -> Dict[str, object]:
    manifest: Dict[str, object] = {"raw_dir": str(paths.raw_dir), "processed_dir": str(paths.processed_dir), "outputs": {}}

    bfs_monthly_path = resolve_file(paths.raw_dir, ["bfs_monthly.csv"])
    bfs_county_path = resolve_file(paths.raw_dir, ["bfs_county_apps_annual.xlsx"])
    area_titles_path = resolve_file(paths.raw_dir, ["area-titles-csv.csv"])
    cbsa_path = resolve_file(paths.raw_dir, ["list1_2023.xlsx"])

    required = {
        "bfs_monthly.csv": bfs_monthly_path,
        "bfs_county_apps_annual.xlsx": bfs_county_path,
        "area-titles-csv.csv": area_titles_path,
        "list1_2023.xlsx": cbsa_path,
    }
    missing_required = [name for name, path in required.items() if path is None]
    if missing_required:
        raise FileNotFoundError(f"Missing required raw file(s): {', '.join(missing_required)}")

    bfs_monthly = ingest_bfs_monthly(bfs_monthly_path)
    bfs_county = ingest_bfs_county_annual(bfs_county_path)
    area_titles = ingest_area_titles(area_titles_path)
    cbsa = ingest_cbsa_delineation(cbsa_path)
    qcew_paths = discover_qcew_files(paths.raw_dir)
    qcew = ingest_qcew_area_files(qcew_paths)

    outputs = {
        "bfs_monthly_long.csv": bfs_monthly,
        "bfs_county_annual_long.csv": bfs_county,
        "area_titles_clean.csv": area_titles,
        "bay_area_cbsa_crosswalk.csv": cbsa,
        "qcew_area_panel.csv": qcew,
    }

    for filename, frame in outputs.items():
        output_path = paths.processed_dir / filename
        write_csv(frame, output_path)
        manifest["outputs"][filename] = {
            "rows": int(len(frame)),
            "columns": list(frame.columns),
            "path": str(output_path),
        }

    manifest["qcew_source_files"] = [path.name for path in qcew_paths]
    manifest["qcew_source_file_count"] = len(qcew_paths)

    manifest_path = paths.processed_dir / "ingestion_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    LOGGER.info("Wrote ingestion manifest to %s", manifest_path)

    return manifest


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Standardize public startup-related source files into processed tables.")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1], help="Repository root path.")
    parser.add_argument("--raw-dir", type=Path, default=None, help="Optional override for raw data directory.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging.")
    return parser


def main() -> None:
    parser = build_argument_parser()
    args = parser.parse_args()
    configure_logging(verbose=args.verbose)

    paths = discover_paths(repo_root=args.repo_root, raw_dir=args.raw_dir)
    manifest = run_ingestion(paths)

    LOGGER.info("Ingestion completed successfully.")
    LOGGER.info("Processed datasets: %s", ", ".join(manifest["outputs"].keys()))


if __name__ == "__main__":
    main()
