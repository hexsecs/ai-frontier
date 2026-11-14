---
uid: b6a90305-a8d1-4d13-9a40-000000000005
title: "AgentOS"
summary: "Local-first Python agent runtime with one gateway, an on-device model router, a deterministic sandbox policy and crash recovery with read-only resumes."
type: project
created: 2026-11-09
updated: 2026-11-10
depth: deep
sources:
  - https://github.com/use-agent-os/agent-os/blob/main/RELEASES.md
  - https://raw.githubusercontent.com/use-agent-os/agent-os/main/RELEASES.md
  - https://raw.githubusercontent.com/use-agent-os/agent-os/main/README.md
  - https://raw.githubusercontent.com/use-agent-os/agent-os/main/pyproject.toml
  - https://raw.githubusercontent.com/use-agent-os/agent-os/main/docs/tools-and-sandbox.md
  - https://raw.githubusercontent.com/use-agent-os/agent-os/main/.github/workflows/ci.yml
  - https://raw.githubusercontent.com/use-agent-os/agent-os/main/src/agentos/tools/dispatch.py
  - https://raw.githubusercontent.com/use-agent-os/agent-os/main/src/agentos/tools/policy/finalize.py
  - https://raw.githubusercontent.com/use-agent-os/agent-os/main/src/agentos/engine/outcome.py
  - https://raw.githubusercontent.com/use-agent-os/agent-os/main/src/agentos/engine/loop_guard.py
  - https://raw.githubusercontent.com/use-agent-os/agent-os/main/src/agentos/engine/turn_runner/outcome.py
  - https://raw.githubusercontent.com/use-agent-os/agent-os/main/src/agentos/gateway/turn_recovery.py
  - https://raw.githubusercontent.com/use-agent-os/agent-os/main/src/agentos/gateway/idempotency.py
  - https://raw.githubusercontent.com/use-agent-os/agent-os/main/src/agentos/sandbox/policy.py
  - https://raw.githubusercontent.com/use-agent-os/agent-os/main/src/agentos/engine/history.py
  - https://raw.githubusercontent.com/use-agent-os/agent-os/main/tests/test_engine/test_tool_pairing_unknown_outcome.py
  - https://raw.githubusercontent.com/use-agent-os/agent-os/main/tests/test_gateway/test_idempotency.py
  - https://api.github.com/repos/use-agent-os/agent-os
  - https://api.github.com/repos/use-agent-os/agent-os/git/trees/main?recursive=1
---

# AgentOS

## What it is

AgentOS is a local-first agent runtime published as the Apache-2.0 Python distribution `use-agent-os` by the GitHub organisation `use-agent-os` (repository `use-agent-os/agent-os`, described by GitHub as "The Open Agent Operation System"). Repository metadata records creation on 2026-07-13 and a last push on 2026-11-10; at the time of this review it carried 78 stars, 55 forks and 12 open issues, with Python as the primary language.

`pyproject.toml` declares the name `use-agent-os`, version `2026.11.11`, `requires-python = ">=3.12"` and the classifier `Development Status :: 3 - Alpha`. Versioning is calendar-versioned by release date, and `README.md` names "AgentOS 2026.11.11" as the current release. `RELEASES.md` is a dated changelog table whose top row is version 2026.11.11 with date 2026-11-11 — one day after the date of this review, so the release string runs ahead of the review date and only the file's own date column is evidence for it.

The product is an end-user agent: one local gateway, a signed macOS desktop app, a web UI, a CLI and chat-channel adapters, plus a "Pilot Router" that classifies each message on-device and routes it to the cheapest capable model. The README's own framing is "local-first agentic trading, minimum tokens", and a large share of the released surface is crypto-trading — wallets, swaps, DCA mandates, stop-loss and take-profit triggers, a Markets tab. The repository also states that AgentOS "is built on OpenSquilla (Apache-2.0) and influenced by OpenClaw and Hermes Agent".

Maturity signals visible in the tree: a large Python package with its own SQL migration series (`migrations/V001__initial_schema.py` through `V015__subagent_wakes.py`), separate TypeScript front ends (`frontend/`, `desktop/`), a Python wheel plus desktop release workflows, and a CI job that lints, type-checks and tests. `pyproject.toml` documents a dependency upper-bound policy that `tests/test_packaging/test_pyproject_invariants.py` is said to recompute from `uv.lock`, so a drifting bound fails CI. No inspected file reports a measured success rate, latency or reliability figure for any agent behaviour; the only quantitative material available is release-note text and README prose.

## Mechanism

Each statement below is established by a file read over HTTPS on 2026-11-10; the file is named.

**Process shape — one gateway, one turn loop.** `README.md` describes a single local web server on `127.0.0.1:18791` built with Starlette, serving a control UI at `/control/`, handling sessions, approvals and scheduling, with the Web UI, CLI, terminal, WebSocket, Slack, Telegram and Discord clients all sharing one `TurnRunner` engine. The tree matches that shape: `src/agentos/engine/turn_runner/` holds the stages (`agent_bootstrap_stage.py`, `history_load_stage.py`, `input_stage.py`, `prompt_assembler_stage.py`, `provider_and_tools_stage.py`, `stream_consumer_stage.py`, `turn_finalizer_stage.py`, `pre_provider_io.py`), and `src/agentos/engine/turn_runner/outcome.py` defines the universal stage return type `StageOutcome`, whose docstring fixes three invariants — terminate implies an early-yield event and no output, success implies output and no early yield, and the value is frozen.

**Routing.** `src/agentos/agentos_router/` implements the on-device Pilot Router (`pilot/strategy.py`, `pilot/model.py`, `task_type.py`, `tiers_util.py`), with the model bundle under `src/agentos/agentos_router/models/pilot_v1/`; `src/agentos/router_strategies.py` and `src/agentos/router_control.py` expose the strategy choice (`pilot-v1` default, `llm_judge` alternative, disabled). `README.md` states the router picks one of four tiers (c0–c3) from message length, language, code, keywords and meaning, and that when the Git-LFS weights are missing it "degrades gracefully — it logs a warning at boot and pins every turn to the default tier (c1) rather than crashing".

**Tool dispatch — one fixed pipeline.** `src/agentos/tools/dispatch.py` documents its own pipeline in the module docstring: an ingress injection guard (implemented in `src/agentos/safety/injection_guard.py`, whose refusal reason for a tool call inside untrusted content the dispatcher imports), then registry lookup with near-miss name resolution, then argument admission (schema validation with lossless coercions), then an optional `ToolHook.before_tool` fan-out, then the policy chain where "first denial wins", then handler dispatch, then a single finalisation point, then `ToolHook.after_tool`, then context reset. `src/agentos/tools/policy/finalize.py` is that finalisation point and is the only place that mints execution status for a tool result, branching on exception, approval-pending on an unsupported surface, denial payload and success. `docs/tools-and-sandbox.md` gives the admission rules in prose: an exact name always wins; a decorated name resolves only when the match is unique; MCP names are never matched loosely; arguments are validated against the tool's schema, lossless mistakes are repaired ("5" for an integer, "true" for a boolean, a JSON-encoded string where an array is expected), and anything else is rejected without running the tool with `error_class: "ToolArgumentsRejected"`.

**Turn outcome taxonomy.** `src/agentos/engine/outcome.py` normalises every failure into one of six kinds — completed, partial, budgetLimited, blocked, failed, interrupted — from fixed code sets. `loop_detected`, `repetition_detected`, `max_iterations` and `tool_failure_loop_exhausted` are "partial"; `approval_required`, `tool_policy_denied`, `request_vetoed` and `sandbox_threshold_exceeded` are "blocked"; `cancelled`, `timeout` and `dropped_by_overflow` are "interrupted"; and a configured spend refusal (`budget_exceeded`) is "budgetLimited".

**Loop control.** `src/agentos/engine/progress_watchdog.py` decides and `src/agentos/engine/loop_guard.py` applies: a `warn` appends guidance to the tool results that triggered it, a `block` answers every call of the proposed batch with a synthetic error result without running it, and a terminal block ends the turn with the error code `loop_detected`. `LOOP_GUARD_MODES` is `("enforce", "observe")`, and `[tools] loop_guard = "observe"` turns enforcement off, leaving decisions only in the turn call log.

**Unknown tool outcomes.** `src/agentos/engine/history.py` provides `repair_tool_pairing`, `UNKNOWN_TOOL_OUTCOME_TEXT` and `is_unknown_tool_outcome_result`. `tests/test_engine/test_tool_pairing_unknown_outcome.py` shows a trailing tool call with no recorded result receiving a synthetic error result carrying that text, orphan and foreign results being dropped, the repair being deterministic across reloads, and the repaired history being accepted by both the Anthropic and the OpenAI payload builders.

**Crash recovery.** `src/agentos/gateway/turn_recovery.py` resumes turns cut short by a restart or crash. Its docstring fixes the policy: the interrupted task is marked `shutdown_interrupted` or `process_restart`; the transcript tail decides whether to close the turn, resume normally, or resume with a restricted replay-safe tool set; that set is an allowlist (`RESTART_SAFE_TOOL_ALLOW`) whose entries must also be registered `read_only=True`; a resume is a synthetic continuation turn run in a recovery lane of `RECOVERY_LANE_CONCURRENCY = 4` with the interrupted run's id as its idempotency key; a recovery cycle makes at most `MAX_ATTEMPTS = 3` attempts with backoff `(2.0, 15.0, 60.0)` seconds; a turn older than `MAX_AGE_MS` (24 hours) is not resumed; and cron, heartbeat, subagent and ACP turns are never resumed. `src/agentos/gateway/turn_recovery_route.py` and `src/agentos/engine/turn_progress.py` supply the tail classification.

**Idempotency.** `src/agentos/gateway/idempotency.py` answers by `(method, idempotency_key)` for a TTL and a size cap; the same key with a different request body is refused as `INVALID_REQUEST` with `details.code: "REQUEST_CONFLICT"`; concurrent duplicates share the first call; a failed call is not remembered; entries whose named side effect is still live are pinned beyond both TTL and cap; and the cache is per gateway process, with `chat.send` and `sessions.send` additionally recording the key on the task they start so a retry after a restart finds the turn instead of re-running it. `tests/test_gateway/test_idempotency.py` asserts each of these behaviours.

**Sandbox.** `src/agentos/sandbox/policy.py` exposes two pure functions: `select_level` (action kind plus a flat `LevelHints` dataclass → `SecurityLevel`) and `build_policy` (level + workspace + settings → a materialised `SandboxPolicy`). The rule table favours escalation — an untrusted source starts at STRICT, a trust-boundary crossing escalates to LOCKED, plain filesystem reads stay at STANDARD, and DISABLED is reachable only by explicit configuration, never by inference. Resource limits scale down with the level (STRICT halves CPU, memory and wall time and pins pids to 128; LOCKED cuts further). Backends live in `src/agentos/sandbox/backend/` (`bubblewrap.py`, `seatbelt.py`, `noop.py`); `README.md` states Bubblewrap is used on Linux, Apple's `sandbox-exec` (Seatbelt) on macOS, and that "Windows does not have this sandbox yet".

**Persistence and state.** State lives in SQLite: `src/agentos/session/`, `src/agentos/gateway/transcripts.py`, `src/agentos/engine/history.py` and the migration series under `migrations/`. Memory is a `MEMORY.md` plus dated Markdown notes, searchable by keyword (SQLite full-text) and by meaning (`sqlite-vec` with an on-device ONNX model under `src/agentos/memory/models/`).

**Configuration surfaces.** `README.md` fixes the config resolution order — `AGENTOS_GATEWAY_CONFIG_PATH` → `./agentos.toml` → `~/.agentos/config.toml` → built-in defaults — with secrets from environment variables always winning over files. `src/agentos/gateway/config.py` implements it and `tests/test_gateway/test_config_reload.py` covers hot reload. Upgrades are described as running config migrations at gateway start and writing a timestamped backup before rewriting any file; the CLI compares CLI and gateway versions once per run, warns when the gateway is older and refuses a newer gateway unless `AGENTOS_ALLOW_VERSION_SKEW=1`.

## Evidence

| Claim | Status | Where |
|---|---|---|
| Tool dispatch is one ordered pipeline with a single finalisation point | Code-inspected | `src/agentos/tools/dispatch.py`, `src/agentos/tools/policy/finalize.py` |
| Unanswered tool calls are repaired to an explicit unknown-outcome result | Code-inspected, test-asserted | `src/agentos/engine/history.py`, `tests/test_engine/test_tool_pairing_unknown_outcome.py` |
| A crash-restarted turn resumes with a read-only tool allowlist | Code-inspected | `src/agentos/gateway/turn_recovery.py` |
| A retried RPC with the same idempotency key does not run twice | Code-inspected, test-asserted | `src/agentos/gateway/idempotency.py`, `tests/test_gateway/test_idempotency.py` |
| Sandbox level selection is deterministic and escalates on untrusted input | Code-inspected | `src/agentos/sandbox/policy.py` |
| Lint, type-check and pytest run on pushes and pull requests | Code-inspected | `.github/workflows/ci.yml` (`ruff check src tests`, `mypy src/agentos`, `pytest tests -q`, `actionlint`, a metric-counter guard) |
| Separate release and front-end workflows exist | Code-inspected | `desktop-release.yml`, `wheelhouse-release.yml`, `frontend.yml`, `llm-e2e.yml` |
| A dispatch corpus with snapshot expectations and a memory benchmark baseline exist | File-tree evidence only, contents not read | `tests/test_tools/dispatch_corpus/`, `tests/test_tools/__snapshots__/test_dispatch_corpus_snapshots.ambr`, `tests/data/memory_bench/BASELINE.md` |
| The 2026-10-27 release added dispatch hardening, loop guard, unknown-outcome persistence and read-only resume | Release-note claim; matching code exists but the notes are the only link between the two | `RELEASES.md` rows 2026.10.27 and 2026.10.27.post1 |
| The 2026-11-02 release added agent-created image flows with `base_rev` conflict checks and cost-gated run overrides | Release-note claim | `RELEASES.md` row 2026.11.2 |
| "Saves tokens, so it costs less to run" | Vendor claim; no measurement, benchmark harness or evaluation result in the inspected files | `README.md` |
| The three-level sandbox keeps tool use safe | Vendor claim plus a code-inspected policy function; no adversarial evaluation present | `README.md`, `src/agentos/sandbox/policy.py` |
| Provider failures are retried within a budget before failing over to the next model | Release-note claim ("up to 6 attempts within 90 s") | `RELEASES.md` row 2026.11.11 (#3825) |
| Tool output and MCP results are treated as untrusted content | Code-inspected plus a release note | `src/agentos/safety/injection_guard.py`, `src/agentos/mcp/discovery.py`; `RELEASES.md` row 2026.10.13 (#3645) |

## Limitations

- **No evaluation of any kind.** The inspected files contain no benchmark, no success-rate table and no ablation for the router, the loop guard, the recovery path or the sandbox policy. The `RELEASES.md` rows and the README are release notes and marketing prose; the one benchmark-shaped artefact in the tree (`tests/data/memory_bench/BASELINE.md`) was not read and is a test fixture, not a published result.
- **Alpha by the project's own classifier.** `pyproject.toml` carries `Development Status :: 3 - Alpha`; the README documents frequent behaviour changes (a rebuilt Control UI, renamed CLI surfaces, renamed tool names such as `functions.Read_File:0` being tolerated).
- **Coverage is uneven by platform and by surface.** Windows has no sandbox; `docs/tools-and-sandbox.md` states the browser tool "Runs outside the sandbox" because Chromium cannot run inside bubblewrap or seatbelt, and that ACP harnesses run as the gateway user outside the sandbox with their own permission mode. The security claim therefore does not cover every tool the agent can reach.
- **Recovery is deliberately partial.** Only user-facing sources (`web`, `cli`, `channel`) are resumed; cron, heartbeat, subagent, ACP and memory-nudge turns are never resumed, and turns older than 24 hours are not resumed. An interrupted scheduled job therefore needs the scheduler's own re-run, not the recovery path.
- **Idempotency is per-process and per-surface.** The cache does not survive a gateway restart, and only the RPC methods that record the key on their task survive one. A tool that performs an external side effect without such a key is outside this mechanism entirely.
- **The router can silently degrade.** Without the LFS weights the router pins every turn to one tier, which turns a routing claim into a single-model deployment without failing loudly.
- **No independent verification.** Nothing on this page has been reproduced by a third party; the repository is vendor-controlled end to end (release notes, README, docs and code), and no security review, audit or penetration report is referenced in the inspected files.

## Competing approaches

Only alternatives the repository itself names.

- **Code base and lineage.** The README's Credits section states AgentOS "is built on OpenSquilla (Apache-2.0) and influenced by OpenClaw and Hermes Agent", and other bundled code is credited in `THIRD_PARTY_NOTICES.md` and `NOTICE`.
- **Migration path.** `README.md` documents `agentos migrate openclaw --json|--apply` and `agentos migrate hermes`, with `MIGRATION.md` describing custom paths and conflict handling, and the migration surface is implemented under `src/agentos/migration/`.
- **Provider layer.** OpenRouter is the default; the README lists the Bankr LLM Gateway, OpenCAP, Surplus Intelligence, OpenAI, Anthropic, Ollama, DeepSeek, Gemini, DashScope/Qwen and "20+ other providers", with routing either local (`pilot-v1`) or by a small model call (`llm_judge`).
- **Harness layer.** `RELEASES.md` (row 2026.10.16) and `docs/acp-agents.md` describe handing coding work to Claude Code, Codex, Gemini CLI, Cursor, Copilot, OpenCode and 20+ other coding harnesses over the Agent Client Protocol via `sessions_spawn(runtime="acp")`.
- **Not compared.** The repository names no competing open-source agent runtime with a feature or benchmark comparison, and contains no head-to-head measurement against another framework.

## Implications

The following is analysis by the KB maintainers, not a claim of the project.

The most transferable idea visible here is the *shape* of the recovery contract rather than the recovery itself: an interrupted tool call is modelled as a third state — completed, not completed, unknown — and the unknown case is answered by removing authority rather than by retrying. The code shows this literally: unknown-outcome calls get a synthetic error result so the transcript stays well-formed, and a resumed turn is handed a read-only allowlist so it can inspect what happened instead of repeating the action. That is a concrete instance of [[concepts/verified-completion-vs-apparent-success]] at the level of an execution log, and it is worth copying even by teams that do not adopt AgentOS.

Second, the separation of *decision* from *application* is clean and cheap: `progress_watchdog` decides, `loop_guard` applies, and a single configuration value (`loop_guard = "observe"`) turns the whole mechanism into telemetry. Being able to run a safety control in shadow mode before enforcing it is a design detail most agent runtimes lack, and it is the precondition for trusting it in production.

Third, the single-finalisation-point rule for tool results is an under-appreciated invariant. Because exactly one function mints execution status, a reader can reason about "was this call truncated, denied, blocked or merely failed" from the record alone. Any harness that lets several call sites decide error semantics will make post-hoc verification of what an agent actually did much harder.

Fourth, the trade the project makes is instructive in the other direction: coverage is uneven, and the README is candid about it (no Windows sandbox, browser and ACP harnesses outside the sandbox). An operator reading only the marketing summary would over-estimate the containment. The engineering lesson is to enumerate, per surface, where the authority boundary actually is — and to treat the gap between the boundary and the tool list as the real risk surface.

Finally, nothing here measures reliability. The release-note cadence is fast and the change surface is wide, so a prospective adopter should assume API churn and treat the recovery and policy semantics as the durable, reviewable part — the part worth reading closely, because it is the part that survives a refactor.

## Reproducible experiment

The central claim worth testing is not the routing but the recovery contract: *an interrupted tool call is resumed without duplicating external effects*. A feasible protocol in a disposable environment, not executed here:

1. **Prepare a disposable agent with one genuinely side-effecting tool.** Install AgentOS from the published wheel, configure a provider key for a sandboxed test account, and add a tool that appends a unique line to a local file (or calls a test-only endpoint) and then sleeps before returning. Record the line's identity.
2. **Crash at three points.** Kill the gateway process (a) after the tool has performed its side effect but before its result is recorded, (b) between the tool dispatch and the side effect, (c) during a batch of parallel calls so some results exist and others do not.
3. **Check the transcript, not the prose.** After restart, verify from the persisted transcript and tool rows that: the unanswered call is present as an explicit unknown-outcome result rather than a silent absence; the resumed turn is recorded as a synthetic continuation; and the tools available to it are the read-only allowlist.
4. **Verify the postcondition independently.** Confirm the side-effecting file contains exactly one line for the interrupted call. A duplicate is a failure of the claim; a missing line with an unknown outcome recorded is a pass.
5. **Control the retry path.** Repeat with `agentos upgrade` (which restarts the managed gateway) instead of a kill, and with two concurrent clients sending the same `chat.send` with the same `idempotency_key` and the same body, then the same key with a different body. Pass criteria: the identical body replays the first answer without starting a second turn; the differing body is refused with `REQUEST_CONFLICT`; the differing body produces no side effect at all.
6. **Report counts, not anecdotes.** Across at least 20 injected crashes per point, report duplicate-side-effect rate, unknown-outcome recording rate, time to resume, and the number of turns that resumed with a non-read-only tool (which would be a contract violation). A single duplicate is enough to falsify the "no duplicated external effects" reading, so the denominator matters more than the mean.

Do not run this against a production wallet, trading desk or any credential that can move money; the README's own trading surface makes that risk real.

## Evidence status

This page is grounded in files fetched over HTTPS on 2026-11-10 and read in full: `README.md`, `RELEASES.md` (the dated changelog table), `pyproject.toml`, `docs/tools-and-sandbox.md`, `.github/workflows/ci.yml`, `src/agentos/tools/dispatch.py`, `src/agentos/tools/policy/finalize.py`, `src/agentos/engine/outcome.py`, `src/agentos/engine/loop_guard.py`, `src/agentos/engine/turn_runner/outcome.py`, `src/agentos/engine/history.py`, `src/agentos/gateway/turn_recovery.py`, `src/agentos/gateway/idempotency.py`, `src/agentos/sandbox/policy.py`, `tests/test_engine/test_tool_pairing_unknown_outcome.py` and `tests/test_gateway/test_idempotency.py` — all under `https://raw.githubusercontent.com/use-agent-os/agent-os/main/`. The repository file tree was read from `https://api.github.com/repos/use-agent-os/agent-os/git/trees/main?recursive=1` (3,989 paths, not truncated) and repository metadata from `https://api.github.com/repos/use-agent-os/agent-os`. Claim types are separated above: code-inspected facts are those asserted from file contents; release-note and README statements are vendor claims; the Limitations assessment and the whole Implications section are analysis by the KB maintainers. Nothing here was installed, cloned, executed, benchmarked or reproduced by the KB maintainers, no project code was run, and no independent replication of any AgentOS claim is known.

## Historical coverage

- [[briefings/2026/11/2026-11-03]] — finding 5, the dated briefing this record was backfilled from.
