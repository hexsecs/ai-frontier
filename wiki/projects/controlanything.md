---
uid: 227e9ec2-28c7-44b5-8fd5-b7024e33fa15
title: "ControlAnything: On-Demand Device Integration by a Coding Agent"
summary: "Mixed-reality agent generates and tests device connectors and hand-control interfaces for MIDI, Bluetooth and keyboard targets."
type: project
created: 2026-11-07
updated: 2026-11-07
depth: brief
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
