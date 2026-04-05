# Bay Area Startup Survival Engine
## Public-data research infrastructure for entrepreneurial formation, employer-conversion proxies, regional concentration, and operating context

This repository is a Markdown-first empirical research system for measuring Bay Area entrepreneurial inflows, county concentration, projected employer conversion, regime shifts, and resilience diagnostics using official U.S. public datasets. It is designed as a clean separation between **original analytical work** and **institution-owned source data**: the repository publishes papers, methodological standards, code, and reproducibility rules, while the underlying statistical files remain outside version control in a non-versioned acquisition layer.

The repository is intended for serious analytical use rather than narrative commentary. Its core objects are county-level business-application dynamics, California-to-county bridge models for employer formation, Bay Area concentration measures, hazard-style diagnostics, real-time nowcast evaluation, and resilience scorecarding. The pipeline is source-contingent by design: each layer executes when the corresponding public source family has been integrated into the acquisition layer, and every script emits explicit coverage diagnostics rather than silently fabricating values or overstating evidentiary coverage.

## Research scope

The repository addresses five linked questions:

1. How large is the Bay Area entrepreneurial inflow relative to California and to its own history?
2. How concentrated is that inflow across the nine Bay Area counties?
3. What order of magnitude is implied for employer-forming startups once state-level conversion information is introduced?
4. Which counties appear more fragile, more resilient, or more cyclically exposed?
5. How should these signals be interpreted under explicit evidentiary and inference constraints?

## Repository architecture

```text
bay-area-startup-survival-engine/
├── README.md
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── Makefile
├── .github/workflows/python-checks.yml
├── tests/
├── data/
│   ├── README.md
│   ├── raw/
│   └── processed/
├── outputs/
├── docs/
├── analysis/
└── src/
```

## Directory guide

| Directory | Function |
|---|---|
| `docs/` | Governance, inference, reproducibility, attribution, and methodological-control standards. |
| `analysis/` | Self-contained Markdown research notes presenting the substantive empirical logic and findings of the repository. |
| `src/` | Python ingestion, transformation, diagnostics, nowcasting, backtesting, and scorecard pipelines. |
| `data/raw/` | Non-versioned source-acquisition layer for public statistical releases. |
| `data/processed/` | Rebuildable intermediate tables excluded from version control. |
| `outputs/` | Derived output layer for diagnostics, scorecards, reporting tables, and scenario exports. |
| `tests/` | Repository integrity, CLI smoke checks, and configuration-validation tests. |

## Repository map

See `docs/repository-map.md` for the complete file inventory and per-file role description.

## Pipeline architecture

| Layer | Primary modules | Main inputs | Main outputs |
|---|---|---|---|
| Validation | `src/validate_public_data_inventory.py` | source-acquisition manifest | coverage report, file diagnostics |
| Ingestion | `src/ingest_public_startup_data.py` | BFS, geography, QCEW source families | cleaned intermediate panels |
| Foundation | `src/build_bay_area_foundation_panel.py` | processed BFS and QCEW tables | Bay Area foundation panel |
| Feature engineering | `src/compute_bay_area_application_features.py`, `src/assemble_bay_area_employer_proxy_panel.py` | annual and monthly BFS | county feature tables, employer-conversion proxies |
| Reporting | `src/build_bay_area_reporting_tables.py` | processed feature tables | publication-ready summary tables |
| Labor context | `src/build_qcew_operating_cost_context.py` | QCEW area files | operating-context tables and coverage diagnostics |
| Forecasting and risk | `src/estimate_bay_area_nowcast_scenarios.py`, `src/compute_bay_area_hazard_proxies.py`, `src/detect_bay_area_regime_shifts.py` | BFS annual/monthly history | scenario tables, hazard indicators, turning-point diagnostics |
| Evaluation and monitoring | `src/backtest_bay_area_application_nowcasts.py`, `src/build_bay_area_resilience_scorecard.py` | forecasting outputs and historical panels | backtests, resilience scorecards |

## Replication workflow

| Step | Command | Expected artifact |
|---|---|---|
| Validate source inventory | `python src/validate_public_data_inventory.py` | `outputs/validation/public_data_validation_report.json` |
| Ingest and standardize | `python src/ingest_public_startup_data.py` | cleaned tables in `data/processed/` |
| Run full pipeline | `python src/run_local_repository_pipeline.py` | derived diagnostics in `outputs/` |
| Smoke test repository | `pytest` | repository integrity and CLI validation |

For convenience:

```bash
make validate
make pipeline
make test
```

## Source institutions and data ownership

| Institution | Dataset family | Role in repository | Redistributed here? |
|---|---|---|---|
| U.S. Census Bureau | Business Formation Statistics (BFS) | entrepreneurial inflow, projected employer conversion, scenario design | No |
| U.S. Census Bureau | geographic delineation files | county and metropolitan mapping | No |
| U.S. Census Bureau | BDS / CBP / SUSB / NES (documented extensions) | downstream business-dynamics and establishment-context extensions | No |
| U.S. Bureau of Labor Statistics | QCEW and area-title files | labor-cost and operating-context layer | No |

The repository does not republish raw institutional files. It documents source pages, expected filenames, and acquisition conventions so that the empirical system can be reconstructed independently.

## How to use this repository

- As a Bay Area startup-ecosystem measurement system grounded in public administrative data.
- As a Markdown-first analytical repository for academic papers, investor-style memoranda, or policy notes.
- As a template for building comparable regional startup-monitoring systems in other U.S. ecosystems.
- As a modular empirical shell that can be extended with additional Census or BLS source families documented in `data/raw/README.md`.

## Copyright and reuse

### Analytical writing and indicator design
The analytical prose, indicator design, methodological architecture, and repository structure are original work. Short quotations with attribution are acceptable for research, teaching, and internal analytical use. Substantial reuse of the analytical writing or indicator framework should credit the author and, where practical, request permission.

### Code
The code is published for inspection, repository-bound replication, and educational use within the repository context. Redistribution of modified or unmodified code outside that context should preserve attribution and the repository’s source-ownership boundaries.

### Underlying source data
The underlying statistical releases remain the property of their respective institutions. In this repository, the primary institutional owners are the U.S. Census Bureau and the U.S. Bureau of Labor Statistics. Nothing in this repository constitutes legal advice.

© 2026 Andrea Trenti. All rights reserved.
• The analytical texts, tables and structure of the indicators are original works protected by copyright.
• The underlying statistical data remain the property of their respective institutions (including, in this repository, the U.S. Census Bureau and the U.S. Bureau of Labor Statistics) and are used exclusively for analytical and educational purposes.
• No open-source or Creative Commons licence is granted for the full reuse of the texts; any substantial reuse requires the author’s permission.
