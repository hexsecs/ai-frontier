---
type: index
title: "Agent execution and recovery"
summary: "Run tools, observe effects and recover interrupted work."
---

# Agent execution and recovery

How do agents execute tools, survive interruptions and establish what actually happened?

## Start here

[[concepts/agent-state-and-lifecycle]] introduces the state model; [[concepts/replay-idempotency-and-effect-semantics]] explains retries and effects. [[experiments/lifecycle-authority-and-retention]] tests those boundaries.

1. [[techniques/durable-agent-execution]] — Compare interrupted calls, safe replay and reconciliation.
2. [[concepts/verified-completion-vs-apparent-success]] — Distinguish a completion claim from an observed outcome.
3. [[techniques/adaptive-recovery]] — Choose repair scope and account for downstream dependencies.

## Compare implementations

| Question | Reading | Important boundary |
|---|---|---|
| What survives restart? | [[projects/agentos]], [[projects/rivet-agents]], [[projects/openma]] | Durable session state alone does not establish exactly-once external effects. |
| What did a failed write do? | [[projects/builderio-agent-native]] | Observed channels and explicit labels bound the verdict. |
| Is a process waiting or finished? | [[projects/receipt]] | Process-state evidence does not establish correctness of prior effects. |
| How are handoffs repaired? | [[projects/dittany]] | Local repair and contribution-graph repair are different interventions. |

## Limits and experiments

Use [[concepts/scoped-assurance]] to bound recovery claims. The crash-injection protocol in [[techniques/durable-agent-execution]] distinguishes duplicate effects, lost effects and explicitly unknown outcomes. Consult [[topics/security-and-authority]] for the authority a resumed agent should receive.


## Checkpoint scope and intervention evidence

[[projects/heragent]] tests semantic setup-block rollback against command- and script-level recovery, while [[projects/toolpulse]] tests runtime tool-use cues. The first reports higher environment-setup success in its benchmarks; the second reports substantial changes in agent responses but aggregate patch success close to baseline ([HerAgent](https://arxiv.org/abs/2611.18443), [ToolPulse](https://arxiv.org/abs/2611.19275)). These are distinct acceptance targets; see [[techniques/adaptive-recovery]] for the scoped comparison.
