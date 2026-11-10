---
uid: 227e9ec2-28c7-44b5-8fd5-b7024e33fa15
title: "ControlAnything: On-Demand Device Integration by a Coding Agent"
summary: "Mixed-reality agent generates and tests device connectors and hand-control interfaces for MIDI, Bluetooth and keyboard targets."
type: project
created: 2026-11-07
updated: 2026-11-07
depth: full
related: [structural-constraint-over-instruction, scoped-assurance]
sources:
  - url: https://arxiv.org/abs/2611.08321
    retrieved: 2026-11-07
---

# ControlAnything: On-Demand Device Integration by a Coding Agent

**Source date:** 2026-11-05. **Primary source:** https://arxiv.org/abs/2611.08321.

## Mechanism and evidence

A Quest 3 wearer selects a real object and requests an interaction; a coding agent writes a Node connector on a laptop, tests transport acknowledgements through existing MIDI, Bluetooth or keypress adapters, and generates AR controls or a per-frame hand program. Code and video are linked at https://github.com/Apolotary/controlanything. In a **single author-only session**, nine of ten requests reached a ready state, median **32.5 seconds** excluding speech transcription; sequential model calls consumed median 89.9% of readiness time. Acknowledgements establish transport delivery, **not physical effects**. One demonstrated target is an OP-1 Field synthesizer. **Experiment:** generate bounded MIDI mappings for a controller with a human stop path; verify the actual synth parameter change independently of transport acknowledgement.

## Evidence status and relations

This is a primary-source account, not an independently executed replication. Related concept pages are analytical cross-project connections, not author-endorsed taxonomies: [[concepts/structural-constraint-over-instruction]], [[concepts/scoped-assurance]].

## Provenance

- https://arxiv.org/abs/2611.08321

## Full-depth synthesis: mechanism and system boundaries

**Core mechanism:** On-demand Node device connector generation plus mixed-reality controls and transport acknowledgement tests. Distinguish the producing model, its tool/runtime privileges, the persistent artifacts, the evaluator and any human authorization. The original source-specific findings and reported metrics remain above; this section adds comparative analysis rather than implying a fresh independent reproduction.

## Evidence quality, negative results and alternatives

**Principal limitation:** Nine of ten ready requests establish connector readiness, not physical actuation, safety, persistence or permission isolation. A plausible alternative explanation is evaluator design, resource allocation or domain-specific task selection rather than a universally better agent architecture. Compare against a simpler baseline under equal budgets. Missing outcomes and failed checks are not successes.

## Typed knowledge relationships

**Analyst-level compares_with:** [[concepts/verified-completion-vs-apparent-success]], [[projects/cua-agentenv]], [[domains/computer-and-device-use]]. These links are evidence-guided conceptual comparisons, **not** assertions that the projects cite, implement or depend on each other. This entry also contributes to [[evaluations/briefing-synthesis-2026-11-03-to-09]]; its acceptance and preservation implications should be evaluated against [[concepts/verified-completion-vs-apparent-success]] and [[concepts/preservation-aware-agent-improvement]].

## Reproducible evaluation plan

**Proposed; not executed:** Test 20 MIDI/Bluetooth/keyboard adapters in a sandbox; instrument actual device state separately from transport acknowledgement and test failed/replayed commands. Freeze the task inputs, model/runtime, tool permissions and budget; record raw traces, checker invocation receipts, task-level outcomes, cost and failure cases. Pre-register acceptance criteria, include an untouched holdout set and make all candidate regressions visible rather than reporting only aggregate wins.

## Adoption decision and open questions

**Recommendation:** Controlled sandbox evaluation before production integration. Require a rollback path and independent verification of side effects. Unknowns include cross-model transfer, distribution shift, independent replication, operator time, and whether the observed mechanism adds value beyond simpler retrieval or orchestration.

## Depth and provenance

This is a **full analytical mining pass** grounded in the original dated briefing and primary-source links, not a claim of new direct source inspection or reproduced benchmarks. Source-reported measurements and newly proposed engineering interpretations are intentionally distinguished.
