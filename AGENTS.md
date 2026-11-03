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
