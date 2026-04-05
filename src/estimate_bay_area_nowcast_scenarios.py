"""
Estimate Bay Area business-application scenarios for 2025 and 2026.

Expected inputs are public raw files stored outside version control.
No raw institutional data are redistributed by this repository.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


from config import BAY_AREA_COUNTIES, REPO_ROOT


@dataclass(frozen=True)
class ScenarioResult:
    scenario: str
    annual_growth: float
    year_2025: float
    year_2026: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bfs-county-file",
        type=Path,
        default=REPO_ROOT / "data" / "raw" / "bfs_county_apps_annual.xlsx",
        help="Path to the annual county business applications Excel file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "outputs" / "scenario_outputs",
        help="Directory where scenario tables and diagnostics will be written.",
    )
    return parser.parse_args()


def _get_ba_columns(columns: Iterable[str]) -> list[str]:
    return [col for col in columns if str(col).startswith("BA")]


def load_county_applications(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"BFS county file not found: {path}")

    df = pd.read_excel(path, header=2, dtype=str)
    required = {"State", "County", "state_fips", "county_fips"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    ba_columns = _get_ba_columns(df.columns)
    if not ba_columns:
        raise ValueError("No annual BA columns found in BFS county file.")

    df = df[df["state_fips"].astype(str).str.zfill(2) == "06"].copy()
    df["county_fips"] = df["county_fips"].astype(str).str.zfill(3)
    df["full_fips"] = df["state_fips"].astype(str).str.zfill(2) + df["county_fips"]
    df = df[df["full_fips"].isin(BAY_AREA_COUNTIES)].copy()

    if df.empty:
        raise ValueError("No Bay Area counties found in supplied BFS county file.")

    for col in ba_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["county_name"] = df["full_fips"].map(BAY_AREA_COUNTIES)
    return df[["full_fips", "county_name", *ba_columns]].sort_values("full_fips")


def aggregate_series(df: pd.DataFrame) -> pd.Series:
    ba_columns = _get_ba_columns(df.columns)
    aggregate = df[ba_columns].sum(axis=0)
    aggregate.index = aggregate.index.str.replace("BA", "", regex=False).astype(int)
    return aggregate.sort_index()


def scenario_rates(series: pd.Series) -> dict[str, float]:
    required_years = {2005, 2019, 2020, 2022, 2023, 2024}
    missing = required_years.difference(series.index.tolist())
    if missing:
        raise ValueError(f"Missing required years for scenario engine: {sorted(missing)}")

    g_struct = (series.loc[2019] / series.loc[2005]) ** (1 / 14) - 1
    g_recent = (series.loc[2024] / series.loc[2022]) ** (1 / 2) - 1
    g_post = (series.loc[2024] / series.loc[2020]) ** (1 / 4) - 1
    g_shock = series.loc[2024] / series.loc[2023] - 1

    return {
        "structural": float(g_struct),
        "recent": float(g_recent),
        "post_2020": float(g_post),
        "shock": float(g_shock),
        "conservative": float(min(g_struct, g_shock)),
        "central": float(0.5 * g_struct + 0.5 * g_recent),
        "upside": float(max(0.5 * g_struct + 0.5 * g_recent, g_post)),
    }


def build_scenarios(series: pd.Series) -> list[ScenarioResult]:
    rates = scenario_rates(series)
    base_value = float(series.loc[2024])

    outputs: list[ScenarioResult] = []
    for name in ("conservative", "central", "upside"):
        g = rates[name]
        year_2025 = base_value * (1 + g)
        year_2026 = year_2025 * (1 + g)
        outputs.append(
            ScenarioResult(
                scenario=name,
                annual_growth=g,
                year_2025=year_2025,
                year_2026=year_2026,
            )
        )
    return outputs


def county_share_table(df: pd.DataFrame) -> pd.DataFrame:
    out = df[["full_fips", "county_name", "BA2023", "BA2024"]].copy()
    total_2024 = out["BA2024"].sum()
    out["share_2024"] = out["BA2024"] / total_2024
    out["share_2024_pct"] = out["share_2024"] * 100
    out["yoy_growth_2024_pct"] = np.where(
        out["BA2023"] > 0,
        (out["BA2024"] / out["BA2023"] - 1) * 100,
        np.nan,
    )
    out = out.sort_values("BA2024", ascending=False).reset_index(drop=True)
    return out


def project_counties(county_shares: pd.DataFrame, scenarios: list[ScenarioResult]) -> pd.DataFrame:
    rows = []
    for result in scenarios:
        for _, row in county_shares.iterrows():
            rows.append(
                {
                    "scenario": result.scenario,
                    "full_fips": row["full_fips"],
                    "county_name": row["county_name"],
                    "share_2024": row["share_2024"],
                    "projected_2025": result.year_2025 * row["share_2024"],
                    "projected_2026": result.year_2026 * row["share_2024"],
                }
            )
    return pd.DataFrame(rows)


def write_outputs(
    output_dir: Path,
    aggregate: pd.Series,
    scenarios: list[ScenarioResult],
    county_table: pd.DataFrame,
    county_projection: pd.DataFrame,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    aggregate_df = (
        aggregate.rename("bay_area_applications")
        .rename_axis("year")
        .reset_index()
    )
    aggregate_df.to_csv(output_dir / "bay_area_ba_annual_series.csv", index=False)

    scenario_df = pd.DataFrame([s.__dict__ for s in scenarios])
    scenario_df.to_csv(output_dir / "bay_area_scenario_matrix.csv", index=False)

    county_table.to_csv(output_dir / "bay_area_county_shares_2024.csv", index=False)
    county_projection.to_csv(output_dir / "bay_area_county_projection_matrix.csv", index=False)

    diagnostics = pd.DataFrame(
        {
            "metric": [
                "applications_2005",
                "applications_2019",
                "applications_2024",
                "cagr_2005_2024",
                "top3_share_2024_pct",
                "hhi_2024",
            ],
            "value": [
                float(aggregate.loc[2005]),
                float(aggregate.loc[2019]),
                float(aggregate.loc[2024]),
                float((aggregate.loc[2024] / aggregate.loc[2005]) ** (1 / 19) - 1),
                float(county_table.head(3)["share_2024"].sum() * 100),
                float((county_table["share_2024"] ** 2).sum() * 10000),
            ],
        }
    )
    diagnostics.to_csv(output_dir / "bay_area_scenario_diagnostics.csv", index=False)


def main() -> None:
    args = parse_args()
    county_df = load_county_applications(args.bfs_county_file)
    aggregate = aggregate_series(county_df)
    scenarios = build_scenarios(aggregate)
    county_table = county_share_table(county_df)
    county_projection = project_counties(county_table, scenarios)
    write_outputs(args.output_dir, aggregate, scenarios, county_table, county_projection)
    print(f"Scenario outputs written to: {args.output_dir}")


if __name__ == "__main__":
    main()
