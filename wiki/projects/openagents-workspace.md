---
uid: 34e885dd-cc52-4f9e-a4bd-8e17ad9c2b66
title: "OpenAgents Workspace"
summary: "Shared human-agent threads coordinate tools, approvals, files and browser artifacts."
type: project
created: 2026-11-21
updated: 2026-11-21
depth: full
sources:
  - https://github.com/openagents-org/openagents
---

# OpenAgents Workspace

**Primary source:** https://github.com/openagents-org/openagents. **Evidence:** inspected maintainer release/README; no independent reproduction.

## Implementation
The OpenAgents README describes a persistent workspace for multiple agent runtimes, shared threads, files and browser views. Its v1.1 description adds private-by-default sharing, task routing, approvals for consequential actions, issues and retained results. A November 20, 2026 repository workflow shows a change described as saving an agent message as knowledge; the exact PR diff was not inspected, so no detailed behavior of that change is asserted.

## Mechanism and bounds
Shared conversation state and knowledge folders improve access to artifacts but do not independently certify their correctness. Explicit approval cards are control-plane decisions; whether every side-effect path is enforced requires testing. [[concepts/delegated-authority-and-revocation]] explains permissions, [[techniques/multi-agent-orchestration]] explains handoffs and [[techniques/artifact-and-claim-provenance]] explains evidence retention. README claims are maintainer documentation, not measured operational guarantees.

## Proposed experiment
Connect two disposable agents and one reviewer, create ten simulated deploy/delete tasks, and vary private/public threads and approval policies. Test cross-user access, bypass through alternate tool paths, retained artifact provenance and whether denied actions caused effects.
