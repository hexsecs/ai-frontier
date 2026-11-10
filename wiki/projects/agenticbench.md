---
uid: b6a90504-a8d1-4d13-9a40-000000000024
title: "AgenticBench"
summary: "Canonical evidence record for AgenticBench; mechanism, limitations, practical implications and source provenance from the November 5 briefing."
type: benchmark
created: 2026-11-09
updated: 2026-11-09
depth: full
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

## Mechanism and boundary

The reusable mechanism is **Agentic task evaluation and measurement protocol**. Distinguish model reasoning, tool execution, persistent state, side effects, and the independently observed acceptance condition. The historical source summary above is the factual evidence base; the interpretation below is an analyst synthesis.

## Critical evidence assessment

**Failure mode / counterweight:** Reported benchmark results are sensitive to harness, evaluator and task distribution. The cited sources have not been independently reproduced in this mining pass. Report source-reported metrics as such, and do not equate a successful demo, publication, repository release or PR proposal with production readiness. Negative and missing results matter as much as successes.

## Directional relationships and comparative interpretation

Related evidence: [[benchmarks/index]]; [[concepts/validation-tier-gap]]. These are analyst-level **compares_with** links, not verified direct dependencies. Compare this mechanism against the simpler baseline, distinguish quality from throughput, and preserve task-level losses rather than averaging them away. See [[evaluations/briefing-synthesis-2026-11-03-to-09]].

## Reproducible evaluation

**Proposed, not executed:** Re-run a frozen task subset with independent scorers; log score variance and judge disagreement. Hold model, prompts, inputs and budget constant; log task-level results, full tool receipts, source spans, failed attempts, checker execution, elapsed time and tokens. Evaluate unseen cases and require explicit evidence before promoting changes to a trusted workflow.

## Deployment considerations and open questions

Sandbox the initial integration. Specify the authority boundary, persistence model, rollback path and owner of independent acceptance. Open questions include transfer to unseen tasks, sensitivity to the evaluator, total operational cost and whether the same improvement survives adversarial failure injection.

## Provenance and depth

**Full analytical treatment based on the dated primary-source briefing; not an independent replication.** Historical claims are preserved above; comparisons, risks and tests in this section are proposed analyses.
