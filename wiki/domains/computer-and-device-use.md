---
uid: 6f7a9b03-78be-47b9-a412-000000000003
title: "Browser, desktop and physical interfaces"
summary: "Agentic interaction with GUI, browser, terminal and physical-device interfaces, with distinct evidence tiers."
type: domain
created: 2026-11-09
updated: 2026-11-22
depth: brief
sources:
  - https://arxiv.org/abs/2611.08321
  - https://github.com/platonai/Browser4/releases/tag/v4.16.9
  - https://github.com/devswha/ovis/releases/tag/v0.5.8
  - https://github.com/trycua/cua/pull/6405
  - https://arxiv.org/abs/2611.05827
---

# Browser, desktop and physical interfaces

This domain groups application contexts, not a validated universal agentic technique. See [[projects/controlanything]], [[projects/cua-agentenv]], [[projects/browser4]], [[benchmarks/index]] for canonical source-backed records. Compare outcomes only after matching task scope, deployment maturity, and independent verification tier. Cross-domain patterns and limitations are synthesized in [[evaluations/briefing-synthesis-2026-11-03-to-09]].


[[projects/agent-browser]] and [[projects/sopguard]] connect saved browser procedures with a distinct cross-origin information-flow question. [[concepts/replay-idempotency-and-effect-semantics]] explains why replay and verified physical or remote effects need separate evidence.


[[projects/browser4]]'s November 21 release describes multi-turn browser-context carry with real-browser end-to-end tests still pending ([release](https://github.com/platonai/Browser4/releases/tag/v4.16.9)). [[projects/ovis]] separately documents agent-specific browser-tool selection for desktop workflows ([release](https://github.com/devswha/ovis/releases/tag/v0.5.8)). Preserving context and authorizing browser actions are independent concerns: a correct follow-up may still be unauthorized, and an authorized action may use stale page observations. Test them separately before combining the mechanisms.
