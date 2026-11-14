---
uid: 0f51e12c-1f8d-4e64-93a8-b0a2f9aed41d
title: "ExpertCrowd-SWE"
summary: "One hundred expert-authored engineering tasks use calibrated executable graders and must-pass merge blockers."
type: project
created: 2026-11-13
updated: 2026-11-13
depth: brief
related: [crossswe]
sources:
  - https://arxiv.org/abs/2611.13246
---

# ExpertCrowd-SWE

**Source:** https://arxiv.org/abs/2611.13246. **Publication:** 2026-11-09. **Evidence status:** author-reported, no independent replication.

## Mechanism
A benchmark of 100 expert-authored, multi-file tasks across 87 open-source projects and 11 languages, each with pinned code, sealed reference solutions and weighted executable graders including must-pass merge blockers.

**Technique:** Calibrated partial-credit grading with adversarial, inert and lazy control patches, instead of relying on final-text evaluation or one binary test.

## Evidence and limits
Seven frontier models, five attempts each, 3,495 scored runs. Reported scores: Claude Opus 5.5 67.3%, GPT-6 Astra 63.7%, with no statistically significant gap. Twenty-four tasks and graders are released; 76 remain held out.

Task selection is conditioned on difficulty for current frontier models; held-out grading limits full independent audit. Model rankings are protocol-specific.

## Comparison and relation
Stronger task and grader realism than shallow code benchmarks; compare with Coder Eval's harness-level checks and November 11's deliverable grading. Not a new agent runtime.

Related: [[projects/crossswe]]. The comparison is analytical, not a demonstrated integration.

## Proposed experiment
Replicate three public tasks with an independent coding harness; verify that no-op and superficially plausible patches score zero and must-pass blockers are enforced.

## Provenance
[[briefings/2026/11/2026-11-13]] — full dated narrative and source-scoped relation audit.
