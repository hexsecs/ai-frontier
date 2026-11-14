---
uid: 00000000-0000-4000-8000-9e0483b32faa
title: "Modern Software Engineering with Verification Agents"
summary: "Treat formal specifications as human-reviewed source of truth and generated code/proofs as regenerable outputs, gated by mechanical checks."
type: project
created: 2026-11-11
updated: 2026-11-11
depth: brief
sources:
  - https://arxiv.org/abs/2611.02285
---

# Modern Software Engineering with Verification Agents

**Original source:** https://arxiv.org/abs/2611.02285  
**Date:** 2026-11-01  
**Evidence status:** Author-reported research; not independently replicated in this knowledge base.

## Mechanism

A proposed spec-first software engineering architecture with verification IR, agent-authored implementations and proofs, semantic merge-conflict detection, and a zero-copy authenticated-router illustration.

Treat formal specifications as human-reviewed source of truth and generated code/proofs as regenerable outputs, gated by mechanical checks.

## Significance and comparison

A radical change in the human review surface for agent-produced software, especially safety-critical embedded components.

Unlike yesterday's process-execution evidence, this targets correctness of the resulting implementation relative to a specification.

## Practical experiment

Prototype a small authenticated message parser: write explicit input/output invariants, generate code and tests, and measure human review time and proof coverage against a conventional PR.

## Limits

Primarily an architectural proposal; its >90% review-attention reduction is explicitly an estimate, not an observed result. Do not adopt zero-human-code-review as a proven practice.

## Related

- [[briefings/2026/11/2026-11-11]]
