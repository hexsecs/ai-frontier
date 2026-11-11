---
uid: b6a90603-a8d1-4d13-9a40-000000000033
title: "Code Simplifier"
summary: "Daily gh-aw cleanup agent: deterministic candidate precompute, Haiku gate and scout, strict evals, six required endings; three vendor-reported no-op runs."
type: workflow
created: 2026-11-09
updated: 2026-11-10
depth: deep
sources:
  - https://github.github.com/gh-aw/blog/2026-11-05-agent-of-the-day/
  - https://raw.githubusercontent.com/github/gh-aw/main/.github/workflows/code-simplifier.md
---

# Code Simplifier

**Origin:** [[briefings/2026/11/2026-11-06]] — finding 3. This is a canonical backfill of the briefing's sourced assessment, expanded on 2026-11-10 with a full read of the workflow source and the vendor blog post. It is not a new independent review, and nothing described here was executed by the KB maintainers.

## What it is

Code Simplifier is a private scheduled GitHub Agentic Workflow in GitHub's own `github/gh-aw` repository, in `.github/workflows/code-simplifier.md`, spotlighted in the gh-aw "Agent of the Day" blog post of 5 November 2026 (byline "Copilot"; site credits GitHub Next and Microsoft Research). Its frontmatter `description` is a single sentence of intent: "Analyzes recently modified code and creates pull requests with simplifications that improve clarity, consistency, and maintainability while preserving functionality." The blog's framing: "Most agents are loud: comments, labels, issues, dispatches. Today's spotlight goes to one that is comfortable being quiet."

The artifact's claim to attention is not that it simplifies code — it is that across the published window it did nothing three times, correctly, and had a structurally mandated way to say so. The blog's own reading: "The honest reading: on days with nothing worth simplifying, the right outcome is no output. A workflow that can say 'nothing to do' cheaply and reliably is doing its job."

**Maturity.** The file declares `private: true` (GitHub's own internal workflow, not a published template), `strict: true` (gh-aw's stricter mode), and runs on `schedule: daily`. No preview or GA status is stated for the workflow itself in the inspected material.

## Mechanism

Everything below was read from the workflow source file on 2026-11-10.

**Frontmatter and budget.** `max-turns: 50`, `max-ai-credits: 1000` per run, `max-daily-ai-credits: 5000`, `timeout-minutes: 30`. Permissions are read-only: `contents`, `issues` and `pull-requests` all `read`; the only write path is the safe-output mechanism. `tracker-id: code-simplifier`. Network is restricted to `allowed: [go]` (Go module fetches for builds), tools are `cli-proxy: true`, `github: mode: local, toolsets: [default]`, and bash is unrestricted (`bash: ["*"]`). Imports pull in shared MCP pagination, the shared skip-if-issue-open gate (title prefix `[code-simplifier]`, kind `pr`), the shared daily-PR base (PR title prefix `[code-simplifier] `, expiry `1d`, labels `[refactoring, code-quality, automation]`, reviewer `copilot`, protected files excluding `.github/extensions/`), telemetry and graders. Two built-in evals are declared: `code_analyzed` ("Did the agent analyze recently modified code for simplification opportunities? Return UNKNOWN when the output records a skip-if-decision no-op before agent execution.") and `pr_created_or_noop` ("Was a pull request created with simplifications, or was noop used when no improvements were needed?").

**The skip-if-decision gate.** Before the agent is invoked at all, gh-aw's decision gate evaluates a single question against the precomputed datasets: "Do @/tmp/gh-aw/agent/code-simplifier/recent-context.json and @/tmp/gh-aw/agent/code-simplifier/source-files.json conclusively establish that no recently modified production code is eligible for simplification under this run's scope? Abstain if either dataset is invalid, incomplete, inconsistent, or contains an eligible candidate." Uncertain evidence preserves execution — the gate abstains (skips the agent) only on conclusive no-candidate evidence. This is the workflow's cheapest no-op: zero model turns.

**Deterministic step 1 — the recent-change dataset.** Plain shell, before any model runs: a `yesterday` date (with a BSD `date -v-1d` fallback), `git log --since='24 hours ago' --no-merges` piped through `jq` into `recent-commits.jsonl` (sha + subject) and a sorted-unique `recent-files.txt`; `gh pr list --state merged --search "merged:>=$YESTERDAY" --limit 100` into `recent-prs.json` (falling back to `[]`); then a `jq` filter that keeps only source files by extension (go, js, cjs, mjs, ts, tsx, py, cs, java, rb, php, kt, swift) while excluding tests (`_test.`, `.test.`, `.spec.`), lockfiles (package-lock.json, pnpm-lock.yaml, yarn.lock, go.sum, Cargo.lock) and generated paths (`.generated.`, `/generated/`, `/dist/`, `/build/`), capped at 20 files; finally `recent-context.json` assembles `{generated_at, window_start, candidate_file_cap: 20, merged_prs, candidate_files}`.

**Deterministic step 2 — the run-history summary.** `gh api repos/$REPO/actions/workflows/code-simplifier.lock.yml/runs?per_page=30` is aggregated by `jq` into `history-summary.json`: sample size, success/failure/cancelled counts, the five most recent failures, and — the interesting part — an explicit `deterministic_candidates` list naming three operations the workflow itself committed to keeping out of the model: "recent PR and commit discovery", "changed-file filtering" and "workflow run history aggregation", each with `move_to: "steps"` and a reason ("This data is fetched every run and can be pre-computed once in deterministic shell steps", "Extension and test/generated-file filtering is deterministic and should not consume AI tokens", "Historical run metadata can be summarized via jq before entering agent context").

**The agent's five phases.** Phase 1 determines scope from the precomputed files, with a fixed `noop` message when no candidates exist ("✅ No code changes detected in the last 24 hours. Code simplifier has nothing to process today.") and a rule not to discover files beyond the deterministic cap. Phase 2 is the "Historical Optimization Gate": read `history-summary.json`, keep the listed operations in deterministic paths, and "If a planned action duplicates one of those candidates, use the precomputed file instead of a tool call." Phase 3 analyzes: for each candidate file, the `scope-filter` sub-agent (`claude-haiku-4.5`) decides inclusion and language ("Set `include` to false for tests, generated files, lockfiles, vendored code, or unsupported languages"), only the matching language skill guidance is loaded, and the `simplification-scout` sub-agent (`claude-haiku-4.5`) proposes "at most 5 opportunities, ordered by expected readability gain, then by lowest risk" as strict JSON (`kind`: clarity|duplication|complexity|naming, `risk`: low|medium). Four inline language skills carry the standards: JavaScript/TypeScript, Go, Python and C#, four rules each (e.g. Go: "prefer explicit error handling and clear guard clauses", "preserve package boundaries and exported API behavior"). Phase 4 validates with `make test-unit`, `make lint`, `make build`. Phase 5 decides: a PR only if all three hold — "meaningful simplifications were made", "behavior is preserved", and all three validation commands succeed — otherwise `noop` with the fixed no-improvements message.

**Command guardrails and required endings.** The agent is forbidden to use `python3` for JSON parsing (`jq`, `cat`, `head` instead), forbidden to retry variations of a blocked command, and must "stop immediately and call `report_incomplete`" after three consecutive permission-denied errors of the same type. The output contract is structural: "You MUST finish by calling exactly one safe-output tool" from a closed list of six — `noop` (no recent changes), `noop` (no beneficial simplifications), `noop` (run stopped at the configured per-run budget ceiling), `create_pull_request`, `report_missing_tool`, `report_missing_data` — and "Do not finish with plain text only." The budget-ceiling message is fixed verbatim ("⚠️ Code simplifier run stopped at configured per-run budget. Processed available deterministic inputs only; no safe write action produced."), and the PR body must list files simplified, the simplifications, source references from the precomputed PR/commit data, validation results and "a brief note on deterministic pre-processing and token-efficiency choices".

## Evidence

**Inspected facts** (checkable by any reader against the same public file):

| Property | Value | Source |
|---|---|---|
| Schedule | daily | frontmatter |
| Budgets | 50 turns, 1000 credits/run, 5000 credits/day, 30-minute timeout | frontmatter |
| Permissions | `contents`/`issues`/`pull-requests` read only | frontmatter |
| Candidate window | 24 hours of commits, merged PRs since yesterday (`--limit 100`) | step 1 |
| Candidate cap | 20 files, by extension allowlist, tests/lockfiles/generated excluded | step 1 |
| Sub-agent models | `scope-filter` and `simplification-scout`, both `claude-haiku-4.5` | agent definitions |
| Scout output shape | ≤5 opportunities, readability gain then lowest risk | agent definition |
| Validation | `make test-unit`, `make lint`, `make build` | phase 4 |
| Required endings | 6: three `noop` variants, `create_pull_request`, `report_missing_tool`, `report_missing_data` | output contract |
| Built-in evals | 2 (`code_analyzed`, `pr_created_or_noop`) | frontmatter |
| Strict mode | `strict: true` | frontmatter |

**Vendor claims and vendor telemetry.** The blog tabulates the last three days of runs, all in `github/gh-aw`:

| Run | Started (UTC) | Conclusion | Duration | Tokens |
|---|---|---|---|---|
| 41571296696 | Nov 3, 03:17 | success | 6.2 min | 8,527 |
| 41766108016 | Nov 4, 03:16 | success | 8.2 min | 9,486 |
| 41960692776 | Nov 5, 03:17 | success | 8.8 min | 8,323 |

"Three for three: no errors, no warnings, one turn each, and about 23 minutes of total duration. The aggregate shows 0 safe-output items across the window, so none of these runs opened a pull request or issue. We did not find a Code Simplifier PR in this window to link, and we are not going to invent one." An audit of the latest run "classifies the behavior as `directed` with a `read_only` actuation style, in the 'Code Fix' task domain. It reports a working set of 7,637 peak input tokens, with a rebuild factor of about 1.0, meaning the context was not being repeatedly reloaded. The audit does flag a higher overall token figure (about 114k) as a finding worth a look, so there may be room to trim."

**What is not published.** No results for the two declared evals; no measurement of whether a produced simplification PR would be correct (in this window, zero were produced); no human evaluation of the scout's opportunity scoring; no denominator for the roughly-114k token figure versus the 7,637-token working set; no failure-mode data (all published runs succeeded).

## Limitations

**Stated by the vendor.** The audit's own finding of "a higher overall token figure (about 114k)" worth a look — the blog concedes cost headroom. The blog also states its abstention standard rather than a quality standard: the runs prove the workflow can stay quiet, not that its simplifications are good.

**Assessed by the KB maintainers:**

- **The published window contains zero writes, so the write path is untested in evidence.** The most consequential branch — a simplification that must preserve behaviour and pass `make test-unit`/`lint`/`build` — has no published run. Everything verified is the no-op path.
- **Token accounting does not reconcile.** The run table shows 8–9k log-summary tokens per run while the audit flags "about 114k" overall for the latest run and a 7,637-token peak working set; the relationship between the three measures is not stated.
- **The token-efficiency gate is self-graded.** Phase 2's "Historical Optimization Gate" asks the agent not to duplicate the three named deterministic candidates, but compliance is prompt-level; the audit's ability to detect waste is what surfaces it, after the fact.
- **Candidate discovery is capped by design.** Twenty files, 24-hour lookback, merged PRs limited to 100 — a busy repository silently drops work, and no queue or catch-up exists in the inspected source.
- **Simplification quality depends on four inline skill files.** The language standards are four bullet points each; nothing measures whether following them yields maintainable code or subtle behaviour changes, and Phase 4's safety net (`make test-unit` etc.) is only as strong as the repository's test suite.
- **The `strict: true` and evals are process checks.** `pr_created_or_noop` treats a PR and a `noop` as equally acceptable outcomes; neither eval measures simplification correctness.

## Competing approaches

Only alternatives the inspected sources name.

- **A monolithic single prompt.** The blog's takeaway names the split as the design: "Splitting a task into a gate, a scout, and language standards keeps each prompt small." The alternative is one prompt doing scoping, discovery and standards.
- **Model-side data discovery versus deterministic precompute.** The workflow's own `deterministic_candidates` list (with `move_to: "steps"`) commits three discovery operations to shell; the alternative is the agent fetching them, which the Phase 2 gate explicitly forbids duplicating.
- **Writing something versus abstaining.** The output contract makes abstention one of six required endings rather than a failure; the blog's "Quiet success is still success" is the vendor's statement of the same contrast.
- **Within gh-aw, the sibling designs.** [[projects/github-contribution-check]] reviews incoming PRs on a four-hour schedule with a deterministic 3-PR cap; [[projects/pr-sous-chef]] nudges idle PRs every five minutes behind a deterministic prefilter. Code Simplifier is the scheduled-writer counterpart: it holds write capability but published only abstentions.

(Analyst note, not from the sources: non-agentic formatters, linters and `gofmt`-class tools are the obvious deterministic alternative for "simplification"; none is named in the inspected material and none is characterised here.)

## Implications

The following is analysis by the KB maintainers, not a claim of GitHub's.

The durable idea is **abstention as a first-class, cheap, structurally required outcome** — the [[concepts/abstention-as-first-class-verdict]] pattern made mechanical in three layers: a decision gate that can skip the agent entirely on conclusive evidence, three verbatim `noop` messages that name *why* nothing was done (no changes, no worthwhile simplifications, budget ceiling), and an output contract that forbids finishing without one of six typed endings. A workflow that must end in a typed outcome cannot end in vague success text, which makes its runs auditable by construction: "check `run.safe_items_count` before assuming a run did nothing wrong" is the blog's own metric advice.

The second lesson is **the workflow polices its own token budget with a written commitment**: the `deterministic_candidates` list inside `history-summary.json` is a machine-readable record of what the workflow promised never to pay model tokens for again. That is an unusual artefact — a self-imposed regression list for cost discipline — and it is checkable: an auditor can diff the agent's tool calls against the three named operations.

The counterweight is the mirror image of PR Sous Chef's: there, half the runs failed and the mechanism was sound; here, all the runs succeeded and the write path is untested. Three correct abstentions are real evidence for the cheap end of the design (gate, budget, endings) and no evidence at all for the expensive end (a behaviour-preserving simplification PR). Anyone adopting this pattern inherits the untested half: the `create_pull_request` branch with its `make test-unit`/`lint`/`build` gate is where the risk lives, and the vendor's own "we are not going to invent one" honesty about the missing PR link is the correct standard for what a reader should conclude — nothing.

## Reproducible experiment

The deterministic half is testable without a model; the write path needs a scratch repository. **This protocol has not been run.**

1. **Gate abstention (no model required).** Prepare `recent-context.json` and `source-files.json` with an empty `candidate_files` array and confirm the skip-if-decision gate skips the agent. Then corrupt one file (invalid JSON) and re-run. Pass criteria: the clean-empty case skips agent execution; the invalid-dataset case *runs* the agent ("Abstain if either dataset is invalid, incomplete, inconsistent, or contains an eligible candidate" — uncertain evidence must preserve execution). A gate that abstains on corrupt data fails the design's conservative direction.
2. **Candidate filter conformance.** Commit 25 eligible source files plus one test, one lockfile, one vendored file and one generated file in the last 24 hours. Pass criteria: exactly 20 candidates emerge, in a deterministic order, with the four ineligible files excluded; the 21st eligible file is silently dropped (the cap binds) and is not discovered later by the agent.
3. **Typed endings.** Run three scenarios — no candidates, candidates with no worthwhile simplification, and a budget exhaustion mid-run (lower `max-turns` to force it). Pass criteria: each run ends in the corresponding fixed `noop` message verbatim; no run ends in plain text.
4. **Write-path arm.** On a scratch repository with a deliberately over-complex recent change and a real test suite, let the workflow produce a PR. Pass criteria: the PR lists simplifications and source references, `make test-unit`/`lint`/`build` results are in the body, behaviour is preserved (tests pass on the PR branch), and a run whose simplification breaks tests does not emit `create_pull_request` (Phase 4 must revert or abstain). This tests the branch with zero published evidence.
5. **Historical-gate compliance.** Instrument the agent's tool calls for one run and diff them against the three `deterministic_candidates`. Pass criterion: no tool call duplicates PR/commit discovery, changed-file filtering or run-history aggregation; a duplicate indicates the gate is prompt-only in practice.
6. **Scout agreement.** On ten real files, compare `simplification-scout`'s ranked opportunities against two human reviewers' independent rankings. Report rank correlation and the false-opportunity rate (changes that would alter behaviour). This measures the quality claim the evals do not.

## Evidence status

This page is grounded in a full read of two public documents on 2026-11-10, fetched by HTTPS without executing anything: the workflow source (https://raw.githubusercontent.com/github/gh-aw/main/.github/workflows/code-simplifier.md) and the vendor blog post "Agent of the Day – November 5, 2026" (https://github.github.com/gh-aw/blog/2026-11-05-agent-of-the-day/). **Inspected:** every mechanism statement — the frontmatter budgets and permissions, the skip-if-decision text, both deterministic steps with their exact filters and caps, the five phases, the `scope-filter` and `simplification-scout` agent definitions and their output shapes, the four language skills, the command guardrails, and the six required endings — comes from the workflow file and can be checked by any reader. **Vendor-claimed:** the three run rows (timestamps, durations, token counts), the "0 safe-output items" aggregate, the audit's `directed`/`read_only` classification, the 7,637-token working set, the ~1.0 rebuild factor, and the ~114k token flag. These are GitHub's reports on GitHub's own repository, with no independent replication; no eval results are published for the two declared evals. The "assessed" items in Limitations and the whole Implications section are analysis by the KB maintainers, and the reproducible experiment is proposed and not executed. Nothing on this page was installed, cloned, compiled or run by the KB maintainers.

## Historical coverage

- [[briefings/2026/11/2026-11-06]] — finding 3, the dated briefing this page backfills.
- Sibling gh-aw workflows under the same platform: [[projects/github-contribution-check]], [[projects/pr-sous-chef]], [[projects/matt-pocock-skills-reviewer]] and the platform page [[projects/github-agentic-workflows]]; the workflow corpus is [[workflows/index]] and the cross-project synthesis is [[evaluations/briefing-synthesis-2026-11-03-to-09]]. These are analyst-selected thematic comparisons, not source-verified dependencies.
