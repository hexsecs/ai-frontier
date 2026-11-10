---
uid: 4b76268a-826f-47b3-87ad-7bbf95f72c01
title: "EvoAudit / Beneath the Surface"
summary: "Audits harness self-evolution for forgotten tasks, cost, transfer, and misleading selection criteria."
type: project
created: 2026-11-08
updated: 2026-11-08
depth: full
sources:
  - https://arxiv.org/abs/2611.07624
---

# EvoAudit / Beneath the Surface

**Source:** https://arxiv.org/abs/2611.07624  
**Date:** 2026-11-05  
**Evidence tier:** Author-reported research; not independently reproduced.

## Mechanism

Researchers compared four harness-evolution methods across general and coding tasks, repeated trials, controlled expansions, component interventions, and candidate-admission replays. EvoAudit revises the selection, analysis, mutation and gate stages in response.

**Key technique:** Preservation-aware recursive self-improvement: compare per-task coverage before and after mutation, measure deployment cost and transfer, and avoid selecting candidates by a single aggregate score.

## Evidence and limitations

All 16 evolved agents gained some previously unsolved tasks while losing some previously solved tasks. One general-task case gained 5.2 reliability points but lost ten previously covered tasks. The highest-scoring candidate was not the best mean improver in any of four candidate pools. Results are author-reported, not independently reproduced.

## Novelty and comparison

High: directly exposes regressions hidden by self-improvement leaderboards, complementing yesterday's Strategist strategy library and the existing capability-locus concept.

## Reproducible next step

For each evolving OpenShelf extraction strategy, retain a task-by-task regression ledger, deployment cost, held-out transfer tests and a rollback candidate.

## Assessment

Strong diagnostic research; prioritize preservation metrics over headline gains.

## Relations

- **evaluates:** harness evolution and regression preservation. **compares_with:** [[projects/strategist]] (analyst comparison; sources are separate studies).

## Full-depth synthesis: mechanism and system boundaries

**Core mechanism:** Per-task gain/loss auditing of harness-evolution candidate selection, mutation, cost and transfer. Distinguish the producing model, its tool/runtime privileges, the persistent artifacts, the evaluator and any human authorization. The original source-specific findings and reported metrics remain above; this section adds comparative analysis rather than implying a fresh independent reproduction.

## Evidence quality, negative results and alternatives

**Principal limitation:** All 16 evaluated evolved agents both gained and lost coverage; aggregate gains can conceal critical regressions, while strict no-regression gates can block useful specialization. A plausible alternative explanation is evaluator design, resource allocation or domain-specific task selection rather than a universally better agent architecture. Compare against a simpler baseline under equal budgets. Missing outcomes and failed checks are not successes.

## Typed knowledge relationships

**Analyst-level compares_with:** [[concepts/preservation-aware-agent-improvement]], [[projects/strategist]], [[projects/envopt]]. These links are evidence-guided conceptual comparisons, **not** assertions that the projects cite, implement or depend on each other. This entry also contributes to [[evaluations/briefing-synthesis-2026-11-03-to-09]]; its acceptance and preservation implications should be evaluated against [[concepts/verified-completion-vs-apparent-success]] and [[concepts/preservation-aware-agent-improvement]].

## Reproducible evaluation plan

**Proposed; not executed:** Replay candidate admission under baseline aggregate scoring versus preservation-aware critical-task gates; count forgotten tasks, transfer and cost. Freeze the task inputs, model/runtime, tool permissions and budget; record raw traces, checker invocation receipts, task-level outcomes, cost and failure cases. Pre-register acceptance criteria, include an untouched holdout set and make all candidate regressions visible rather than reporting only aggregate wins.

## Adoption decision and open questions

**Recommendation:** Controlled sandbox evaluation before production integration. Require a rollback path and independent verification of side effects. Unknowns include cross-model transfer, distribution shift, independent replication, operator time, and whether the observed mechanism adds value beyond simpler retrieval or orchestration.

## Depth and provenance

This is a **full analytical mining pass** grounded in the original dated briefing and primary-source links, not a claim of new direct source inspection or reproduced benchmarks. Source-reported measurements and newly proposed engineering interpretations are intentionally distinguished.
