---
uid: b6a90504-a8d1-4d13-9a40-000000000024
title: "AgenticBench"
summary: "Canonical evidence record for AgenticBench; mechanism, limitations, practical implications and source provenance from the November 5 briefing."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: brief
sources:
  - https://agenticbench.org/
---

# AgenticBench

**Origin:** [[briefings/2026/11/2026-11-05]] — finding 4. **Provenance:** This canonical record is backfilled from the archived research briefing. It is not a fresh independent source review or replication. Date and evidence limitations remain as reported in the snapshot.

## Archived evidence and assessment

**Date:** Leaderboard updated November 4, 2026. **Source:** [benchmark and methodology](https://agenticbench.org/). **Verdict:** Strongly actionable security evaluation; narrow coverage, not a code-quality ranking.

**Built/demonstrated:** An independent rolling evaluation of what coding-agent harnesses do with local machine data, network egress, telemetry, workspace boundaries and secrets. The current v0.7.0 suite has 11 checks and 26 approved harness records. The November 4 additions include Step Code 0.1.6 and Amp build 0.0.1793692836-g3a602a, each 6/11; Hermes Agent 0.22.5 was tested October 30 and scored 7/11. The leaderboard lists Codex 0.163.0 and GitHub Copilot CLI 1.0.103 at 11/11 in their respective October tests.

**Agentic mechanism:** Test the execution *harness* rather than only the code the model generates. Tests assess observable security and privacy controls of a tool-using runtime.

**Why frontier / comparison:** November 4's ToolGuardian proposed policy enforcement; this benchmark examines deployed harness behavior. A passing coding benchmark cannot establish safe workspace isolation or secret handling.

**Practical takeaway:** Run an isolated acceptance suite against the exact installed Hermes/OpenCode/Codex versions before giving an agent real credentials. Record version, test definition, egress destinations, permission prompts, and secret exposure outcomes.

**Caveat:** A pass count is not a comprehensive security certification. The leaderboard explicitly counts not-applicable and untested checks in its denominator; different test versions and conditions must not be compared as though equivalent. No local verification of these scores was performed.

## Knowledge-base synthesis

This entry preserves the finding as a reusable canonical reference rather than leaving it accessible only by briefing date. Compare its stated mechanism and evidence tier against [[concepts/scoped-assurance]], [[concepts/validation-tier-gap]], and the [November 3–9 cross-briefing synthesis](../evaluations/briefing-synthesis-2026-11-03-to-09.md). These are analyst-level thematic connections, not assertions that the original project cites or implements the linked concepts. Future source verification should replace this backfill with a deeper independently checked treatment while retaining this page identity.
