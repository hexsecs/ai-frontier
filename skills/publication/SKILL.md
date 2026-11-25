---
name: publication
description: Publish reviewable ingestion PRs with current-base reconciliation and required validation.
---

# publication

Inspect current main and open PR queue. Avoid concurrent competing synthesis changes; serialize publication or use explicitly dependent drafts. Verify merge base before writes; if diverged, perform three-way reconciliation preserving both sides, using a merge commit without force push where supported. Use atomic commits and guarded ref updates; inspect resulting diff. Run check_frontmatter.py, check_article_prose.py, check_briefing_mining.py, check_links.py, openshelf lint ., renderer/chart/navigation tests and site build/rendered links; use editorial_report.py as advisory. Never claim local checks were executed if unavailable. Record per-finding evidence and validation in PR, address review findings, verify latest head checks, enable authorized auto-merge only within existing protections. Verify actual merge and Pages deployment; distinguish pending from complete. If unstable or checks missing, inspect triggers and report exact state, invoke recovery next run.

Require a trusted current-head Codex review receipt and zero unresolved review threads before merging. Request explicit review using @codex review; a thumbs-up alone is not a receipt. If main advances, synchronize and re-review. Require the review-policy status when installed; until branch protection is configured, do not treat the workflow as mandatory enforcement. After resolving threads, rerun the review gate and verify the latest head. Never bypass a missing receipt.
