---
uid: b6a90406-a8d1-4d13-9a40-000000000016
title: "ToolGuardian"
summary: "Declarative security framework that vets MCP-style tools before admission and authorizes each invocation in task context."
type: project
created: 2026-11-09
updated: 2026-11-10
depth: deep
related: [structural-constraint-over-instruction, secure-agent-operations, verified-completion-vs-apparent-success]
sources:
  - https://arxiv.org/abs/2607.21835
  - https://arxiv.org/html/2607.21835v1
---

# ToolGuardian

## What it is

ToolGuardian is a policy-driven security framework for agent–tool interactions, reported in the arXiv preprint "ToolGuardian: Declarative Security for AI Agent-Tool Interactions" (arXiv:2607.21835, submitted 23 July 2026, cs.CR; preprint, no peer-reviewed venue claimed; arXiv perpetual non-exclusive licence). The paper lists two authors: Arun Ravindran (Department of Electrical and Computer Engineering, University of North Carolina at Charlotte) and Saurabh Deochake (SentinelOne, Mountain View, CA).

The threat it names is that a third-party tool exposed to an agent may look benign at the interface level while embedding unsafe behaviour in its implementation. The authors cite MalTool for the observation that malicious MCP-style tools can preserve benign-looking interfaces while performing confidentiality, integrity and availability attacks. The framework's two claims of novelty are, in the authors' words, "to the best of our knowledge", the first application of Answer Set Programming to agent–tool security across both pre-admission vetting and task-aware runtime authorization, and the separation of *characterization* (evidence gathering about a tool) from *enforcement* (the decision), so that the same evidence can be judged by different policy mechanisms.

Enforcement happens at two stages. **Vetting** asks whether a tool should be admitted at all, independent of any task. **Runtime authorization** asks whether a specific invocation is permitted in the current task context. The paper's justification for the split is that the same capability can be benign in one task and unsafe in another — network access is fine for a weather query and unsafe after sensitive local data has been read — and that individually plausible actions can become unsafe when composed.

## Mechanism

The architecture has four stages: tool characterization, fact generation, policy evaluation and enforcement.

**Progressive evidence (four additive levels).** *L0, description-based*: declared functionality from tool descriptions, package metadata, READMEs and API specifications. This evidence is supplied by the tool provider and is therefore treated as untrusted — it can guide policy interpretation but cannot establish conformance. *L1, system-call characterization*: observed OS interactions during execution, exposing coarse capabilities such as file reads and writes, network access and process execution, but without application-level semantics (a connection may be normal API access or covert exfiltration). *L2, mock execution and observed effects*: the tool is run in a controlled environment with representative inputs and mock external dependencies, recording outbound requests, accessed data categories, command invocations and local or remote state changes; coverage remains limited to the exercised branches. *L3, static source analysis*: AST analysis of the implementation to expose latent code paths, conditional branches, embedded endpoints and dangerous API use; it may over-approximate by flagging unreachable code, and it is unavailable for opaque binaries. The evaluation uses cumulative tiers P₀ = L₀, P₁ = P₀ ∪ L₁, P₂ = P₁ ∪ L₂, P₃ = P₂ ∪ L₃.

**Effect conformance.** L0 declarations are contrasted with L2 observed effects to produce declared-versus-observed mismatches — undeclared network communication, unexpected sensitive-data access, silent state mutation, behaviour inconsistent with the advertised task. These are emitted as *facts*, not resolved inside the characterization pipeline, so the policy layer decides whether a mismatch causes rejection, restriction, a warning, or a runtime block.

**Fact vocabulary.** All evidence is normalized into a common fact form so that ASP, heuristic and LLM realizations see comparable inputs: `capability(T, network_access)`, `data_access(T, env_vars)`, `observed_http_post(T, Endpoint)`, `modifies_remote_state(T, github_issue)`, `effect_mismatch(T, undeclared_network_access)`. The same vocabulary serves both stages: at vetting it summarizes a tool's security-relevant behaviour; at runtime it is combined with task-specific facts such as whether the task permits network access, sensitive-data handling or state modification.

**Policy.** The framework is guided by least privilege, zero trust for unverified tools, capability-oriented access control and information-flow restrictions between sensitive-data access and external communication. The vetting policy supports four outcomes — deny admission, admit with operational restriction, admit with cautionary warning, unrestricted admission — with hard rejection rules for covert network communication, unauthorized code execution, destructive filesystem activity and suspicious capability combinations. The runtime policy evaluates capability authorization, effect authorization, declared-versus-observed behaviour and multi-tool interaction risk, and produces allow/block with structured explanation tags.

**Three realizations of one policy intent.** The **ASP** realization encodes deny conditions, exceptions, effect-conformance checks and compositional constraints as explicit rules over the facts, solved with the Clingo solver through its Python interface; solutions are stable models (answer sets), so the developer specifies conditions and the solver derives conclusions. The **heuristic** realization is imperative Python: deterministic risk scores from capabilities, provenance and suspicious indicators, with runtime authorization checking observed capabilities and effects against the task profile, and all interactions between capabilities, effects, task context and multi-tool workflows hand-encoded as thresholds and conditionals. The **LLM** realization is a prompt-based interpreter over the same facts, task context and output contract, run with the open-source reasoning model `openai/gpt-oss-120b` accessed through OpenRouter at temperature zero. All three produce the same output schema — decision outcome, explanation tags, optional restriction annotations.

**Threat model.** The adversary controls the implementation of one or more tools available to the agent, may trigger hidden behaviour by particular inputs, execution contexts, environment variables or multi-step workflows, and may supply incomplete or misleading descriptions. The framework assumes the adversary does *not* compromise the kernel, hypervisor, hardware, model weights, serving stack or the enforcement components, and that policy evaluation and runtime mediation execute correctly. Out of scope: side-channel and microarchitectural attacks, prompt injection that does not result in unsafe external tool behaviour, and any behaviour unobservable under the available characterization or runtime monitoring — which the paper says motivates the layered characterization strategy in the first place.

## Evidence

All numbers in this section are **author-reported** from the single preprint; none has been independently replicated.

**Setup.** 16 MCP-style tools — 8 benign and 8 malicious variants derived from real open-source MCP implementations that keep the original external functionality and user-facing descriptions. The malicious variants cover covert exfiltration to a remote endpoint (db-mcp family), unauthorized remote project/item deletion, unauthorized poisoning of remote project fields, abuse of stored credentials for unauthorized API requests, covert outbound beacons during otherwise legitimate command execution, local file read plus exfiltration, document read plus exfiltration over the network, and local file search/read plus remote exfiltration. The runtime benchmark has 20 curated scenarios: 12 atomic single-invocation cases and 8 composite multi-step workflows (the composites cover sensitive-data access then network egress, credential-bearing context then network use, destructive change then external propagation, and read-then-remote-mutation). The vetting evaluation produces 64 decisions per realization (16 tools × P₀–P₃). Ground-truth labels are benchmark-defined reference outcomes. The positive class is deny.

**Vetting, deny-class F1 with accuracy in parentheses (Table III).**

| Realization | P₀ (descriptions) | P₁ (+syscalls) | P₂ (+observed effects) | P₃ (+source analysis) |
|---|---|---|---|---|
| ASP | 0.56 (50%) | 0.77 (81%) | **0.86 (88%)** | 0.82 (81%) |
| Heuristic | 0.56 (50%) | 0.77 (81%) | **0.86 (88%)** | 0.76 (69%) |
| LLM | null (50%) | 0.40 (63%) | **0.86 (88%)** | 0.82 (81%) |

At P₀ the LLM realization never outputs hard reject — it issues warning on five of the eight malicious tools — so deny-precision and F1 are undefined; the paper uses this to argue that description-level facts are insufficient for reliable LLM deny decisions while the rule-based realizations can still apply explicit conservative rules. At P₃ the ASP and LLM realize identical confusion counts (TP 7, FP 2, FN 1, TN 6), while the heuristic achieves perfect malicious recall (TP 8, FN 0) at the cost of five benign false rejects (FP 5, TN 3).

**Non-monotonicity of evidence.** Characterization depth improves vetting from P₀ to P₂ but not beyond: ASP F1 rises 0.56 → 0.77 → 0.86 and then falls to 0.82 at P₃, because static analysis exposes powerful but legitimate capabilities in benign tools. The representative failure is Tool_011, a benign terminal controller with external process execution, code execution and screen capture, which ASP and the LLM hard-reject at P₃.

**Partial interventions (Tables V–VII).** On the eight malicious tools, ASP hard-rejects 7 at P₃ with 1 partial (restricted admission), the heuristic hard-rejects all 8, and the LLM matches ASP. On the eight benign tools, ASP at P₀ produces 3 restricted_admit and 5 hard rejects; at P₁ and P₂ all 8 are restricted with no hard reject; at P₃ it is 6 restricted and 2 hard rejects, with no outright admission. Under the binary metric the restricted admissions count as true negatives, so the binary F1 hides the operational friction; the paper makes this point explicitly and argues for reporting restricted_admit separately.

**Runtime authorization (Table IX), all at P₃.**

| Realization | Overall | Atomic | Composite |
|---|---|---|---|
| ASP | 20/20 | 12/12 | 8/8 |
| Heuristic | 20/20 | 12/12 | 8/8 |
| LLM (full prompt) | 20/20 | 12/12 | 8/8 |

The paper itself qualifies this result: the catalog is small and co-designed with the policy rules, so it "validates specification–implementation alignment rather than deployment-scale coverage".

**Policy-specification ablations (Tables X–XI), facts held fixed at P₃.**

| Variant | Accuracy | F1 deny | FP | FN | Atomic | Composite |
|---|---|---|---|---|---|---|
| LLM, full prompt | 100% | 1.00 | 0 | 0 | — | — |
| LLM, ablated prompt | 75.0% | 0.84 | 4 | 1 | — | — |
| Heuristic, full | 100% | 1.00 | 0 | 0 | 12/12 | 8/8 |
| Heuristic, no compositional rules | 80.0% | 0.83 | 0 | 4 | 12/12 | 4/8 |
| Heuristic, simplified | 60.0% | 0.67 | 2 | 6 | 10/12 | 2/8 |

Removing compositional source–sink reasoning preserves atomic correctness but falsely allows four composite deny scenarios; the simplified variant also introduces two atomic false rejects and misses six composite denials. The LLM ablation removes explicit runtime rules, the compositional-risk table and closed reason codes while keeping the same P₃ facts, and degrades accuracy to 75.0% with four false denies and one false allow. The paper reads both as evidence that structured facts alone are insufficient.

**LLM cost (Table VIII).** Average per-decision token use: vetting at P₃ 2,156 input / 584 output; runtime with the full prompt 2,748 / 586; runtime with the ablated prompt 1,399 / 347. The paper reports Clingo solver overhead as negligible relative to characterization and LLM evaluation.

**Composite case study (§VIII-E, Appendix C).** A database-query tool and a GitHub project-management tool are each individually admissible, but their ordered use is denied because database records flow toward an external remote update.

## Limitations

**Stated by the authors.** The benchmark is a controlled set of 16 MCP-style tools and 20 runtime scenarios, which is "sufficient to study the proposed policy mechanisms" but does not cover the MCP ecosystem; more tool categories, implementation styles and deployment environments may expose different failure modes, and a larger benchmark would give more stable false-positive and false-negative estimates. The evaluation is MCP-centred; other agent–tool ecosystems may expose different metadata, invocation semantics, permission models, sandboxing assumptions and logging, and the paper proposes future evaluation on browser agents, code-execution agents, cloud API agents, plugin ecosystems and enterprise automation tools. Composition depth is bounded: the composite cases are short workflows, whereas real agents run long chains where risk accumulates through indirect dependencies, repeated transformations, delayed effects or intermediate artifacts, so the policy would need longer histories, temporal constraints, cross-invocation provenance and workflow-level invariants. The paper is also explicit that ASP gives determinism, not correctness — "a wrong rule, missing exception, or incomplete characterization fact can still produce an incorrect decision" — and recommends rule-coverage tests, mutation tests, independently authored scenarios and formal safety invariants as future work. On the LLM results it notes the model was not asked to inspect raw code but received normalized facts, explicit guidance and a fixed output contract, so the comparison understates the cost of unscaffolded LLM inspection.

**Assessed from the reporting.**

- **Single source, no artifact.** Everything rests on one arXiv preprint (v1, 23 July 2026). A search of the inspected HTML for a code or data link finds only third-party scanner repositories cited as related work (Cisco's mcp-scanner, MCPScan.ai) and arXiv's own infrastructure; no ToolGuardian implementation, fact-extraction pipeline, benchmark corpus or ASP rule set is publicly linked in the inspected text, so the configurations cannot be rerun as written and no independent replication is known.
- **Very small absolute counts.** The headline 0.86 / 88% is 14 of 16 decisions correct at P₂; at P₃ the ASP confusion matrix is seven true positives, two false positives, one false negative and six true negatives. The runtime "20/20" is twenty curated scenarios, and the composite denominator is eight.
- **The runtime result is close to specification conformance, not coverage.** The authors say so themselves: the catalog is co-designed with the rules, all three very different realizations score identically, and the paper offers no held-out scenarios. A rule set and a test set written together can be perfect without being right.
- **The strongest ablation is on the heuristic baseline.** Removing compositional rules degrades the heuristic; no equivalent ablation is reported for the ASP rules, even though the conclusion drawn ("runtime security depends … on explicit policy structure for composition") is stated generally. The ASP rule set's own completeness is untested.
- **Internal inconsistency in the composite count.** §VII-B and Table II state 8 composite scenarios, while §VII-C says "The 7 composite scenarios" and §VIII-C says "12 atomic and 7 composite cases", although Table IX reports 8/8 composite for every realization. The prose and the table disagree in the inspected text.
- **The ASP advantage is not demonstrated.** At P₂ all three realizations tie at 0.86 / 88%; at P₃ ASP and the LLM tie exactly (same confusion counts, same partial-outcome table). On the evidence reported, the declarative realization buys auditability and the ablation story, not accuracy.
- **Vetting labels are coarse and partly tautological.** Benign tools are labelled allow and malicious variants deny; a variant derived from a real tool with an injected behaviour is a fairly obvious positive, and the realistic case — a benign tool with a dangerous capability combination — is exactly what the framework gets wrong (Tool_011, two false rejects at P₃).
- **Threat-model gaps.** The adversary is assumed not to compromise the enforcement components, and the framework does not attempt to prove tool correctness. A malicious tool that behaves benignly under mock inputs and static analysis but activates on a live trigger (a particular environment variable, a rare input) is inside the assumed adversary's capability but not detectible by the stated evidence sources.
- **LLM-realization cost.** Even at ~2.7k input tokens per runtime decision, LLM-based enforcement carries recurring per-call cost that the ASP and heuristic realizations do not, once their policies are written.

## Competing approaches

**Compared directly, under identical inputs, output contract and scenarios.** The **imperative heuristic baseline** encodes policy as risk scores, thresholds and hand-written authorization checks, with all interactions hand-coded. The **LLM policy interpreter** reasons over the same structured facts and policy instructions through prompting, at temperature zero. The comparison is thus a controlled test of the *realization*, holding evidence fixed — which is the paper's methodological strength, since it separates "what evidence we have" from "how we decide".

**Cited as related and differentiated.** *MalTool* (Hu et al., arXiv:2602.12194) motivates the problem by showing malicious tools that are hard to distinguish from benign ones by description alone, and reports that existing detectors struggle to do so reliably. *Malicious agent skills in the wild* (Liu et al., arXiv:2602.06547) extends the concern to third-party agent extensions carrying credential theft and undocumented capabilities. *MCP Security Bench* (Zhang et al., arXiv:2510.15994), *MCP-SafetyBench* (Zong et al., ICLR 2026) and *MCPSecBench* (Yang et al., arXiv:2508.13220) supply benchmarks for MCP attacks and safety. *Prompt injection attack to tool selection* (Shi et al., NDSS 2026) covers attacks that manipulate which tool the agent selects; *InjecAgent* (Zhan et al., ACL 2024 Findings) covers indirect prompt injection in tool-integrated agents. On the defence side the paper lists MCP scanners, static-analysis tools, dependency inspection, rule-based checks, conventional malware and program-analysis tools, and LLM-based semantic vetting — citing Cisco AI Defense's `mcp-scanner` and MCPScan.ai as examples — and a body of runtime work on privilege-control policies, task alignment, causal attribution and prompt-injection defences at the tool-call boundary. Conceptually the framework builds on declarative access control, capability security, information-flow control and logic-based policy specification.

The authors' positioning claim is that prior work treats agent-tool security as either malicious-tool generation, tool-selection manipulation, pre-use scanning or runtime injection defence, whereas ToolGuardian treats it as a two-stage policy problem with characterization separated from enforcement. That is a framing claim about the literature, not a head-to-head result — the paper compares policy realizations, not other security frameworks. Within this knowledge base, [[projects/agentshield]] is the adjacent security project (defending web applications from agents, the inverse direction), and the framing here is a concrete instance of [[concepts/structural-constraint-over-instruction]]: the LLM is not the final authority on whether a side effect is permitted.

## Implications

The following is analysis by the KB maintainers, not a claim of the authors.

The most transferable idea is the separation of evidence from decision. Expressing what a tool does as a normalized fact vocabulary, and making the decision procedure a swappable realization over those facts, means the expensive part — characterization — is done once and can be re-judged under a different policy without re-running the tool. That is a genuinely useful engineering decomposition for any tool gateway, and it is the part of the paper that does not depend on ASP being the right formalism.

The second takeaway is the asymmetry in the ablations, and it argues for restraint. Removing compositional reasoning from the heuristic preserved atomic correctness and failed only on composite cases; removing rules from the LLM prompt cost 25 points of accuracy. In other words, the policy structure did the work, not the facts and not the reasoning engine. For a team building a tool gateway, the practical consequence is that the effort should go into the rule set and its composition semantics — source–sink relationships across a workflow, not into a larger model or a richer prompt. It also means a rule set that is never ablated should be assumed incomplete.

Third, the calibration result is the one to carry into deployment. At P₃ no realization fully admitted any benign tool: six of eight benign tools were admitted only with restrictions and two were hard-rejected, and the rejected ones were rejected for having real capabilities. A deployment reading only the deny-class F1 would conclude the policy is nearly perfect; the operational reality is that the policy is mostly saying "restricted" while occasionally blocking legitimate administration tools. Any rollout should therefore instrument restricted_admit as a first-class outcome and track false restriction separately from false rejection — the distinction the paper itself insists on.

Fourth, on defence claims: what this evaluation would have caught is a tool whose hidden behaviour shows up in syscall traces, mock execution or source analysis, and a workflow whose risk comes from a source–sink pair the policy models. What it would not have caught is a malicious tool whose activation condition is outside the exercised inputs and the available source, a tool whose dangerous behaviour is triggered by the agent's own legitimate usage rather than by an unusual input, and any bypass of the mediation layer itself, which the threat model explicitly excludes. The paper's own out-of-scope list is honest about this; the deployment implication is that the framework's coverage is bounded by the characterization evidence, so the characterization step is the security-critical one and should be hardened first.

Fifth, the composition result suggests where to put the effort in a multi-tool agent. Atomic authorization is the easy half; the paper's own case study shows two individually benign tools whose ordered use is unsafe. Any policy engine that reasons about one call at a time will miss exactly the cases the paper's composite scenarios are built around, so the workflow-level data structure is worth designing before the rule language.

## Reproducible experiment

No artifact is linked in the inspected text, so any check means reimplementing the characterization and policy layers from §V–VI. A feasible independent test:

1. **Build a small corpus with held-out scenarios.** Construct 10–20 MCP-style tools, at least half of them benign high-capability tools (process execution, shell access, database queries, network egress) rather than only obviously benign ones, plus variants with one embedded malicious behaviour each that preserve the original description. Write the malicious variants *before* the policy rules, and keep the rule set blind to them.
2. **Implement the four evidence levels separately** — L0 descriptions, L1 syscall traces, L2 mock execution with mocked dependencies, L3 AST analysis — and emit the fact vocabulary the paper uses (`capability`, `data_access`, `observed_http_post`, `modifies_remote_state`, `effect_mismatch`). Then produce the cumulative tiers P₀–P₃ and measure deny-class F1 and accuracy at each tier.
3. **Test the non-monotonicity claim.** The paper's most falsifiable and most interesting result is that F1 peaks at P₂ and falls at P₃ because static analysis flags legitimate capabilities. If in your corpus the P₃ tier only improves detection, the security–utility trade-off is a property of their benign-tool selection, not a law; if it reproduces, treat characterization depth as a calibration knob, not a "more evidence is better" dial.
4. **Run three realizations over the same facts and contract.** Implement a rule-based realization, a heuristic realization and an LLM realization (a local or open-weight model at temperature zero) over the identical fact base and the identical output schema, then ablate each: remove the compositional source–sink rules and the conformance exceptions, and remove the policy guidance from the LLM prompt while keeping the facts. The paper's reference points are 0.86 / 88% at P₂ for all three, 20/20 runtime, 75.0% for the ablated LLM prompt, 80.0% for the heuristic without compositional rules and 60.0% for the simplified heuristic. Directional agreement — especially that the ablations degrade while the facts stay fixed — is the informative result.
5. **Report restricted_admit separately.** Count, per realization and tier, how many benign tools are admitted only with restrictions, and how many are hard-rejected for possessing real capabilities. A binary metric will not show this, and the paper's own tables show the gap between 88% accuracy and a policy that admits nothing outright.
6. **Write independent composite scenarios last.** Compose scenarios that pair a benign source with a benign sink in an order the policy did not anticipate, and hold them out from rule development. A pass here is the only meaningful evidence that the composition rules generalize; a fail is consistent with the paper's own admission that the catalog was co-designed with the rules.

Substituting an available open-weight model for `openai/gpt-oss-120b` is straightforward; substituting the 16-tool corpus and the 20 scenarios is the larger and more important deviation, and any differences should be reported with the results.

## Evidence status

This page is grounded in a full read of the primary source — the arXiv abstract page (https://arxiv.org/abs/2607.21835) and the complete HTML full text including §V–X, the eleven result tables, the appendices (tool benchmark, task catalogue, enforcement case study) and the reference list (https://arxiv.org/html/2607.21835v1) — fetched on 2026-11-10. Every quantitative result is **author-reported**; the heuristic and LLM baselines were run by the authors, the paper is a single preprint (v1) with no peer-reviewed venue claimed, and no independent replication is known. A full-text search for a code or data link found only third-party scanner repositories cited as related work, so no ToolGuardian implementation or benchmark corpus is publicly linked in the inspected text. The internal inconsistency in the composite-scenario count (7 versus 8) is present in the source text as inspected. Claim types are separated in the text: the first-ASP-framework and differentiation claims are the authors'; the items under "Assessed from the reporting" and the whole Implications section are analysis by the KB maintainers. Nothing on this page was reproduced, executed, cloned or tested by the KB maintainers, and no malicious tool code was run.

## Historical coverage

- [[briefings/2026/11/2026-11-04]] — dated full-fidelity research and cross-project synthesis; this page is the deep-depth grounding of the ToolGuardian finding.
