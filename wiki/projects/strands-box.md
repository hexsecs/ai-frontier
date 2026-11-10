---
uid: 43f5e5d7-9c80-4250-98e6-48b6c493bdb5
title: "Strands Box — Stateful policy sandbox for agents"
summary: "An open-source Rust sandbox for Linux and Apple-silicon macOS combining OS access restrictions, egress control, an MCP b"
type: project
created: 2026-11-10
updated: 2026-11-10
depth: full
sources:
  - https://github.com/strands-agents/box
---

# Strands Box — Stateful policy sandbox for agents

**Source and date:** https://github.com/strands-agents/box (2026-11-10 (repository inspected; not a release date)).

## Mechanism

An open-source Rust sandbox for Linux and Apple-silicon macOS combining OS access restrictions, egress control, an MCP broker and a policy engine. Policies can condition an outbound request on previous file reads or elapsed time. Default-deny semantic and temporal policies enforced outside the agent process, with event history shared across tool gateways.

## Evidence and novelty

The public repository includes code, tests, examples and documentation; no independently verified effectiveness metric was identified in this review. Promising implementation of cross-tool, history-dependent permissions rather than static allowlists.

## Comparison

Complements previously covered Agensh and ToolGuardian: the distinctive idea is policy conditioned on action history across interpreters and gateways.

## Limitations

Preview-stage project; do not infer production hardening or complete containment from its README. Updated repository activity does not establish launch date.

## Reproducible next step

In a disposable VM, test whether reading a designated secret file reliably blocks subsequent outbound HTTP and MCP calls; test bypass paths and policy logging.

## Related

- [[briefings/2026/11/2026-11-10]] — dated full-fidelity research and cross-project synthesis.
