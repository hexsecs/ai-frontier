---
uid: a29b51f0-ec09-4b70-9e90-900000000002
title: "Tracybot"
summary: "Links coding-agent changes to developer prompts and exports task-level design decisions."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: full
sources:
  - https://arxiv.org/abs/2611.09395
  - https://github.com/TracyTeam/tracybot
---

# Tracybot

**Source:** https://arxiv.org/abs/2611.09395

**Code:** https://github.com/TracyTeam/tracybot  
**Date:** 2026-11-06  
**Evidence tier:** Author-reported research; not independently reproduced.

## Mechanism

Open-source VS Code/Git integration that records planning and build prompts as Tasklets, maps agent-generated code changes to Tasklets at line level, and exports significant decisions as architecture records.

**Key technique:** Line-level code-to-intent provenance with tasklet identity surviving the conversation-to-commit boundary.

## Evidence and limitations

Two design-science iterations; a seven-person focus group and 24-person survey found the approach perceived as useful and understandable. This is usability evidence, not a measured reduction in defects.

Small subjective usability study, not a controlled test of code correctness, audit coverage, or production reliability.

## Novelty and comparison

Compared with the earlier Claude ACP provenance and GitHub review traces, Tracybot attaches intent to specific changed lines, making future reviewers less dependent on a lost chat transcript.

## Reproducible next step

Prototype an equivalent source-to-claim provenance ledger: each OpenShelf concept assertion points to the source excerpt, mining run, reviewer decision and commit.

## Assessment

The dated [[briefings/2026/11/2026-11-09]] report contains the complete comparison and research audit. Treat source-specific findings as evidence, not independently reproduced outcomes.

## Relations

- **Evidence-backed mechanism:** Line-level code-to-intent provenance with tasklet identity surviving the conversation-to-commit boundary. Source: https://arxiv.org/abs/2611.09395.
- **Analyst-level relation:** Compared with the earlier Claude ACP provenance and GitHub review traces, Tracybot attaches intent to specific changed lines, making future reviewers less dependent on a lost chat transcript.

## Full-depth synthesis: mechanism and boundaries

**Core mechanism:** Tasklets linking prompts and architectural decisions to changed source lines and Git commits. Separate model inference, persistent state, tool privileges, side effects and independent acceptance evidence. The dated source findings above are retained without silently upgrading their evidence tier.

## Evidence quality and counterarguments

**Principal limitation:** Small usability studies measure perceived utility, not correctness or complete provenance coverage. Potential confounders include task selection, evaluator design, resource budgets and deployment context. Compare to a simpler baseline; distinguish benchmark, user judgement, tool acknowledgement and independently checked task completion. Missing checks are unknown, never passes.

## Directional knowledge relationships

**Analyst-level compares_with:** [[projects/procgrep]], [[projects/cheme-as-code]]. These are cross-study comparisons, not verified dependency or implementation links. The item contributes to [[evaluations/briefing-synthesis-2026-11-03-to-09]], [[concepts/verified-completion-vs-apparent-success]] and [[concepts/preservation-aware-agent-improvement]] where relevant. Preserve disagreements and task-level regressions rather than forcing a universal conclusion.

## Reproducible test plan

**Proposed, not executed:** Audit 50 generated lines for prompt, task, decision, commit and check links; inject missing trace segments. Freeze source snapshots, models, budgets and checker definitions; record each run's full trace, failures, costs, independent acceptance and held-out results. Publish negative cases and per-task changes alongside any aggregate metrics.

## Adoption guidance and unanswered questions

Evaluate first in a constrained environment with explicit authorization, source traceability, validator execution records and rollback. Unknowns: independent replication, transfer beyond source tasks, total operating cost and effects on other consumers of the shared environment.

## Provenance and depth statement

**Full analytical synthesis of the archived briefing**, not a claim that new source experiments were performed or original benchmarks reproduced. Primary URLs and author-reported measurements remain in the earlier sections; proposed interpretations and experiments are editorial analysis.
