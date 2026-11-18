---
uid: 6d13b0c9-4f8a-4e71-9a63-1190cced0118
title: "Agent Behavior as Code (ABCAgent)"
summary: "Reusable parameterized executable behavior: A model designs or revises a symbolic program with unbound inputs; a determ"
type: project
created: 2026-11-18
updated: 2026-11-18
depth: full
sources:
  - https://arxiv.org/abs/2610.04824
---

# Agent Behavior as Code (ABCAgent)

**Primary source:** https://arxiv.org/abs/2610.04824 (published 2026-10-04). Engineering finding; evidence is author-reported unless otherwise noted.

## Implementation and general mechanism

Authors evaluate on six benchmarks, including task variants; they report 71.9% versus 47.4% Pass^4 on a telecom benchmark, and 98.3% versus 97.3% on GSM-Symbolic. Program reuse avoids repeating full model-controlled loops.

The general concept is **reusable parameterized executable behavior**. A model designs or revises a symbolic program with unbound inputs; a deterministic executor runs it, with neural calls only at declared points and variant checks before reuse.

## Novelty and evidence boundary

Programs are explicitly rebindable and tested on generated input variants before admission; contrasts with a prompt-only or record-and-replay procedure. October discovery, not a new November release. Author-reported single-harness comparisons; deterministic control does not prove correct assumptions. One-off WorkArena tasks reportedly cost more.

Compare [[techniques/deterministic-workflow-reuse]]: program reuse still needs an applicability and regression gate.

## Practical implication and proposed test

Compile repetitive engineering checks into parameterized procedures, but gate reuse with metamorphic tests and allow a model-controlled fallback for changed conditions.

**Proposed, unexecuted:** Implement a five-step repository audit as an agent loop and a generated Python procedure; vary repository and branch inputs across 20 runs and compare correctness, cost, and regression on altered inputs.
