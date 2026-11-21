---
uid: f9ad7395-9826-4c03-aac6-e99638289529
title: Delegated authority and revocation
summary: Explain authority scope, inheritance ceilings and revocation independently of task delegation or model instructions.
type: concept
created: '2026-11-16'
updated: '2026-11-16'
depth: full
sources:
- https://raw.githubusercontent.com/compozy/compozy/8cbf8a5a4dcb343f349e2b47635a461bea0c9b24/CHANGELOG.md
- https://raw.githubusercontent.com/strands-agents/box/d5278f29972f7bf2f688e3fa76511d3a29705f33/docs/design/policy.md
- https://raw.githubusercontent.com/CopilotKit/OpenBot/3083c34b0e9153b86c532112bdf0048202e91000/README.md
- https://raw.githubusercontent.com/thunderbird/thunderbolt/2f81a4d9897cc92839632137fc7d38fee75ba240/CHANGELOG.md
---

# Delegated authority and revocation

## What authority means here

Task delegation assigns work; authority determines which consequential operations may be performed. A useful design description identifies the grantor, subject, resource/action scope, lifetime, enforcement point and revocation behavior. These are analytical dimensions for comparison, not a claim that the implementations share a formal capability system.

An **inheritance ceiling** prevents a delegated child from acquiring more authority than its parent is permitted to confer. **Revocation** changes what is allowed from that point onward; it does not automatically undo earlier effects. A connector credential, a model's instruction and an externally enforced permission are different objects.

## Mechanisms and limits

[[projects/compozy]] documents narrowing default spawned tools to parent authority, retaining stricter workspace policies and canceling descendants under terminal delegated sessions ([changelog](https://raw.githubusercontent.com/compozy/compozy/8cbf8a5a4dcb343f349e2b47635a461bea0c9b24/CHANGELOG.md)). These release fixes describe intended enforcement and lifecycle behavior, not a proven absence of escalation.

[[projects/strands-box]] uses an external policy engine with recorded action history, deny defaults and forbid precedence ([policy design](https://raw.githubusercontent.com/strands-agents/box/d5278f29972f7bf2f688e3fa76511d3a29705f33/docs/design/policy.md)). Authorization can depend on previous events; it is not merely a static tool list.

[[projects/openbot]] puts target resolution, policy evaluation and audit recording before the action ([README](https://raw.githubusercontent.com/CopilotKit/OpenBot/3083c34b0e9153b86c532112bdf0048202e91000/README.md)). Its documented permissive default remains a boundary: having a gateway does not mean the installed policy is restrictive.

[[projects/thunderbolt]] documents reusable provider connections and authorization ([changelog](https://raw.githubusercontent.com/thunderbird/thunderbolt/2f81a4d9897cc92839632137fc7d38fee75ba240/CHANGELOG.md)). Credential reuse is a connector-lifecycle feature, not evidence that its authority model is equivalent to a child-tool ceiling or history-sensitive policy.

## Information flow is a separate constraint

An action may be individually permitted yet carry data from a source into an inappropriate destination. [[projects/sopguard]] examines agent-mediated cross-origin flows. That is related to, but not interchangeable with, permission to invoke the browser. [[concepts/structural-constraint-over-instruction]] and [[techniques/secure-agent-operations]] explain the enforcement boundary; [[concepts/agent-state-and-lifecycle]] explains cancellation and reconciliation.

## Proposed test and evidence status

In a disposable parent/child workflow, vary grant scope, revoke access during a pending operation, cancel the parent and restart the runtime. Attempt the same operation through each child, connector and replay path. Record allowed/denied effects, surviving credentials, queued work and effects committed before revocation. Test data-flow restrictions separately with a canary. No universal propagation or revocation guarantee follows from the cited documents, and no such experiment has been run here.

### Evidence integrity across delegated readers

Authority to invoke a retrieval tool does **not** establish that its returned information is trustworthy. [[projects/weakest-agent-multi-agent-break]] ([study](https://arxiv.org/abs/2611.17520)) isolates a delegated-reader vulnerability: strong orchestrators directly reading forged file-store records almost never made harmful revisions in over 1,000 author-reported trials, but delegating the same reading to weaker agents produced failures across distinct configurations (20/180, 44/180, 75/180 and 553/900). These are separate denominators, not a pooled failure rate. A separate simulated delivery experiment found that aggregators propagated corrupted worker output in 751/757 trials.

This evidence extends the authority model with an **information-integrity boundary**: a worker may be authorized to read, yet its assertions still require provenance and independent checks before consequential downstream action. It does not establish that all smaller models or all multi-agent teams are unsafe. [[projects/aligning-ai-teams]] studies responsibility for team-wide safety invariants, a different mechanism; a safety lead cannot substitute for checking forged evidence. Test direct and delegated retrieval under identical planted records and tool scopes, counting independently verified claims and downstream writes rather than prompt compliance.


## Evidence trust is not delegated with task authority

The delegated-reader result above concerns *information integrity* rather than permission inheritance. A second independent, older source, [Beyond Single-Model Injection: A Threat Model and Defense Architecture for Prompt Injection in Multi-Agent Systems](https://arxiv.org/abs/2609.22949) (September 2026), reports a six-agent testbed with indirect tool-output injection and inter-agent-message attack paths. Its authors report 43% success for indirect tool-output attempts and an overall reduction from 31.2% to 4.2% with combined defenses; these are author-reported measurements under their own test conditions, **not** replication of the Weakest Agent study or evidence that provenance alone solves the problem.

The two independent reports support the bounded architectural question: how does lower-trust material become a trusted instruction or asserted fact as it crosses an agent boundary? The Weakest Agent study tests a weaker delegated reader passing contaminated evidence upstream; the September threat-model study tests several inter-agent and tool-output injection routes and bundled defenses. Their denominators, attackers and success criteria differ. Do not pool their rates or equate task delegation with authority delegation.

A defensible boundary keeps source evidence separate from worker interpretation, preserves origin and retrieval context, treats subordinate summaries as untrusted claims, and independently verifies high-impact facts before consequential writes. These are proposed controls, not a demonstrated integrated defense. [[techniques/artifact-and-claim-provenance]] describes the evidence chain and [[concepts/verified-completion-vs-apparent-success]] bounds acceptance.

**Promotion decision:** Two independent sources now exist, but they do not isolate the same mechanism or demonstrate a common effective mitigation. Retain this bounded synthesis here rather than creating a broad new concept. A future concept requires a clear definition distinguishing evidence laundering from ordinary prompt injection, independently matched mechanism evidence and meaningful counterexamples.
