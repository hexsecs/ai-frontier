---
uid: b6a90404-a8d1-4d13-9a40-000000000014
title: "Claude Agent ACP"
summary: "ACP adapter for the Claude Agent SDK; 0.101.0 release-please PR: idle compaction before cache expiry, Bun executables, Auto-mode default, streamed v2 commands."
type: project
created: 2026-11-09
updated: 2026-11-10
depth: deep
sources:
  - https://github.com/agentclientprotocol/claude-agent-acp/pull/1516
  - https://github.com/agentclientprotocol/claude-agent-acp/releases/tag/v0.101.0
  - https://agentclientprotocol.com/protocol/v2/overview
  - https://agentclientprotocol.com/rfds/subagents
---

# Claude Agent ACP

**Origin:** [[briefings/2026/11/2026-11-04]] — finding 4. **Provenance:** deep re-grounding of the archived backfill against sources inspected on 2026-11-10; the briefing remains the immutable historical record.

## What it is

Claude Agent ACP is an ACP-compatible coding agent: an adapter that exposes the Claude Agent SDK to any Agent Client Protocol client. It lives in the `agentclientprotocol` GitHub organization at `agentclientprotocol/claude-agent-acp`, published by the ACP project itself and framed by that project as an implementation of the protocol. The repository README lists its capability surface: context @-mentions, images, tool calls with permission requests, compact file changes through the negotiated AIR diff patch extension, following, edit review, TODO lists, nested subagent transcripts, interactive and background terminals, custom slash commands, client MCP servers, an Ultracode session config option, `/mcp` in chat, session-scoped long-running goals, structured errors, recommended config values, permission presentation, one-fact-per-field tool call reports, and standalone executables built with Bun.

The page's proximate artifact is the release pull request [#1516](https://github.com/agentclientprotocol/claude-agent-acp/pull/1516), "chore(main): release 0.101.0" — a fully automated release-please PR, opened and commented by the `acp-release-bot` on 2 November 2026, force-pushed three times (most recently at 12:01 UTC on 5 November), and merged by maintainer benbrandt into `main` on 5 November 2026 with commit `85aec26`. The release compares `v0.100.0...v0.101.0`, was published 5 November at 21:07, and carried 10 release assets. The PR reports "14 of 15 checks passed"; no human review was recorded on the PR itself. The linked issue #1454 ("Support idle compaction (compact before the prompt cache expires) in ACP sessions") closed on merge.

**Maturity.** Public repository under the protocol organization (2.7k stars, 474 forks, 991 commits, 97 open issues and 43 open pull requests as read on 2026-11-10), release automation via Release Please, and multi-platform distribution: each release attaches archives for Linux (glibc and musl), macOS and Windows, on x64 and arm64, holding two files — `claude-agent-acp` and the Claude CLI it runs — that need no Node.js install; `CLAUDE_CODE_EXECUTABLE` selects an existing Claude CLI, Bun is needed to build, and the smoke build drives a real session needing a Claude login. The project is a 0.x-versioned adapter: no stability guarantee is stated for any release in the inspected material.

## Mechanism

**What the release PR changed.** Release-please bookkeeping only: `.release-please-manifest.json`, `CHANGELOG.md`, `package-lock.json` and `package.json`. The features below shipped in earlier PRs and are made public by this release; the release PR itself contains no behavioural code.

**The four features of 0.101.0** (each with its PR and commit, from the release notes):

1. **Compact idle sessions before the prompt cache expires** (#1522, commit `a79d073`), closing #1454 and #1518. The mechanism named in the issue title is cache-aware lifecycle management: an idle session is compacted while the provider's prompt cache is still warm, rather than after it has expired and been lost — trading a summarization step against the cost of rebuilding a long context from scratch on the next turn.
2. **Single-file executables built with Bun** (#1524, commit `e3f0b6c`) — the distribution mechanism behind the 10 release assets.
3. **Sessions start in Auto mode by default** (#1533, commit `7ea9eec`) — the default permission mode for new sessions.
4. **Streaming of v2 background command output** (#1512, commit `53e3eec`) — background commands stream their output incrementally to the client instead of surfacing on completion.

**Two fixes:** honour the configured fallback for unavailable restored modes (#1520, commit `8bbdea6`), and update to `@anthropic-ai/claude-agent-sdk` 0.3.318 (#1525, commit `1d4418f`).

**The protocol layer the adapter operationalises.** From the ACP v2 overview and the subagents RFD (inspected 2026-11-10): ACP v2 is served as a draft — clients that request version 2 or later in `initialize` get v2, all others get v1; `CLAUDE_AGENT_ACP_PROTOCOL` pins the adapter's protocol version, and `auto` is the default. Subagent attribution is specified in the RFD as: the Agent announces a child via `subagent_update` before any child traffic, carrying `title`, `description`, work `state` and optional `cwd`/`capabilities`; delegated tasks travel as `session_message` upserts; tool calls reference child sessions via `session` content. The adapter's README-level feature list ("nested subagent transcripts") is the user-visible consequence of that attribution mechanism.

**The release mechanism itself.** Release Please generates the PR from conventional commits, the bot force-pushes the branch as commits land, and one merge both publishes the tag and closes the linked issues. The 0.101.0 changelog therefore is a faithful index of what merged since 0.100.0 — but the release PR demonstrates that the *release* of protocol-facing capability (idle compaction, Auto-mode default, v2 command streaming) can carry no protocol review: "No reviews" is recorded on the PR, and the merge is a single-maintainer action on a bot-generated branch.

## Evidence

| Claim | Tier |
|---|---|
| Release 0.101.0 exists, published 2026-11-05, comparing v0.100.0...v0.101.0 | Inspected (PR and release page) |
| PR #1516 changed only release bookkeeping (4 files) | Inspected (PR file list) |
| The four features and two fixes with their PR numbers and commits | Claimed by release notes (inspected as text; the underlying PRs were not opened) |
| Merge by benbrandt, 14 of 15 checks passed, 10 release assets | Inspected (PR and release page) |
| Repository scale: 2.7k stars, 474 forks, 991 commits | Inspected on 2026-11-10 |
| ACP v2 served as a draft; negotiation and pinning behaviour | Inspected (v2 overview) |
| Subagent attribution via `subagent_update`, `session_message`, `session` content | Inspected (subagents RFD) |

What the inspected material does **not** contain: any measured result for any feature (no latency figure for idle compaction, no cache-hit rate, no executable size or startup time, no client-compatibility matrix), any issue tracker evidence that the four features work as described beyond their presence in the changelog, and any benchmark or comparison with ACP v1 behaviour.

## Limitations

- **The release notes are the only evidence the features exist.** Each feature's PR was not opened by the KB maintainers; the changelog is Release Please's rendering of conventional commits, which is trustworthy as a record of what was merged and unverified as a record of behaviour.
- **ACP v2 is an explicit draft.** The overview itself frames v2 as draft; a client relying on the streamed background commands (#1512) is depending on draft-protocol surface.
- **Idle compaction's benefit is asserted, not measured.** The issue title names the mechanism (compact before the prompt cache expires); no published figure shows the cache-expiry boundary, the compaction threshold, or the token economics on either side.
- **Cross-client compatibility is documented, not tested publicly.** The README lists negotiated capabilities (AIR diff patches, permission requests, background terminals); nothing in the inspected material shows which third-party clients exercise which surface, or with what result.
- **The release process concentrated the decision.** One maintainer merged a bot-generated, unreviewed PR that published a protocol-facing release — normal for release-please projects, and still a single point of judgement for capability shipping.

## Competing approaches

Only alternatives the inspected sources name.

- **ACP v1 versus draft ACP v2**, including the negotiation mapping (version 2 or later requested in `initialize` yields v2; everyone else gets v1) and the `CLAUDE_AGENT_ACP_PROTOCOL` pin as the escape hatch — the two ways a client and this adapter can disagree about protocol surface.
- **Node.js distribution versus Bun single-file executables** — the release makes the standalone executable the supported default and `CLAUDE_CODE_EXECUTABLE` the override for an existing CLI.
- **Other agents behind the same protocol.** The ACP organization's framing is that the adapter is one implementation of a client-neutral protocol; the alternative to `claude-agent-acp` specifically is any other agent the same ACP client can drive — named in the inspected material only as the protocol's client-implementation framing, without a matrix.

(Analyst note, not from the sources: running Claude Code directly against its own UI, or other vendor agents with their native clients, are the obvious non-ACP alternatives; none is characterised here.)

## Implications

The following is analysis by the KB maintainers, not a claim of the authors'.

Read as a maintenance specimen, the interesting engineering is **cache-aware session lifecycle as a protocol responsibility**. Idle compaction before prompt-cache expiry (#1522) moves a cost decision — compact now while the cache is warm versus rebuild later — into the adapter, on the theory that the adapter is the only party that knows both the session's idleness and the cache window. That is an instance of [[concepts/improvement-lives-in-external-state]] inverted: the state that matters (provider cache temperature) is invisible to the client and only partially visible to the adapter, so the adapter guesses on the client's behalf. Whether the guess is right is exactly what the release does not measure.

Second, **release automation can carry protocol capability without protocol review**. The 0.101.0 release shipped a permission-mode default change (Auto mode), a v2 protocol surface (streamed background commands) and a lifecycle change (idle compaction) through a single unreviewed bot PR. For consumers, the practical consequence is that pinning the adapter version (not `auto`) is the only way to hold a stable protocol contract — the pinning escape hatch exists precisely because the default flow moves.

Third, the subagent attribution mechanism (`subagent_update` before child traffic, `session_message` upserts, `session` content references) is a clean answer to action attribution in delegated-agent settings: every child is announced before it acts, and tool calls remain traceable to their owning session. Whatever its implementation quality here, the RFD's shape is the transferable part.

The counterweight is that nothing published measures any of it. The page's contribution is the mechanism record and its evidence tiers, not a verdict that the adapter is good at its job.

## Reproducible experiment

Proposed, not executed; all arms use published releases and public ACP clients, freezing versions.

1. **Idle compaction economics.** Drive a session to a large context, leave it idle across the compaction threshold, and measure next-turn input tokens and latency against a control that never idles. Report numerator and denominator (turns, context size, cache-hit rate if exposed). Pass criterion: the compacted session's next turn is cheaper or faster than the rebuild path; a compacted session that is *more* expensive falsifies the feature's premise.
2. **Auto-mode default.** Start a fresh session on 0.101.0 with no config and assert the effective permission mode from the client's permission-request stream. Pass criterion: Auto mode without explicit configuration; a prompt for mode selection falsifies the default change.
3. **v2 negotiation matrix.** From one ACP client, connect twice — once requesting v1, once v2 — and record which background-command behaviour each session exhibits. Pass criterion: v1 sessions behave as v0.100.0 did; only v2 sessions stream.
4. **Subagent attribution conformance.** Trigger a session that spawns a nested subagent and capture the message stream. Pass criteria: a `subagent_update` precedes any child traffic; the child's tool calls carry `session` references; no tool call appears attributed to the parent that the child performed.
5. **Executable isolation.** Run the Bun-built executable on a clean machine without Node.js and confirm session startup, MCP server attach and background terminals work; record binary size and cold-start time. Pass criterion: full function with no Node.js present.

## Evidence status

Grounded in HTTPS reads on 2026-11-10 of PR [#1516](https://github.com/agentclientprotocol/claude-agent-acp/pull/1516) (metadata, conversation, bot timeline, file list, checks count, reviewers panel), the release page for tag v0.101.0 (notes, assets, publication timestamp), the ACP v2 overview, and the subagents RFD. **Inspected:** release and PR metadata, the release-please mechanics, the negotiation and pinning documentation, and the subagent attribution specification. **Claimed by the release notes:** the four features and two fixes with their PR numbers and commits — read as text, with the underlying PRs unopened. **Not done by the KB maintainers:** any execution, installation, session, or benchmark; no independent evaluation, client-compatibility test, or measurement of any feature is claimed, and none is known to them.

## Historical coverage

- [[briefings/2026/11/2026-11-04]] — finding 4, the dated full-fidelity research briefing that selected this release PR.
- Analyst-selected context, not source-verified dependencies: [[projects/agentos]] and [[projects/rivet-agents]] for other agent-framework approaches to protocol and runtime boundaries; [[projects/agent-orchestrator]] consumes claude-agent-acp as its Claude Code Chat driver, per its own documentation; the cross-project synthesis is [[evaluations/briefing-synthesis-2026-11-03-to-09]].
