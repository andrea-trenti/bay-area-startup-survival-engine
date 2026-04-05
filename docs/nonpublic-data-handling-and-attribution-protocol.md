# Nonpublic Data Handling and Source Attribution Protocol
## Repository rules for raw-file exclusion, reproduction, and lawful attribution

## Abstract
This repository is intentionally designed so that the published GitHub project contains analytical text, scripts, and reproducibility instructions, but not the raw data files downloaded from official external institutions. The rationale is both legal and practical. Many underlying files remain the property of the institutions that publish them; some are large, subject to revision, or inconvenient to redistribute within a lightweight academic repository. The correct architecture is therefore public code and documentation with a non-versioned source-data layer retained outside repository version control.

This protocol defines how source files should be acquired, stored, referenced, and cited. It also defines how tables and figures should disclose provenance. The goal is not merely compliance. A rigorous attribution and nonredistribution standard improves auditability, reduces accidental version drift, and makes the repository more legible to professors, hiring teams, investors, and policy audiences.

## 1. Repository principle
The repository owner publishes:

- original analytical Markdown documents;
- original Python scripts and directory logic;
- source maps, manifests, and citation standards;
- derived outputs generated from source files retained outside version control, where such outputs do not recreate proprietary or institutionally controlled bulk datasets.

The repository owner does **not** publish:

- the raw BFS, CBP, QCEW, or other downloaded source files themselves;
- mirrored copies of institutionally maintained datasets;
- large derivative tables that effectively substitute for the original datasets when those originals remain controlled by the source institution.

## 2. Local data architecture
The expected repository architecture is:

```text
project-root/
├── README.md
├── docs/
├── analysis/
├── src/
├── data/
│   ├── raw/
│   │   ├── bfs/
│   │   ├── qcew/
│   │   ├── cbp/
│   │   └── geography/
│   ├── interim/
│   └── derived/
└── outputs/
```

The `data/raw/` tree is ignored by Git. It exists only on the analyst's machine. Scripts should read from `data/raw/` if available and otherwise fall back to user-provided paths or emit explicit error messages.

## 3. Attribution rule for every figure and table
Every figure, chart, table, or derived CSV produced from external data should carry a provenance note in one of the following forms.

### 3.1 Figure note template
> **Source:** Author's calculations from U.S. Census Bureau Business Formation Statistics annual county file, downloaded from the official Census website; geographic mapping from the July 2023 CBSA delineation file.

### 3.2 Table note template
> **Notes:** Counts refer to business applications, not venture-backed startups. County-level annual values may incorporate Census disclosure-avoidance procedures. Raw source files are not redistributed in this repository and must be downloaded from the original institutions.

### 3.3 Script header template
Each Python file should begin with a short header block containing:

- analytical purpose,
- expected input files,
- output objects,
- redistribution note.

A compliant example:

```python
"""
Build Bay Area business-application scenario tables from source files acquired separately from official public releases.
Expected inputs are external raw files stored outside version control.
No raw institutional data are redistributed by this repository.
"""
```

## 4. Citation standard inside Markdown papers
Markdown papers in this repository use a numbered references section. Citations should identify:

1. institution or author,
2. short title,
3. year if available,
4. source type,
5. URL where the data or methodological note was obtained.

When the raw file itself is not hosted in the repository, the text should say so explicitly. Example:

> The underlying annual county file is retained only in the non-versioned acquisition layer and is not redistributed in the GitHub repository; the official download location is listed in the references section.

## 5. Legal and practical rationale for excluding raw data
### 5.1 Institutional ownership
The analytical text and repository structure are original intellectual output. The underlying statistical files remain the property of their respective institutions. Redistributing raw files can create unnecessary ambiguity around ownership, version control, and terms of use.

### 5.2 Revision risk
Official data products are revised. BFS county annual counts were updated in June 2025 to add 2024 and revise earlier years.[1] A repository that mirrors raw files risks becoming stale or internally inconsistent if future scripts are run against newer institutional releases.

### 5.3 Repository hygiene
Public repositories used for academic or professional signaling should remain lightweight, transparent, and reproducible. Publishing scripts plus precise source links is typically superior to uploading large external raw files.

## 6. Required legal notice for the README
The main README should contain both a plain-English reuse summary and the fixed legal block requested for this project. The legal block must remain verbatim. That requirement is not stylistic; it creates consistency across future repository extensions and prevents accidental dilution of the reuse standard.

## 7. Required `.gitignore` logic
At minimum, the following patterns should remain excluded from version control:

```gitignore
# Raw and derived data
/data/raw/
/data/interim/
/data/derived/
/outputs/

# Python cache and virtual environments
__pycache__/
*.pyc
.venv/
.env/

# Notebook checkpoints
.ipynb_checkpoints/
```

## 8. Provenance register standard
For each major source file, the repository should maintain a simple register either in Markdown or CSV with the following columns:

- `source_group`
- `official_institution`
- `official_title`
- `download_url`
- `download_date`
- `local_filename`
- `redistributed_in_repo` (always `no` for raw files)
- `notes`

This register should never contain the raw data itself. It exists to make the acquisition process auditable.

## 9. What may be shared publicly
The following are normally acceptable for public sharing:

- compact derived summary tables created by the analyst;
- model coefficients estimated from public data;
- charts that do not substitute for the full raw dataset;
- explanatory notes on methodology and variable construction;
- scripts that require the user to download raw files independently.

The following should generally remain outside version control unless the institution explicitly allows convenient redistribution and the repository owner chooses to do so:

- full downloaded raw CSV or XLSX bundles;
- mirrored archives of official ZIP packages;
- machine-readable large extracts that recreate the underlying dataset in full.

## 10. Practical wording standard for the repository
Whenever the repository refers to the missing raw-data layer, the wording should be direct and formal. Recommended wording:

> Raw source files are intentionally excluded from version control. The repository provides analytical documentation, code, and exact source references, but users must download the underlying institutional files directly from the original publishers.

This wording is clear, accurate, and professionally legible.

## 11. Conclusion
A high-quality academic repository is not improved by indiscriminate data dumping. It is improved by explicit provenance, auditable transformations, lawful attribution, and a clean separation between the analyst's original work and the institutions' raw statistical products. This protocol operationalizes that separation. It should remain binding across all future repository extensions added to this project.

## References
[1] U.S. Census Bureau — Business Formation Statistics, official release page noting annual county update and revisions, https://www.census.gov/econ/bfs/index.html.

[2] U.S. Census Bureau — Business Formation Statistics annual county data page, official data-access page, https://www.census.gov/econ/bfs/data/county.html.

[3] U.S. Bureau of Labor Statistics — Quarterly Census of Employment and Wages, official overview page, https://www.bls.gov/cew/.

[4] U.S. Census Bureau — County Business Patterns, official product page, https://www.census.gov/programs-surveys/cbp.html.
