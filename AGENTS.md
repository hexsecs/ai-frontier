# Knowledge-base maintenance policy

This is an OpenShelf v1.7 KB. Read `kb.yaml`, `index.md`, and relevant pages before making changes.

1. Daily briefings are historical snapshots: do not silently rewrite published briefings. Correct errors with a dated correction note or PR.
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

## Mandatory briefing-to-knowledge ingestion

Every new dated briefing is BOTH a full-fidelity historical report and a knowledge-mining transaction. A briefing-only PR is incomplete unless a documented zero-change mining audit justifies it.

1. Before writing, inspect `kb.yaml`, this file, `docs/FIGURES.md`, `automation/briefing-policy.yaml`, the latest briefing, and the canonical project, concept, technique, signal, experiment and evaluation indexes.
2. Archive the COMPLETE user-visible report at `wiki/briefings/YYYY/MM/YYYY-MM-DD.md`, including original primary-source URLs, caveats, comparisons, verdicts, experiments, frontier signal, and supported portable figures. Never replace it with a recap. Historical snapshots are immutable; same-day revisions must reconcile the existing file without silently discarding material.
3. Mine EVERY selected finding for projects, concepts, techniques, benchmarks, evidence, experiments, and directional relationships. For each candidate, search existing pages by canonical URL/DOI/arXiv ID, title, alias, and semantic meaning. Prefer updating a canonical page to creating a duplicate.
4. Update or create canonical `wiki/projects/` pages and relevant `wiki/concepts/`, `wiki/techniques/`, `wiki/evaluations/`, `wiki/signals/` or `wiki/experiments/` pages when the evidence warrants it. Do not create a concept merely because one project mentions it; distinguish independently supported cross-project phenomena from single-project techniques.
5. Record directional, evidence-backed relations (e.g. `implements`, `extends`, `evaluates`, `compares_with`, `depends_on`, `mitigates`, `contradicts`) in a **Knowledge mining** section of the dated briefing, with canonical wiki links and source URLs. Separate verified relationships from analyst hypotheses; include counterexamples, negative findings, and uncertainty. Add reciprocal `related:` links to relevant pages using existing OpenShelf conventions.
6. Preserve existing `uid` and `created` on edits. New content pages need a fresh UUID, required OpenShelf 1.7 fields, an evidence-appropriate `depth`, and real `sources`. Promote depth based on substance, never mention count. Update category indexes, root navigation if necessary, and `log.md`.
7. Include a **Knowledge mining** section in each new briefing with the exact headings `### Canonical updates`, `### Relations and evidence`, and `### Mining audit`. Name the pages created/updated, relation additions, duplicates avoided, unresolved candidates, and any justified no-change decisions. This section is part of the full-fidelity report and must be archived.
8. Before opening a PR, run `python scripts/check_frontmatter.py`, `python scripts/check_briefing_mining.py`, `openshelf lint .`, and relevant chart-conversion tests. Do not bypass failures. Enable GitHub auto-merge only when required checks pass; verify merge and Pages deployment separately. If access/checks fail, report the exact incomplete state.
9. Do not invent source evidence, inferred feedback, relation certainty, benchmark data, or claims of independent reproduction. No speculative relation is promoted to fact.
