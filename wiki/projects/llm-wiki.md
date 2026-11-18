---
uid: a787f577-3d0d-4201-ac62-8b6b84238767
depth: full
title: "LLM Wiki"
summary: "LLM Wiki is a desktop app that compiles documents into a persistent, graph-linked wiki, extending Karpathy's pattern with review and deep research."
type: project
created: 2026-11-17
updated: 2026-11-17
related: [openwiki, openshelf, open-knowledge-format, context-as-infrastructure]
sources:
  - url: https://github.com/nashsu/llm_wiki
    retrieved: 2026-11-17
  - url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
    retrieved: 2026-11-17
---

# LLM Wiki

## What it is

LLM Wiki (`nashsu/llm_wiki`) is a cross-platform desktop application that turns a user's documents into an organized, interlinked knowledge base automatically. It is the most widely adopted end-user implementation of Andrej Karpathy's LLM Wiki pattern: created on 2026-04-08, four days after the gist, it carries 21,725 GitHub stars, 2,464 forks, 907 commits, and 62 releases as of 2026-11-17, and tracking lists of the pattern's ecosystem consistently place it as the flagship implementation. Its one-line statement of the pattern matches the gist's: instead of traditional RAG — retrieve and answer from scratch on every query — the LLM incrementally builds and maintains a persistent wiki from the user's sources, so knowledge is compiled once and kept current.

Where LangChain's OpenWiki (see [[projects/openwiki]]) aims the same pattern at codebases and drives it from a coding agent or CLI, LLM Wiki aims it at a person's document corpus and drives it from a desktop application a human operates: a three-column interface (knowledge tree and file tree, chat, preview), a bundled chat agent, and a human review queue. The division of labor is the gist's own — the human curates, the LLM maintains — with the application supplying the machinery the gist leaves to a general-purpose coding agent.

All capability statements in the sources are **project-reported** from the project's README. The README publishes no benchmark of wiki quality, retrieval accuracy, or ingest correctness; its one quantitative apparatus (a four-signal relevance model for its knowledge graph) is described with weights but without evaluation. Adoption is the evidence, and it is adoption of an application, not validation of the pattern's claims.

## Mechanism

**What is kept from the pattern.** The application follows the gist's architecture directly: a three-layer structure of raw sources (immutable) → wiki (LLM-generated) → schema (rules and configuration); the three core operations — ingest, query, lint; `index.md` as the content catalog and navigation entry point; `log.md` as the chronological operation record; `[[wikilink]]` cross-references; YAML frontmatter on every page; and compatibility with Obsidian, so the wiki directory also works as an Obsidian vault.

**Purpose.** The application adds `purpose.md`, a file the gist has no equivalent for: it defines the wiki's goals, key questions, research scope, and evolving thesis — the *why*, distinct from the schema's *how*. The LLM reads it during every ingest and query, and can suggest updates to it from usage patterns. Scenario templates (research, reading, personal growth, business, general) pre-configure `purpose.md` and the schema for common uses.

**Two-step ingest.** The gist describes single-step ingest; LLM Wiki splits it into two sequential LLM calls. In the analysis step, the model reads a source and produces a structured analysis — key entities, concepts, arguments, connections to existing wiki content, contradictions and tensions with what the wiki already says, and recommendations for wiki structure. In the generation step, a second call turns the analysis into files: a source summary with frontmatter (`type`, `title`, `sources[]`), entity and concept pages with cross-references, updated `index.md`, `log.md`, and `overview.md`, review items for human judgment, and search queries for its deep-research feature. Supporting machinery: a SHA256 incremental cache hashes source files before ingest so unchanged files are skipped; a persistent ingest queue processes sources serially, survives restarts, and retries failed tasks up to three times; a folder watcher picks up external changes in `raw/sources/` and runs them through the same ingest/delete lifecycle; deleting a source cascades cleanup to derived pages. Multi-format parsing covers PDF, Office documents, EPUB/MOBI, Org-mode, images, and web clips, with built-in, cloud, or local (MinerU) PDF processing, and multimodal image ingestion that captions embedded images with a vision model.

**Knowledge graph.** Beyond wikilinks, the application builds a relevance graph over pages with a four-signal model: direct link (weight ×3.0), source overlap — pages sharing a raw source, via frontmatter `sources[]` (×4.0), Adamic-Adar common-neighbor similarity (×1.5), and type affinity (×1.0). Louvain community detection clusters pages by link topology independent of their declared types, scoring each community's cohesion (intra-edge density) and flagging clusters below 0.15. A graph-insights feature ranks surprising connections (cross-community edges, cross-type links, peripheral-to-hub couplings) and knowledge gaps, each actionable with one click into deep research. Retrieval is a pipeline over this graph, with an optional vector semantic search via LanceDB against any OpenAI-compatible embedding endpoint, and a "read sources only" mode that answers exclusively from original imported material.

**Review and research loops.** An asynchronous review system has the LLM flag items for human judgment, with predefined actions and pre-generated search queries attached, so curation happens as a queue rather than as editing. Deep Research generates LLM-optimized search topics, runs multi-query web search (Tavily, SerpApi, or SearXNG), and auto-ingests results into the wiki — the wiki can extend its own source base under its purpose statement. A Rust-backend chat agent with tool use (wiki, source, graph, and web retrieval; workspace file generation; shell execution under approval) is built in. The wiki is also exposed outward: a local HTTP API and MCP server on `127.0.0.1:19828` provide hybrid search, file read, graph traversal, and source rescan to other agents, and a ready-made agent skill installs into Claude Code or Codex in one command. State — conversations, settings, review items, project configuration — persists across restarts, and projects export and import as complete archives.

## Evidence

- **Adoption (repository metadata, 2026-11-17):** 21,725 stars and 2,464 forks within seven months of creation; 907 commits and 62 releases indicate sustained maintenance. Independent tracking lists of the LLM Wiki ecosystem (an auto-updating awesome list cataloguing 89 pattern projects as of October 2026) place this application first among implementations. These are attention and uptake measures.
- **Mechanism specificity:** the ingest split, the graph relevance weights, the cohesion threshold, and the queue's retry behavior are stated numerically in the README, which makes the implementation unusually inspectable as a design — but inspectability is not evaluation, and this knowledge base has not run the application.
- **No quality measurements in the sources:** no figures for ingest fidelity (whether generated pages faithfully represent sources), contradiction-detection accuracy (the analysis step claims to surface tensions with existing content), retrieval quality with or without the graph and vector layers, or review-queue precision (how often flagged items actually need judgment). The four-signal relevance model's weights are asserted, not derived in any cited experiment.

## Limitations

- **The pattern's central claim is untested here too.** Like every project in this cluster, LLM Wiki asserts that a compiled wiki beats per-query retrieval; it ships both (the wiki, plus optional vector search and a sources-only mode) without publishing a comparison. The honest reading is that the application is a bet on the pattern, executed at scale — not evidence for it.
- **Contradiction handling is a prompt step, not a mechanism.** Detecting "contradictions & tensions" happens inside the analysis LLM call. There is no claim-level evidence tracking comparable to OpenWiki's Grounded Claims, no versioned source pointers per fact, and no described procedure for resolving a detected contradiction beyond generation and the human review queue. What the queue catches therefore depends on an unmeasured flagging step.
- **Summarization loss compounds by design.** Two-step ingest inserts an analysis artifact between source and page; deep research then ingests web results into the same wiki, where they become sources for later pages. Each layer is a summary of a summary, and the system description offers no fidelity check at any layer — the failure mode secondary commentary on this tool category flags most often (early summarization errors propagating as authoritative pages).
- **The graph's authority exceeds its warrant.** Louvain communities and surprise scores are presented in the interface as structure the user can act on (one click launches research), but the relevance weights and the 0.15 cohesion flag are heuristics with no published validation; a plausible-looking cluster is a visualization of link topology, not a finding about the domain.
- **License ambiguity.** GitHub's repository metadata reports the license as "Other (NOASSERTION)" — the repository contains a `LICENSE` file, but its terms were not classified by GitHub and were not independently verified for this page. Users who care about the distinction between open-source and source-available should read the file itself.

## Competing approaches

- **OpenWiki ([[projects/openwiki]]).** The same pattern with the opposite center of gravity: codebases rather than documents, a CLI and coding-agent integrations rather than a desktop app, and an evidence mechanism (Grounded Claims with versioned source pointers and pre-update rechecks) where LLM Wiki has a review queue. LLM Wiki's graph analysis, community detection, and multimodal ingest have no OpenWiki equivalents. A user choosing between them is mostly choosing a corpus and a working style, not a pattern.
- **The gist, unimplemented (Karpathy's own setup).** A folder, a schema file, and a general coding agent (Claude Code, Codex, OpenCode) doing ingest, query, and lint by instruction, browsed in Obsidian. Zero installation and total schema freedom; every automation LLM Wiki ships — queue, cache, watcher, graph, review — must be improvised. LLM Wiki's existence at 21,000+ stars is itself evidence about how many users prefer the machinery pre-built.
- **Agent-skill implementations (for example Astro-Han/karpathy-llm-wiki, ~2,600 stars).** The pattern packaged as an installable skill for Claude Code, Cursor, and Codex — the middle option: no new application, but a maintained ingest/query/lint procedure with citations inside the agent the user already runs. Dozens of such skills and Obsidian plugins exist (the tracking list counts 31 agent skills and plugins); they differ mainly in schema choices their authors make on the user's behalf.
- **Hosted codebase wikis (DeepWiki, Google Code Wiki).** Adjacent rather than competing: they generate wikis of *code repositories* on vendor infrastructure for reading and Q&A, with no persistent user-owned wiki to curate. They answer "explain this repo"; LLM Wiki answers "maintain my knowledge."
- **OpenShelf and OKF ([[projects/openshelf]], [[projects/open-knowledge-format]]).** Standards, not applications: LLM Wiki's vault is Obsidian-compatible Markdown with its own frontmatter conventions (`sources[]`, page types), and neither standard is natively read or written by it. Its projects could in principle be exported into either format; the graph and review state that differentiate the application would not survive the trip, because both formats model pages and links, not application state.

## Implications

LLM Wiki is the demand signal for this whole cluster: within days of a methodology gist, users adopted a full desktop application implementing it, and within months it out-starred most agent tools in this corpus. Read together with OpenWiki's trajectory, the pattern's market has two clear poles — a personal-knowledge application operated by a human, and a codebase tool operated by an agent — and the gist's original framing (a person and their agent tending one wiki) is being pulled toward both. The application's additions also mark where the bare pattern hurts in practice: a purpose file (agents need direction, not just structure), a review queue (generation outruns curation), and an incremental cache (re-ingesting unchanged sources is the pattern's silent cost). Those are the same pressure points this corpus records for agent memory generally — admission, direction, and cost — in [[techniques/agent-skills-and-memory]].

## Reproducible experiment

The experiment that would test this application's distinctive claims **has not been run**: ingest a fixed document corpus with known cross-document contradictions and known community structure (synthetic or annotated) into LLM Wiki and into a plain gist-style setup (same base model, schema file only). Measure (1) contradiction recall — of the planted contradictions, how many the analysis step flagged into pages or the review queue; (2) ingest fidelity — page claims checked against sources on a sampled audit; (3) retrieval quality on a fixed question set across four configurations (wiki only, wiki + graph, wiki + vector, sources-only), which would price the graph and embedding layers the application adds; (4) incremental cost — tokens consumed re-ingesting the corpus after a 5% source change, with and without the SHA256 cache. Arms (1) and (3) test the application's own differentiators rather than the pattern's premise, which is why their absence from the record is conspicuous.

## Evidence status

Project documentation only. This page is built from the project's README and GitHub repository metadata, read on 2026-11-17, plus the Karpathy gist it implements. Mechanism descriptions are the project's stated behavior. Adoption figures are repository metadata recorded with their date. No independent evaluation, benchmark, or replication of the application's output quality exists in the sources, the application was not run by the KB maintainers, and the license file was not independently classified beyond GitHub's NOASSERTION metadata.

## Related pages

- [[projects/openwiki]] — the codebase-facing implementation of the same pattern.
- [[projects/open-knowledge-format]] — the bundle standard neither this app nor the gist natively speaks.
- [[projects/openshelf]] — the composition standard; a single-vault app sits below its layer.
- [[projects/context-as-infrastructure]] — compiled context as infrastructure, with the cluster's only measured result (cost, not accuracy).
- [[techniques/agent-skills-and-memory]] — the corpus's synthesis on persistent stores, where this application is the consumer-scale instance.

