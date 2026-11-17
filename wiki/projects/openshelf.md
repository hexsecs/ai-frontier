---
uid: 9af54ee7-7989-4b35-8db1-4f4dcc1b0e3a
depth: full
title: "OpenShelf"
summary: "OpenShelf is an open standard for composable Markdown knowledge bases: a kb.yaml manifest, L0–L3 progressive context, and pinned cross-KB composition."
type: project
created: 2026-11-17
updated: 2026-11-17
related: [openwiki, open-knowledge-format, llm-wiki, context-as-infrastructure]
sources:
  - url: https://github.com/OpenNorms/openshelf
    retrieved: 2026-11-17
  - url: https://opennorms.github.io/openshelf/
    retrieved: 2026-11-17
  - url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
    retrieved: 2026-11-17
---

# OpenShelf

## What it is

OpenShelf is an open standard for the LLM Wiki pattern — the pattern Andrej Karpathy's April 2026 gist describes, in which an LLM builds and maintains a persistent, interlinked Markdown wiki from raw sources so knowledge is compiled once and kept current instead of re-derived on every query. Where other projects in this cluster build tools that *produce* a wiki, OpenShelf standardizes only what is needed to *connect* knowledge bases to each other and to a project, and leaves everything else — layout, page types, naming, workflow — to each KB's owner.

The specification is at v1.7 and describes itself as stable; the repository (`OpenNorms/openshelf`, created 2026-10-28) holds the spec, JSON Schemas, a Python reference CLI, examples, and a composite GitHub Action. Code is MIT-licensed; the specification and examples are CC-BY-4.0. Knowledge bases created with it carry their own licenses (`openshelf init` defaults a new KB to CC-BY-4.0).

A disclosure belongs at the top of this page rather than in its evidence section: **this knowledge base is itself an OpenShelf KB, and its maintainer is also a maintainer of OpenShelf.** The page is therefore a self-description by an interested party, held to this corpus's usual rule — mechanism from primary sources, claims labelled, limitations stated — with the conflict named rather than smoothed over. The adoption evidence below is reported with that conflict in view: OpenShelf's public footprint is small (1 GitHub star, 52 commits as of 2026-11-17), and its real deployment is a network of KBs maintained by its own authors and collaborators, including this one. Nothing in the sources constitutes independent adoption at scale.

## Mechanism

The contract is small and strict; the conventions around it are explicitly optional.

**Manifest.** A KB is a directory with a `kb.yaml` at its root — the only fixed path in the spec. It declares the spec version (`openshelf: "1.7"`), a human `id`, a `title`, a one-paragraph `description`, and optionally where pages, index, and sources live (`layout`), custom page types, a profile, a license, maintainers, visibility (`public`, `internal`, or `private`), a published `url`, and the ids of KBs it links into (`depends`). Fields a consumer does not understand must be ignored.

**Identity.** A KB should carry a `uid`: a UUID minted once at creation and never changed, which identifies the KB across renames and repository moves (a mirror keeps the `uid`; a diverging fork must mint a fresh one). Pages have the same two-level identity: a path-derived id used in links, and a frontmatter `uid` minted once that survives renames and moves within and between KBs. Tooling, not the maintaining LLM, is expected to mint uids — the spec's stated reason is that a UUID an LLM writes from memory is not reliably random.

**Pages.** A page is a Markdown file with YAML frontmatter. Only two fields are required: `title`, and `summary` — one sentence, at most 160 characters, the text indexes and search show. Pages should also carry `uid`, `type` (free text; a KB may declare custom types in `kb.yaml`, including types with required fields that lint then enforces), `created`, `updated`, a `depth`, and `sources` (each a URL or a KB-relative path, optionally with a content hash lint must verify). Unknown fields must be ignored by consumers. Depth is a four-step sizing ladder that prices a page's context cost before it is loaded: `stub` and `brief` at roughly 750 tokens, `full` at 2,500, `deep` at 6,000, with promotion treated as an editorial decision rather than a consequence of accumulated text.

**Progressive context.** Every KB exposes the same four tiers: **L0**, the description (at most 300 characters, always loaded for every connected KB); **L1**, the index (loaded when a task touches the KB's scope); **L2**, individual pages (loaded when relevant); **L3**, raw sources (loaded only to verify or extend a page). Composition scales because connecting a KB costs one L0 block in a project's always-on context, regardless of the KB's size; depth is paid per task and per page.

**Links.** Inside a KB, pages may use Markdown links or Obsidian wikilinks, and consumers must resolve both. Links into another KB use `kb://<kb-id>/<page-id>` (with a `[[<kb-id>:<page-id>]]` wikilink shorthand valid when the target is declared in `depends`). A cross-KB link resolves when that KB is connected, falls back to the target's published `url` when known, and otherwise renders as plain text — so a KB can reference KBs it does not vendor. A moved page may leave a stub carrying `redirect: <new-id>`, which consumers must follow.

**Composition.** A project declares its KBs in `.openshelf/kbs.yaml`, each with a source, a ref, and a `use` hint saying when that KB is relevant. `openshelf sync` fetches each KB, pins its exact commit and `uid` in `.openshelf/kbs.lock`, and writes `.openshelf/context.md` containing one L0 block per KB; the project's `AGENTS.md` or `CLAUDE.md` points at that file. Sync *fails* if a different KB answers to a familiar `id` (a substitution), if two connected KBs share a `uid`, or if an `id` changed while the `uid` did not (diagnosed as a rename, to be adopted deliberately). Connected KBs are read-only to the project; knowledge gained while working is contributed back through each KB's own maintenance process in its own repository. Visibility is enforced at this boundary: a non-public KB's L0 text, `use` hint, and paths are never written into the committed `context.md` — they go to a gitignored local context file, or the connection is refused.

**Relations without editing sources.** A composing project may assert how pages in different KBs relate in a project-owned overlay (`.openshelf/relations.yaml`), without modifying either KB. Overlay types are `related` and `same-as` (symmetric), `broader`/`narrower` (inverses), and `supersedes` (directional). An overlay relation remains visibly the composition's claim, not the KB's; `same-as` records that two pages describe the same entity *for this composed view* and never merges them. If a KB later adopts a relation into its own pages, the overlay entry is removed, so a relation lives in exactly one layer at a time.

**Tooling.** The `openshelf` CLI (Python 3.10+) initializes KBs, lints them against the spec, generates and verifies raw-source checksum manifests, mints uids, and performs `add`/`sync` for compositions. `openshelf mcp` serves a project's connected KBs to any MCP client over stdio, one tier at a time — `list_kbs` (L0), `read_index` (L1), `read_page` (L2), `read_source` (L3), and `search` — read-only, re-reading files on every call so edits appear without a restart. A composite GitHub Action lints KB repositories in CI. One profile is defined: `awesome`, which makes each entry of an awesome list a sourced, cross-linked page while the index still reads as a classic awesome list — the mechanism behind the registry of KBs built from awesome lists (`hexsecs/awesome-kb` and its topic KBs).

## Evidence

- **Existence and conformance (primary sources):** the v1.7 specification, its JSON Schemas, and the reference CLI are public and were read in full for this page. The spec's compatibility contract (§10) ties tool and spec versions together: tool `X.Y.Z` fully implements spec `X.Y`, and a KB declaring an earlier `X.Y` works with any later tool of the same major version.
- **Deployment (maintainer-reported, conflict disclosed above):** OpenShelf KBs in active maintenance by the standard's own network include this knowledge base, a registry KB and topic KBs built from awesome lists (embedded security, automotive security, with security and AI/LLM-agents KBs scaffolded), a multi-agent security-research project's wiki, a target-assessment KB, and a private business-ideas KB. These demonstrate the composition machinery operating across public, internal, and private visibility tiers; they are not independent adoption, and no deployment outside the authors' network is recorded in the sources.
- **Public adoption signals:** 1 GitHub star and 0 forks as of 2026-11-17 — negligible as an attention measure, recorded because this corpus records such measures for every project rather than omitting an unflattering one.
- **No effect measurements:** nothing in the sources measures whether OpenShelf composition improves agent task performance, retrieval precision, or context efficiency against a baseline (for example, connecting the same KBs as plain directories, or loading L1 eagerly). The progressive-context design is an argument from context economics, not a measured result.

## Limitations

- **Adoption is the open question.** The standard's machinery — substitution detection, rename diagnosis, relation overlays — is engineered for a world of many independently owned KBs composing into many projects. Its actual world, per the sources, is one maintainer network. Design weight spent on multi-party failure modes is unjustified by evidence until unaffiliated KBs compose in practice; the simpler parts of the contract (manifest, summary, tiers) are the parts any single KB uses daily.
- **The contract is enforced by lint, not by construction.** A KB that stops running `openshelf lint` drifts silently: summaries go stale, uids can be duplicated by copy-paste, indexes omit pages. The spec's minting rule (tools, not LLMs, mint uids) exists because the failure was anticipated; nothing prevents it in an unlinted KB.
- **Summaries are a single point of failure.** L0 and the index's summary lines are what an agent uses to decide relevance. A wrong or stale 160-character summary hides a page as effectively as deleting it, and the format carries no mechanism — no equivalent of OpenWiki's evidence recheck — for noticing that a summary no longer matches its page. Freshness of the *summary layer* is a maintenance discipline, not a format guarantee.
- **No freshness or trust fields.** OpenShelf has `created`/`updated` dates and source citations, but nothing corresponding to OKF v0.2's `verified`, `status`, or `stale_after` (see [[projects/open-knowledge-format]]): a consumer cannot tell from frontmatter whether a page was ever checked, or when it should be distrusted. In this corpus's terms, the standard prices context (depth, tiers) more carefully than warrant.
- **Composition is read-only by design.** The contribute-back rule keeps ownership clean, but it means a project that learns something cannot annotate the KB it learned from; corrections travel through the KB's own process and latency. Relation overlays are the one write a composer gets, and they are deliberately not visible when the KB is rendered standalone.

## Competing approaches

- **Open Knowledge Format ([[projects/open-knowledge-format]]).** The parallel standard, from Google Cloud. OKF standardizes the single bundle with the thinnest possible contract (only `type` required) and, in v0.2, adds per-concept provenance, verification, and lifecycle fields. OpenShelf standardizes composition across KBs — identity, pinning, cross-KB addressing, visibility, overlays — and requires more of each page (title plus summary). A bundle can in principle be described by both: adding a `kb.yaml` and per-page `summary`/`uid` fields to an OKF bundle (for example, one produced by OpenWiki) would make it composable as an OpenShelf KB while its OKF fields ride along as ignored extensions, and OpenShelf pages' extra fields are equally preservable by OKF consumers. No tool performs this mapping today; the compatibility is a property of the two specs' ignore-unknown-fields rules, not an implemented bridge.
- **OpenWiki workspaces ([[projects/openwiki]]).** OpenWiki's `openwiki link` groups several repositories' wikis into a named workspace with cross-wiki search — composition, but of wikis one tool generated, registered privately under `~/.openwiki`, without pinned revisions, stable cross-KB identity, or visibility rules. It composes a tool's own outputs; OpenShelf composes anyone's KBs, including hand-written ones.
- **Git submodules, vendoring, and monorepos.** The incumbent ways to combine knowledge bases: copy the files in, pin by submodule, or merge the repositories. All three dissolve KB ownership and identity — a vendored copy that diverges is indistinguishable from the original — which is precisely the failure OpenShelf's `uid`-checked sync is built to refuse.
- **A single wiki per project (the gist's default).** Karpathy's pattern as usually practiced: one wiki, one owner, no composition question at all. For a single project this remains the right scope; OpenShelf's contract only earns its cost when a second KB, a second owner, or a second project appears.

## Implications

OpenShelf is this corpus's clearest instance of a standard written *by* agent-maintained practice rather than for it: its load-bearing ideas — progressive context pricing, identity that survives renames, refusal to silently publish a private KB, relations that live in exactly one layer — are each answers to a failure that only appears when agents maintain many KBs over time (context blowup, substitution, leakage, duplicated relations). Whether the answers generalize beyond the practice that produced them is the adoption question above. For this knowledge base specifically, the standard is also infrastructure: the KB's own index, depth ladder, and lint gates are OpenShelf mechanisms, so the format's limitations recorded here (summary staleness, no trust fields) are live properties of the corpus the reader is currently using.

## Reproducible experiment

The composition claim is testable and **has not been run**: connect the same set of KBs to a project two ways — as an OpenShelf composition (L0 always-on, deeper tiers on demand) and as plain directories the agent may browse freely — and run a fixed task suite spanning tasks that need one KB, several, and none. Measure total context tokens consumed, task success, and wrong-KB retrieval errors (answers drawn from an irrelevant KB's pages). The prediction the design makes is specific: equal success at materially lower always-on token cost, with wrong-KB errors concentrated in the plain-directory arm. A second, cheaper test exercises the identity machinery: rename a connected KB, substitute a different KB under a familiar `id`, and fork a KB without re-minting its `uid`; sync must diagnose each distinctly. That half is deterministic and could be run against the reference CLI today.

## Evidence status

Specification and maintainer documentation, with a disclosed conflict of interest: the KB maintaining this page is an OpenShelf KB and shares a maintainer with the standard. Mechanism descriptions are from the v1.7 specification and README, read in full on 2026-11-17, and are a reliable basis for what the standard requires. Deployment claims are maintainer-reported and limited to the authors' own network; public adoption signals are minimal and are reported as such. No independent evaluation, no unaffiliated adoption study, and no measurement of composition's effect on agent performance exists in the sources. Nothing was executed for this page beyond reading the primary texts and this KB's own lint tooling, which runs the reference implementation.

## Related pages

- [[projects/openwiki]] — a wiki generator whose OKF output could be made composable under this standard.
- [[projects/open-knowledge-format]] — the parallel bundle standard; the two are compared field by field above.
- [[projects/llm-wiki]] — a single-vault desktop implementation; composition is out of its scope by design.
- [[projects/context-as-infrastructure]] — compiled context inside one system; OpenShelf is the same compile-once instinct at the inter-KB boundary.
- [[techniques/agent-skills-and-memory]] — persistent external state for one agent; OpenShelf is persistent external state addressed across projects.

