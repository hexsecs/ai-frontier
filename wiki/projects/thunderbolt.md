---
uid: 019a5b21-21b4-7c91-8a42-18d90b5e11f6
title: "Thunderbird Thunderbolt 0.1.164–0.1.165"
summary: "Reusable provider authorization and bounded renderer recovery in an agent-enabled desktop workspace."
type: project
created: 2026-11-16
updated: 2026-11-16
depth: brief
sources:
  - https://github.com/thunderbird/thunderbolt/blob/main/CHANGELOG.md
  - https://raw.githubusercontent.com/thunderbird/thunderbolt/2f81a4d9897cc92839632137fc7d38fee75ba240/CHANGELOG.md
---

# Thunderbird Thunderbolt 0.1.164–0.1.165

**Source and date:** https://github.com/thunderbird/thunderbolt/blob/main/CHANGELOG.md (2026-11-11–12).

Thunderbolt adds reusable provider connections and authorization, improves MCP connection entry, and bounds WebKit renderer recovery after crashes. Its surrounding release history documents agent workspace attachments, browser/test workflows and authorization surfaces, but the cited versions do not establish autonomous email-task success.

**Mechanism:** Reusable connector identity and explicit authorization in an end-user agent workspace, with bounded GUI recovery.

**Evidence and limits:** A useful exploration outside coding agents: connector lifecycle and embedded browser crashes matter for consumer automation. Compared with generic MCP integrations, the concrete delta is provider authorization reuse and a recoverable desktop runtime. Real application integration, but mainly incremental reliability work. Release documentation does not independently establish measured reliability.

**Evaluation:** Using a disposable account, authorize two providers once, interrupt the embedded web view and verify connection reuse, no silent privilege expansion and correct resumption of an unfinished draft.

## Conceptual context

Distinguish assignment and connector identity from enforced action scope, inheritance ceilings and revocation. See [[concepts/delegated-authority-and-revocation]]. Locate enforcement surfaces and retain the limits of the tested security boundary. See [[techniques/secure-agent-operations]].
