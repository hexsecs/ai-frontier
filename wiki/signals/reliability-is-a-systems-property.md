---
uid: e5293fb7-2647-4963-b610-9fe02204e08b
depth: brief
title: "Agent reliability is a systems property"
summary: "A cross-project hypothesis linking verification, recovery, memory, orchestration, and security."
type: signal
created: 2026-11-02
updated: 2026-11-02
sources: []
---

# Agent reliability is a systems property

The imported projects suggest an engineering loop: plan → execute → [verify](../techniques/verification-and-evidence.md) → [recover selectively](../techniques/adaptive-recovery.md) → [update skills and memory](../techniques/agent-skills-and-memory.md) after regression checks → [evaluate](../techniques/evaluation-and-simulation.md). [Orchestration](../techniques/multi-agent-orchestration.md) and [security](../techniques/secure-agent-operations.md) constrain each stage.

**Hypothesis, not validated architecture:** these connections were mined from prior summaries and require source-level verification.

## Proposed experiment

Compare workflows with and without independent verification, contribution-level recovery, and regression-gated memory updates. Measure accuracy, wasted calls, recovery latency, and preserved work.
