---
uid: a29b51f0-ec09-4b70-9e90-900000000003
title: "ProcGrep / Agent Trajectories as Programs"
summary: "Fingerprints coding-agent procedures from action trajectories rather than outcome scores."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: full
sources:
  - https://arxiv.org/abs/2606.16988
---

# ProcGrep / Agent Trajectories as Programs

**Source:** https://arxiv.org/abs/2606.16988  
**Date:** 2026-11-02  
**Evidence tier:** Author-reported research; not independently reproduced.

## Mechanism

A procedural representation and ProcGrep auditing library for coding-agent trajectories; compares how agents act across SWE-bench tasks instead of merely scoring final correctness.

**Key technique:** Induce compact procedural vocabularies from traces, then compare action-pattern distributions and behavioral fingerprints.

## Evidence and limitations

The paper reports identification of unseen trajectories from ten agents at 85.7% accuracy and a Jensen–Shannon divergence of 0.25 for a teacher/student comparison. Revised November 2; first posted June 15.

Identification accuracy does not imply safety or correctness. Version update is recent, underlying project is older.

## Novelty and comparison

Complements EvoAudit's per-task regression accounting by measuring changes in the process used to obtain outcomes; can detect procedural drift even when headline success is unchanged.

## Reproducible next step

Fingerprint the source-selection, test-running and citation-checking trajectories of two OpenShelf agents before and after harness changes; flag new shortcuts and missing verification stages.

## Assessment

The dated [[briefings/2026/11/2026-11-09]] report contains the complete comparison and research audit. Treat source-specific findings as evidence, not independently reproduced outcomes.

## Relations

- **Evidence-backed mechanism:** Induce compact procedural vocabularies from traces, then compare action-pattern distributions and behavioral fingerprints. Source: https://arxiv.org/abs/2606.16988.
- **Analyst-level relation:** Complements EvoAudit's per-task regression accounting by measuring changes in the process used to obtain outcomes; can detect procedural drift even when headline success is unchanged.

## Full-depth synthesis: mechanism and boundaries

**Core mechanism:** Procedural vocabulary induction and agent fingerprinting from action trajectories. Separate model inference, persistent state, tool privileges, side effects and independent acceptance evidence. The dated source findings above are retained without silently upgrading their evidence tier.

## Evidence quality and counterarguments

**Principal limitation:** Identification accuracy does not imply safe behavior; equivalent outcomes can arise from unsafe shortcuts. Potential confounders include task selection, evaluator design, resource budgets and deployment context. Compare to a simpler baseline; distinguish benchmark, user judgement, tool acknowledgement and independently checked task completion. Missing checks are unknown, never passes.

## Directional knowledge relationships

**Analyst-level compares_with:** [[projects/tracybot]], [[projects/evoaudit]]. These are cross-study comparisons, not verified dependency or implementation links. The item contributes to [[evaluations/briefing-synthesis-2026-11-03-to-09]], [[concepts/verified-completion-vs-apparent-success]] and [[concepts/preservation-aware-agent-improvement]] where relevant. Preserve disagreements and task-level regressions rather than forcing a universal conclusion.

## Reproducible test plan

**Proposed, not executed:** Compare 30 task traces before/after agent updates and detect omitted validation steps against independent logs. Freeze source snapshots, models, budgets and checker definitions; record each run's full trace, failures, costs, independent acceptance and held-out results. Publish negative cases and per-task changes alongside any aggregate metrics.

## Adoption guidance and unanswered questions

Evaluate first in a constrained environment with explicit authorization, source traceability, validator execution records and rollback. Unknowns: independent replication, transfer beyond source tasks, total operating cost and effects on other consumers of the shared environment.

## Provenance and depth statement

**Full analytical synthesis of the archived briefing**, not a claim that new source experiments were performed or original benchmarks reproduced. Primary URLs and author-reported measurements remain in the earlier sections; proposed interpretations and experiments are editorial analysis.
