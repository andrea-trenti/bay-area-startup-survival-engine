#!/usr/bin/env python3
"""
Build Markdown-ready reporting tables from the Bay Area employer proxy outputs.

The script consumes outputs produced by `assemble_bay_area_employer_proxy_panel.py`
and writes compact Markdown tables that can be pasted into README files, research
notes, or issue trackers without manual spreadsheet work.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Markdown reporting tables for Bay Area startup outputs.")
    parser.add_argument("--input-dir", default="outputs/modeling", help="Directory containing derived CSV outputs.")
    parser.add_argument("--output-dir", default="outputs/reporting", help="Directory for generated Markdown tables.")
    parser.add_argument("--latest-year", type=int, default=None, help="Override latest year selection.")
    return parser.parse_args()


def markdown_table(frame: pd.DataFrame) -> str:
    return frame.to_markdown(index=False)


def build_county_scorecard(county_panel: pd.DataFrame, year: int) -> pd.DataFrame:
    frame = county_panel[county_panel["year"] == year].copy()
    keep = [
        "county_name",
        "business_applications_obs",
        "county_share_obs",
        "employer_formations_proxy",
        "regional_proxy_share",
        "county_yoy_growth",
    ]
    frame = frame[keep].sort_values("employer_formations_proxy", ascending=False).reset_index(drop=True)
    frame["county_share_obs"] = frame["county_share_obs"] * 100.0
    frame["regional_proxy_share"] = frame["regional_proxy_share"] * 100.0
    frame["county_yoy_growth"] = frame["county_yoy_growth"] * 100.0
    frame = frame.rename(
        columns={
            "county_name": "County",
            "business_applications_obs": "Observed applications",
            "county_share_obs": "Application share (%)",
            "employer_formations_proxy": "Employer proxy",
            "regional_proxy_share": "Proxy share (%)",
            "county_yoy_growth": "YoY applications (%)",
        }
    )
    return frame.round(2)


def build_region_scorecard(region_summary: pd.DataFrame) -> pd.DataFrame:
    frame = region_summary.copy()
    keep = [
        "year",
        "bay_area_business_applications_obs",
        "bay_area_employer_formations_proxy",
        "california_conversion_ratio_spliced",
        "applications_yoy_growth",
        "proxy_yoy_growth",
        "top3_county_share_obs",
        "county_hhi_obs",
    ]
    frame = frame[keep].rename(
        columns={
            "year": "Year",
            "bay_area_business_applications_obs": "Observed applications",
            "bay_area_employer_formations_proxy": "Employer proxy",
            "california_conversion_ratio_spliced": "CA conversion ratio",
            "applications_yoy_growth": "Applications YoY (%)",
            "proxy_yoy_growth": "Proxy YoY (%)",
            "top3_county_share_obs": "Top-3 county share (%)",
            "county_hhi_obs": "County HHI",
        }
    )
    frame["CA conversion ratio"] = frame["CA conversion ratio"] * 100.0
    frame["Applications YoY (%)"] = frame["Applications YoY (%)"] * 100.0
    frame["Proxy YoY (%)"] = frame["Proxy YoY (%)"] * 100.0
    frame["Top-3 county share (%)"] = frame["Top-3 county share (%)"] * 100.0
    return frame.round(2)


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    county_path = input_dir / "bay_area_county_employer_proxy_panel.csv"
    region_path = input_dir / "bay_area_region_employer_proxy_summary.csv"

    if not county_path.exists() or not region_path.exists():
        raise FileNotFoundError(
            "Required modeling outputs are missing. Run assemble_bay_area_employer_proxy_panel.py first."
        )

    county_panel = pd.read_csv(county_path)
    region_summary = pd.read_csv(region_path)

    latest_year = args.latest_year or int(region_summary["year"].max())

    county_scorecard = build_county_scorecard(county_panel, latest_year)
    region_scorecard = build_region_scorecard(region_summary)

    county_md = [
        f"# Bay Area County Scorecard ({latest_year})",
        "",
        "Observed applications are direct county annual counts; employer proxy is state-anchored.",
        "",
        markdown_table(county_scorecard),
        "",
    ]
    region_md = [
        "# Bay Area Regional Summary",
        "",
        "The conversion ratio is the California annual-average spliced `SBF4Q / BA` series.",
        "",
        markdown_table(region_scorecard),
        "",
    ]

    county_md_path = output_dir / "bay_area_county_scorecard.md"
    region_md_path = output_dir / "bay_area_region_scorecard.md"

    county_md_path.write_text("\n".join(county_md), encoding="utf-8")
    region_md_path.write_text("\n".join(region_md), encoding="utf-8")

    print(f"[ok] wrote {county_md_path}")
    print(f"[ok] wrote {region_md_path}")


if __name__ == "__main__":
    main()
