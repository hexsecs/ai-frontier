---
uid: a573ebff-6226-41c3-b231-a38fddd96584
title: "AgenTopology — Declarative multi-agent topology"
summary: "TypeScript project defining a declarative .at language for agent teams, with a 109-rule validator and scaffold/plan targets for Claude Code, Codex and Cursor."
type: project
created: 2026-11-10
updated: 2026-11-10
depth: deep
sources:
  - https://github.com/agentopology/agentopology
  - https://raw.githubusercontent.com/agentopology/agentopology/main/README.md
  - https://raw.githubusercontent.com/agentopology/agentopology/main/package.json
  - https://raw.githubusercontent.com/agentopology/agentopology/main/CHANGELOG.md
  - https://raw.githubusercontent.com/agentopology/agentopology/main/LICENSE
  - https://raw.githubusercontent.com/agentopology/agentopology/main/spec/grammar.md
  - https://raw.githubusercontent.com/agentopology/agentopology/main/spec/validation.md
  - https://raw.githubusercontent.com/agentopology/agentopology/main/src/parser/validator.ts
  - https://raw.githubusercontent.com/agentopology/agentopology/main/src/plan/brief.ts
  - https://raw.githubusercontent.com/agentopology/agentopology/main/src/plan/render.ts
  - https://raw.githubusercontent.com/agentopology/agentopology/main/examples/code-review.at
  - https://raw.githubusercontent.com/agentopology/agentopology/main/docs/PRIOR_ART.md
  - https://registry.npmjs.org/agentopology
---

# AgenTopology — Declarative multi-agent topology

## What it is

AgenTopology is a TypeScript project published to npm as `agentopology`: a declarative language (`.at` files) for describing a team of agents — who works, when they work, and what they know when they work — plus a CLI that validates such a file, scaffolds platform-native agent configuration from it, or renders an execution brief for a coding agent that is already running.

Identity and maintenance. The repository is `agentopology/agentopology`, a GitHub organisation account; `package.json` names the author as **Nadav Naveh** and the README closes with the same attribution. The licence is **Apache-2.0** (the repository `LICENSE` file is the full Apache 2.0 text, and the npm registry entry reports the same SPDX identifier). The homepage is `agentopology.com`. The GitHub API reports the repository as created **2026-03-11T22:51:18Z**, public, TypeScript, with 107 stars at inspection time.

Version evidence. The `package.json` on `main` carries `"version": "0.9.2"`, and the npm registry reports `latest: 0.9.2`, published **2026-11-09T13:05:37Z**; the first publish, `0.1.0`, is timestamped **2026-03-19T09:23:06.787Z** on the registry, with 21 versions in total and a release every few weeks. The release evidence is split across channels: git tags run to `v0.8.0`, but the GitHub Releases feed stops at **v0.5.1, published 2026-08-26**, and the repository's own `CHANGELOG.md` has an `[Unreleased]` section that announces the removal of four bindings "in 0.10.0" — a version that is not published. The README still carries a "New in 0.4" banner while the CLI reference documents a `guard` command and an `inventory` command that the changelog places in 0.9.x.

Maturity signals. The repository contains 110 TypeScript source files and 51 vitest test files across `src/**/__tests__` and `src/__tests__/e2e`, 10 example topologies under `examples/`, plus `kitchen-sink.at` and `openclaw-battle-test.at` at the root. The validator implements rule identifiers **V1 through V109**. Against that, there is **no CI configuration**: the `.github` directory contains only `ISSUE_TEMPLATE/` and `PULL_REQUEST_TEMPLATE.md`, with no `workflows/` directory, so neither the test suite nor the rule set is enforced by the project's own automation. No peer-reviewed venue, third-party audit or independent replication is referenced anywhere in the inspected files.

## Mechanism

**The language.** `spec/grammar.md` ("AgenTopology Language Specification v1.0", created by Nadav Naveh) defines the `.at` extension and states four principles: single-valued constructs, single source of truth, readability by a non-engineer, and parseability — the grammar is declared **LL(2)**, so a compiler can extract the full graph deterministically in O(n) without backtracking. Lexical rules fix a small primitive set (quoted strings, numbers, booleans, lowercase identifiers with hyphens, uppercase template variables), and one rule per line is mandatory for key-value fields, because unquoted multi-token values would otherwise be ambiguous; the spec's own example shows `model: sonnet retry: 3` collapsing into one value. Blocks are keyword-delimited with braces (`agent explorer { ... }`, `meta { ... }`, `gate validation { ... }`); lists are bracketed and comma-separated, with an explicit `[]` meaning "none" as distinct from an omitted field. Paths resolve relative to the scaffolded output directory, except `agent.reads`/`agent.writes`, which are runtime workspace paths.

The node and edge vocabulary visible in `examples/code-review.at` covers `topology` (with `meta`, `providers`, `orchestrator`, `roles`), `action`, `agent`, `gates`/`gate`, `flow` edges with `[when ... , max N]` attributes, `memory`, `triggers`, `hooks` and `settings` with `allow`/`deny` lists. Agents carry `model`, `role`, `permissions` (`supervised`/`autonomous`), `phase`, `tools`, `reads`, `writes`, `behavior: advisory`, `outputs` with pipe-separated typed enums, and an inline `prompt` block. The `flow` block in that example expresses fan-out (`intake -> [analyzer, security-scanner]`), conditional routing on an agent's declared output (`[when reviewer.verdict == approve]`) and a gate placed between two nodes. The README documents further constructs not exercised in that file: `group` blocks with `speaker-selection`, `max-rounds` and `termination`; `store brain` with `type: brain`, `path` and `format: obsidian`; `agent custodian-of:`; `mcp-servers` with `env`; `hooks` with `on:`/`matcher:`/`run:`; memory stores with eleven backends and retrieval strategies.

**Parser and validator.** `src/parser/` holds `lexer.ts`, `ast.ts`, `index.ts`, `known-fields.ts`, `paths.ts`, `run.ts` and `validator.ts`. The validator is 3,846 lines and contains rule identifiers V1–V109, with severities `error` and `warning`; the README and CLI reference both describe "109 rules". `spec/validation.md` documents a different, smaller set — it opens with "These 35 rules are enforced by the `.at` compiler at parse time" and contains 35 `## Rule` headings — and its examples show concrete failure modes: duplicate names, reserved keywords, dangling flow references, orphan agents, conditions on undeclared `outputs`, back-edges without `max N`, agents without a `model`, imports that do not resolve, and actions in `flow` that the orchestrator does not `handles`. The validator also holds the enforcement-metadata rules added late in the changelog: **V104**–**V106** (the `strength`, `by`, `at`, `match`, `bypass` and `guard` vocabulary), **V107** (a hook matcher that can never match, such as permission-rule syntax `Bash(rm -rf *)`), **V108** (`exit 1` does not block; only `exit 2` does) and **V109** (a `strength: refuse` hook whose matcher misses a named tool of the guarded MCP server).

**Two lifecycles.** The README separates `scaffold` from `plan`. `scaffold` writes platform configuration to disk (`.claude/agents/`, `.claude/skills/`, `.mcp.json`, `.claude/settings.json` for Claude Code; `.codex/config.toml` and `AGENTS.md` for Codex; `.cursor/rules/*.mdc`, `.cursor/mcp.json` and `.cursor/hooks.json` for Cursor; a `<topology>.workflow.js` plus `-SEAM.md`, `-README.md` and `-LOSSY-REPORT.md` for the experimental Claude Workflow target). `plan` writes nothing: it validates, resolves execution order and hands the host coding agent a markdown brief, on the reasoning that the agent already in the session is the runtime. The README's own table states the difference sharply — `scaffold` gives "real hooks, mechanically enforced" gates, while `plan` gives an "evidence contract".

**The execution brief.** `src/plan/brief.ts` and `src/plan/render.ts` are where the interesting contracts live. `buildExecutionBrief` computes a typed structure and `renderBriefMarkdown` is the only shipped renderer; the file's own header explains the choice of markdown — the consumer is a language model on three vendors, and JSON "invites the model to summarize the document rather than execute it". The typed structures are:

- `Handoff { from, to, passes, withholds }`, where `passes` is the writer's `writes` intersected with the reader's `reads` — "what actually crosses" — and `withholds` is the rest of the writer's outputs, deliberately not offered to the reader.
- `BlindPair { step, a, b }` — two roles in the same step with no edge between them, which the README motivates directly: "two researchers who see each other's work are one opinion, paid for twice".
- `GateTier`, an ordered ladder from strongest to weakest: `preventive` (tool allowlist, needs a file), `enforced` (hook, exit code 2, needs a file), `fileless-verify` (Workflow script, Claude Code only), `evidence-orchestrator`, `evidence-agent`, `advisory`. The comment states the tier "is chosen by what the host platform actually offers, not by preference".
- `StepEvidence = "present" | "missing" | "undecidable"`, where "undecidable" is described as a first-class answer rather than a failure, because a gate, a human node, or an agent declaring no outputs cannot be judged from declared writes.
- `Unenforceable { node, field, declared }` and `PreflaggedAmbiguity { kind, at, question, alternatives, fix }`, where `fix` is "a concrete `.at` edit that removes the ambiguity. This is the payoff."
- `Autonomy = "plan" | "execute" | "auto"`, the three notches the README describes as show-and-wait, run-and-announce, and run-and-report.

The renderer emits a front-matter header (`brief: agentopology/v1`, topology, version, source, root, autonomy, ambiguity-log), a section that refuses to enact a topology that does not validate, and per-role cards containing TASK CONTEXT, ROLE, INSTRUCTIONS, INPUTS, OUTPUTS, ISOLATION, WITHHELD, a section titled "TOOL POLICY — DECLARED BUT NOT ENFORCED", and a RETURN PROTOCOL requiring exactly one fenced ````at-output` block. The WITHHELD section instructs the role not to read the upstream role's files and to say so in its reply rather than reading them.

**Declared versus enforced.** The README is explicit that five features are platform *registrations* rather than steps — `triggers`, `schedules`, `mcp-servers`, `hooks`, and per-agent `tools`/`permissions` — and that they "cannot work fileless on any vendor", so `plan` names them instead of silently skipping them. The `plan` output in the README shows the two warnings this produces: roles whose tool restrictions "cannot be set inline — running unrestricted", and triggers and hooks that "need `agentopology scaffold`". For the file-based path the changelog records the opposite failure and the fix: on 0.9.1 a gate could fail open, because Claude Code blocks only on exit 2, `before-agent.sh` exited 1 with `CLAUDE_PROJECT_DIR` unset, `jq` missing produced 127, and a never-written gate script exited 0 — in each case the agent launched with its gate skipped; 0.9.2 makes those paths exit 2.

**Enforcement auditing.** The `guard` command and `guard <file> --check` read-only subcommand are the project's own answer to the declared-versus-enforced gap: for every gate, approval step and deny/ask rule, it works out what the Claude Code binding compiles it to and then inspects the project, classifying each step as `refuse` (its hook or settings rule is on disk and anchored to `$CLAUDE_PROJECT_DIR`), `none` (the binding generates one but the project lacks it), or `hope` (no hook exists; only prose asks for it), and it prints "enforcement: k of m steps refuse". A gate may cite the code that refuses with `at: "path:line"` and `match:`, and `guard --check` verifies the citation on disk. The `inventory` command and `validate --inventory` complete the loop from the other side: they enumerate what is live in a project (every `.claude` file with its sha256, each `settings.json` hook handler, each `.mcp.json` server, each `package.json` script) and report "coverage: k of n live things are in the .at".

**Round trip and outputs.** `src/import/` (a Claude Code importer, `serializer.ts`, `flow.ts`, `walk.ts`) supports reverse-engineering platform files back into `.at`; `src/exporters/` renders markdown, mermaid, JSON, ascii and brief; `src/visualizer/` produces an interactive graph, and `visualize-brain` renders a markdown vault as a self-contained HTML file. The repository also ships its own development topology (`.claude/topologies/parser-dev.at`) and six `.claude/agents/` role files, so the tool is used to build itself.

## Evidence

Everything in this section was established by reading files over HTTPS on 2026-11-10. Nothing was executed.

| Artefact inspected | What it establishes | Kind |
|---|---|---|
| `package.json` | name `agentopology`, version 0.9.2, Apache-2.0, author Nadav Naveh, `bin: agentopology → dist/cli/index.js`, subpath exports for `/parser`, `/bindings`, `/plan`, `/render`, `/resolve`; scripts `build` (tsc), `test` (vitest run), `drift` | code-inspected |
| `src/parser/validator.ts` (3,846 lines) | rule identifiers V1–V109 present; severities `error`/`warning`; enforcement-metadata rules V104–V109 | code-inspected |
| `spec/grammar.md` | LL(2) claim, primitive types, one-field-per-line rule, block/list/enum syntax, path-resolution table | code-inspected (documented spec) |
| `spec/validation.md` | documents **35** rules with worked invalid/valid examples — fewer than the 109 the validator implements | code-inspected |
| `src/plan/brief.ts` (594 lines) | `Handoff`, `BlindPair`, `GateTier`, `StepEvidence`, `Unenforceable`, `PreflaggedAmbiguity`, `Autonomy` types; the comment that ~70% of agents across 11 topologies declare `writes` and are therefore decidable | code-inspected |
| `src/plan/render.ts` | brief header fields, refusal section, per-role card sections including "TOOL POLICY — DECLARED BUT NOT ENFORCED" and the ````at-output` return protocol | code-inspected |
| `examples/code-review.at` | a complete topology exercising providers, orchestrator, roles, actions, agents with typed `outputs`, fan-out flow, a gate, memory, triggers, hooks and settings allow/deny | code-inspected |
| `CHANGELOG.md` | per-version change record; the `guard`, `inventory`, `strength`/`by`/`at`/`match`/`bypass`/`guard` feature set; the 0.9.2 fail-closed gate fix; the `[Unreleased]` removal of four bindings | code-inspected |
| `docs/PRIOR_ART.md` | the project's own priority claim (published March 2026, "graph engineering" terminology circulating July 2026) and its explicit list of named predecessors | claim, in-project |
| npm registry | 21 versions, `0.1.0` on 2026-03-19, `0.9.2` on 2026-11-09 | registry record |
| GitHub API | repository created 2026-03-11, 107 stars, no `workflows/` under `.github` | registry record |
| File tree (`main`) | 197 blobs, 110 `.ts` files, 51 vitest test files, 10 example `.at` files, 17 docs, 7 spec files | code-inspected |

## Limitations

**Stated by the project itself.** The README says the experimental targets are "kept, not verified the way claude-code is", that `plan` "cannot spawn agents itself, so it does not pretend to", and that four features cannot work fileless on any vendor. The changelog records open findings it did not fix: a hook whose `run` is `exit 1` scaffolds a stub that exits 0 (**N29**) and a matcher in permission-rule syntax never matches a tool name (**N30**). `docs/PRIOR_ART.md` states plainly that the data plane of the graph is unfinished — that `EdgeDef` carries twelve fields and "all twelve are control plane", and that the context graph is the harder half the project is still building.

**Assessed from the inspected files.**

- **No evaluation of any kind.** No benchmark, ablation, productivity study or user study appears in the inspected files. The only quantitative claim about the project's own history is the priority argument in `docs/PRIOR_ART.md`, which is a date comparison against a terminology trend and is explicitly not a claim of priority over named projects. This is a large gap against the README's framing.
- **The docs lag the code, and the code lags its own version numbers.** `spec/validation.md` documents 35 rules while the validator implements 109; the README's programmatic-API comment says "109 built-in rules, V1-V106" while the validator also implements V107–V109; the README's platform table lists 4 targets while its lifecycle table says "8 targets"; the README banner says "New in 0.4" while npm is at 0.9.2; and the changelog's `[Unreleased]` section announces a 0.10.0 removal that has not shipped. Establishing the current supported target set requires reading three files and reconciling them, not reading one.
- **No CI.** With no workflow files, the 51 test files, the rule set and the `npm run drift` hook-contract check are not run automatically on the project's own commits. Nothing in the inspected files establishes that the suite passes at the published version.
- **Fileless mode is enforcement-free by construction.** In `plan` mode the tool restrictions, hooks, MCP registrations and triggers are named as unenforceable and the brief's own heading says "DECLARED BUT NOT ENFORCED". A gate in that mode degrades to `evidence-orchestrator` or `evidence-agent`, which means the agent's own report is the evidence. Whether any host agent actually follows the brief — the `at-output` return protocol, the WITHHOLDED instruction, the blind-pair separation — is untested in the inspected files.
- **Handoffs are computed from declarations, not observations.** `passes` and `withholds` are derived from declared `writes`/`reads`; the `present`/`missing`/`undecidable` evidence check only looks at whether the filesystem holds what was declared. An agent that writes a file it never declared is invisible to the contract. This is the same declared-versus-observed gap that [[projects/receipt]] documents for process state.
- **Group chats have no concurrency semantics.** The README says group chat compiles to "a file-based protocol — a shared transcript file that agents read and append to sequentially", so the declared `speaker-selection`, `max-rounds` and `termination` are implemented as text sequencing rather than as a scheduler.
- **Scale and portability are unevidenced.** The only scale datum in the inspected files is a code comment ("31 of 44 agents across 11 real topologies declare `writes`"), over an unstated corpus. No target other than Claude Code is described as verified.
- **Single-maintainer provenance.** The specification, the package metadata and the README all name one author; no reviewer, steward or organisation is identified.

## Competing approaches

Only alternatives the source itself names. `docs/PRIOR_ART.md` names **LangGraph**, **AutoGen** and **Google ADK** as "also doing graph orchestration before the vocabulary arrived", while claiming a narrower priority about the term rather than over the projects. The README names **OpenClaw** as the platform whose `soul.md`, skill files, channel configs and gateway setup the `.at` file is meant to replace, and the changelog records the removal of the `openclaw` binding and importer in the unreleased section. The README positions the project against hand-maintained configuration ("You spend hours wiring up AGENT.md files, soul.md configs, MCP servers, hooks, and scripts") and against a database-backed memory layer, where the Company Brain is described as "Pure markdown, zero infrastructure. No vector DB, no MCP server." The "Terraform for AI agents" slogan names an analogy to declarative infrastructure, and the `claude-workflow` target is the project's own alternative compilation path for deterministic fan-out phases, documented in `docs/AT_VS_WORKFLOW_STRATEGY.md`.

## Implications

The following is analysis by the KB maintainers, not a claim of the project.

The most transferable idea is that a declaration and its enforcement should be separate artifacts with an explicit audit between them. AgenTopology's `guard --check` triage — `refuse`, `none`, `hope` — is a concrete, machine-derivable answer to a question most multi-agent frameworks leave implicit: does anything actually stop the agent? It generalises beyond this tool: any declarative policy layer should be able to answer "of the restrictions I declared, how many are mechanically enforced, and how many are merely advisory?", and should fail closed on the difference. That is the concrete form of [[concepts/validation-tier-gap]] and [[concepts/scoped-assurance]] applied to agent configuration.

Second, the handoff contract is worth borrowing as a schema rather than as a product. `passes = writes ∩ reads`, `withholds = the rest`, plus an explicit blind-pair list, is a compact way to say what crosses a boundary and what must not — and it generalises the concern behind [[projects/receipt]] and [[concepts/verified-completion-vs-apparent-success]] to the *data* plane rather than the *effect* plane. The related move of computing what is deliberately withheld, and telling the downstream role in advance that it must not read it, is a design pattern that would apply to any staged agent pipeline.

Third, the ambiguity log is a good mechanism. Logging every decision the host agent would have had to guess, each with the concrete file edit that would remove the guess, converts a specification into a patch queue. That is more actionable than a lint warning and more honest than a best-effort resolution. It is the same instinct as [[concepts/structural-constraint-over-instruction]]: put the constraint in the artifact rather than in the instruction.

Fourth, and as a caution: the repository's own internal inconsistency — 35 documented rules against 109 implemented, four targets against eight, a 0.4 banner against a 0.9.2 package — is a reminder that a declarative artifact's value depends entirely on the compiler behind it. Nothing in a `.at` file establishes that the tool that reads it is current, correct or even tested in CI. A team adopting this pattern should treat the generator's conformance tests as the real deliverable, not the language.

Finally, in a broader frame, the project's own split between "the execution graph" and "the context graph" is a useful diagnostic for any agent-orchestration design: it is easy to declare who calls whom, and much harder to declare what crosses the call. Most multi-agent frameworks in this KB's corpus specify the first.

## Reproducible experiment

The central claim to test is that a single declarative topology produces equivalent, verifiable agent-team behaviour on more than one platform, and that the difference between declared and enforced restrictions can be measured rather than asserted. A feasible protocol:

1. **Author one topology.** Write a researcher → builder → adversarial-reviewer team in `.at` with three agents, a `gate` between builder and reviewer running a script, declared `reads`/`writes` on each role, an `outputs` verdict enum, and per-agent `tools` lists that differ between roles.
2. **Scaffold to two targets.** Run `agentopology scaffold` for `claude-code` and for `codex`, and diff the generated permission surfaces — which tools each role is granted, whether the deny list survives, how the gate becomes a hook in each target. Record every declared restriction that is not mechanically present in the generated files.
3. **Run the plan path.** Run `agentopology plan` on the same file with `--mode plan` and record, verbatim, the unenforceable declarations the tool reports and the "DECLARED BUT NOT ENFORCED" section of the brief. Pass criterion: the tool names every registration-type feature it cannot honour and none of them is silently omitted.
4. **Audit enforcement.** In a throwaway project containing the scaffolded files, run `agentopology guard <file> --check`. Pass criterion: the tool reports each step as `refuse`, `none` or `hope` with a reason, and the count of `refuse` steps equals the number of gates and deny rules that are actually present in the generated `.claude/settings.json` — a mismatch in either direction fails the check.
5. **Behavioural cross-check.** Run the same task on each platform with the same model and the same budget, and compare only what the tool can be held to: the handoff set actually read by each role (from the transcript), whether the withheld file was read, and whether the gate script ran and blocked. The pre-registered failure condition is a role reading a file the topology withholds, or a gate that never blocked on a deliberately failing check.
6. **Round-trip check.** Run `agentopology sync` and `agentopology import --target claude-code` over the scaffolded directory and diff the reconstructed `.at` against the original. A pass is a diff that contains only known lossy conversions, which the tool is expected to report rather than hide.

Report per-target results separately; do not average across targets, because the README explicitly treats only Claude Code as verified. Substituting models or agent versions changes the behavioural comparison and should be reported as a substitution.

## Evidence status

Grounded in HTTPS reads on **2026-11-10** of: the repository page and GitHub API repository record for `agentopology/agentopology`; `README.md`, `package.json`, `CHANGELOG.md`, `LICENSE`, `spec/grammar.md`, `spec/validation.md`, `src/parser/validator.ts`, `src/plan/brief.ts`, `src/plan/render.ts`, `examples/code-review.at` and `docs/PRIOR_ART.md` from `https://raw.githubusercontent.com/agentopology/agentopology/main/…`; the recursive file tree of `main` via the GitHub API; the `spec/claude-code/hooks-contract.json` and `hooks-contract.2.1.295.json` snapshots named in the changelog; and the npm registry record for `agentopology`.

Code-inspected facts: the 109 rule identifiers and their severities in the validator; the grammar and validation rule sets as written in `spec/`; the type definitions and brief structure in `src/plan/`; the example topology's constructs; the changelog's per-version claims; the npm and GitHub timestamps and counts. Claims, not verified here: every efficacy, adoption or priority claim in the README and in `docs/PRIOR_ART.md`; the description of the 0.4→0.9.x feature history in the changelog (read as text, not as verified behaviour); and the comment-level statistic "31 of 44 agents across 11 real topologies declare `writes`", whose corpus is not identified in the inspected files. The project ships no CI configuration, no benchmark and no independent evaluation; none is known to this knowledge base.

**Nothing on this page was executed, installed, cloned, built or benchmarked by the KB maintainers.** No project code was run; only text files were fetched over HTTPS.

## Historical coverage

- [[briefings/2026/11/2026-11-10]] — dated full-fidelity research and cross-project synthesis; this page retains that snapshot's "v0.4 described, release date unverified" caveat as superseded by the registry and repository records fetched here.
