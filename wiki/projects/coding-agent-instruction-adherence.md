---
uid: 73f18c20-423b-4b9f-8c20-000000000004
title: "Coding-agent instruction adherence"
summary: "Empirical measurement of context-file compliance."
type: project
created: 2026-11-25
updated: 2026-11-26
depth: brief
sources:
  - https://arxiv.org/abs/2611.13709v1
---

# Coding-agent instruction adherence

November 10, 2026 preprint. [Primary source](https://arxiv.org/abs/2611.13709v1).

## Mechanism and evidence

Researchers derive executable measurements from actionable context-file instructions and assess associated agent commits. Compliance varies substantially by instruction category and agent.

## Limits

Observable postconditions cover only a subset of possible instructions; a measurement script can itself be wrong. Section 4.2 and Table 6 report accepted measurement scripts for 4,123 of 6,552 observable instructions. Results are author-reported; no independent replication is cited.

## Proposed experiment

Test generated validators against known-good and deliberately invalid fixtures. See [[concepts/verified-completion-vs-apparent-success]] for the distinction between observed checks and task acceptance.
