---
uid: d68485cd-6cdf-484a-b961-d312f8594d15
depth: full
title: "OpenWiki"
summary: "LangChain's OpenWiki CLI generates and maintains a Markdown wiki for a codebase or personal sources, tracking each fact to versioned source evidence."
type: project
created: 2026-11-17
updated: 2026-11-17
related: [openshelf, open-knowledge-format, llm-wiki, context-as-infrastructure]
sources:
  - url: https://github.com/langchain-ai/openwiki
    retrieved: 2026-11-17
  - url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
    retrieved: 2026-11-17
---

# OpenWiki

## What it is

OpenWiki is an open-source command-line tool from LangChain that writes and maintains agent documentation for a codebase. It turns a repository — or, in its personal mode, a set of connected knowledge sources — into a linked Markdown wiki that the user owns as plain files, and that a coding agent can search and read as context. The repository was created on 2026-06-22; as of 2026-11-17 it carries 17,990 GitHub stars, 1,325 forks, 525 commits, and 32 releases, under the MIT license. It requires Node.js 22.22.0 or newer and is installed with `npm install -g openwiki`.

OpenWiki is an implementation of the LLM Wiki pattern Andrej Karpathy published as a gist in April 2026: instead of re-deriving knowledge from raw sources on every query (the retrieval-augmented generation default), an LLM compiles knowledge once into persistent, interlinked pages and keeps those pages current. OpenWiki's own framing is "a living wiki for your code, your agents, and you." Its two nearest named relatives in its own documentation lineage are Cognition's DeepWiki and Factory's AutoWiki, both hosted codebase-wiki products; OpenWiki's differentiator is that the wiki is generated locally, stored in the repository, and maintained through the user's own coding agent or its standalone agent.

The mechanism below is documented in unusual operational detail in the project README. The performance evidence is a different matter: the README publishes no benchmark of documentation quality, accuracy, or maintenance cost, and no independent evaluation was found in the sources inspected. Adoption (stars, forks, release cadence) is the strongest public signal, and it measures attention, not correctness.

## Mechanism

OpenWiki runs in two modes. **Code mode** (the default) documents the current repository into an `openwiki/` directory inside it. **Personal mode** (`openwiki personal --init`) builds a personal wiki at `~/.openwiki/wiki` from connected sources. There are two execution paths for code mode: inside a coding agent the user already runs (integrations exist for Codex, Claude Code, OpenCode, Cursor, GitHub Copilot CLI, Kiro, IBM Bob, Oh My Pi, Antigravity, and Pi), where the host agent does the research and writing with its own authenticated model session; or through OpenWiki's own Deep Agents documentation agent via the standalone CLI, with fifteen supported model providers including OpenAI, Anthropic, Gemini, AWS Bedrock, and local OpenAI-compatible endpoints.

Generation is organized as a durable queue of independent page jobs. `openwiki/.run.json` checkpoints an active run; a page advances only after its Markdown, its Claims, verification, and its entry in `openwiki/.page-manifest.json` are all durable, so completed pages survive interruptions and an interrupted run resumes rather than restarting. The native CLI can document several pages concurrently (`OPENWIKI_PAGE_CONCURRENCY`, 1–8, default 1); a worker that hits a provider rate limit lowers the run's concurrency and its page is restored for a later run. Coding-agent integrations consume the same queue sequentially through an MCP lifecycle: `openwiki_begin → openwiki_submit_plan → openwiki_next_page → openwiki_submit_page → … → openwiki_finish`.

The design's center is **Grounded Claims**. Each repository page's load-bearing facts are tracked as Claims, each pointing to versioned source evidence such as `repo://src/server.ts#L40-L82`, persisted in sidecar files under `openwiki/.claims/` that travel with the Markdown. Before an update, OpenWiki re-checks every persisted evidence version — before deciding whether the repository changed at all. A stale or unresolved Claim forces work on its owning page even if the planner would omit it; the page worker receives only the Claims requiring attention, explicitly confirms, revises, adds, or retracts them, and unaffected Claims are retained deterministically without being re-sent through the model. A page receives a `verified` stamp only after a successful submission reconciles a non-empty, complete Claims set and passes a final evidence recheck. A clean update — no source or Claim drift — skips model work entirely and leaves wiki content untouched. Claims currently cover repository evidence only; facts derived from connectors, including LangSmith traces, are explicitly not claimed.

Output is emitted as **Google Open Knowledge Format (OKF) v0.2** bundles in both modes (see [[projects/open-knowledge-format]]): every concept document carries YAML frontmatter with a required `type`, plus optional `generated`, `verified`, `sources`, `status`, and `stale_after` fields that OpenWiki maintains. Repository pages project their Claims evidence into the frontmatter `sources` field. Pages embed Mermaid diagrams where the generator judges them clearer than prose; after each run, diagrams that fail validation are converted in place to plain text fences with an explanatory comment, and a later update repairs them.

Around the core loop: `openwiki_search` and `openwiki_read` give agents local, read-only, model-free retrieval over the wiki; `openwiki link` groups several repositories' wikis into named workspaces with cross-wiki search; `openwiki visualize` renders an interactive node graph with a live Markdown reader and can export a static visualizer. Personal mode ingests through nine connectors (custom MCP, local git repositories, Notion, Gmail, X/Twitter, web search, Hacker News, and Slack), each writing raw data and manifests under `~/.openwiki/connectors/` before synthesis. In code mode, a LangSmith connector can enrich pages with recent trace data — tool calls, outcomes, latency — so documentation reflects runtime behavior, not only source. Scheduled updates are supported by copying a provided GitHub Actions, GitLab CI, or Bitbucket workflow that opens a documentation PR when the wiki changes. A `.openwikiignore` file (glob syntax with negation) is a hard read boundary: ignored paths are never read or reproduced. OpenWiki maintains only its own marked block inside a repository's `AGENTS.md` (and an existing `CLAUDE.md`), and never rewrites the user-authored `openwiki/INSTRUCTIONS.md` brief that scopes generation. Telemetry is anonymous and aggregate, on by default, and disabled by `OPENWIKI_TELEMETRY_DISABLED=1` or `DO_NOT_TRACK=1`.

## Evidence

All capability statements in the sources are **project-reported**: they come from the project's own README and repository metadata. No independent evaluation, replication, or third-party benchmark of OpenWiki's output quality was found in the sources inspected for this page.

- **Adoption signals (repository metadata, 2026-11-17):** 17,990 stars and 1,325 forks in under five months from creation (2026-06-22), 525 commits, 32 releases. These measure uptake and maintenance activity, not documentation accuracy.
- **Mechanism verifiability:** the Claims reconciliation protocol, the durability boundary for page completion, and the no-op update behavior are specified in the README at a level that makes them testable against the shipped CLI — but this knowledge base has not run the tool, and no published third-party test of those behaviors was found.
- **No quality measurements:** the README reports no precision/recall figures for Claim staleness detection, no human ratings of generated pages, no comparison against hand-written documentation, and no cost figures for a generation or update run. The repository contains an `evals/` directory, but no published results from it were inspected for this page.

## Limitations

- **The evidence base is the vendor's own documentation.** Every mechanism claim above is LangChain describing its own tool. The Grounded Claims design is, on its face, the strongest provenance mechanism in this tool cluster — versioned evidence per fact, rechecked before updates — but its real-world precision (how often drift is caught, how often stale Claims are missed or falsely flagged) is unmeasured in public.
- **Host-driven runs are narrower than CLI runs.** Coding-agent integrations support repository code wikis only, not personal brains, and connector-sourced context (including LangSmith) is not yet supported on that path. The two execution paths therefore do not offer the same product.
- **Claims stop at the repository boundary.** Connector-derived facts are unclaimed, so a personal wiki's synthesized pages carry no equivalent of the code wiki's evidence tracking — exactly the content class where unattributed synthesis is hardest to audit.
- **Scale is handled by retrieval, not by loading.** The wiki is consumed through search-and-read tools; the README's own guidance is that retrieval is "optional context, not a routine step at the start of every task." A wiki of hundreds of pages helps only when the agent chooses to consult it — the same admission problem this corpus records for agent memory files (see [[projects/security-impact-of-coding-agent-memory-files]]).
- **Generated diagrams degrade silently by design.** A Mermaid diagram that fails validation ships as a text fence until a later update repairs it; a reader of a single snapshot cannot tell a degraded diagram from an intentional one without the comment the converter leaves.

## Competing approaches

- **Cognition DeepWiki (hosted).** Generates a wiki for a public GitHub repository by changing `github.com` to `deepwiki.com`; over 50,000 public repositories were indexed at its May 2025 launch, and a free no-auth MCP server exposes the wikis to agents. Private repositories require a Devin account, and the wiki lives on Cognition's infrastructure rather than as files the user owns. It is the zero-install alternative; OpenWiki is the local, git-native one. (Characterized from Cognition's launch material and Devin documentation as cited in secondary comparisons; not deep-read for this page.)
- **Factory AutoWiki and Google Code Wiki (hosted).** Both generate repository wikis as hosted products — AutoWiki treats documentation as a build artifact regenerated through Factory's agent platform; Code Wiki generates and hosts wikis for public repositories with Gemini chat. Neither produces a user-owned Markdown bundle in the repository. (Named in OpenWiki's own related-work framing and secondary comparisons; not deep-read for this page.)
- **LLM Wiki desktop app ([[projects/llm-wiki]]).** The same Karpathy pattern aimed at personal documents rather than codebases: a desktop application with a knowledge graph, community detection, and a human review queue, instead of a CLI driven by a coding agent. The two tools partition the pattern by surface — repository versus document corpus, agent-operated versus human-operated.
- **OpenShelf ([[projects/openshelf]]).** Not a generator at all: a standard for composing many independently owned Markdown knowledge bases into one project. OpenWiki produces one wiki per repository (linkable into workspaces); OpenShelf standardizes how many KBs — however authored — are declared, pinned, and read together. They operate at different layers and are treated as complements in this corpus, with the mapping between OKF output and OpenShelf metadata analyzed on the OpenShelf page.
- **Hand-written documentation and plain RAG.** The baselines the whole category argues against: documentation a human maintains (accurate until it drifts, expensive to keep current) and retrieval over raw sources at query time (always current, re-derived on every query, no accumulated synthesis). OpenWiki's Claims mechanism is best read as an attempt to get the compiled wiki's economics without its usual failure mode — confident, stale pages — by pricing each fact's evidence into the update loop.

## Implications

OpenWiki is the clearest statement in this corpus that the maintenance problem, not the generation problem, is the hard part of agent documentation. Its engineering budget visibly goes to durability (resumable page jobs), drift detection (Claims rechecked before the planner runs), and restraint (no-op runs that touch nothing). If the Claims mechanism works as specified, it is a concrete instance of this corpus's verification pattern applied to prose: a claim is retained only while its evidence still verifies, which is the same shape as KARMA's retain-iff-gain gate and SkillCompiler's validated admission, transposed from skills to facts (see [[techniques/agent-skills-and-memory]] and [[concepts/improvement-lives-in-external-state]]). Whether it works as specified is precisely what the missing evaluations would show.

The tool also marks the LLM Wiki pattern's center of gravity moving from personal knowledge (the gist's framing) to codebase documentation, where sources are versioned, evidence pointers are stable line ranges, and CI can schedule maintenance — the environment where the pattern's provenance ideas are easiest to make rigorous.

## Reproducible experiment

No published evaluation protocol exists in the sources, so the experiment that would test OpenWiki's central claim is specified here and **has not been run**. Seed a set of repositories with known, documented facts; generate wikis with `openwiki --init`; then apply a series of source changes of graded subtlety (renames, behavior changes behind unchanged signatures, deleted features, moved files) and run `openwiki --update` after each. Measure: (1) Claim-level precision and recall — of the facts the changes made false, how many the update flagged or rewrote; of the facts flagged, how many were actually false; (2) page-level staleness in the resulting wiki, rated blind against the new source; (3) model cost per update versus a full regeneration and versus a no-Claims ablation if one can be configured; (4) no-op fidelity — an update run on an unchanged repository must produce a byte-identical wiki. Arms (1) and (4) test the mechanism's stated guarantees directly; both are deterministic enough that a failure would be decisive.

## Evidence status

Project documentation only. This page is built from the project's own README and GitHub repository metadata, read in full on 2026-11-17, plus the Karpathy gist it cites as its pattern source. Mechanism descriptions are the project's stated behavior — a reasonable basis for describing what the tool is designed to do, not evidence for how well it does it. No output wiki was generated, no Claim reconciliation was exercised, and no independent evaluation or replication exists in the sources. Star and fork counts are attention measures recorded with their date; they will drift.

## Related pages

- [[projects/open-knowledge-format]] — the format OpenWiki emits.
- [[projects/openshelf]] — the composition standard one layer up.
- [[projects/llm-wiki]] — the desktop implementation of the same pattern.
- [[projects/context-as-infrastructure]] — the corpus's other compiled-context system; its measured result (cost savings, no accuracy gain) is the cautionary baseline for this whole cluster.
- [[techniques/agent-skills-and-memory]] — gated admission to persistent stores, the pattern Claims instantiate for facts.

