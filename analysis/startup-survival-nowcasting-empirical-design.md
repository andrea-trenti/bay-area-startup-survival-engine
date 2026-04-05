# Startup Survival Nowcasting Empirical Design

## Abstract

This note sets out the empirical strategy for a Bay Area startup-intelligence engine built on public U.S. data. The problem is not to predict “startup success” as a vague binary outcome, but to model a sequence of linked transitions: initiation, projected employer conversion, realized employer dynamics, and operating-scale conditions. The repository therefore treats startup measurement as a layered state-space problem in which county-level business applications are the initiation signal observed in the repository evidence base, California-level formation series provide high-frequency conversion information, and later BDS/QCEW integration supplies realized employer and labor-market structure [1][2][3][4].

The design is intentionally conservative. It does not infer firm-level success from web-text or venture press coverage. Instead, it begins with transparent public statistics and uses them to build a county-level nowcasting architecture. This approach is slower than a high-variance classification approach trained on loosely comparable labels, but it is substantially more defensible and better aligned with academic and policy standards.

## 1. Introduction

Bay Area startup analysis is usually distorted by one of two mistakes. The first is conceptual inflation: treating any visible startup, funding event, or application filing as proof of durable economic formation. The second is geographic inflation: treating “the Bay Area” as an interchangeable label for counties, metros, and broad commuting systems. This project rejects both shortcuts.

The objective is to build a research-grade pipeline that can answer the following question:

> Given the observed pattern of business applications across the nine-county Bay Area, what can be inferred about near-term employer conversion and medium-term operating conditions, and what cannot?

This is a narrower and more serious question than generic “winner prediction.” It is also the appropriate foundation for later extensions into startup finance, labor absorption, and capital-efficiency analysis.

## 2. Data and stylised facts

The core public source architecture supports a meaningful first-stage system.

First, the annual county BFS workbook reports county-level business applications from **2005 to 2024** [1]. In the annual county workbook, the nine-county Bay Area recorded **50,602** applications in 2005 and **97,505** in 2024, implying growth of **92.7%** over the period and an annualized growth rate of about **3.5%** [1]. The post-2019 rise is especially large: the regional total increased from **70,440** in 2019 to **97,505** in 2024, or **38.4%** [1].

Second, the geographic distribution is highly concentrated. In 2024, Santa Clara County accounted for **22,219** applications, Alameda County for **19,498**, and San Francisco County for **18,699**; together these three counties represented **62.0%** of all nine-county applications [1]. The 2024 county-share Herfindahl-Hirschman Index is approximately **0.163**, or **1,630** on the conventional 10,000-point scale, which corresponds to an “effective number” of about **6.1** equal-sized counties rather than nine [1].

Third, the annual series shows a post-pandemic surge followed by post-surge normalization rather than collapse. The regional total rose from **80,289** in 2020 to **93,695** in 2021, eased to **85,995** in 2022, jumped to a cycle high of **101,112** in 2023, and then slipped to **97,505** in 2024, a decline of **3.6%** year on year [1]. The decline was not uniform: San Francisco County still grew **5.7%** in 2024, Marin grew **8.8%**, and San Mateo grew **3.7%**, while Solano fell **18.1%**, Alameda **11.0%**, and Contra Costa **9.9%** [1].

Fourth, California remains a very large national application market. In the monthly BFS file, California’s seasonally adjusted total business applications (`BA_BA`) were **48,748** in December 2025, **57,033** in January 2026, and **50,221** in February 2026 [2]. These correspond to roughly **9.8%**, **10.8%**, and **10.1%** of the U.S. totals in those months [2]. California’s seasonally adjusted 2025 annual total in the monthly file sums to **549,317**, up **5.6%** from the corresponding 2024 adjusted total of **520,151** [2].

These stylised facts justify a design in which Bay Area county applications provide the allocation structure while California monthly series provide the timing signal.

## 3. Framework

### 3.1 State representation

Let:

- \(BA_{i,t}\) = business applications in county \(i\) and year \(t\);
- \(BA^{CA}_{m}\) = California monthly business applications in month \(m\);
- \(PBF4Q^{CA}_{m}\) = California projected employer business formations within four quarters in month \(m\);
- \(QCEW_{i,t}\) = county labor-market context vector (establishments, employment, wages) for county \(i\), year \(t\);
- \(S_{i,t+h}\) = latent startup operating-scale or survival condition for county \(i\) at horizon \(h\).

The repository does **not** observe \(S_{i,t+h}\) directly at present. Instead, it estimates intermediate signals that are economically meaningful.

### 3.2 County application share

The first object is the county allocation share:

$$
s_{i,t} = \frac{BA_{i,t}}{\sum_{j \in \mathcal{B}} BA_{j,t}}
$$

where \(\mathcal{B}\) is the nine-county Bay Area set.

### 3.3 State-level employer-conversion bridge

Because county-level projected formation data are not available in the monthly BFS file, the nowcast uses a California conversion bridge:

$$
\theta_m = \frac{PBF4Q^{CA}_{m}}{BA^{CA}_{m}}
$$

where \(\theta_m\) measures the state-level expected conversion intensity from applications to projected employer formations in month \(m\).

### 3.4 County nowcast

A conservative county-level projected employer-formation proxy is then:

$$
\widehat{EF}_{i,t+h} = s_{i,t} \cdot \Theta_{t+h} \cdot BA^{CA}_{t+h}
$$

where \(\Theta_{t+h}\) is a smoothed California conversion ratio and \(BA^{CA}_{t+h}\) is the projected California application level over the relevant horizon. This is a **regional allocation nowcast**, not a county-level structural estimate of true employer conversion.

### 3.5 Operating-condition augmentation

When the relevant QCEW Bay Area county files are integrated into the acquisition layer, the county nowcast can be conditioned on labor-market variables:

$$
\widehat{S}_{i,t+h} = f\!\left(\widehat{EF}_{i,t+h}, \Delta wage_{i,t}, \Delta estabs_{i,t}, \Delta empl_{i,t}, c_i\right)
$$

where \(c_i\) captures time-invariant county characteristics. This extension recognizes that the startup pipeline is shaped not only by initiation volume but also by labor-cost and establishment-density conditions.

## 4. Scenarios and analysis

### 4.1 Conservative scenario: mean reversion after the 2023 peak

Suppose Bay Area county applications remain below the 2023 high and Bay Area share of California applications reverts toward the **2023 share of 18.11%**. Applying that share to the California adjusted 2025 total of **549,317** yields an implied Bay Area total of about **99,468** applications [1][2]. This is modestly above the observed 2024 total and consistent with a stabilization scenario rather than a renewed surge.

### 4.2 Central scenario: 2024 regional share persists

If the Bay Area keeps its **2024 share of California applications at 18.89%**, the same California 2025 adjusted total implies about **103,776** Bay Area applications [1][2]. Relative to 2024, that would be growth of approximately **6.4%**. Economically, this would indicate that the Bay Area is not merely following California’s cycle but also maintaining regional concentration within the state’s startup pipeline.

### 4.3 High-concentration scenario: gains accrue to core counties

A stronger regional total does not imply even diffusion. If total applications rise while the county-share HHI remains near the 2024 level of **0.163** or increases, the Bay Area would be experiencing expansion through already-dominant counties rather than broad-based spatial diffusion [1]. In practice, that would likely mean incremental gains accruing disproportionately to Santa Clara, Alameda, San Francisco, and San Mateo.

### 4.4 Why results differ

The scenarios differ because three mechanisms move separately:

1. **State cycle effect**: California application growth can rise or fall independently of Bay Area share.
2. **Regional share effect**: the Bay Area’s share of California applications can expand even if the state total is flat.
3. **Within-region concentration effect**: gains may accrue to dominant counties, increasing concentration without broadening the regional base.

This decomposition is more informative than a single aggregate forecast because it identifies where the signal is coming from.

## 5. Risks and caveats

### 5.1 Measurement risk

Business applications are intent signals, not realized startup success [1][2]. Any interpretation that treats a rise in \(BA\) as equivalent to a rise in durable employer formation is too strong.

### 5.2 Aggregation risk

The conversion bridge uses California-level monthly projected formations because county-level projected formations are not available in the main monthly BFS file [2][7]. This is analytically useful but not a substitute for county-specific employer-conversion data.

### 5.3 Operating-conditions risk

The QCEW files assembled in the acquisition layer do not cover the Bay Area county universe in full. Operating-economics conclusions should therefore be framed as contingent on the availability of the relevant county files [5][6].

### 5.4 Structural-break risk

The post-2020 application surge may reflect a persistent shift in entrepreneurial behavior, tax/reporting practices, platform-based self-employment, or a mixture of all three. Historical parameters estimated on pre-2020 data alone may therefore understate present baseline formation propensity [1][2].

## 6. Comparison and implications

### 6.1 For founders and operators

The useful signal is not simply whether applications are high. It is whether application intensity is broadening across counties and whether later labor-market indicators support scaling. A region dominated by a few counties may be dynamic, but it may also be congested and more expensive to scale in.

### 6.2 For investors

A county-allocation nowcast helps separate two ideas that are often blurred: statewide startup momentum and subregional concentration. These are not the same. A venture market can remain active while the spatial breadth of entrepreneurial formation narrows.

### 6.3 For policymakers

The proper policy question is not whether the Bay Area still has many startups. The better question is whether initiation increasingly clusters in already-dominant counties while adjacent counties fail to convert entrepreneurial intent into employer scale. That is where public infrastructure, permitting speed, commercial affordability, and labor-market frictions become relevant.

## 7. Conclusion

A credible public-data startup engine begins with disciplined measurement rather than theatrical prediction. The Bay Area files already support a strong first-stage architecture: county annual applications for spatial allocation, California monthly BFS for timing and conversion context, and a clear roadmap for later BDS/QCEW integration. This design will not answer every startup question immediately, but it answers the right ones first and creates a defensible foundation for advanced survival, finance, and operations analysis.

## References

[1] U.S. Census Bureau — *County Level Business Applications*, annual county BFS workbook, 2005–2024, dataset.

[2] U.S. Census Bureau — *Business Formation Statistics monthly data* and present release documentation, 2026.

[3] U.S. Census Bureau — *Business Dynamics Statistics (BDS)* program overview, 2025.

[4] U.S. Census Bureau — *BDS Methodology*, 2025.

[5] U.S. Bureau of Labor Statistics — *Guide to QCEW Data Sources*, 2026.

[6] U.S. Bureau of Labor Statistics — *QCEW Downloadable Data Files* and *NAICS-Based Annual CSV Layout*, documentation.

[7] U.S. Census Bureau — *Business Formation Statistics: Methodology*, 2026.
