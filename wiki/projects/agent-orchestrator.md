---
uid: 4b76268a-826f-47b3-87ad-7bbf95f72c05
title: "Agent Orchestrator (OrchestratorInc)"
summary: "Runs coding-agent fleets with isolated worktrees, CI-repair reactions, and review escalation."
type: project
created: 2026-11-08
updated: 2026-11-08
depth: brief
sources:
  - https://github.com/OrchestratorInc/agent-orchestrator
---

# Agent Orchestrator (OrchestratorInc)

**Source:** https://github.com/OrchestratorInc/agent-orchestrator  
**Date:** 2026-11-08 (repository inspected; launch date unverified)  
**Evidence tier:** Implementation documented; no independent benchmark.

## Mechanism

An open-source fleet manager for parallel coding agents, with isolated worktrees, branches and pull requests, configurable runtime/agent adapters, and event-driven reactions to CI failures and review comments. Repository describes desktop and mobile supervision.

**Key technique:** Lifecycle orchestration with event-triggered repair and human escalation instead of an always-running supervising model.

## Evidence and limitations

The public repository and README document implementation surfaces and configuration, but this briefing has not reproduced throughput, reliability or cost improvements. Repository inspection date is not a release date; the repository's original launch date is unverified.

## Novelty and comparison

Incremental components but practical integration: directly relevant to automating OpenShelf PR repair. Unlike a generic multi-agent chat framework, the control unit is a worktree/PR lifecycle.

## Reproducible next step

Pilot two parallel coding agents on low-risk KB maintenance issues, enforce a two-retry CI repair cap, and track merge-ready PRs per dollar plus human intervention rate.

## Assessment

Practical implementation worth evaluating; do not mistake repository features for production evidence.

## Relations

- **implements:** worktree-isolated coding-agent execution, CI reaction handling and review escalation.
