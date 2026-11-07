---
uid: 82646864-0ef3-463a-b9b5-a036e650bf25
title: "Strategist: Evolving Reasoning with Agents"
summary: "Meta-agent evolves reusable executable inference strategies from task feedback and transfers them across tasks and models."
type: project
created: 2026-11-07
updated: 2026-11-07
depth: brief
related: [improvement-lives-in-external-state, capability-locus]
sources:
  - url: https://arxiv.org/abs/2611.03618
    retrieved: 2026-11-07
---

# Strategist: Evolving Reasoning with Agents

**Source date:** 2026-11-02. **Primary source:** https://arxiv.org/abs/2611.03618.

## Mechanism and evidence

A meta-agent retrieves reusable executable blueprints, synthesizes new inference strategies, tests candidates on a small development set, revises them, and retains them in a library. On 30 benchmarks the authors report beating the strongest baseline on 24, with mean accuracy 74.7% versus 74.0% at 39% lower inference cost. These are author-reported evaluations, not independent replication. The distinct mechanism relative to SkillCompiler is **strategy-level reuse across tasks and models**, rather than selectively compiling operations within a skill. The blueprint library, not model weights, carries adaptation. **Experiment:** compare learned strategies against fixed prompting on held-out OpenShelf extraction tasks; track quality, cost, transfer and leakage.

## Evidence status and relations

This is a primary-source account, not an independently executed replication. Related concept pages are analytical cross-project connections, not author-endorsed taxonomies: [[concepts/improvement-lives-in-external-state]], [[concepts/capability-locus]].

## Provenance

- https://arxiv.org/abs/2611.03618
