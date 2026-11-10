---
uid: dd2c44b0-b381-4922-96a1-45231a4634eb
title: "ToolSpace — Execution-grounded tool environments"
summary: "A pipeline for synthesizing realistic multi-tool agent tasks from real MCP traces. It extracts data, state and retry dep"
type: project
created: 2026-11-10
updated: 2026-11-10
depth: full
sources:
  - https://arxiv.org/abs/2611.05036
---

# ToolSpace — Execution-grounded tool environments

**Source and date:** https://arxiv.org/abs/2611.05036 (2026-11-03).

## Mechanism

A pipeline for synthesizing realistic multi-tool agent tasks from real MCP traces. It extracts data, state and retry dependencies from adjacent calls, clusters tool-composition graphs, generates stateful scenarios and retains only tasks replayable from a known initial state. Execution-witnessed dependency graphs, state-aware random walks, rollback, and assertion-based task checks.

## Evidence and novelty

Authors report that harder benchmark variants reduce seven frontier models' scores by as much as 38.2 points; average score for Qwen3.6-35B-A3B rises from 23.0 to 41.0 with their training pipeline (43.2 with RL). High: uses observed tool interactions as the foundation of environment synthesis, rather than LLM-imagined workflows.

## Comparison

Extends the Nov 9 EnvOpt theme in a different direction: EnvOpt reorganizes environments for better agents; ToolSpace constructs execution-valid environments to train and stress agents.

## Limitations

Training and benchmark scores are author-reported; synthetic environments may omit real service outages and permission boundaries.

## Reproducible next step

Capture sanitized GitHub, CI and OpenShelf tool traces; infer state dependencies, synthesize 20 replayable multi-tool tasks, and compare against manually written test tasks.

## Related

- [[briefings/2026/11/2026-11-10]] — dated full-fidelity research and cross-project synthesis.
