---
uid: cd1550c6-6e3b-44a6-9300-ff5c8b79f84c
title: "ChemE-as-Code: An Open-Source Platform for Agentic AI in Chemical Engineering"
summary: "Git-versioned engineering artifacts, deterministic calculation tools and provenance checks support agent-driven plant design."
type: project
created: 2026-11-07
updated: 2026-11-07
depth: full
related: [structural-constraint-over-instruction, scoped-assurance]
sources:
  - url: https://arxiv.org/abs/2611.07947
    retrieved: 2026-11-07
---

# ChemE-as-Code: An Open-Source Platform for Agentic AI in Chemical Engineering

**Source date:** 2026-11-05. **Primary source:** https://arxiv.org/abs/2611.07947.

## Mechanism and evidence

One general-purpose agent selects skills and tools across process simulation, P&IDs, equipment sizing, layout, HAZOP and environmental analysis. Artifacts are machine-readable, linked and versioned in Git; calculations execute outside the LLM and report input provenance and stale dependent outputs. An illustrative ammonia engineering package cost **USD 224** in API calls for design sessions. Planted faults show both detections and blind spots. The paper explicitly states no independent engineer reviewed the design; this is a feasibility demonstration, not evidence of a safe or production-ready plant. **Experiment:** represent an embedded security assurance case as versioned, linked artifacts, automatically invalidating dependent claims when test evidence changes.

## Evidence status and relations

This is a primary-source account, not an independently executed replication. Related concept pages are analytical cross-project connections, not author-endorsed taxonomies: [[concepts/structural-constraint-over-instruction]], [[concepts/scoped-assurance]].

## Provenance

- https://arxiv.org/abs/2611.07947

## Full-depth synthesis: mechanism and system boundaries

**Core mechanism:** Git-versioned typed engineering artifacts, deterministic calculators and provenance-linked downstream checks. Distinguish the producing model, its tool/runtime privileges, the persistent artifacts, the evaluator and any human authorization. The original source-specific findings and reported metrics remain above; this section adds comparative analysis rather than implying a fresh independent reproduction.

## Evidence quality, negative results and alternatives

**Principal limitation:** Internally consistent calculations do not prove physical correctness, HAZOP completeness or independent engineering certification. A plausible alternative explanation is evaluator design, resource allocation or domain-specific task selection rather than a universally better agent architecture. Compare against a simpler baseline under equal budgets. Missing outcomes and failed checks are not successes.

## Typed knowledge relationships

**Analyst-level compares_with:** [[concepts/verified-completion-vs-apparent-success]], [[projects/tracybot]], [[projects/auto-research]]. These links are evidence-guided conceptual comparisons, **not** assertions that the projects cite, implement or depend on each other. This entry also contributes to [[evaluations/briefing-synthesis-2026-11-03-to-09]]; its acceptance and preservation implications should be evaluated against [[concepts/verified-completion-vs-apparent-success]] and [[concepts/preservation-aware-agent-improvement]].

## Reproducible evaluation plan

**Proposed; not executed:** Recompute 20 engineering dependencies after controlled upstream edits; measure stale artifacts, traceable changes and expert-review discrepancies. Freeze the task inputs, model/runtime, tool permissions and budget; record raw traces, checker invocation receipts, task-level outcomes, cost and failure cases. Pre-register acceptance criteria, include an untouched holdout set and make all candidate regressions visible rather than reporting only aggregate wins.

## Adoption decision and open questions

**Recommendation:** Controlled sandbox evaluation before production integration. Require a rollback path and independent verification of side effects. Unknowns include cross-model transfer, distribution shift, independent replication, operator time, and whether the observed mechanism adds value beyond simpler retrieval or orchestration.

## Depth and provenance

This is a **full analytical mining pass** grounded in the original dated briefing and primary-source links, not a claim of new direct source inspection or reproduced benchmarks. Source-reported measurements and newly proposed engineering interpretations are intentionally distinguished.
