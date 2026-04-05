from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_key_scripts_exist() -> None:
    expected = [
        "src/validate_public_data_inventory.py",
        "src/ingest_public_startup_data.py",
        "src/build_bay_area_foundation_panel.py",
        "src/run_local_repository_pipeline.py",
    ]
    for relative in expected:
        assert (REPO_ROOT / relative).exists()


def test_cli_help_commands() -> None:
    commands = [
        [sys.executable, "src/validate_public_data_inventory.py", "--help"],
        [sys.executable, "src/run_local_repository_pipeline.py", "--help"],
    ]
    for command in commands:
        result = subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True)
        assert result.returncode == 0
        assert "usage" in result.stdout.lower() or "usage" in result.stderr.lower()
