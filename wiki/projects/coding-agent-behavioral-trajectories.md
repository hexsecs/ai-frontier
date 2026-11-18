---
uid: a8f431d0-70d2-4c88-b39c-6b4a1ef70118
title: "Interpreting Coding Agents Through Their Behavioral Trajectories"
summary: "Process observability distinct from task success: A deterministic rule-based parser maps heterogeneous raw traces to normaliz"
type: project
created: 2026-11-18
updated: 2026-11-18
depth: full
sources:
  - https://arxiv.org/abs/2611.17440
---

# Interpreting Coding Agents Through Their Behavioral Trajectories

**Primary source:** https://arxiv.org/abs/2611.17440 (published 2026-11-12). Engineering finding; evidence is author-reported unless otherwise noted.

## Implementation and general mechanism

The authors analyze 143,209 trajectories from 125 configurations and 117 models, auditing parser annotations against a six-model consensus on 500 events. The released parser and analysis pipeline distinguish behavioral profiles even among agents with similar task success.

The general concept is **process observability distinct from task success**. A deterministic rule-based parser maps heterogeneous raw traces to normalized search, edit and test actions, then compares aggregate behavioral fingerprints.

## Novelty and evidence boundary

A large-scale, action-normalized comparison across agent stacks, complementing earlier ProcGrep procedural fingerprinting without claiming the same method. Parser agreement with model consensus is not human ground truth; cross-repository task composition is not fully controlled, and profiles do not establish causal superiority.

Compare [[projects/procgrep]] and [[techniques/evaluation-and-simulation]]: both study traces, but the parser, corpus and evaluation differ.

## Practical implication and proposed test

Collect normalized search/edit/test trajectories alongside acceptance tests for coding-agent CI, and compare behaviors only under matched tasks and budgets.

**Proposed, unexecuted:** Run two agent harnesses on 15 identical pinned issues; normalize their traces and compare test-before-edit rate, repeated searches, and accepted patches without using success as a parser feature.
