---
uid: d691c930-8bb3-4f68-996a-bac137a64f23
title: "ServerBench: Agent-Designed LLM Serving Systems"
summary: "A benchmark where coding agents modify complete specialized LLM serving systems and experiment against latency-qualified token value per GPU"
type: project
created: 2026-11-13
updated: 2026-11-13
depth: brief
related: [verified-completion-vs-apparent-success]
sources:
  - https://arxiv.org/abs/2611.06841
---

# ServerBench: Agent-Designed LLM Serving Systems

**Source:** https://arxiv.org/abs/2611.06841. **Publication:** 2026-11-04. **Evidence:** author-reported; no independent replication.

## Mechanism
A benchmark where coding agents modify complete specialized LLM serving systems and experiment against latency-qualified token value per GPU dollar, with stateful replay and independent verification.

**Technique:** Closed-loop infrastructure optimization with workload-relevant experiments, stateful session replay and acceptance tests for optimized execution paths.

## Evidence and limitations
Across 11 agent models and three deployments, 22 of 33 runs produced verified systems and 13 beat the strongest baseline. Best reported result is 2.97 value-dollars per GPU dollar on Gemma E4B, 4.87× the vLLM reference.

Author-reported on specified GPU deployments; best-run comparisons do not establish typical improvement.

## Comparison
Moves beyond patch correctness to autonomous systems-performance engineering with an externally measurable objective.

Related: [[concepts/verified-completion-vs-apparent-success]]; relation is analytical, not a demonstrated integration.

## Proposed experiment
In a sandbox, let two coding agents optimize a small inference service against a fixed replay trace; require correctness, p95 latency and cost accounting.

## Provenance
[[briefings/2026/11/2026-11-13]] — complete dated narrative.
