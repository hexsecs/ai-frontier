# AI Frontier taxonomy review — 2026-11-09

## Decision proposed

Retain the eight current OpenShelf 1.7 types for backward compatibility while separating **entity kind** from **subject domain**, **evidence maturity**, and **relations**. The current `project` bucket is overloaded: it contains actual implementations, evaluation datasets and benchmark papers (e.g. TandemBench, MASBench, WeaveBench), observational reports (GitHub Octoverse), and operational case studies (AI-written software assurance). The `technique` index also contains subject domains such as embodied/scientific agents. The `experiments` index is empty despite numerous reproducible proposals embedded in briefings.

## Recommended new first-class types

| Type | Definition | Existing candidates | Why it matters |
|---|---|---|---|
| `benchmark` | A named task suite, dataset or evaluation protocol with a stable measurement definition | TandemBench, MASBench, ST-Bench, WeaveBench, CrossSWE, AgentSWE | Separate **what is measured** from an agent that implements a solution |
| `case-study` | Observational report, deployment incident, field experience or retrospective with explicit setting and limitations | AI-written software assurance case; GitHub Octoverse 2026 | Avoid presenting production anecdotes or observational metrics as product implementations |
| `workflow` | Runnable agent automation or integration recipe, with triggers, tools, trust boundaries and outputs | GitHub Agentic Workflows, Skills Reviewer, Code Simplifier, PR Sous Chef | Allows readers to find repeatable operational recipes distinct from standalone products |
| `domain` | Subject/application area used for discovery and grouping, not a mechanism | Scientific agents, robotics, coding agents, security, browser automation | Prevent a broad research field from masquerading as a single reusable technique |

**Do not immediately add** `actor`, `organization`, `dataset` or `paper`: their retrieval benefit is not yet demonstrated, and each would require entity migration and maintenance. Keep datasets inside benchmark records unless standalone datasets become common. A source paper is provenance, not necessarily a knowledge-base entity.

## Keep and sharpen current types

- `briefing`: immutable time-stamped source report, never the only home of reusable findings.
- `project`: a named implementation, library, framework, deployed system, or research prototype.
- `concept`: cross-project claim/phenomenon with supporting **and contradictory** evidence.
- `technique`: reusable method, algorithm or architecture that can be implemented by multiple projects; exclude subject-domain headings.
- `evaluation`: comparison, replication attempt, synthesis, methodological critique, or evidence audit **about** systems or benchmarks.
- `experiment`: concrete test protocol with inputs, controls, acceptance criteria, metrics, evidence tier and result status (proposed, run, independently replicated).
- `signal`: time-sensitive, falsifiable emerging trend; record freshness and confidence, retire or promote as evidence matures.
- `index`: navigation only.

## Orthogonal facets (not page types)

Record `domain` (coding, robotics, scientific research, browser, security), `maturity` (proposal, prototype, deployed, retired), `evidence_tier` (vendor claim, author evaluation, independently replicated, field observation), `artifact` (paper, repo, dataset, incident), and `status` (active, superseded, uncertain) as metadata/tags **after** verifying the OpenShelf 1.7 schema accepts the chosen fields. Until then, use existing tags or descriptive text; do not introduce unvalidated frontmatter.

## Ingestion and migration plan

1. **Completed in this branch:** Promote the 24 November 3–6 selections into canonical, source-attributed project records at evidence-appropriate `brief` depth, without modifying historical briefings. The November 7–9 fifteen project records already exist. This is a first-pass canonical ingestion, **not** independent deep-source verification.
2. Add source-verified depth in later passes. Do not automatically label a backfilled briefing section `deep`; preserve evidence qualifiers and link to the original dated report.
3. Add the four new types to `kb.yaml` only after schema validation, then reclassify the identified benchmark/case-study/workflow records without changing `uid`, `created`, URL slug or citations.
4. Extract a first-class `experiment` page for the cross-briefing hidden-acceptance and regression-preservation protocol. Link it from the synthesis, projects, and experiment index.
5. Require the ingestion checker to verify that every briefing finding resolves to an existing canonical page or a documented, justified exception; checking headings alone does not prove ingestion.
6. Add structured directional relation provenance only when supported by the source; preserve analyst hypotheses as such. Ensure reciprocal links and index reachability.

## Audit boundary

The October 30–November 2 reports are partially reconstructed and cannot be treated as complete source transcripts. The November 3–9 complete briefings contain 41 selected findings; 24 were not indexed as individual canonical records on `main` before this backfill. Some November 3–6 records may be related to older canonical entries; future source-level deduplication should merge true aliases rather than silently deleting pages.

## Recommended acceptance gates

- Every selected item has a canonical ID or documented no-change exception.
- All pages pass frontmatter, source, link and OpenShelf validation.
- No duplicate canonical URL, DOI or arXiv ID across records unless explicitly justified.
- No new type is introduced without schema validation and migration tests.
- A synthesis page must include counterexamples and experiments, not just a list of links.
