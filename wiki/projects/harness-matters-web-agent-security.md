---
uid: a8945753-d4a2-459b-9b1a-3d9c62b07a05
title: "Harness Matters — Measuring and Dissecting Security Resilience in Web Agents"
summary: "WebTrap Farm evaluates how agent harness stages and models jointly determine browser-agent security."
type: project
created: 2026-11-12
updated: 2026-11-12
depth: brief
related: [coder-eval]
sources:
  - https://arxiv.org/abs/2611.11971
---

# Harness Matters — Measuring and Dissecting Security Resilience in Web Agents

**Source:** https://arxiv.org/abs/2611.11971  
**Date:** 2026-11-09  
**Evidence status:** Author-reported research; not independently replicated.

## Mechanism

WebTrap Farm is a systematic evaluation framework spanning malicious user instructions, prompt injection and deceptive web designs. It decomposes a web-agent harness into goal interpretation, perception, planning and execution, and pairs attacks with usability calibration tasks.

**Technique:** Stage-localized adversarial evaluation with matched benign controls, separating a model's inability to finish a task from a genuine security defense.

## Evidence and bounds

The authors report vulnerable behavior across evaluated harnesses, including some unsafe actions in the absence of overt malicious content. Both model and harness have statistically significant effects in their analysis; the abstract does not provide a defensible universal attack-rate figure.

## Novelty and comparison

It supplies a way to evaluate whether Baya-like structural changes really improve safety rather than merely making an agent unable to act. Unlike November 10's Strands Box, this measures harness susceptibility rather than enforcing policy.

## Reproducible experiment

Build 12 paired benign/adversarial browser tasks, vary only the harness while holding model, websites and budgets constant, and classify errors by perception, planning and execution stage.

## Verdict

High evaluation relevance; new November research, but no independently replicated measurements here.

## Related

- [[briefings/2026/11/2026-11-12]] — complete dated evidence and cross-project synthesis.
- [[projects/coder-eval]] — analyst comparison, not a demonstrated head-to-head; source URLs and limitations in the briefing.
