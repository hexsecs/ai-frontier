---
uid: 6926662f-0fd0-4f98-8803-c0265fcbdb7c
title: "Values Shape What Self-Improving Coding Agents Build"
summary: "Persistent value statements alter evolved coding solutions, but self-revision can erase intended differences."
type: project
created: 2026-11-19
updated: 2026-11-19
depth: full
sources:
  - https://arxiv.org/abs/2611.23067
---

# Values Shape What Self-Improving Coding Agents Build

**Primary source:** [https://arxiv.org/abs/2611.23067](https://arxiv.org/abs/2611.23067) (submitted 2026-11-17). This is a research implementation described and evaluated by its authors; no independent reproduction is claimed.

## Reusable concept and mechanism

**General concept:** Governance instructions as optimization inputs.

**Specific mechanism:** Place short Schwartz higher-order value statements in persistent agent instructions, hold them fixed during self-improvement iterations, compare held-out scores and solution structure, then test allowing agents to rewrite the values.

[[concepts/capability-locus]] locates persistent instruction effects; [[concepts/preservation-aware-agent-improvement]] requires per-task regression tracking.

## Evidence and novelty

The authors report that openness-to-change instructions improve held-out performance while conservation instructions can underperform no-values controls; solution size and approaches change. Letting agents revise their own values narrows differences, and literature-distilled values show no detectable gain.

The contribution is the specific mechanism and its evaluated boundary, not a general assertion that agents have become autonomous or reliable.

## Limits and counterexamples

The observed effect is task- and prompt-dependent, not a universal ranking of values or proof of normative alignment. The study concerns a controlled self-improving coding setup.

## Proposed bounded experiment

Run 12 deterministic coding tasks under fixed instruction variants and an unchanged baseline. Freeze prompts in one arm, allow revision in another, and measure independent correctness, code complexity, safety constraints and value drift.
