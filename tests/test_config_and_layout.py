from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import BAY_AREA_COUNTIES, SOURCE_MANIFEST  # noqa: E402


def test_bay_area_scope_size() -> None:
    assert len(BAY_AREA_COUNTIES) == 9
    assert BAY_AREA_COUNTIES["06085"] == "Santa Clara County"


def test_source_manifest_core() -> None:
    assert set(SOURCE_MANIFEST) == {
        "bfs_monthly.csv",
        "bfs_county_apps_annual.xlsx",
        "list1_2023.xlsx",
        "area-titles-csv.csv",
    }
    for spec in SOURCE_MANIFEST.values():
        assert "institution" in spec
        assert "source_url" in spec
        assert "role" in spec
        assert "expected_parser" in spec


def test_repository_layout() -> None:
    for relative in ["README.md", "src", "docs", "analysis", "data/raw", "data/processed", "outputs", ".github"]:
        assert (REPO_ROOT / relative).exists()
