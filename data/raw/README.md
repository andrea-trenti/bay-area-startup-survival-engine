# Source Acquisition Register

This repository does not publish raw statistical source files. Instead, it documents the official source pages, the expected acquisition filenames, and the folder conventions required for replication.

## Core acquisition set

| Expected filename | Institution | Source page | Purpose |
|---|---|---|---|
| `bfs_monthly.csv` | U.S. Census Bureau | `https://www.census.gov/econ/bfs/present/index.html` | Monthly Business Formation Statistics time-series file. |
| `bfs_county_apps_annual.xlsx` | U.S. Census Bureau | `https://www.census.gov/econ/bfs/data/county.html` | Annual county business applications workbook. |
| `list1_2023.xlsx` | U.S. Census Bureau | `https://www2.census.gov/programs-surveys/metro-micro/geographies/reference-files/2023/delineation-files/list1_2023.xlsx` | July 2023 delineation file for county and metropolitan mapping. |
| `area-titles-csv.csv` | U.S. Bureau of Labor Statistics | `https://www.bls.gov/cew/classifications/areas/qcew-area-titles.htm` | QCEW area-code and area-title reference table. |

## Optional analytical extensions

| Suggested asset | Institution | Source page | Why it helps |
|---|---|---|---|
| Annual QCEW county and area CSV files for California/Bay Area geographies | U.S. Bureau of Labor Statistics | `https://www.bls.gov/cew/downloadable-data-files.htm` | Enables wage and employment context for Bay Area counties. |
| BDS county/MSA datasets by sector and age | U.S. Census Bureau | `https://www.census.gov/data/datasets/time-series/econ/bds/bds-datasets.html` | Extends the repository toward realized downstream business dynamics. |
| CBP county and MSA files | U.S. Census Bureau | `https://www.census.gov/programs-surveys/cbp/data/datasets.html` | Adds establishment structure and payroll context. |
| Nonemployer Statistics county/MSA files | U.S. Census Bureau | `https://www.census.gov/programs-surveys/nonemployer-statistics/data/datasets.html` | Extends coverage for nonemployer business activity. |
| SUSB files by MSA and industry | U.S. Census Bureau | `https://www.census.gov/programs-surveys/susb/data/datasets.html` | Adds employer-size and industry structure. |

## Acquisition conventions

1. Preserve institutional filenames when practical; otherwise rename files to the repository filenames listed above.
2. Store source files only in `data/raw/`.
3. Record the download date, original source URL, and file size or checksum in your own acquisition log.
4. Do not commit those files to GitHub.
5. Rebuild processed outputs after any source refresh.

## Attribution note

The repository may cite institutions, file titles, release dates, source pages, and dataset descriptions. It does not claim ownership of the underlying source files.
