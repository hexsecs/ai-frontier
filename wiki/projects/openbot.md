---
uid: c13ec812-fad9-4509-b33a-87634a095daf
depth: full
title: "OpenBot"
summary: "CopilotKit's self-hosted agent coworker: an audit-first policy gateway records every action before it runs, plus human takeover; no measurements published."
type: project
created: 2026-11-02
updated: 2026-11-02
related: [scoped-assurance, structural-constraint-over-instruction, validation-tier-gap]
sources:
  - url: https://github.com/CopilotKit/openbot
    retrieved: 2026-11-02
  - url: https://github.com/CopilotKit/openbot/blob/main/docs/architecture.md
    retrieved: 2026-11-02
---

# OpenBot

## What it is

OpenBot is CopilotKit's open-source (MIT) framework for self-hosted AI coworkers: agents in the shape of a hosted assistant, working through a web app, Slack, Teams, or text message, each with its own browser, logins, files, and granted tools. A Bot is any endpoint speaking AG-UI, CopilotKit's open agent-to-user protocol, so agents built on LangGraph, Mastra, CrewAI, or by hand all arrive the same way, and the governance below rides the protocol rather than the framework.

The project bounds its own claims, and this page keeps the bounds: OpenBot calls itself "a template, not a product" — meant to be cloned and made one's own, with no hosted version — and carries a beta badge: "under active development… Expect rough edges and bugs."

"Self-hosted" needs its qualification. The app, the per-person computers, and the product database are the operator's, but the server refuses to start without a CopilotKit Intelligence project and licence: durable threads and memory live in Intelligence, a separate component that is licensed, managed by default, and self-hostable (a free plan exists). Inference likewise goes to whichever external model API the administrator keys in — no model ships in the box. By default, then, the self-hosted deployment has an external core.

## Mechanism

The load-bearing mechanism is a single policy gateway on the server. Anything a Bot does to a computer, a file, an MCP server, or a component returns to the server first: the gateway resolves the target from a server-held snapshot, evaluates the current action policy, **writes the audit row, and only then calls the computer** — in the README's words, "There is no path that acts without the record existing first." A forwarded action that fails earns a second audit row. Shell commands pass through the same gate, so a rule can refuse a shell outright or refuse particular commands, and the command is on the record either way.

Policy is expressed in CEL, with case-insensitive `contains()` and `matches()` helpers, over fields describing the attempted action: `tool.name`, `intent`, `bot.id`, `actor.id`, `page.url` / `page.host`, `element.ref` / `element.role` / `element.name` / `element.type`, `key`, `command`, `file.path` / `file.name` / `file.extension`, and `mcp.server` / `mcp.tool` / `mcp.effect`. Most distinctive is `initiator.kind` / `initiator.id` — what started the run (person, deployment, routine, responsibility, memory, handoff) — so a rule can refuse a scheduled routine what it would allow a person; the value travels inside the signed run assertion, so a Bot cannot relabel its own run. Evaluation is deny-before-allow, and the engine fails closed: a missing or empty policy permits nothing, a broken deny rule denies, and a broken allow rule does not permit.

One fact about the default belongs here, not just in Limitations: the shipped startup default policy is `deny: []` and `allow: ["true"]` — allow-all — unless `AGENT_COMPUTER_POLICY` or a saved administrator policy replaces it. The fail-closed semantics above describe the engine; a fresh deployment runs permissive until an operator writes policy.

Isolation is per person: a supervisor service gives each person their own container, holding a folder and a browser profile for each of their Bots — its own Chromium, logins, and workspace. Each computer's browser and shell egress passes through a filter proxy applying the Bot's network policy (`allow_all`, `defaults_plus_allowlist`, `allowlist_only`, `deny_all`); the server pushes the policy before the computer acts and whenever it wakes, and until a policy arrives nothing may leave. Cloud metadata addresses are refused in every mode.

Human takeover is the designed fallback for the moments automation should stop. A Bot that hits a login wall, a 2FA prompt, or a bot check ("Verify you are human", a CAPTCHA) files a help request, recorded with the page it was made on; a person takes control in the same panel, solves the check themselves, and hands back — OpenBot never solves a bot check on anyone's behalf. The events are audited as `computer.help_requested`, `computer.control_taken`, and `computer.control_released`. While a person is driving, Bot actions are refused rather than queued; a run with no browser attached pauses instead, waiting on the handover.

State is split. The deployment's own PostgreSQL (with pgvector) holds product data: policy, audit, credentials, grants, channels, component metadata. Threads and memory live in CopilotKit Intelligence, which holds the content and does the recall; OpenBot keeps what Intelligence has no field for — provenance, review state, which Bot formed a memory, which source imported it — and filters everything Intelligence returns before a Bot sees it: calls ask for user scope only and project-scoped results are dropped, so one person's Bot never sees another person's memory.

## Evidence

**There are no performance measurements to report, and that absence is the finding.** The README and architecture documentation contain no benchmarks, no task-success or accuracy figures, no latency numbers, no evaluation results, and no usage statistics for OpenBot itself; no adversarial or correctness evaluation of the gateway appears in the sources either. The published support for the governance claims is architectural description and an auditable mechanism, not measurement.

The only numbers present are operational parameters, not results: routines carry a 15-minute minimum interval and a cap of 20 enabled routines, and a routine is disabled after ten consecutive failures; audit CSV export is capped at 5,000 rows and says so via an `X-Audit-Export-Truncated` header. The one quantitative-sounding claim — that a model picks the right tool "reliably out of about ten, and unreliably out of thirty" — is an author assertion with no cited study. Repository activity as of 2026-11-03 (9,926 stars, 1,218 forks, 632 commits, 19 releases since 2026-08-17) is an adoption signal, not product evidence.

## Limitations

The load-bearing caveat is the shipped default named in Mechanism: the startup policy is `deny: []` / `allow: ["true"]`, so out of the box the gateway permits everything. The fail-closed property protects a deployment only once an operator replaces the default with real policy — the safety property is available, not out-of-the-box, and in a default deployment the audit trail records permitted actions, not enforced refusals.

The architecture document is unusually candid about its own non-controls, and this page credits that candour by repeating them as limitations rather than presenting them as discoveries:

- `knowledge.yaml` accepts Google Drive and OneDrive declarations and is validated, but nothing reads it yet.
- `channels.allowed_groups` is a declaration, not a running control: `users.groups` is never populated by any sign-in path, so a group-based rule has nothing to evaluate.
- The egress filter governs traffic that honours the proxy variables; a process that opens a raw socket bypasses it — the docs assign that layer to Kubernetes NetworkPolicy.
- The computer also exposes lower-level token-protected endpoints beside the gateway; the README warns operators to keep them private and not use them to bypass the gateway.

One further limit is evident on inspection: the gateway governs the tool calls that route back through the server, but a Bot served from its own AG-UI endpoint runs its own loop, and that endpoint's internal behaviour is outside the gateway by construction.

## Competing approaches

The sources offer positioning, not comparisons; nothing below is measured against OpenBot anywhere in them. Against hosted assistants (the README names ChatGPT, Claude, and Grok): the same shape, but "it runs on your infrastructure and you can change anything about it." Against ungoverned tool access: the gateway is "the difference between an agent that can use your tools and an agent you can let near them." Against framework lock-in: because a Bot is any AG-UI endpoint, "the governance rides the protocol rather than the framework." All three are vendor claims, labelled as such.

## Implications

OpenBot makes the audit record a precondition of action rather than a by-product, which is what lets the record serve as an account: a refusal names its rule, and an action with no record is an action that did not happen through the gateway — within the limits above, notably the default policy and the calls that never route through the server. The transferable ideas are the audit-first ordering itself and the initiator field: policy that can distinguish a person asking from a routine firing makes standing automation governable by the same rules as interactive use, a distinction most tool-gating designs cannot express. What none of this establishes is effectiveness — whether the gateway's policies catch real misuse, and at what cost in refused legitimate work, is unmeasured (see [[techniques/secure-agent-operations]] and [[techniques/verification-and-evidence]]).

## Reproducible experiment

No experiment was run for this page; the checks below are ones a reader with a deployment can perform, and the first two are the README's own suggested trials. (1) Audit-first invariant: install from the quick start, ask a Bot to open a page and fill a form (the README suggests httpbin.org), then inspect `/admin/audit` and confirm a decision row exists for each action, written before it took effect. (2) Deny path: add a deny rule at `/admin/boundaries` matching that action and retry; the action should be refused, with the refusal naming the rule. (3) Default check: on a fresh deployment, confirm the effective policy is the shipped `allow: ["true"]` default, then set a malformed `AGENT_COMPUTER_POLICY` and confirm the server refuses to start rather than starting open. Together these test the page's three load-bearing claims — record-before-act, fail-closed on broken policy, allow-all by default — against the running system rather than the documentation.

## Evidence status

This page documents a mechanism and makes no effectiveness claim anywhere. Its claims rest on the project's own published documentation — the repository README and `docs/architecture.md`, read in full for this revision (2026-11-03) — cross-checked against repository facts visible on the repo page (licence, creation date, tags, activity counts). Vendor framing is labelled as vendor claim where it appears, and observations drawn from inspection are labelled as such. No OpenBot code was executed, installed, or run for this page, and no benchmark was reproduced — none exists in the sources to reproduce. This revision is the re-verification pass the previous version of this page called for: the mechanism is as described; the measurements do not exist.

## Historical coverage

[Briefing 2026-11-02](../briefings/2026/11/2026-11-02.md)
