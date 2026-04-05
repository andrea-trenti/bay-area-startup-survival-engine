"""
Build a QCEW-based operating-cost context panel.

This script inventories QCEW annual area files from the source-acquisition layer, extracts private-sector summary rows, and writes either a Bay Area panel or an explicit coverage report. Raw institutional files remain outside version control.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import pandas as pd


from config import BAY_AREA_COUNTIES, REPO_ROOT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--qcew-dir",
        type=Path,
        default=REPO_ROOT / "data" / "raw",
        help="Directory containing annual QCEW area CSV files.",
    )
    parser.add_argument(
        "--area-title-file",
        type=Path,
        default=REPO_ROOT / "data" / "raw" / "area-titles-csv.csv",
        help="QCEW area title mapping file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "outputs" / "qcew_context",
        help="Directory where processed outputs will be written.",
    )
    return parser.parse_args()


def list_qcew_files(qcew_dir: Path) -> list[Path]:
    return sorted(qcew_dir.glob("20*.annual *.csv"))


def normalize_fips(value: object) -> str:
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return text.zfill(5)


def load_area_titles(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["area_fips", "area_title"])
    df = pd.read_csv(path, dtype=str)
    df["area_fips"] = df["area_fips"].map(normalize_fips)
    return df[["area_fips", "area_title"]]


def select_private_total(df: pd.DataFrame) -> pd.DataFrame:
    cols = {
        "area_fips",
        "year",
        "own_code",
        "industry_code",
        "size_code",
        "annual_avg_estabs_count",
        "annual_avg_emplvl",
        "total_annual_wages",
        "annual_avg_wkly_wage",
        "avg_annual_pay",
        "area_title",
        "own_title",
        "industry_title",
        "size_title",
    }
    missing = cols.difference(df.columns)
    if missing:
        raise ValueError(f"Missing expected QCEW columns: {sorted(missing)}")

    out = df.copy()
    out["area_fips"] = out["area_fips"].map(normalize_fips)
    out["own_code"] = pd.to_numeric(out["own_code"], errors="coerce")
    out["size_code"] = pd.to_numeric(out["size_code"], errors="coerce")
    out["industry_code"] = out["industry_code"].astype(str).str.strip()

    mask = (
        (out["own_code"] == 5)
        & (out["industry_code"] == "10")
        & (out["size_code"] == 0)
    )
    out = out.loc[mask, list(cols)].copy()

    numeric_cols = [
        "annual_avg_estabs_count",
        "annual_avg_emplvl",
        "total_annual_wages",
        "annual_avg_wkly_wage",
        "avg_annual_pay",
    ]
    for col in numeric_cols:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    return out


def read_qcew_private_totals(files: Iterable[Path]) -> pd.DataFrame:
    chunks = []
    for path in files:
        try:
            df = pd.read_csv(path)
            selected = select_private_total(df)
            selected["source_filename"] = path.name
            chunks.append(selected)
        except Exception as exc:  # pragma: no cover - diagnostic path
            chunks.append(
                pd.DataFrame(
                    {
                        "area_fips": [],
                        "year": [],
                        "own_code": [],
                        "industry_code": [],
                        "size_code": [],
                        "annual_avg_estabs_count": [],
                        "annual_avg_emplvl": [],
                        "total_annual_wages": [],
                        "annual_avg_wkly_wage": [],
                        "avg_annual_pay": [],
                        "area_title": [],
                        "own_title": [],
                        "industry_title": [],
                        "size_title": [],
                        "source_filename": [],
                        "error": [f"{path.name}: {exc}"],
                    }
                )
            )
    if not chunks:
        return pd.DataFrame()
    return pd.concat(chunks, ignore_index=True, sort=False)


def build_inventory(files: list[Path], area_titles: pd.DataFrame) -> pd.DataFrame:
    inventory = pd.DataFrame({"source_filename": [f.name for f in files]})
    inventory["year_from_filename"] = inventory["source_filename"].str.extract(r"^(\d{4})")
    inventory["area_fips"] = inventory["source_filename"].str.extract(r"annual\s+(\d{5})")
    inventory["area_fips"] = inventory["area_fips"].map(normalize_fips)
    if not area_titles.empty:
        inventory = inventory.merge(area_titles, on="area_fips", how="left")
    inventory["is_bay_area_target"] = inventory["area_fips"].isin(BAY_AREA_COUNTIES)
    return inventory


def write_outputs(output_dir: Path, inventory: pd.DataFrame, private_totals: pd.DataFrame) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    inventory.to_csv(output_dir / "qcew_local_inventory.csv", index=False)

    if private_totals.empty:
        missing = pd.DataFrame(
            {
                "area_fips": list(BAY_AREA_COUNTIES.keys()),
                "area_title_expected": list(BAY_AREA_COUNTIES.values()),
                "present_in_local_inventory": False,
            }
        )
        missing.to_csv(output_dir / "bay_area_qcew_missing_targets.csv", index=False)
        return

    private_totals.to_csv(output_dir / "qcew_private_totals_extracted.csv", index=False)

    bay_area = private_totals[private_totals["area_fips"].isin(BAY_AREA_COUNTIES)].copy()
    if bay_area.empty:
        missing = pd.DataFrame(
            {
                "area_fips": list(BAY_AREA_COUNTIES.keys()),
                "area_title_expected": list(BAY_AREA_COUNTIES.values()),
                "present_in_local_inventory": False,
            }
        )
        missing.to_csv(output_dir / "bay_area_qcew_missing_targets.csv", index=False)
        return

    bay_area["wages_per_employee_check"] = bay_area["total_annual_wages"] / bay_area["annual_avg_emplvl"]
    bay_area = bay_area.sort_values(["year", "avg_annual_pay"], ascending=[True, False])
    bay_area.to_csv(output_dir / "bay_area_qcew_operating_cost_context.csv", index=False)

    summary = (
        bay_area.groupby("year", dropna=False)
        .agg(
            total_private_establishments=("annual_avg_estabs_count", "sum"),
            total_private_employment=("annual_avg_emplvl", "sum"),
            total_private_wages=("total_annual_wages", "sum"),
            mean_avg_annual_pay=("avg_annual_pay", "mean"),
            mean_avg_weekly_wage=("annual_avg_wkly_wage", "mean"),
        )
        .reset_index()
    )
    summary.to_csv(output_dir / "bay_area_qcew_operating_cost_summary.csv", index=False)


def main() -> None:
    args = parse_args()
    area_titles = load_area_titles(args.area_title_file)
    files = list_qcew_files(args.qcew_dir)
    inventory = build_inventory(files, area_titles)
    private_totals = read_qcew_private_totals(files)
    write_outputs(args.output_dir, inventory, private_totals)
    print(f"QCEW outputs written to: {args.output_dir}")


if __name__ == "__main__":
    main()
