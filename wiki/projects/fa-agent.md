---
uid: 4395c49d-be77-41d3-be9e-66441c1d9ccd
title: "FA-Agent: Multimodal Seismic First-Arrival Picking"
summary: "Visual agent uses processing tools and expert skills to keep, correct or abstain on ambiguous seismic first-arrival picks."
type: project
created: 2026-11-07
updated: 2026-11-07
depth: brief
related: [abstention-as-first-class-verdict, improvement-lives-in-external-state]
sources:
  - url: https://arxiv.org/abs/2611.06555
    retrieved: 2026-11-07
---

# FA-Agent: Multimodal Seismic First-Arrival Picking

**Source date:** 2026-11-04. **Primary source:** https://arxiv.org/abs/2611.06555.

## Mechanism and evidence

A multimodal model inspects a seismic gather, zooms into questionable regions, calls processing and quality-control tools, and decides whether to retain, correct or remove an initial first-arrival pick. Expert-reviewed cases are incorporated into reusable skills; a local model can keep survey data on site. The authors processed 1,000 randomly sampled field gathers and present three detailed examples, plus semi-synthetic tests with known arrivals. No independently reproduced quantitative improvement is established in the abstract. The key transferable idea is **evidence-aware removal of uncertain outputs** instead of confident hallucination. **Experiment:** apply the keep/correct/remove triage to noisy CAN frame classification, tracking precision, abstention and expert review burden.

## Evidence status and relations

This is a primary-source account, not an independently executed replication. Related concept pages are analytical cross-project connections, not author-endorsed taxonomies: [[concepts/abstention-as-first-class-verdict]], [[concepts/improvement-lives-in-external-state]].

## Provenance

- https://arxiv.org/abs/2611.06555
