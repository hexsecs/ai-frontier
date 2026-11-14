---
uid: 67f38b07-421d-429e-9069-56b4ba1b7acb
title: "WorkflowArena: Executable Multi-Agent Orchestration"
summary: "A 145-task benchmark evaluates model-authored worker delegation, workflow organization and integrated deliverable verification."
type: project
created: 2026-11-13
updated: 2026-11-13
depth: brief
related: [expertcrowd-swe, crossswe, verified-completion-vs-apparent-success]
sources:
  - https://arxiv.org/abs/2611.12856
---

# WorkflowArena: Executable Multi-Agent Orchestration

**Primary source:** https://arxiv.org/abs/2611.12856 (November 9, 2026). **Evidence:** author-reported benchmark; independent replication not verified.

## Mechanism and artifact

WorkflowArena measures whether an agent can author the executable workflow coordinating its own worker agents. The benchmark comprises 145 long-horizon tasks across eight professional domains. Each task begins from a workspace and demands an integrated, interdependent deliverable evaluated by a hidden verifier. Delegation is recorded, allowing analysis of both final output and worker organization.

## Evidence and boundaries

Nine models were evaluated. No single delegation configuration dominates all domains. At high effort, Claude Code configurations tend to delegate less frequently with larger worker groups, while Codex configurations delegate more often to smaller groups. With executor model held fixed on a challenging subset, workflows authored by Claude Opus 5.5 substantially improve weaker executors. These are author-reported observations, not a proven production advantage. The abstract does not supply a universal improvement percentage.

## Comparison and test

Compared with [[projects/crossswe]], which checks cross-repository change consistency, WorkflowArena isolates model-authored coordination and integrated artifact grading. Compared with [[projects/expertcrowd-swe]], its grading emphasizes orchestrated multi-component deliverables rather than maintainer-authored merge blockers. These are analytical comparisons, not head-to-head experiments.

**Reproducible experiment:** Hold model, tasks and budget constant for five interdependent repository-and-document tasks. Compare a single agent, a fixed two-worker workflow and a model-authored delegation structure. Record verified completion, integration errors, worker count, cost, retries and critical-path duration.

**Verdict:** Novel orchestration benchmark with inspectable evaluation framing; real-world transfer and independent replication remain open.
