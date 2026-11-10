---
uid: 82646864-0ef3-463a-b9b5-a036e650bf25
title: "Strategist: Evolving Reasoning with Agents"
summary: "Meta-agent evolves reusable executable inference strategies from task feedback and transfers them across tasks and models."
type: project
created: 2026-11-07
updated: 2026-11-07
depth: full
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

## Full-depth synthesis: mechanism and system boundaries

**Core mechanism:** A versioned library of executable inference blueprints selected and refined by a meta-agent. Distinguish the producing model, its tool/runtime privileges, the persistent artifacts, the evaluator and any human authorization. The original source-specific findings and reported metrics remain above; this section adds comparative analysis rather than implying a fresh independent reproduction.

## Evidence quality, negative results and alternatives

**Principal limitation:** Improvements on 24/30 benchmarks do not establish per-task preservation; development-set search can overfit, and reported cost savings depend on accounting. A plausible alternative explanation is evaluator design, resource allocation or domain-specific task selection rather than a universally better agent architecture. Compare against a simpler baseline under equal budgets. Missing outcomes and failed checks are not successes.

## Typed knowledge relationships

**Analyst-level compares_with:** [[concepts/preservation-aware-agent-improvement]], [[projects/evoaudit]], [[projects/envopt]]. These links are evidence-guided conceptual comparisons, **not** assertions that the projects cite, implement or depend on each other. This entry also contributes to [[evaluations/briefing-synthesis-2026-11-03-to-09]]; its acceptance and preservation implications should be evaluated against [[concepts/verified-completion-vs-apparent-success]] and [[concepts/preservation-aware-agent-improvement]].

## Reproducible evaluation plan

**Proposed; not executed:** Compare baseline and evolving strategy library on 30 fixed and 20 untouched transfer tasks. Measure exact per-task gains/losses, prompt+tool tokens, latency, and rollback. Freeze the task inputs, model/runtime, tool permissions and budget; record raw traces, checker invocation receipts, task-level outcomes, cost and failure cases. Pre-register acceptance criteria, include an untouched holdout set and make all candidate regressions visible rather than reporting only aggregate wins.

## Adoption decision and open questions

**Recommendation:** Controlled sandbox evaluation before production integration. Require a rollback path and independent verification of side effects. Unknowns include cross-model transfer, distribution shift, independent replication, operator time, and whether the observed mechanism adds value beyond simpler retrieval or orchestration.

## Depth and provenance

This is a **full analytical mining pass** grounded in the original dated briefing and primary-source links, not a claim of new direct source inspection or reproduced benchmarks. Source-reported measurements and newly proposed engineering interpretations are intentionally distinguished.
