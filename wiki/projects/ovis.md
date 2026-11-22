---
uid: c29f5b6b-b8bb-4f79-a720-9ed31d4839e2
title: "Ovis"
summary: "Remote desktop-agent workspace with per-agent browser tool assignment and selectable browser opening."
type: project
created: 2026-11-22
updated: 2026-11-22
depth: full
sources:
  - https://github.com/devswha/ovis/releases/tag/v0.5.8
---

# Ovis

**Primary release:** [November 21, 2026](https://github.com/devswha/ovis/releases/tag/v0.5.8).

The November 21 v0.5.8 release notes describe desktop apps opening web links in a chosen browser, agent-specific browser-tool assignment through Settings, and an optional single-sign-in account-opening mode on a PC. These are maintainer-documented features; no independent security or usability measurements are provided.

**Mechanism.** Browser capability is selected for each agent rather than being implicitly available to all; link opening and browser tool invocation are different actions. [[concepts/delegated-authority-and-revocation]] explains the difference between tool assignment and enforced resource/action scope; [[techniques/secure-agent-operations]] discusses mediation and bypass risk.

**Novelty.** A practical incremental desktop/remote-workflow integration. A UI setting does not by itself establish that an agent cannot reach a browser through another tool or an already-open session.

**Proposed experiment.** Create two agents, grant a browser tool to only one, and attempt 20 benign browser actions via direct and alternate paths on a disposable profile. Record denied effects, unexpected navigation and cross-agent session leakage. No security audit was performed.
