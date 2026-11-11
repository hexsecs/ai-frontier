---
uid: e9c7e0ee-bc7a-428f-baf9-eed1f17ba02f
depth: deep
title: "GitHub Copilot Fusion"
summary: "GitHub Copilot Fusion: generally available runtime router and orchestrator for Copilot models and execution patterns."
type: project
created: 2026-11-01
updated: 2026-11-10
related: ["improvement-lives-in-external-state"]
sources:
  - url: https://github.blog/changelog/2026-10-28-route-and-orchestrate-models-with-github-copilot-fusion/
    retrieved: 2026-11-02
  - url: https://docs.github.com/copilot/concepts/models/copilot-fusion
    retrieved: 2026-11-02
  - url: https://docs.github.com/copilot/concepts/models/auto-model-selection
    retrieved: 2026-11-02
  - url: https://docs.github.com/copilot/how-tars/administer-copilot/manage-for-enterprise/manage-availability-of-default-models
    retrieved: 2026-11-02
  - https://docs.github.com/copilot/reference/copilot-billing/models-and-pricing
---

# GitHub Copilot Fusion

## What it is

GitHub Copilot Fusion is a generally available feature of GitHub Copilot, announced in the changelog post "Route and orchestrate models with GitHub Copilot Fusion" on October 28, 2026, and documented in the GitHub Copilot documentation under "About GitHub Copilot Fusion". Instead of selecting a specific model for each task, the user selects **Copilot Fusion** in the model picker and chooses an effort level; Copilot then routes and orchestrates models for the task and returns a single response. GitHub describes Fusion as "an intelligent runtime model router and orchestrator" that "chooses models and execution patterns for your task, then returns a single response."

Fusion is a composite of two earlier GitHub systems: Project HydraFusion, which contributed the multi-model orchestration, and Copilot auto model selection, which contributed the model-selection logic that GitHub calls "fine-tuned model selection". Research-preview users of auto, HydraFusion, and HydraFusion Max were automatically transitioned to the corresponding Fusion effort levels. GitHub states Fusion is generally available on all Copilot plans in Visual Studio Code, the GitHub Copilot app, the Copilot CLI, and JetBrains IDEs; routing to locally installed models is in public preview.

## Mechanism

Routing is decided per prompt rather than per session: different prompts in one conversation can use different execution patterns. For each request, GitHub's documentation says Fusion evaluates the task using capability signals for reasoning, code generation, debugging and tool use, together with real-time system health and availability, and selects an execution pattern, reasoning effort and the models that run it; effort and model choice are set per step.

The stated objective is "the most efficient execution pattern that meets the quality bar for your chosen effort level", and Fusion only adds model calls when a task warrants them, so a straightforward task does not wait or use AI credits for a review it does not need.

Fusion uses three execution patterns. **Single** has one model solve the task directly. **Cascade** has an efficient model draft a response, with a quality check that accepts the draft or escalates to a stronger model; per the changelog's diagram description, escalation goes to a "repair model" that produces a "fresh-start answer", the draft being discarded rather than patched. **Critique** has one model draft a response while another model reviews it and the original model revises; GitHub's own sources disagree on the critic count (one reviewing model per the changelog, multiple models critiquing in parallel with feedback aggregated per the documentation) and do not reconcile this, so the count is treated as unresolved.

The user-facing control is the effort level, which sets the quality/cost/latency trade-off the router optimises for: Fusion Standard "balances cost, quality, and latency" and selects one model for each task; Fusion High is "balanced orchestration with moderate token savings", aimed at substantial, well-scoped coding tasks where extra model calls may be worth the time and credits; Fusion Max prioritises frontier capability while still considering token efficiency; Fusion Fast is not user-selectable and is used only where fast models are required, in Visual Studio Code inline chat. Administrators instead control the model pool through model policies and the "Configure Copilot Fusion models" settings page, and can set Fusion, at any effort level, as the default model under Enterprise managed settings.

Fusion keeps the main conversation on the same model whenever possible, so it keeps benefiting from cached tokens, while assisting models such as a reviewer receive only the context they need; routing occurs along natural cache boundaries and large complexity changes. Fusion has no context window of its own — each step runs within the limits of the model running it — and the context window displayed for Fusion is a conservative value based on the smallest limits among the models it uses.

The local-model preview extends the pool to two locally installed models: MAI Code 1.1 Flash, installable from the Copilot CLI, the Copilot app or Visual Studio Code on specification-compliant Windows machines, and Qwen3.8 Flash Next, served locally via Ollama in the Copilot CLI and identified as "qwen3.8-flash-next-local". Either can be chosen only at the Fusion Standard effort level and only with experimental features enabled (a "Local model auto routing" app setting, or the CLI's `--experimental` flag); the docs mark this feature public preview and subject to change, and offer a non-Fusion alternative of a custom agent pinned to a local model invoked explicitly in the prompt.

Billing runs per model used at standard rates, with no separate Fusion charge; because Fusion High and Max can use more than one model, a task may consume more AI credits than it would with Fusion Standard, and paid Copilot plan users receive a 30% discount on model costs when using Fusion through November 30, 2026. GitHub documents that Fusion works separately from subagents and does not start them; this is one of the disclosed Copilot Fusion limitations.

The documentation notes that Fusion chooses an execution pattern when needed, for each prompt, so different prompts in the same session can use different patterns; the docs give the example that a first prompt using the single pattern may be followed by a follow-up using the critique pattern.

While Fusion works, the documentation says the user can follow the progress of each step and the model being used, and that intermediate drafts might be revised or discarded, so Fusion shows the final response only.

## Evidence

Every performance figure for Fusion comes from GitHub's launch changelog; none has independent verification, and each is labelled a vendor claim here.

- **Vendor claim:** in the Artificial Analysis Coding Agent Index, Copilot Fusion Max scored 60. This is GitHub citing a third-party index whose report — methodology, task set, sample size, variance — is not given in the changelog and was not inspected for this page.
- **Vendor claim:** that score was "within two points of Claude Code with Opus 5.5 Max" on the same index (the comparator's name as printed in the post; its exact score is not stated).
- **Vendor claim:** Fusion Max delivered that result "at about half the average API cost per task" relative to that comparator, "using about half as many tokens," and took "about 40% less time per task."
- **Vendor claim, unquantified:** pattern selection adds "minimal latency," and performance has improved since Project HydraFusion launched.

The changelog also quotes a customer testimonial — Hari Pokhrel, Principal Software Engineer at AT&T, stating that Fusion Standard "has improved token efficiency across AT&T by automatically selecting the right model for the task", reducing unnecessary spend and preserving capacity for higher-value work; he adds that "We've also seen its decision-making improve over time". This is anecdotal, unquantified, and not independently verified.

That is the entire quantitative record in the sources. The mechanism descriptions above are vendor-stated product behaviour — a reasonable basis for describing what the feature is, not evidence for how well it works. The administrator-side model controls and billing terms documented alongside the announcement are product documentation, not performance evidence.

GitHub publishes no evaluation of Fusion's behaviour in production, and the sources inspected contain no accuracy, pattern-frequency or failure-mode data; the only published quantitative content is the changelog's vendor claims and the quoted AT&T testimonial.

## Limitations

The limitations below are analyst-assessed from the absence of material in the vendor sources, except where a vendor disclosure is quoted.

- **No independent evaluation, no reproducible benchmark.** Every performance number traces to GitHub's own announcement; the single external anchor — the Artificial Analysis index score — is quoted without methodology and was not inspected here, and no task list, harness, task set, prompts, or per-task results are published against which the cost, token and time claims could be reproduced or audited.
- **No pattern-level or failure-mode data.** The mechanism is documented, but its operating statistics — pattern frequencies, cascade acceptance and escalation rates, critique revision rates — are unmeasured in public, and nothing is published on judge or critic error rates, bad escalations, or quality regressions relative to picking a single frontier model manually.
- **Opaque, moving target.** The router's signals and thresholds are undisclosed, and GitHub states that "the execution patterns and model pool used may change over time". The post-hoc model list names which models ran, not why. Any measurement of Fusion is a snapshot of a system the vendor can silently alter.
- **Unresolved internal inconsistency.** The Critique pattern's critic count differs between the changelog and the documentation (see Mechanism); the sources do not reconcile it.
- **A disclosed operational hazard.** GitHub's documentation warns: "If Copilot Fusion discards a draft, changes that the draft already made in your workspace, such as file edits, aren't undone automatically. Review changes before you commit them." A discarded Cascade draft can therefore leave file edits behind even though its answer was rejected.

## Competing approaches

The alternatives below are the ones GitHub's own sources put next to Fusion.

- **Named-model selection (manual picking).** The pre-Fusion default: the user selects a specific model in the picker and switches manually as the work changes. This is the baseline Fusion is positioned against — the AT&T testimonial's complaint is precisely its failure mode, developers choosing a powerful model for a complex task and forgetting to switch back — but the sources offer no benchmark of Fusion against competent manual selection; the testimonial is the whole of the evidence.
- **Copilot auto model selection (the simpler sibling).** Where Fusion is not offered, the picker shows **Auto** instead; auto model selection remains available on surfaces Fusion does not cover. It is Fusion's selection half without the orchestration half: the same two cooperating systems route each prompt to a *single* model, along cache boundaries, and the user steers with three tiers — Efficiency (cost), Balance (cost, quality, latency), Intelligence (quality) — rather than effort levels. Paid-plan users get a 10% discount on model costs with auto, against Fusion's promotional 30%. Because auto selection is Fusion minus the cascade and critique patterns, it is the natural ablation for isolating what orchestration adds — and GitHub publishes no comparison between the two.
- **A single frontier model for everything.** The quality-first alternative, and the only one with numbers attached: the changelog's comparator, Claude Code with Opus 5.5 Max, against which Fusion Max claims parity within two index points at roughly half the cost and tokens, in 40% less time (all vendor claims, above). The sources name this configuration only as a benchmark comparator, not as a routing or orchestration offering.

GitHub's sources name no third-party model-routing or orchestration products.

## Implications

The following is analysis by the KB maintainers, not a claim of GitHub's.

Fusion moves model selection from a user decision to a platform behaviour: the user picks an effort level and a policy-bounded pool, and the vendor's router makes per-prompt decisions the user cannot inspect. The effort level and the administrator model policies are therefore the real control surfaces — governance happens at the pool level, not the prompt level.

The economics of cascade and critique orchestration are likewise knowable only to the vendor: users are billed per model used for a process whose operating statistics are unpublished, and because Fusion High and Max can use more than one model, a task may consume more AI credits than it would with Fusion Standard.

The discarded-draft disclosure shifts a concrete review burden onto users: an orchestration pattern can leave file edits from an answer the system itself rejected, so reviewing working-tree changes before committing becomes part of using the feature safely.

The transferable takeaway is governance design rather than routing design: the real control surface is the effort level and the administrator model policies, and any organisation adopting Fusion should decide its default-effort policy and model pool before rollout, because per-prompt routing decisions are not inspectable by the user.

**Analyst note.** The governance takeaway generalizes beyond Fusion: any platform that moves model choice into a per-prompt router should still expose an auditable control surface, because cost and quality outcomes are only actionable if someone can inspect the routing decisions being made.

## Reproducible experiment

No executable artifact exists for Fusion: GitHub publishes no harness, task list, prompts, or per-task results, and Fusion is a hosted feature that cannot be downloaded or version-pinned. There is therefore nothing to reproduce from the sources. What follows is the third-party evaluation protocol that *would* test GitHub's claims, specified so the gap between claim and verification is concrete. **It has not been run.**

- **Task suite.** A fixed, published suite of coding-agent tasks spanning the capability categories the router claims to sense — reasoning, code generation, debugging, and tool use — with per-task success criteria frozen in advance.
- **Arms.** (a) Fusion at each user-selectable effort level (Standard, High, Max); (b) each pool model run singly, including the changelog's comparator configuration (Claude Code with the named Opus model); (c) Copilot auto model selection, as the ablation separating routing from orchestration.
- **Quality measurement.** Task-level success scored independently of the vendor. The quality index GitHub cites — the Artificial Analysis Coding Agent Index — should be re-measured by the evaluator rather than quoted: the claims to test are Fusion Max's score of 60 and its position within two points of the comparator, and re-using the vendor-cited number verifies nothing; sample sizes, per-task outcomes, and variance must be published — the changelog provides none.
- **Cost and latency accounting.** For every task and arm: API cost at published per-model rates, tokens (input, output, and cached reported separately), and wall-clock time; this directly tests the remaining claims — about half the average API cost per task, about half as many tokens, about 40% less time per task, all relative to the comparator arm.
- **Operating statistics.** Using the client's per-response model list, log execution-pattern frequencies, cascade acceptance and escalation rates, and critique revision rates per effort level — the statistics the vendor sources omit.

Two limits would apply even to a well-run version of this protocol. It measures a hosted system the vendor can change silently, so its results are a dated snapshot, not a property of a fixed artifact; and effort levels are trade-off policies that cannot be held constant across systems, so comparisons inherit the comparator's own settings as a confound.

## Evidence status

This page is grounded in the vendor sources inspected on 2026-11-10: the changelog post at https://github.blog/changelog/2026-10-28-route-and-orchestrate-models-with-github-copilot-fusion/, the Copilot Fusion documentation at https://docs.github.com/copilot/concepts/models/copilot-fusion, the auto model selection documentation, the enterprise model-availability documentation, and the Copilot billing documentation at https://docs.github.com/copilot/reference/copilot-billing/models-and-pricing. All performance figures are **vendor claims** from the changelog; the mechanism descriptions are **vendor-stated product behaviour** — a reasonable basis for describing what the feature is, not evidence for how well it works.

The inspected facts are the documented routing and orchestration model, the effort levels, the local-model preview, the administrator model policies and billing terms. The claimed facts are the Artificial Analysis Coding Agent Index score of 60, the two-point comparator margin, and the cost, token and time savings; the single third-party figure is quoted by the vendor without methodology and was not inspected here.

Nothing on this page was executed, installed, cloned or benchmarked by the KB maintainers; no workflow code was run, and nothing here reflects an independent evaluation of Fusion.

## Historical coverage

[Briefing 2026-11-01](../briefings/2026/11/2026-11-01.md)
