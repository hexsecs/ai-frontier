---
uid: 9e817117-35ed-46dc-be4b-b41b5e1832fd
title: "extension.dev MCP"
summary: "Capability-separated publication authority with source-grounded mechanisms and evidence limits."
type: project
created: 2026-11-20
updated: 2026-11-20
depth: full
sources:
  - https://github.com/extensiondev/mcp
---

# extension.dev MCP

**Primary source:** https://github.com/extensiondev/mcp. **Source date:** 2026-11-19.

## Demonstrated capability and mechanism

An MCP server gives agents tools to build, run, inspect, test and ship browser extensions, separating local tools from authenticated platform tools. Feature groups, --no-ship refusals, project scoping and owner approval gate publishing and store submission.

**Reusable concept:** Capability-separated publication authority. Concrete domain-specific authorization boundary; November 19 denotes repository activity, not a release. No independent security audit.

## Boundaries and test

Build a harmless extension in no-ship mode; attempt ten forbidden platform operations and verify no external side effects.

This is a proposed experiment, not an independently reproduced result. See [[briefings/2026/11/2026-11-20]] and [[concepts/verified-completion-vs-apparent-success]] for comparisons and acceptance limits.
