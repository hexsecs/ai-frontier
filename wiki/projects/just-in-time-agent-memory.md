---
uid: 00000000-0000-4000-8000-31653de0a8a1
title: "Just-In-Time Agent Memory with Runtime Agentic Research (JAM)"
summary: "Query-conditioned multi-step evidence retrieval over preserved raw history, rather than pre-compressing everything into fixed summaries."
type: project
created: 2026-11-11
updated: 2026-11-11
depth: brief
sources:
  - https://arxiv.org/abs/2609.34385
---

# Just-In-Time Agent Memory with Runtime Agentic Research (JAM)

**Original source:** https://arxiv.org/abs/2609.34385  
**Date:** 2026-09-28  
**Evidence status:** Author-reported research; not independently replicated in this knowledge base.

## Mechanism

A two-part memory system: a Memorizer stores complete history in hierarchical pages, and a trained Researcher investigates original records at query time. Memory-Gym synthesizes grounded tasks across nine types and six domains; source code is released.

Query-conditioned multi-step evidence retrieval over preserved raw history, rather than pre-compressing everything into fixed summaries.

## Significance and comparison

Provides an actionable architecture for long-lived agents whose historical evidence is too valuable to discard.

Extends the evidence-provenance theme from Tracybot and OpenShelf by reconstructing the relevant past at the moment of need.

## Practical experiment

Index 100 archived agent runs with compact summaries plus raw logs; compare JAM-style iterative navigation against single-shot retrieval on 30 provenance questions.

## Limits

Reported quality/cost gains are author-reported; September publication is deliberately labeled older, selected for architectural relevance.

## Related

- [[briefings/2026/11/2026-11-11]]
