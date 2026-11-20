---
uid: 0cc0daba-ce30-4a88-8d35-6e44813c6be4
title: "openJiuwen Agent Core 0.1.20"
summary: "Cancel-safe delegated execution with source-grounded mechanisms and evidence limits."
type: project
created: 2026-11-20
updated: 2026-11-20
depth: full
sources:
  - https://github.com/openJiuwen-ai/agent-core/releases/tag/v0.1.20
---

# openJiuwen Agent Core 0.1.20

**Primary source:** https://github.com/openJiuwen-ai/agent-core/releases/tag/v0.1.20. **Source date:** 2026-10-29.

## Demonstrated capability and mechanism

The release adds long-lived expert teams, scheduled verifier/challenger review, computer use and model routing, plus fixes to canceled queued tasks executing and restart-time MCP reconnect. Explicit scheduling, reviewer roles, timeouts and state-transition corrections across cancellation and recovery.

**Reusable concept:** Cancel-safe delegated execution. Older substantial runtime release, not new November research. Maintainer release notes; no independent stress test.

## Boundaries and test

Queue 100 tasks, cancel 30 before start, restart, and assert none of the canceled tasks execute.

This is a proposed experiment, not an independently reproduced result. See [[briefings/2026/11/2026-11-20]] and [[concepts/verified-completion-vs-apparent-success]] for comparisons and acceptance limits.
