---
uid: 019a5b21-21b3-7c91-8a42-18d90b5e11f6
title: "Compozy 0.7.1–0.7.2"
summary: "Compozy 0.7.1–0.7.2 implements agent infrastructure relevant to lifecycle, authority, recovery or artifact management."
type: project
created: 2026-11-16
updated: 2026-11-16
depth: brief
sources:
  - https://github.com/compozy/compozy/blob/main/CHANGELOG.md
---

# Compozy 0.7.1–0.7.2

**Source and date:** https://github.com/compozy/compozy/blob/main/CHANGELOG.md (2026-11-15).

Compozy fixes parent wakeups when delegated subagents are deleted or canceled, orphan reconciliation at boot, long-running gate leases, subprocess output retention, session authority preservation and default child-tool scope narrowing. These are explicit production-oriented failure-mode fixes, not benchmarked success rates.

**Mechanism:** Reconcile a durable delegation tree and tool-authority ceiling across cancellation, deletion, process exit and restart.

**Evidence and limits:** The novelty is operational evidence of where multi-agent runtimes fail: a child can disappear while its parent remains blocked or inherits excessive authority. Compared with WorkflowArena's orchestration scoring, this addresses lifecycle correctness. High operational value; maintenance release rather than new research. Release documentation does not independently establish measured reliability.

**Evaluation:** Fault-inject 100 delegated tasks with random child deletion, cancellation and daemon restart. Verify every parent eventually reaches a terminal state, no orphan retains a tool grant and stdout survives process exit.
