# Bay Area Geographic Scope and FIPS Governance

## Abstract

This note fixes the geographic boundary of the project and converts a vague regional label into a reproducible identifier system. The repository uses a **primary analytical boundary** equal to the official nine-county Bay Area used by the Metropolitan Transportation Commission (MTC): Alameda, Contra Costa, Marin, Napa, San Francisco, San Mateo, Santa Clara, Solano, and Sonoma Counties [1]. The note also records the relevant Census metropolitan and combined statistical area codes needed when the analysis shifts from county-level business applications to metro-level business dynamics or labor-market series [2][3].

The central methodological point is that “Bay Area” is not a single universally interchangeable geography. For startup formation, county-level identifiers are preferred because the public annual county Business Formation Statistics (BFS) workbook is directly county based [4]. For certain establishment and labor-market statistics, official metro or CSA definitions become useful; however, they should be treated as **secondary aggregation layers**, not as replacements for the nine-county baseline. Failure to distinguish these layers introduces silent scope drift, especially when Santa Cruz, San Benito, or Stockton-area counties are inadvertently pulled into broad CSA-based calculations [1][2].

## 1. Purpose

The repository is designed to support formal empirical work on startup formation, projected employer conversion, operating conditions, and eventual survival proxies in the U.S. innovation economy, with a primary regional emphasis on the Bay Area. For this purpose, every downstream script, table, and paper must inherit a stable geographic contract. The contract adopted here is:

1. **Default region for “Bay Area”**: the nine counties recognized by MTC [1].
2. **Default atomic unit**: county FIPS.
3. **Secondary aggregation layers**: Census MSAs and CSA identifiers, used only when the source data are not available at county level or when metro comparability is analytically superior [2][3].
4. **No implicit boundary switching**: any move from county to metro or CSA must be declared in the text and encoded in the script configuration.

## 2. Primary analytical boundary

### 2.1 Official nine-county Bay Area

MTC states that the Bay Area consists of nine counties [1]. The repository uses the following canonical list.

| County | State FIPS | County FIPS | Full county code | QCEW `area_fips` | Notes |
|---|---:|---:|---|---|---|
| Alameda County | 06 | 001 | 06001 | `06001` | East Bay core county |
| Contra Costa County | 06 | 013 | 06013 | `06013` | East Bay outer county |
| Marin County | 06 | 041 | 06041 | `06041` | North Bay |
| Napa County | 06 | 055 | 06055 | `06055` | North Bay / wine cluster |
| San Francisco County | 06 | 075 | 06075 | `06075` | Urban core |
| San Mateo County | 06 | 081 | 06081 | `06081` | Peninsula |
| Santa Clara County | 06 | 085 | 06085 | `06085` | Silicon Valley core |
| Solano County | 06 | 095 | 06095 | `06095` | North/East Bay fringe |
| Sonoma County | 06 | 097 | 06097 | `06097` | North Bay |

The practical advantage of this definition is that it is transparent, politically and institutionally recognized, and directly compatible with county-based BFS and QCEW source files [1][4][5].

### 2.2 Why counties are the primary layer

County identifiers are superior for the baseline repository because:

- the annual county BFS workbook publishes business applications by county code directly [4];
- QCEW area files are natively keyed by county `area_fips` values [5][6];
- county FIPS are stable keys for merges, crosswalks, and reproducible filtering;
- the county layer allows explicit treatment of within-region concentration rather than collapsing the Bay Area into a single metro number.

This matters empirically because startup activity is highly concentrated within the region. In the BFS county annual file, the nine-county Bay Area recorded **97,505** business applications in 2024, of which **22.8%** came from Santa Clara County, **20.0%** from Alameda County, and **19.2%** from San Francisco County; the top three counties therefore accounted for **62.0%** of the regional total [4].

## 3. Secondary statistical areas

### 3.1 Relevant metro and combined statistical areas

The official Census delineation file and the BLS area-title lookup identify the principal metro and CSA codes relevant to the Bay Area [2][5]:

| Statistical area | Code | Source coding style | Role in the repository |
|---|---|---|---|
| San Francisco-Oakland-Fremont, CA MSA | 4186 | BLS `C4186` | Secondary metro layer for urban core comparisons |
| San Jose-Sunnyvale-Santa Clara, CA MSA | 4194 | BLS `C4194` | Secondary metro layer for Silicon Valley comparisons |
| San Jose-San Francisco-Oakland, CA CSA | 488 | BLS `CS488` | Broad combined area, used sparingly |
| Napa, CA MSA | 3490 | BLS `C3490` | Separate North Bay metro component |

The Census 2023 delineation file also places Santa Cruz-Watsonville and other adjacent metros inside the broader CSA framework [2]. Those geographies are analytically useful for commuting-system or innovation-belt questions, but they are **not** part of the default nine-county Bay Area boundary.

### 3.2 Scope contamination risk

The repository distinguishes three nested concepts:

- **Bay Area (default)**: nine MTC counties.
- **Core Bay Area metros**: San Francisco-Oakland-Fremont and San Jose-Sunnyvale-Santa Clara.
- **Broad Bay Area CSA**: San Jose-San Francisco-Oakland CSA, which may include additional counties or adjacent metros.

If a script silently substitutes CSA coverage for the nine-county baseline, startup counts, wages, and establishment totals can change materially. The result is not a minor formatting issue but a change in the unit of analysis. Every file must therefore state which geography is active.

## 4. Identifier architecture

### 4.1 Canonical keys

The following key conventions are mandatory:

- `state_fips`: two-character string, zero-padded.
- `county_fips`: three-character string, zero-padded.
- `county_geoid`: five-character concatenation `state_fips + county_fips`.
- `area_fips`: BLS area code, stored as string to preserve leading zeros and alphanumeric metro codes.
- `cbsa_code`, `csa_code`: stored as string in processed outputs to avoid accidental numeric coercion.

### 4.2 Merge precedence

When two files contain overlapping identifiers, the merge order is:

1. `county_geoid` or `area_fips` direct match.
2. Explicit crosswalk built from Census `list1_2023.xlsx`.
3. Title-based matching only as a last-resort validation step, never as the primary merge key.

### 4.3 Name normalization rule

County and area titles should be preserved in human-readable outputs, but scripts must never rely on names as the join key. Examples:

- `San Francisco County, California` (BLS title)
- `San Francisco County` (Census workbook label)
- `San Francisco-Oakland-Fremont, CA MSA` (BLS metro title)

These strings are descriptive labels, not stable IDs.

## 5. Analytical implications

The geographic contract influences model design directly.

### 5.1 Formation analysis

Use county BFS annual applications as the regional backbone because county variation is a feature, not a nuisance. County-level modeling allows the project to measure concentration, spatial persistence, and diffusion from core technology counties to adjacent counties [4].

### 5.2 Employer conversion and survival

Projected employer formations in BFS are not county-level in the monthly file; they are published at national, regional, and state frequency in the main monthly release [7][8]. The correct design is therefore:

- county annual applications for within-region allocation;
- California monthly formation signals for timing and cyclical adjustment;
- later BDS/QCEW integration for realized employer and establishment dynamics.

### 5.3 Labor-market context

QCEW should enter the repository at county level whenever the relevant Bay Area county files are available, because wage and establishment structure differ materially between Santa Clara, San Francisco, Alameda, and the northern counties [5][6]. Metro-level aggregation is useful for benchmark comparisons against peer hubs, but the county layer should remain the default within-region operating lens.

## 6. Governance rules for all future files

Every future Markdown note, script, notebook, figure, or table must obey the following rules:

1. The phrase **Bay Area** means the nine MTC counties unless explicitly redefined.
2. Any departure from the nine-county boundary must be declared in the first methodology section.
3. Any `area_fips` or Census area code used in code must be shown in a machine-readable dictionary.
4. Any county omitted because of missing source files must be flagged as a coverage issue, not silently dropped.
5. Title-based joins are prohibited in production outputs when a FIPS-based crosswalk is available.

## 7. Conclusion

A serious startup-formation repository cannot tolerate geographic ambiguity. The Bay Area is widely discussed as a single innovation ecosystem, but public data arrive through county, metro, and CSA containers that are not interchangeable. The correct design choice is to treat the nine-county region as the legal and analytical baseline, retain county FIPS as the canonical join key, and use metro or CSA codes only as explicitly declared secondary layers. This keeps the repository reproducible, defensible, and suitable for later expansion into survival and operating-economics work.

## References

[1] Metropolitan Transportation Commission — *What Is MTC?*, institutional page describing the nine-county San Francisco Bay Area, accessed 2026.

[2] U.S. Census Bureau — *List 1. Core Based Statistical Areas, Metropolitan Divisions, and Combined Statistical Areas, July 2023*, delineation file, 2023.

[3] U.S. Census Bureau — *Metropolitan and Micropolitan Delineation Files*, program documentation, 2026.

[4] U.S. Census Bureau — *County Level Business Applications*, annual county BFS workbook, 2005–2024, dataset.

[5] U.S. Bureau of Labor Statistics — *QCEW area titles CSV* and downloadable area definitions, dataset support files.

[6] U.S. Bureau of Labor Statistics — *Guide to QCEW Data Sources* and *NAICS-Based Annual CSV Layout*, methodology and file-layout documentation.

[7] U.S. Census Bureau — *Business Formation Statistics: Methodology*, technical documentation, 2026.

[8] U.S. Census Bureau — *Business Formation Statistics Monthly Release / Current PDF*, 2026 release note and data description.
