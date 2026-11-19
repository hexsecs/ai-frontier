---
uid: ae85eced-fcdd-4aa6-a34b-81c4d0015a73
title: "When Agent Skills Go Stale"
summary: "Environment changes invalidate stored agent skills; selective execution-grounded maintenance can recover value."
type: project
created: 2026-11-19
updated: 2026-11-19
depth: full
sources:
  - https://arxiv.org/abs/2611.22525
---

# When Agent Skills Go Stale

**Primary source:** [https://arxiv.org/abs/2611.22525](https://arxiv.org/abs/2611.22525) (submitted 2026-11-17). This is a research implementation described and evaluated by its authors; no independent reproduction is claimed.

## Reusable concept and mechanism

**General concept:** Staleness and applicability of external skill state.

**Specific mechanism:** Replay checks recorded from successful executions without model calls; compare current observations against saved skill assumptions, verify conflicts, repair affected material, validate, or rebuild.

[[techniques/agent-skills-and-memory]] and [[techniques/deterministic-workflow-reuse]] explain why saved operational choices need revalidation.

## Evidence and novelty

Across four task settings and two models, previously helpful skills sometimes reduce performance by over 10 percentage points or increase steps by nearly 40%. Maintenance improves accuracy by up to 67 points and reduces steps by up to 37% in selected settings. These are author-reported, setting-dependent effects; amortization is estimated at roughly 21–42 subsequent tax-form uses.

The contribution is the specific mechanism and its evaluated boundary, not a general assertion that agents have become autonomous or reliable.

## Limits and counterexamples

The source studies controlled environment transitions, not arbitrary production drift. A changed check can signal a benign change; unchanged checks need not establish semantic equivalence.

## Proposed bounded experiment

Pin ten task fixtures; mutate endpoint names, field identifiers and package versions. Compare no skill, stale skill, procedural skill and selective replay-maintained skill. Record independent task correctness, tool steps, maintenance cost, false alarms and regressions.
