---
uid: 23abcbf8-64ae-4817-b6c2-71fd45bce65f
title: "ASPIRE robotics"
summary: "Coding agents refine executable sensorimotor skills, storing improvements in a skill repository."
type: project
created: 2026-11-24
updated: 2026-11-25
depth: full
sources:
  - https://github.com/NVlabs/ASPIRE
---

# ASPIRE robotics

**Source:** https://github.com/NVlabs/ASPIRE. **Date:** October 2026 v1.0 (older release).

## Mechanism

ASPIRE treats skill code refinement as continual learning and parallel practice as distributed training. The README reports 99% success on 80 LIBERO-Pro tasks for v1.0. See [[techniques/agent-skills-and-memory]] for the related mechanism and its evaluation boundaries.

## Evidence limits

Author-reported benchmark result; no independent replication or proof of safe physical operation. Full evaluation protocol was not inspected.

## Proposed experiment

In simulation, compare frozen and iteratively refined skills against fixed held-out tasks; record regressions, success and API cost. Not executed.
