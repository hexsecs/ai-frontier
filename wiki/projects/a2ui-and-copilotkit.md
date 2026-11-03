---
uid: cba96f25-06f2-4a76-a029-4cc6c409d711
depth: deep
title: "A2UI and CopilotKit"
summary: "Google's A2UI protocol lets agents emit declarative UI from a trusted component catalog; CopilotKit carries it over AG-UI and renders it natively in apps."
type: project
created: 2026-10-30
updated: 2026-11-02
sources:
  - url: https://developers.googleblog.com/build-generative-ui-apps-with-a2ui-copilotkit-agents/
    retrieved: 2026-11-02
  - url: https://a2ui.org/specification/v0.9.1-a2ui/
    retrieved: 2026-11-02
  - url: https://github.com/a2ui-project/a2ui
    retrieved: 2026-11-02
  - url: https://docs.copilotkit.ai/generative-ui/a2ui
    retrieved: 2026-11-02
---

# A2UI and CopilotKit

## What it is

This page covers two separate artifacts with two different owners, and the distinction matters for everything that follows.

**A2UI** is an open protocol specification created by Google (Apache-2.0, with contributions from CopilotKit and the open-source community). It defines how an AI agent describes a user interface as a stream of declarative JSON messages, which the client then renders using its *own* native components. The agent never sends executable code; it can only compose components from a catalog the client has declared in advance. The spec's own framing of the problem is "how can AI agents safely send rich UIs across trust boundaries?" The current production version is v0.9.1; v1.0 exists only as a release candidate. (Even the name is not fully settled: the Google blog and the spec expand A2UI as "Agent-to-UI" / "Agent to UI," while the GitHub README expands it as "Agent-to-User Interface.")

**CopilotKit** is a separate, open-source agentic application framework. In the stack the Google blog post demonstrates, CopilotKit supplies three things A2UI itself does not: the **AG-UI** protocol, which carries A2UI payloads between the agent backend and the frontend as typed events; a runtime that brokers that connection and applies A2UI middleware to registered agents; and renderers that turn the message stream into native UI inside the app. AG-UI is a transport and interaction protocol, not a generative-UI specification — CopilotKit's own explainer is explicit on this point. A2UI is transport-agnostic and names other bindings (A2A, MCP, SSE+JSON-RPC, WebSockets, REST); the CopilotKit/AG-UI carriage is one integration, not part of the protocol.

## Mechanism

### The A2UI protocol

An A2UI conversation is organized around **surfaces**: identified UI regions (`surfaceId`), each created before components or data are sent to it, with its `surfaceId` and `catalogId` fixed at creation (reconfiguration means delete and recreate). The server-to-client protocol defines exactly four message types:

- `createSurface` — create a new surface and begin rendering it.
- `updateComponents` — add or update component definitions in a surface.
- `updateDataModel` — insert or replace data in a surface's data model.
- `deleteSurface` — remove a surface and its contents.

Components arrive as a flat adjacency list; the tree is implicit through ID references, one component must have the id `root`, and definitions may arrive in any order and reference not-yet-existing children. The client renders placeholders and begins once `root` is defined, so UIs render progressively as the stream arrives, and invalid references are skipped.

The set of things an agent may draw is a **catalog**, expressed as JSON Schema. The protocol's Basic Catalog defines 18 components — Text, Image, Icon, Video, AudioPlayer, Row, Column, List, Card, Tabs, Divider, Modal, Button, CheckBox, TextField, DateTimeInput, ChoicePicker, Slider — and 14 named client-side functions (validation and formatting helpers such as `required`, `regex`, `email`, `formatCurrency`, `openUrl`). Clients may define custom catalogs; a `catalogId` is just a string identifier, not a resolvable resource, so client and server developers must agree on shared catalogs out of band.

UI structure and application data are kept separate. Component properties are dynamic values: a literal, a JSON Pointer path into the surface's data model, or a function call. Templates instantiate a component per array item. Input components write user input into the *client-side* data model immediately and reactively, but keystrokes trigger no network calls; state reaches the server only when a component `action` fires (sending the values of the paths named in its context) or when the surface was created with `sendDataModel: true`. Actions are named events or local function calls — never transmitted code. Input components also carry declarative `checks`; a button whose checks fail is disabled automatically, so form validation runs on the client without a model call.

Since v0.9, generation is **prompt-first**: rather than constraining the model with structured output, the catalog schema and examples are embedded in the model's prompt and the model emits free JSON, which is then validated. On failure, the validator returns a standardized error — code `VALIDATION_FAILED`, the `surfaceId`, a JSON Pointer `path` to the failing field, and a one-sentence message — to the model for self-correction.

### The CopilotKit stack

On the client, the app defines its catalog with `createCatalog` from `@copilotkit/a2ui-renderer`: each definition pairs a Zod props schema with a natural-language `description` and a renderer mapping to the app's own component. Per the Google blog, "the `description` goes into the agent's prompt, so the model knows when to reach for `FlightCard` instead of a generic card. The Zod schema validates the props it sends back." The Basic Catalog can be merged in with `includeBasicCatalog: true`, and the catalog can also be created dynamically on the client and shipped to the server with the request. CopilotKit offers two flavors: a **dynamic schema**, where the model generates the A2UI schema against the registered catalog, and a **fixed schema**, where the developer authors the schema and the agent supplies only data.

Enabling A2UI in the CopilotKit runtime is a single option (`a2ui: {}` on `CopilotRuntime`), which automatically applies `A2UIMiddleware` to all registered agents. Generation runs in a **dedicated sub-agent**, which — in the blog's words — keeps "the catalog and protocol rules out of your main agent's context window" while the surface streams to the client. The spec's validate-and-correct loop surfaces here as a product feature: invalid generations are caught, the specific errors go back for a correction, and when retries are exhausted the surface resolves to a short message so the conversation continues. Rendering on the frontend is automatic; alternatively, the AG-UI event stream can be consumed directly and handed to any compliant renderer (@a2ui/react, Lit, Angular, Flutter).

The blog's worked example is a flight-booking flow — search, results, passenger details, confirmation — evolving on a single `surfaceId`: inputs bind to data paths such as `/booking/cabin`, a button's action names which paths to send back, and the agent re-emits against the same surface.

## Evidence

**There are no quantitative results to report.** No primary source for either artifact — the Google blog post, the v0.9.1 specification, the A2UI repository, or the CopilotKit documentation — contains a benchmark, a latency figure, a schema-validity or correction-recovery rate, an adoption metric, or a user study. Every benefit either vendor asserts is unquantified, and this page invents no numbers to fill the gap.

What *can* be checked is structural and bibliographic:

- The protocol defines **4 message types**, quoted verbatim in the spec — a specification fact.
- The **Basic Catalog contains 18 components** (and 14 functions): stated in the blog and independently countable in the spec's catalog table — a specification fact, cross-checked between two primary sources.
- **Version state:** v0.9.1 is the "Current" production release, v0.9 is "Stable," v0.8 is "Legacy," and v1.0 is a "Candidate" that renames `theme` to `surfaceProperties` and adds a client-to-server `actionResponse` RPC — per the version table on a2ui.org.
- **Repository metadata** (independently observable on the GitHub landing page, crawled 2026-11-03; point-in-time and will drift): repo created 2025-09-24; 16,946 stars; 1,362 forks; 1,735 commits; 13 releases; Apache-2.0. The README banner reads "Early stage public preview … Expect changes."
- SDK packages exist on PyPI (`a2ui-core`, `a2ui-agent-sdk`), npm (`@a2ui/web_core`, `@a2ui/lit`, `@a2ui/angular`, `@a2ui/react`, `@a2ui/markdown-it`), and pub.dev (`a2ui_core`, `a2ui_agent`), with several others explicitly listed as not yet published.

Against that, the headline benefits are **vendor claims** (Google for A2UI, CopilotKit for the stack), asserted without measurement:

- **Security:** "anything the agent invents outside that set is caught before it reaches the screen" and "no UI injection attacks" (vendor claim — Google).
- **Portability:** the same agent response rendering natively across React, Lit, Angular, SwiftUI, Jetpack Compose, and Flutter (vendor claim — Google).
- **Generation reliability:** the correction loop described as "self-healing output," such that "nothing broken reaches the screen" (vendor claim — Google, describing CopilotKit's implementation).
- **LLM-friendliness:** the flat streaming JSON structure is "designed for easy generation," letting models "build UIs incrementally without perfect JSON in one shot" (vendor claim — a2ui.org).

No independent replication or third-party evaluation of any of these claims was found in, or cited by, the primary sources.

## Limitations

Stated by the sources themselves:

- **Pre-1.0 and moving.** The spec page is a living document; v1.0's renames mean v0.9.1 implementations face a breaking-ish transition, and four protocol generations coexist across official documentation — CopilotKit's older docs still describe the v0.8 theme system.
- **Prompt-first trades constraint for validation burden.** The spec's own words: the approach "requires more complex post-generation validation, as the LLM is not strictly constrained by the schema," plus robust error handling and correction before rendering.
- **Renderer coverage is thinner than the portability claim.** The repo README lists host frameworks as "currently: Web or Flutter," with official React, Jetpack Compose, and SwiftUI support on the roadmap — even though an `@a2ui/react` package is already published and the blog lists SwiftUI and Jetpack Compose as render targets.
- **A declarative ceiling.** CopilotKit's own taxonomy lists "limited full customization" as the declarative pillar's weakness: "Custom UI patterns may not be possible. Visual differences can still occur if specs are interpreted differently."
- **Catalog agreement is out-of-band.** Interoperability depends on client and server developers coordinating catalog IDs socially; the protocol provides no discovery or negotiation mechanism.

Analyst-assessed (following from the design; not stated by the sources):

- **The core loop has no reliability evidence.** The value proposition rests on models emitting schema-valid, semantically appropriate UI and on the correction loop converging. No source reports first-pass validity, correction success, retry counts, or the latency and token cost of the loop — so "self-healing" is currently a mechanism, not a measured property.
- **The security boundary is structural, not total.** The catalog prevents component and code injection, but within trusted components the agent still controls content: Text supports Markdown, Image and Video render from URLs, and buttons carry labels and actions. A manipulated agent can build a deceptive or phishing-shaped interface entirely from trusted components; the spec's only mitigation is attribution fields (`iconUrl`, `agentDisplayName`) that orchestrators are told to validate. Content-level safety remains the host app's problem.
- **Trust shifts rather than vanishes.** Safety now depends on catalog design and renderer correctness — the spec warns validators silently skip tree-integrity checks if a catalog types component IDs as raw strings — and the README explicitly blesses "smart wrapper" components, including iframe containers for legacy content, whose sandboxing is left to the developer.
- **State convergence is optimistic.** Two-way binding is client-local; the server treats the data model received at action time as current. Multi-surface or multi-agent write conflicts are not addressed in the sources read.
- **Ecosystem risk.** A2UI's backing is Google plus the AG-UI/CopilotKit ecosystem. Whether the catalog-based model attracts renderer investment on surfaces controlled by other vendors is unproven, and several first-party renderers remain unpublished.

## Competing approaches

The sources position A2UI within a generative-UI spectrum:

- **Controlled generation** — the developer builds each component ahead of time and the agent only chooses which to render with what data (including decision-model variants such as Typesafe's Jev, named in the blog). Brand-safe, but no deep customization. CopilotKit's own controlled primitives (components registered as frontend tools, tool-call and state rendering) sit here.
- **Open-JSON-UI (OpenAI)** — a declarative JSON UI schema, in the same pillar as A2UI in CopilotKit's taxonomy.
- **Raw code generation** — the agent returns HTML/JavaScript/Dart rendered in a sandboxed iframe. Maximally expressive, but executes model-written code and drifts from the host design system.
- **MCP-UI (Microsoft and Shopify) and MCP Apps** — iframe-based generative UI extending MCP: third-party servers ship their own UI, rendered sandboxed with no frontend renderer required. CopilotKit lists their weaknesses as "hard to style, secure, or port" and web-first.
- **Text-only responses** — the baseline the blog post opens against.

## Implications

A2UI's real proposal is a placement of the trust boundary: the component catalog becomes a security and policy artifact — the enumerated set of things an agent is allowed to make a user see and touch — while rendering authority stays with the host app. That makes catalog design and renderer correctness the new review surface for agent UI, in place of reviewing generated code. For adopters, the practical consequences are threefold. First, the stack is a pre-1.0 bet: budget for protocol churn, including the v1.0 renames. Second, the property that decides whether the approach works in production — how often models produce valid, appropriate UI on the first pass, and what the correction loop costs — is exactly the property nobody has published numbers for, so any serious adoption has to instrument it locally. Third, the contest with iframe-based approaches (MCP Apps) is partly an ecosystem contest over whose surfaces get renderer investment, and it is unresolved.

## Reproducible experiment

The missing numbers are measurable with published artifacts, and the following protocol would produce them. (Proposed here; not performed for this page.)

1. Stand up the A2UI Restaurant Finder quickstart (Gemini ADK agent, Lit renderer) or the CopilotKit Dojo dynamic-schema demo, unmodified.
2. Fix a graded set of ~50 UI-generation requests, from single-card displays to multi-step forms with validation. Run each against at least two models, logging: first-pass validity (fraction of generations passing catalog validation with no `VALIDATION_FAILED`), correction-loop recovery rate within the configured retries, retries consumed, and end-to-end latency and token cost per surface.
3. Replay identical recorded message streams into two renderers (e.g. `@a2ui/react` and `@a2ui/lit`) and diff the rendered component trees, testing the portability claim at the level the spec actually defines.
4. Probe the content boundary: instruct the agent (directly, then via injected tool output) to produce deceptive text, misleading button labels, and a credential-shaped form using only Basic Catalog components, and record what reaches the screen.

Steps 2–4 measure, respectively, the reliability claim, the portability claim, and the security claim — each currently vendor-asserted only.

## Evidence status

Read in full on 2026-11-02 for this page: the Google Developers Blog announcement; the A2UI Protocol v0.9.1 specification; the a2ui.org homepage and version table; the `a2ui-project/a2ui` repository landing page and README; CopilotKit's A2UI documentation, generative-UI concepts overview, generative-UI taxonomy page, and dynamic-schema documentation. Not inspected: the v1.0 candidate and v0.9/v0.8 spec texts (only version-table summaries), the raw JSON schema files, renderer or SDK source code, and the repository's `conformance/` and `eval/` directories. AG-UI's own specification was not read in full; AG-UI details rest on the A2UI spec's binding section and CopilotKit's documentation. No code was executed and no demo was run. All quantitative content on this page is structural (spec counts, version states, repository metadata); every benefit claim is a vendor claim and is labelled as such where it appears.

## Historical coverage

[Briefing 2026-10-30](../briefings/2026/10/2026-10-30.md)
