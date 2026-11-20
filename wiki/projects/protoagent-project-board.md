---
uid: 1f567c0b-3d20-4fa8-a015-266a5f169b1c
title: "protoAgent Project Board"
summary: "Durable work-state reconciliation with source-grounded mechanisms and evidence limits."
type: project
created: 2026-11-20
updated: 2026-11-20
depth: full
sources:
  - https://github.com/protoLabsAI/projectBoard-plugin
---

# protoAgent Project Board

**Primary source:** https://github.com/protoLabsAI/projectBoard-plugin. **Source date:** 2026-11-19.

## Demonstrated capability and mechanism

A beads-backed Kanban work graph dispatches ready cards through ACP coding agents into disposable worktrees, gates PRs and reconciles unfinished work after restart. Cards are projections of a single work graph; execution, review and merge update explicit states.

**Reusable concept:** Durable work-state reconciliation. Concrete workboard-to-PR integration; November 19 denotes repository activity, not verified release date. No independent throughput benchmark.

## Boundaries and test

Interrupt six disposable cards before and after PR creation; verify no duplicate PRs or stranded tasks after restart.

This is a proposed experiment, not an independently reproduced result. See [[briefings/2026/11/2026-11-20]] and [[concepts/verified-completion-vs-apparent-success]] for comparisons and acceptance limits.
