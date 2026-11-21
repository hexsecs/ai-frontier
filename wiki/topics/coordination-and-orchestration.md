---
type: index
title: "Coordination and orchestration"
summary: "Divide work, exchange artifacts and assess the value of delegation."
---

# Coordination and orchestration

How do agents divide work, preserve shared information and integrate a correct final deliverable?

## Start here

[[concepts/contracts-and-compositional-correctness]] explains dependency obligations; [[concepts/agent-state-and-lifecycle]] explains terminal child/parent states. [[concepts/delegated-authority-and-revocation]] separates work assignment from permission.

1. [[techniques/multi-agent-orchestration]] — Compare mechanisms rather than treating all teams as interchangeable.
2. [[evaluations/multi-agent-value-and-coordination]] — Assess accepted output against total cost.
3. [[concepts/verified-completion-vs-apparent-success]] — Verify the integrated result.

## Compare architectures and instruments

| Concern | Reading | Distinction |
|---|---|---|
| Shared workspace and approvals | [[projects/openagents-workspace]] | Sharing artifacts, using an agent and approving publication are different authorities. |
| Shared work and parallel integration | [[projects/agensh]], [[projects/agent-orchestrator]] | Worker count, authority and integration gates are separate choices. |
| Typed handoffs and repair | [[projects/agenticds]], [[projects/dittany]] | Declared contracts do not establish successful downstream execution. |
| Artifact-centric coordination | [[projects/geofaham]], [[projects/crossswe]] | Geospatial metadata and repository interfaces require different checks. |
| Partial information | [[projects/masbench]] | Communication closes information gaps at a cost. |
| Authored workflows | [[projects/workflowarena]] | Worker organization and integrated deliverables are evaluated together. |
| Plan selection and team value | [[projects/tandembench]], [[projects/st-bench]] | Selecting an optimal plan differs from executing a useful team workflow. |

## Limits and experiments

No universal team size follows from these different protocols. [[evaluations/multi-agent-value-and-coordination]] proposes matched-budget tests and separates coverage from conditional quality. [[topics/agent-execution-and-recovery]] covers interrupted workers; [[topics/security-and-authority]] covers their permissions.


## Whole-team safety obligations

[[projects/aligning-ai-teams]] finds in controlled tasks that peer critique and group chat do not reliably protect whole-system safety goals when delegated workers focus on their local roles. A named safety lead plus coordinator-authored specification improved alignment in the studied tradeoffs ([primary paper](https://arxiv.org/abs/2611.17820)). This is not proof that a safety lead always improves coding quality; use [[techniques/multi-agent-orchestration]] for comparison with typed contracts and evolving team rules.

## Harness mechanism integration

[[projects/elite-evaluation-free-self-improvement]] integrates independently proposed changes to one coding-agent implementation without selecting candidate agents by downstream task score. This is source-level integration, not multi-agent task delegation or proof of whole-system correctness; compare [[concepts/preservation-aware-agent-improvement]].


[[projects/protoagent-project-board]] grounds delegated coding work in a durable task board and PR lifecycle; [[projects/openjiuwen-agent-core-020]] documents scheduled verifier/challenger review and cancellation-state fixes. Neither establishes cross-framework interoperability. See [[techniques/multi-agent-orchestration]].
