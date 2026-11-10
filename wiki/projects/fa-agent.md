---
uid: 4395c49d-be77-41d3-be9e-66441c1d9ccd
title: "FA-Agent: Multimodal Seismic First-Arrival Picking"
summary: "Visual agent uses processing tools and expert skills to keep, correct or abstain on ambiguous seismic first-arrival picks."
type: project
created: 2026-11-07
updated: 2026-11-07
depth: full
related: [abstention-as-first-class-verdict, improvement-lives-in-external-state]
sources:
  - url: https://arxiv.org/abs/2611.06555
    retrieved: 2026-11-07
---

# FA-Agent: Multimodal Seismic First-Arrival Picking

**Source date:** 2026-11-04. **Primary source:** https://arxiv.org/abs/2611.06555.

## Mechanism and evidence

A multimodal model inspects a seismic gather, zooms into questionable regions, calls processing and quality-control tools, and decides whether to retain, correct or remove an initial first-arrival pick. Expert-reviewed cases are incorporated into reusable skills; a local model can keep survey data on site. The authors processed 1,000 randomly sampled field gathers and present three detailed examples, plus semi-synthetic tests with known arrivals. No independently reproduced quantitative improvement is established in the abstract. The key transferable idea is **evidence-aware removal of uncertain outputs** instead of confident hallucination. **Experiment:** apply the keep/correct/remove triage to noisy CAN frame classification, tracking precision, abstention and expert review burden.

## Evidence status and relations

This is a primary-source account, not an independently executed replication. Related concept pages are analytical cross-project connections, not author-endorsed taxonomies: [[concepts/abstention-as-first-class-verdict]], [[concepts/improvement-lives-in-external-state]].

## Provenance

- https://arxiv.org/abs/2611.06555

## Full-depth synthesis: mechanism and system boundaries

**Core mechanism:** Multimodal seismic inspection with keep, correct or remove decisions, tools and expert-reviewed reusable skills. Distinguish the producing model, its tool/runtime privileges, the persistent artifacts, the evaluator and any human authorization. The original source-specific findings and reported metrics remain above; this section adds comparative analysis rather than implying a fresh independent reproduction.

## Evidence quality, negative results and alternatives

**Principal limitation:** Abstention/removal can improve apparent precision by lowering coverage; expert review and instrument-specific distribution shift must be measured. A plausible alternative explanation is evaluator design, resource allocation or domain-specific task selection rather than a universally better agent architecture. Compare against a simpler baseline under equal budgets. Missing outcomes and failed checks are not successes.

## Typed knowledge relationships

**Analyst-level compares_with:** [[concepts/abstention-as-first-class-verdict]], [[projects/auto-research]], [[projects/st-bench]]. These links are evidence-guided conceptual comparisons, **not** assertions that the projects cite, implement or depend on each other. This entry also contributes to [[evaluations/briefing-synthesis-2026-11-03-to-09]]; its acceptance and preservation implications should be evaluated against [[concepts/verified-completion-vs-apparent-success]] and [[concepts/preservation-aware-agent-improvement]].

## Reproducible evaluation plan

**Proposed; not executed:** Blind 100 first-arrival picks with expert consensus; report retained coverage, error conditional on retention, correction quality and unsafe false confidence. Freeze the task inputs, model/runtime, tool permissions and budget; record raw traces, checker invocation receipts, task-level outcomes, cost and failure cases. Pre-register acceptance criteria, include an untouched holdout set and make all candidate regressions visible rather than reporting only aggregate wins.

## Adoption decision and open questions

**Recommendation:** Controlled sandbox evaluation before production integration. Require a rollback path and independent verification of side effects. Unknowns include cross-model transfer, distribution shift, independent replication, operator time, and whether the observed mechanism adds value beyond simpler retrieval or orchestration.

## Depth and provenance

This is a **full analytical mining pass** grounded in the original dated briefing and primary-source links, not a claim of new direct source inspection or reproduced benchmarks. Source-reported measurements and newly proposed engineering interpretations are intentionally distinguished.
