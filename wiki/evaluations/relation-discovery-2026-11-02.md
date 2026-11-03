---
uid: b54b13d9-becf-4eec-a930-975759b1202a
depth: full
title: "Relation discovery — 2026-11-02"
summary: "An evaluation of the summary-level relation pass against source-level mining: which of its eight themes survived as evidenced concepts, and which dissolved."
type: evaluation
created: 2026-11-02
updated: 2026-11-02
sources: []
---

# Relation discovery — 2026-11-02

## What this evaluation is

This page is the record of the knowledge base's first relation-discovery pass — and, as of the deepening campaign under issue #2, the evaluation of that pass. The original pass grouped project *summaries* by shared vocabulary. Mining pass 1 (2026-11-02) then mined the 24 *deepened* project pages (clusters A–D) at source level, requiring verbatim evidence from both sides of every relation. It preserves the original results as the historical record and maps them against the source-level pass's yield — a register of 26 concepts, 38 typed relations, and 19 single-source holds — stating which groupings survived scrutiny, which dissolved, and why. The six register entries so far written as pages are [[concepts/evaluator-circularity]], [[concepts/scoped-assurance]], [[concepts/improvement-lives-in-external-state]], [[concepts/ground-truth-fallibility]], [[concepts/protocol-relative-scores]], and [[concepts/information-content-dominance]].

## The original pass, as run

Method, in the original's own words: "Grouped the 34 imported project summaries by shared engineering concerns. A project can belong to multiple groups. These are candidate `related` links, **not** evidence of citations, shared code, equivalence, or empirical dependence."

Reported results:

- 8 architectural themes
- 49 candidate project-to-technique links
- 34 projects represented
- 1 synthesis signal

- [Verification and evidence](../techniques/verification-and-evidence.md): 7 associations
- [Adaptive recovery](../techniques/adaptive-recovery.md): 6 associations
- [Agent skills and memory](../techniques/agent-skills-and-memory.md): 6 associations
- [Multi-agent orchestration](../techniques/multi-agent-orchestration.md): 7 associations
- [Evaluation and simulation](../techniques/evaluation-and-simulation.md): 8 associations
- [Embodied and scientific agents](../techniques/embodied-and-scientific-agents.md): 6 associations
- [Secure agent operations](../techniques/secure-agent-operations.md): 7 associations
- [Generative interfaces](../techniques/generative-interfaces.md): 2 associations

The original closed with a promised next step: "Read primary papers and repository documentation, classify relation strength, identify contradictions, and add bidirectional links to project pages after verification." Mining pass 1 was that step, run over the deepened subset — and its yield differed in kind: almost no project-to-technique links, and instead the concepts and project-to-project relations the summary pass had no way to see.

## What source-level mining confirmed

Three of the eight themes re-emerged as evidence-backed structure — each time transformed.

**Agent skills and memory → confirmed most cleanly.** The theme's intuition, that these projects share something about stored state, survived as the register's strong entry [[concepts/improvement-lives-in-external-state]] (7 supporting pages) and its sibling family: accumulated-state-as-asset, persistent-memory-steers-later-behavior, and negative-transfer-of-experience. Source-level reading sharpened the grouping into a claim with bounds — improvement located in external state, a null result where stored text failed to steer, and a sign question about transfer — where the summary pass could only assert co-membership.

**Verification and evidence → confirmed, but inverted toward limits.** The theme re-emerged as [[concepts/scoped-assurance]] (strong, 8 pages), verification-is-load-bearing, and precommitment, plus one technique seed (gated-admission) resolved out of the concept track. But the surviving content is largely about verification's *warrant*: results holding only inside the scope exercised, gates that do not guarantee hold-out improvement. The summary pass grouped projects that *use* verification; the deepened pages show them sharing the problem of what a passed check actually proves.

**Evaluation and simulation → confirmed as the richest vein, with the simulation strand dropped.** The largest original bucket (8 associations) produced the register's strongest entry, [[concepts/evaluator-circularity]] (12 pages, 3 clusters), and a family of measurement concepts: [[concepts/ground-truth-fallibility]], [[concepts/protocol-relative-scores]], evaluator-identity-relativity, construct-validity-leakage, and claims-are-not-evidence. Again the direction inverted: evaluation survived not as a technique the projects apply but as the site of their shared failure modes. No concept about simulation as such emerged — that strand of the bucket found no two-sided evidence and quietly lapsed.

A cross-cutting observation: the strongest concept's 12 pages were scattered across several of the original buckets. The summary pass sorted projects by what they are *about*; the evidenced relations run along what their results *do*, and the two sortings do not coincide.

## What it corrected or dissolved

**Adaptive recovery → dissolved as a mechanism, its members redistributed.** The repair projects exist, but their evidenced cross-project content is not a shared recovery mechanism. What re-emerged from those pages is feedback *content* ([[concepts/information-content-dominance]]: rubric-aware feedback repairs, verdict-only feedback does not) and evaluator-dependence (evaluator-identity-relativity: whether a repair counts as good depends on who grades it). One repair candidate, aggregation-creates-solutions, sits in the single-source holds. The theme named a task the projects perform; the relations live in how their loops are fed and judged.

**Multi-agent orchestration → dissolved.** Seven associations produced no evidenced cross-project orchestration relation. The one deeply-related multi-agent page, evoteam, carries relations about external state and internal-judgment circularity; its orchestration-specific candidate, team-as-persistent-asset, is a single-source hold. Shared vocabulary — teams, roles, coordination — was not shared mechanism.

**Embodied and scientific agents → dissolved.** A domain bucket. Its pages (molrsi, hera, garden, bioagent among them) do carry evidenced relations, but they run through state, evaluation, and information content — nothing relates these projects *qua* embodiment or scientific setting. Domain is not a mechanism, and co-membership in a domain evidenced nothing.

**Secure agent operations → dissolved in pass 1.** The security pages' evidenced relations are evaluation relations: pre-crime-for-agents supports scoped assurance, and the memory-files study is the null result bounding [[concepts/improvement-lives-in-external-state]] and an exhibit inside claims-are-not-evidence. The security-specific candidates — trust-boundary-as-catalog, training-carries-the-gain, detection-horizon-collapse — are all single-source holds. Pass 1 neither confirms a security relation layer nor refutes one; the deepened security pages simply evidenced other things first.

**Generative interfaces → dissolved.** The smallest bucket (2 associations) had the least to survive on. A2UI's distinctive candidate, trust-boundary-as-catalog, is a hold; webanything's relations are evaluation-side (circularity, scoped assurance, protocol-relativity). Two summaries sharing an interface vocabulary never evidenced a shared mechanism.

The structural reason is the same in each dissolution: summary-level grouping detects *co-occurrence of vocabulary*; a relation survives source-level mining only when both pages' texts exhibit the same mechanism, failure mode, benchmark, or contradiction. Buckets built on topic, domain, or task vocabulary have no reason to coincide with buckets built on mechanism — and mostly, they didn't.

## What remains candidate

- The 49 candidate links themselves were never audited link-by-link. Pass 1 changed the unit of analysis rather than verifying the list; the links stand exactly as the original caveat left them — candidates, neither confirmed nor refuted individually.
- 19 concepts rest on a single page each (among them coupling-as-difficulty, abstention-as-first-class-verdict, downstream-priced-retrieval, execution-instability, defective-specifications) and are held, ungraded, for pass 2.
- Three multi-page candidates were deferred with reasons recorded in the register: comparator-construction-shapes-margins (single-cluster), capability-locus (a live two-page disagreement — hera against agenticds — that no verdict has earned), and validation-tier-gap (nearest to editorial judgment).
- Five cross-cluster relations are recorded as suspected — unverified, inferred from shared concept membership only.
- Mining pass 2, over the pages deepened since (clusters E–F), remains outstanding; it is the pass that re-adjudicates the holds and deferrals.

## Method comparison

The two passes mined different strata and their yields differ in kind, not just in count. The summary pass read 34 one-paragraph summaries and produced 8 themes and 49 candidate project-to-technique links: a map of the corpus's *vocabulary*, cheap and complete in coverage, with every link explicitly unevidenced. Pass 1 read 24 fully deepened pages and produced 26 concepts and 38 relations (15 shares-mechanism, 11 same-failure-mode, 7 supports, 4 contradicts, 1 shares-benchmark), each relation carrying verbatim evidence from both sides, plus the discipline to *not* assert: 19 holds, 3 deferrals, 5 suspected relations flagged rather than claimed, and 8 internal flags recorded against the miners' own work.

Stated precisely: **summaries mine vocabulary; deepened pages mine mechanisms.** A summary says what a project is about, in words its importers chose; a deepened page records what its evaluation actually did — who graded, what the gate selected on, where the gain lived — and relations exist at that level or not at all. The original pass's own caveat said its links were not evidence of empirical dependence; pass 1 is what the corpus looks like when empirical dependence is the admission test. The cost asymmetry is real and cuts the other way: the summary pass covered all 34 projects in one sitting, while pass 1's evidence standard restricted it to the 24 pages deepened by then. Coverage and warrant trade off; the KB now has one pass of each kind, and this page is where their disagreement is kept.

## Evidence status

This is the KB evaluating its own process. Both passes are internal artifacts: the original page (preserved above) and the mining pass 1 register, whose entries and evidence the mappings in this page are drawn from. The mappings are checkable — every concept named here is a register entry, the six written concept pages are linked, and the register's supporting quotations are the same ones the concept pages carry. No external source is cited because none is involved; the underlying project results remain author-reported, as recorded on their own pages. The verdicts are graded by the register's own discipline: a theme counts as confirmed only where a register entry rests on two-sided evidence from the theme's member pages, and as dissolved where pass 1's evidence from those pages runs along other lines entirely. Pass 2 may move items between sections of this page; until it runs, the holds and deferrals above are the honest state of the relation layer.
