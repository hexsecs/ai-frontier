---
uid: 00000000-0000-4000-8000-09ce894552e7
title: "LLM-as-Code: Agentic Programming for Agent Harness"
summary: "Call-tree/DAG-derived context and deterministic control flow rather than an LLM controlling every step."
type: project
created: 2026-11-11
updated: 2026-11-11
depth: brief
sources:
  - https://arxiv.org/abs/2606.15874
---

# LLM-as-Code: Agentic Programming for Agent Harness

**Original source:** https://arxiv.org/abs/2606.15874  
**Date:** 2026-11-09 revision (original June 14)  
**Evidence status:** Author-reported research; not independently replicated in this knowledge base.

## Mechanism

A program-directed agent harness where deterministic code owns branching, looping and stopping while models are invoked for bounded reasoning; the paper includes a computer-use case study and links implementation code.

Call-tree/DAG-derived context and deterministic control flow rather than an LLM controlling every step.

## Significance and comparison

Separates the model's probabilistic judgments from the workflow's correctness-critical transitions. A substantive recent revision, not a newly introduced November project.

Complements RECEIPT's execution-state observation: control-flow ownership and truthful completion are distinct layers.

## Practical experiment

Refactor one 20-step browser or CI workflow into explicit program-owned states with model calls only for ambiguous decisions; compare retries, token usage and unverified completion.

## Limits

The abstract reports greater stability without a headline quantitative figure; no independent replication was conducted.

## Related

- [[briefings/2026/11/2026-11-11]]
