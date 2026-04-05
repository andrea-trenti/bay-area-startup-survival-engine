# Repository Map

This document provides the complete file inventory for the repository and explains how the folders interact as a single empirical system.

## Root files

- `README.md` — landing page, architecture summary, and reuse boundaries.
- `.gitignore` — exclusion rules for non-versioned source files and rebuildable artifacts.
- `pyproject.toml` — project metadata, tool configuration, and dependency declaration.
- `requirements.txt` — lightweight installation path for direct repository use.
- `Makefile` — convenience commands for validation, pipeline execution, testing, linting, and smoke checks.

## Documentation layer

- `docs/startup-data-governance-and-source-map.md` — source hierarchy, ownership boundaries, and evidence-chain design.
- `docs/bay-area-geographic-scope-and-fips-governance.md` — nine-county Bay Area scope and county-code governance.
- `docs/startup-data-dictionary-and-measurement-boundaries.md` — variable definitions and interpretation limits.
- `docs/model-governance-and-inference-boundaries.md` — acceptable claims, prohibited claims, and inferential boundaries.
- `docs/reproducibility-protocol-and-citation-standard.md` — provenance discipline, rerun rules, and citation conventions.
- `docs/identification-robustness-and-sensitivity-standard.md` — robustness hierarchy, sensitivity rules, and evidentiary grading.
- `docs/nonpublic-data-handling-and-attribution-protocol.md` — public-release boundaries and source-attribution requirements.
- `docs/feature-engineering-and-alert-threshold-standard.md` — construction rules for derived indicators and alert systems.
- `docs/public-release-and-source-attribution-standard.md` — publication-grade release standards.
- `docs/out-of-time-validation-and-backtesting-standard.md` — evaluation protocol for pseudo-real-time testing.
- `docs/uncertainty-decomposition-and-confidence-band-standard.md` — confidence-band and uncertainty-reporting standards.
- `docs/repository-integration-and-validation-note.md` — repository-wide validation protocol.
- `docs/repository-map.md` — this inventory document.

## Analytical layer

- `analysis/startup-survival-nowcasting-empirical-design.md` — empirical design for startup-pipeline monitoring.
- `analysis/bay-area-business-applications-structural-patterns.md` — structural reading of county application flows.
- `analysis/bay-area-employer-formation-bridge-model.md` — translation from applications to employer-conversion proxies.
- `analysis/bay-area-county-concentration-and-scaling-patterns.md` — county asymmetries and concentration logic.
- `analysis/bay-area-startup-formation-cycle-2005-2024.md` — long-run cycle analysis.
- `analysis/bay-area-near-term-startup-scenario-framework.md` — scenario design for near-term inflow paths.
- `analysis/bay-area-startup-hazard-proxy-system.md` — upstream hazard-style monitoring system.
- `analysis/bay-area-county-turning-point-and-regime-shift-diagnostics.md` — turning-point and regime-shift diagnostics.
- `analysis/bay-area-real-time-nowcast-backtesting-framework.md` — pseudo-real-time forecast evaluation.
- `analysis/bay-area-county-resilience-scorecard-and-monitoring-system.md` — resilience and monitoring scorecard.

## Code layer

- `src/config.py` — geographic scope, path registry, and source manifest.
- `src/validate_public_data_inventory.py` — source manifest validation and coverage reporting.
- `src/ingest_public_startup_data.py` — source ingestion and standardization.
- `src/build_bay_area_foundation_panel.py` — foundation panel assembly.
- `src/compute_bay_area_application_features.py` — feature engineering from BFS history.
- `src/assemble_bay_area_employer_proxy_panel.py` — employer-conversion proxy assembly.
- `src/build_bay_area_reporting_tables.py` — report-ready table generation.
- `src/build_qcew_operating_cost_context.py` — labor-context extraction and diagnostics.
- `src/estimate_bay_area_nowcast_scenarios.py` — near-term scenario generation.
- `src/compute_bay_area_hazard_proxies.py` — hazard-style diagnostics.
- `src/detect_bay_area_regime_shifts.py` — turning-point and regime-shift detection.
- `src/backtest_bay_area_application_nowcasts.py` — historical backtesting framework.
- `src/build_bay_area_resilience_scorecard.py` — resilience scorecard generator.
- `src/run_local_repository_pipeline.py` — orchestrated pipeline runner.

## Data and outputs

- `data/raw/README.md` — source acquisition register and filename conventions.
- `data/processed/README.md` — rebuildable intermediate layer rules.
- `outputs/README.md` — derived output layer description.

## Tests and automation

- `tests/test_cli_files.py` — repository layout and CLI smoke tests.
- `tests/test_config_and_layout.py` — configuration and manifest validation.
- `.github/workflows/python-checks.yml` — continuous-integration checks.
