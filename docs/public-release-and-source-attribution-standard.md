# Public Release and Source Attribution Standard
## Repository controls for non-redistribution of third-party raw data and formal source handling

## Purpose
This standard governs how the repository is published in public form while relying on third-party institutional datasets that are downloaded, stored, and processed within the acquisition layer. The project is designed to separate original analytical work from raw statistical material produced by public agencies. That separation is not cosmetic. It is the legal and methodological foundation of the repository.

The project therefore publishes original Markdown analysis, code, indicator definitions, processing logic, and derived non-substitutive summaries, but does not publish downloaded raw source files in the version-controlled repository unless a source's own terms permit redistribution and such redistribution is intentionally chosen. The default rule in this project is stricter: raw data remain outside the public repository.

## Publication architecture
The repository is built around four layers:

1. **Source layer** — external institutional files downloaded from official providers.
2. **Local processing layer** — scripts that standardize, validate, and transform those files.
3. **Analytical layer** — Markdown documents, methods notes, and generated summary tables.
4. **Public release layer** — the GitHub repository excluding source files retained outside version control and machine-specific artifacts.

Only layers 2 through 4 are intended for publication by default.

## Non-redistribution rule
The repository must not re-upload or mirror the institutional files that were manually downloaded from public providers unless a deliberate release decision is taken after verifying source terms. The default operational rule is therefore:

- raw input files are stored in the acquisition layer,
- raw input directories are excluded through `.gitignore`,
- the public repository documents provenance and acquisition paths,
- readers are instructed how to obtain the files directly from the original institutions.

This rule preserves source integrity, reduces unnecessary duplication, and avoids turning the repository into an unofficial data mirror.

## What may be published
The following categories are publishable by default:
- original analytical Markdown files,
- original Python scripts,
- derived metadata inventories that do not substitute for the original source files,
- compact summary tables that are clearly transformative and analytically embedded,
- file manifests and provenance notes,
- methodological documentation.

The following categories should remain private by default:
- downloaded raw CSV, XLSX, TXT, ZIP, and extracted institutional files,
- bulk intermediary tables that materially reproduce the source,
- non-versioned caches and intermediate processing artifacts,
- personal environment files.

## Source attribution standard
Every analytical file using third-party data must identify, at minimum:
1. the institution,
2. the dataset title or description,
3. the release year or release window if known,
4. the type of source (dataset, delineation file, statistical bulletin, reference table),
5. the role of the source in the analysis.

A citation is adequate only if a competent reader can identify the upstream source family from the text.

## Required wording for raw-data separation
Where appropriate, repository files should communicate the following meaning in professionally varied language:
- the raw institutional data were downloaded from official sources,
- those raw files are intentionally not included in the public GitHub repository,
- the repository provides the processing logic and source references needed to reproduce the analysis from independently acquired source files.

This statement should appear in the README, in data-governance notes, and in any methodological file that a reader is likely to consult first.

## Transformative-output rule
Derived tables may be published only when they are meaningfully transformed relative to the source. A publishable derived table generally satisfies at least one of the following conditions:
- it aggregates multiple source fields into a new indicator,
- it combines multiple public sources into a new analytical construct,
- it encodes methodological judgment not present in the source,
- it is too compact to substitute for the underlying raw file.

By contrast, a simple re-export of a downloaded source file under a different name is not publishable under this repository standard.

## Documentation minimums for each public release
Each public release should contain enough information for an informed reader to understand:
- what the release adds relative to prior repository versions or prior public snapshots,
- which raw source families are assumed in the background,
- what the scripts produce,
- which outputs are controlled versus production-ready,
- which limitations follow from missing source families in the acquisition layer.

## Source-coverage contingency rule
This repository permits modular replication. When the acquisition layer does not include every optional source family:
- scripts must degrade gracefully,
- missing-target reports should be produced instead of hard failure where feasible,
- analytical notes must distinguish observed evidence from intended future enrichment,
- no claim should imply that a missing dataset was fully observed if it was not.

## Formal attribution examples
Appropriate references include formulations such as:
- U.S. Census Bureau annual county business-applications dataset.
- U.S. Census Bureau and OMB CBSA delineation reference file.
- U.S. Bureau of Labor Statistics QCEW annual by-area files.

What should be avoided:
- vague phrases such as “public files from the internet,”
- unattributed figures or tables,
- raw data embedded in screenshots without source metadata,
- copied tables without institutional identification.

## Copyright and ownership logic
The repository owner may assert copyright over:
- original explanatory text,
- original methodological structuring,
- original score construction and indicator architecture,
- code written for ingestion, validation, transformation, and analysis,
- the structure and sequencing of the repository.

The repository owner should not claim ownership over:
- the underlying public statistics produced by third-party institutions,
- dataset naming conventions created by source agencies,
- the agencies' original metadata or methodology text.

## Practical repository controls
Minimum public-repository controls should include:
- a restrictive `.gitignore` for raw data directories and archives,
- clear folder separation between `data/`, `outputs/`, `analysis/`, and `src/`,
- comments in scripts explaining expected acquisition-layer file paths,
- analytical notes that distinguish data source, transformation, and inference.

## Conclusion
A strong public research repository is not a raw-data dump. It is a transparent analytical system with clear provenance, reproducible logic, and disciplined publication boundaries. This standard ensures that the repository remains technically serious, legally careful, and academically credible while still being reproducible by readers who obtain the same source files from the official providers.
