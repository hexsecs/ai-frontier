---
name: source-verification
description: Verify primary source identity and claim support before knowledge ingestion.
---

# source-verification

Resolve canonical URL, identifier, title, authors or project owner, date, and version. Read actual relevant passages, not snippets or HTTP status. For papers invoke arxiv-reading. For software use official implementation/release documentation and pin commit or tag where possible. Record source locator, inspected passage, attributed claim, evidence tier and limitations in PR evidence. Search archive and open PRs for URL/DOI/arXiv ID, aliases and semantic duplicates. Distinguish author claims, independent replication, analyst interpretation and proposed tests. If retrieval fails, use bounded alternate routes; retain previously verified evidence with its original scope and date if available. Never upgrade abstract-only evidence to full-text verification. Unresolved identity or unsupported claims stay out of factual articles; record exclusions in PR.
