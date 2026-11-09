---
uid: a29b51f0-ec09-4b70-9e90-900000000003
title: "ProcGrep / Agent Trajectories as Programs"
summary: "Fingerprints coding-agent procedures from action trajectories rather than outcome scores."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: brief
sources:
  - https://arxiv.org/abs/2606.16988
---

# ProcGrep / Agent Trajectories as Programs

**Source:** https://arxiv.org/abs/2606.16988  
**Date:** 2026-11-02  
**Evidence tier:** Author-reported research; not independently reproduced.

## Mechanism

A procedural representation and ProcGrep auditing library for coding-agent trajectories; compares how agents act across SWE-bench tasks instead of merely scoring final correctness.

**Key technique:** Induce compact procedural vocabularies from traces, then compare action-pattern distributions and behavioral fingerprints.

## Evidence and limitations

The paper reports identification of unseen trajectories from ten agents at 85.7% accuracy and a Jensen–Shannon divergence of 0.25 for a teacher/student comparison. Revised November 2; first posted June 15.

Identification accuracy does not imply safety or correctness. Version update is recent, underlying project is older.

## Novelty and comparison

Complements EvoAudit's per-task regression accounting by measuring changes in the process used to obtain outcomes; can detect procedural drift even when headline success is unchanged.

## Reproducible next step

Fingerprint the source-selection, test-running and citation-checking trajectories of two OpenShelf agents before and after harness changes; flag new shortcuts and missing verification stages.

## Assessment

The dated [[briefings/2026/11/2026-11-09]] report contains the complete comparison and research audit. Treat source-specific findings as evidence, not independently reproduced outcomes.

## Relations

- **Evidence-backed mechanism:** Induce compact procedural vocabularies from traces, then compare action-pattern distributions and behavioral fingerprints. Source: https://arxiv.org/abs/2606.16988.
- **Analyst-level relation:** Complements EvoAudit's per-task regression accounting by measuring changes in the process used to obtain outcomes; can detect procedural drift even when headline success is unchanged.
