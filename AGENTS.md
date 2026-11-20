# Knowledge-base maintenance policy

This is an OpenShelf v1.7 KB. Read `kb.yaml`, `index.md`, and relevant pages before making changes.

1. Daily briefings are historical snapshots: preserve their factual record. Correct errors or perform owner-authorized editorial cleanup through a PR that explains the correction or cleanup. GitHub history records article changes; do not add change reports to article prose.
2. Deduplicate discoveries by canonical repo URL, DOI, arXiv identifier, or official project URL. Update existing project pages rather than creating title variants.
3. Each page must have `title` and a one-sentence `summary` (maximum 160 characters). New pages must get a newly generated UUID `uid`, plus `created`, `updated`, `type`, and `sources` when applicable. Preserve `uid` and `created` on revisions.
4. Every significant factual claim must be supported by a source; label vendor claims, author-reported benchmark results, independent replications, and speculation separately.
5. Link related pages using full OpenShelf page IDs, e.g. `[[techniques/verification]]`.
6. Keep `index.md` and category indexes navigable; all pages must be reachable from the root index.
7. Maintain the 70–80% core and 20–30% exploratory balance; avoid repeats unless evidence changed.
8. Never claim a source was inspected, a repository tested, or a benchmark reproduced unless it was.
9. Never execute untrusted repository code or publish secrets; use isolated environments for testing.
10. Record substantive changes and validation results in PR descriptions; submit changes as PRs and run `openshelf lint .` before merge.

11. CI must reject missing or invalid content-page UUIDs, required dates, titles, summaries, types, or source metadata. Index navigation pages use lighter metadata; templates are excluded from validation.

## Knowledge ingestion and article writing

The KB is the knowledge. Write articles about systems, mechanisms, evidence, comparisons, limitations and experiments. Do not put paragraphs about ingestion, pages created, deduplication, audits, preference inference or agent activity in content pages. Record maintenance decisions, change explanations and validation results in the PR description. GitHub commits and PRs are the change record; do not create or maintain a separate repository changelog.

1. Before drafting, read `kb.yaml`, this file, `docs/FIGURES.md`, `automation/briefing-policy.yaml`, the latest briefing and relevant category indexes. Search canonical URLs, DOI/arXiv IDs, aliases and semantic matches before creating pages.
2. Resolve each finding to an existing canonical record or create an evidence-appropriate record. Update existing passages when evidence changes; do not append a new maintenance or synthesis section on every ingestion. Preserve UUIDs and creation dates, and promote depth only when substance warrants it.
3. Integrate knowledge into the text: link each selected discovery to its canonical page in its own section; link relevant techniques and comparisons where they explain the mechanism, evidence or limitation. Explain what the connection means. Do not impose a link quota or invent a relationship to satisfy a check.
4. Update canonical project, benchmark, case-study, workflow, domain, concept, technique, evaluation, signal and experiment pages where warranted. A project mention alone does not justify a new concept. Cross-project claims need independently supported evidence, counterexamples and explicit limits.
5. Put directional relationships in explanatory prose beside the relevant claim, with source provenance and certainty. Distinguish source-established relations, analyst comparisons and untested hypotheses. Reciprocal navigation is useful, but never reverse a directional claim merely to create a backlink. Frontmatter `related:` is navigation, not a replacement for explanation.
6. Archive the full substantive briefing, including source URLs, caveats, comparisons, verdicts, proposed tests and supported figures. Keep cross-project synthesis when it teaches something. Exclude process reports, search diaries, selection bookkeeping and preference commentary. Evidence limitations belong next to the affected claims.
7. Review the previous seven briefings and relevant canonical pages for changed evidence and cross-project implications. Incorporate warranted changes into existing knowledge passages; otherwise explain the no-change decision in the PR. Reprocessing the same evidence must not create duplicate pages or repeated paragraphs.
8. In the PR description, identify canonical changes, duplicates avoided, unresolved candidates, any justified no-change decisions and validation results. These are review evidence, not article content. Update navigation when needed.
9. Run `python scripts/check_frontmatter.py`, `python scripts/check_briefing_mining.py`, `python scripts/check_links.py`, `openshelf lint .` and relevant renderer/chart tests. Structural validation cannot establish relationship truth: review the diff for source support, meaningful placement, changed evidence and absence of process prose. Enable auto-merge only after required checks pass; verify merge and Pages deployment separately.
10. Published briefings retain their factual record. Owner-authorized editorial cleanup may relocate existing analysis and remove process commentary; document the scope and rationale in the PR. Do not silently change historical findings, measurements or evidence status.

## Source integrity and reader-facing prose

- Never invent a source, URL, quotation, author, release date, benchmark result, relationship or claim of inspection. Inspect the actual source before adding a factual claim; title/snippet discovery alone is insufficient. Existing citations are leads, not proof.
- Match source identity (title, project, authors and identifier) and verify the passage supporting each significant claim. Pin version-sensitive code references to a commit or release when possible. Cite internal canonical pages and external primary sources freely where they support the text.
- A successful HTTP response establishes availability, not truth or claim support. Retrieval failures establish neither fabrication nor falsity. Record identity checks, claim checks and unresolved access separately in PR evidence or `automation/audits/`; do not call a source check a replication.
- Distinguish author/vendor-reported findings, independently reproduced results, analyst interpretations and proposed experiments. “No independent replication is cited” is appropriate when that is all the available evidence establishes; do not assert that none exists without an adequate search.
- Articles must not describe their own edits, upgrades, depth campaigns, mining passes, promotion decisions or creation history. Write “Acquisition precedes evaluation,” not “This page corrects the earlier description of acquisition.” GitHub history and PRs document changes. Preserve subject-relevant evidence limitations and source citations.
- A scientific workflow, ingestion technique or evaluation of an agent's process may itself be an article subject. Discuss that subject normally; the prohibition concerns commentary about creating or maintaining this KB's articles.
- Before merge, run `python scripts/check_article_prose.py` as well as the existing checks. Its narrow textual checks catch known maintenance language; passing them does not establish complete editorial quality or factual accuracy.


## Organization and navigation

- Use `wiki/topics/` pages with the existing `index` type for question-led reading paths. Keep canonical IDs stable and link new content from a category index and a relevant reading path.
- Keep entity type, application domain and evidence status distinct. Use existing types and tags; do not introduce unvalidated frontmatter. State evidence status beside the affected claim when a page contains mixed evidence.
- Use full canonical IDs in `related:`. This metadata and generated backlinks provide navigation only; explain scientific relationships and provenance in article prose.
- A project describes one implementation; a technique explains a reusable mechanism; a concept states a bounded cross-project phenomenon; an evaluation compares evidence; an experiment specifies a test and its status. A presentation records a talk, video essay, lecture or recorded demo; its claims are the presenter's own unless independently corroborated. Briefings preserve dated discovery records.
- Run `python scripts/editorial_report.py` for nonblocking navigation suggestions. Suggestions are not link quotas, evidence judgments or grounds for automatic scientific backlinks.


## Full wiki ingestion

For each finding, resolve its own canonical entity by source identity; a comparison link alone is insufficient. Record in the PR the general concept, specific mechanism, synthesis pages reviewed and disposition: update-existing, create-new or no-change with a specific evidence-based reason. Project-only archiving is not full wiki ingestion. Verify declared substantive synthesis changes against the diff and report unresolved source identity/access separately.

Concept pages may teach sourced foundational distinctions as well as bounded cross-project phenomena. Definitions require authoritative support; empirical claims about benefit, transfer or prevalence retain the multiple-source and counterevidence requirements. Prefer substantive updates to existing syntheses over duplicate general overviews. A dated architecture diagram or frontier-signal paragraph does not replace living canonical integration.
