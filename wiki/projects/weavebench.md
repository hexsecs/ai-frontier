---
uid: a29b51f0-ec09-4b70-9e90-900000000004
title: "WeaveBench"
summary: "Evaluates real desktop agents across GUI, CLI and code with trajectory-aware checks."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: brief
sources:
  - https://aclanthology.org/2026.emnlp-main.658/
---

# WeaveBench

**Source:** https://aclanthology.org/2026.emnlp-main.658/  
**Date:** 2026-10  
**Evidence tier:** Peer-reviewed benchmark; author-reported measurements.

## Mechanism

A 114-task benchmark across eight work domains using a real Ubuntu desktop, requiring mixed GUI, command-line and coding actions within the same long-horizon workflow.

**Key technique:** Cross-interface trajectories with a judge that examines files, screenshots, logs and actions, including shortcut or fabricated-evidence detection.

## Evidence and limitations

Best reported PassRate is 41.2% across evaluated model/runtime pairings. Outcome-only grading overestimated performance. Peer-reviewed EMNLP 2026 publication in October; not a November release.

Benchmark conditions are specific to the configured Ubuntu desktop and judge; no evidence of generalized real-world reliability.

## Novelty and comparison

A stronger end-to-end test than browser-only or terminal-only benchmarks, directly relevant to agents that edit code, inspect browser output and manipulate desktop tools.

## Reproducible next step

Construct ten mixed-interface tests for a local agent: read a repository, use a browser to inspect source docs, modify code, run tests, and provide verifiable screenshots and artifacts.

## Assessment

The dated [[briefings/2026/11/2026-11-09]] report contains the complete comparison and research audit. Treat source-specific findings as evidence, not independently reproduced outcomes.

## Relations

- **Evidence-backed mechanism:** Cross-interface trajectories with a judge that examines files, screenshots, logs and actions, including shortcut or fabricated-evidence detection. Source: https://aclanthology.org/2026.emnlp-main.658/.
- **Analyst-level relation:** A stronger end-to-end test than browser-only or terminal-only benchmarks, directly relevant to agents that edit code, inspect browser output and manipulate desktop tools.
