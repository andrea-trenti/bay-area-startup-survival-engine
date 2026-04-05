# Out-of-Time Validation and Backtesting Standard
## Evaluation rules for annual Bay Area startup nowcasts built from public U.S. statistical releases

## Purpose
This standard defines how real-time and pseudo-real-time startup nowcasts must be evaluated in this repository. Its scope is narrow by design: it governs annual nowcasts of the Bay Area business-application pipeline derived from the U.S. Census Bureau's Business Formation Statistics monthly release and the annual county business-applications file.[1][2] It does not govern venture-funding forecasts, startup exits, patent forecasts, or firm-level valuation models.

A public-data startup repository becomes fragile very quickly when forecast claims are reported without a disciplined evaluation protocol. The typical failure mode is straightforward: a model looks persuasive in-sample, the analyst reports a single error statistic, and the forecast is then treated as stable even though it may only work under one calendar pattern or one post-shock period. This repository therefore treats evaluation as a first-class analytical object rather than a cosmetic appendix.

The governing principle is that every annual nowcast must be judged under the information set that would have existed at the forecast origin. That implies that historical shares, seasonal fractions, and scaling parameters must be estimated using only data available before the target year. Any benchmark that leaks future information into the calibration window is invalid for publication.

## Validation architecture
### 1. Target variable
The target variable is the annual Bay Area business-applications total:

$$A_t^{BA} = \sum_{i \in \mathcal{B}} A_{i,t}$$

where $A_{i,t}$ is the annual number of business applications in Bay Area county $i$ during year $t$, and $\mathcal{B}$ is the fixed nine-county operating universe used in the repository.

### 2. Information set
At forecast origin $(t,m)$, where $t$ is year and $m$ is the latest observed month, only the following information is admissible:
- monthly California Business Formation Statistics values observed through month $m$ of year $t$;[1]
- annual Bay Area county values up to year $t-1$ from the county business-applications release;[2]
- the fixed geographic mapping rules documented elsewhere in the repository.[3]

### 3. Preferred pseudo-real-time backtest
The preferred backtest is a rolling-origin exercise:
1. choose a forecast cutoff month such as March, June, or September;
2. compute the year-$t$ California year-to-date total through month $m$;
3. estimate the historical year-end completion fraction using only prior years;
4. convert California YTD to a California annual forecast;
5. multiply by a lagged Bay Area share of California applications estimated only from prior years;
6. compare the resulting forecast with the realized Bay Area annual total.

This design avoids the false precision of high-frequency county modeling, which is not supported by the public releases in scope.

## Required forecast windows
Every model revision must be tested at a minimum on the following cutoffs:
- **March cut-off**: early-year signal under high uncertainty.
- **June cut-off**: mid-year update with materially more information.
- **September cut-off**: late-year estimate used to assess whether the model meaningfully improves as the year matures.

Additional months may be reported, but these three windows are mandatory because they reveal whether the model's value is primarily in early identification or only in near-completion extrapolation.

## Required metrics
Each backtest table must report the following metrics for every cutoff:

### Mean absolute percentage error
$$MAPE = \frac{100}{N} \sum_{t=1}^{N} \left| \frac{\hat{A}_t^{BA} - A_t^{BA}}{A_t^{BA}} \right|$$

### Root mean squared error
$$RMSE = \sqrt{\frac{1}{N}\sum_{t=1}^{N}(\hat{A}_t^{BA} - A_t^{BA})^2}$$

### Mean error
$$ME = \frac{1}{N}\sum_{t=1}^{N}(\hat{A}_t^{BA} - A_t^{BA})$$

### Median absolute percentage error
$$MdAPE = median\left(100 \times \left| \frac{\hat{A}_t^{BA} - A_t^{BA}}{A_t^{BA}} \right|\right)$$

### Directional accuracy
A supplementary statistic should indicate whether the forecast captured the sign of the year-over-year change in the Bay Area total.

A single metric is never sufficient. MAPE can look acceptable while the model remains systematically biased; RMSE can be dominated by one shock year; mean error can hide instability when positive and negative misses offset. The repository therefore reports the full set.

## Benchmark hierarchy
Any new forecast model must be compared against, at minimum, three baselines:

1. **Naive carry-forward share model**  
   Bay Area share in year $t$ equals the previous year's realized share.

2. **Rolling-average share model**  
   Bay Area share in year $t$ equals the average share over a trailing window, typically three years.

3. **Historical completion-fraction model**  
   California annual total is extrapolated from YTD using the average historical completion fraction at the same month.

A new model should not be described as an improvement unless it beats these baselines on at least two of the three required cutoffs or materially improves early-year accuracy without damaging later-window stability.

## Window governance
The preferred default is:
- trailing **5-year** average for calendar completion fractions;
- trailing **3-year** average for the Bay Area share of California applications.

Those window lengths are pragmatic rather than sacred. They balance two competing objectives:
- using enough history to stabilize the denominator;
- avoiding pre-pandemic patterns dominating post-2020 dynamics.

Any change in those windows must be documented explicitly and justified in methodological terms. Silent window changes are not permitted.

## Shock treatment
Pandemic-era distortions, administrative revisions, or structural breaks should not be removed automatically. The baseline position is to include the full historical sample unless there is clear statistical or institutional evidence that a period is non-comparable. If an analyst excludes a period, the repository must publish:
- the rule used for exclusion;
- the resulting change in estimated error;
- the qualitative reason why the excluded period is not informative.

## Publication rules
A forecast note may describe a model as:
- **stable**, if it improves or broadly matches baseline error across March, June, and September cutoffs;
- **promising but immature**, if it improves March or June error but deteriorates later windows;
- **not publication-ready**, if it does not outperform the baseline or if its gains depend entirely on one atypical period.

The phrase **prediction of startup survival** must not be used for these nowcasts. The target is the annual application pipeline, not realized startup mortality or downstream venture outcomes.

## Documentation requirements
Every file that reports a nowcast or historical backtest must include:
- the target definition;
- the cutoff month;
- the estimation window;
- the baseline(s) used for comparison;
- the error metrics reported;
- the data sources and release dates used;
- a caveat stating that public business-applications data are upstream formation indicators rather than direct startup-performance measures.

## References
[1] U.S. Census Bureau — Business Formation Statistics monthly public release, dataset and methodology notes.  
[2] U.S. Census Bureau — County business-applications annual dataset, public county-level file.  
[3] U.S. Office of Management and Budget / U.S. Census Bureau — CBSA and CSA delineation reference file used for geographic validation and county coding.
