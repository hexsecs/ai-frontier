---
uid: 0c17c078-693d-4eca-99fe-235e08f47719
title: "Verified completion versus apparent success"
summary: "Agent completion claims, user approval, tool acknowledgements and passing checks do not establish independently verified outcomes."
type: concept
created: 2026-11-09
updated: 2026-11-09
depth: full
sources:
  - https://arxiv.org/abs/2611.07464
  - https://arxiv.org/abs/2611.07947
  - https://arxiv.org/abs/2611.08321
  - https://arxiv.org/abs/2610.08651
  - https://arxiv.org/abs/2610.13361
---

# Verified completion versus apparent success

## Claim and boundary

A task's apparent success is not equivalent to independent acceptance. This is an **analyst synthesis** across November 3–9 reports, not a claim that these projects share implementations. Distinguish five different observable outcomes: (1) agent declaration; (2) user approval; (3) tool acknowledgement; (4) executed validator result; and (5) independent, task-complete acceptance. A result at a lower tier cannot be silently promoted to a higher one.

## Supporting and limiting evidence

- **FINCOSMOS** ([[projects/fincosmos]], [paper](https://arxiv.org/abs/2611.07464)) reports **zero of 150** sessions satisfying its independent acceptance criteria, including user-approved sessions. Its hidden-intent, data-cutoff and metric-recomputation tests provide unusually concrete evidence of the gap. These are author-run benchmark results, not production failure rates.
- **ControlAnything** ([[projects/controlanything]], [paper](https://arxiv.org/abs/2611.08321)) reports 9/10 ready requests, but readiness establishes connector and transport acknowledgements, **not physical effects**. Acknowledgement is not actuation evidence.
- **ChemE-as-Code** ([[projects/cheme-as-code]], [paper](https://arxiv.org/abs/2611.07947)) versions engineering artifacts and checks dependency consistency; the illustrative ammonia design was **not independently engineer-reviewed**. Internal consistency is narrower than domain certification.
- **Production assurance case** ([[projects/assuring-ai-written-software]], [paper](https://arxiv.org/abs/2610.08651)) reports silently missing or proxy-based checks and an automated repair that disrupted operations. The check-execution record itself must be independently observable. Single-case qualitative evidence.
- **AgentSWE** ([November 3 briefing](../briefings/2026/11/2026-11-03.md), [paper](https://arxiv.org/abs/2610.13361)) tests agents that construct other agents. Acceptance must cover the built agent's actual behavior rather than its self-description.

## Competing explanations and counterweights

A failed strict benchmark may reflect demanding or brittle acceptance criteria rather than an inherently useless agent. Conversely, user approval can be legitimate for subjective tasks. The synthesis concerns **claims of objective task completion**, where acceptance conditions can be operationalized; it does not imply every task needs an external oracle.

## Typed, evidence-scoped relations

- FINCOSMOS **evaluates** hidden-intent acceptance; ControlAnything **illustrates** a narrower transport-acknowledgement tier; ChemE-as-Code **implements** internal provenance checks. These are source-backed roles, not direct citations between projects.
- The production case **contradicts** the assumption that the presence of automated review implies that the review actually ran.
- **Extends** [[concepts/scoped-assurance]] and [[concepts/validation-tier-gap]] with an explicit acceptance-evidence ladder.

## Reproducible experiment

Create 30 repository-ingestion tasks with hidden acceptance rules and planted failures: missing source dates, fabricated metrics, skipped validators, unresolved canonical aliases and tools that acknowledge a write without persisting it. Compare agent self-verdict, user-style review, and independent checker verdict. Report full-acceptance rate, false acceptances, abstentions and checker execution coverage, not merely PR counts.

## Evidence status

Cross-paper inference assembled from the cited primary reports and existing canonical records; no experiment run for this synthesis. Published numbers remain author-reported.
