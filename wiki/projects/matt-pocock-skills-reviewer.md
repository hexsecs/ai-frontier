---
uid: b6a90602-a8d1-4d13-9a40-000000000032
title: "Matt Pocock Skills Reviewer"
summary: "gh-aw PR reviewer applying five commit-pinned Matt Pocock skills: Haiku triage, fixed write shapes, three vendor-reported runs, no accuracy evidence."
type: workflow
created: 2026-11-09
updated: 2026-11-10
depth: deep
sources:
  - https://github.github.com/gh-aw/blog/2026-11-06-agent-of-the-day/
  - https://raw.githubusercontent.com/github/gh-aw/main/.github/workflows/mattpocock-skills-reviewer.md
---

# Matt Pocock Skills Reviewer

**Origin:** [[briefings/2026/11/2026-11-06]] — finding 2. This is a canonical backfill of the briefing's sourced assessment, expanded on 2026-11-10 with a full read of the workflow source and the vendor blog post. It is not a new independent review, and nothing described here was executed by the KB maintainers.

## What it is

The Matt Pocock Skills Reviewer is a private pull-request reviewer built as a GitHub Agentic Workflow (gh-aw) inside GitHub's own `github/gh-aw` repository, in `.github/workflows/mattpocock-skills-reviewer.md`. GitHub featured it as the "Agent of the Day" blog post of 6 November 2026 (byline "Copilot"; the site footer credits GitHub Next and Microsoft Research). Its frontmatter `description` states the job: "Reviews pull requests using Matt Pocock's engineering skills to provide targeted, high-quality improvement suggestions based on the type of changes."

The blog's framing of the design instinct: "A good reviewer doesn't recite the whole style guide. They look at the change in front of them and ask the one or two questions that matter." The distinctive move is **lens selection by change type** — a bug fix is reviewed through `/diagnosing-bugs` and `/tdd`, a refactor through `/codebase-design` and `/improve-codebase-architecture` — rather than one generic review rubric for every PR.

**Maturity.** The file declares `private: true`, so this is GitHub's own internal workflow, not a published template; no preview or GA status is stated for it anywhere in the inspected material, and the blog entry is a spotlight, not a product announcement. The engine is GitHub's Copilot CLI engine (`engine.id: copilot`, `copilot-sdk: true`) with cost-oriented model routing (`goal: cost`, `mode: economy`).

**Why the page exists.** Three things make this workflow more than a prompt: it imports a third party's skills into GitHub's own review write path and pins them by commit; it delegates lens selection to a cheap classifier with a well-specified fallback; and it bounds investigation with an explicit tool-call budget born from a real production failure (#66819). The Evidence section is short, because almost everything published about it is three self-reported runs.

## Mechanism

Everything below was read from the workflow source file on 2026-11-10.

**Frontmatter.** Triggers: `pull_request` with `types: [ready_for_review]` and `paths-ignore` for `*.md`, `docs/**`, `.changeset/**` and `scratchpad/**` (documentation-only changes never start the reviewer), plus a centralized slash command (`name: [matt, review]`) on both pull-request comment and review-comment events. Permissions: `contents: read`, `pull-requests: read`, `copilot-requests: write`. Budget: `max-daily-ai-credits: 10000` and `timeout-minutes: 30` — the timeout carries a source comment explaining the raise: "Raised from 15m: skill-driven PR reviews on larger diffs were hitting the engine step's hard timeout mid-review (not a hang) - see #66819." The engine caps continuations at 6. A `cache` key (`pr-prefetch-v2`) pins the pre-fetched PR data to the PR number, head SHA and run id. Imports: the shared PR-review base (with `min-integrity: approved`), the shared telemetry module, and the shared PR-diff data fetch. Network access is `allowed: [defaults, go]`; GitHub access runs through `gh-proxy` with `cli-proxy: true`.

**The skills, pinned by commit.** Exactly five skills are imported, all pinned to one commit hash `49dd158d1076134a641b33efb035946536778336`: `mattpocock/skills/diagnosing-bugs`, `/tdd`, `/codebase-design`, `/improve-codebase-architecture`, `/grill-with-docs`. They are installed via `gh skill` under `.github/skills/`. The workflow instructs the agent to discover present skills with `find "${GITHUB_WORKSPACE}/.github/skills" -name "SKILL.md" | head -30` and — importantly — to "Use the inline skill guidance below by default. Only read a skill file when the inline guidance is insufficient for the specific PR." The skill text is therefore prompt guidance for the reviewer, not executed code, and the pinned commit is the supply-chain control on that guidance.

**Seven steps.** (1) Load pre-fetched PR data — `/tmp/gh-aw/agent/pr-meta.json` (number, title, body, headRefName, additions, deletions, changedFiles, files), `pr-diff.patch` (lock files and generated artifacts excluded) and `pr-review-comments.json` (existing comments, to avoid duplication) — under an explicit prohibition: "Do NOT call any GitHub MCP tools for PR data." A 3,000-line patch is treated as potentially truncated, and the reviewer must focus on the highest-impact files and call out missing context. (2) Read available skills. (3) Invoke the `pr-triage` helper and use its JSON. (4) Review using the selected skills, focusing on `high_impact_files`, with per-skill focus questions (e.g. `/tdd`: "Are there failing tests written before the implementation?"; `/diagnosing-bugs`: "Is the root cause properly addressed, or only the symptom?"). (5) Post inline review comments. (6) Submit the overall review (`APPROVE` / `REQUEST_CHANGES` / `COMMENT`; an approval is submitted before any check run, and a check run is added only with "a concrete success summary that helps the author or merge queue"). (7) Optionally post one summary comment.

**Triage delegation and its fallback.** `pr-triage` is a `claude-haiku-4.5` sub-agent that classifies the PR into exactly one of seven `change_type` values (`bug_fix`, `new_feature`, `refactor_cleanup`, `architecture_change`, `tests_only`, `documentation`, `mixed_unclear`), recommends 1–2 skills from a fixed mapping table, ranks `high_impact_files` and returns `key_signals`, as strict JSON. The fallback rule is the load-bearing part: "**Fallback — never fail the review because of triage.**" If the call errors, times out, returns empty output or unparseable text, the agent retries at most once, logs one line, then applies the same classification logic itself directly against the pre-fetched data, ranks `high_impact_files` by largest additions + deletions among non-generated changed files, treats `key_signals` as empty — and must "mention in the Step 6 review body that skill selection used the fallback heuristic."

**The investigation budget.** "Large, cross-cutting diffs can tempt open-ended tracing through the codebase to build architectural context — bound that exploration to roughly 20 tool calls beyond Steps 1-3. If you reach that budget without a clear picture, stop investigating and submit the best review supported by the evidence gathered so far (call out remaining uncertainty in the review body) rather than continuing to chase every reference; this is what previously caused engine-step timeouts on large diffs (#66819)." The budget converts a hang-class failure into a bounded, disclosed-uncertainty outcome.

**Write path.** All writes go through gh-aw safe outputs with hard maxima: `create-pull-request-review-comment` max 10, `submit-pull-request-review` max 1, `add-comment` max 1 with `hide-older-comments: true`, and `mentions` restricted to `@copilot`. Comments are emitted by piping JSON to the `safeoutputs` CLI from bash (not as a native tool), with strict encoding rules: apostrophes encoded as `\u0027`, no shell double quotes, control characters escaped rather than raw. Each inline comment is prefixed with its skill name in brackets (`**[/tdd]**`), keeps immediately visible text to 1–2 sentences, wraps code examples and multi-step suggestions in `<details>` blocks, and ends with "@copilot please address this." The review body itself uses progressive disclosure (brief summary visible, themes collapsed). Scope rules cap the work: changed lines only; priority order `security > correctness > maintainability > style`; at most 10 inline comments; skip auto-generated files. Tone is specified: "Professional and collegial — not grumpy, not sycophantic." Abstention is a success criterion: "uses `noop` instead of generic praise when there is nothing useful to say." Every published artifact carries the attribution footer: `> 🧠 *Reviewed using Matt Pocock's skills by [{workflow_name}]({run_url})*{ai_credits_suffix}{history_link}`.

## Evidence

**Inspected facts** (checkable by any reader against the same public file):

| Property | Value | Source |
|---|---|---|
| Triggers | `pull_request` (`ready_for_review`, docs paths ignored) + slash commands `matt` / `review` | frontmatter |
| Permissions | `contents: read`, `pull-requests: read`, `copilot-requests: write` | frontmatter |
| Daily AI credit cap | 10000 | frontmatter |
| Job timeout | 30 minutes (raised from 15; comment cites #66819) | frontmatter |
| Imported skills | 5, all pinned at commit `49dd158d…` | frontmatter |
| Triage model | `claude-haiku-4.5` (inline `pr-triage` agent) | agent definition |
| Triage fallback | ≤1 retry, then inline heuristic + disclosure in review body | step 3 |
| Investigation budget | ~20 tool calls beyond Steps 1–3 | prompt |
| Patch cap | 3,000 lines, treated as potentially truncated | step 1 |
| Safe-output maxima | 10 inline comments, 1 review, 1 summary comment | frontmatter |
| Built-in evals | none declared | frontmatter |

**Vendor claims and vendor telemetry.** The blog reports that "within the last hour of this writing, the workflow ran three times on `pull_request` events, each on a different Copilot-authored branch. All three completed successfully":

| Run | Branch | Duration | Tokens (log summary) |
|---|---|---|---|
| 42229926994 | `copilot/fix-verify-output-id` | 13.1m | 58,142 |
| 42230049178 | `copilot/fix-details-open-escaping` | 11.4m | 51,209 |
| 42230089145 | `copilot/fix-strict-mode-env-vars` | 18.1m | 103,570 |

"A structured audit of run 42230049178 reports zero errors and zero warnings, and an adaptive execution style with four tool types. Its write path was deliberately narrow: one inline pull request review comment and one submitted review. No sprawl, no pile of drive-by comments. The audit also flagged two medium-severity notes: high token usage, and a declared sub-agent model (`pr-triage`) that wasn't observed in the model requests."

**What is not published.** No evaluation of review quality exists anywhere in the inspected material: no false-positive or false-negative rate for the skill-based comments, no maintainer acceptance rate, no comparison against a generic reviewer, and no results for any eval — this workflow, unlike [[projects/github-contribution-check]] (2 built-in evals) and [[projects/pr-sous-chef]] (4), declares **no built-in evals at all**; its "Success Criteria" are prompt text. No token figure carries a stated denominator, and no failing run is represented.

## Limitations

**Flagged by the vendor's own audit.** High token usage, and the declared `pr-triage` sub-agent model was not observed in the model requests. The blog calls this "useful honesty from the tooling, and it is a reasonable starting point for anyone tuning cost on this workflow" — the flag is published, but neither post nor workflow resolves it: either the economy routing overrode the Haiku pin, or the audit's model-request telemetry missed the sub-agent's calls. The sources do not say which.

**Assessed by the KB maintainers:**

- **Token variance is 2× with no explanation.** 51,209 to 103,570 tokens across three similar runs on the same repository; nothing published says what drives the spread, and the 30-minute timeout comment suggests large diffs are the known cost driver.
- **The evidence population is GitHub reviewing its own agent's PRs.** All three runs targeted Copilot-authored branches (`copilot/fix-*`); no run on a human-authored PR is published, and review behaviour on adversarial or messy human diffs is unrepresented.
- **No evals, and no eval results.** The workflow's quality bar lives entirely in prompt text; no published artifact measures whether skill-selected reviews find more real issues than generic review.
- **Third-party guidance in the write path.** The five skills are pinned, which is the right control, but their content was written for a different context (Matt Pocock's engineering guidance); no source evaluates whether applying them to gh-aw's Go/TypeScript codebase produces correct review comments.
- **Truncation by design.** The 3,000-line patch cap means very large PRs are reviewed partially; the workflow requires calling out missing context, but nothing measures how often the cap binds.
- **n = 3 self-reported runs, all successful.** The failure mode (including the #66819 timeout class that shaped the design) is unrepresented in the published evidence.

## Competing approaches

Only alternatives the inspected sources name.

- **A single generic review prompt.** The success criteria state the contrast directly: "focuses on the highest-impact changed lines instead of broad restatement of the PR" and "uses `noop` instead of generic praise" — the alternative is the reviewer that recites the PR and praises everything.
- **Reading the skill files versus inline guidance.** The workflow itself contains both designs and prefers the cheaper one: "Use the inline skill guidance below by default. Only read a skill file when the inline guidance is insufficient for the specific PR."
- **Failing the review when triage fails.** The fallback rule explicitly rejects aborting on a broken classifier: "never fail the review because of triage."
- **Unbounded codebase exploration.** The investigation budget rejects "open-ended tracing through the codebase" in favour of a bounded review with disclosed uncertainty — the design that the #66819 timeouts forced.

(Analyst note, not from the sources: static analysis, linters and human-only review are the obvious non-agentic alternatives for this task; none is named in the inspected material and none is characterised here.)

## Implications

The following is analysis by the KB maintainers, not a claim of GitHub's.

The transferable pattern is **lens selection before depth**: a cheap classifier picks one or two focused review rubrics, and the expensive reviewer applies them instead of a generic checklist. This is [[concepts/structural-constraint-over-instruction]] in a weak form — the change-type-to-skill mapping is prompt text rather than enforced structure — but it is a fixed, published mapping table, which at least makes it auditable. The same idea appears across the gh-aw corpus with different payloads: [[projects/github-contribution-check]] selects the rubric deterministically, [[projects/pr-sous-chef]] selects the work deterministically, and this workflow delegates selection to a model. The spectrum from deterministic selection to model-selected selection is itself the interesting comparison: each step toward model selection buys adaptivity and pays in auditability.

Three smaller lessons generalise. First, **pinning third-party skills by commit hash** is the supply-chain control any workflow that imports external prompt guidance should copy; guidance changes only when the workflow file changes. Second, **the triage fallback is a resilience rule with an honesty clause**: degrade to a deterministic heuristic, cap the retries at one, and disclose the degradation in the output — a concrete instance of [[concepts/abstention-as-first-class-verdict]] turned inside out, where the disclosure rather than the abstention is the terminal output. Third, **the investigation budget shows how to absorb a timeout class of failure**: bound the work, ship the best supported output, and label the residual uncertainty, rather than letting the engine's hard timeout decide the outcome.

The counterweight is familiar from the rest of this corpus: nothing published measures whether skill-selected reviews are *better*, only that they are *shaped* correctly. The mechanism is checkable against the source file; the value is unmeasured, and the audit's own two flags — cost, and a sub-agent whose model it could not observe — are exactly the kinds of open questions that no run table answers.

## Reproducible experiment

The mechanism's claims are falsifiable on a throwaway repository with gh-aw installed; **this protocol has not been run.**

1. **Triage fallback.** Break the `pr-triage` invocation (for example by pointing its model at an unavailable name) on a PR with a mixed bug-fix-plus-refactor diff. Pass criteria: the review still completes, the skill choice follows the inline mapping, `high_impact_files` is ranked by additions + deletions, and the review body states that the fallback heuristic was used. A missing or failed review, or an undisclosed fallback, fails.
2. **Budget bound (#66819 regression).** Open a large cross-cutting refactor PR that tempts reference-chasing. Pass criteria: the run finishes inside the 30-minute timeout and the review body calls out remaining uncertainty where the budget cut exploration short. A run that hits the engine step timeout fails.
3. **Abstention.** Open a small, clean, well-tested code change. Pass criterion: `noop` or an approval with at most minor suggestions; any generic praise comment fails the workflow's own success criterion.
4. **Skill-mapping accuracy.** Construct twenty PRs spanning all seven `change_type` classes, run `pr-triage`, and compare its classification and skill recommendation against human labels. Report per-class agreement. This supplies the accuracy comparison the vendor has not published.
5. **Write-shape conformance.** Run against a PR with many issues. Pass criteria: at most 10 inline comments, exactly one submitted review, at most one summary comment, every comment prefixed with a skill bracket and ending with the `@copilot` prompt, and all payloads valid JSON emitted through the `safeoutputs` CLI.
6. **Cost arm.** Run the same PR set under `mode: economy` versus a pinned non-economy configuration, recording tokens and review usefulness. The audit's "high token usage" flag is the hypothesis under test; the pass criterion is directional — a two-fold token spread on similar PRs should be explainable by diff size or withdrawn as a claim.

## Evidence status

This page is grounded in a full read of two public documents on 2026-11-10, fetched by HTTPS without executing anything: the workflow source (https://raw.githubusercontent.com/github/gh-aw/main/.github/workflows/mattpocock-skills-reviewer.md) and the vendor blog post "Agent of the Day – November 6, 2026" (https://github.github.com/gh-aw/blog/2026-11-06-agent-of-the-day/). **Inspected:** every mechanism statement — triggers, permissions, credit cap, timeout and its #66819 comment, the five pinned skills and their commit, the `pr-triage` agent definition and fallback rule, the investigation budget, the safe-output maxima and encoding rules, the scope and tone rules — comes from the workflow file and can be checked by any reader. **Vendor-claimed:** the three run rows (branches, durations, token counts), the audit of run 42230049178 (zero errors/warnings, adaptive style, four tool types, one comment plus one review), and the two medium-severity audit flags. These are GitHub's reports on GitHub's own repository, with no independent replication and no published denominator. The "assessed" items in Limitations and the whole Implications section are analysis by the KB maintainers, and the reproducible experiment is proposed and not executed. Nothing on this page was installed, cloned, compiled or run by the KB maintainers, and no independent evaluation of this workflow is known to them.

## Historical coverage

- [[briefings/2026/11/2026-11-06]] — finding 2, the dated briefing this page backfills.
- Sibling gh-aw workflows under the same platform: [[projects/github-contribution-check]] (deterministic rubric selection), [[projects/pr-sous-chef]] (deterministic work selection), and the platform page [[projects/github-agentic-workflows]]; the workflow corpus is [[workflows/index]] and the cross-project synthesis is [[evaluations/briefing-synthesis-2026-11-03-to-09]]. Analyst-level comparison only: [[projects/skillcompiler]] treats skills as compilable programs rather than review guidance — a different use of the skills idea, and no source here connects the two. These are analyst-selected thematic comparisons, not source-verified dependencies.
