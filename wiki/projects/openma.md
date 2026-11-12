---
uid: b6a90507-a8d1-4d13-9a40-000000000027
title: "OpenMA"
summary: "Self-hostable managed-agent platform separating session, execution and recovery from harness, sandbox and model, with Claude and OpenAI API surfaces."
type: project
created: 2026-11-09
updated: 2026-11-10
depth: deep
sources:
  - https://github.com/openma-ai/open-managed-agents
  - https://raw.githubusercontent.com/openma-ai/open-managed-agents/main/README.md
  - https://raw.githubusercontent.com/openma-ai/open-managed-agents/main/docs/v1-architecture.md
  - https://raw.githubusercontent.com/openma-ai/open-managed-agents/main/docs/openai-agents-compatibility-status.md
  - https://raw.githubusercontent.com/openma-ai/open-managed-agents/main/packages/session-runtime/src/machine.ts
  - https://raw.githubusercontent.com/openma-ai/open-managed-agents/main/packages/session-runtime/package.json
  - https://raw.githubusercontent.com/openma-ai/open-managed-agents/main/packages/sandbox/src/recovery.ts
  - https://raw.githubusercontent.com/openma-ai/open-managed-agents/main/packages/managed-agents-runtime/package.json
  - https://raw.githubusercontent.com/openma-ai/open-managed-agents/main/apps/agent/src/harness/interface.ts
  - https://raw.githubusercontent.com/openma-ai/open-managed-agents/main/.github/workflows/ci.yml
  - https://api.github.com/repos/openma-ai/open-managed-agents
  - https://api.github.com/repos/openma-ai/open-managed-agents/git/trees/main?recursive=1
---

# OpenMA

## What it is

OpenMA (Open Managed Agents) is a self-hostable platform for running managed agent sessions, published under the Apache-2.0 licence by the organisation `openma-ai` in the repository `openma-ai/open-managed-agents`. GitHub metadata records creation on 2026-04-10 and a last push on 2026-11-10; at the time of this review the repository had 353 stars, 60 forks and 91 open issues, is written chiefly in TypeScript, and carries the topic set `agent-platform`, `agent-sandbox`, `agent-client-protocol`, `anthropic-managed-agents`, `claude-managed-agents`, `openai-agents-api`, `byok`, `cloudflare`, `modal` and `self-hosted-agents`. Its declared homepage is `https://openma.ai`.

The project's own positioning is in the README's first lines: "Any model. Any harness. Any sandbox. Any cloud." — OpenMA "handles sessions, execution and recovery, so you can build and run agents with any model, any harness, any sandbox, on any cloud. An open-source, self-hostable alternative to Claude Managed Agents and OpenAI Agents API." The README qualifies this itself in the same document: "'Any' means you can extend these interfaces; available features and setup depend on the selected adapters." That sentence is the most honest framing of the project available in the inspected files.

Structurally this is a large monorepo — 5,021 paths in the recursive tree, not truncated. It contains a `packages/` layer of internal libraries, an `apps/` layer with the Cloudflare Worker app (`apps/main`), a Node host (`apps/main-node`), a React console (`apps/console`), a marketing site (`apps/web`), a documentation site (`apps/docs`), the harness process (`apps/agent`), a workflow service (`apps/matter`) and a Vercel adapter (`apps/main-vercel`), plus `test/`, `scripts/`, `seo/` and an `rl/` tree containing a reinforcement-learning trainer (`rl/verl/verl_trainer.py`, `rl/reward.ts`) and a Terminal-Bench cloud runner (`rl/tasks/terminal-bench/run-cloud.ts`).

Maturity signals: the repository publishes a hosted service and a self-hosted deployment path, keeps a machine-written compatibility report with dated acceptance runs, and separates a stable `v0` application from a `v1` SDK-first architecture in migration. Counter-signals: the two core runtime packages inspected — `@open-managed-agents/session-runtime` and `@open-managed-agents/runtime` — are marked `"private": true` with version `0.1.0`, and the OpenAI compatibility adapter is described as a tested subset rather than full parity. The repository states plainly: "OpenMA is an independent implementation. Check the API and runtime coverage before migrating."

## Mechanism

Each statement below is established by a file read over HTTPS on 2026-11-10; the file is named.

**The division of labour.** `README.md` calls OpenMA a "meta-harness" that "manages the resources and lifecycle around an agent loop", and describes two placements. With the harness *outside* the sandbox, the model loop runs in the platform and the sandbox executes tools; session history is kept separately from both, "so a sandbox failure does not erase the conversation and a replacement harness can rebuild context from durable events". With the harness *inside* the sandbox, Claude Code, Codex or another established harness is brought into a managed sandbox and its agent loop, context management, tools and skills are reused rather than rebuilt. The host-side harness interface is `apps/agent/src/harness/interface.ts`, whose `HarnessInterface` requires a `run` method and optionally provides `interruptPending`, `dispose` and `onSessionInit`; the compaction decision is described there as estimating tokens and firing above 75% of the model's context window.

**Store and port architecture.** `docs/v1-architecture.md` defines an "interface-package plus implementation-package model": a domain interface is independently installable and free of platform or database-driver dependency, and implementations point inward at it. The document enumerates the extracted domain families — `agent-store`, `credential-store`, `deployment-store`, `deployment-run-store`, `dream-store`, `environment-store`, `environment-work-store`, `file-store`, `memory-store-store`, `memory-document-store`, `skill-store`, `tunnel-store`, `user-profile-store`, `session-store`, `session-event-store`, `session-resource-store`, `session-thread-store` and `vault-store` — each with a memory and a SQL implementation. It also fixes three modelling rules that matter for consistency: Session Threads are an independent aggregate from Sessions; Thread Events are "not a second writable event model or table" but "a narrow read projection (`SessionThreadEventStore`) of the same append-only `SessionEventStore`"; and Session Resources are "a projection of the Session aggregate, not a second Session copy". The same document records that v0 and v1 coexist during migration and that new v1 packages may not import v0 apps, routes, Durable Objects or service containers.

**Turn lifecycle.** `packages/session-runtime/src/machine.ts` holds the `SessionStateMachine`, described in its own header as "a single source for turn lifecycle on both CF and Node". Its surface is `runHarnessTurn(agentId, userMessage)` — beginTurn → harness.run → endTurn — plus `onWake()` and `destroy()`. `onWake()` "Detect orphan turns (sessions row marked 'running' with a turn_id we don't recognise as our own active turn) and reconcile them via `recoverInterruptedState`", and the header says it is called from the Cloudflare Durable Object `alarm()` "every 30s while a turn is in flight, and on cold start when a request hits an evicted DO", and from `SessionRegistry.bootstrap()` at Node process start. All platform differences are pushed into a `RuntimeAdapter`: "Per-platform polymorphism is entirely in the RuntimeAdapter the machine holds (one impl, both platforms via SqlClient + the optional hintTurnInFlight callback)." The machine's dependencies include a per-session `SandboxPort`, a model builder, a tools builder and an optional `beforeSandboxDestroy` hook for flushing provider and filesystem state.

**Concurrency, claiming and ordering.** The README's scaling section states that for harnesses outside the sandbox, "replicas claim different sessions in parallel through a durable execution outbox, renewable leases, and fencing; work within a session stays ordered", while in-sandbox harnesses "use the separate Environment Work claim, rather than nesting a second Session execution claim". The same document states the constraint on extensions: "New adapters must preserve required transaction, claim/retry, and conditional-write semantics. Background queues, Session execution claims, and Environment Work have distinct contracts." The corresponding packages are visible in the tree: `packages/queue/src/ports.ts` for the queue and dead-letter contracts, `packages/managed-agents-application/src/sessions/work-admission.ts` for session work admission, and `packages/managed-agents-application/src/environment-work/` for the separate Environment Work surface.

**Sandbox loss is a first-class case.** `packages/sandbox/src/recovery.ts` implements recovery from a vanished sandbox, citing "ADR 0005, 'Sandbox disappears'". Its policy is explicit and conservative: sandboxes are treated as cattle that a provider may reclaim at any time; liveness is probed with `probeSandboxLiveness`, which returns `alive`, `lost` or `unknown`; a sandbox that cannot be probed reports `unknown` and "hosts never replace a sandbox they cannot prove lost"; a failed probe is retried once so a single network blip is not read as a loss; and critically, "The operation is not retried: it may have had effects outside the sandbox, and the files it relied on may be older in the replacement, so the caller (the agent) decides what to redo." Replacement failures surface as `SandboxReplacedError` and `SandboxRecoveryFailedError`, and recovery gives up after `maxReplacements` (default 3).

**API surfaces.** The README's compatibility table lists four: Claude Managed Agents at `/v1/*` (the official Anthropic SDK is pinned to `0.120.0`); OpenAI Agents API at `/openai/v1/*` (SDK baseline `openai@7.15.0`); Kimi Hosted Agents at `/kha/v1/*`, an opt-in Node subset gated behind `OMA_KIMI_KHA_COMPAT=1`, disabled by default and not available on hosted Cloudflare; and OpenMA extensions at `/v1/oma/*` for Model Cards and product-specific features.

**Infrastructure choice.** The README's stack table offers SQLite, PostgreSQL, MySQL, Cloudflare D1 and Durable Object SQL for the database; SQL-backed queues, Cloudflare Queues and an in-memory adapter for the queue; and S3-compatible storage, Cloudflare R2, the local filesystem and an in-memory blob adapter for objects. Deployment paths are Native Node.js/Docker, Fly.io, Vercel (Beta) and Cloudflare. Sandboxes are E2B, Daytona, LiteBox, Cloudflare Sandbox and others, with adapters under `packages/sandbox-adapter-*` (daytona, e2b, boxrun, litebox, opensandbox) and runtime hosts under `packages/managed-runtime-*` (cloudflare, node, modal, vercel, e2b, blaxel, daytona, boxlite, sprites, superserve). The README warns that the deployment "does not fall back to running agent commands in an unisolated host subprocess", and that "A successful `/health` response confirms server readiness, not that a model or sandbox task has succeeded."

**Credentials.** The README states that Model Cards encrypt provider keys at rest and that Vault-backed gateways support scoped access to private services, but qualifies it: "enforced credential isolation depends on the provider and runtime profile."

## Evidence

| Claim | Status | Where |
|---|---|---|
| Turn lifecycle has one implementation shared by both platforms | Code-inspected | `packages/session-runtime/src/machine.ts` |
| Orphan turns are detected and reconciled on a 30-second alarm and at Node bootstrap | Code-inspected | `packages/session-runtime/src/machine.ts` |
| A lost sandbox is replaced, but the failed operation is deliberately not retried | Code-inspected | `packages/sandbox/src/recovery.ts` |
| Stores are split into interface and implementation packages with memory and SQL variants | Code-inspected | `docs/v1-architecture.md` |
| CI classifies changes into graded impact surfaces and scopes console E2E by domain | Code-inspected | `.github/workflows/ci.yml` (`scripts/ci-impact-surfaces.mjs`, `scripts/ci-console-e2e-scope.mjs`, unit-tested; merge-queue check context `verify`) |
| The Anthropic and OpenAI SDK contracts are pinned and audited against a fixed baseline | Code-inspected | `README.md` (SDK `0.120.0`, `openai@7.15.0`), `docs/openai-agents-compatibility-status.md` (audit date 2026-09-11, hosted acceptance 2026-09-16) |
| Compatibility acceptance: 43 SDK methods, 44 scenarios, 42 HTTP operations; release-candidate results of 61/93/73 items, 68 Node checks, 12 E2E scenarios, 4 ACP, 23 SQL, 24 native-thread, 8 local-sandbox and 14 built web pages | Vendor-reported; the same document states the tests used a local controlled model and "不计作真实 OpenAI 模型或物理沙箱供应商联调" — not a real OpenAI model or physical sandbox provider integration | `docs/openai-agents-compatibility-status.md` |
| The deployment serves a `/health` endpoint and refuses to run agent commands unisolated | Code-inspected | `README.md` (self-hosting section) |
| Harness contract includes interrupt, dispose and session-init hooks and a 75% compaction threshold | Code-inspected | `apps/agent/src/harness/interface.ts` |
| A harness benchmark and a Terminal-Bench cloud runner exist in the repository | File-tree evidence only; no results read | `packages/evals-runner/`, `packages/harbor-tasks/`, `packages/eval-core/`, `rl/tasks/terminal-bench/run-cloud.ts` |
| Recovery, resume, coordination and parity have dedicated test suites | File-tree evidence only; contents not read | `packages/session-runtime/test/` (`execution-host.test.ts`, `coordination-policy.test.ts`, `settle-batch.test.ts`), `test/integration/recovery-do.test.ts`, `test/integration/long-idle-recovery.test.ts`, `test/integration/session-resume-mcp.test.ts`, `test/integration/parity.test.ts` |
| Session recovery, cancellation and cleanup work reliably across providers | Vendor claim; no measured reliability figures in the inspected files | `README.md` |

## Limitations

- **The "any model, any harness, any sandbox, any cloud" claim is qualified by the README itself.** The qualifier — availability depends on the selected adapters — appears in the same document, and several adapters are explicitly partial: OpenMA's dynamic subagent controls exist on Node only and use single-level delegation, hosted Cloudflare differs, and the Kimi adapter is "a tested protocol subset, not full Hosted Agents parity or a claim of hosted availability".
- **Acceptance evidence is self-reported and locally scoped.** The compatibility report's own closing note states that the tests used a local controlled model and do not count as integration with real OpenAI models or physical sandbox providers. Nothing in the inspected files is an independent reproduction.
- **No reliability measurement.** The inspected files contain no figures for recovery success rate, cancellation correctness, duplicate side-effect rate or recovery latency. The claim that sessions are durable and recoverable is architectural — it is visible in the state machine and the append-only event store — but is not quantified anywhere.
- **Sandbox loss is detected, not repaired.** By design the failed operation is not retried and the caller must decide what to redo; the workspace in the replacement may be older than the files the operation relied on. A team that assumes transparent continuity will be wrong.
- **Credential isolation is conditional.** The README states enforced isolation depends on the provider and runtime profile, and the credential-egress requirement is delegated to the runtime host guide; a self-hosted deployment that misconfigures its provider does not get a safe default.
- **Pre-1.0 internals.** The packages that implement the turn lifecycle and the runtime host are private and versioned `0.1.0`, so their interfaces are not a stability promise; the public surface is the HTTP contract and the SDK.
- **Migration is a project.** v0 and v1 coexist by the architecture document's own statement, and the OpenAI adapter maps onto native OpenMA entities rather than reimplementing them — which means the adapter's limits are the platform's limits at those surfaces.
- **Vendor-controlled throughout.** All sources are first-party. No security review, audit or third-party penetration test is referenced in the inspected files, and 91 open issues were open at the time of review.

## Competing approaches

Only alternatives the repository itself names.

- **Claude Managed Agents (Anthropic).** The README calls OpenMA "an open-source, self-hostable alternative to Claude Managed Agents and OpenAI Agents API", serves the `/v1/*` contract through the official Anthropic SDK, and ships migration material (`apps/web/src/content/blog/migrate-from-claude-managed-agents.md`, `apps/docs/src/content/docs/claude-managed-agents-compatibility.mdx`). Its compatibility page and comparison table live at `apps/web/src/pages/compare.astro` and `apps/web/src/content/components/ComparisonTable.astro`.
- **OpenAI Agents API.** Served at `/openai/v1/*` through a dedicated adapter package (`packages/openai-agents-compat/`) with its own compatibility report, and discussed in `apps/web/src/content/blog/openai-agents-api-self-hosted.md`.
- **Kimi Hosted Agents.** An experimental opt-in adapter at `/kha/v1/*`, compared in `apps/web/src/content/blog/kimi-hosted-agents-vs-openma.md` and `apps/web/src/content/blog/zh/kimi-hosted-agents-vs-openma.md`.
- **OpenMatter.** The README names the separate `openma-ai/OpenMatter` project as implementing a Loop runtime for work events, and states that "Unified Bond/Loop hosting in this OpenMA revision remains a proposed integration" (`docs/adr/0011-matter-bond-and-loop.md`).
- **Not compared.** The repository does not benchmark itself against other self-hosted agent platforms; the comparison material is about API contracts, not measured outcomes.

## Implications

The following is analysis by the KB maintainers, not a claim of the project.

The most interesting design decision visible in the code is the refusal to retry after a lost sandbox. A system that silently re-runs a failed operation after its execution environment has been replaced cannot know whether the first attempt had effects outside that environment — so OpenMA hands the decision back to the agent and reports the replacement explicitly. That is the same instinct as AgentOS's read-only resume allowlist (see [[projects/agentos]]) arriving from the opposite direction: in both cases the framework declines to make the exactly-once promise it cannot keep, and instead makes the ambiguity observable. That is the property to look for in any managed-agent platform, and it is a stronger signal than a durability slogan.

Second, the port/store split is the durable part of the design. With eighteen domain-store families enumerated in the architecture document, each with a memory and a SQL implementation, and Thread Events explicitly defined as a read projection of one append-only event log, the platform avoids the classic failure of an agent system that quietly grows a second source of truth. The rule "resources are a projection of the session, not a second session copy" is worth stealing verbatim as an architectural constraint, because it is the constraint whose absence makes reconciliation impossible later.

Third, the honest framing of "any X" matters more than the slogan. The repository states its own limits in the same breath as its claims, down to a per-adapter note that the OpenAI compatibility limits "do not describe the entire platform" — a sentence most projects in this space would omit. A reader evaluating a platform should look for exactly that sentence; its absence is a warning sign, and its presence is still not a measurement.

Fourth, the compatibility report is worth reading as an artifact in its own right, whatever one thinks of OpenMA. Pinning the external SDK version, fixing an audit date, listing what is covered and what is not, and stating that the tests used a local model rather than the real provider is a rare level of candour for a vendor document. It is also, importantly, a report about contract coverage, not about agent quality: nothing in it says how well an agent completes a task under OpenMA.

Finally, for the KB's own comparison work, OpenMA and [[projects/rivet-agents]] sit on the same axis from opposite ends: Rivet makes the durable process the unit and lets the platform follow from it, while OpenMA makes the managed session the unit and separates harness, sandbox and storage behind adapters. The interesting question for either is the one OpenMA itself names in its sandbox-recovery policy — whether an interrupted operation can be resumed without duplicating an external effect — and neither repository's inspected files answer it with a measurement.

## Reproducible experiment

The central claim worth testing is that a session survives the loss of its execution environment without duplicating side effects, and that the platform reports the ambiguity instead of hiding it. A feasible protocol in a disposable environment, not executed here:

1. **Stand up the smallest deployment.** Use the documented Node/Docker path with an isolated `SANDBOX_PROVIDER`, a scratch database and a test-only model endpoint; confirm readiness with `/health` while recording that, per the README, this proves only server readiness.
2. **Create a session with one side-effecting step.** Configure an agent whose tool appends a unique identifier to a scratch store (a local file in a self-hosted sandbox, or a test bucket). Send a normal message so the session runs end to end, then inspect the session event stream to learn what a completed turn looks like in this deployment's records.
3. **Destroy the sandbox mid-turn.** While the side-effecting tool is in flight, force the sandbox provider to report the sandbox as lost (a stopped provider process is the simplest trigger). Observe whether the platform replaces the sandbox, restores the workspace, and continues from the session event log.
4. **Check the three properties the design promises.** (a) The failed operation is *not* silently retried: there must be an explicit replacement or failure record for it. (b) The side-effecting store contains exactly one copy of the identifier. (c) The turn's final state is distinguishable from a successful turn by an observer reading the event stream rather than the model's prose. A duplicate identifier, a silent retry, or a completion record with no preceding failure record each fail one property.
5. **Compare the two harness placements.** Repeat step 3 with the harness outside the sandbox and with an in-sandbox harness via the ACP adapter, and record whether the session history survives the sandbox failure in each case — the README's stated reason for separating history from both.
6. **Exercise the contract surface, not just the happy path.** With the pinned SDK baselines (`@anthropic-ai/sdk@0.120.0`, `openai@7.15.0`), call a small fixed set of `/v1/*` and `/openai/v1/*` endpoints — create agent, create session, send event, read events, cancel, resume — and check each against the compatibility report's claims, including the cases it says are unsupported. Expect the unsupported ones to fail loudly rather than degrade silently; a silent success on an unsupported path is itself a finding.
7. **Report denominators.** Over at least 20 forced sandbox losses, report duplicate-side-effect rate, explicit-replacement-record rate, and whether the session remained readable afterwards. Keep a note of which failures the platform surfaces versus which the test harness had to infer.

Keep the run disposable: the platform holds model credentials, wallet-style secrets are out of scope, and "no fallback to an unisolated host subprocess" is a claim about the deployment, not a guarantee you should assume after a misconfiguration.

## Evidence status

This page is grounded in files fetched over HTTPS on 2026-11-10 and read: `README.md`, `docs/v1-architecture.md`, `docs/openai-agents-compatibility-status.md`, `packages/session-runtime/src/machine.ts`, `packages/session-runtime/package.json`, `packages/sandbox/src/recovery.ts`, `packages/managed-agents-runtime/package.json`, `apps/agent/src/harness/interface.ts` and `.github/workflows/ci.yml` — all under `https://raw.githubusercontent.com/openma-ai/open-managed-agents/main/`. The repository file tree was read from `https://api.github.com/repos/openma-ai/open-managed-agents/git/trees/main?recursive=1` (5,021 paths, not truncated) and metadata from `https://api.github.com/repos/openma-ai/open-managed-agents`. Claim types are separated above: code-inspected facts come from file contents; the compatibility acceptance counts are vendor-reported and are labelled as such, including the report's own caveat that they used a local controlled model; the Limitations assessment and the whole Implications section are analysis by the KB maintainers. Nothing here was installed, cloned, executed, benchmarked or reproduced by the KB maintainers, no project code was run, and no independent replication of any OpenMA claim is known.

## Historical coverage

- [[briefings/2026/11/2026-11-05]] — finding 7, the dated briefing this record was backfilled from.
- [[evaluations/briefing-synthesis-2026-11-03-to-09]] — the cross-project synthesis that placed this record against [[techniques/multi-agent-orchestration]] and [[projects/agensh]].
