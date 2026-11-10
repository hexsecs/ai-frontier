---
uid: 4b76268a-826f-47b3-87ad-7bbf95f72c03
title: "MASBench"
summary: "Benchmarks multi-agent protocols, memory, and routing under partially observable tasks."
type: benchmark
created: 2026-11-08
updated: 2026-11-08
depth: full
sources:
  - https://arxiv.org/abs/2610.04672
---

# MASBench

**Source:** https://arxiv.org/abs/2610.04672  
**Date:** 2026-10-03  
**Evidence tier:** Author-reported research; not independently reproduced.

## Mechanism

A multi-agent evaluation suite with reasoning, scheduling and game tasks where each participant sees only partial information. It tests protocol, memory and routing mechanisms and scores task performance alongside communication cost.

**Key technique:** Partial-observability collaboration evaluation, with explicit cost effectiveness rather than assuming all agents can see the global state.

## Evidence and limitations

Authors publish code at https://github.com/BUPT-GAMMA/MASBench and describe deterministic evaluation metrics. This briefing does not extract a single comparable aggregate performance gain from the paper.

## Novelty and comparison

Useful methodological correction: TandemBench supplies full global information, while real agent teams often operate with access boundaries and missing observations.

## Reproducible next step

Test multi-agent OpenShelf mining with per-agent source subsets and measure the information exchanged, final relation accuracy, and token cost.

## Assessment

Important gap-fill rather than a new November launch; inspect code before adopting its scoring.

## Relations

- **evaluates:** multi-agent collaboration under partial observability. **compares_with:** [[projects/tandembench]] (different information assumptions; analyst comparison).

## Full-depth synthesis: mechanism and system boundaries

**Core mechanism:** Partially observable collaboration tasks with explicit communication protocols, routing and memory cost. Distinguish the producing model, its tool/runtime privileges, the persistent artifacts, the evaluator and any human authorization. The original source-specific findings and reported metrics remain above; this section adds comparative analysis rather than implying a fresh independent reproduction.

## Evidence quality, negative results and alternatives

**Principal limitation:** More agent communication can improve coverage yet reduce efficiency; comparisons may depend on information partition and task family. A plausible alternative explanation is evaluator design, resource allocation or domain-specific task selection rather than a universally better agent architecture. Compare against a simpler baseline under equal budgets. Missing outcomes and failed checks are not successes.

## Typed knowledge relationships

**Analyst-level compares_with:** [[projects/tandembench]], [[projects/agensh]], [[projects/st-bench]]. These links are evidence-guided conceptual comparisons, **not** assertions that the projects cite, implement or depend on each other. This entry also contributes to [[evaluations/briefing-synthesis-2026-11-03-to-09]]; its acceptance and preservation implications should be evaluated against [[concepts/verified-completion-vs-apparent-success]] and [[concepts/preservation-aware-agent-improvement]].

## Reproducible evaluation plan

**Proposed; not executed:** Benchmark centralized and decentralized teams at fixed total token budgets under 0%, 30% and 60% information withholding; score task acceptance and communication overhead. Freeze the task inputs, model/runtime, tool permissions and budget; record raw traces, checker invocation receipts, task-level outcomes, cost and failure cases. Pre-register acceptance criteria, include an untouched holdout set and make all candidate regressions visible rather than reporting only aggregate wins.

## Adoption decision and open questions

**Recommendation:** Controlled sandbox evaluation before production integration. Require a rollback path and independent verification of side effects. Unknowns include cross-model transfer, distribution shift, independent replication, operator time, and whether the observed mechanism adds value beyond simpler retrieval or orchestration.

## Depth and provenance

This is a **full analytical mining pass** grounded in the original dated briefing and primary-source links, not a claim of new direct source inspection or reproduced benchmarks. Source-reported measurements and newly proposed engineering interpretations are intentionally distinguished.

## Full-depth mechanism and scope

**Multi-agent protocols under partial observability.** Model the input/task, worker or evaluator, state transition, persisted artifact and external acceptance oracle separately. The original source and evidence summary above anchors the factual claims. This analysis distinguishes implementation behavior from measurement protocol and operational deployment.

## Evidence quality, negative findings and confounders

**Principal counterweight:** More communication may not resolve missing information; performance is sensitive to task allocation and hidden state. Check whether the cited source reports a controlled comparison, author-only result, user perception, benchmark score, or production observation. These evidence tiers are not interchangeable. Missing independent validation, hidden costs, sampling bias and failure-to-execute checks should be reported rather than assumed away.

## Comparative and typed knowledge synthesis

Compare with [[benchmarks/index]]; [[projects/tandembench]] and [[evaluations/briefing-synthesis-2026-11-03-to-09]]. **Relationship type: compares_with (analyst synthesis)**, not a verified implementation dependency or head-to-head result. For any cross-paper numeric comparison, require matching tasks, models, runtime, budget, and independent scoring before treating differences as meaningful.

## Reproducible evaluation protocol

**Proposed; not executed:** Compare centralized, peer-to-peer and role-based teams with controlled partial-information reveals. Pre-register task set, control, held-out cases, success criteria and failure taxonomy. Record tool and validator execution receipts, raw artifacts, per-task scores, regressions, uncertainty, time and tokens. Fail closed on unknown acceptance outcomes. Preserve negative cases and report false positives and false negatives.

## Practical integration and open questions

Start in an isolated environment with least privilege, explicit state ownership, deterministic checkpoints and rollback. Ask whether the mechanism generalizes beyond the source's distribution, whether a simpler baseline is competitive, and what evidence independently proves success. Record promotion criteria before deployment.

## Provenance and research status

**Full evidence-scoped analytical depth** mined from the archived briefing and its canonical source references. New comparative claims and experiments are analyst hypotheses, not independently reproduced findings. The original paper/repository was not re-run in this pass.
