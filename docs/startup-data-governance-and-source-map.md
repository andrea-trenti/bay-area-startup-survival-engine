# Startup Data Governance and Source Map

## Abstract

This document defines the source hierarchy, ownership boundaries, measurement logic, and release discipline of the Bay Area Startup Survival Engine. The repository is designed around a strict separation between original analytical work and institution-owned statistical releases. Its empirical shell can be replicated from public sources without republishing those source files inside the repository.

The immediate empirical focus is the Bay Area startup-entry layer: county-level business applications, California-level employer-formation signals, geographic concentration, and operating-context diagnostics. The broader design is modular. Additional layers—such as Business Dynamics Statistics, County Business Patterns, or QCEW labor context—can be added without changing the legal or methodological boundary between source ownership and analytical authorship.

## 1. Why governance matters here

A credible startup repository must solve two problems simultaneously. The first is **measurement**: startup ecosystems are often discussed in broad narrative terms even though the underlying processes—application, employer conversion, labor absorption, survival, and scale—are heterogeneous and only partially observable. The second is **governance**: GitHub repositories frequently mix original analysis with institution-owned files in ways that blur rights, provenance, and reproducibility.

For a repository intended to read as serious academic or analytical work, that ambiguity is unacceptable. The repository therefore adopts a documented source hierarchy, a non-versioned source-data rule, explicit replication conventions, and clear limits on what each empirical layer can establish.

## 2. Source hierarchy

### 2.1 Core sources

The repository is built around four core public source families.

First, **Business Formation Statistics (BFS)** provide monthly and annual information on business applications and projected employer formations. These are the primary entry-layer sources for entrepreneurial inflow and conversion context [1].

Second, **Business Dynamics Statistics (BDS)** provide annual downstream measures such as establishment births, shutdowns, and job creation or destruction. These series are important for later extensions into survival and realized post-entry dynamics [2].

Third, **Quarterly Census of Employment and Wages (QCEW)** provides labor-market and wage context at detailed geographic levels. In this repository, QCEW plays a supporting role: it enriches the operating-context layer when the relevant area files are included in the acquisition layer [3].

Fourth, **official geography crosswalks** from Census and BLS govern county scope, metropolitan delineation, and area-title interpretation [4][5].

### 2.2 Controlled replication boundary

The repository was validated in a controlled replication environment assembled from official public releases. That environment is sufficient to establish the core Bay Area entry layer, verify parser behavior, test path discipline, and confirm that source-contingent modules surface explicit coverage diagnostics under non-matching or unavailable source conditions.

This is the correct methodological stance. A public repository should not presume identical source coverage across independent replications; it should document the source requirements for each layer and make execution boundaries transparent.

### 2.3 Immediate Bay Area stylized facts

Even the entry-layer source set already supports meaningful Bay Area results. The county BFS workbook shows that the nine-county Bay Area recorded **101,112** business applications in 2023 and **97,505** in 2024, a year-over-year decline of roughly **3.6%**. In 2024, Santa Clara County recorded **22,219** applications, Alameda **19,498**, San Francisco **18,699**, Contra Costa **13,311**, San Mateo **9,497**, Sonoma **4,930**, Solano **4,440**, Marin **3,586**, and Napa **1,325** [1]. Santa Clara and San Francisco together accounted for about **42.0%** of Bay Area applications in 2024, while the full nine-county Bay Area represented approximately **18.9%** of California county-level applications [1].

These are entry-layer facts, not claims about startup quality or long-run survival. The repository keeps that distinction explicit throughout.

## 3. Ownership structure

The repository contains three legally distinct layers.

1. **Original analytical work** — Markdown papers, indicator definitions, transformation logic, folder architecture, derived tables, and Python code.
2. **Institution-owned source data** — Census and BLS statistical releases maintained in the non-versioned acquisition layer for replication.
3. **Reproducible derived artifacts** — processed tables and outputs created from the source-acquisition layer.

Only the first layer is published as original repository content. The second and third layers remain outside the public repository unless redistribution is expressly authorized by the issuing institution.

## 4. Measurement discipline

The repository measures entrepreneurial inflow first and only then moves toward conversion and resilience diagnostics.

- **Applications are not startups.** They are leading indicators of entrepreneurial intent [1].
- **Bridge-model outputs are not direct observations.** County-level employer-conversion outputs inherit state-level transition information and must be labeled as modeled proxies [1][2].
- **Labor-context modules are conditional.** QCEW enriches the operating-context layer when the corresponding area files are included in the acquisition layer [3].
- **Geographic scope is explicit.** The repository uses a documented nine-county Bay Area operating definition rather than an implicit “Silicon Valley” shorthand [4][5].

## 5. Release rule

The public repository may include:
- analytical prose,
- methodological standards,
- source-page references,
- expected filenames,
- Python code,
- empty acquisition-layer folders with README files,
- and tests or workflow files.

The public repository should not include raw statistical files or source-dependent derived artifacts unless redistribution is clearly permitted.

## 6. Implications

For founders, the repository shows that Bay Area startup analysis should begin with county-specific entry intensity rather than symbolic regional labels. For investors, it provides a disciplined shell for distinguishing inflow from conversion and resilience. For policymakers, it offers a framework in which entry, labor context, and downstream survival can be analyzed without collapsing them into one imprecise “startup strength” metric.

## 7. Conclusion

The source map is not a housekeeping note; it is part of the analytical design. A startup repository is only as credible as its treatment of ownership, scope, and inference. By separating source ownership from original work and by structuring replication boundaries explicitly, the repository becomes cleaner legally, stronger methodologically, and more credible as public research infrastructure.

## References

[1] U.S. Census Bureau — Business Formation Statistics present release, county workbook, and methodology notes, dataset/documentation.  
[2] U.S. Census Bureau — Business Dynamics Statistics overview and methodological documentation, dataset/documentation.  
[3] U.S. Bureau of Labor Statistics — Quarterly Census of Employment and Wages overview and annual averages documentation, dataset/documentation.  
[4] U.S. Census Bureau — Metropolitan and micropolitan delineation reference files, geographic crosswalk/documentation.  
[5] U.S. Bureau of Labor Statistics — QCEW area-title reference files, geographic crosswalk/documentation.
