---
uid: fd965a5d-5f47-4f96-8519-03c90fc21fa1
title: "ToolPulse — Cueing and spotting tool-use detours"
summary: "Runtime feedback intervention versus verified task repair: State-based pre-dispatch cues, execution-feedback inspection, semantic traj."
type: project
created: 2026-11-17
updated: 2026-11-17
depth: full
sources:
  - https://arxiv.org/abs/2611.19275
---

# ToolPulse — Cueing and spotting tool-use detours

**Primary study:** [https://arxiv.org/abs/2611.19275](https://arxiv.org/abs/2611.19275), 2026-11-14. This is an author-reported research implementation; no independent replication is claimed.

## Mechanism and boundary

State-based pre-dispatch cues, execution-feedback inspection, semantic trajectory spotting and auxiliary-model advice. The reusable distinction is **runtime feedback intervention versus verified task repair**. [[techniques/adaptive-recovery]] and [[concepts/verified-completion-vs-apparent-success]] explain the neighboring mechanism and its limits; similarity of vocabulary does not imply identical architecture.

## Evidence and novelty

Across 1,350 SWE-agent trajectories on 90 Python, C++ and Java bug-fix tasks, authors report substantive responses after 61.6–90.9% of valid detour triggers, but aggregate repair outcomes remain close to baseline; some configurations save tokens.

A rare process-level intervention evaluation that explicitly separates changed behavior from actual bug repair. **Boundary:** Author-reported experiments; intervention trigger validity and symptom cessation do not establish independent patch correctness.

## Practical engineering test

Run 30 fixed failing repository tasks with no intervention, short state-based cues, and richer advice. Freeze model and tool budget; report valid triggers, avoided repeat calls, independently passing tests, tokens and false interventions.

**Engineering implication:** Instrument repetitive tool calls before dispatch and after tool results; do not reward an intervention unless the final test passes.
