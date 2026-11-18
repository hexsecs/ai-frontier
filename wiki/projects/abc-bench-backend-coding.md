---
uid: f0e73a16-91b4-4e8b-b6d1-0c7a8e290118
title: "ABC-Bench: Agentic Backend Coding in Real-World Development"
summary: "Deployment-complete acceptance versus patch-only scoring: 224 executable backend tasks across eight languages and 19 frameworks requi"
type: benchmark
created: 2026-11-18
updated: 2026-11-18
depth: full
sources:
  - https://aclanthology.org/2026.findings-acl.1142/
---

# ABC-Bench: Agentic Backend Coding in Real-World Development

**Primary source:** https://aclanthology.org/2026.findings-acl.1142/ (published 2026-07-01). Engineering finding; evidence is author-reported unless otherwise noted.

## Implementation and general mechanism

A published ACL Findings benchmark evaluates agentic coding as the complete service-development lifecycle rather than a patch-only unit test. Its authors report that contemporary systems struggle with end-to-end success.

The general concept is **deployment-complete acceptance versus patch-only scoring**. 224 executable backend tasks across eight languages and 19 frameworks require agents to explore repositories, configure services and pass external end-to-end API tests.

## Novelty and evidence boundary

Realistic service deployment and API-level acceptance broaden the measured outcome beyond repository edits; older peer-reviewed benchmark newly considered here. July publication, not a recent launch. Abstract supports task counts and evaluation design but not an independently verified success-rate figure; environment reliability may affect scores.

[[concepts/verified-completion-vs-apparent-success]] explains why a patch is weaker evidence than externally exercised API behavior.

## Practical implication and proposed test

For AI Frontier's repository automation, score deployed artifact behavior and externally executed tests, not only PR creation or local lint.

**Proposed, unexecuted:** Choose five containerized services with documented API smoke tests; run the same coding agent with patch-only versus deployment-complete acceptance, recording setup failures separately.
