---
uid: e9c7e0ee-bc7a-428f-baf9-eed1f17ba02f
depth: full
title: "GitHub Copilot Fusion"
summary: "GitHub Copilot Fusion routes each prompt to models and a single, cascade, or critique pattern by capability signals, system health, and effort level."
type: project
created: 2026-11-01
updated: 2026-11-03
related: [improvement-lives-in-external-state]
sources:
  - url: https://github.blog/changelog/2026-10-28-route-and-orchestrate-models-with-github-copilot-fusion/
    retrieved: 2026-11-02
  - url: https://docs.github.com/copilot/concepts/models/copilot-fusion
    retrieved: 2026-11-02
  - url: https://docs.github.com/copilot/concepts/models/auto-model-selection
    retrieved: 2026-11-02
  - url: https://docs.github.com/copilot/how-tos/administer-copilot/manage-for-enterprise/manage-availability-of-default-models
    retrieved: 2026-11-02
---

# GitHub Copilot Fusion

## What it is

GitHub Copilot Fusion is a generally available feature of GitHub Copilot, announced in an October 28, 2026 changelog post. It is selected in the Copilot model picker *instead of* a specific model: the user chooses the Fusion system, and Copilot decides which models to run. GitHub describes it as "an intelligent runtime model router and orchestrator" that "chooses models and execution patterns for your task, then returns a single response."

Fusion is a composite of two earlier GitHub systems: Project HydraFusion contributed the multi-model orchestration, and Copilot auto model selection contributed the model-selection logic ("fine-tuned model selection," in the changelog's wording). Research-preview users (auto, HydraFusion, HydraFusion Max) were automatically transitioned to the corresponding Fusion effort levels.
Per GitHub, Fusion is available on all Copilot plans in Visual Studio Code, the GitHub Copilot app, the Copilot CLI, and JetBrains IDEs. One sub-feature is explicitly not generally available: routing to locally installed models is in public preview (detailed under Mechanism).

The mechanism below is documented in reasonable detail by the vendor; the performance evidence is not independently verified.
## Mechanism

Routing is decided **per prompt**, not per session: different prompts in one conversation can use different models and patterns. For each request, GitHub's documentation says Fusion evaluates the task using capability signals — for reasoning, code generation, debugging, and tool use — together with real-time system health and availability, and selects an execution pattern, reasoning effort, and the models that run it — effort and model choice set per step, not just per prompt. The stated objective is "the most efficient execution pattern that meets the quality bar for your chosen effort level," and Fusion only adds model calls when a task warrants them, so a straightforward task does not pay for a review it does not need.

The selection logic inherited from auto model selection is described as two cooperating systems, one tracking system health and availability, the other evaluating task complexity. Beyond that, the router's internals are unspecified: no signal definitions, no thresholds, no description of how the "fine-tuned" selection model works. Pattern selection is, per GitHub, "a lightweight step that adds minimal latency" — a vendor claim, unquantified. Post-hoc observability is limited: step progress and models can be followed while Fusion works, and the models used are listed under the response (hover the effort-level name), but intermediate drafts are not shown and nothing documents *why* a model or pattern was chosen.

Fusion uses three execution patterns:

- **Single.** One model solves the task directly.
- **Cascade.** An efficient model drafts a response; a quality check (a "judge," in the documentation's terminology) inspects the draft and either accepts it or escalates to a stronger model. Per the changelog's diagram description, escalation goes to a "repair model" that produces a "fresh-start answer" — the draft is discarded, not patched.
- **Critique.** One model drafts a response, another model or models review it, and the original model revises. GitHub's own sources disagree on the critic count — one reviewing model (changelog) versus multiple models critiquing in parallel with feedback aggregated (documentation) — and do not reconcile it, so the count is treated here as unresolved.

The user's main control is the **effort level**, which sets the quality/cost/latency trade-off the router optimises for. Fusion Standard "balances cost, quality, and latency" and, per the documentation, selects one model for each task. Fusion High is balanced orchestration with moderate token savings, aimed at substantial, well-scoped coding tasks where extra model calls may be worth the time and credits. Fusion Max prioritises frontier capability while still considering token efficiency. A fourth level, Fusion Fast, is not user-selectable; it is used only where fast models are required, in Visual Studio Code inline chat. There is no user-facing routing configuration — no rules and no per-task model pinning inside Fusion.

Fusion keeps the main conversation on the same model whenever possible, so it keeps benefiting from cached tokens; assisting models, such as a reviewer, receive only the context they need. Routing occurs along natural cache boundaries and large complexity changes to limit cache costs. Fusion has no context window of its own — each step runs within the limits of the model running it — and the context window displayed for Fusion is a conservative value based on the smallest limits among the models it uses. It works separately from subagents and does not start them.
The local-model preview extends the pool to two locally installed models: MAI Code 1.1 Flash (installable from the Copilot CLI, the Copilot app, or Visual Studio Code on specification-compliant Windows machines) and Qwen3.8 Flash Next (served locally via Ollama in the Copilot CLI, identified as "qwen3.8-flash-next-local"). Either can be chosen only at the Standard effort level and only with experimental features enabled (a "Local model auto routing" app setting, or the CLI's `--experimental` flag); the feature is marked public preview and subject to change. The docs also offer a non-Fusion alternative: a custom agent pinned to a local model, invoked explicitly in the prompt.

The model pool is administrator-controlled and not fixed. Administrators decide, through model policies and a dedicated "Configure Copilot Fusion models" settings page, which models Fusion can pick from; they can view the pool, set each model's effective policy state independently, and disable a model for Fusion without disabling it for everyone. They can also set Fusion, at any effort level, as the default model under Enterprise managed settings. Models are excluded when absent from the user's plan or barred by administrator, data-residency/FedRAMP, or evaluation-model policies; if none is available to a user, Fusion does not appear in their picker. The pool changes as new models become available and as GitHub evaluates which perform best.

Billing is per model used at standard rates, with no separate Fusion charge; High and Max can consume more AI credits than Standard because they may use more than one model. Paid-plan users receive a 30% discount on model costs when using Fusion through November 30, 2026.

## Evidence

Every performance figure for Fusion comes from GitHub's launch changelog. None has independent verification, and each is labelled a vendor claim here.

- **Vendor claim:** in the Artificial Analysis Coding Agent Index, Copilot Fusion Max scored 60. This is GitHub citing a third-party index whose report — methodology, task set, sample size, variance — is not given in the changelog and was not inspected for this page.- **Vendor claim:** that score was "within two points of Claude Code with Opus 5.5 Max" on the same index (the comparator's name as printed in the post; its exact score is not stated).
- **Vendor claim:** Fusion Max delivered that result "at about half the average API cost per task" relative to that comparator, "using about half as many tokens," and took "about 40% less time per task."
- **Vendor claim, unquantified:** pattern selection adds "minimal latency," and performance has improved since Project HydraFusion launched.

The changelog also quotes a customer testimonial — Hari Pokhrel, Principal Software Engineer at AT&T, stating that Fusion Standard "has improved token efficiency across AT&T by automatically selecting the right model for the task." This is a vendor-published testimonial: anecdotal, unquantified, and not independently verified.

That is the entire quantitative record in the sources.

## Limitations

The limitations below are analyst-assessed from the absence of material in the vendor sources, except where a vendor disclosure is quoted.

- **No independent evaluation, no reproducible benchmark.** Every performance number traces to GitHub's own announcement; the single external anchor — the Artificial Analysis index score — is quoted without methodology and was not inspected here, and no task list, harness, prompts, or per-task results are published against which the cost, token, and time claims could be reproduced or audited.
- **No pattern-level or failure-mode data.** The mechanism is documented, but its operating statistics — pattern frequencies, cascade acceptance and escalation rates, critique revision rates — are unmeasured in public, and nothing is published on judge or critic error rates, bad escalations, or quality regressions relative to picking a single frontier model manually.
- **Opaque, moving target.** The router's signals and thresholds are undisclosed, and GitHub states that "the execution patterns and model pool used may change over time." The post-hoc model list names which models ran, not why. Any measurement of Fusion is a snapshot of a system the vendor can silently alter.
- **Unresolved internal inconsistency.** The Critique pattern's critic count differs between the changelog and the documentation (see Mechanism); the sources do not reconcile it.
- **A disclosed operational hazard.** GitHub's documentation warns: "If Copilot Fusion discards a draft, changes that the draft already made in your workspace, such as file edits, aren't undone automatically. Review changes before you commit them." A discarded Cascade draft can therefore leave file edits behind even though its answer was rejected.
- **No baseline comparisons.** Fusion is never quantified against the obvious alternatives: a human picking models, or auto model selection alone. The AT&T testimonial is the only evidence offered on the manual-selection comparison, and it is anecdotal.

## Competing approaches

The alternatives below are the ones GitHub's own sources put next to Fusion. Two of them are also Fusion's ingredient systems — lineage as well as alternatives.

- **Named-model selection (manual picking).** The pre-Fusion default: the user selects a specific model in the picker and switches manually as the work changes. This is the baseline Fusion is positioned against — the AT&T testimonial's complaint is precisely its failure mode, developers choosing a powerful model for a complex task and forgetting to switch back — but the sources offer no benchmark of Fusion against competent manual selection; the testimonial is the whole of the evidence.
- **Copilot auto model selection (the simpler sibling).** Where Fusion is not offered, the picker shows **Auto** instead; auto model selection remains available on surfaces Fusion does not cover, including the cloud, GitHub.com Chat, GitHub Mobile, Eclipse, Xcode, and Visual Studio. It is Fusion's selection half without the orchestration half: the same two cooperating systems route each prompt to a *single* model, along cache boundaries, and the user steers with three tiers — Efficiency (cost), Balance (cost, quality, latency), Intelligence (quality) — rather than effort levels. Paid-plan users get a 10% discount on model costs with auto selection, against Fusion's promotional 30%. Because auto selection is Fusion minus the cascade and critique patterns, it is the natural ablation for isolating what orchestration adds — and GitHub publishes no comparison between the two.
- **A single frontier model for everything.** The quality-first alternative, and the only one with numbers attached: the changelog's comparator, Claude Code with Opus 5.5 Max, against which Fusion Max claims parity within two index points at roughly half the cost and tokens, in 40% less time (all vendor claims, above). The sources name this configuration only as a benchmark comparator, not as a routing or orchestration offering.

GitHub's sources name no third-party model-routing or orchestration products. (Analyst context: third-party LLM routers and gateways exist as a product category, but none is named or evaluated in Fusion's primary sources, so none is characterised here.)
## Implications

Fusion moves model selection from a user decision to a platform behaviour: the user picks an effort level and a policy-bounded pool, and the vendor's router makes per-prompt decisions the user cannot inspect. The effort level and the administrator model policies are therefore the real control surfaces — governance happens at the pool level, not the prompt level. The economics of cascade and critique orchestration are likewise knowable only to the vendor: users are billed per model used for a process whose operating statistics are unpublished. Finally, the discarded-draft disclosure shifts a concrete review burden onto users: an orchestration pattern can leave file edits from an answer the system itself rejected, so reviewing working-tree changes before committing becomes part of using the feature safely.

## Reproducible experiment

No executable artifact exists for Fusion: GitHub publishes no harness, task list, prompts, or per-task results, and Fusion is a hosted feature that cannot be downloaded or version-pinned. There is therefore nothing to reproduce *from* the sources. What follows is the third-party evaluation protocol that *would* test GitHub's claims, specified so the gap between claim and verification is concrete. **It has not been run.**

- **Task suite.** A fixed, published suite of coding-agent tasks spanning the capability categories the router claims to sense — reasoning, code generation, debugging, and tool use — with per-task success criteria frozen in advance.
- **Arms.** (a) Fusion at each user-selectable effort level (Standard, High, Max); (b) each pool model run singly, including the changelog's comparator configuration (Claude Code with the named Opus model); (c) Copilot auto model selection, as the ablation separating routing from orchestration.
- **Quality measurement.** Task-level success scored independently of the vendor. The quality index GitHub cites — the Artificial Analysis Coding Agent Index — should be re-measured by the evaluator rather than quoted: the claims to test are Fusion Max's score of 60 and its position within two points of the comparator, and re-using the vendor-cited number verifies nothing. Sample sizes, per-task outcomes, and variance must be published — the changelog provides none.
- **Cost and latency accounting.** For every task and arm: API cost at published per-model rates, tokens (input, output, and cached reported separately), and wall-clock time. This directly tests the remaining claims — about half the average API cost per task, about half as many tokens, about 40% less time per task, all relative to the comparator arm.
- **Operating statistics.** Using the client's per-response model list, log execution-pattern frequencies, cascade acceptance and escalation rates, and critique revision rates per effort level — the statistics the vendor sources omit (see Limitations).

Two limits would apply even to a well-run version of this protocol. It measures a hosted system the vendor can change silently, so its results are a dated snapshot, not a property of a fixed artifact; and effort levels are trade-off policies that cannot be held constant across systems, so comparisons inherit the comparator's own settings as a confound. Neither limit excuses the current record: as far as the sources show, no arm of this protocol has been executed by anyone outside the vendor.

## Evidence status

Vendor announcement only. The entire evidence base for this page is GitHub's changelog post and GitHub's product documentation — the vendor describing its own generally available product. There is no paper, no benchmark with inspectable methodology, and no independent evaluation or replication in the sources. The one third-party figure (the Artificial Analysis index score of 60) is quoted by the vendor without methodology, and the one customer data point (AT&T) is a vendor-published testimonial. Mechanism descriptions above are vendor-stated product behaviour — a reasonable basis for describing what the feature is, not evidence for how well it works. Nothing about this evidence base has changed since the page was first written: the four sources were re-checked on 2026-11-03, with no material change found. The promotion from `brief` to `full` reflects the completeness of the treatment — the full nine-section apparatus, an expanded mechanism and competing-approaches analysis, and an explicit (unrun) evaluation protocol — and **not** any improvement in the underlying evidence, which remains exactly as weak as the Evidence section records.

## Historical coverage

[Briefing 2026-11-01](../briefings/2026/11/2026-11-01.md)
