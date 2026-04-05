# Repository Validation Protocol

## Scope

This note records the integration logic of the consolidated public repository and the execution checks performed before release. Its purpose is procedural: a repository of this kind should demonstrate path stability, cross-script compatibility, and clean separation between source-data ownership and original analytical work.

## Consolidation logic

The published repository integrates the published analytical and infrastructure layers into one coherent structure. Four repository-wide corrections were applied during consolidation:

1. **Pack-specific wrappers were removed.** All substantive files now live directly in `docs/`, `analysis/`, `src/`, `data/`, and `outputs/`.
2. **Repository-relative defaults were standardized.** Scripts now resolve paths through the repository root rather than through delivery-specific folders.
3. **Geographic constants were centralized.** Bay Area county scope and the core file manifest are defined in `src/config.py`.
4. **Execution controls were formalized.** The repository now includes a `Makefile`, `pyproject.toml`, a minimal test suite, and a GitHub Actions workflow.

## Validation protocol

Validation was performed in a controlled replication environment assembled from official public releases. The validation objective was twofold:

- confirm that the repository executes cleanly when the core Census/BLS files are present;
- confirm that optional source families generate explicit coverage diagnostics when unavailable or geographically non-matching.

The validation environment included a BFS monthly file, a BFS annual county workbook, a metropolitan delineation file, a BLS area-title crosswalk, and a heterogeneous QCEW subset sufficient for parser verification and conditional-execution testing.

## Execution checks completed

The following scripts were executed successfully under the consolidated structure:

- `src/validate_public_data_inventory.py`
- `src/ingest_public_startup_data.py`
- `src/build_bay_area_foundation_panel.py`
- `src/compute_bay_area_application_features.py`
- `src/assemble_bay_area_employer_proxy_panel.py`
- `src/build_bay_area_reporting_tables.py`
- `src/build_qcew_operating_cost_context.py`
- `src/estimate_bay_area_nowcast_scenarios.py`
- `src/compute_bay_area_hazard_proxies.py`
- `src/detect_bay_area_regime_shifts.py`
- `src/backtest_bay_area_application_nowcasts.py`
- `src/build_bay_area_resilience_scorecard.py`

Intermediate and output artifacts created during validation were removed from the public release folder so that the GitHub repository remains consistent with the non-redistribution policy for source-dependent files.

## Interpretation

The completed checks support four conclusions.

First, the folder structure is internally coherent.  
Second, the scripts no longer depend on delivery-specific paths.  
Third, optional layers surface explicit diagnostics rather than hidden substitutions.  
Fourth, the repository can be published as a clean public shell while remaining fully usable by anyone who independently downloads the documented source files.

## Boundary

Successful validation does not imply uniform source coverage across independent replications. Labor-context outputs, for example, depend on the presence of geographically corresponding QCEW files in the acquisition layer. The repository exposes such coverage boundaries explicitly and treats them as part of the evidence chain.
