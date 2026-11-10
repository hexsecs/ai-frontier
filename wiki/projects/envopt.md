---
uid: a29b51f0-ec09-4b70-9e90-900000000001
title: "EnvOpt"
summary: "Optimizes persistent information environments to reduce agent cost and improve task success."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: brief
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
