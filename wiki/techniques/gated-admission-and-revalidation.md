---
uid: 48c08f75-dde8-4484-9562-da89e59fe8f4
title: "Gated admission and revalidation"
summary: "Validate reusable agent artifacts before admission, retain applicable evidence and revalidate after relevant changes."
type: technique
created: 2026-11-14
updated: 2026-11-16
depth: full
sources:
  - https://arxiv.org/html/2610.39508v1
  - https://arxiv.org/html/2610.39884v2
  - https://arxiv.org/html/2611.05251v1
  - https://github.com/vercel-labs/agent-browser/releases/tag/v0.42.0
---

# Gated admission and revalidation

## Mechanism

An admission gate separates a candidate artifact from the store that future agent work trusts. Revalidation asks whether earlier acceptance still applies after the artifact, its contract or its environment changes. The lifecycle is a cross-project architectural comparison; the gates below certify different properties.

| Design | Admission decision | Reuse boundary |
|---|---|---|
| [[projects/skillcompiler]] | Validate a program against operation inputs, outputs and local checks before admission. | Reuse requires compatible bindings, satisfied preconditions, required interfaces and an applicable validation record. Implementation, contract or supported-condition changes require revalidation. |
| [[projects/karma]] | Retain candidate knowledge patches through validation and snapshot rollback. | Knowledge is evaluated in an offline decision setting; a development-set gain does not certify safe transfer to another domain. |
| [[projects/auto-research]] | Automatic tool checks, a different-provider model review and human promotion to the trusted branch. | The reported-number provenance gate is a separate check from admission of the tool itself. |

Sources: [SkillCompiler, program assets and validation](https://arxiv.org/html/2610.39508v1), [KARMA, validation/rollback and transfer](https://arxiv.org/html/2610.39884v2), [auto_research, sections 3 and 5](https://arxiv.org/html/2611.05251v1). Mechanisms and outcomes remain author-reported.

## Design questions

Keep candidate creation separate from authority to promote. Record the accepted artifact and the conditions under which its checks apply. Reuse should consult those conditions rather than treating a historical pass as permanent certification. A rollback snapshot supports recovery; it does not identify every semantic regression. Invocation authorization remains distinct from admission: a valid tool may still be inappropriate for the current request. Compare [[projects/toolguardian]] and [[topics/security-and-authority]].

## Applicability after replay and environment changes

[[techniques/deterministic-workflow-reuse]] compares operation compilation, task compilation and recorded replay. [[projects/skillcompiler]] explicitly requires applicable validation records and observable preconditions; [[projects/agent-browser]] instead documents saved-flow execution tiers ([SkillCompiler](https://arxiv.org/html/2610.39508v1), [agent-browser](https://github.com/vercel-labs/agent-browser/releases/tag/v0.42.0)). Do not infer equivalent admission guarantees from the fact that both reuse an artifact.

When a resource, session, permission or requirement changes, ask which prior validation still applies. [[concepts/replay-idempotency-and-effect-semantics]] explains why deterministic rerunning does not settle an uncertain mutation. [[concepts/contracts-and-compositional-correctness]] explains why valid local artifacts need integration checks. These are analytical implications and proposed evaluation dimensions, not measured benefits from a demonstrated combined system.

## Limits and counterexamples

auto_research's defect-injection study reports defects that passed automatic checks and a defect surviving subsequent review; it also reports rejected correct changes. Admission therefore has both false negatives and false positives. KARMA's transfer analysis bounds assumptions that retained knowledge helps every domain. SkillCompiler's local validation is narrower than whole-task correctness. These are reasons to test the gate and preserve [[concepts/scoped-assurance]], not reasons to treat all gates as interchangeable.

[[concepts/improvement-lives-in-external-state]] locates persistent artifacts. [[concepts/preservation-aware-agent-improvement]] asks what earlier capabilities are lost. [[techniques/agent-skills-and-memory]] compares the wider memory lifecycle.

## Proposed gate-isolation experiment

Freeze a candidate stream, source tasks, base model and reusable store. Compare identical candidates under no gate, schema/local execution checks, and independent acceptance plus a task-level regression gate. Test on held-out cases and previously solved cases; include changed invocation conditions. Record false admissions, false rejections, retained correctness, negative transfer, revalidation cost and rollback behavior. Keep admission decisions separate from the evaluator used to measure outcomes. No experiment is reported here.

## Evidence status and reading path

The cited primary papers were read on November 14, 2026. The lifecycle comparison is analytical; it is not an independently replicated gain from adding a gate. Continue through [[topics/memory-and-improvement]] and [[topics/verification-and-evaluation]].
