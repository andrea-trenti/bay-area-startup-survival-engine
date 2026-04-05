PYTHON ?= python

.PHONY: help validate ingest foundation features nowcast risk scorecard pipeline test lint compile smoke clean

help:
	@echo "Available targets: validate ingest foundation features nowcast risk scorecard pipeline test lint compile smoke clean"

validate:
	$(PYTHON) src/validate_public_data_inventory.py

ingest:
	$(PYTHON) src/ingest_public_startup_data.py

foundation:
	$(PYTHON) src/build_bay_area_foundation_panel.py

features:
	$(PYTHON) src/compute_bay_area_application_features.py
	$(PYTHON) src/assemble_bay_area_employer_proxy_panel.py
	$(PYTHON) src/build_bay_area_reporting_tables.py

nowcast:
	$(PYTHON) src/estimate_bay_area_nowcast_scenarios.py
	$(PYTHON) src/backtest_bay_area_application_nowcasts.py

risk:
	$(PYTHON) src/compute_bay_area_hazard_proxies.py
	$(PYTHON) src/detect_bay_area_regime_shifts.py

scorecard:
	$(PYTHON) src/build_bay_area_resilience_scorecard.py

pipeline:
	$(PYTHON) src/run_local_repository_pipeline.py

lint:
	ruff check .

compile:
	$(PYTHON) -m compileall src tests

smoke:
	$(PYTHON) src/run_local_repository_pipeline.py --dry-run

test:
	pytest

clean:
	rm -rf .pytest_cache .ruff_cache
