---
uid: a573ebff-6226-41c3-b231-a38fddd96584
title: "AgenTopology — Declarative multi-agent topology"
summary: "A declarative `.at` language for defining agent roles, flows, memory and tool permissions. The CLI validates topologies,"
type: project
created: 2026-11-10
updated: 2026-11-10
depth: full
sources:
  - https://github.com/agentopology/agentopology
---

# AgenTopology — Declarative multi-agent topology

**Source and date:** https://github.com/agentopology/agentopology (2026-11-10 (repository inspected; v0.4 described, release date unverified)).

## Mechanism

A declarative `.at` language for defining agent roles, flows, memory and tool permissions. The CLI validates topologies, visualizes dependencies, scaffolds platform-specific configurations, or issues a plan for an existing coding agent to execute with subagents. Harness-as-code with explicit handoff contracts, blind roles, validation and disclosure of features that cannot be enforced in fileless mode.

## Evidence and novelty

Repository contains parser/source, examples, a CLI and tests. Claims of cross-platform support are implementation claims; no comparative productivity benchmark was verified. Medium-high: topology as a portable typed artifact, not another chat-based swarm demo.

## Comparison

A practical configuration-layer counterpart to the previously covered agent orchestration and ACP provenance work; unlike those, it focuses on declarative portability.

## Limitations

Portability and enforcement differ by target runtime; never mistake a declared restriction for a sandbox-enforced one.

## Reproducible next step

Describe the same researcher–builder–adversarial-reviewer team for Hermes and Codex; diff generated permissions and explicitly record non-enforceable constraints.

## Related

- [[briefings/2026/11/2026-11-10]] — dated full-fidelity research and cross-project synthesis.
