---
uid: 814a6a12-e9ea-4b6a-b702-7561fe7c5e80
title: "Coder Eval — Declarative CI Tests for Coding Agents"
summary: "Runs coding agents on sandboxed YAML tasks with measurable postconditions, skill activation checks and CI gates."
type: project
created: 2026-11-12
updated: 2026-11-12
depth: brief
related: [harness-matters-web-agent-security]
sources:
  - https://github.com/UiPath/coder_eval
---

# Coder Eval — Declarative CI Tests for Coding Agents

**Source:** https://github.com/UiPath/coder_eval  
**Date:** 2026-11-12 (repository inspected; original release date unverified)  
**Evidence status:** Source repository inspected; release date and independent evaluation not verified.

## Mechanism

UiPath's open-source Coder Eval executes actual coding agents such as Codex, Claude Code, OpenCode and Pi in sandboxes using declarative YAML tasks. It scores generated files, command outcomes and weighted criteria, records tool/token telemetry and supports A/B configurations and GitHub Actions gates.

**Technique:** Harness-agnostic execution-grounded evaluation; independent task assertions, skill-trigger detection, and regression gating.

## Evidence and bounds

The repository includes implementation, example tasks, tests, a CLI and a CI action. No independent benchmark proving general agent quality improvements was established; its value is test infrastructure, not a published leaderboard.

## Novelty and comparison

Directly applicable to validating AI Frontier PR-writing agents and agent skills. Compared with ToolSpace's synthetic execution-witnessed environments, this runs user-defined domain tasks against actual coding harnesses.

## Reproducible experiment

Define 12 tasks covering Markdown frontmatter, broken internal links, source provenance, CI repairs and branch cleanup. Run two agents on identical fixtures, require file-state assertions, and publish pass rates and tool cost per verified task.

## Verdict

Immediately actionable implementation; newer repository activity is not evidence of a new launch.

## Related

- [[briefings/2026/11/2026-11-12]] — complete dated evidence and cross-project synthesis.
- [[projects/harness-matters-web-agent-security]] — analyst comparison, not a demonstrated head-to-head; source URLs and limitations in the briefing.
