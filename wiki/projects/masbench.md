---
uid: 4b76268a-826f-47b3-87ad-7bbf95f72c03
title: "MASBench"
summary: "Benchmarks multi-agent protocols, memory, and routing under partially observable tasks."
type: benchmark
created: 2026-11-08
updated: 2026-11-08
depth: brief
sources:
  - https://arxiv.org/abs/2610.04672
---

# MASBench

**Source:** https://arxiv.org/abs/2610.04672  
**Date:** 2026-10-03  
**Evidence tier:** Author-reported research; not independently reproduced.

## Mechanism

A multi-agent evaluation suite with reasoning, scheduling and game tasks where each participant sees only partial information. It tests protocol, memory and routing mechanisms and scores task performance alongside communication cost.

**Key technique:** Partial-observability collaboration evaluation, with explicit cost effectiveness rather than assuming all agents can see the global state.

## Evidence and limitations

Authors publish code at https://github.com/BUPT-GAMMA/MASBench and describe deterministic evaluation metrics. This briefing does not extract a single comparable aggregate performance gain from the paper.

## Novelty and comparison

Useful methodological correction: TandemBench supplies full global information, while real agent teams often operate with access boundaries and missing observations.

## Reproducible next step

Test multi-agent OpenShelf mining with per-agent source subsets and measure the information exchanged, final relation accuracy, and token cost.

## Assessment

Important gap-fill rather than a new November launch; inspect code before adopting its scoring.

## Relations

- **evaluates:** multi-agent collaboration under partial observability. **compares_with:** [[projects/tandembench]] (different information assumptions; analyst comparison).
