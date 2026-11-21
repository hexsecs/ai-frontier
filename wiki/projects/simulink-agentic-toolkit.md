---
uid: c49d0eb3-65b5-4871-8d55-6134c7a36e20
title: "Simulink Agentic Toolkit"
summary: "MATLAB MCP tools and domain skills let coding agents inspect, edit and check Simulink models."
type: project
created: 2026-11-21
updated: 2026-11-21
depth: full
sources:
  - https://github.com/matlab/simulink-agentic-toolkit
---

# Simulink Agentic Toolkit

**Primary source:** https://github.com/matlab/simulink-agentic-toolkit. **Evidence:** inspected maintainer release/README; no independent reproduction.

## Implementation
The MathWorks repository documents an MCP server connection to MATLAB/Simulink, paired with domain skills for model-based design. Tools include model_overview, model_read, model_edit, model_check and diagnostics. It requires MATLAB R2023a or newer with Simulink; some checks and skills require additional licensed products. Repository activity was observed November 21, 2026, not verified as a release date.

## Mechanism and bounds
The tool layer exposes structured model operations; the skills layer encodes domain procedures. Model structure checks catch certain malformed connections but do not establish functional safety, requirements satisfaction or real-vehicle behavior. [[concepts/contracts-and-compositional-correctness]] separates local model checks from whole-system acceptance; [[techniques/embodied-and-scientific-agents]] addresses simulation-versus-physical evidence. No independent correctness comparison was identified in the inspected README.

## Proposed experiment
On five small shipped example models, plant known disconnected ports and parameter errors; compare agent editing with and without skills while keeping tools fixed. Record structural detection, simulation output differences, tool-call count and human-reviewed requirements coverage. Do not use safety-critical production models.
