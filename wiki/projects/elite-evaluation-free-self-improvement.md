---
uid: c11e853a-0104-4bd9-90ba-e9c4b61ef002
title: "ELITE — Evaluation-Free Recursive Self-Improvement"
summary: "Coding-agent self-improvement integrates complementary mechanisms without downstream candidate task scoring."
type: project
created: 2026-11-19
updated: 2026-11-19
depth: full
sources:
  - https://arxiv.org/abs/2611.21056
---

# ELITE — Evaluation-Free Recursive Self-Improvement

**Primary source:** [https://arxiv.org/abs/2611.21056](https://arxiv.org/abs/2611.21056) (submitted 2026-11-16). This is a research implementation described and evaluated by its authors; no independent reproduction is claimed.

## Reusable concept and mechanism

**General concept:** Mechanism integration without candidate outcome selection.

**Specific mechanism:** Explore-then-Integrate independently modifies a shared parent, inspects complementary, conflicting and redundant code changes, then reimplements compatible mechanisms in one descendant; deterministic validity checks replace downstream candidate task evaluation inside the loop.

[[concepts/preservation-aware-agent-improvement]] supplies regression gates; [[concepts/capability-locus]] distinguishes harness change from model-weight change.

## Evidence and novelty

Authors report SWE-bench Pro performance from 60.0% to 85.6%, versus 86.7% DGM and 88.3% HGM in their evaluated configurations, and evolution time 8.8× and 3.2× faster respectively. Transfer averages 73.3% on SWE-bench Verified and 69.3% on Polyglot.

The contribution is the specific mechanism and its evaluated boundary, not a general assertion that agents have become autonomous or reliable.

## Limits and counterexamples

Evaluation-free describes candidate selection inside evolution, not absence of final benchmark evaluation or proof of safety. Source abstract and primary paper identity were inspected; full HTML paper was unavailable in this run. Independent replication is not established.

## Proposed bounded experiment

Implement two small, isolated agent harness edits from the same baseline, reconcile compatible mechanisms and compare with evaluate-and-select under fixed compute. Score a held-out task set and count lost previously solved cases.
