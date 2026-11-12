---
uid: 0eb71986-637c-49d3-b7aa-bffe70fd013a
title: "fastbrowse — Bounded Browser Agent with Quote-Level Evidence"
summary: "A browser agent that chooses actual page controls, cites source quotes and gates irreversible actions in code."
type: project
created: 2026-11-12
updated: 2026-11-12
depth: brief
related: [baya-compile-then-execute]
sources:
  - https://github.com/agent-labs-dev/fastbrowse
---

# fastbrowse — Bounded Browser Agent with Quote-Level Evidence

**Source:** https://github.com/agent-labs-dev/fastbrowse  
**Date:** 2026-11-12 (repository inspected; release date unverified)  
**Evidence status:** Source repository inspected; release date and independent evaluation not verified.

## Mechanism

A Rust/Python browser agent indexes controls that actually exist on each page, uses a choice model to select actions, and has an LLM compose answers grounded in quoted page evidence. Code gates submit, payment, deletion and sending; secrets are restricted to declared origins.

**Technique:** Constrained action selection, quote-linked provenance, origin-bound credentials, code-owned authorization and resource budgets.

## Evidence and bounds

Its maintainers report 99.2% successful runs versus 96.3% for a hosted Browser Use agent across 46 tasks run three times each, with reported per-run costs $0.0296 versus $0.3180. This is a developer-run comparison, not an independent result; its documented campaign did not measure runtime.

## Novelty and comparison

Combines answer provenance and action boundaries in a working browser harness. Baya precompiles all operations; fastbrowse instead bounds the runtime action space to controls present on the page and protects sensitive side effects.

## Reproducible experiment

Use ten controlled pages containing benign controls, misleading buttons, prompt injections and source citations. Compare quoted-evidence correctness and unauthorized-action attempts, without real credentials or payments.

## Verdict

Interesting engineering tradeoff and code artifact; claims about cost and reliability require reproduction.

## Related

- [[briefings/2026/11/2026-11-12]] — complete dated evidence and cross-project synthesis.
- [[projects/baya-compile-then-execute]] — analyst comparison, not a demonstrated head-to-head; source URLs and limitations in the briefing.
