---
uid: 27cbd7a6-2314-4bf6-8d4f-53fd672db706
title: "Multi-agent value and coordination"
summary: "Compare delegation by accepted output, information exchange and total resource cost under matched evaluation conditions."
type: evaluation
created: 2026-11-14
updated: 2026-11-14
depth: full
sources:
  - https://arxiv.org/html/2610.04672v2
  - https://arxiv.org/html/2610.07763v1
  - https://raw.githubusercontent.com/microsoft/Agensh/2dae4e14a653da48549fd9aa093f834841475d6c/README.md
---

# Multi-agent value and coordination

## The question

Delegation is useful when the integrated accepted output justifies its resource and coordination costs. More workers, better information exchange, broader task coverage and better conditional answer quality are different explanations. A useful comparison identifies which explanation the experiment can isolate.

## Evidence map

| Evidence | Question isolated | Boundary |
|---|---|---|
| [[projects/masbench]] | How protocol, memory and routing close deliberately distributed information gaps. | Partial-observability tasks and communication rules define what can be inferred. |
| [[projects/st-bench]] | Whether generated teams improve scientific task outcomes relative to a single-agent baseline, and at what cost. | Coverage and quality conditional on producing realistic output must be separated. |
| [[projects/agensh]] | How self-organized workers coordinate through shared workspace, messages and context. | A larger team can receive more aggregate compute even when wall-clock duration is fixed. |

Sources: [MASBench](https://arxiv.org/html/2610.04672v2), [ST-Bench](https://arxiv.org/html/2610.07763v1), [Agensh README](https://raw.githubusercontent.com/microsoft/Agensh/2dae4e14a653da48549fd9aa093f834841475d6c/README.md). The table is an analyst comparison, not a pooled empirical ranking.

## What the evidence does and does not support

MASBench constructs tasks where agents hold different information, allowing controlled study of collaboration mechanisms. That design differs from giving every worker the complete prompt. ST-Bench reports that much of the team advantage comes from producing realistic numerical outputs on more queries, while conditional numerical quality is comparable to its baseline. It also reports additional inference-time cost and variation across configurations. Consequently, “more successful tasks” does not by itself show that every completed answer improved.

Agensh documents asynchronous cooperation through a Git workspace, messages and shared context. Its architecture is relevant to integration, but its worker count alone cannot establish cost efficiency. No result here establishes a universal best team size. [[concepts/protocol-relative-scores]] and [[concepts/comparator-construction-shapes-margins]] explain why budgets and baseline construction must remain visible.

[[projects/workflowarena]] adds a distinct instrument for authored worker workflows; [[projects/tandembench]] examines coordination-plan selection; [[projects/geofaham]] supplies artifact-centric coordination in another domain. Consult their canonical records for source-specific evidence; these are reading links, not additional results independently verified by this comparison.

## Proposed controlled experiment

Run fixed interdependent tasks with 1, 2, 4 and 8 workers under two separate conditions: fixed total token/spend budget, and fixed wall-clock budget with aggregate resource use recorded. Hold model, tools, input access and acceptance checker constant. Repeat tasks across seeds or run order. Record fully accepted deliverables, regressions, partial-information mistakes, conflicts, communication cost, total tokens and critical-path time. Separate coverage from quality conditional on completion, and include setup and integration overhead. Report per-task outcomes rather than only an average.

This protocol tests team value; it does not assume a favorable result. [[concepts/verified-completion-vs-apparent-success]] motivates independent integrated acceptance.

## Evidence status and reading path

Primary documents were read on November 14, 2026. Study outcomes remain author-reported; no benchmark or framework was executed here. Continue through [[topics/coordination-and-orchestration]] and [[techniques/multi-agent-orchestration]].
