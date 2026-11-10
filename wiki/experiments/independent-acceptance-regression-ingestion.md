---
uid: 8c0f6e39-1d5a-4d7b-88f5-000000000041
title: "Independent acceptance and regression preservation for autonomous KB ingestion"
summary: "A reproducible proposed test of agent ingestion correctness, evidence provenance, preserved task coverage and cost."
type: experiment
created: 2026-11-09
updated: 2026-11-09
depth: full
sources:
  - https://arxiv.org/abs/2611.07464
  - https://arxiv.org/abs/2611.07624
  - https://arxiv.org/abs/2611.07372
  - https://arxiv.org/abs/2610.08651
---

# Independent acceptance and regression preservation for autonomous KB ingestion

**Status: proposed; not executed.** Derived from [[concepts/verified-completion-vs-apparent-success]], [[concepts/preservation-aware-agent-improvement]] and [[evaluations/briefing-synthesis-2026-11-03-to-09]]. Sources motivate the design; they do not report this experiment's results.

## Hypothesis

An ingestion agent that uses hidden acceptance tests, explicit source-provenance checks and a task-level regression gate will produce fewer falsely accepted canonical edits than one evaluated by self-reported completion or headline page count.

## Protocol

1. Assemble **30** ingestion tasks with verifiable ground truth: source dates, benchmark conditions, canonical aliases, correct directional relations, and counterexamples. Freeze **20** additional transfer cases before any optimization.
2. Seed hidden failure modes: source citation pointing to the wrong claim, two records for one DOI, absent validator execution, stale aliases, a regression in an existing concept, and a tool write acknowledged but not persisted.
3. Compare three arms with the same model, source access and token budget: baseline ingestion; baseline plus independent acceptance; and independent acceptance plus a regression-preserving strategy/environment gate.
4. For each case, preserve the source excerpt or source span, agent action log, candidate diff, checker execution receipt, independent verdict and rollback state.
5. Evaluate blind on the held-out 20 cases. Report any critical provenance violation separately from average quality.

## Metrics and acceptance criteria

Primary: fraction of tasks passing **all** hidden acceptance checks, false-acceptance rate, and previously correct relations lost. Secondary: relation precision/recall, abstention accuracy, citation completeness, missing-check detection, tokens, wall time and duplicate writes. Reject promotion when a critical source-integrity check is absent or a previously correct critical relation is lost, regardless of mean score.

## Confounders and limitations

Hidden-check quality itself needs audit; benchmark tasks may not represent real research; checker-model overlap can create evaluator circularity. Blind reviewers to treatment arm, report checker false positives, and avoid claiming production benefit from a small synthetic evaluation.

## Evidence status

This is a design specification, **not a result**. No acceptance rates, savings or improvements are asserted.
