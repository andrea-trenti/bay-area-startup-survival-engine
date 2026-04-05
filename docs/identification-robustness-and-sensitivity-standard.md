# Identification, Robustness, and Sensitivity Standard
## Empirical standards for a public-data startup formation repository

## Abstract
This document defines the identification, robustness, and sensitivity rules that govern empirical claims in this repository. The central constraint is structural: the project relies on public administrative aggregates rather than private startup microdata. As a result, the repository is designed to identify regularities in business formation, projected employer conversion, geographic concentration, and operating-cost context, but not to recover causal firm-level treatment effects. The correct empirical posture is therefore disciplined inference rather than causal overreach.

The core data spine combines Business Formation Statistics (BFS), annual county business-application counts, County Business Patterns (CBP), and the Quarterly Census of Employment and Wages (QCEW). BFS are based on IRS EIN applications and Census administrative infrastructure, begin in July 2004, and include business applications as well as actual and projected employer formations within four and eight quarters.[1][2] The annual county series applies disclosure-avoidance noise and calibration constraints at the county level, which is analytically acceptable for regional trend work but requires explicit sensitivity treatment whenever county-level year-over-year differences are interpreted.[3]

The purpose of this standard is to make the repository defensible in an academic, policy, or investor-facing setting. Every load-bearing statement must be classed as either descriptive, predictive, or structural. Descriptive statements summarize observed aggregates. Predictive statements estimate short-horizon paths from observed historical series. Structural statements explain why regional outcomes may differ across counties or time. Only the first two can be directly supported from the core public-data architecture; the third requires disciplined use of theory, cross-dataset triangulation, and clearly labeled caveats.

## 1. Introduction
A repository built on public startup-related aggregates faces a familiar problem: the data are unusually broad, timely, and credible, but the underlying economic object is not the startup in the venture-capital sense. BFS track business applications for EINs and projected transitions into employer firms, which is a stronger signal than raw firm registrations yet still broader than venture-backed company formation.[1][2] CBP and QCEW describe employer establishments, payroll, employment, and wages, but they do so at the establishment and industry level rather than the startup financing level.[4][5]

This does not weaken the project if the inferential target is defined correctly. The repository should answer questions such as: how concentrated is new business application activity within the Bay Area; how persistent are county application shares across cycles; what range of 12- to 24-month employer conversion is consistent with the public data; and how should observed wage and establishment structures be interpreted as operating context rather than as direct startup outcomes. It does not directly measure startup quality, venture return potential, founder productivity, or the causal effect of county or regional policy on startup success.

## 2. Data-generating processes and inferential boundaries
### 2.1 Business Formation Statistics
BFS provide timely and high-frequency data on business applications and employer formations originating from those applications.[1][2] The monthly series begin in July 2004 and are available nationally, regionally, and by state; county-level annual counts are also available.[2][3] The relevant series include:

- $BA$: business applications.
- $BF4Q$: employer businesses formed within four quarters of application.
- $PBF4Q$: projected employer businesses formed within four quarters when realized payroll observations are not fully observed within the relevant release window.
- $SBF4Q$: the spliced series that combines $BF4Q$ and $PBF4Q$.[2]

The key implication is that $BA$ is a leading signal of entrepreneurial initiation, but not every application becomes an employer business. Therefore, any startup-nowcasting framework should distinguish between initiation intensity and realized employer conversion.

### 2.2 County annual counts and disclosure avoidance
For annual county business applications, the Census Bureau injects differentially private geometric noise into county counts, rounds negative values to zero, and calibrates county counts to published state totals.[3] This means the county series are usable for broad trend and concentration analysis, but small year-over-year changes at the county level should not automatically be treated as economically meaningful. The signal-to-noise ratio is materially higher when the analyst:

1. aggregates across multiple Bay Area counties,
2. compares multi-year averages rather than isolated annual deltas,
3. evaluates shares and concentration measures rather than raw low-level counts,
4. uses scenario bands rather than pseudo-precise point forecasts.

### 2.3 Employer establishment datasets
CBP provides annual subnational employer-establishment data including establishments, employment during the week of March 12, first-quarter payroll, and annual payroll.[4][5] QCEW publishes quarterly counts of employment and wages reported by employers and covers more than 95 percent of U.S. jobs.[6] These are not startup datasets. They should be treated as operating-environment datasets that proxy labor-cost intensity, sector depth, and employer ecosystem thickness.

## 3. Claim taxonomy
Every empirical claim in this repository should be assigned to one of the following classes.

### 3.1 Descriptive claims
A descriptive claim summarizes observed public aggregates and requires no structural interpretation beyond definitional accuracy. Example:

> Bay Area annual business applications rose from 50,602 in 2005 to 97,505 in 2024 in the repository's nine-county definition, implying a nominal count increase of 92.7 percent and a compound annual growth rate of roughly 3.5 percent over the full period.

This is descriptive because it simply aggregates county counts from the annual BFS county file.

### 3.2 Predictive claims
A predictive claim extrapolates from the historical series. These claims are allowed when the model is transparent, the forecast horizon is short, and scenario bands are reported. Example:

> A central scenario based on blended structural and recent growth rates yields a 2025 Bay Area application range near 101,000-102,000, while a conservative scenario that carries forward the latest negative year-over-year shock yields a level closer to 94,000.

This is predictive because it uses historical counts and explicit growth assumptions.

### 3.3 Structural claims
A structural claim explains *why* patterns occur. Structural claims must be framed as mechanisms, not as proven causal effects. Example:

> Counties with deeper private payroll bases and denser employer ecosystems may absorb entrepreneurial inflows more efficiently because founders can hire from thicker labor markets and contract against more specialized service providers.

This is structural and must always be paired with caveats because the present data do not identify the causal pathway directly.

## 4. Baseline empirical framework
### 4.1 Aggregate startup-initiation equation
Let $BA_{c,t}$ denote annual business applications in county $c$ and year $t$. The Bay Area aggregate is:

$$
BA^{BA}_{t} = \sum_{c \in \mathcal{C}_{BA}} BA_{c,t}
$$

where $\mathcal{C}_{BA}$ is the nine-county Bay Area set used in this repository: Alameda, Contra Costa, Marin, Napa, San Francisco, San Mateo, Santa Clara, Solano, and Sonoma.

The county share is:

$$
s_{c,t} = \frac{BA_{c,t}}{\sum_{j \in \mathcal{C}_{BA}} BA_{j,t}}
$$

and concentration may be summarized by a Herfindahl-Hirschman style index:

$$
HHI_t = 10{,}000 \times \sum_{c \in \mathcal{C}_{BA}} s_{c,t}^{2}
$$

### 4.2 Scenario engine
The repository's short-horizon forecast discipline uses three growth concepts:

- structural growth, estimated from a longer pre-pandemic horizon,
- recent growth, estimated from the most recent multi-year window,
- shock carry-forward, estimated from the latest year-over-year observation.

If $g^{struct}$ is the structural rate, $g^{recent}$ the recent rate, and $g^{shock}$ the latest annual shock, then the central scenario can be written as:

$$
g^{central} = 0.5 g^{struct} + 0.5 g^{recent}
$$

while the conservative scenario may be written as:

$$
g^{cons} = \min(g^{struct}, g^{shock})
$$

and the upside scenario as:

$$
g^{up} = \max(g^{central}, g^{post})
$$

where $g^{post}$ is a post-2020 recovery CAGR. The point is not that these weights are uniquely correct, but that they are explicit, auditable, and reproducible.

## 5. Robustness protocol
### 5.1 Time-window robustness
All trend-based conclusions should be tested on at least three windows:

- full history: 2005-2024,
- pre-pandemic benchmark: 2005-2019,
- post-shock window: 2020-2024.

A conclusion is **time-window robust** if its sign and broad magnitude survive all three windows.

### 5.2 Geographic-definition robustness
Bay Area definitions vary in practice. The repository standard is the nine-county MTC-style Bay Area. Robustness checks should also consider:

- Bay Area core five: Alameda, San Francisco, San Mateo, Santa Clara, Contra Costa,
- official CBSA mapping without manual exclusion,
- Bay Area plus San Benito where the San Jose CBSA delineation includes it.[7]

A conclusion is **geographically robust** if it survives the inclusion or exclusion of San Benito and other peripheral counties.

### 5.3 Metric robustness
Whenever possible, claims should be checked across at least two related metrics:

- level and share,
- year-over-year growth and multi-year CAGR,
- application counts and projected employer-conversion proxies,
- total payroll and average wage.

### 5.4 Disclosure-avoidance robustness
County annual BFS counts are protected by differentially private noise.[3] For that reason:

- avoid over-interpreting single-county one-year changes below roughly low double-digit percentage ranges unless corroborated by neighboring counties or multi-year persistence;
- prefer county rankings, share distributions, or rolling averages;
- treat reversals in very small counties as fragile evidence.

## 6. Sensitivity classification of conclusions
The repository should use four labels.

### 6.1 Strong
A result is **strong** if it is visible in aggregated Bay Area totals, survives alternative windows, and is not dependent on a single county.

### 6.2 Moderate
A result is **moderate** if it survives most but not all windows or depends on a small subset of counties with high economic weight.

### 6.3 Fragile
A result is **fragile** if it depends on one-year county-level noise, narrow subsamples, or limited QCEW coverage within the assembled source-acquisition layer.

### 6.4 Provisional
A result is **conditional** if it depends on a source family that is not represented in the relevant Bay Area acquisition layer.

## 7. Interpretation discipline
Three recurring errors must be avoided.

### 7.1 Startup-vs-business conflation
Not every EIN application is a venture-scale startup. BFS are broader than venture-backed formation. The repository can model entrepreneurial intensity, not venture success directly.[1][2]

### 7.2 Establishment-vs-firm conflation
CBP and QCEW are establishment-centric. A multi-establishment company may appear in multiple places, while a startup may initially have only one establishment.[4][5][6]

### 7.3 Payroll-vs-cost conflation
Average weekly wages and payroll totals are useful labor-cost proxies, but they are not complete startup cost measures. Rent, compute, legal, compliance, and customer-acquisition costs remain outside the core repository evidence base.

## 8. Practical standard for repository outputs
A repository output should meet the following minimum standard before being treated as publication-ready:

1. It names the raw source file or official source URL.
2. It defines the county universe explicitly.
3. It states whether the result is descriptive, predictive, or structural.
4. It specifies whether the result is strong, moderate, fragile, or conditional.
5. It avoids false precision in forecast outputs.
6. It separates operating-context evidence from startup-outcome evidence.

## 9. Conclusion
The strength of this repository is breadth, transparency, and reproducibility. The weakness is that public administrative startup proxies do not identify firm-level venture outcomes. The correct methodological response is not to dilute ambition but to sharpen definitions. Aggregated BFS data are powerful for measuring entrepreneurial initiation and broad employer-conversion tendencies. CBP and QCEW are powerful for characterizing the employer environment into which startups are born. Together they support serious regional analysis, provided the analyst clearly separates observation, prediction, and mechanism.

## References
[1] U.S. Census Bureau — Business Formation Statistics: Definitions, official definitions page, https://www.census.gov/econ_file/econ/bfs/definitions.html.

[2] U.S. Census Bureau — Business Formation Statistics: Methodology, official methodology page, https://www.census.gov/econ/bfs/methodology.html.

[3] U.S. Census Bureau — Business Formation Statistics Technical Documentation: Methodology, county disclosure-avoidance notes, https://www.census.gov/econ/bfs/technicaldocumentation/methodology.html.

[4] U.S. Census Bureau — County Business Patterns, official product page, https://www.census.gov/programs-surveys/cbp.html.

[5] U.S. Census Bureau — County Business Patterns Methodology, official methodology page, https://www.census.gov/programs-surveys/cbp/technical-documentation/methodology.html.

[6] U.S. Bureau of Labor Statistics — Quarterly Census of Employment and Wages, official overview page, https://www.bls.gov/cew/.

[7] U.S. Census Bureau — Core Based Statistical Areas Delineation File, July 2023, official reference file, https://www2.census.gov/programs-surveys/metro-micro/geographies/reference-files/2023/delineation-files/list1_2023.xlsx.
