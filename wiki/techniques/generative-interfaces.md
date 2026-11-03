---
uid: cb0b9b68-5a1f-43f7-9604-dc30d0f53fab
depth: full
title: "Generative interfaces"
summary: "Agents propose declarative UI or actions; a trusted host validates against a pre-declared catalog or policy before anything renders or runs."
type: technique
created: 2026-11-02
updated: 2026-11-02
related: [a2ui-and-copilotkit, openbot]
sources:
  - url: https://a2ui.org/specification/v0.9.1-a2ui/
    retrieved: 2026-11-02
  - url: https://developers.googleblog.com/build-generative-ui-apps-with-a2ui-copilotkit-agents/
    retrieved: 2026-11-02
  - url: https://github.com/CopilotKit/openbot
    retrieved: 2026-11-02
---

# Generative interfaces

## What it is

This technique bucket collects the designs in the corpus where an agent's output crosses into a user-facing surface the agent does not own, and a host-controlled structure is interposed between what the agent proposes and what the user sees or what takes effect. The centre of the bucket is [A2UI and CopilotKit](../projects/a2ui-and-copilotkit.md): an agent describes a user interface as a stream of declarative JSON, composed only from a component catalog the client declared in advance, and the host renders it with its own native components. The agent never sends executable code. [OpenBot](../projects/openbot.md), a self-hosted agent coworker, is retained as a bounded second instance, not a co-equal pillar: its user-facing surface is a chat and shared-computer panel rather than generated UI, and its centre of gravity is the policy gateway treated on [[techniques/secure-agent-operations]]. What it shares with A2UI is the abstract move — agent output is a proposal, and a pre-declared, host-held structure disposes of it before it has effects — plus a common substrate, since an OpenBot Bot is any endpoint speaking AG-UI, the CopilotKit protocol that also carries A2UI payloads.

The honesty constraint on this page is set by the KB's own concept mining: in the [relation-discovery evaluation](../evaluations/relation-discovery-2026-11-02.md), the generative-interfaces theme dissolved. Two project summaries sharing an interface vocabulary never evidenced a shared mechanism, and A2UI's distinctive candidate concept, the catalog as trust boundary, remains a hold rather than a finding. This page is therefore a technique synthesis over two instances of host interposition — one strong, one bounded — not a claim that the corpus demonstrates a unified generative-interface mechanism.

## Mechanism variants

**Validate-then-render (A2UI).** An A2UI conversation is organised around surfaces: identified UI regions whose `surfaceId` and `catalogId` are fixed at creation. The server-to-client protocol has exactly four message types — `createSurface`, `updateComponents`, `updateDataModel`, `deleteSurface`. Components arrive as a flat adjacency list with an implicit tree, render progressively once the `root` component is defined, and skip invalid references. The catalog the agent may draw from is expressed as JSON Schema; the protocol's Basic Catalog defines 18 components and 14 client-side functions, and clients may define custom catalogs. Structure and data are kept separate: component properties bind to a client-side data model by JSON Pointer, input components write into that model immediately without network calls, and state reaches the server only when a component action fires or the surface opts into `sendDataModel`. Actions are named events or local function calls — never transmitted code. Since v0.9, generation is prompt-first: the catalog schema and examples are embedded in the model's prompt, the model emits free JSON, and a validator checks it afterwards, returning a standardised `VALIDATION_FAILED` error — surface, JSON Pointer path, one-sentence message — for self-correction. In the CopilotKit stack, AG-UI carries the payloads as typed events, generation runs in a dedicated sub-agent, and the app defines its catalog by pairing a Zod props schema with a natural-language description that goes into the agent's prompt; when correction retries are exhausted, the surface resolves to a short message so the conversation continues.

**Gate-then-act, with takeover (OpenBot, bounded instance).** Anything a Bot does to a computer, file, or MCP server returns to the server first: the gateway evaluates the current CEL policy over fields describing the attempted action — including `initiator.kind` / `initiator.id`, which travel inside a signed run assertion so a Bot cannot relabel its own run — writes the audit row, and only then calls the computer. There is no path that acts without the record existing first. The conversational surface adds the variant's distinctive element: when a Bot hits a login wall, a 2FA prompt, or a bot check, it files a help request and a person takes control in the same panel, solves the check, and hands back; while a person is driving, Bot actions are refused rather than queued.

The transferable pattern across both is a placement decision. Generating UI descriptions — or action proposals — is cheap and untrusted, so the engineering concentrates at the boundary the host controls: a catalog and validator in one case, a policy gateway and audit ordering in the other. In neither design does the host execute agent-supplied code as the price of a rich surface.

## Evidence and measured effects

**No effectiveness evidence exists for either instance, and that absence is the finding.** No primary source for A2UI or CopilotKit — the Google blog post, the v0.9.1 specification, the A2UI repository, or the CopilotKit documentation — contains a benchmark, a latency figure, a schema-validity or correction-recovery rate, an adoption metric, or a user study. OpenBot's documentation likewise contains no benchmarks, task-success or accuracy figures, latency numbers, evaluation results, or usage statistics, and no adversarial or correctness evaluation of its gateway; its only numbers are operational parameters, such as a 15-minute minimum routine interval and a 5,000-row cap on audit CSV export.

What can be checked is structural. For A2UI: the four message types and the Basic Catalog's 18 components and 14 functions are specification facts, cross-checked between the blog and the spec; the version state (v0.9.1 production, v1.0 a release candidate) is stated on a2ui.org. Every benefit claim is a vendor claim, labelled as such on the project page: that anything the agent invents outside the catalog "is caught before it reaches the screen," that the correction loop is "self-healing output" such that "nothing broken reaches the screen," and that the same agent response renders natively across React, Lit, Angular, SwiftUI, Jetpack Compose, and Flutter. For OpenBot, the published support for its governance claims is architectural description and an auditable mechanism — a design that can be inspected and, per the project page's proposed checks, exercised — not measurement of whether its policies catch real misuse or at what cost in refused legitimate work. No independent replication or third-party evaluation of any of these claims was found in, or cited by, the sources.

## Failure modes and bounds

The boundary these designs build is structural, not total, and both project pages mark its edges.

- **Content inside trusted components is uncontrolled.** A2UI's catalog prevents component and code injection, but within trusted components the agent still controls content: Text supports Markdown, Image and Video render from URLs, and buttons carry labels and actions. A manipulated agent can build a deceptive or phishing-shaped interface entirely from trusted components; the spec's only mitigation is attribution fields that orchestrators are told to validate. Content-level safety remains the host app's problem.
- **Prompt-first generation shifts the burden to validation.** The spec's own words: the approach "requires more complex post-generation validation, as the LLM is not strictly constrained by the schema." Whether models emit valid, semantically appropriate UI on the first pass, and what the correction loop costs in latency and tokens, is exactly the unmeasured property the design's value rests on.
- **The shared artifacts are socially coordinated.** A `catalogId` is just a string, not a resolvable resource; interoperability depends on client and server developers agreeing catalogs out of band, with no discovery or negotiation mechanism. Renderer coverage is also thinner than the portability claim: the A2UI README lists host frameworks as "currently: Web or Flutter," with several official renderers still on the roadmap.
- **Structure present, constraint absent.** OpenBot's shipped startup default policy is `deny: []` and `allow: ["true"]` — allow-all until an operator replaces it — so a fresh deployment's gateway records permitted actions rather than enforcing refusals. The same documentation candidly lists declarations that are not controls: a `knowledge.yaml` that is validated but read by nothing, and a group allowlist whose underlying field is never populated.
- **The gate covers only what routes through it.** OpenBot's gateway governs calls that return to the server; a Bot endpoint's internal loop is outside it by construction, and a process opening a raw socket bypasses the egress filter. Human takeover, the conversational variant's fallback, depends on a person being available to drive; otherwise the run pauses.

## Open questions

- What are A2UI's first-pass schema-validity rate, correction-loop recovery rate, and per-surface latency and token cost across models? The project page proposes a concrete protocol for measuring them; nobody has published the numbers.
- Does the catalog model attract renderer investment on surfaces controlled by other vendors, or does the ecosystem contest with iframe-based approaches (MCP-UI, MCP Apps) settle elsewhere? The portability claim is untestable as a market fact until then.
- For gated coworker surfaces: do audit-first policies catch real misuse in deployment, at what false-refusal cost, and how often does human takeover actually fire? A takeover rate high enough to matter would change the economics of the coworker shape itself.
- Is there any setting in which the two variants genuinely compose — generated UI as the surface through which a gated agent's proposals and takeover requests are presented — or is the shared AG-UI substrate the whole of the connection? The corpus contains no instance of the composition.

## Evidence status

This page is a synthesis over the KB's two deepened project pages, [A2UI and CopilotKit](../projects/a2ui-and-copilotkit.md) and [OpenBot](../projects/openbot.md), and the relation-discovery evaluation's disposition of this theme; it introduces no external sources and no facts beyond them. A2UI is kept as the technique's central instance. OpenBot is demoted to a bounded instance: it is an operations-and-governance design with a conversational surface, included here for the shared host-interposition move and the AG-UI substrate, not as a second generative-UI system. All benefit claims for both instances are vendor claims or architectural descriptions in their sources; no effectiveness result — benchmark, validity rate, user study, gateway evaluation — exists in the corpus for either, and none is claimed here. The theme's dissolution in concept mining stands: this page documents a pattern an engineer can choose, at the strength the two instances support, not a mechanism the corpus has evidenced across projects.
