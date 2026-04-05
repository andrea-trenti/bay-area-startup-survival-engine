# Bay Area Startup Hazard Proxy System
## A relative fragility framework based on annual county business-application dynamics

## Abstract
This note develops a transparent hazard-proxy system for the Bay Area startup funnel using annual county business-applications data from the U.S. Census Bureau.[1] The objective is narrow and explicit: rank counties by relative fragility in their application streams using observable momentum, growth persistence, volatility, and drawdown statistics. The system does **not** estimate startup failure probabilities. It constructs a diagnostic ordering that helps identify where the entrepreneurial pipeline appears more exposed to instability.[1]

The Bay Area aggregate rose from 50,602 applications in 2005 to 97,505 in 2024, implying a long-run compound annual growth rate of roughly 3.5 percent.[1] But the cross-county structure is heterogeneous. In 2024, Santa Clara accounted for 22.79 percent of Bay Area applications, Alameda 20.00 percent, and San Francisco 19.18 percent; the top three counties therefore represented 61.96 percent of the regional total.[1] At the same time, 2024 year-over-year growth ranged from -18.11 percent in Solano to +8.80 percent in Marin.[1]

Using a composite proxy score built from recent momentum, 2019-2024 CAGR, volatility of annual growth, and drawdown depth, the most fragile counties in the 2024 cross-section are Napa, Solano, Alameda, and Contra Costa.[1] The strongest relative readings are Sonoma, San Francisco, Santa Clara, and Marin.[1] Those results are best interpreted as early-warning signals about the **application pipeline**, not as direct claims about startup mortality, capital scarcity, or venture outcomes.

## 1. Introduction
Bay Area startup analysis often collapses diverse geographies into a single ecosystem narrative. That is analytically costly. A region can be growing at the aggregate level while specific counties face deteriorating county entrepreneurial inflows. Conversely, a county with a small absolute base can display dramatic percentage swings with negligible influence on the regional aggregate.

A hazard-proxy system helps solve that problem by imposing a disciplined cross-sectional language. It identifies where the application stream is fragile, where it is resilient, and where apparent weakness is actually just scale noise. Because the public annual business-applications file does not directly observe venture-backed formation, exits, or firm survival, the correct ambition is comparative diagnosis rather than false prediction.[1]

## 2. Data and stylised facts
The underlying sample is the annual county business-applications dataset, restricted to the nine-county Bay Area universe used throughout this repository.[1] The Bay Area aggregate was 50,602 in 2005, 70,440 in 2019, 80,289 in 2020, 93,695 in 2021, 85,995 in 2022, 101,112 in 2023, and 97,505 in 2024.[1] The 2024 reading therefore remained 38.4 percent above the 2019 level and 92.7 percent above the 2005 level.[1]

County structure remains highly concentrated. In 2024 Santa Clara recorded 22,219 applications, Alameda 19,498, San Francisco 18,699, Contra Costa 13,311, and San Mateo 9,497.[1] Sonoma and Solano contributed 4,930 and 4,440 respectively; Marin recorded 3,586 and Napa 1,325.[1] The top three counties represented 61.96 percent of all Bay Area applications in 2024, while the Herfindahl-style county concentration measure was approximately 1,630 on a 0-10,000 scale.[1]

Recent momentum was uneven. Between 2023 and 2024, Alameda fell by 2,401 applications, Contra Costa by 1,461, Solano by 982, and Santa Clara by 335.[1] Offsetting gains came from San Francisco (+1,011), San Mateo (+342), Marin (+290), and Sonoma (+88).[1] Because the regional aggregate declined by 3,607 applications in 2024, Alameda alone explained 66.6 percent of the net decline and Contra Costa another 40.5 percent, while San Francisco offset 28.0 percent of the contraction.[1]

## 3. Framework
Let $A_{i,t}$ denote county $i$'s annual business applications in year $t$. The hazard-proxy system combines four ingredients.

First, recent momentum:

$$g_{i,2024}^{YoY} = \left(\frac{A_{i,2024}}{A_{i,2023}} - 1\right) \times 100$$

Second, medium-run growth persistence from 2019 to 2024:

$$g_{i}^{CAGR,2019-2024} = \left(\frac{A_{i,2024}}{A_{i,2019}}\right)^{1/5} - 1$$

Third, historical instability measured as the standard deviation of annual YoY growth over the available sample.

Fourth, drawdown depth:

$$DD_i = \min_t \left(\frac{A_{i,t}}{\max_{\tau \le t} A_{i,\tau}} - 1\right) \times 100$$

To create a cross-county composite, variables that imply greater fragility when larger in absolute value are aligned in a risk direction, standardized, and averaged. The resulting index is then rescaled to a 0-100 range. Formally,

$$H_i = 100 \times \frac{\bar{z}_i - \min(\bar{z})}{\max(\bar{z}) - \min(\bar{z})}$$

where $\bar{z}_i$ is the average of the standardized risk-oriented components for county $i$.

## 4. Scenarios and analysis
### Scenario A — recent momentum dominates
If the analyst emphasizes the latest annual change, then Solano (-18.11 percent), Alameda (-10.96 percent), Napa (-10.71 percent), and Contra Costa (-9.89 percent) emerge as the most exposed counties in 2024.[1] Counties with positive 2024 growth, notably Marin (+8.80 percent), San Francisco (+5.72 percent), and San Mateo (+3.74 percent), screen as more resilient on a short-horizon basis.[1]

### Scenario B — medium-run persistence dominates
Using 2019-2024 CAGR, every Bay Area county still shows positive medium-run growth, with Sonoma at 7.77 percent, Contra Costa at 7.47 percent, San Francisco at 7.12 percent, and Santa Clara at 6.71 percent.[1] Napa remains positive at 6.07 percent despite its weak 2024 reading.[1] This matters: a county can register short-run fragility without looking structurally impaired over a five-year window.

### Scenario C — volatility and drawdown dominate
On the instability dimension, Solano and Napa stand out. Solano's YoY growth volatility is 14.72 percentage points and its maximum drawdown reaches 22.45 percent; Napa's volatility is 11.02 percentage points and its maximum drawdown 23.45 percent.[1] By contrast, Marin's volatility is 6.48 percentage points and Santa Clara's maximum drawdown is only 8.32 percent.[1]

### Composite result
Combining the four dimensions yields the following relative ordering in 2024: Napa (100.0), Solano (90.2), Alameda (58.9), Contra Costa (47.1), San Mateo (14.4), Marin (10.1), Santa Clara (10.0), San Francisco (5.2), and Sonoma (0.0).[1] The interpretation is not that Napa is economically weaker than Santa Clara in any absolute sense. The interpretation is that Napa's annual application stream is more fragile relative to its own history and to its Bay Area peers.

## 5. Risks and caveats
The first risk is conceptual. Business applications are not startup deaths, not financing events, and not firm exits.[1] Any language implying mortality estimation would overstate what the data can support.

The second risk is scale distortion. Small counties can exhibit high percentage volatility from modest absolute changes. Napa's and Solano's elevated proxy scores reflect genuine instability in the application stream, but those counties account for only 1.36 percent and 4.55 percent of 2024 Bay Area applications respectively.[1]

The third risk is omitted-variable bias. The score does not include wages, office costs, venture availability, patenting, founder quality, or sector composition. It is therefore a narrow pipeline fragility measure.

The fourth risk is governance drift. Composite scores become unreliable when thresholds and transformations change from release to release. The repository therefore fixes the component set and scaling logic unless a new methodology note explicitly revises the system.

## 6. Comparison and implications
For founders and operators, the main implication is county-level heterogeneity. A Bay Area narrative based solely on regional aggregates can hide important county-level regime differences. For investors, the system can function as a screening overlay for ecosystem monitoring, especially when combined later with funding, hiring, or wage data. For policymakers, the score is useful not because it predicts startup failure, but because it shows where entrepreneurial inflows appear least stable and where county support mechanisms may need closer inspection.

The most important comparison is between high-weight and low-weight counties. Alameda and Contra Costa combine relatively weak 2024 momentum with meaningful scale; they matter for the regional total.[1] Napa and Solano show deeper fragility signals, but their smaller scale limits their macro influence. Santa Clara and San Francisco remain systemically important because even modest changes there carry large regional consequences.[1]

## 7. Conclusion
A credible public-data startup repository should distinguish between descriptive scale, cyclical momentum, and fragility. The hazard-proxy system offers that distinction. It shows that the Bay Area application pipeline remained historically elevated in 2024, yet county-level readings became materially more uneven.[1] The strongest analytical use of this framework is not headline ranking. It is disciplined decomposition: which counties are large, which are unstable, which are accelerating, and which are pulling the regional aggregate up or down.

What would improve certainty most is the addition of downstream outcome data: employer conversion, establishment births, funding events, and labor demand. Within the repository's evidentiary boundary, the hazard-proxy system should be treated as a rigorous upstream diagnostic rather than as a complete solution to the startup-survival problem.

## References
[1] U.S. Census Bureau — County Business Applications, annual county dataset, public statistical release used for Bay Area county aggregation and derived indicator construction.
