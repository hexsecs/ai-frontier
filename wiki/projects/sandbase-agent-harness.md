---
uid: 439f4fb6-4ad4-4199-aac1-deafbe05f8dd
title: "SandBase Agent Harness"
summary: "A self-hosted runtime with SQLite session state, resumable event streams, sandbox backends and MCP approval policies."
type: project
created: 2026-11-23
updated: 2026-11-25
depth: full
sources:
  - https://github.com/sandbaseai/sandbase-harness
---

# SandBase Agent Harness

**Source:** https://github.com/sandbaseai/sandbase-harness. **Source date:** 2026-11-23. This is observed repository activity, not a confirmed original release date.

## Mechanism and demonstrated scope

The implementation README documents SQLite metadata and workspace file storage, resumable server-sent events, MCP permission policies and approvals, and local-process, Docker, Kubernetes and worker sandbox backends. The reusable boundary is [[concepts/delegated-authority-and-revocation]]; this implementation does not by itself establish that other systems share its results.

## Evidence and limits

Implementation-specific README inspected November 25; its quickstart names v0.3.8, but release timing and version-specific behavior have not been verified. November 23 remains the original discovery date, not a release date. Backend isolation and approval enforcement have not been independently tested. The described behavior should be treated as implementation documentation or author-reported findings, not independent replication.

## Proposed bounded experiment

On a sandbox test account, attempt 20 permitted and denied tool actions across resumed sessions, recording approval enforcement and replay fidelity. No experiment is reported as executed here.
