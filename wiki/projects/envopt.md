---
uid: a29b51f0-ec09-4b70-9e90-900000000001
title: "EnvOpt"
summary: "Optimizes persistent information environments to reduce agent cost and improve task success."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: full
sources:
  - https://arxiv.org/abs/2611.07372
---

# EnvOpt

**Source:** https://arxiv.org/abs/2611.07372  
**Date:** 2026-11-05  
**Evidence tier:** Author-reported research; not independently reproduced.

## Mechanism

Automated end-to-end modification of stationary agent environments such as document, ticket and workspace information organization, using tasks without reference answers or explicit graders.

**Key technique:** Environment optimization as a third optimization axis alongside model weights and agent harnesses.

## Evidence and limitations

On AutomationBench, authors report Claude Haiku 4.5 cost reduced 72.7% and pass rate improved 14.34%; transfer to Opus 5 reduced cost 68.1% and improved pass rate 1.34%. On top of an optimized Meta-Harness, a further 83.4% cost reduction and 11.17% accuracy increase are reported. Units for accuracy improvements are as described in the abstract and should not be casually interpreted as percentage points.

Author-reported benchmarks; no independent replication inspected. Environment changes can benefit a benchmark while harming other users or downstream tools.

## Novelty and comparison

A shared knowledge base can itself be optimized for agent consumption. Unlike the earlier Context as Infrastructure project, the intervention searches the environment end to end rather than only changing retrieved claim representations.

## Reproducible next step

A/B test AI Frontier's current Markdown/wiki layout against agent-optimized entry points on 30 held-out ingestion tasks, measuring token cost, verified relationship precision, and navigation failures.

## Assessment

The dated [[briefings/2026/11/2026-11-09]] report contains the complete comparison and research audit. Treat source-specific findings as evidence, not independently reproduced outcomes.

## Relations

- **Evidence-backed mechanism:** Environment optimization as a third optimization axis alongside model weights and agent harnesses. Source: https://arxiv.org/abs/2611.07372.
- **Analyst-level relation:** A shared knowledge base can itself be optimized for agent consumption. Unlike the earlier Context as Infrastructure project, the intervention searches the environment end to end rather than only changing retrieved claim representations.

## Full-depth synthesis: mechanism and boundaries

**Core mechanism:** Optimizing stationary documents and shared workspace structure independently of model weights and harness. Separate model inference, persistent state, tool privileges, side effects and independent acceptance evidence. The dated source findings above are retained without silently upgrading their evidence tier.

## Evidence quality and counterarguments

**Principal limitation:** Author-reported cost and pass-rate improvements may overfit benchmark workflows and harm human readers. Potential confounders include task selection, evaluator design, resource budgets and deployment context. Compare to a simpler baseline; distinguish benchmark, user judgement, tool acknowledgement and independently checked task completion. Missing checks are unknown, never passes.

## Directional knowledge relationships

**Analyst-level compares_with:** [[projects/strategist]], [[projects/tigerless-agent-memory]]. These are cross-study comparisons, not verified dependency or implementation links. The item contributes to [[evaluations/briefing-synthesis-2026-11-03-to-09]], [[concepts/verified-completion-vs-apparent-success]] and [[concepts/preservation-aware-agent-improvement]] where relevant. Preserve disagreements and task-level regressions rather than forcing a universal conclusion.

## Reproducible test plan

**Proposed, not executed:** A/B 30 held-out KB tasks on baseline and optimized structure; score independently checked relations, tokens and navigation failures. Freeze source snapshots, models, budgets and checker definitions; record each run's full trace, failures, costs, independent acceptance and held-out results. Publish negative cases and per-task changes alongside any aggregate metrics.

## Adoption guidance and unanswered questions

Evaluate first in a constrained environment with explicit authorization, source traceability, validator execution records and rollback. Unknowns: independent replication, transfer beyond source tasks, total operating cost and effects on other consumers of the shared environment.

## Provenance and depth statement

**Full analytical synthesis of the archived briefing**, not a claim that new source experiments were performed or original benchmarks reproduced. Primary URLs and author-reported measurements remain in the earlier sections; proposed interpretations and experiments are editorial analysis.
