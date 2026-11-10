---
uid: 7217a117-3d75-46cc-900f-f6b65d3aba96
title: "Preservation-aware agent improvement"
summary: "An evolved agent strategy must retain previously verified task coverage, not merely increase aggregate benchmark performance."
type: concept
created: 2026-11-09
updated: 2026-11-09
depth: full
sources:
  - https://arxiv.org/abs/2611.03618
  - https://arxiv.org/abs/2611.07624
  - https://arxiv.org/abs/2611.07372
  - https://arxiv.org/abs/2610.42141
  - https://arxiv.org/abs/2610.07763
---

# Preservation-aware agent improvement

## Claim and mechanism

Optimizing an agent's strategies, harness, or environment can increase aggregate performance while harming individual tasks. A durable improvement loop needs a **regression ledger**, immutable held-out tests, cost accounting, and rollback. This is a cross-study design inference, not a shared technique proven by the authors collectively.

## Evidence and distinctions

- **Strategist** ([[projects/strategist]], [paper](https://arxiv.org/abs/2611.03618)) evolves reusable inference programs and reports improvements on 24/30 benchmarks, with reported lower inference cost. This demonstrates strategy search, **not** a guarantee that all previously solved cases are retained.
- **EvoAudit** ([[projects/evoaudit]], [paper](https://arxiv.org/abs/2611.07624)) reports that all 16 evolved agents both gained and lost task coverage; one improved reliability by 5.2 points while losing ten solved tasks. Its selection diagnostics directly motivate preservation-aware admission.
- **EnvOpt** ([[projects/envopt]], [paper](https://arxiv.org/abs/2611.07372)) optimizes the persistent information environment; its cost and accuracy gains are author-reported under AutomationBench conditions. Shared-environment changes can have effects on other tasks that were not in the optimization objective.
- **RoboArchitect** ([[briefings/2026/11/2026-11-03]], [paper](https://arxiv.org/abs/2610.42141)) evolves a control harness around a frozen robot policy. This locates adaptation outside model weights, but its domain and evaluation tier differ from coding agents.
- **ST-Bench** ([[projects/st-bench]], [paper](https://arxiv.org/abs/2610.07763)) separates multi-agent answer coverage from conditional numerical quality and inference time. More completed outputs need not mean more accurate outputs.

## Limits and counterexamples

EvoAudit's loss of coverage does not establish that every optimization harms retained tasks. Some task distributions tolerate deliberate trade-offs. Strong preservation requirements can prevent beneficial specialization. Record the allowed regression budget explicitly instead of pretending all metrics can improve simultaneously.

## Typed relations

- EvoAudit **evaluates and bounds** Strategist-style evolutionary selection; this is an analytical comparison across independent papers, not a published head-to-head.
- EnvOpt **extends the optimization locus** from harness/strategy to external environment.
- ST-Bench **evaluates** the distinction between coverage and conditional correctness, a necessary guardrail for measuring any improvement.
- **Extends** [[concepts/capability-locus]], [[concepts/improvement-lives-in-external-state]], and [[concepts/protocol-relative-scores]].

## Experiment: task-level preservation gate

Use 30 previously validated OpenShelf extraction cases and 20 untouched transfer cases. Compare baseline, strategy-evolved, and environment-optimized variants. Store per-task before/after correctness, newly solved cases, previously solved cases lost, relation precision, abstention, tokens, wall time and revert success. Reject a candidate if it breaks a critical source-integrity case even when mean score improves.

## Evidence status

Synthesis grounded in author-reported studies; no independent reproduction or production deployment demonstrated here.
