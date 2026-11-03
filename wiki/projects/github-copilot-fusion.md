---
uid: e9c7e0ee-bc7a-428f-baf9-eed1f17ba02f
depth: brief
title: "GitHub Copilot Fusion"
summary: "GitHub Copilot Fusion routes each prompt to models and a single, cascade, or critique pattern by capability signals, system health, and effort level."
type: project
created: 2026-11-01
updated: 2026-11-02
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

Per GitHub, Fusion is available on all Copilot plans in Visual Studio Code, the GitHub Copilot app, the Copilot CLI, and JetBrains IDEs. One sub-feature is explicitly not generally available: routing to locally installed models (MAI Code 1.1 Flash or Qwen3.8 Flash Next) is in public preview, Standard-effort only, and requires experimental features.

The mechanism below is documented in reasonable detail by the vendor; the performance evidence is not independently verified, and every quantitative figure is labelled accordingly.

## Mechanism

Routing is decided **per prompt**, not per session: different prompts in the same conversation can use different models and different execution patterns. For each request, GitHub's documentation says Fusion evaluates the task using capability signals — for reasoning, code generation, debugging, and tool use — together with real-time system health and availability, and selects an execution pattern, a level of reasoning effort, and the models that run it. The stated objective is "the most efficient execution pattern that meets the quality bar for your chosen effort level." The selection logic inherited from auto model selection is described as two cooperating systems, one tracking system health and availability, the other evaluating task complexity. Beyond that, the router's internals are unspecified: no signal definitions, no thresholds, no description of how the selection model works. GitHub states that pattern selection is "a lightweight step that adds minimal latency" — a vendor claim, unquantified in the documentation.

Fusion uses three execution patterns:

- **Single.** One model solves the task directly.
- **Cascade.** An efficient model drafts a response; a quality check (a "judge," in the documentation's terminology) inspects the draft and either accepts it or escalates to a stronger model. Per the changelog's diagram description, escalation goes to a "repair model" that produces a "fresh-start answer" — the draft is discarded, not patched.
- **Critique.** One model drafts a response, another model or models review it, and the original model revises. GitHub's own sources disagree on the critic count: the changelog describes a single reviewing model, while the documentation describes multiple models critiquing in parallel with feedback aggregated. The sources do not reconcile this, so the critic count is treated here as unresolved.

The user's main control is the **effort level**, which sets the quality/cost/latency trade-off the router optimises for. Fusion Standard "balances cost, quality, and latency" and, per the documentation, selects one model for each task. Fusion High is balanced orchestration with moderate token savings; Fusion Max prioritises frontier capability while still considering token efficiency. A fourth level, Fusion Fast, is not user-selectable; per the documentation it is used only where fast models are required, in Visual Studio Code inline chat. There is no user-facing routing configuration — no rules and no per-task model pinning inside Fusion.

Fusion keeps the main conversation on the same model whenever possible, so it keeps benefiting from cached tokens; assisting models, such as a reviewer, receive only the context they need. Routing occurs along natural cache boundaries and large changes in conversation complexity to avoid cache-related costs. Fusion has no context window of its own — each step runs within the limits of the model running it — and it works separately from subagents and does not start them.

The model pool is administrator-controlled and not fixed. Enterprise and organization administrators decide which models Fusion can pick from through model policies; they can disable a model for Fusion without disabling it for everyone, and can set Fusion, at any effort level, as the default under Enterprise managed settings. Models are excluded when not in the user's plan or excluded by administrator, data-residency/FedRAMP, or evaluation-model policies; if no Fusion model is available to a user, Fusion does not appear in their picker. GitHub states that the pool changes as new models become available and as GitHub evaluates which models perform best.

Billing is per model used, at each model's standard rate, with no separate Fusion charge; High and Max can consume more AI credits than Standard because they may use more than one model. GitHub states that paid-plan users receive a 30% discount on model costs when using Fusion through November 30, 2026.

## Evidence

Every performance figure for Fusion comes from GitHub's launch changelog. None has independent verification, and each is labelled a vendor claim here.

- **Vendor claim:** in the Artificial Analysis Coding Agent Index, Copilot Fusion Max scored 60. This is GitHub citing a third-party index whose report — methodology, task set, sample size, variance — is not given in the changelog and was not inspected for this page.
- **Vendor claim:** that score was "within two points of Claude Code with Opus 5.5 Max" on the same index (the comparator's name as printed in the post; its exact score is not stated).
- **Vendor claim:** Fusion Max delivered that result "at about half the average API cost per task" relative to that comparator, "using about half as many tokens," and took "about 40% less time per task."
- **Vendor claim, unquantified:** pattern selection adds "minimal latency," and performance has improved since Project HydraFusion launched.

The changelog also quotes a customer testimonial — Hari Pokhrel, Principal Software Engineer at AT&T, stating that Fusion Standard "has improved token efficiency across AT&T by automatically selecting the right model for the task." This is a vendor-published testimonial: anecdotal, unquantified, and not independently verified.

That is the entire quantitative record in the sources.

## Limitations

The limitations below are analyst-assessed from the absence of material in the vendor sources, except where a vendor disclosure is quoted.

- **No independent evaluation.** Every performance number traces to GitHub's own announcement. The single external anchor — the Artificial Analysis index score — is quoted by the vendor without methodology and was not inspected here.
- **No reproducible benchmark.** No task list, harness, prompts, or per-task results are published, so the cost, token, and time claims cannot be reproduced or audited from the sources.
- **No pattern-level data.** The mechanism is documented, but its operating statistics — pattern frequencies, cascade acceptance and escalation rates, critique revision rates — are unmeasured in public.
- **No failure-mode data.** Nothing is published on judge or critic error rates, bad escalations, or quality regressions relative to picking a single frontier model manually.
- **Opaque, moving target.** The router's signals and thresholds are undisclosed, and GitHub states that "the execution patterns and model pool used may change over time." Any measurement of Fusion is a snapshot of a system the vendor can silently alter.
- **Unresolved internal inconsistency.** The changelog and the documentation describe the Critique pattern with different critic counts (one reviewer versus multiple parallel critics); the discrepancy is unresolved in the sources.
- **A disclosed operational hazard.** GitHub's documentation warns: "If Copilot Fusion discards a draft, changes that the draft already made in your workspace, such as file edits, aren't undone automatically. Review changes before you commit them." In the Cascade pattern, a discarded draft can therefore leave file edits behind even though its answer was rejected.
- **No baseline comparisons.** Fusion is never quantified against the obvious alternatives: a human picking models, or Fusion's own predecessor, auto model selection alone. The AT&T testimonial is the only evidence offered on the manual-selection comparison, and it is anecdotal.

## Competing approaches

GitHub's sources name no third-party model-routing or orchestration products. Project HydraFusion and Copilot auto model selection are Fusion's own predecessors — its two ingredient systems — which makes them lineage, not competitors. Claude Code with Opus 5.5 Max appears only as a benchmark comparator in the index claim; the sources do not present it as a routing or orchestration offering. (Analyst context: third-party LLM routers and gateways exist as a product category, but none is named or evaluated in Fusion's primary sources, so none is characterised here.)

## Implications

Fusion moves model selection from a user decision to a platform behaviour: the user picks an effort level and a policy-bounded pool, and the vendor's router makes per-prompt decisions the user cannot inspect. The effort level and the administrator model policies are therefore the real control surfaces — governance happens at the pool level, not the prompt level. The economics of cascade and critique orchestration (how often escalation fires, and what it costs when it does) are likewise knowable only to the vendor for now: users are billed per model used for a process whose operating statistics are unpublished. Finally, the discarded-draft disclosure shifts a concrete review burden onto users: an orchestration pattern can leave file edits from an answer the system itself rejected, so reviewing working-tree changes before committing becomes part of using the feature safely.

## Evidence status

Vendor announcement only. The entire evidence base for this page is GitHub's changelog post and GitHub's product documentation — the vendor describing its own generally available product. There is no paper or technical report, no published benchmark with inspectable methodology, and no independent evaluation or replication in the sources. The one third-party figure (the Artificial Analysis index score of 60) is quoted by the vendor without methodology, and the one customer data point (AT&T) is a vendor-published testimonial. Mechanism descriptions above are vendor-stated product behaviour — a reasonable basis for describing what the feature is, not evidence for how well it works. There is nothing public to reproduce — no artifact, harness, or dataset accompanies the claims — so this page carries no reproducible-experiment section, and its depth is `brief` because the source base cannot support more.

## Historical coverage

[Briefing 2026-11-01](../briefings/2026/11/2026-11-01.md)
