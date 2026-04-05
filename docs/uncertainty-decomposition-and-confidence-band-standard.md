# Uncertainty Decomposition and Confidence-Band Standard
## Rules for expressing statistical, structural, and interpretive uncertainty in public Bay Area startup diagnostics

## Objective
This document defines how uncertainty must be represented whenever the repository publishes derived indicators, scorecards, scenario tables, or annual nowcasts based on public startup-proxy data.[1][2] The purpose is not rhetorical caution. It is analytical hygiene. Public entrepreneurial datasets are useful precisely because they are broad, consistent, and transparent. They are also limited because they operate upstream of many outcomes users care about, including venture financing, revenue growth, and startup survival. Any technical project that ignores that distinction will overstate what the evidence can support.

The repository therefore separates uncertainty into explicit layers rather than compressing it into vague language. Each analytical output must identify which part of the conclusion is data-rich, which part is model-dependent, and which part is interpretive.

## Uncertainty layers
### 1. Measurement uncertainty
Measurement uncertainty comes from the raw source itself. Examples include:
- administrative lags or revisions in monthly releases;[1]
- incomplete present-year coverage;
- differences between monthly statewide and annual county releases;
- classification choices embedded in public statistical systems.

Measurement uncertainty is generally narrower than conceptual uncertainty, but it must still be disclosed when latest-observation values are incomplete or subject to revision.

### 2. Sampling or aggregation uncertainty
These public files are generally administrative or universe-style releases rather than classical survey samples, yet uncertainty still enters through aggregation decisions. A Bay Area total depends on a fixed set of counties. A resilience score depends on the weighting of volatility, momentum, drawdown, and scale. An annual nowcast depends on how state-level monthly data are translated into regional totals. This is not random noise in the textbook sense; it is model-architecture uncertainty.

### 3. Structural uncertainty
Structural uncertainty arises because the observed indicator is not the final economic object of interest. Business applications are not employer births, and employer births are not startup exits or venture returns.[1][2] A county can look strong on application momentum and still perform poorly on downstream conversion. Structural uncertainty is therefore highest whenever the analysis moves from observed upstream flow to inferred downstream outcome.

### 4. Scenario uncertainty
Scenario uncertainty is the uncertainty introduced by assumptions. If a note imposes alternative completion fractions, different share windows, or stress assumptions for county momentum, those assumptions must be separated clearly from observed data. Scenario outputs should never be described as estimates of fact.

## Confidence-band policy
The repository allows two classes of interval statements.

### A. Statistical bands around a model output
These may be used when the output emerges from a repetitive, explicitly defined procedure such as rolling backtests or bootstrap resampling. The method used to construct the band must be documented. Acceptable methods include:
- empirical percentile bands from rolling backtest errors;
- bootstrap distributions using historical residuals;
- deterministic sensitivity ranges from bounded parameter changes.

### B. Interpretation bands
Where formal interval estimation is not credible, the output must instead use qualitative interpretation bands:
- **high confidence**: conclusion is directly observed and consistent across windows;
- **moderate confidence**: conclusion depends on limited transformation but remains stable across specifications;
- **low confidence**: conclusion relies on strong structural mapping or short-sample assumptions.

The repository should prefer interpretation bands to pseudo-precise numeric intervals when the data-generating process does not justify formal probabilistic language.

## Required decomposition for any major claim
Every major claim must be decomposed into:
1. **Observed statement** — what the raw data directly show.
2. **Derived statement** — what follows after a transparent transformation.
3. **Interpretive statement** — what is being inferred about the startup ecosystem.

For example:
- Observed: Bay Area annual business applications fell from 101,112 in 2023 to 97,505 in 2024.[2]
- Derived: the decline equals 3.6 percent year over year.[2]
- Interpretive: the entrepreneurial inflow softened in 2024, but the data do not establish whether downstream startup quality deteriorated.

This structure prevents category errors.

## Sensitivity protocol
Every score or forecast published in the repository must undergo at least one sensitivity check. Acceptable sensitivity checks include:
- changing the trailing window length;
- excluding one anomalous period;
- replacing z-score normalization with min-max normalization;
- testing a median-based scale instead of a mean-based scale;
- removing the scale component from a composite score.

Sensitivity results must be summarized succinctly:
- unchanged ranking or conclusion;
- modest ranking drift with stable top/bottom group;
- substantial reordering, implying low robustness.

## Language control
The following claims are prohibited unless directly supported by the data:
- “the model predicts startup failure”;
- “the score measures startup quality”;
- “the nowcast captures venture activity”;
- “confidence interval” without a defined construction rule.

Preferred language:
- “upstream entrepreneurial pipeline”;
- “formation proxy”;
- “relative resilience score”;
- “diagnostic range”;
- “scenario envelope.”

## Practical publication rule
A result may be highlighted prominently only if:
- the sign and direction are stable across reasonable specifications;
- the result is not driven by a single county with small base effects;
- the result survives at least one alternative window or normalization rule.

If these conditions are not met, the conclusion must be demoted to a caveat or appendix-level observation.

## References
[1] U.S. Census Bureau — Business Formation Statistics monthly public release, methodology and definitions.  
[2] U.S. Census Bureau — County business-applications annual public file.  
[3] U.S. Census Bureau — geographic delineation and county coding references used to enforce a fixed regional universe.
