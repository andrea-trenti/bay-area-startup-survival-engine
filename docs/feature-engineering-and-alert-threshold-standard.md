# Feature Engineering and Alert Threshold Standard
## Derived indicators for Bay Area startup-cycle monitoring from annual county business-application data

## Purpose
This document defines the derived indicators used to transform the annual county business-applications file into a disciplined Bay Area startup-cycle monitoring system. The underlying institutional source is the U.S. Census Bureau's annual county business-applications dataset.[1] In this repository, the annual applications series is treated as an upstream entrepreneurial-intent and firm-formation pressure indicator rather than as a direct measure of venture-backed startup creation. That boundary is critical. The series is broad, economically meaningful, and available at county level, but it is not equivalent to a company-level venture financing database.[1]

The goal of this standard is therefore not to claim false precision. It is to specify a reproducible indicator architecture that converts raw annual counts into interpretable features for descriptive analysis, scenario construction, and early-warning diagnostics. The resulting metrics are designed for public-data research workflows, regional ecosystem benchmarking, and longitudinal monitoring across Bay Area counties.

## Scope
The standard applies to the repository's nine-county Bay Area definition:
- Alameda County
- Contra Costa County
- Marin County
- Napa County
- San Francisco County
- San Mateo County
- Santa Clara County
- Solano County
- Sonoma County

County inclusion is governed through FIPS codes and can be cross-checked against the Census delineation file used elsewhere in the repository.[2]

## Core measurement philosophy
Three principles govern the indicator layer.

### 1. Preserve institutional meaning
Raw business applications are left untouched before aggregation other than type conversion, FIPS normalization, and missing-value handling. No smoothing is applied to the source series before the baseline panel is written.

### 2. Separate level, momentum, and stress
A county with a high level of applications is not necessarily accelerating. A county with strong recent growth may still exhibit high historical instability. For that reason, the repository separates:
- level indicators,
- momentum indicators,
- concentration indicators,
- stress or hazard-style indicators.

### 3. Treat risk metrics as proxies, not probabilities
No derived score in this repository should be interpreted as a statistical probability of failure, closure, or startup mortality. The annual applications series does not observe startup exits directly. All risk-oriented metrics are therefore diagnostic proxies intended to flag relative fragility in the county application stream.

## Derived indicators

### 1. Application level
For county $i$ in year $t$:

$$A_{i,t} = \text{annual business applications}$$

Regional Bay Area applications are defined as:

$$A_{BA,t} = \sum_i A_{i,t}$$

This is the primary scale variable. It measures the gross inflow of new business applications in the defined geography.[1]

### 2. Year-over-year absolute change

$$\Delta A_{i,t} = A_{i,t} - A_{i,t-1}$$

This indicator is useful for contribution accounting. It identifies which counties explain most of a regional increase or decline in a given year.

### 3. Year-over-year percent change

$$g_{i,t}^{YoY} = \left(\frac{A_{i,t}}{A_{i,t-1}} - 1\right) \times 100$$

This is the default momentum measure. It is simple, transparent, and suitable for cross-county comparison. It is unstable for very small series, which is why it must always be interpreted jointly with the level variable.

### 4. Multi-year CAGR
For a window from $t-k$ to $t$:

$$g_{i,t}^{CAGR,k} = \left(\frac{A_{i,t}}{A_{i,t-k}}\right)^{1/k} - 1$$

The repository uses a five-year window when possible for medium-run structural growth and a three-year or five-year comparison for shorter-horizon cycle interpretation. CAGR is less noisy than annual growth and more appropriate for regime comparisons.

### 5. Regional share

$$s_{i,t} = \frac{A_{i,t}}{A_{BA,t}} \times 100$$

This variable measures the weight of each county in the Bay Area startup funnel. High-share counties can dominate regional aggregates and can therefore distort naive readings of ecosystem-wide change.

### 6. Concentration metrics
The repository uses at least two concentration statistics:

- **Top-3 share**: the sum of the three largest county shares in year $t$.
- **HHI**: 

$$HHI_t = \sum_i (100 \times s_{i,t}/100)^2 = \sum_i s_{i,t}^2$$

when $s_{i,t}$ is expressed in percentage-point form divided by 100 before squaring.

These indicators are not antitrust measures in this context. They are structural descriptors of how concentrated the regional application base is across counties.

### 7. Drawdown from running peak
For any county or regional series:

$$DD_{i,t} = \left(\frac{A_{i,t}}{\max_{\tau \le t} A_{i,\tau}} - 1\right) \times 100$$

This is the preferred stress measure for annual business applications. It captures the distance from the historical high-water mark and therefore distinguishes transitory weakness from full recovery.

### 8. Volatility of annual growth
For county $i$:

$$\sigma_i^{YoY} = sd(g_{i,t}^{YoY})$$

computed over the available sample excluding the first undefined observation. This metric captures instability in the county's application stream and enters the hazard-proxy layer.

### 9. Hazard proxy score
The repository's hazard-proxy score is a composite ranking index, not a probability model. It combines:
- negative recent annual growth,
- negative medium-run growth,
- growth volatility,
- drawdown depth.

Each component is standardized cross-sectionally and then averaged. The resulting score is rescaled to a 0–100 range. Counties with higher values are interpreted as more exposed to application-stream fragility relative to the peer set.

The score is used for ranking, not for causal claims.

## Alert thresholds
The repository uses explicit thresholds for diagnostic alerts. These are conservative governance rules rather than econometric significance tests.

### County-level momentum alerts
- **Soft negative momentum**: YoY growth below -5 percent.
- **Hard negative momentum**: YoY growth below -10 percent.
- **Acceleration break**: change in YoY growth below -10 percentage points versus the prior year.

### County-level stress alerts
- **Moderate drawdown**: present level more than 5 percent below historical peak.
- **Severe drawdown**: present level more than 10 percent below historical peak.
- **High volatility**: long-run standard deviation of YoY growth above the regional median plus one-half standard deviation.

### Regional concentration alerts
- **Top-3 concentration pressure**: top-3 share above 60 percent.
- **Structural concentration pressure**: HHI above the long-run median by at least 10 percent.

These thresholds are intentionally simple. They are designed for reproducibility and comparability across releases, not for formal statistical testing.

## Interpretation rules
1. A county can rank as high-risk in the hazard-proxy system even if its long-run CAGR remains positive. This occurs when recent momentum weakens sharply or drawdowns become unusually deep.
2. A county with low share can display extreme percent volatility without materially moving the regional aggregate. Level and share must therefore be read together.
3. Regional weakness can be dominated by one or two large counties. Contribution analysis should always accompany any claim about Bay Area-wide deterioration.
4. Drawdown is more informative than annual growth when distinguishing transitory shocks from incomplete recoveries.

## Data limitations
- Business applications are not observed startup exits.
- The series is broad and includes many non-venture firms.[1]
- County series may capture tax, legal, and administrative shifts in filing behavior, not only entrepreneurial economics.
- Annual counts are too coarse for short-cycle event interpretation.
- Hazard-proxy rankings are relative within the nine-county system and should not be extrapolated mechanically to other ecosystems.

## Minimum reproducibility requirements
Any file in this repository that uses derived indicators from annual county applications must:
1. identify the source file used,
2. define the Bay Area county universe explicitly,
3. report the exact transformation rules for growth, shares, and drawdowns,
4. state clearly whether a score is descriptive, diagnostic, or predictive,
5. avoid the phrase "failure probability" unless a true supervised exit dataset is introduced.

## References
[1] U.S. Census Bureau — County Business Applications, annual county dataset, public statistical release.
[2] U.S. Office of Management and Budget / U.S. Census Bureau — Core Based Statistical Area delineation reference file, 2023 release.
