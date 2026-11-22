---
uid: 6f7a9b02-78be-47b9-a412-000000000002
title: "Scientific and embodied systems"
summary: "Agentic research, robotics and scientific instruments grouped as an application domain, not a single mechanism."
type: domain
created: 2026-11-09
updated: 2026-11-21
depth: brief
sources:
  - https://arxiv.org/abs/2611.05251
  - https://arxiv.org/abs/2611.06555
  - https://arxiv.org/abs/2611.07947
---

# Scientific and embodied systems

[[projects/simulink-agentic-toolkit]] brings agent tools into model-based design through MATLAB/Simulink MCP operations and domain skills ([source](https://github.com/matlab/simulink-agentic-toolkit)). Its model checks are engineering-artifact validation, not evidence of physical actuation or certified safety. It should be compared with instrument and robotics studies only after separating simulation, model consistency and independently observed physical outcomes.

This domain groups application contexts, not a validated universal agentic technique. See [[projects/auto-research]], [[projects/fa-agent]], [[projects/cheme-as-code]], [[projects/roboarchitect]] for canonical source-backed records. Compare outcomes only after matching task scope, deployment maturity, and independent verification tier. Cross-domain patterns and limitations are synthesized in [[evaluations/briefing-synthesis-2026-11-03-to-09]].


[[projects/the-agentic-researcher]] provides a canonical long-running scientific workflow record. [[concepts/agent-state-and-lifecycle]] and [[techniques/artifact-and-claim-provenance]] distinguish duration, execution state and the evidence behind a scientific claim.


[[projects/robocoevo]] ([primary paper](https://arxiv.org/abs/2611.19081)) studies a simulation-only loop in which an agent writes recovery programs for failed robot-policy rollouts and retrains the policy on corrective experience. Unlike frozen-policy harness evolution, both program and policy change; [[techniques/embodied-and-scientific-agents]] distinguishes that mechanism from physical instrument evidence.
