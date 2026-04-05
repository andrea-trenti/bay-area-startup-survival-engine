# Bay Area 2025-2026 Scenario Matrix
## Short-horizon application paths under conservative, central, and upside assumptions

## Abstract
This note translates the historical Bay Area business-application series into a transparent scenario matrix for 2025 and 2026. The objective is not to generate false precision. It is to provide a disciplined range for startup-initiation inflows using publicly auditable assumptions and the official annual county business-applications release integrated into the acquisition layer.[1][2] The correct target variable is annual business applications in the repository's nine-county Bay Area definition.

The historical anchor points are strong enough to support bounded scenario work. Bay Area applications equaled 50,602 in 2005, 70,440 in 2019, 80,289 in 2020, 93,695 in 2021, 85,995 in 2022, 101,112 in 2023, and 97,505 in 2024.[3] These values imply a pre-pandemic structural growth rate of roughly 2.4 percent per year over 2005-2019, a recent 2022-2024 growth rate of about 6.5 percent per year, a post-2020 CAGR near 5.0 percent, and a latest observed year-over-year contraction of 3.6 percent in 2024.[3]

Under those anchors, a conservative path yields roughly 94,027 applications in 2025 and 90,672 in 2026; a central path yields approximately 101,831 in 2025 and 106,348 in 2026; and an upside path yields about 102,357 in 2025 and 107,451 in 2026.[4] These are not forecasts in the asset-pricing sense. They are reproducible scenario points intended to discipline downstream employer-conversion and labor-absorption analysis.

## 1. Introduction
A high-frequency startup repository needs a short-horizon expectations framework. Without one, every update becomes a backward-looking description. The challenge is that public startup proxies are broad and noisy: BFS county annual counts are informative, but they are not equivalent to a venture-funding dataset. The solution is to use a scenario matrix rather than a single deterministic projection.

This note therefore asks a narrow question: given the observed path of Bay Area business applications through 2024, what annual range is consistent with transparent continuation assumptions into 2025 and 2026? The answer matters because applications are the inflow that later conditions projected employer formation, hiring demand, and county-level ecosystem pressure.

## 2. Data and stylised facts
The scenario engine uses the annual county business-applications file, aggregated to the nine-county Bay Area.[3] The observed path is summarized below.

| Year | Bay Area business applications |
|---|---:|
| 2005 | 50,602 |
| 2010 | 53,186 |
| 2015 | 62,683 |
| 2019 | 70,440 |
| 2020 | 80,289 |
| 2021 | 93,695 |
| 2022 | 85,995 |
| 2023 | 101,112 |
| 2024 | 97,505 |

Three facts follow immediately.[3]

1. The long-run level is materially higher than in the mid-2000s.
2. The post-2020 period introduced both an upward level shift and higher volatility.
3. The most recent observation is a decline from 2023, but not a return to the pre-pandemic baseline.

## 3. Framework
Define the annual Bay Area application total as $BA_t$. The scenario engine uses four observed growth anchors:

- structural growth,

$$
g^{struct} = \left(\frac{BA_{2019}}{BA_{2005}}\right)^{1/14} - 1
$$

- recent growth,

$$
g^{recent} = \left(\frac{BA_{2024}}{BA_{2022}}\right)^{1/2} - 1
$$

- post-2020 growth,

$$
g^{post} = \left(\frac{BA_{2024}}{BA_{2020}}\right)^{1/4} - 1
$$

- latest shock,

$$
g^{shock} = \frac{BA_{2024}}{BA_{2023}} - 1
$$

The scenario rules are:

$$
g^{central} = 0.5g^{struct} + 0.5g^{recent}
$$

$$
g^{cons} = \min(g^{struct}, g^{shock})
$$

$$
g^{up} = \max(g^{central}, g^{post})
$$

Projected levels follow:

$$
\widehat{BA}_{t+1} = BA_t(1+g)
$$

and for the two-year horizon,

$$
\widehat{BA}_{t+2} = BA_t(1+g)^2
$$

Every symbol is directly observable or transparently computed from the historical series.

## 4. Scenarios and analysis
### 4.1 Growth anchors
Using the observed Bay Area counts, the repository computes the following approximate rates:[4]

- $g^{struct} \approx 2.39\%$
- $g^{recent} \approx 6.48\%$
- $g^{post} \approx 4.98\%$
- $g^{shock} \approx -3.57\%$

These values show why a single forecast would be misleading. The long-run structural trend is positive but moderate, the recent multi-year rebound is substantially stronger, and the latest year introduces a negative shock.

### 4.2 Scenario table
The resulting matrix is:

| Scenario | Growth assumption | 2025 applications | 2026 applications |
|---|---:|---:|---:|
| Conservative | -3.57% | 94,027 | 90,672 |
| Central | 4.44% | 101,831 | 106,348 |
| Upside | 4.98% | 102,357 | 107,451 |

These values are rounded from the script outputs.[4]

### 4.3 County allocation logic
The scenario engine can allocate projected totals back to counties by holding the latest observed county shares fixed. Under the 2024 share distribution, Santa Clara would receive about 22.8 percent of projected aggregate applications, Alameda 20.0 percent, and San Francisco 19.2 percent.[3][4] This is a reasonable short-horizon convention when there is insufficient evidence for a structural county-share break.

### 4.4 Interpretation
The conservative path is not a recession forecast in macroeconomic terms; it is a disciplined carry-forward of the latest observed negative annual shock. The central path assumes that some combination of long-run trend and recent rebound remains intact. The upside path assumes that the post-2020 elevated entrepreneurial regime persists. Together, the range is more informative than a single pseudo-precise number.

## 5. Risks and caveats
The scenario matrix is intentionally simple. It does not include interest-rate variables, sector composition, financing conditions, or migration flows. It also relies on county annual counts that incorporate disclosure-avoidance procedures.[2] For those reasons, the outputs should be treated as scenario points rather than formal forecasts with estimated confidence intervals.

The conservative scenario is sensitive to a single annual decline in 2024. The upside scenario is sensitive to the assumption that the post-2020 regime persists. The central scenario is the most stable of the three because it blends structural and recent information, but it is still only a transparent heuristic.

## 6. Comparison and implications
For founders and operators, the main implication is that the Bay Area likely remains a very high-entry entrepreneurial system even under a conservative normalization path. For investors, the range highlights an important distinction between application inflow and funded-company opportunity: a strong application environment is necessary but not sufficient for high-quality venture outcomes. For policymakers, the scenario logic provides a way to discuss entrepreneurial capacity without relying exclusively on venture-round databases.

The broader methodological implication is that public-data startup repositories should prefer scenario bands over single-number prophecy. This preserves credibility and improves comparability across updates.

## 7. Conclusion
The historical Bay Area series supports a defensible 2025-2026 scenario range rather than a single deterministic forecast. Under the repository's present evidence base, the most plausible band runs from roughly 90,700 to 107,500 applications by 2026, depending on whether the 2024 correction deepens, stabilizes, or gives way to continued elevated formation intensity.[3][4] This range should be used as an upstream input to the employer-conversion and labor-context layers in the repository.

## References
[1] U.S. Census Bureau — Business Formation Statistics: Methodology, official methodology page, https://www.census.gov/econ/bfs/methodology.html.

[2] U.S. Census Bureau — Business Formation Statistics Technical Documentation: Methodology, county disclosure-avoidance notes, https://www.census.gov/econ/bfs/technicaldocumentation/methodology.html.

[3] U.S. Census Bureau annual county business-applications file (`bfs_county_apps_annual.xlsx`), downloaded separately from the official Census release page and excluded from GitHub version control.

[4] Author's calculations generated by `estimate_bay_area_nowcast_scenarios.py` from the annual county source file and the repository's nine-county Bay Area definition.
