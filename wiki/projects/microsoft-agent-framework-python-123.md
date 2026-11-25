---
uid: aaffc69a-591d-495c-b6a2-b14302281bd2
title: "Microsoft Agent Framework Python 1.23"
summary: "SDK release fixes atomic memory writes, completion waits, nested stream cleanup and MCP connection recovery."
type: project
created: 2026-11-23
updated: 2026-11-23
depth: full
sources:
  - https://github.com/microsoft/agent-framework/releases
---

# Microsoft Agent Framework Python 1.23

**Source:** https://github.com/microsoft/agent-framework/releases. **Source date:** 2026-10-22. 

## Mechanism and demonstrated scope

Atomic Memory and Todo writes, execution-identity-bound background completion waits, abandoned nested-stream closure and owned MCP connection recovery. The reusable boundary is [[concepts/agent-state-and-lifecycle]]; this implementation does not by itself establish that other systems share its results.

## Evidence and limits

Maintainer release notes; no independent crash-recovery or exactly-once external-effect measurements. The described behavior should be treated as implementation documentation or author-reported findings, not independent replication.

## Proposed bounded experiment

On 20 disposable workflows, interrupt writes and nested streams, then compare durable records, lost events and externally verified effects. No experiment is reported as executed here.
