# Processed Data

This directory is reserved for rebuildable intermediate tables created by the ingestion and transformation scripts. Its contents are intentionally excluded from Git because they can be regenerated from the source-acquisition layer documented in `data/raw/README.md`.

Typical contents include:
- standardized BFS monthly tables,
- annual county application panels,
- geography crosswalk extracts,
- QCEW coverage diagnostics,
- Bay Area feature panels,
- employer-conversion proxy tables.

These files are derived intermediate tables excluded from version control and reproducible from the documented source layer.
