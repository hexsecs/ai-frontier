---
uid: b6a90502-a8d1-4d13-9a40-000000000022
title: "SeaFlow"
summary: "Canonical evidence record for SeaFlow; mechanism, limitations, practical implications and source provenance from the November 5 briefing."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: brief
sources:
  - https://arxiv.org/abs/2611.01840
  - https://github.com/Applied-Machine-Learning-Lab/NeurIPS2026_SeaFlow
---

# SeaFlow

**Origin:** [[briefings/2026/11/2026-11-05]] — finding 2. **Provenance:** This canonical record is backfilled from the archived research briefing. It is not a fresh independent source review or replication. Date and evidence limitations remain as reported in the snapshot.

## Archived evidence and assessment

**Date:** November 1, 2026 paper; repository inspected November 5. **Sources:** [paper](https://arxiv.org/abs/2611.01840), [implementation](https://github.com/Applied-Machine-Learning-Lab/NeurIPS2026_SeaFlow). **Verdict:** High relevance and actionable; author-reported competition evidence.

**Built/demonstrated:** A framework for decomposing complex tasks into procedures with explicit applicability conditions. Procedures either execute code or call a model; execution feedback refines the decomposition and procedure selection. The authors evaluated bargaining, negotiation and persuasion in the GLEE competition and report first overall in the competition in the repository description.

**Agentic mechanism:** Turn repeatable decision segments into code while reserving LLM reasoning for uncertain or context-dependent steps. This is *selective compilation of behavior*, not blind conversion of every agent thought into a script.

**Evidence:** The paper reports that most observed final-decision procedures are implemented as code. The repository contains an implementation, but the competition result and efficiency claims are author-reported here; no controlled local cost or accuracy comparison was performed.

**Why frontier / comparison:** Builds on the pattern in SkillCompiler already cataloged in the KB: the novel emphasis is semantic task decomposition with explicit applicability conditions and feedback-driven evolution in interactive strategic tasks. It suggests a useful optimization objective: replace repeated model calls with stable procedures without losing adaptability.

**Practical takeaway:** Instrument a recurring agent workflow and classify each decision as deterministic, bounded-choice, or genuinely open-ended. Compile only the first two classes, then measure cost, success and fallback frequency.

**Caveat:** Success in negotiation games does not establish performance in repository engineering or browser automation; applicability-condition errors may silently route work to an unsuitable procedure.

## Knowledge-base synthesis

This entry preserves the finding as a reusable canonical reference rather than leaving it accessible only by briefing date. Compare its stated mechanism and evidence tier against [[concepts/scoped-assurance]], [[concepts/validation-tier-gap]], and the [November 3–9 cross-briefing synthesis](../evaluations/briefing-synthesis-2026-11-03-to-09.md). These are analyst-level thematic connections, not assertions that the original project cites or implements the linked concepts. Future source verification should replace this backfill with a deeper independently checked treatment while retaining this page identity.
