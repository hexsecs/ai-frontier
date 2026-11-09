---
uid: 4b76268a-826f-47b3-87ad-7bbf95f72c01
title: "EvoAudit / Beneath the Surface"
summary: "Audits harness self-evolution for forgotten tasks, cost, transfer, and misleading selection criteria."
type: project
created: 2026-11-08
updated: 2026-11-08
depth: brief
sources:
  - https://arxiv.org/abs/2611.07624
---

# EvoAudit / Beneath the Surface

**Source:** https://arxiv.org/abs/2611.07624  
**Date:** 2026-11-05  
**Evidence tier:** Author-reported research; not independently reproduced.

## Mechanism

Researchers compared four harness-evolution methods across general and coding tasks, repeated trials, controlled expansions, component interventions, and candidate-admission replays. EvoAudit revises the selection, analysis, mutation and gate stages in response.

**Key technique:** Preservation-aware recursive self-improvement: compare per-task coverage before and after mutation, measure deployment cost and transfer, and avoid selecting candidates by a single aggregate score.

## Evidence and limitations

All 16 evolved agents gained some previously unsolved tasks while losing some previously solved tasks. One general-task case gained 5.2 reliability points but lost ten previously covered tasks. The highest-scoring candidate was not the best mean improver in any of four candidate pools. Results are author-reported, not independently reproduced.

## Novelty and comparison

High: directly exposes regressions hidden by self-improvement leaderboards, complementing yesterday's Strategist strategy library and the existing capability-locus concept.

## Reproducible next step

For each evolving OpenShelf extraction strategy, retain a task-by-task regression ledger, deployment cost, held-out transfer tests and a rollback candidate.

## Assessment

Strong diagnostic research; prioritize preservation metrics over headline gains.

## Relations

- **evaluates:** harness evolution and regression preservation. **compares_with:** [[projects/strategist]] (analyst comparison; sources are separate studies).
