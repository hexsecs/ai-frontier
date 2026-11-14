---
uid: b6a90403-a8d1-4d13-9a40-000000000013
title: "BuilderIO agent-native"
summary: "BuilderIO agent-native PR #8670: classify failed writes from observed writes with fail-closed channels; AI-reviewed, merged 2026-11-04."
type: project
created: 2026-11-09
updated: 2026-11-10
depth: deep
sources:
  - https://github.com/BuilderIO/agent-native/pull/8670
  - https://github.com/BuilderIO/agent-native/pull/8670/files
  - https://github.com/BuilderIO/agent-native/pull/8670/commits
  - https://raw.githubusercontent.com/BuilderIO/agent-native/dec69e4c2c184df705e428e249bccd4b99ba1c52/scripts/guard-no-unobserved-writes.ts
  - https://raw.githubusercontent.com/BuilderIO/agent-native/dec69e4c2c184df705e428e249bccd4b99ba1c52/packages/core/src/action.ts
  - https://raw.githubusercontent.com/BuilderIO/agent-native/dec69e4c2c184df705e428e249bccd4b99ba1c52/packages/core/src/outbound-write-observation.ts
  - https://raw.githubusercontent.com/BuilderIO/agent-native/dec69e4c2c184df705e428e249bccd4b99ba1c52/packages/core/src/db/sql-write-classifier.ts
  - https://raw.githubusercontent.com/BuilderIO/agent-native/dec69e4c2c184df705e428e249bccd4b99ba1c52/packages/core/src/db/note-sql-statement.ts
---

# BuilderIO agent-native

## What it is

BuilderIO agent-native is a TypeScript framework for building agentic apps (repository description: "A framework for building agentic apps"; homepage agent-native.com; MIT licence). The page's artifact is PR [#8670](https://github.com/BuilderIO/agent-native/pull/8670), "Stop agent runs ending on write_tool_outcome_unknown when a rejected write saved nothing", opened by contributor enzoames on 3 November 2026, fixing internal issue ENG-14466, and merged into `main` by its author on 4 November 2026 at 19:10 UTC (merge commit `4e36f27`, head commit `dec69e4c2c184df705e428e249bccd4b99ba1c52`, 10 commits on branch `enzoames/changes-100157`, +10,019/−169 changed lines across 128 files; 285 of 323 checks passed at merge; the branch was deleted after merge).

Two things make the PR worth a canonical page. The mechanism: it replaces handler-entry-based write classification ("might have written" the moment a handler starts) with **observed-write classification** — a failed call is classified from the writes the framework actually saw — implemented as a fail-closed observation funnel across every write channel. And the review record: the PR went through four rounds of review by `builder-factory` (human-side approvals) and `builder-io-integration[bot]` — Builder's own AI code reviewer, which produced substantive findings the author then fixed or declined *with spec-level evidence*, in public threads.

## Mechanism

**The failure mode being fixed.** The PR body: "the framework marked every write action as 'might have written' the moment its handler started, so any failure that carried no `NoWriteError` / `retrySafe` label was classified `unknown`. The loop then blocked that tool and ended the run as `write_tool_outcome_unknown`, even for rejections thrown before anything was saved (for example Design `create-file` rejecting HTML for a missing HubSpot marker). In the retained production Design runs, 7 of 9 failures were that shape." A pre-save rejection was therefore ending whole agent runs.

**Observed-write classification** (read from the raw files at head commit `dec69e4c` on 2026-11-10):

- **Database.** Every non-read SQL statement is observed at the single funnel all drivers share (`withDbTimeout`), plus the Drizzle session and PGlite layers that bypass it. The classifier in `sql-write-classifier.ts` **fails closed**: only `SELECT`, `SHOW`, `SET`/`RESET`, transaction control, `LOCK`, and `EXPLAIN` without `ANALYZE` are reads; a `WITH` is a read only if no CTE writes; multi-statement strings are writes unless every statement is a read; a query with no SQL text counts as a write. A `SELECT`, `WITH` or `VALUES` calling a listed side-effecting built-in (`pg_notify`, `pg_logical_emit_message`, `setval`, `dblink*`, the large-object writers, `pg_terminate_backend`, `pg_cancel_backend`, `pg_reload_conf`, `pg_rotate_logfile`, `pg_create_*`, `pg_drop_*`, `pg_replication_*`) counts as a write, matched on word boundaries after comments, string literals and quoted identifiers are masked; `nextval`, `set_config` and advisory locks stay reads; agent-authored SQL additionally refuses `pg_*`, `lo_*`, `dblink*` and `setval` outright.
- **Outbound HTTP.** A lazily installed, idempotent wrapper around `globalThis.fetch` notes every non-GET/HEAD/OPTIONS request before sending. Framework telemetry inside an action (analytics, error capture, LLM completions, embeddings, decision providers, the Neon HTTP SQL transport) is exempt via `withoutWriteObservation`. **If `fetch` cannot be wrapped, the framework logs one warning and every call counts as having sent a write, so a failure stays `unknown`** — the wrap failure is itself fail-closed.
- **Other channels.** `noteExternalWrite(channel)` before local-disk writes and deletes, Local File Mode writers, child processes (run-code sandbox, scaffold CLI), and MCP tool calls; `provider-api-request` is observed through the fetch wrapper. Framework bookkeeping (audit rows, change markers, presence heartbeats, schema setup and migration ledger rows, `LOCK TABLE`) does not count as the action's own write; `kind: "data"` migrations still do.
- **Effect computation.** `invocationEffect` uses the observed evidence for failures a call threw itself; a call whose result never arrived (timeout or abort) keeps prior behaviour, "because it may still be running"; `changed` (UI refresh) stays as conservative as before; `NoWriteError`, `retrySafe`, typed errors and write receipts still take precedence.

**Template fixes in the same PR.** Design `create-file` validates before the version snapshot, with the auxiliary `snapshotDesignBeforeAgentEdit` inside `withoutWriteObservation` and same-turn retry idempotence (deterministic ids with `onConflictDoNothing`, state-hash short-circuit); Slides `import-file`/`import-pptx`/`import-google-slides-reference` label the "no slides/deck written" rejection as `NoWriteError` (pre-rejection uploads are orphan blobs, not deck data); real-database (PGlite) specs cover the Design and Slides failed-write paths.

**The enforcement guard.** A new diff-scoped guard `no-unobserved-writes` (`scripts/guard-no-unobserved-writes.ts`, 985 lines): new disk writes, child processes, `node:http(s)` clients and vendor SDK imports in action and server code need a `noteExternalWrite(...)` before them in the same function (or in a same-file helper they call first, ordered so no earlier `return` can skip the note), or an explicit `// observed-write-ok: <reason>`. It matches import aliases, namespace imports, bare `fs` names, `.writeFile(`/`.appendFile(`, fs `open` with non-read flags, FileHandle methods, `child_process` aliases, and resolves `noteExternalWrite` to the framework export only (a local lookalike no longer satisfies it). An HTTP-client or SDK import, which has no call site, passes on any note in the file — a stated limit of the guard.

## Evidence

**Inspected.** The PR page (metadata, full description, commit list, review threads, merge state), the file list (128 changed files: `packages/core/src/action.ts` +68/−14, `action-frame.ts` +62/−1, the new `action-frame.spec.ts`, `action.outbound-writes.spec.ts` at 342 lines, `agent/production-agent-rejected-writes.spec.ts` at 87, db observation specs, `outbound-write-observation.ts` at 122, `mcp-client/manager.ts`, `server/*`, `coding-tools/sandbox/local-child-process-adapter.ts`, `collab/agent-presence.ts`, `decisions/providers`, the Design and Slides templates, `scripts/guard-no-unobserved-writes.ts` at 985 and `scripts/run-guards.ts`, changesets and changelog entries), and the raw core files at head commit `dec69e4c`.

**The AI review record (inspected in the PR threads).** `builder-io-integration[bot]` reviewed four times; `builder-factory` approved four times (twice 3 November, twice 4 November). The bot's findings and their adjudication:

| Builder bot finding (date) | Outcome |
|---|---|
| Observed writes discarded for declared read-only calls (`action.ts`, Nov 3) | **Declined** — same as `main`; read-only POSTs (GA4, Search Console, HubSpot search) would regress to `write_tool_outcome_unknown`; pinned by a spec ("is none when a read-only POST fails after sending") |
| MCP `isError` bypasses observed-write evidence (`action.ts`, Nov 3) | **Declined** — existing #8130 behaviour; "every MCP call notes before it is sent, so applying that evidence to a reported error would make every `isError` result `unknown`" |
| Side-effecting `SELECT` functions read as reads (`sql-write-classifier.ts`, Nov 3) | **Fixed** in `f9d7519` — the built-in list and word-boundary masking described above |
| File-wide note suppresses unrelated writes (guard, Nov 3) | **Fixed** in `f9d7519` — per-function, per-path notes |
| `fetch` that cannot be wrapped is ignored (review body, Nov 3) | **Fixed** in `d4b0872` — every call counts as having sent a write |
| Same-line note after the write; conditional note on a skipping path; shadowed no-op helper; aliased `fs`/`FileHandle` writes (guard, Nov 3–4) | **Fixed** in `d4b0872` — column-ordered, block-scoped, helper-name resolution, alias coverage |
| Helper note may not run before the write; more fs write APIs; hoisted nested-write ordering (Nov 4) | **Fixed** in `1b74bfc` — call-order proof, `write`/`writev`/`ftruncate`/`link`/`chmod`/`chown`/`utimes`/`mkdtemp` + Sync forms |
| Mail Gmail lookup falsely marked a write (`manage-draft.ts`) | **Fixed by removal** — the author's own `noteExternalWrite("gmail")` was redundant (fetch already observes those writes) and made reads look like writes |
| Multiline dynamic child-process imports; `import { promises as disk }` aliases (guard, Nov 4) | Findings on the final head; addressed in the guard's final state |

**Author-reported verification** (on head `f9d7519`, not independently reproduced): Core build and typecheck pass; vitest over the listed Core directories plus browser and outbound-write specs: 603 files, 14,536 tests passed, 2 skipped; mutation (`pnpm mutation:changed`, all 93 ranges) global score 91.63% against the 50% break (`note-sql-statement.ts` 100%, `sql-write-classifier.ts` 96.94%); `pnpm guards` all 103 checks pass; guard tests 45/45; spec-driven checks confirmed by mutation ("reverting Core to entered-only classification fails the new three-way case"). Earlier pushes report full Core (908 files, 20,201 tests), Design actions+server (277 files, 3,688 tests) and the Slides/Analytics/Mail/Calendar/Clips/Assets/Plan/Dispatch suites. CI on intermediate heads: three jobs failed — two caused by the PR (a spec had mocked `saveGmailDraft` away so no `fetch` happened; the mock was fixed to send the POST) and one not (a Content DB test failing on pure `main` at `0b1ae94f74`); the first push had also hit `ERR_PNPM_NO_MATURE_MATCHING_VERSION` for `@tailwindcss/oxide-wasm32-wasi 4.3.4` under the `minimumReleaseAge` limit.

**Not verified by anyone in the record:** deployed behaviour, and the production reason for one unexplained `edit-design` block (the author's hypothesis: the loop holding back later calls of a tool once an earlier call was `unknown`).

## Limitations

**Known gaps, stated by the author and left conservative on purpose:** a `SELECT` calling an app-defined SQL function that writes is not seen (the classifier knows only built-ins; the repo defines none that a `SELECT` calls); a remote MCP tool that changes state and then returns `isError` stays retryable (pre-existing #8130 behaviour); custom `FileUploadProvider`/`PrivateBlobProvider` on non-fetch SDKs are not observed; a client that captured `fetch` before the first action frame, or swapped it mid-action, is not observed; better-auth's own Drizzle instances on hosted Postgres are not observed; read-via-POST calls inside an action count as writes so they stay `unknown`.

**Assessed by the KB maintainers:**

- **Every verification number is author-reported.** The 14,536 tests, 91.63% mutation score and 103 guard checks are the contributor's own runs; no independent reproduction exists in the record, and the merged PR shows 285 of 323 checks passing — with the failures explained in-thread but the explanations unverified.
- **The three declined findings are unresolved, documented risks.** Read-only-declared actions that nonetheless write; MCP tools that mutate and then report `isError`; and the guard's SDK-import exemption are all real paths to retrying a write that may have succeeded. Each was declined with a spec as evidence, not fixed.
- **Observation completeness is the whole security property.** A write channel the framework cannot see reads as retry-safe — the exact inverse of the failure mode the PR fixes. The guard narrows but does not close this (its own header states the file-wide-note limit for imports).
- **The 7-of-9 production figure is unaudited.** "In the retained production Design runs" is the author's count from internal telemetry (ENG-14466); the runs themselves are not published.

## Competing approaches

Only alternatives the inspected sources name.

- **The prior fix, PR #8130** ("Stop ending agent runs on writes that were rejected before they wrote"): treated an MCP tool's `isError` result as a known failure. This PR builds on it and preserves its early return — the two designs layer rather than replace each other.
- **Handler-entry classification** ("might have written" on entry) — the `main` behaviour this PR replaces, retained in the branches where evidence is genuinely unavailable (result never arrived, `fetch` unwrappable).
- **Labels over observation** — `NoWriteError` and `retrySafe` as explicit per-action declarations, which still take precedence over observed evidence; the observed-write funnel is the fallback for unlabeled failures, not a replacement for labelling.
- **Per-driver instrumentation** versus the single shared funnel — the PR's own design notes the Drizzle session and PGlite layers that bypass `withDbTimeout` and had to be instrumented separately.

Canonical context: [[projects/agentos]] and [[projects/rivet-agents]] are other agent frameworks in this corpus with distinct completion-verification postures; the cross-cutting questions are tracked in [[evaluations/briefing-synthesis-2026-11-03-to-09]] (analyst-selected, not source-verified).

## Implications

The following is analysis by the KB maintainers, not a claim of the authors.

The transferable principle is **classify from observed effects, not from execution position**. "The handler started, therefore it might have written" is the same error class as "the agent said done, therefore it is done" — an inference from control flow where an observation of the world was available. The fix makes the framework's write channels observable at a small number of funnels and then reasons from the observations, with fail-closed defaults at every boundary (unknown SQL is a write; an unwrappable `fetch` means every call wrote; a never-arrived result stays `unknown`). This is [[concepts/verified-completion-vs-apparent-success]] implemented as infrastructure: the run-ending verdict `write_tool_outcome_unknown` becomes evidence-derived instead of position-derived, and the conservative direction is explicit in every default.

Second, **the guard turns a review convention into a checked invariant**. "Every new write site must be observed" cannot be enforced by prompt discipline in a large codebase; a 985-line AST-based guard with per-path note ordering, alias coverage and export resolution is what makes the invariant survive future commits — [[concepts/structural-constraint-over-instruction]] at the level of CI enforcement. The guard's own documented limits (imports have no call site; type-aware SDK analysis is "a different guard") are the honest boundary of static enforcement.

Third — and unusually for this corpus — **the review record itself is evidence about AI code review**. The bot's findings were specific, mechanistic and partly correct (the `SELECT` side-effect finding was fixed and hardened the classifier; the `fetch`-unwrap finding produced the fail-closed default). Two were declined *with pinned specs and regression reasoning*, one declined finding exposed a genuine redundancy in the author's own code (the Gmail note), and the author's adjudication style — quote the spec, name the regression, decline with evidence — is a working model for human adjudication of machine review. What the record does not show is the bot's false-positive rate on unaffected code, or what a second independent reviewer would have flagged that neither bot nor author did.

## Reproducible experiment

Proposed, not executed; arms use the published PR and repository at the merged commit.

1. **Pre-save rejection (the headline claim).** In a scratch app, induce Design `create-file` rejecting HTML for a missing HubSpot marker. Pass criteria: the run no longer ends in `write_tool_outcome_unknown`; the effect is classified `none`; no retry is attempted. A return to `unknown` or a tool block falsifies the PR's central claim.
2. **Fail-closed classifier.** Feed `sql-write-classifier` statements covering each branch: plain `SELECT`, `SELECT ... INTO`, `WITH` containing a writing CTE, multi-statement strings, empty SQL text, a `SELECT` calling `pg_notify`, `setval` inside a string literal, a column named `setval`. Pass criteria: only the documented reads pass as reads; every ambiguous form is a write. This is checkable against the published spec file.
3. **Wrap-failure conservatism.** Make `globalThis.fetch` non-writable in a test runtime and run an action that fails mid-POST. Pass criterion: the failure classifies `unknown` (every call counted as a write), with exactly one warning logged — the fail-closed branch.
4. **Declined-finding arms.** (a) An action declared `readOnly` that sends a mutation: assert the failure reads `none` per the pinned spec, and record that this is the documented, declined risk. (b) An MCP tool that writes then returns `isError`: assert it stays retryable (the #8130-accepted gap). These arms do not pass or fail the PR; they verify that the declined findings behave as adjudicated.
5. **Guard conformance.** Introduce, in a copy of the repo: an unnoted `fs.writeFile`, a note after the write on the same line, a note inside a conditional branch the write skips, a helper with a note behind an early `return`, an aliased `import { promises as disk }` write, a local `noteExternalWrite` lookalike. Pass criteria: all are flagged; only a real note on every path before the write passes. This tests the guard's published rules rather than the author's word.

## Evidence status

Grounded in HTTPS reads on 2026-11-10 of the PR page (metadata, description, commit list, the four Builder review rounds and their threads, merge state), the PR file and commit listings, and the raw files at head commit `dec69e4c2c184df705e428e249bccd4b99ba1c52` (`action.ts`, `action-frame.ts`, `outbound-write-observation.ts`, `db/sql-write-classifier.ts`, `db/note-sql-statement.ts`, `scripts/guard-no-unobserved-writes.ts`). **Inspected:** PR identity, timeline, review-thread contents and outcomes, the changed-file inventory, and the mechanism as present in the raw code. **Author-reported:** every verification figure (test counts, mutation score, guard checks, CI explanations) and the 7-of-9 production-failure count; none of it was reproduced by the KB maintainers. **Bot-generated:** the Builder findings, quoted as the reviewer's statements and adjudicated by the author's in-thread replies. Nothing on this page was installed, cloned, compiled, executed or benchmarked by the KB maintainers; no independent evaluation of the PR's behaviour is known to them, and deployed behaviour is unverified by anyone in the record.

## Historical coverage

- [[briefings/2026/11/2026-11-04]] — the dated full-fidelity research briefing and cross-project synthesis that selected this PR.
- [[evaluations/briefing-synthesis-2026-11-03-to-09]] — the cross-project synthesis layer covering this and sibling agent-framework findings.
