---
uid: 4b76268a-826f-47b3-87ad-7bbf95f72c04
title: "ST-Bench"
summary: "Measures multi-agent scientific-analysis coverage, numerical realism, and inference-time tradeoffs."
type: benchmark
created: 2026-11-08
updated: 2026-11-08
depth: full
sources:
  - https://arxiv.org/abs/2610.07763
---

# ST-Bench

**Source:** https://arxiv.org/abs/2610.07763  
**Date:** 2026-10-06  
**Evidence tier:** Author-reported research; not independently reproduced.

## Mechanism

Researchers adapted 100 Earth-science data-analysis tasks into 2,067 paper-grounded queries, then compared five generated multi-agent systems under two training protocols against single-agent baselines on the same GPT-5 backbone.

**Key technique:** Separates coverage (producing a realistic metric) from conditional metric quality, and measures inference time as a first-class constraint.

## Evidence and limitations

Nine of ten multi-agent configurations beat the cheapest single-agent baseline; the strongest nearly tripled the composite score but required about four times the inference time. A more economical configuration retained much of the benefit at under twice the time. These are author-reported benchmark findings.

## Novelty and comparison

The gains largely arise from answering more queries, not necessarily better numbers once a plausible number is produced. This complicates generic claims that more agents mean higher accuracy.

## Reproducible next step

For research extraction, track answered-question coverage, conditional correctness, and total inference time separately. Compare specialist teams to one agent on the same model.

## Assessment

Substantive evaluation, but older than the preferred window and scientific tasks differ from production workflows.

## Relations

- **evaluates:** multi-agent scientific analysis, coverage, numerical realism and inference cost.

## Full-depth synthesis: mechanism and boundaries

**Core mechanism:** Scientific-task evaluation separating coverage, conditional numerical correctness and inference cost. Separate model inference, persistent state, tool privileges, side effects and independent acceptance evidence. The dated source findings above are retained without silently upgrading their evidence tier.

## Evidence quality and counterarguments

**Principal limitation:** Producing more outputs does not imply higher scientific accuracy; author-reported task protocols may differ from real analysis. Potential confounders include task selection, evaluator design, resource budgets and deployment context. Compare to a simpler baseline; distinguish benchmark, user judgement, tool acknowledgement and independently checked task completion. Missing checks are unknown, never passes.

## Directional knowledge relationships

**Analyst-level compares_with:** [[projects/masbench]], [[projects/auto-research]]. These are cross-study comparisons, not verified dependency or implementation links. The item contributes to [[evaluations/briefing-synthesis-2026-11-03-to-09]], [[concepts/verified-completion-vs-apparent-success]] and [[concepts/preservation-aware-agent-improvement]] where relevant. Preserve disagreements and task-level regressions rather than forcing a universal conclusion.

## Reproducible test plan

**Proposed, not executed:** Repeat a fixed 100-query sample across single/multi-agent systems; score coverage, numeric error, abstention and latency. Freeze source snapshots, models, budgets and checker definitions; record each run's full trace, failures, costs, independent acceptance and held-out results. Publish negative cases and per-task changes alongside any aggregate metrics.

## Adoption guidance and unanswered questions

Evaluate first in a constrained environment with explicit authorization, source traceability, validator execution records and rollback. Unknowns: independent replication, transfer beyond source tasks, total operating cost and effects on other consumers of the shared environment.

## Provenance and depth statement

**Full analytical synthesis of the archived briefing**, not a claim that new source experiments were performed or original benchmarks reproduced. Primary URLs and author-reported measurements remain in the earlier sections; proposed interpretations and experiments are editorial analysis.

## Full-depth mechanism and scope

**Scientific multi-agent analysis evaluation.** Model the input/task, worker or evaluator, state transition, persisted artifact and external acceptance oracle separately. The original source and evidence summary above anchors the factual claims. This analysis distinguishes implementation behavior from measurement protocol and operational deployment.

## Evidence quality, negative findings and confounders

**Principal counterweight:** Coverage and conditional numerical correctness can move in opposite directions; output count is not scientific validity. Check whether the cited source reports a controlled comparison, author-only result, user perception, benchmark score, or production observation. These evidence tiers are not interchangeable. Missing independent validation, hidden costs, sampling bias and failure-to-execute checks should be reported rather than assumed away.

## Comparative and typed knowledge synthesis

Compare with [[benchmarks/index]]; [[projects/auto-research]] and [[evaluations/briefing-synthesis-2026-11-03-to-09]]. **Relationship type: compares_with (analyst synthesis)**, not a verified implementation dependency or head-to-head result. For any cross-paper numeric comparison, require matching tasks, models, runtime, budget, and independent scoring before treating differences as meaningful.

## Reproducible evaluation protocol

**Proposed; not executed:** Compare agent teams on held-out scientific datasets, measuring complete tasks, numerical accuracy and compute. Pre-register task set, control, held-out cases, success criteria and failure taxonomy. Record tool and validator execution receipts, raw artifacts, per-task scores, regressions, uncertainty, time and tokens. Fail closed on unknown acceptance outcomes. Preserve negative cases and report false positives and false negatives.

## Practical integration and open questions

Start in an isolated environment with least privilege, explicit state ownership, deterministic checkpoints and rollback. Ask whether the mechanism generalizes beyond the source's distribution, whether a simpler baseline is competitive, and what evidence independently proves success. Record promotion criteria before deployment.

## Provenance and research status

**Full evidence-scoped analytical depth** mined from the archived briefing and its canonical source references. New comparative claims and experiments are analyst hypotheses, not independently reproduced findings. The original paper/repository was not re-run in this pass.
