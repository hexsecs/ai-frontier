---
uid: 4b76268a-826f-47b3-87ad-7bbf95f72c02
title: "TandemBench"
summary: "Tests whether decision models can select and verify optimal multi-agent coordination plans."
type: project
created: 2026-11-08
updated: 2026-11-08
depth: brief
sources:
  - https://arxiv.org/abs/2611.05827
---

# TandemBench

**Source:** https://arxiv.org/abs/2611.05827  
**Date:** 2026-11-04  
**Evidence tier:** Author-reported research; not independently reproduced.

## Mechanism

A 1,200-question benchmark based on 200 collaborative cooking scenarios and 30 recipe tasks. Execution and exact search determine the best plan; paired questions include or omit the optimal candidate.

**Key technique:** Paired counterfactual optimality verification: distinguish selecting a good supplied plan from detecting when every supplied plan is suboptimal.

## Evidence and limitations

40 native decision models and 10 general language models were evaluated. The strongest native decision model reached 62.50% decision accuracy, while optimality-verification performance stayed near chance. Dataset and evaluation code are public at https://github.com/lililibaohang/TandemBench. Author-reported.

## Novelty and comparison

High for multi-agent decision verification: a router may rank alternatives reasonably but cannot reliably tell when its option set is deficient.

## Reproducible next step

For a coding-agent scheduler, generate paired task-allocation cases with and without the truly optimal plan and score the ability to request a new plan.

## Assessment

Reproducible benchmark design, limited to fully observable simulated coordination.

## Relations

- **evaluates:** optimality of multi-agent coordination decisions. **compares_with:** [[projects/masbench]] (globally observable vs partially observable; analyst comparison).
