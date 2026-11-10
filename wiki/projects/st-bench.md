---
uid: 4b76268a-826f-47b3-87ad-7bbf95f72c04
title: "ST-Bench"
summary: "Measures multi-agent scientific-analysis coverage, numerical realism, and inference-time tradeoffs."
type: benchmark
created: 2026-11-08
updated: 2026-11-08
depth: brief
sources:
  - https://arxiv.org/abs/2610.07763
---

# ST-Bench

**Source:** https://arxiv.org/abs/2610.07763  
**Date:** 2026-10-06  
**Evidence tier:** Author-reported research; not independently reproduced.

## Mechanism

Researchers adapted 100 Earth-science data-analysis tasks into 2,067 paper-grounded queries, then compared five generated multi-agent systems under two training protocols against single-agent baselines on the same GPT-5 backbone.

**Key technique:** Separates coverage (producing a realistic metric) from conditional metric quality, and measures inference time as a first-class constraint.

## Evidence and limitations

Nine of ten multi-agent configurations beat the cheapest single-agent baseline; the strongest nearly tripled the composite score but required about four times the inference time. A more economical configuration retained much of the benefit at under twice the time. These are author-reported benchmark findings.

## Novelty and comparison

The gains largely arise from answering more queries, not necessarily better numbers once a plausible number is produced. This complicates generic claims that more agents mean higher accuracy.

## Reproducible next step

For research extraction, track answered-question coverage, conditional correctness, and total inference time separately. Compare specialist teams to one agent on the same model.

## Assessment

Substantive evaluation, but older than the preferred window and scientific tasks differ from production workflows.

## Relations

- **evaluates:** multi-agent scientific analysis, coverage, numerical realism and inference cost.
