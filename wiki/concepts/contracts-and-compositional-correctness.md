---
uid: 697dcb21-5baf-4948-8449-e8aee7cd0e32
title: Contracts and compositional correctness
summary: Distinguish valid component outputs from satisfied dependencies and independently accepted whole-task outcomes.
type: concept
created: '2026-11-16'
updated: 2026-11-21
depth: full
sources:
- https://arxiv.org/html/2610.39608
- https://arxiv.org/html/2610.42144
- https://arxiv.org/html/2611.01484v1
---

# Contracts and compositional correctness

## The distinction

A contract states the inputs, outputs, preconditions or obligations expected at a boundary. A schema can establish the shape of an artifact; an executable check can test a stated behavior. Neither alone proves that every dependency is satisfied or that the assembled workflow meets its objective.

**Compositional correctness** asks what must hold between components as well as within them. The comparison below identifies a dependency problem across different settings; it does not assert that those settings share one experimentally established failure mechanism.

A structured domain tool can make local obligations observable without proving the full engineering artifact correct. [[projects/simulink-agentic-toolkit]] ([MathWorks repository](https://github.com/matlab/simulink-agentic-toolkit)) exposes model reading, editing, structural checks and diagnostics through MCP, with separate model-based-design skills. A detected disconnected port is a local model defect; a passing structural check does not establish correct simulation behavior, requirements coverage or physical safety. The toolkit's documentation is implementation evidence, not an independent functional-safety validation. A controlled test should compare planted connection faults, parameter faults and system-level acceptance separately.

## Evidence-bearing examples

[[projects/agenticds]] makes model decisions instantiate typed objects before deterministic code consumes them, with plans, protocols and evidence packages exchanged across roles ([paper](https://arxiv.org/html/2610.39608)). Typed exchange makes obligations explicit; downstream usefulness still needs evaluation.

[[projects/dittany]] derives expected contributions and acceptance conditions from requirements and method specifications, connects dependencies, and preserves validated contributions during action- or graph-level repair ([paper](https://arxiv.org/html/2610.42144)). This explains why recovery scope can exceed the location of the visible failure.

[[projects/crossswe]] constructs jointly necessary multi-repository tasks and evaluates the complete final repository state ([paper](https://arxiv.org/html/2611.01484v1)). Locally plausible changes can still leave incompatible interfaces. A task spanning several repositories is not automatically evidence that every change was jointly necessary.

## Three questions to check

1. **Local validity:** does each artifact satisfy its own declared checks?
2. **Boundary compatibility:** do producer outputs meet consumer assumptions, versions and dependency conditions?
3. **Task acceptance:** do the integrated effects satisfy the actual objective, including requirements not represented in local schemas?

These questions are an analytical checklist, not an independently validated evaluation protocol. [[concepts/scoped-assurance]] bounds each check; [[concepts/verified-completion-vs-apparent-success]] distinguishes whole-task acceptance from reported progress.

[[projects/workflowarena]] and [[projects/geofaham]] provide adjacent canonical records on integrated deliverables and typed spatial artifacts. They are reading leads, not additional measurements reproduced for this comparison. [[techniques/multi-agent-orchestration]] discusses handoffs; [[techniques/gated-admission-and-revalidation]] discusses reusable component admission.

## Limits and proposed test

A perfectly implemented contract can encode the wrong requirement. Formal checking is relative to the specification and trusted assumptions, as the [[projects/alphaproof-code]] record illustrates. Schema agreement, test success and proof acceptance should therefore retain their actual scope.

Construct paired components that pass local tests but violate a shared version, unit or interface assumption. Compare local-only checks with cross-boundary and final acceptance checks. Report interface violations, falsely accepted tasks, preserved valid work and repair cost. No result is asserted for this proposed test; underlying study results remain author-reported.
