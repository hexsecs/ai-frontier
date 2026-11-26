---
name: publication
description: Publish reviewable ingestion PRs with current-base reconciliation and required validation.
---

# publication

Inspect current main and open PR queue. Avoid concurrent competing synthesis changes; serialize publication or use explicitly dependent drafts. Verify merge base before writes; if diverged, perform three-way reconciliation preserving both sides, using a merge commit without force push where supported. Use atomic commits and guarded ref updates; inspect resulting diff. Run check_frontmatter.py, check_article_prose.py, check_briefing_mining.py, check_links.py, openshelf lint ., renderer/chart/navigation tests and site build/rendered links; use editorial_report.py as advisory. Never claim local checks were executed if unavailable. Record per-finding evidence and validation in PR, address review findings, verify latest head checks, do not enable native auto-merge; use fresh PR-specific authorization before any controlled merge. Verify actual merge and Pages deployment; distinguish pending from complete. If unstable or checks missing, inspect triggers and report exact state, invoke recovery next run.

Require a trusted current-head Codex review receipt and zero unresolved review threads before merging. Request explicit review using @codex review. A thumbs-up alone is insufficient. If main advances, synchronize and re-review.

Deployment prerequisites include native required conversation resolution, stale approval dismissal and strict, source-bound validation checks, with bypass restricted. Review authorization is evaluated live. A commit check can retain success during a GitHub API outage or after a review changes, so the review policy does not publish a commit check. Keep unattended merging disabled until live enforcement is verified.

Pre-merge authorization: run `python -m scripts.premerge_authorize PR EXPECTED_FULL_HEAD_SHA` from trusted main with repository credentials. It independently reads current PR, review receipts, threads, main and native required checks twice; errors or changed head/base deny authorization. The result is a snapshot, not a reusable token. This initial controller is read-only; do not enable unattended merging. A later controlled merge must use expected-head matching and verified native protections; review-state races remain possible between API reads and merge.
