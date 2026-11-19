---
uid: 7217a117-3d75-46cc-900f-f6b65d3aba96
title: "Preservation-aware agent improvement"
summary: "An evolved agent strategy must retain previously verified task coverage, not merely increase aggregate benchmark performance."
type: concept
created: 2026-11-09
updated: 2026-11-19
depth: full
sources:
  - https://arxiv.org/abs/2611.03618
  - https://arxiv.org/abs/2611.07624
  - https://arxiv.org/abs/2611.07372
  - https://arxiv.org/abs/2610.42141
  - https://arxiv.org/abs/2610.07763
  - https://arxiv.org/abs/2611.21056
  - https://arxiv.org/abs/2611.23067
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

## Mechanism integration and persistent values

[[projects/elite-evaluation-free-self-improvement]] ([November 16 paper](https://arxiv.org/abs/2611.21056)) changes the selection signal: multiple agent-harness mechanisms are developed independently from a common parent and combined by code inspection and deterministic validity checks rather than by downstream candidate task scores. Its reported 60.0% to 85.6% SWE-bench Pro improvement demonstrates a promising alternative to expensive evaluate-and-select, **not** that the resulting agent preserved all previously solved cases. Evaluation-free applies inside the candidate evolution loop; final benchmarks still evaluate the outcome. This contrasts with [[projects/evoaudit]]'s measured task losses under conventional evolution, but neither study performs a head-to-head preservation test across identical tasks.

[[projects/values-shape-self-improving-coding-agents]] ([November 17 paper](https://arxiv.org/abs/2611.23067)) introduces a separate optimization input: a short value statement in persistent instructions affects the kinds of solutions evolved and their held-out performance. Allowing the agent to revise the statement narrows the observed treatment differences. This is evidence that the instruction file is a mutable capability input, not evidence that a value statement enforces security. For reproducible improvement, freeze policy and instruction versions during comparisons and explicitly test what happens when the agent can edit them.

A discriminating preservation experiment should factorially vary candidate-selection mechanism (evaluate/select versus source-level integration) and instruction mutability (fixed versus self-editable), while holding baseline tasks, evaluation budget and hidden regression cases fixed. Report new solves, lost solves, critical failures and cost separately. Author-reported results from the two studies are not directly comparable and do not establish a general performance ranking.

