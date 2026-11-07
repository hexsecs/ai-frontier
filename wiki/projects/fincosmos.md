---
uid: 8b867faa-1a65-4b5a-a927-41c40ccc9e78
title: "FINCOSMOS: An Open-World Evaluation Paradigm for Agents in Finance"
summary: "Open-world agent evaluation combines hidden user intent, live data acquisition, point-in-time replay and programmatic veto checks."
type: project
created: 2026-11-07
updated: 2026-11-07
depth: brief
related: [scoped-assurance, protocol-relative-scores, abstention-as-first-class-verdict]
sources:
  - url: https://arxiv.org/abs/2611.07464
    retrieved: 2026-11-07
---

# FINCOSMOS: An Open-World Evaluation Paradigm for Agents in Finance

**Source date:** 2026-11-05. **Primary source:** https://arxiv.org/abs/2611.07464.

## Mechanism and evidence

A simulated user holds a hidden compositional strategy; agents must elicit the specification, fetch their own web data, implement a cutoff-safe backtest, and submit an auditable report. Programmatic verification recomputes metrics and checks 15 veto conditions. In 150 sessions across four coding agents and a no-tools model, **zero** were accepted, even when the simulated user signed off. Agents elicited only 54–64% of unspecified details. Authors report expert attribution of 88.33% of failures to agents. With feedback and persistent memory, one agent learned ten tasks, but the exact training/evaluation separation must be inspected before interpreting this as general transfer. The strongest finding is a **user approval versus correctness gap**. **Experiment:** build hidden-intent, source-cutoff and recomputation vetoes for agent-generated security research reports.

## Evidence status and relations

This is a primary-source account, not an independently executed replication. Related concept pages are analytical cross-project connections, not author-endorsed taxonomies: [[concepts/scoped-assurance]], [[concepts/protocol-relative-scores]], [[concepts/abstention-as-first-class-verdict]].

## Provenance

- https://arxiv.org/abs/2611.07464
