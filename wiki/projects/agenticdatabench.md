---
uid: 71c2a91e-3b0d-47f9-9c21-2d17b6a50118
title: "AgenticDataBench: Real Data-Agent Workflow Evaluation"
summary: "Skill-composition coverage for data workflows: The benchmark extracts recurring data-science skills from task solutions, c"
type: benchmark
created: 2026-11-18
updated: 2026-11-18
depth: full
sources:
  - https://arxiv.org/abs/2607.01647
---

# AgenticDataBench: Real Data-Agent Workflow Evaluation

**Primary source:** https://arxiv.org/abs/2607.01647 (published 2026-07-02). Exploratory, older discovery; evidence is author-reported unless otherwise noted.

## Implementation and general mechanism

The authors release a testbed with task and evaluation scripts and describe five real B2B fintech use cases, skill clusters and a held-out private set of 98 tasks in the repository.

The general concept is **skill-composition coverage for data workflows**. The benchmark extracts recurring data-science skills from task solutions, clusters them and composes real and generated tasks spanning 15 domains with fine-grained ground truth.

## Novelty and evidence boundary

An exploratory application of skill-level coverage and realistic data workflows outside the usual coding-agent benchmark; not a new November paper. July research; some tasks are synthetic and private test cases cannot be independently inspected. Repository leaderboard claims are not independent replications.

[[concepts/protocol-relative-scores]] and [[techniques/evaluation-and-simulation]] clarify why skill composition and withheld test cases matter.

## Practical implication and proposed test

Use a skill-coverage matrix to detect blind spots in recurring research and data-analysis agents rather than relying on aggregate pass rates.

**Proposed, unexecuted:** Construct 12 synthetic data-cleaning tasks from four reusable skills; withhold three compositions, compare an agent's skill-level errors and final outputs against deterministic reference queries.
