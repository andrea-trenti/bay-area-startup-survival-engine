# Startup Data Dictionary and Measurement Boundaries

## Abstract

This note defines the statistical objects used throughout the repository and separates three distinct economic processes that are often conflated in startup commentary: **business application flow**, **projected employer conversion**, and **realized employer dynamics**. The distinction is essential. The Business Formation Statistics (BFS) program measures business applications from EIN filings and links them to projected and realized employer formations at selected aggregation levels [1][2]. The Business Dynamics Statistics (BDS) program measures realized annual business dynamics among employer firms and establishments, including startups, shutdowns, and job creation or destruction [3][4]. The Quarterly Census of Employment and Wages (QCEW) program measures covered employment, establishments, and wage structure, not startup quality or survival directly [5][6].

The repository therefore treats each source as a component of a measurement system rather than as a stand-alone truth source. BFS is the high-frequency front end; BDS is the realized annual employer-dynamics back end; QCEW is the operating-environment and labor-cost layer. The core source architecture already supports a strong formation-intelligence system, but it should not be mistaken for a complete realized-survival model. This note formalizes those boundaries so that later inferences remain defensible.

## 1. Conceptual separation

### 1.1 Business applications are not startups in the strict employer sense

BFS measures applications for an Employer Identification Number (EIN) submitted on IRS Form SS-4 and uses these applications to construct several business application series [1][2]. An application is evidence of business initiation intent, but it is not equivalent to a new employer firm. Some applications never convert into employer businesses; others remain nonemployer entities for long periods.

### 1.2 Projected employer formations are model-based transition measures

BFS provides projected employer formations because the Census Bureau can observe which applications later generate first payroll tax liability and can model the expected probability and duration of that transition [1][7]. This makes BFS unusually valuable for near-term startup pipeline monitoring, but it still differs from ex post realized startup counts.

### 1.3 Realized employer dynamics are annual and slower

BDS measures actual employer-side dynamics annually, including firm startups, shutdowns, establishment openings and closings, and job reallocation [3][4]. It is the correct source for long-run survival-style analysis of employer businesses, but it is inherently lower frequency than BFS.

### 1.4 Labor-market conditions are conditioning variables, not outcome labels

QCEW measures covered establishments, employment, wages, and related labor-market variables for more than 95 percent of U.S. payroll jobs [5]. These data are critical for contextualizing startup formation and scaling conditions, but they do not identify startup success by themselves.

## 2. Core series dictionary

### 2.1 BFS application series

The `bfs_monthly.csv` source file contains the following business-application series [1][2]:

| Series code | Meaning | Interpretation | Main use in this repository |
|---|---|---|---|
| `BA_BA` | Business applications | Total EIN applications associated with potential business starts | Headline initiation flow |
| `BA_CBA` | High-propensity business applications from corporations | More selective initiation measure | Composition / quality signal |
| `BA_HBA` | High-propensity business applications | Subset judged more likely to become employer businesses | Near-term employer pipeline proxy |
| `BA_WBA` | Business applications with planned wages | Applications indicating planned payroll | Early labor-intent proxy |

These application series should never be described as “startup births” without qualification.

### 2.2 BFS formation series

The same file includes formation-oriented series [1][2]:

| Series code | Meaning | Interpretation | Repository use |
|---|---|---|---|
| `BF_BF4Q` | Actual employer business formations within 4 quarters | Realized conversion of prior applications | State/national formation anchor |
| `BF_BF8Q` | Actual employer business formations within 8 quarters | Broader realized conversion window | Lagged formation anchor |
| `BF_PBF4Q` | Projected business formations within 4 quarters | Model-based expected conversion | Nowcasting core |
| `BF_PBF8Q` | Projected business formations within 8 quarters | Longer-horizon expected conversion | Medium-term nowcast |
| `BF_SBF4Q` | Spliced business formations within 4 quarters | Historical continuity series | Back-casting / comparability |
| `BF_SBF8Q` | Spliced business formations within 8 quarters | Historical continuity series | Back-casting / comparability |
| `BF_DUR4Q` | Average duration to first payroll within 4 quarters | Speed of conversion | Friction / delay metric |
| `BF_DUR8Q` | Average duration to first payroll within 8 quarters | Speed over longer horizon | Persistence / delay metric |

The methodological point is straightforward: these formation variables are not direct counts of successful companies; they are conversion-related measures from application to employer status.

### 2.3 BDS variable family

BDS, when added, will provide annual realized employer-side variables such as firm startups, shutdowns, establishment births and deaths, job creation, and job destruction [3][4]. In this repository, BDS is the preferred source for ex post structural dynamics because it measures the churn of paid-employment businesses rather than application intent.

### 2.4 QCEW variable family

QCEW annual area files include at least the following high-level variables [5][6]:

- `annual_avg_estabs_count`
- `annual_avg_emplvl`
- `total_annual_wages`
- `annual_avg_wkly_wage`
- `avg_annual_pay`

These should be interpreted as labor-market context variables that influence startup cost conditions, hiring feasibility, and sectoral operating intensity.

## 3. Measurement boundaries

### 3.1 What the core source architecture can establish cleanly

With the assembled within the acquisition layer BFS county annual workbook, monthly BFS file, area titles file, and CBSA delineation crosswalk, the repository can already do the following rigorously:

1. measure long-run county-level business application trends in the nine-county Bay Area [1][8];
2. measure regional concentration and diffusion across Bay Area counties [1][8];
3. map California and U.S. monthly application cycles [1];
4. build initial nowcasting relationships between Bay Area annual application intensity and California monthly employer-conversion signals [1][2].

### 3.2 What the core source architecture does not establish on its own

Without the full Bay Area QCEW county universe and selected BDS metro/county extracts, the repository does not measure:

- actual employer survival rates for Bay Area startups;
- county-level realized payroll conversion from application to employer formation;
- full operating-cost panels for every Bay Area county and sector.

These are not shortcomings of the repository design; they are data-boundary issues that need to be disclosed explicitly.

## 4. Adjustment and comparability rules

### 4.1 Monthly BFS: adjusted vs unadjusted

The `sa` flag in BFS distinguishes seasonally adjusted from unadjusted series [1]. Repository rule:

- use **adjusted (`A`)** series for cyclical comparisons and trend nowcasts;
- use **unadjusted (`U`)** series only when exact release replication or seasonal pattern analysis is required.

### 4.2 Annual county BFS workbook

The county annual workbook is a separate annual product and should not be numerically forced to equal the sum of seasonally adjusted monthly series. Differences may arise from revisions, adjustment procedures, and the distinct publication mechanics of the annual county product [1][7].

### 4.3 QCEW annual wage context

When using QCEW:

- restrict baseline context rows to `own_code = 0`, total covered employment;
- prefer total-industry rows (`industry_code = 10`) for county-wide operating context;
- treat detailed industry rows as sector context, not headline regional totals.

## 5. Derived variables used by this repository

The repository constructs several derived statistics from the raw public files.

### 5.1 County application share

For county \(i\) in year \(t\):

$$
s_{i,t} = \frac{BA_{i,t}}{\sum_{j \in \mathcal{B}} BA_{j,t}}
$$

where \(BA_{i,t}\) is annual business applications in county \(i\), and \(\mathcal{B}\) is the nine-county Bay Area set.

### 5.2 Annual momentum

$$
g_{i,t} = \frac{BA_{i,t} - BA_{i,t-1}}{BA_{i,t-1}}
$$

This is used as a simple formation-intent acceleration measure, not as a realized success metric.

### 5.3 Concentration index

$$
HHI_t = \sum_{i \in \mathcal{B}} s_{i,t}^2
$$

A higher \(HHI_t\) means startup initiation is concentrated in fewer counties.

### 5.4 Proxy employer-conversion rate

When state monthly BFS formation series are used to scale county annual applications, the repository defines a state-level bridge:

$$
\theta_t = \frac{PBF4Q_{CA,t}}{BA_{CA,t}}
$$

where \(PBF4Q_{CA,t}\) is California projected formations within four quarters and \(BA_{CA,t}\) is California business applications. This is a state-level transition proxy, not a county-level realized conversion estimate.

## 6. Data-quality and legal handling rules

1. Raw source files are referenced and processed within the acquisition layer but are not redistributed in the public repository.
2. Every Markdown analysis must identify the exact source family behind each load-bearing number.
3. Derived CSVs may be published if they are materially transformed and do not violate source terms, but the default repository posture is to publish code and documentation first.
4. Source institutions retain ownership of the underlying public datasets [1][3][5].

## 7. Conclusion

The central methodological discipline of this repository is semantic precision. Business applications, projected employer formations, realized employer dynamics, and labor-market operating context are different statistical objects generated by different public systems. A serious startup-finance or startup-operations analysis must preserve those distinctions. The core public-data stack is sufficient for formation intelligence and near-term nowcasting; fuller survival inference requires downstream BDS integration and broader Bay Area labor-context coverage.

## References

[1] U.S. Census Bureau — *Business Formation Statistics: Methodology* and BFS data documentation, 2026.

[2] U.S. Census Bureau — *Business Formation Statistics Current Release / About the Data*, 2026.

[3] U.S. Census Bureau — *Business Dynamics Statistics (BDS)* program overview, 2025.

[4] U.S. Census Bureau — *BDS Methodology*, 2025.

[5] U.S. Bureau of Labor Statistics — *Guide to QCEW Data Sources*, 2026.

[6] U.S. Bureau of Labor Statistics — *QCEW Field Layouts for NAICS-Based Annual CSV Files*, methodology documentation.

[7] U.S. Census Bureau — *Business Formation Statistics, February 2026*, release PDF.

[8] U.S. Census Bureau — *County Level Business Applications*, annual county workbook, 2005–2024, dataset.
