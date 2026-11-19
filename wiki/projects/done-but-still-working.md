---
uid: 445880ab-0edb-4f9b-80ff-896800dce5c7
title: "Done, But Still Working — Coding Agent Stop Policies"
summary: "Intermediate-patch replay quantifies cost savings and quality risks when coding agents stop after self-tests."
type: project
created: 2026-11-19
updated: 2026-11-19
depth: full
sources:
  - https://arxiv.org/abs/2611.22901
---

# Done, But Still Working — Coding Agent Stop Policies

**Primary source:** [https://arxiv.org/abs/2611.22901](https://arxiv.org/abs/2611.22901) (submitted 2026-11-17). This is a research implementation described and evaluated by its authors; no independent reproduction is claimed.

## Reusable concept and mechanism

**General concept:** Anytime acceptance and stopping under uncertain quality.

**Specific mechanism:** Replay intermediate coding-agent patches, score each against hidden tests, and evaluate counterfactual stop-or-select policies without regenerating trajectories when state replay is faithful.

[[concepts/verified-completion-vs-apparent-success]] distinguishes local success signals from accepted outcomes; [[techniques/evaluation-and-simulation]] addresses scoring protocols.

## Evidence and novelty

About 6,000 runs from eight open models in two scaffolds show under 1% to 57% potential hindsight savings depending on configuration. A repeated passing-patch rule saves 23% in preregistered replication, but its quality non-inferiority was not established; policy imitation saves 30% across six seeds with quality uncertainty.

The contribution is the specific mechanism and its evaluated boundary, not a general assertion that agents have become autonomous or reliable.

## Limits and counterexamples

A passing self-test is not independent hidden-test success. Retrospective replay applies to policies that stop or choose earlier states, not interventions that would alter future behavior.

## Proposed bounded experiment

Run 20 pinned coding tasks with hidden tests; compare original completion, first green self-test and twice-green identical patch. Measure tokens, wall time, hidden-test regressions and unrepaired failures.
