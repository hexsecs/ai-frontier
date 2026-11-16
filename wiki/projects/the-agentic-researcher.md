---
uid: f49edda6-73de-46b1-918c-9ac2cadad07c
title: The Agentic Researcher
summary: Sandboxed CLI agents conduct long-running scientific investigations with scheduled checks and reproducible reporting conventions.
type: project
created: '2026-11-16'
updated: 2026-11-16
depth: full
sources:
- https://arxiv.org/html/2603.15914
- https://github.com/ZIB-IOL/The-Agentic-Researcher
---

# The Agentic Researcher

## Mechanism and evidence

[The Agentic Researcher](https://arxiv.org/html/2603.15914) combines methodological instructions with a sandboxed container and existing CLI coding agents for mathematical and computational research. Its account includes multi-node experiments, scheduled monitoring and idle periods between checks. These are author-reported demonstrations, not a measured reliability distribution.

Long duration is distinct from lifecycle correctness. Scheduling a later check does not itself establish successful experiment completion, artifact provenance or safe recovery. [[concepts/agent-state-and-lifecycle]] explains these distinctions; [[techniques/artifact-and-claim-provenance]] explains what evidence a reported conclusion needs.

## Limits and proposed experiment

Humans set research direction and assess results. Sandboxing and methodological prompts do not establish scientific validity or eliminate the need for cost controls and independent acceptance. The framework's portability claim is not a head-to-head benchmark of all supported harnesses.

Run a bounded parameter sweep with immutable configurations, fixed spending and independent evaluation of outputs. Interrupt one worker and inspect recovery, logs and repeated effects. Compare reproducibility and accepted outcomes, not only unattended hours. This is a proposed experiment, not a completed replication.

## Provenance

The March paper is the older exploratory selection in [[briefings/2026/11/2026-11-14]]. Its separate identity must not be confused with [[projects/autosr]], a different scientific search system.

## Conceptual context

Compare persistence, interrupted work and reconciliation without assuming exactly-once external effects. See [[techniques/durable-agent-execution]].
