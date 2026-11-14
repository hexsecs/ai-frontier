---
uid: e2f32dc4-4ed5-40d5-9a90-c8a98f9d9e31
title: "GeoFaham: Multi-Agent Disaster Geospatial Analytics"
summary: "Specialist agents coordinate geospatial analysis with typed artifacts, persistent responses and dependency-aware planning."
type: project
created: 2026-11-13
updated: 2026-11-13
depth: brief
related: [crossswe]
sources:
  - https://arxiv.org/abs/2611.04977
---

# GeoFaham: Multi-Agent Disaster Geospatial Analytics

**Source:** https://arxiv.org/abs/2611.04977. **Publication:** 2026-11-03. **Evidence:** author-reported; no independent replication.

## Mechanism
Specialist agents for vector operations, map features, imagery discovery and raster analysis, coordinated by a dual-ledger orchestrator. A Response Store persists full spatial artifacts with typed metadata while agents exchange compact identifiers.

**Technique:** Artifact-centric multi-agent coordination with dependency-aware planning, validation and replanning across spatial and temporal data.

## Evidence and limitations
On a 40-task benchmark grounded in 17 disaster records, the authors report 0.940 overall versus 0.879 for the next-best baseline and 7.5× fewer tokens.

Author-run benchmarks do not prove emergency-response readiness.

## Comparison
An unusual consequential domain where correctness depends on provenance of huge non-text artifacts.

Related: [[projects/crossswe]]; relation is analytical, not a demonstrated integration.

## Proposed experiment
Replay five public disaster tasks and inspect coordinate reference systems, timestamp lineage, raster-vector alignment and artifact handoffs.

## Provenance
[[briefings/2026/11/2026-11-13]] — complete dated narrative.
