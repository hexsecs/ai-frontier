---
uid: 48bc81ce-4e5b-4e21-8f7b-261114000002
title: agent-browser
summary: Rust CLI for agent-driven browser control with snapshot references and experimental recorded flow replay.
type: project
created: 2026-11-14
updated: 2026-11-16
depth: full
sources:
  - https://github.com/vercel-labs/agent-browser
  - https://github.com/vercel-labs/agent-browser/releases/tag/v0.42.0
  - https://github.com/vercel-labs/agent-browser/releases/tag/v0.43.0
---

# agent-browser

The CLI exposes browser actions and compact accessibility snapshots with element references. Version 0.42.0 (November 10, 2026) adds experimental saved flows that try direct HTTP replay, in-page requests and browser command replay. Version 0.43.0 (November 12) adds contextual hints to distinguish ambiguous or unlabeled controls. These are implemented release features, not measured task-success improvements.

The replay hierarchy extends constrained browser execution ideas in [[projects/fastbrowse|fastbrowse]] and [[projects/baya-compile-then-execute|Baya]] but introduces state-consistency and authorization concerns when substituting requests for GUI actions. An independent read-after-write acceptance check is needed for consequential tasks.

**Experiment:** Replay five disposable browser tasks and measure success, latency, token cost, and unintended side effects under stale sessions.

Sources: https://github.com/vercel-labs/agent-browser/releases/tag/v0.42.0 ; https://github.com/vercel-labs/agent-browser/releases/tag/v0.43.0

## Conceptual context

Distinguish reconstructing history, rerunning a procedure and safely repeating its intended effect. See [[concepts/replay-idempotency-and-effect-semantics]]. Compare reusable procedures by applicability conditions, execution boundaries and fallback rather than assuming universal benefits. See [[techniques/deterministic-workflow-reuse]].
