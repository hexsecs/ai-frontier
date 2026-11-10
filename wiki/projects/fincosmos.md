---
uid: 8b867faa-1a65-4b5a-a927-41c40ccc9e78
title: "FINCOSMOS: An Open-World Evaluation Paradigm for Agents in Finance"
summary: "Open-world agent evaluation combines hidden user intent, live data acquisition, point-in-time replay and programmatic veto checks."
type: project
created: 2026-11-07
updated: 2026-11-07
depth: full
related: [scoped-assurance, protocol-relative-scores, abstention-as-first-class-verdict]
sources:
  - url: https://arxiv.org/abs/2611.07464
    retrieved: 2026-11-07
---

# FINCOSMOS: An Open-World Evaluation Paradigm for Agents in Finance

**Source date:** 2026-11-05. **Primary source:** https://arxiv.org/abs/2611.07464.

## Mechanism and evidence

A simulated user holds a hidden compositional strategy; agents must elicit the specification, fetch their own web data, implement a cutoff-safe backtest, and submit an auditable report. Programmatic verification recomputes metrics and checks 15 veto conditions. In 150 sessions across four coding agents and a no-tools model, **zero** were accepted, even when the simulated user signed off. Agents elicited only 54–64% of unspecified details. Authors report expert attribution of 88.33% of failures to agents. With feedback and persistent memory, one agent learned ten tasks, but the exact training/evaluation separation must be inspected before interpreting this as general transfer. The strongest finding is a **user approval versus correctness gap**. **Experiment:** build hidden-intent, source-cutoff and recomputation vetoes for agent-generated security research reports.

## Evidence status and relations

This is a primary-source account, not an independently executed replication. Related concept pages are analytical cross-project connections, not author-endorsed taxonomies: [[concepts/scoped-assurance]], [[concepts/protocol-relative-scores]], [[concepts/abstention-as-first-class-verdict]].

## Provenance

- https://arxiv.org/abs/2611.07464

## Full-depth synthesis: mechanism and system boundaries

**Core mechanism:** Hidden compositional user intent, independently sourced point-in-time market data, and programmatic veto/recomputation. Distinguish the producing model, its tool/runtime privileges, the persistent artifacts, the evaluator and any human authorization. The original source-specific findings and reported metrics remain above; this section adds comparative analysis rather than implying a fresh independent reproduction.

## Evidence quality, negative results and alternatives

**Principal limitation:** Zero full acceptances among 150 reported sessions is benchmark-specific; hidden requirements can be stringent, and subjective user approval cannot substitute for numerical audit. A plausible alternative explanation is evaluator design, resource allocation or domain-specific task selection rather than a universally better agent architecture. Compare against a simpler baseline under equal budgets. Missing outcomes and failed checks are not successes.

## Typed knowledge relationships

**Analyst-level compares_with:** [[concepts/verified-completion-vs-apparent-success]], [[projects/weavebench]], [[experiments/hidden-acceptance-regression-ingestion]]. These links are evidence-guided conceptual comparisons, **not** assertions that the projects cite, implement or depend on each other. This entry also contributes to [[evaluations/briefing-synthesis-2026-11-03-to-09]]; its acceptance and preservation implications should be evaluated against [[concepts/verified-completion-vs-apparent-success]] and [[concepts/preservation-aware-agent-improvement]].

## Reproducible evaluation plan

**Proposed; not executed:** Create 30 hidden-requirement research tasks with cutoff dates, fabricated data and conflicting approvals; compare agent self-score, human approval and independent acceptance. Freeze the task inputs, model/runtime, tool permissions and budget; record raw traces, checker invocation receipts, task-level outcomes, cost and failure cases. Pre-register acceptance criteria, include an untouched holdout set and make all candidate regressions visible rather than reporting only aggregate wins.

## Adoption decision and open questions

**Recommendation:** Controlled sandbox evaluation before production integration. Require a rollback path and independent verification of side effects. Unknowns include cross-model transfer, distribution shift, independent replication, operator time, and whether the observed mechanism adds value beyond simpler retrieval or orchestration.

## Depth and provenance

This is a **full analytical mining pass** grounded in the original dated briefing and primary-source links, not a claim of new direct source inspection or reproduced benchmarks. Source-reported measurements and newly proposed engineering interpretations are intentionally distinguished.
