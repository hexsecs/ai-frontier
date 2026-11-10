---
uid: 4b76268a-826f-47b3-87ad-7bbf95f72c02
title: "TandemBench"
summary: "Tests whether decision models can select and verify optimal multi-agent coordination plans."
type: benchmark
created: 2026-11-08
updated: 2026-11-08
depth: full
sources:
  - https://arxiv.org/abs/2611.05827
---

# TandemBench

**Source:** https://arxiv.org/abs/2611.05827  
**Date:** 2026-11-04  
**Evidence tier:** Author-reported research; not independently reproduced.

## Mechanism

A 1,200-question benchmark based on 200 collaborative cooking scenarios and 30 recipe tasks. Execution and exact search determine the best plan; paired questions include or omit the optimal candidate.

**Key technique:** Paired counterfactual optimality verification: distinguish selecting a good supplied plan from detecting when every supplied plan is suboptimal.

## Evidence and limitations

40 native decision models and 10 general language models were evaluated. The strongest native decision model reached 62.50% decision accuracy, while optimality-verification performance stayed near chance. Dataset and evaluation code are public at https://github.com/lililibaohang/TandemBench. Author-reported.

## Novelty and comparison

High for multi-agent decision verification: a router may rank alternatives reasonably but cannot reliably tell when its option set is deficient.

## Reproducible next step

For a coding-agent scheduler, generate paired task-allocation cases with and without the truly optimal plan and score the ability to request a new plan.

## Assessment

Reproducible benchmark design, limited to fully observable simulated coordination.

## Relations

- **evaluates:** optimality of multi-agent coordination decisions. **compares_with:** [[projects/masbench]] (globally observable vs partially observable; analyst comparison).

## Full-depth synthesis: mechanism and system boundaries

**Core mechanism:** Paired coordination-plan questions with and without the actual optimal plan, grounded in executable collaborative tasks. Distinguish the producing model, its tool/runtime privileges, the persistent artifacts, the evaluator and any human authorization. The original source-specific findings and reported metrics remain above; this section adds comparative analysis rather than implying a fresh independent reproduction.

## Evidence quality, negative results and alternatives

**Principal limitation:** A decision model can select the best supplied option while failing to recognize that all supplied options are suboptimal; simulation optimum is domain-specific. A plausible alternative explanation is evaluator design, resource allocation or domain-specific task selection rather than a universally better agent architecture. Compare against a simpler baseline under equal budgets. Missing outcomes and failed checks are not successes.

## Typed knowledge relationships

**Analyst-level compares_with:** [[projects/masbench]], [[projects/agensh]], [[concepts/verified-completion-vs-apparent-success]]. These links are evidence-guided conceptual comparisons, **not** assertions that the projects cite, implement or depend on each other. This entry also contributes to [[evaluations/briefing-synthesis-2026-11-03-to-09]]; its acceptance and preservation implications should be evaluated against [[concepts/verified-completion-vs-apparent-success]] and [[concepts/preservation-aware-agent-improvement]].

## Reproducible evaluation plan

**Proposed; not executed:** Construct 50 paired plan-selection cases; withhold the optimum in half; score correct selection, correct rejection, regret and reasoning cost. Freeze the task inputs, model/runtime, tool permissions and budget; record raw traces, checker invocation receipts, task-level outcomes, cost and failure cases. Pre-register acceptance criteria, include an untouched holdout set and make all candidate regressions visible rather than reporting only aggregate wins.

## Adoption decision and open questions

**Recommendation:** Controlled sandbox evaluation before production integration. Require a rollback path and independent verification of side effects. Unknowns include cross-model transfer, distribution shift, independent replication, operator time, and whether the observed mechanism adds value beyond simpler retrieval or orchestration.

## Depth and provenance

This is a **full analytical mining pass** grounded in the original dated briefing and primary-source links, not a claim of new direct source inspection or reproduced benchmarks. Source-reported measurements and newly proposed engineering interpretations are intentionally distinguished.

## Full-depth mechanism and scope

**Selection and verification of multi-agent coordination plans.** Model the input/task, worker or evaluator, state transition, persisted artifact and external acceptance oracle separately. The original source and evidence summary above anchors the factual claims. This analysis distinguishes implementation behavior from measurement protocol and operational deployment.

## Evidence quality, negative findings and confounders

**Principal counterweight:** Selecting a plausible team plan does not prove global optimality; scoring depends on candidate-plan coverage. Check whether the cited source reports a controlled comparison, author-only result, user perception, benchmark score, or production observation. These evidence tiers are not interchangeable. Missing independent validation, hidden costs, sampling bias and failure-to-execute checks should be reported rather than assumed away.

## Comparative and typed knowledge synthesis

Compare with [[benchmarks/index]]; [[projects/masbench]] and [[evaluations/briefing-synthesis-2026-11-03-to-09]]. **Relationship type: compares_with (analyst synthesis)**, not a verified implementation dependency or head-to-head result. For any cross-paper numeric comparison, require matching tasks, models, runtime, budget, and independent scoring before treating differences as meaningful.

## Reproducible evaluation protocol

**Proposed; not executed:** Generate plans for 30 tasks, hold out optimal-plan evidence, compare selected plans with independent execution outcomes. Pre-register task set, control, held-out cases, success criteria and failure taxonomy. Record tool and validator execution receipts, raw artifacts, per-task scores, regressions, uncertainty, time and tokens. Fail closed on unknown acceptance outcomes. Preserve negative cases and report false positives and false negatives.

## Practical integration and open questions

Start in an isolated environment with least privilege, explicit state ownership, deterministic checkpoints and rollback. Ask whether the mechanism generalizes beyond the source's distribution, whether a simpler baseline is competitive, and what evidence independently proves success. Record promotion criteria before deployment.

## Provenance and research status

**Full evidence-scoped analytical depth** mined from the archived briefing and its canonical source references. New comparative claims and experiments are analyst hypotheses, not independently reproduced findings. The original paper/repository was not re-run in this pass.
