---
uid: d32307fe-7e0d-46f0-b8b7-aed4fa2a0c0f
title: Paperclip
summary: Persistent agent files, explicit task assignment and observable browser takeover in a documented operations release.
type: project
created: '2026-11-16'
updated: '2026-11-16'
depth: full
sources:
- https://raw.githubusercontent.com/paperclipai/paperclip/b4fa1c7fb1c9adafc6407bc46381a0ab89f4b4fd/releases/v2026.1005.0.md
---

# Paperclip

## Mechanism and evidence

[Paperclip v2026.1005.0](https://raw.githubusercontent.com/paperclipai/paperclip/b4fa1c7fb1c9adafc6407bc46381a0ab89f4b4fd/releases/v2026.1005.0.md) documents agent-owned files persisting across tasks and sessions, GitHub-synchronized skills and Browser Use Cloud sessions that people can observe and take over. The same release says that mentions no longer start work: explicit assignment or review requests trigger execution.

Persistence and task ownership solve different problems. Retained files provide continuity, while explicit assignment determines when work starts. [[concepts/agent-state-and-lifecycle]] separates those states; [[concepts/delegated-authority-and-revocation]] distinguishes task assignment from permission to act. These are analyst comparisons, not proof that Paperclip implements every mechanism on those pages.

## Limits and proposed test

The release notes establish documented features, not an independently measured recovery or security rate. Persistent files do not prove that every tool effect can be safely retried. See [[techniques/durable-agent-execution]] and [[techniques/agent-skills-and-memory]].

Proposed test: use disposable tasks, force a restart, perform a human takeover and verify which files, ownership records and browser state survive. Check that a mention alone cannot trigger execution. Record duplicate effects and uncertain outcomes separately. No test was run here.

## Provenance

Historical discovery: [[briefings/2026/11/2026-11-14]]. The cited October release is older than that briefing date.
