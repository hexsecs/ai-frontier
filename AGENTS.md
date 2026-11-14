# Knowledge-base maintenance policy

This is an OpenShelf v1.7 KB. Read `kb.yaml`, `index.md`, and relevant pages before making changes.

1. Daily briefings are historical snapshots: preserve their factual record. Correct errors or perform owner-authorized editorial cleanup through a PR with a dated `log.md` entry. GitHub history records article changes; do not add change reports to article prose.
2. Deduplicate discoveries by canonical repo URL, DOI, arXiv identifier, or official project URL. Update existing project pages rather than creating title variants.
3. Each page must have `title` and a one-sentence `summary` (maximum 160 characters). New pages must get a newly generated UUID `uid`, plus `created`, `updated`, `type`, and `sources` when applicable. Preserve `uid` and `created` on revisions.
4. Every significant factual claim must be supported by a source; label vendor claims, author-reported benchmark results, independent replications, and speculation separately.
5. Link related pages using full OpenShelf page IDs, e.g. `[[techniques/verification]]`.
6. Keep `index.md` and category indexes navigable; all pages must be reachable from the root index.
7. Maintain the 70–80% core and 20–30% exploratory balance; avoid repeats unless evidence changed.
8. Never claim a source was inspected, a repository tested, or a benchmark reproduced unless it was.
9. Never execute untrusted repository code or publish secrets; use isolated environments for testing.
10. Update `log.md` for substantive maintenance; submit changes as PRs and run `openshelf lint .` before merge.

11. CI must reject missing or invalid content-page UUIDs, required dates, titles, summaries, types, or source metadata. Index navigation pages use lighter metadata; templates are excluded from validation.

## Knowledge ingestion and article writing

The KB is the knowledge. Write articles about systems, mechanisms, evidence, comparisons, limitations and experiments. Do not put paragraphs about ingestion, pages created, deduplication, audits, preference inference or agent activity in content pages. Record maintenance decisions in the PR description and substantive changes in `log.md`.

1. Before drafting, read `kb.yaml`, this file, `docs/FIGURES.md`, `automation/briefing-policy.yaml`, the latest briefing and relevant category indexes. Search canonical URLs, DOI/arXiv IDs, aliases and semantic matches before creating pages.
2. Resolve each finding to an existing canonical record or create an evidence-appropriate record. Update existing passages when evidence changes; do not append a new maintenance or synthesis section on every ingestion. Preserve UUIDs and creation dates, and promote depth only when substance warrants it.
3. Integrate knowledge into the text: link each selected discovery to its canonical page in its own section; link relevant techniques and comparisons where they explain the mechanism, evidence or limitation. Explain what the connection means. Do not impose a link quota or invent a relationship to satisfy a check.
4. Update canonical project, benchmark, case-study, workflow, domain, concept, technique, evaluation, signal and experiment pages where warranted. A project mention alone does not justify a new concept. Cross-project claims need independently supported evidence, counterexamples and explicit limits.
5. Put directional relationships in explanatory prose beside the relevant claim, with source provenance and certainty. Distinguish source-established relations, analyst comparisons and untested hypotheses. Reciprocal navigation is useful, but never reverse a directional claim merely to create a backlink. Frontmatter `related:` is navigation, not a replacement for explanation.
6. Archive the full substantive briefing, including source URLs, caveats, comparisons, verdicts, proposed tests and supported figures. Keep cross-project synthesis when it teaches something. Exclude process reports, search diaries, selection bookkeeping and preference commentary. Evidence limitations belong next to the affected claims.
7. Review the previous seven briefings and relevant canonical pages for changed evidence and cross-project implications. Incorporate warranted changes into existing knowledge passages; otherwise explain the no-change decision in the PR. Reprocessing the same evidence must not create duplicate pages or repeated paragraphs.
8. In the PR description, identify canonical changes, duplicates avoided, unresolved candidates, any justified no-change decisions and validation results. These are review evidence, not article content. Update navigation and `log.md` for substantive maintenance.
9. Run `python scripts/check_frontmatter.py`, `python scripts/check_briefing_mining.py`, `python scripts/check_links.py`, `openshelf lint .` and relevant renderer/chart tests. Structural validation cannot establish relationship truth: review the diff for source support, meaningful placement, changed evidence and absence of process prose. Enable auto-merge only after required checks pass; verify merge and Pages deployment separately.
10. Published briefings retain their factual record. Owner-authorized editorial cleanup may relocate existing analysis and remove process commentary; document it with a dated entry in `log.md` and the PR. Do not silently change historical findings, measurements or evidence status.
