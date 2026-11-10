---
uid: a29b51f0-ec09-4b70-9e90-900000000004
title: "WeaveBench"
summary: "Evaluates real desktop agents across GUI, CLI and code with trajectory-aware checks."
type: benchmark
created: 2026-11-09
updated: 2026-11-09
depth: full
sources:
  - https://aclanthology.org/2026.emnlp-main.658/
---

# WeaveBench

**Source:** https://aclanthology.org/2026.emnlp-main.658/  
**Date:** 2026-10  
**Evidence tier:** Peer-reviewed benchmark; author-reported measurements.

## Mechanism

A 114-task benchmark across eight work domains using a real Ubuntu desktop, requiring mixed GUI, command-line and coding actions within the same long-horizon workflow.

**Key technique:** Cross-interface trajectories with a judge that examines files, screenshots, logs and actions, including shortcut or fabricated-evidence detection.

## Evidence and limitations

Best reported PassRate is 41.2% across evaluated model/runtime pairings. Outcome-only grading overestimated performance. Peer-reviewed EMNLP 2026 publication in October; not a November release.

Benchmark conditions are specific to the configured Ubuntu desktop and judge; no evidence of generalized real-world reliability.

## Novelty and comparison

A stronger end-to-end test than browser-only or terminal-only benchmarks, directly relevant to agents that edit code, inspect browser output and manipulate desktop tools.

## Reproducible next step

Construct ten mixed-interface tests for a local agent: read a repository, use a browser to inspect source docs, modify code, run tests, and provide verifiable screenshots and artifacts.

## Assessment

The dated [[briefings/2026/11/2026-11-09]] report contains the complete comparison and research audit. Treat source-specific findings as evidence, not independently reproduced outcomes.

## Relations

- **Evidence-backed mechanism:** Cross-interface trajectories with a judge that examines files, screenshots, logs and actions, including shortcut or fabricated-evidence detection. Source: https://aclanthology.org/2026.emnlp-main.658/.
- **Analyst-level relation:** A stronger end-to-end test than browser-only or terminal-only benchmarks, directly relevant to agents that edit code, inspect browser output and manipulate desktop tools.

## Full-depth synthesis: mechanism and boundaries

**Core mechanism:** 114 long-horizon desktop tasks combining GUI, shell and code, with trajectory-aware assessment. Separate model inference, persistent state, tool privileges, side effects and independent acceptance evidence. The dated source findings above are retained without silently upgrading their evidence tier.

## Evidence quality and counterarguments

**Principal limitation:** Reported pass rate depends on model/runtime and judge; outcome-only checks can overcount success. Potential confounders include task selection, evaluator design, resource budgets and deployment context. Compare to a simpler baseline; distinguish benchmark, user judgement, tool acknowledgement and independently checked task completion. Missing checks are unknown, never passes.

## Directional knowledge relationships

**Analyst-level compares_with:** [[projects/fincosmos]], [[projects/cua-agentenv]]. These are cross-study comparisons, not verified dependency or implementation links. The item contributes to [[evaluations/briefing-synthesis-2026-11-03-to-09]], [[concepts/verified-completion-vs-apparent-success]] and [[concepts/preservation-aware-agent-improvement]] where relevant. Preserve disagreements and task-level regressions rather than forcing a universal conclusion.

## Reproducible test plan

**Proposed, not executed:** Run 20 tasks with snapshot resets; compare outcome-only and trace-aware graders, false acceptance and checker coverage. Freeze source snapshots, models, budgets and checker definitions; record each run's full trace, failures, costs, independent acceptance and held-out results. Publish negative cases and per-task changes alongside any aggregate metrics.

## Adoption guidance and unanswered questions

Evaluate first in a constrained environment with explicit authorization, source traceability, validator execution records and rollback. Unknowns: independent replication, transfer beyond source tasks, total operating cost and effects on other consumers of the shared environment.

## Provenance and depth statement

**Full analytical synthesis of the archived briefing**, not a claim that new source experiments were performed or original benchmarks reproduced. Primary URLs and author-reported measurements remain in the earlier sections; proposed interpretations and experiments are editorial analysis.
