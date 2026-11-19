---
uid: 8f9e8b6c-8d64-4214-a793-c00b9b74b1f4
title: "ForceHarness — Physical Feedback for Frozen Models"
summary: "Self-terminating force primitives and physics summaries enable frozen multimodal models to control contact tasks."
type: project
created: 2026-11-19
updated: 2026-11-19
depth: full
sources:
  - https://arxiv.org/abs/2611.21099
---

# ForceHarness — Physical Feedback for Frozen Models

**Primary source:** [https://arxiv.org/abs/2611.21099](https://arxiv.org/abs/2611.21099) (submitted 2026-11-16). This is a research implementation described and evaluated by its authors; no independent reproduction is claimed.

## Reusable concept and mechanism

**General concept:** Fast local control beneath slow model decisions.

**Specific mechanism:** Calibrate contact force from wrist sensors or joint torques; execute self-terminating closed-loop force primitives; translate force traces into physical quantities with uncertainty before returning them to an API-only multimodal model.

[[techniques/embodied-and-scientific-agents]] compares measured physical control against simulated policy evolution and other instrument feedback loops.

## Evidence and novelty

Authors report GPT-6 Astra zero-shot physical-arm task success improving from 3.3% to 90.0% without a wrist force sensor, and simulation gains of 17.5 points on ForceBench and 34.3 on HiddenPhys.

The contribution is the specific mechanism and its evaluated boundary, not a general assertion that agents have become autonomous or reliable.

## Limits and counterexamples

These are author-reported task-specific outcomes, not evidence of general robot safety. The controller layer, calibration and task conditions contribute to the result; no independent replication was established.

## Proposed bounded experiment

In a deterministic contact simulator, compare raw force telemetry, physics-summary observations and autonomous local force primitives across 12 held-out parameter seeds. Track success, force-limit violations and intervention latency.
