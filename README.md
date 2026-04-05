# Bay Area Startup Survival Engine

**Repository description:** A public-data research repository for measuring startup formation, projected employer conversion, county concentration, labor-market absorption, and operating context in the San Francisco Bay Area using U.S. Census Bureau and U.S. Bureau of Labor Statistics datasets.

This repository is designed as a serious analytical base for a multi-file GitHub project on Bay Area startups, entrepreneurial finance, operations, labor demand, and local ecosystem structure. The core logic is intentionally empirical: business applications proxy the top of the startup funnel; projected formations and later business dynamics proxy conversion and survival; county- and area-level labor data provide a partial operating environment; and geographic crosswalks allow consistent aggregation from county files to Bay Area definitions. The repository therefore focuses on reproducible transformations, defensible measurement, and explicit legal separation between original analytical work and third-party raw data.

The repository consists primarily of Markdown research notes and Python scripts. It **does not** redistribute the raw statistical files used to build the analysis. Raw data were downloaded from public institutional sources, stored locally, and processed through scripts that can be rerun by any reader with access to the same source files. This is intentional: the analytical structure is original work, while the underlying data remain subject to the conditions and ownership of the original institutions.

## Files in this repository

- `startup-data-governance-and-source-map.md` — Technical note defining the source hierarchy, local file inventory, legal treatment of raw data, and the measurement logic used in the project.
- `.gitignore` — Repository protection rules preventing accidental publication of raw data, derived outputs, local caches, and environment-specific artifacts.
- `src/ingest_public_startup_data.py` — Robust ingestion pipeline that standardizes the uploaded Census/BLS files into reusable processed tables.
- `src/build_bay_area_foundation_panel.py` — Analytical builder that converts the processed inputs into a Bay Area foundation panel, summary tables, and coverage diagnostics.

## Project scope

The current release is a **foundation pack**. It establishes the repository architecture, data provenance rules, and the first reproducible Python layer. The immediate analytical focus is the Bay Area startup funnel rather than a vague “startup success” narrative. That distinction matters. A business application is not a startup birth; a projected formation is not a realized employer firm; a county with more applications is not automatically more productive; and a venture hub can be financially vibrant while still exhibiting weak broad-based employer formation in selected sectors. The repository is therefore built to separate at least five stages:

1. **Applications** — early pipeline volume.
2. **Projected formations** — expected near-term conversion into employer businesses.
3. **Observed business dynamics** — births, deaths, job creation, and shutdowns once additional BDS files are added locally.
4. **Operating environment** — county/MSA labor and wage conditions from QCEW.
5. **Geographic concentration** — the distribution of Bay Area activity across the nine-county region.

With the currently uploaded files, the repository can already establish a strong empirical baseline. The annual county business-applications file implies that the nine-county Bay Area recorded **101,112** applications in 2023 and **97,505** in 2024, a decline of about **3.6%** year over year. Santa Clara County alone contributed **22,219** applications in 2024, while San Francisco County recorded **18,699**, Alameda County **19,498**, Contra Costa County **13,311**, and San Mateo County **9,497**. Together, Santa Clara and San Francisco accounted for roughly **42.0%** of Bay Area applications in 2024, while the full nine-county Bay Area represented about **18.9%** of all California county-level business applications in the same year. These numbers do not prove startup quality, but they immediately identify concentration, scale, and regional dependence.

The monthly BFS file provides a second, more timely signal. In the seasonally adjusted California series, total business applications were **57,033** in January 2026 and **50,221** in February 2026, while projected business formations within four quarters were **4,114** in February 2026. At the U.S. level, the same February 2026 release reports **496,443** business applications and **28,994** projected formations within four quarters. This makes California materially important in the national pipeline, but also underscores why any Bay Area-specific project must reconcile local annual county files with broader state and national monthly series instead of treating one file as a complete answer.

## How to use this project

- Use the Python scripts to rebuild a clean local analytical base after downloading the underlying files from the original public sources.
- Use the Markdown notes as a formal source-governance layer for investor memos, policy notes, academic assignments, and technical GitHub documentation.
- Extend the repository by adding BDS county/MSA files, SUSB, Nonemployer Statistics, patents, venture databases, or SEC/EDGAR event data without changing the repository’s legal logic.
- Keep raw data outside the public repository; rerun the scripts locally and publish only analytical outputs that do not violate source terms or personal data constraints.
- Treat the current release as the empirical infrastructure for later modules on survival analysis, financing concentration, labor-market absorption, and startup ecosystem optimization.

## References and data sources

The papers and scripts in this repository rely primarily on the following categories of sources:

[1] U.S. Census Bureau datasets and documentation, especially Business Formation Statistics (BFS), Business Dynamics Statistics (BDS), and metropolitan/county delineation files.  
[2] U.S. Bureau of Labor Statistics datasets and technical notes, especially the Quarterly Census of Employment and Wages (QCEW).  
[3] Public geographic reference tables used to map counties to metropolitan statistical areas and Bay Area definitions.  
[4] Local non-public raw extracts downloaded from the official sources above and processed through the repository scripts.  
[5] Later repository extensions may incorporate additional public filings, venture market reports, or patent data, but those are not redistributed here unless explicitly permitted.

## Copyright and reuse

The analytical text, file architecture, variable definitions, transformation logic, and indicator design in this repository are original work. The repository does **not** grant an open-source or Creative Commons license for full-text reuse of the analytical documents. Reasonable quotation for research, teaching, classroom presentation, private study, or internal business use is generally acceptable when proper attribution is given. Substantial reuse of the text, structure, or analytical framework should credit the author and, where feasible, be accompanied by a permission request. Nothing in this repository constitutes legal advice, and users remain responsible for verifying the reuse conditions of any third-party data source.

© 2026 Andrea Trenti. All rights reserved.  
• The analytical texts, tables and structure of the indicators are original works protected by copyright.  
• The underlying statistical data remain the property of their respective institutions (World Bank, IMF, industry associations, etc.) and are used exclusively for analytical and educational purposes.  
• No open-source or Creative Commons licence is granted for the full reuse of the texts; any substantial reuse requires the author’s permission.
