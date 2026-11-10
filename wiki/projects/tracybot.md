---
uid: a29b51f0-ec09-4b70-9e90-900000000002
title: "Tracybot"
summary: "Links coding-agent changes to developer prompts and exports task-level design decisions."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: brief
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
