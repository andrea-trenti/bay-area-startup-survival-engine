"""Run the repository-wide Bay Area startup analytics pipeline in sequence."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from config import RAW_DIR, REPO_ROOT


PIPELINE_REGISTRY = {
    "validate": ["src/validate_public_data_inventory.py"],
    "ingest": ["src/ingest_public_startup_data.py"],
    "foundation": ["src/build_bay_area_foundation_panel.py"],
    "qcew": ["src/build_qcew_operating_cost_context.py"],
    "features": [
        "src/compute_bay_area_application_features.py",
        "src/assemble_bay_area_employer_proxy_panel.py",
        "src/build_bay_area_reporting_tables.py",
    ],
    "forecast": ["src/estimate_bay_area_nowcast_scenarios.py"],
    "risk": [
        "src/compute_bay_area_hazard_proxies.py",
        "src/detect_bay_area_regime_shifts.py",
        "src/backtest_bay_area_application_nowcasts.py",
    ],
    "scorecard": ["src/build_bay_area_resilience_scorecard.py"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=RAW_DIR,
        help="Directory containing source files acquired from the issuing institutions.",
    )
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="Python interpreter used to execute downstream scripts.",
    )
    parser.add_argument(
        "--skip",
        nargs="*",
        default=[],
        choices=sorted(PIPELINE_REGISTRY),
        help="Named pipeline layers to skip.",
    )
    parser.add_argument(
        "--only",
        nargs="*",
        default=[],
        choices=sorted(PIPELINE_REGISTRY),
        help="If provided, execute only the selected named layers.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the execution plan without running the scripts.",
    )
    return parser.parse_args()


def build_steps(python_executable: str, raw_dir: Path) -> list[list[str]]:
    raw = str(raw_dir)
    return [
        [python_executable, "src/validate_public_data_inventory.py", "--raw-dir", raw],
        [python_executable, "src/ingest_public_startup_data.py", "--repo-root", str(REPO_ROOT), "--raw-dir", raw],
        [python_executable, "src/build_bay_area_foundation_panel.py", "--repo-root", str(REPO_ROOT)],
        [python_executable, "src/build_qcew_operating_cost_context.py", "--qcew-dir", raw, "--area-title-file", str(raw_dir / "area-titles-csv.csv")],
        [python_executable, "src/compute_bay_area_application_features.py", "--raw-dir", raw],
        [python_executable, "src/assemble_bay_area_employer_proxy_panel.py", "--raw-dir", raw],
        [python_executable, "src/build_bay_area_reporting_tables.py"],
        [python_executable, "src/estimate_bay_area_nowcast_scenarios.py", "--bfs-county-file", str(raw_dir / "bfs_county_apps_annual.xlsx")],
        [python_executable, "src/compute_bay_area_hazard_proxies.py", "--bfs-county-file", str(raw_dir / "bfs_county_apps_annual.xlsx")],
        [python_executable, "src/detect_bay_area_regime_shifts.py", "--bfs-county-file", str(raw_dir / "bfs_county_apps_annual.xlsx")],
        [python_executable, "src/backtest_bay_area_application_nowcasts.py", "--bfs-monthly-file", str(raw_dir / "bfs_monthly.csv"), "--bfs-county-file", str(raw_dir / "bfs_county_apps_annual.xlsx")],
        [python_executable, "src/build_bay_area_resilience_scorecard.py", "--bfs-county-file", str(raw_dir / "bfs_county_apps_annual.xlsx")],
    ]


def classify_step(script_path: str) -> str:
    for layer, members in PIPELINE_REGISTRY.items():
        if script_path in members:
            return layer
    raise KeyError(script_path)


def run_step(cmd: list[str], dry_run: bool) -> None:
    if dry_run:
        print("[dry-run]", " ".join(cmd))
        return
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


def main() -> None:
    args = parse_args()
    steps = build_steps(args.python, args.raw_dir)
    selected = set(args.only) if args.only else set(PIPELINE_REGISTRY)
    skipped = set(args.skip)

    for step in steps:
        layer = classify_step(step[1])
        if layer not in selected or layer in skipped:
            continue
        run_step(step, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
