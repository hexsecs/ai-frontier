---
uid: e24ace71-ea6a-447d-a0d8-6a2fb8c987fe
depth: full
title: "Open Knowledge Format"
summary: "Google's Open Knowledge Format packages knowledge as Markdown bundles with YAML frontmatter; v0.2 adds provenance, verification, and freshness fields."
type: project
created: 2026-11-17
updated: 2026-11-17
related: [openwiki, openshelf, llm-wiki]
sources:
  - url: https://github.com/GoogleCloudPlatform/open-knowledge-format
    retrieved: 2026-11-17
  - url: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
    retrieved: 2026-11-17
  - url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
    retrieved: 2026-11-17
---

# Open Knowledge Format

## What it is

The Open Knowledge Format (OKF) is an open specification from Google Cloud for representing knowledge — the metadata, context, and curated insight surrounding data and systems — as a directory of Markdown files with YAML frontmatter. It was published on 2026-06-12 by Sam McVeety (Tech Lead, Data Analytics) and Amir Hormati (Tech Lead, BigQuery) as v0.1; v0.2 followed on 2026-07-24. The spec is Apache-2.0 licensed, vendor-neutral by declaration, and deliberately minimal: there is no schema registry, no central authority, and no required tooling or SDK. In the spec's own terms, if you can `cat` a file you can read OKF, and if you can `git clone` a repository you can ship it.

OKF explicitly formalizes the LLM Wiki pattern from Andrej Karpathy's April 2026 gist: knowledge compiled once by an agent into interlinked pages, then maintained, rather than re-derived from raw sources at query time. Where the gist is a methodology, OKF is the interchange layer for its output — the thing that lets a bundle authored by one agent or organization be consumed by another. Google's Knowledge Catalog (formerly Dataplex) ingests OKF bundles as one runtime consumer; the format itself prescribes no storage, serving, or query infrastructure. The spec originally lived inside the `GoogleCloudPlatform/knowledge-catalog` repository and moved in August 2026 to its own repository, `GoogleCloudPlatform/open-knowledge-format`, with the original location frozen as a snapshot.

This page treats OKF as a project in this corpus's sense — a canonical artifact with a mechanism and an evidence record — while noting it is a specification, not a system: it generates nothing and maintains nothing. Everything about its effect on agent behavior is mediated by tools that produce or consume it, principally LangChain's OpenWiki (see [[projects/openwiki]]), which emits OKF v0.2 bundles.

## Mechanism

The unit of distribution is a **bundle**: a directory tree of Markdown files, shipped as a git repository, an archive, or a subdirectory of a larger tree. Each non-reserved file is a **concept** — one unit of knowledge such as a table, a metric, an API, or a playbook — and a concept's identifier is its path within the bundle without the `.md` suffix. Two filenames are reserved at every level: `index.md` (the bundle's catalog; the root index declares `okf_version: "0.2"`) and `log.md` (its chronological record). Relationships between concepts are expressed as ordinary Markdown links.

Frontmatter conformance is intentionally thin. Exactly one field is required: `type`, a short producer-defined string naming the kind of concept. Recommended fields are `title`, `description` (a one-line summary), `resource` (a URI for the real asset the concept describes), and `tags`. Consumers must tolerate unknown types and preserve unknown fields, so producers can extend frontmatter without breaking the format.

Version 0.2's additions answer the trust questions that arise once agents write most of a corpus. They are all optional, and a v0.1 bundle remains valid:

- **Provenance — `sources`:** the materials a concept derives from, each with a resource reference and optional author, usage count, and last-modified data.
- **Trust — `generated` and `verified`:** `generated: {by, at}` records who or what wrote the content and when it last changed (replacing v0.1's `timestamp` field, one of v0.2's two breaking changes); `verified` records who confirmed it. Consumers derive a trust tier from `verified`: unverified (absent), machine-confirmed, or human-reviewed (at least one `human:<id>` actor).
- **Lifecycle — `status` and `stale_after`:** `status` is `draft`, `stable`, or `deprecated` (absent means stable); `stale_after` is an absolute instant on or after which the concept is stale.
- **Attested Computation:** a concept type for values that must be produced a sanctioned way, carrying a runtime (for example BigQuery, dbt, or Python), typed parameters, an executor that returns a receipt, and an attester — deterministic code with no LLM involvement — that checks the receipt.

Conformance (§11) is three rules: every non-reserved Markdown file has parseable YAML frontmatter; every frontmatter block has a non-empty `type`; and every `index.md` and `log.md` follows the specified structure. Since August 2026, all timestamps in the spec are ISO 8601 datetimes with an explicit UTC offset. The specification roughly doubled between versions, from about 2,000 words (451 lines) in v0.1 to about 5,200 words (roughly 1,000 lines) in v0.2, with the growth concentrated in the trust and lifecycle machinery.

The Google Cloud integration illustrates the intended consumption path. Documented in August 2026, it maps a bundle into Knowledge Catalog by registering an EntryGroup for the bundle, an EntryType for its concepts, and an AspectType carrying the structured trust fields; a Metadata-as-Code CLI (`kcmd`) reads the bundle from git and writes one catalog entry per concept, so concepts inherit the catalog's identity and access controls. A worked example turns a nine-concept bundle into seventeen pushed entries. This is one consumer's mapping, not part of the format — the spec defines no discovery mechanism, no HTTP path, and no way for a system to find bundles on the open web.

## Evidence

OKF is a specification, so its evidence record is adoption and implementation rather than measured effect. All items below are **author-reported or project-reported** unless noted.

- **Producer adoption:** LangChain's OpenWiki — 17,990 stars as of 2026-11-17 — emits OKF v0.2 bundles in both its modes and maintains the v0.2 provenance and verification fields from its Grounded Claims pipeline (see [[projects/openwiki]]). This is the format's most visible independent producer.
- **Platform consumption:** Google Cloud's Knowledge Catalog ingests OKF bundles, with the EntryGroup/EntryType/AspectType mapping documented by Google in August 2026, including a worked nine-concept example.
- **Ecosystem tooling:** third-party validators and explainers exist (for example IWE's OKF validation), and the awesome-llm-wiki tracking list catalogs the wider pattern ecosystem OKF sits in. These indicate implementer attention, not measured benefit.
- **No effect measurements:** no source inspected for this page measures whether OKF-formatted knowledge improves agent task performance, answer accuracy, or maintenance cost against any baseline — against RAG over the same sources, against a proprietary format, or against unstructured Markdown. The format's premise (compiled knowledge beats re-derivation) is inherited from the Karpathy gist, which is a methodology essay, not an evaluation.

## Limitations

- **Minimalism is the mechanism and the gap.** With `type` as the only required field, two fully conformant bundles can share almost no structure beyond filenames. Interoperability is therefore shallow by design: a consumer can parse any bundle, but cannot assume summaries exist, sources are cited, or verification fields are populated — the trust fields that motivate v0.2 are exactly the ones a producer may omit.
- **No typed relations.** Links are untyped Markdown links. Proposals for typed edges were raised by contributors after v0.2 but are not in the specification, so a bundle cannot express that one concept supersedes, contradicts, or derives from another except in prose.
- **Trust fields are assertions, not checks.** `verified` records that someone or something claims to have confirmed a concept; the format defines the tiers but no verification procedure, and nothing in conformance requires the claim to be true. The Attested Computation type is the exception — it binds a value to a deterministic attester — and it covers computed values only.
- **Freshness is declared, not detected.** `stale_after` is an author-set deadline. Nothing in the format notices when a concept's subject changes before that date; staleness detection belongs to producers (OpenWiki's Claims recheck is one such mechanism, and it lives outside the format).
- **Governance is single-vendor.** The spec is Apache-2.0 and described as vendor-neutral, but it is authored and controlled by Google Cloud, with no standards-body home — unlike, for comparison, the agent protocols that sit under the Linux Foundation. Two breaking renames in the first minor version bump (`timestamp` → `generated.at`; body citations → `sources`) show the format is still moving.
- **Discovery is unsolved.** The spec deliberately defines no discovery file or registry; how an agent finds relevant bundles beyond being handed one is left to each ecosystem (Google's answer is Knowledge Catalog; OpenShelf's is its registry and composition files — see [[projects/openshelf]]).

## Competing approaches

- **OpenShelf ([[projects/openshelf]]).** The closest parallel: another open, Markdown-plus-frontmatter standard for agent knowledge, also descended from the same Karpathy gist. The design centers differ. OKF standardizes the *bundle* — one self-contained unit, minimally specified, with trust metadata on each concept. OpenShelf standardizes *composition* — many independently owned KBs connected to a project through a manifest (`kb.yaml`), stable identity (`uid` minted once per KB and page), cross-KB addressing (`kb://` links), pinned revisions (`kbs.lock`), and progressive context tiers (L0–L3) that price each KB's context cost. OpenShelf requires more of a page (`title` plus a ≤160-character `summary`) where OKF requires only `type`; OKF has lifecycle and attestation fields OpenShelf lacks; OpenShelf has identity and composition machinery OKF deliberately omits. Neither format reads the other natively today.
- **Proprietary catalog metadata (Knowledge Catalog native entries, Dataplex aspects).** The incumbent enterprise approach OKF is designed to feed rather than replace: knowledge as entries in a managed metadata service with IAM, rather than as files in git. OKF's bet is that the file form is the portable interchange and the catalog is one consumer among several.
- **`llms.txt` and `AGENTS.md` conventions.** Adjacent single-file conventions: `llms.txt` points models at a site's important pages; `AGENTS.md` instructs an agent working in a repository. Both are pointers or instructions for a consumer already in place; neither packages knowledge itself into addressable, provenance-carrying units.
- **Plain RAG corpora.** The baseline: documents chunked into a vector index, knowledge re-derived per query. OKF bundles can be indexed the same way — the format does not forbid it — but its premise is that the compiled, linked, human-readable layer is the asset, and retrieval is a fallback over it rather than the primary representation.

## Implications

OKF's significance for this corpus is less its field list than its provenance: a hyperscaler's data organization looked at the agent-knowledge problem and standardized *files in git* — the same substrate as this knowledge base — rather than a service API. Its v0.2 trajectory is also diagnostic: within six weeks, real use pushed the format from "Markdown with a type field" toward trust, freshness, and attestation, which is independent evidence that the binding constraint on agent-maintained knowledge is not expression but warrant — the same constraint this corpus's concept layer records as [[concepts/scoped-assurance]] and [[concepts/evaluator-circularity]]. The open question the format poses to its ecosystem is whether optional trust fields get populated in practice; a format whose trust layer is optional will be populated exactly where a producer (like OpenWiki) makes population automatic, and left empty where it is manual.

## Reproducible experiment

A format has no behavior to reproduce, so the decisive test is comparative and **has not been run**: take one knowledge domain with a fixed question set whose answers are known; represent it three ways — an OKF bundle with full v0.2 trust fields, the same bundle with trust fields stripped, and a RAG index over the same source documents — and give agents tasks that include questions whose underlying facts were changed after bundle creation. Measure answer accuracy, citation correctness, and stale-fact error rate (answers repeating the pre-change fact). The stripped-bundle arm isolates the trust fields' contribution: if agents do not actually use `verified` and `stale_after` to discount stale or unverified concepts, v0.2's additions are documentation, not mechanism. No arm of this protocol appears in the sources.

## Evidence status

Specification and vendor documentation only. This page is built from the OKF v0.2 specification and its repositories (read 2026-11-17), Google Cloud's published integration documentation as reported in August 2026 coverage, and the Karpathy gist the spec cites. Authorship, dates, and field definitions are spec facts. Adoption items are project-reported (OpenWiki's OKF emission is from OpenWiki's own documentation; the Knowledge Catalog mapping is Google's). No measurement of OKF's effect on any agent task exists in the sources, and nothing here was independently verified by the KB maintainers beyond reading the primary texts.

## Related pages

- [[projects/openwiki]] — OKF's most visible producer; its Claims pipeline populates the trust fields.
- [[projects/openshelf]] — the parallel standard centered on composition rather than the bundle.
- [[projects/llm-wiki]] — the desktop implementation of the shared pattern, using its own frontmatter conventions rather than OKF.
- [[projects/context-as-infrastructure]] — a compiled-context system whose claim–evidence discipline anticipates OKF's provenance fields.

