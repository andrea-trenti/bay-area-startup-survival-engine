# Python Pipelines

This directory contains the executable research infrastructure of the repository. The codebase is modular by design: validation, ingestion, feature engineering, labor-context diagnostics, nowcasting, backtesting, and scorecarding are separated into distinct scripts so that each empirical layer remains auditable.

## Execution order

1. `validate_public_data_inventory.py`
2. `ingest_public_startup_data.py`
3. `build_bay_area_foundation_panel.py`
4. `compute_bay_area_application_features.py`
5. `assemble_bay_area_employer_proxy_panel.py`
6. `build_bay_area_reporting_tables.py`
7. `build_qcew_operating_cost_context.py`
8. `estimate_bay_area_nowcast_scenarios.py`
9. `compute_bay_area_hazard_proxies.py`
10. `detect_bay_area_regime_shifts.py`
11. `backtest_bay_area_application_nowcasts.py`
12. `build_bay_area_resilience_scorecard.py`
13. `run_local_repository_pipeline.py`

## Design principles

- Source files belong to a non-versioned acquisition layer, not to the public repository payload.
- Processed and output files are rebuildable artifacts and remain excluded from Git.
- Source-contingent families are handled conditionally and reported through explicit coverage diagnostics.
- Bay Area geography is centralized in `src/config.py` and should not be redefined ad hoc.
- Every executable layer should be auditable from inputs to written outputs.
