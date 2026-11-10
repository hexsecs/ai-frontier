---
uid: dabbda38-5d69-44a0-adfc-eaef69fa768a
title: "Agent-R² — Real-source productivity task synthesis"
summary: "A training-data pipeline grounded in occupational task seeds, workflow evidence and authentic web-sourced attachments. F"
type: project
created: 2026-11-10
updated: 2026-11-10
depth: full
sources:
  - https://arxiv.org/abs/2611.08219
---

# Agent-R² — Real-source productivity task synthesis

**Source and date:** https://arxiv.org/abs/2611.08219 (2026-11-05).

## Mechanism

A training-data pipeline grounded in occupational task seeds, workflow evidence and authentic web-sourced attachments. From 10,000 candidates it constructs 4,000 tasks with multi-format files and deliverable-level rubrics, then trains a 4B agent with supervised and reinforcement learning. Real-document task grounding, fine-grained deliverable rubrics, and training against shortcut-prone agent behavior.

## Evidence and novelty

Authors report Agent-R²-4B scores 51.0% on GDPval and 14.8% on OfficeQA, versus 48.0% and 13.8% for their cited Qwen3-235B comparison. High: shifts optimization toward realistic file-grounded deliverables instead of isolated tool-call benchmarks.

## Comparison

Like WeaveBench from Nov 9, it evaluates deliverables; unlike WeaveBench, it synthesizes training examples and trains a smaller model.

## Limitations

Author-reported model comparison; benchmark task distributions and model settings matter, and no independent replication was checked.

## Reproducible next step

Create 20 real-document deliverable tasks from permission-cleared technical standards and project files; grade factual grounding, artifact correctness and unsupported shortcuts separately.

## Related

- [[briefings/2026/11/2026-11-10]] — dated full-fidelity research and cross-project synthesis.
