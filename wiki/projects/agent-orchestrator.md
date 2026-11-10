---
uid: 4b76268a-826f-47b3-87ad-7bbf95f72c05
title: "Agent Orchestrator (OrchestratorInc)"
summary: "Runs coding-agent fleets with isolated worktrees, CI-repair reactions, and review escalation."
type: project
created: 2026-11-08
updated: 2026-11-08
depth: full
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

## Full-depth synthesis: mechanism and boundaries

**Core mechanism:** Isolated worktrees, PR-based agent handoffs, event-driven CI repair and review escalation. Separate model inference, persistent state, tool privileges, side effects and independent acceptance evidence. The dated source findings above are retained without silently upgrading their evidence tier.

## Evidence quality and counterarguments

**Principal limitation:** A working fleet manager is not proof of productivity; CI-repair loops and conflicts can outweigh parallelism. Potential confounders include task selection, evaluator design, resource budgets and deployment context. Compare to a simpler baseline; distinguish benchmark, user judgement, tool acknowledgement and independently checked task completion. Missing checks are unknown, never passes.

## Directional knowledge relationships

**Analyst-level compares_with:** [[projects/agensh]], [[workflows/index]]. These are cross-study comparisons, not verified dependency or implementation links. The item contributes to [[evaluations/briefing-synthesis-2026-11-03-to-09]], [[concepts/verified-completion-vs-apparent-success]] and [[concepts/preservation-aware-agent-improvement]] where relevant. Preserve disagreements and task-level regressions rather than forcing a universal conclusion.

## Reproducible test plan

**Proposed, not executed:** Run 20 matched repo tasks with 1/2/4 workers and equal budgets; count accepted PRs, conflicts, loops and reviewer effort. Freeze source snapshots, models, budgets and checker definitions; record each run's full trace, failures, costs, independent acceptance and held-out results. Publish negative cases and per-task changes alongside any aggregate metrics.

## Adoption guidance and unanswered questions

Evaluate first in a constrained environment with explicit authorization, source traceability, validator execution records and rollback. Unknowns: independent replication, transfer beyond source tasks, total operating cost and effects on other consumers of the shared environment.

## Provenance and depth statement

**Full analytical synthesis of the archived briefing**, not a claim that new source experiments were performed or original benchmarks reproduced. Primary URLs and author-reported measurements remain in the earlier sections; proposed interpretations and experiments are editorial analysis.
