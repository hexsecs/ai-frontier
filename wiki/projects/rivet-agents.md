---
uid: b6a90505-a8d1-4d13-9a40-000000000025
title: "Rivet Agents"
summary: "Rivet's agent infrastructure runs coding agents as durable Actors whose conversations, tool calls and plans persist in the Actor's own SQLite database."
type: project
created: 2026-11-09
updated: 2026-11-10
depth: deep
sources:
  - https://github.com/rivet-dev/agents
  - https://raw.githubusercontent.com/rivet-dev/agents/main/README.md
  - https://raw.githubusercontent.com/rivet-dev/agents/main/packages/pi/package.json
  - https://raw.githubusercontent.com/rivet-dev/agents/main/packages/pi/src/actor.ts
  - https://raw.githubusercontent.com/rivet-dev/agents/main/packages/pi/src/runtime.ts
  - https://raw.githubusercontent.com/rivet-dev/agents/main/packages/pi/src/actions.ts
  - https://raw.githubusercontent.com/rivet-dev/agents/main/packages/pi/src/answers.ts
  - https://raw.githubusercontent.com/rivet-dev/agents/main/packages/pi/src/storage.ts
  - https://raw.githubusercontent.com/rivet-dev/agents/main/packages/pi/src/watches.ts
  - https://raw.githubusercontent.com/rivet-dev/agents/main/packages/pi/src/drain.ts
  - https://raw.githubusercontent.com/rivet-dev/agents/main/packages/sandbox-adapter/package.json
  - https://raw.githubusercontent.com/rivet-dev/agents/main/packages/sandbox-adapter/src/index.ts
  - https://raw.githubusercontent.com/rivet-dev/agents/main/packages/sandbox-adapter/src/agentos.ts
  - https://raw.githubusercontent.com/rivet-dev/agents/main/docs/content/docs/index.mdx
  - https://raw.githubusercontent.com/rivet-dev/agents/main/docs/content/guides/durable-ai-agents.mdx
  - https://raw.githubusercontent.com/rivet-dev/agents/main/docs/content/guides/agent-design-patterns.mdx
  - https://raw.githubusercontent.com/rivet-dev/agents/main/docs/content/guides/run-claude-code.mdx
  - https://raw.githubusercontent.com/rivet-dev/agents/main/.github/workflows/ci.yaml
  - https://api.github.com/repos/rivet-dev/agents
  - https://api.github.com/repos/rivet-dev/agents/git/trees/main?recursive=1
---

# Rivet Agents

## What it is

Rivet Agents is the agent infrastructure published by Rivet in the repository `rivet-dev/agents`, under the Apache-2.0 licence. GitHub describes the repository as "A durable process per agent, with memory that survives restarts"; its topics include `actor-model`, `durable-execution`, `agent-sdk`, `coding-agents`, `pi-agent`, `opencode`, `e2b` and `daytona`. Metadata records creation on 2026-01-25 and a last push on 2026-11-08, with 1,635 stars, 141 forks and 93 open issues at the time of this review.

The root `README.md` frames the repository as "Agent infrastructure from Rivet" and names two products: **Rivet Agents**, which runs agents such as Pi "as durable Rivet Actors" through the packages `@rivet-dev/pi` and `@rivet-dev/sandbox-adapter`, with docs under `docs/`; and **Sandbox Agent**, a separate Rust-and-TypeScript sub-project under `sandbox-agent/` for running coding agents in sandboxes and controlling them over HTTP. The README also records that "Everything in this repository ships on one version line", released by a script under `scripts/release/` that bumps every package, publishes crates and npm packages, uploads binaries and tags `v<version>`.

The inspected packages are versioned `0.5.6`: `@rivet-dev/pi`, described as "Run the Pi coding agent as a durable Rivet Actor", and `@rivet-dev/sandbox-adapter`, "Sandbox providers for agent harnesses running in Rivet Actors". `@rivet-dev/pi` depends on `@earendil-works/pi-coding-agent ~1.5.0` and declares `rivetkit` as a peer dependency at `>=2.3.28 <2.4.0 || ^3.0.0`; both packages require Node `>=22.19.0`. The public surface is an adapter, not a new runtime: the underlying durable harness is Earendil's Pi Durable, and `docs/content/docs/index.mdx` carries the note that "Pi Durable is still in beta, so expect its API to change between releases." The repository tree holds 1,808 paths, including a Rust `sandbox-agent` server, a `foundry` platform UI, and more than 150 files under `examples/docs/` across 33 directories that mirror the guides one for one.

## Mechanism

Each statement below is established by a file read over HTTPS on 2026-11-10; the file is named.

**The unit is an Actor.** `packages/pi/src/actor.ts` exports `pi()`, which "Defines a Rivet Actor that owns one Pi Durable harness". The actor's options carry the Pi Durable registry, models, settings, credentials, sandbox, documents and hooks; the function throws if a `db` option is supplied ("pi() owns the actor database; remove the db option") and throws if no registry is passed; and the app's own actions and lifecycle hooks receive the harness as `c.pi`. Three typed watch events are declared — `pi.view`, `pi.taskGraph`, `pi.doc` — and the actions "match Pi Durable's API one to one", with nested objects becoming dotted action names.

**State lives in the Actor's own database.** `packages/pi/src/runtime.ts` wires Pi Durable's `SqliteStorage` into the actor, so "Pi Durable stores conversations, tasks, and documents in the actor's SQLite database" and a run "can sleep, crash, or upgrade mid-run, and resume when the actor wakes". The same file defines the lifecycle vocabulary: `PiStatus` is `open | sleeping | destroyed`, and `PiStop` is either a sleep with a `drainUntil` deadline or an immediate destroy. `packages/pi/src/drain.ts` sets `DEFAULT_SLEEP_GRACE_PERIOD_MS` to fifteen minutes — "so a running model call or tool call can finish before an upgrade restarts the actor" — and reserves thirty seconds of that grace for closing Pi and suspending the sandbox.

**Its own tables, migrated in place.** `packages/pi/src/storage.ts` defines migrations under the version table `pi_durable_schema_version`: version 1 creates `pi_sandbox` (a singleton row holding the provider name, the sandbox id and its creation time); version 2 creates `pi_durable_watch` keyed by connection id and watch key; version 3 creates `pi_file` (`path`, `content` BLOB, `mtime_ms`) for the file tools of agents without a sandbox; and version 4 renames the pre-0.5.1 Pi Durable tables with the `pi_` prefix, keeping their data.

**Watching is resumable.** `packages/pi/src/watches.ts` defines frame types where "seq 0 carries the view; later frames carry Chord operations", with `value.entries` holding only the newest entries and older pages fetched through `conversation.entries`. Watches are stored in `pi_durable_watch` "so a connection that survives sleep gets its watches back on wake", and a frame with `seq` 0 replaces everything the client had, as after a reattach.

**Action surface.** `packages/pi/src/actions.ts` exposes Pi Durable's `Harness`, `Conversation` and `Submission` methods under `harness`, `conversation` and `submission`, plus a `prompt` convenience action. `PiPromptOptions` documents `requestId` — "Deduplicates retries: a second prompt with the same id returns the first one's submission" — and `whenBusy` of `steer | followUp | reject`; `PiPromptResult` is either `done` (with the answer's text and the submission id) or `unanswered` (with Pi's reason, "such as a model error").

**Exactly-once is offered, not guaranteed.** `docs/content/guides/durable-ai-agents.mdx` states the intended semantics: Pi "saves each model call and tool call to the Actor's SQLite database before the next one starts, so there is no separate workflow engine, queue, or database to run", and a crash, deploy or restart "loses at most about the last second of streamed text". For tools, the contract is explicit and is the part worth quoting: a read-only tool sets `replay: "safe"` and "simply runs again"; a mutating tool must use `api.memo` to "save an idempotency key with the tool call before the booking, and a rerun gets the same key", so the target API returns the first booking; and "A tool without `replay: "safe"` isn't run again. The model gets a result saying the call stopped partway and decides what to do." Multi-step work is expressed as a task, which "saves a checkpoint after each step and resumes from the last one". The same at-least-once care appears in `packages/pi/src/answers.ts`, where the `onAnswer` hook is guarded by an `api.memo` keyed on the response id — "A run that resumes after a crash yields the same answer again" — so the hook fires once per answer even across a resume.

**Sandboxes are a separate, replaceable seam.** `packages/sandbox-adapter/src/index.ts` defines the `Sandbox` interface (`exec`, `readFile`, `writeFile`, `mkdir`, `stat`, `readdir`, `exists`, absolute paths, an absolute `cwd`) and the `SandboxProvider` interface (`create`, `connect`, optional `suspend`, optional `destroy`, plus a `name` that is "Stored next to the sandbox id so a changed provider is detected on wake"). Provider implementations are `e2b.ts`, `daytona.ts`, `docker.ts`, `freestyle.ts` and `agentos.ts`; the package's exports and optional peer dependencies (`e2b`, `@daytonaio/sdk`, `freestyle`) match that list.

**Running an external coding agent.** The `docs/content/guides/run-*.mdx` family (`run-claude-code`, `run-codex`, `run-opencode`, `run-amp`) describes a second, thinner pattern: one Actor per session keyed by the session id, a sandbox that installs the CLI itself, and the harness driven through `exec`. For Claude Code the guide uses `claude -p` with `--output-format stream-json` and `--verbose`, and `--resume` to continue Claude Code's own session stored under `~/.claude` inside the sandbox. The guide is explicit about the security trade: `--dangerously-skip-permissions` is used "because nobody is there to approve them. The sandbox is the boundary", and the provider key is passed only in the `env` of a single `exec` call — though "code in the sandbox can read it. Give the sandbox a key with a spending limit."

**Keying.** `docs/content/guides/agent-design-patterns.mdx` makes the key the design decision: per user, per thread, or per task, with "an action that calls `c.destroy()` deletes the agent and its sandbox".

**A naming collision to avoid.** `packages/sandbox-adapter/src/agentos.ts` implements a provider named `agentos` that calls "the Services agentOS actor" through `c.client().agentOS.getOrCreate(["sandbox", actorId], ...)`, with the VM's files kept in that actor's SQLite. This is Rivet's own agentOS actor service, not the `use-agent-os/agent-os` project catalogued at [[projects/agentos]]; the two must not be conflated.

## Evidence

| Claim | Status | Where |
|---|---|---|
| Each agent is an Actor whose harness state lives in the Actor's SQLite | Code-inspected | `packages/pi/src/actor.ts`, `packages/pi/src/runtime.ts`, `docs/content/docs/index.mdx` |
| The adapter owns its own tables and migrates them without losing data | Code-inspected | `packages/pi/src/storage.ts` (versions 1–4) |
| Watches survive sleep and are reattached on wake | Code-inspected | `packages/pi/src/watches.ts`, `packages/pi/src/storage.ts` |
| A retried `prompt` with the same `requestId` returns the first submission | Code-inspected | `packages/pi/src/actions.ts` |
| The answer hook does not fire twice after a crash resume | Code-inspected | `packages/pi/src/answers.ts` (`api.memo` guard) |
| Sleep drains for up to fifteen minutes so an in-flight call can finish | Code-inspected | `packages/pi/src/drain.ts` |
| Tool replay policy is explicit: `replay: "safe"`, or `api.memo` for an idempotency key, or neither and the model decides | Documentation claim plus code-inspected `api.memo` usage | `docs/content/guides/durable-ai-agents.mdx`, `packages/pi/src/answers.ts` |
| Sandbox providers are pluggable and the provider identity is persisted with the sandbox id | Code-inspected | `packages/sandbox-adapter/src/index.ts`, `packages/sandbox-adapter/package.json` |
| CI builds, type-checks, tests, boundary-checks and lints both packages, and runs the Rust and SDK test suites | Code-inspected | `.github/workflows/ci.yaml` (`pnpm build`, `check-types`, `test`, `check-boundaries`, `lint`, `npm pack --dry-run`, `pnpm test:packed`, `cargo test` for four sandbox-agent targets, SDK tests) |
| Unit tests exist for the actor, storage, watches, upgrades, wake-while-busy, credentials and tracing | File-tree evidence only; contents not read | `packages/pi/tests/` (`actor.test.ts`, `storage.test.ts`, `watch.test.ts`, `upgrade.test.ts`, `upgrade-from-published.test.ts`, `wake-while-busy.test.ts`, `on-answer.test.ts`, `connection-hooks.test.ts`, `credentials.test.ts`, five `tracing*.test.ts`) |
| Worked examples exist for every documented guide | File-tree evidence only | `examples/docs/` (162 files across 33 directories) |
| The Sandbox Agent sub-project is a separate Rust and TypeScript stack with its own SDKs and vendored platform binaries | File-tree evidence only | `sandbox-agent/server/packages/*` (58 Rust files), `sandbox-agent/sdks/{typescript,react,cli,acp-http-client,persist-sqlite,persist-postgres,persist-indexeddb,persist-rivet}`, `sandbox-agent/sdks/gigacode/platforms/*/bin/gigacode` (prebuilt 15–22 MB binaries committed to the tree) |
| "A crash … loses at most about the last second of streamed text" | Vendor documentation claim; no measurement in the inspected files | `docs/content/guides/durable-ai-agents.mdx` |
| Agents are more reliable or cheaper than a non-durable loop | No evidence in the inspected files: no benchmark, no ablation, no comparative measurement | — |

## Limitations

- **Exactly-once for external effects is delegated to the application.** The framework gives the tools (`api.memo`, `replay: "safe"`) and the model a message that the call stopped partway; it does not reconcile an ambiguous side effect, and a tool without `replay: "safe"` is simply not re-run. This is a deliberate, documented boundary, but it means the durability guarantee covers *local* state, not the outside world.
- **Durability rests on an upstream beta.** The harness is Earendil's Pi Durable, which `docs/content/docs/index.mdx` states is "still in beta", pinned here to `~1.5.0`. The adapter's own version `0.5.6` is pre-1.0, and the whole repository ships on one version line, so a Pi Durable change propagates here.
- **The "last second" figure is documentation, not measurement.** The claim that a crash loses at most about the last second of streamed text is stated in prose; no test in the inspected files measures recovery latency, and the tree contains no benchmark suite or comparative evaluation.
- **The provider key is exposed to sandboxed code.** The Claude Code guide warns that "code in the sandbox can read it" and advises a spending-limited key; permissions are skipped deliberately with the sandbox as the only boundary. A reader who treats "provider keys never enter the sandbox" as absolute would be misreading the guide.
- **Coverage is narrower than the product surface.** The `run-*` guides cover Claude Code, Codex, OpenCode and AMP; ACP harnesses in the `sandbox-agent` sub-project are a separate Rust implementation with its own test matrix.
- **Actor semantics are RivetKit's, not this repository's.** Lifecycle, sleeping, keying and the SQLite-per-actor model come from `rivetkit` and Pi Durable; this repository is the integration layer, so a claim about Rivet Agents is partly a claim about two dependencies.
- **Two products, one repository.** `packages/` is the Rivet Agents line (TypeScript); `sandbox-agent/` is a distinct Rust server with a `foundry` platform UI and its own SDKs. They are released on one version line but share no implementation, so evidence about `@rivet-dev/pi` does not transfer to Sandbox Agent and vice versa. `sandbox-agent/research/specs/` holds design notes rather than measurements.
- **No independent verification.** Everything inspected is first-party, no security review or audit is referenced, and 93 issues were open at the time of review.

## Competing approaches

Only alternatives the repository itself names.

- **Pi Durable itself** (`@earendil-works/pi-durable`, `earendil.com/posts/pi-durable`) is the underlying harness; this repository's contribution is running it inside a Rivet Actor, not replacing it.
- **Other coding agents as the harness** — Claude Code, Codex, Gemini CLI, Cursor, Copilot, OpenCode and AMP — are supported through the `run-*` guides and, in `sandbox-agent`, through ACP-compatible adapters with an `opencode-adapter` and an `acp-http-adapter`.
- **Sandbox providers** — E2B, Daytona, Docker, Freestyle, and Rivet's own `agentos` actor service — are alternatives to one another within `packages/sandbox-adapter`; the `agentos` provider is a different product from [[projects/agentos]].
- **Comparison material** in the repository is about APIs and platforms (the `sandbox-agent` website pages, `docs/content/docs/` reference material), not about measured agent outcomes; no benchmark against another agent framework is present.

## Implications

The following is analysis by the KB maintainers, not a claim of the project.

The most useful idea here is the *separation of local durability from external idempotency*. Rivet makes the local state strong — every model call and tool call is written to the Actor's SQLite before the next begins, and the Actor sleeps and wakes with its conversation intact — and then refuses to extend that strength to the outside world. `replay: "safe"` for reads, `api.memo` for writes, and "the model decides what to do" for the ambiguous middle is a three-way classification of side effects that is more honest than a single exactly-once promise, and it maps directly onto [[concepts/verified-completion-vs-apparent-success]]: the framework's job is to make the ambiguous case *visible* rather than to guess it.

Second, the actor-per-key design is a genuinely useful operational primitive. The guide's "one agent per key" pattern — per user, per thread, per task, with `c.destroy()` cleaning up the agent and its sandbox — means isolation is a key-selection decision rather than an infrastructure project, and it makes the "which conversation does this message continue?" question answerable in one line. That is a better default than a single long-lived session with a growing transcript.

Third, the choice to store the *harness* in the same database as the application state, and to expose it as `c.pi`, removes a whole class of integration failure: there is no separate workflow engine, queue or database to run. The counterweight is that the boundary between "application code" and "agent state" becomes thin, so a team that wants independent scaling or independent durability of the two must add machinery the default design does not.

Fourth, the security posture deserves reading closely rather than skimming. The guide's `--dangerously-skip-permissions` with "the sandbox is the boundary" and a provider key that sandboxed code can read is an honest statement of a trade-off, not a hidden one. It also means the blast radius of a sandbox escape equals the blast radius of the provider key — a constraint that belongs in a deployment's threat model, and that the guide itself helps to write.

Finally, for comparison work, this project and [[projects/openma]] sit on the same axis from opposite ends. Rivet makes the durable process the primitive and asks you to accept its actor semantics; OpenMA separates session, execution and recovery behind adapters and asks you to accept its port boundaries. Both refuse the exactly-once promise for external effects — the honest position — and neither inspected file measures how often the ambiguous branch is actually taken. That measurement gap, rather than either architecture, is the more interesting frontier.

## Reproducible experiment

The claim worth testing is the one the framework is careful about: *local agent state survives a crash, and an interrupted side effect is surfaced rather than silently replayed*. A feasible protocol in a disposable environment, not executed here:

1. **Stand up a minimal agent.** Use one of the documented examples (`examples/docs/durable-ai-agents/`), a disposable database, and a provider key with a spending limit. Give the agent two tools: a read-only one marked `replay: "safe"`, and a mutating one that appends a unique identifier to a scratch store and records the identifier with `api.memo` before the write.
2. **Crash at four points.** Kill the worker (a) between the model call and the tool call, (b) during the mutating tool after the write but before the result is recorded, (c) during the mutating tool before the write, (d) during a sleep/drain cycle triggered by an upgrade.
3. **Check the local state first.** After restart, verify from the Actor's SQLite tables that the conversation and the plan survived, that the tool round is present, and that the watch a connected client held is reattached rather than lost. This is the framework's own claim and should be checked directly, not inferred from prose.
4. **Check the external state second.** The scratch store must contain exactly one copy of the identifier in cases (b) and (c). A duplicate is a failure of the `api.memo` contract; a missing write with an explicit "stopped partway" result is the documented behaviour and a pass.
5. **Check the ambiguous branch explicitly.** Force the model to call the mutating tool *without* `replay: "safe"` and without `api.memo`, then crash mid-call. The pass criterion is the framework's: the tool is not re-run, and the transcript contains a result telling the model the call stopped partway, so the decision is the agent's. Verify that by reading the transcript, not by reading the final reply.
6. **Check the answer hook.** Install an `onAnswer` hook that appends to a log, then crash after an answer is produced but before it is delivered. The log must contain one entry per answer, not two, because the `api.memo` guard in `packages/pi/src/answers.ts` is keyed on the response id.
7. **Control for the drain path.** Separately, trigger a sleep with an in-flight call and confirm the fifteen-minute grace behaviour: the call finishes, then the Actor sleeps, then a new prompt wakes it with the same conversation. Report whether the wake was automatic or needed an explicit request.
8. **Report denominators.** Over at least 20 crashes per point, report duplicate-side-effect rate, correct unknown-outcome rate, conversation-survival rate and time-to-resume. Do not report a mean latency without the count of runs that did not recover at all.

Run this entirely against scratch state and a spending-limited key; the interesting failures will be in the ambiguous branch, not the happy path.

## Evidence status

This page is grounded in files fetched over HTTPS on 2026-11-10 and read: `README.md`, `packages/pi/package.json`, `packages/pi/src/actor.ts`, `runtime.ts`, `actions.ts`, `answers.ts`, `storage.ts`, `watches.ts` and `drain.ts`, `packages/sandbox-adapter/package.json`, `packages/sandbox-adapter/src/index.ts` and `src/agentos.ts`, `docs/content/docs/index.mdx`, `docs/content/guides/durable-ai-agents.mdx`, `docs/content/guides/agent-design-patterns.mdx`, `docs/content/guides/run-claude-code.mdx` and `.github/workflows/ci.yaml` — all under `https://raw.githubusercontent.com/rivet-dev/agents/main/`. The repository file tree was read from `https://api.github.com/repos/rivet-dev/agents/git/trees/main?recursive=1` (1,808 paths, not truncated) and metadata from `https://api.github.com/repos/rivet-dev/agents`. Claim types are separated above: code-inspected facts come from file contents; the "loses at most about the last second" figure and the tool-replay semantics are vendor documentation claims; the Limitations assessment and the whole Implications section are analysis by the KB maintainers. Nothing here was installed, cloned, executed, benchmarked or reproduced by the KB maintainers, no project code was run, and no independent replication of any Rivet claim is known.

## Historical coverage

- [[briefings/2026/11/2026-11-05]] — finding 5, the dated briefing this record was backfilled from.
- [[evaluations/briefing-synthesis-2026-11-03-to-09]] — the cross-project synthesis that placed this record against [[projects/agentos]] and [[projects/builderio-agent-native]].
