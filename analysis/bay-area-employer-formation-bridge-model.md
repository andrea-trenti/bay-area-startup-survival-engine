# Bay Area Employer-Formation Bridge Model
## Translating county business applications into state-anchored employer-startup proxies

## Abstract

The assembled within the acquisition layer public-data stack contains rich Bay Area county counts of business applications, but not a directly observed county panel of employer business formations. This note addresses that gap by constructing a bridge model: annual county application counts are combined with California's monthly spliced business-formation ratio from the Census Business Formation Statistics (BFS) to generate a county-level proxy for implied employer startups. The exercise is useful because it moves the project from a pure initiation-count framework toward a more economically relevant measure of founder-to-employer conversion, while remaining honest about inferential limits [1][2].

Using the annual county applications workbook documented in the repository, the nine-county Bay Area recorded 97,505 business applications in 2024, down from 101,112 in 2023 but still 38.4% above 2019 and 92.7% above 2005 on the same annual-count basis. California's seasonally adjusted annual-average spliced four-quarter conversion ratio, computed as monthly `SBF4Q / BA`, was about 8.33% in 2023 and 8.35% in 2024 in the assembled within the acquisition layer monthly BFS file. Applying that state bridge to Bay Area county application totals implies roughly 8,424 employer-forming startups in 2023 and 8,141 in 2024, with Santa Clara, Alameda, and San Francisco together accounting for about 62.0% of the region's implied employer-forming volume in 2024 [1][5].

These figures are not direct observations of county employer startups. They are state-anchored projections intended for comparative regional analysis, scenario building, and capital-allocation research. Their main analytical value lies in ranking, stress testing, and identifying concentration risk, not in replacing official startup counts.

## 1. Introduction

Raw application counts are informative but incomplete. A business application is a signal of entrepreneurial intent, not an employer firm. For an operations, finance, or industrial-policy lens, the question of greater interest is whether the formation pipeline converts application flow into payroll-bearing firms. The BFS are particularly valuable here because they explicitly distinguish business applications from actual or projected employer formations and document the mechanics linking the two [1][2].

The challenge is geographic resolution. In the core source architecture, county-level annual data are available for business applications, while employer-formation signals are available in the monthly BFS at the state level. This creates a classical partial-observability problem: the geography of initiation is finer than the geography of conversion. Rather than ignore the finer county variation, the repository can estimate a Bay Area county-level employer-formation proxy by importing the California transition environment into county application totals.

## 2. Data and stylised facts

The annual county applications workbook covers U.S. counties from 2005 through 2024. Aggregating the nine Bay Area counties in the annual county workbook yields 50,602 applications in 2005, 70,440 in 2019, 80,289 in 2020, 93,695 in 2021, 85,995 in 2022, 101,112 in 2023, and 97,505 in 2024 [5]. The 2024 level is therefore 3.6% below 2023, 21.4% above 2020, 38.4% above 2019, and 92.7% above 2005 on the same data construction [5].

The county distribution is highly concentrated. In 2024, Santa Clara County accounted for 22,219 applications, Alameda 19,498, and San Francisco 18,699; Contra Costa followed with 13,311 and San Mateo with 9,497. The remaining four counties—Sonoma, Solano, Marin, and Napa—together represented less than 14.7% of the regional total [5]. The top three counties therefore captured roughly 61.96% of all Bay Area applications in 2024, implying a county-level Herfindahl-Hirschman Index of about 0.163 and an “effective county count” of roughly 6.14 out of the nine-county universe [5].

The California monthly BFS file shows that adjusted total business applications were 43,345.9 per month on average in 2024 and 45,776.4 in 2025, while the corresponding spliced four-quarter formations averaged 3,619.1 and 3,695.7 respectively. The resulting state-level annual-average conversion ratio was about 8.35% in 2024 and 8.07% in 2025, down materially from approximately 11.77% in 2019 and 12.57% in 2018 [1][5]. The key stylised fact is therefore a post-2020 environment with substantially higher application volumes but a lower application-to-employer conversion ratio.

## 3. Framework

Let $BA_{c,t}$ denote observed annual business applications in county $c$ and year $t$. Let $\theta_{CA,t}$ denote the California annual-average spliced conversion ratio derived from monthly seasonally adjusted BFS totals:

$$
\theta_{CA,t} = \frac{\overline{SBF4Q}_{CA,t}}{\overline{BA}_{CA,t}}
$$

where $\overline{SBF4Q}_{CA,t}$ is the annual average of monthly California `BF_SBF4Q` values and $\overline{BA}_{CA,t}$ is the annual average of monthly California `BA_BA` values.

The baseline county employer-formation proxy is:

$$
\widehat{EF}_{c,t} = BA_{c,t} \times \theta_{CA,t}
$$

where:
- $\widehat{EF}_{c,t}$ is implied employer-forming startups,
- $BA_{c,t}$ is observed county applications,
- $\theta_{CA,t}$ imports the state conversion environment.

Regional implied employer formations are obtained by summation:

$$
\widehat{EF}_{BA,t} = \sum_{c \in BA} \widehat{EF}_{c,t}
$$

This setup assumes that county differences in employer conversion are second-order relative to the state-level financing, labor-market, and regulatory environment. That assumption is not literally true, but it is operationally useful as a first-pass regional bridge.

## 4. Scenarios and analysis

### Scenario A: 2024 baseline conversion environment

Applying California's 2024 conversion ratio of roughly 8.35% to Bay Area county applications implies about 8,141 employer-forming startups in the region [5]. The county ranking remains dominated by Santa Clara (about 1,855), Alameda (about 1,628), and San Francisco (about 1,561), followed by Contra Costa (about 1,111) and San Mateo (about 793) [5].

### Scenario B: 2023 conversion environment applied to 2024 applications

If 2024 county applications were evaluated under the slightly weaker-but-still-similar 2023 California conversion ratio of about 8.33%, the regional implied total would be only marginally lower, just above 8.1 thousand [5]. This indicates that the headline difference between 2023 and 2024 implied employer formation is driven more by changes in application counts than by annual-average conversion shifts.

### Scenario C: Reversion to 2019 conversion efficiency

If the 2024 Bay Area application volume were paired with California's 2019 conversion ratio of roughly 11.77%, implied employer-forming startups would rise to around 11,480. The arithmetic is important: the shortfall between this counterfactual and the 2024 baseline is roughly 3.3 thousand firms, which suggests that today's weaker conversion environment may be at least as important as raw application volume for understanding startup pipeline quality [1][5].

### Scenario D: Downside stress using a 2025-like conversion environment

Using the 2025 annual-average California conversion ratio of about 8.07% as a downside calibration would push the 2024 Bay Area implied total to roughly 7,873. This is not a recession scenario; it is only a modest deterioration in conversion efficiency. Even so, the result is a decline of about 268 implied employer-forming firms relative to the baseline [5].

The economic interpretation is straightforward. Startup ecosystems can look strong on gross application flow while still suffering from weaker transition to payroll-bearing firms. That distinction matters for labor-market impact, commercial real estate demand, service-provider revenues, and venture pipeline conversion.

## 5. Risks and caveats

The bridge is analytically useful but imperfect.

First, county-level conversion rates surely differ. Santa Clara and San Francisco likely convert applications into employer firms at a different rate than Napa or Solano because industrial composition, founder profile, capital access, and labor demand differ. The bridge suppresses this heterogeneity.

Second, the BFS measure employer formation based on payroll tax liabilities, whereas the BDS identify startups differently, using employment and annual timing conventions. The Census Bureau states explicitly that the two systems do not match exactly, even if they track closely [1].

Third, the county annual workbook captures applications, not company-level attributes. It cannot reveal whether county-level changes are driven by sector mix, gig-style legal filings, founder demographics, or policy frictions.

Fourth, the bridge should not be interpreted as a county forecast of formal firm births in a legal or statistical sense. It is a structured proxy for research use.

## 6. Comparison and implications

For founders and operators, the main implication is that application abundance should not be confused with operating formation quality. In a weaker conversion environment, more applications may be needed to generate the same eventual employer base.

For investors and accelerators, the bridge offers a screening signal. A county that combines high application intensity with stable implied conversion may warrant closer attention than a county with high noise but weak conversion-adjusted scale.

For policymakers, the distinction between initiation and employer conversion points to a more precise policy question. If applications remain high but conversion weakens, the likely bottlenecks lie downstream: permitting, access to first hires, financing frictions, compliance costs, or demand uncertainty. Policy aimed only at “entrepreneurship promotion” may miss the actual constraint.

## 7. Conclusion

The Bay Area application pipeline remains large, but the conversion environment appears structurally less favorable than before 2020. In the observed public data, 2024 Bay Area applications remained close to 100 thousand, yet California's application-to-employer conversion ratio was only around 8.35%, far below pre-2020 norms [1][5]. This combination supports a disciplined interpretation: the region still generates entrepreneurial intent at scale, but the translation of intent into payroll-bearing firms appears thinner than in the late-2010s environment.

The bridge model should be treated as a research instrument rather than a final statistic. Its value lies in making county-level startup analysis more economically meaningful while preserving methodological honesty. Additional county-level startup, payroll, firm-age, or venture-financing data would materially improve precision.

## References

[1] U.S. Census Bureau — *Business Formation Statistics Methodology*, technical documentation, 2021, <https://www.census.gov/programs-surveys/bfs/technical-documentation/methodology.html>.

[2] U.S. Census Bureau — *Business Formation Statistics, February 2026*, monthly release/PDF, 2026, <https://www.census.gov/econ/bfs/pdf/bfs_present.pdf>.

[3] U.S. Census Bureau — *Business Dynamics Statistics (BDS)*, program page, updated 2025, <https://www.census.gov/programs-surveys/bds.html>.

[4] U.S. Census Bureau — *Delineation Files (July 2023)*, geography reference page, 2023, <https://www.census.gov/geographies/reference-files/time-series/demo/metro-micro/delineation-files.html>.

[5] Author calculations from `bfs_county_apps_annual.xlsx` and `bfs_monthly.csv`, transformed through the repository workflow.
