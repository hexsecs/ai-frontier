---
type: index
title: "Coordination and orchestration"
summary: "Divide work, exchange artifacts and assess the value of delegation."
---

# Coordination and orchestration

How do agents divide work, preserve shared information and integrate a correct final deliverable?

## Start here

1. [[techniques/multi-agent-orchestration]] — Compare mechanisms rather than treating all teams as interchangeable.
2. [[evaluations/multi-agent-value-and-coordination]] — Assess accepted output against total cost.
3. [[concepts/verified-completion-vs-apparent-success]] — Verify the integrated result.

## Compare architectures and instruments

| Concern | Reading | Distinction |
|---|---|---|
| Shared work and parallel integration | [[projects/agensh]], [[projects/agent-orchestrator]] | Worker count, authority and integration gates are separate choices. |
| Typed handoffs and repair | [[projects/agenticds]], [[projects/dittany]] | Declared contracts do not establish successful downstream execution. |
| Artifact-centric coordination | [[projects/geofaham]], [[projects/crossswe]] | Geospatial metadata and repository interfaces require different checks. |
| Partial information | [[projects/masbench]] | Communication closes information gaps at a cost. |
| Authored workflows | [[projects/workflowarena]] | Worker organization and integrated deliverables are evaluated together. |
| Plan selection and team value | [[projects/tandembench]], [[projects/st-bench]] | Selecting an optimal plan differs from executing a useful team workflow. |

## Limits and experiments

No universal team size follows from these different protocols. [[evaluations/multi-agent-value-and-coordination]] proposes matched-budget tests and separates coverage from conditional quality. [[topics/agent-execution-and-recovery]] covers interrupted workers; [[topics/security-and-authority]] covers their permissions.
