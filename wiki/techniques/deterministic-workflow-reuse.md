---
uid: cd229b81-9c88-4785-9d52-ede46930e22a
title: Deterministic workflow reuse
summary: Compare selective compilation, applicability-conditioned procedures and recorded replay without assuming equivalent effects.
type: technique
created: '2026-11-16'
updated: '2026-11-16'
depth: full
sources:
- https://arxiv.org/html/2610.39508v1
- https://arxiv.org/html/2611.06039
- https://arxiv.org/html/2611.01840
- https://github.com/vercel-labs/agent-browser/releases/tag/v0.42.0
---

# Deterministic workflow reuse

## The reusable mechanism

An agent can construct or discover a procedure, then execute that procedure without making every intermediate decision through a model. The reusable artifact may be one operation, a task program, an applicability-conditioned workflow or a recorded interaction. The selection of the reusable unit and the conditions under which it remains valid are central design choices.

## Comparison

| Approach | Reusable unit | Boundary |
|---|---|---|
| [[projects/skillcompiler]] | Programs for well-specified operations, combined with agent-guided steps. | Reuse requires compatible bindings, observed preconditions, available interfaces and applicable validation. |
| [[projects/baya-compile-then-execute]] | A Python program against a Trusted Website API, compiled before seeing live site content. | Live content cannot induce fresh model-planned operations; unexpected adaptation is constrained too. |
| [[projects/seaflow]] | Subtasks with explicit applicability conditions and procedures that run code or invoke a model. | The workflow evolves from feedback; competition evidence does not establish broad task transfer. |
| [[projects/agent-browser]] | A recorded browser task with HTTP, page-request and browser-command replay tiers. | Session freshness and the equivalence of resulting effects need separate checks. |

Sources: [SkillCompiler](https://arxiv.org/html/2610.39508v1), [Baya](https://arxiv.org/html/2611.06039), [SeaFlow](https://arxiv.org/html/2611.01840), [agent-browser release](https://github.com/vercel-labs/agent-browser/releases/tag/v0.42.0). The table is an analyst comparison of distinct mechanisms, not a pooled benchmark or demonstrated integration.

## Admission, invalidation and fallback

Before reusing a procedure, identify its inputs, preconditions, expected effects, permitted interfaces and acceptance check. An environment, credential or requirement change can invalidate the prior record even if the code is unchanged. [[techniques/gated-admission-and-revalidation]] covers artifact acceptance; [[concepts/contracts-and-compositional-correctness]] covers the dependencies between individually valid operations.

Fallback is part of the contract. A procedure may refuse, return control to a model or try a different execution tier. A fallback that silently expands authority or repeats an uncertain mutation changes the safety problem. See [[concepts/replay-idempotency-and-effect-semantics]] and [[concepts/delegated-authority-and-revocation]].

## Counterexamples and test

Deterministic execution can reliably repeat the wrong procedure. A compiled workflow can preserve a mistaken specification, and a saved flow can omit an important browser-side effect. Removing model calls therefore establishes neither correctness nor a universal cost advantage after compilation and validation overhead.

Proposed test: compare live model planning, reused validated procedures and procedure-plus-fallback on fixed tasks. Vary environmental drift and stale credentials. Measure accepted outcomes, invalidation detection, duplicate effects, authority violations, construction/validation cost and execution cost separately. No experiment is reported here.

### Parameter binding and metamorphic admission

[[projects/agent-behavior-as-code]] ([October 4 paper](https://arxiv.org/abs/2610.04824)) uses a model to write or revise symbolic programs whose inputs remain unbound until execution. Repeated tasks can rebind parameters and run under deterministic control flow, with model calls retained at specified reasoning points. The authors describe variant tests that reject parameters which fail to influence execution, plus regression checks before editing a stored procedure. This differs from recorded browser-flow replay, which reuses observed action sequences, and from compile-then-execute browser isolation, which restricts access to untrusted live content. Those distinctions do not imply a head-to-head performance ranking.

The authors report 71.9% versus 47.4% Pass^4 on telecom tasks and 98.3% versus 97.3% on GSM-Symbolic; the same report notes that one-off WorkArena tasks cost more. Deterministic execution preserves the program's control flow, not correctness of its assumptions, tool side effects or applicability to new tasks. Test changed-input behavior, previously accepted cases, external effects and one-off overhead before admitting a reusable procedure.
