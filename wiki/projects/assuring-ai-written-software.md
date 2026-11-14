---
uid: a29b51f0-ec09-4b70-9e90-900000000005
title: "A Case Study in Assuring AI-Written Software"
summary: "One operator's production healthcare platform, built by coding agents and governed by agents, exposed proxy checks, silent audits and an unsafe repair."
type: case-study
created: 2026-11-09
updated: 2026-11-10
depth: deep
sources:
  - https://arxiv.org/abs/2610.08651
  - https://arxiv.org/html/2610.08651v1
---

# A Case Study in Assuring AI-Written Software

## What it is

"A Case Study in Assuring AI-Written Software" is a short observational paper by Lindsey Ferris (Independent Researcher) and Sierra Bonilla (University College London), submitted to arXiv on 6 October 2026 (arXiv:2610.08651; subject classes cs.SE, cs.AI and cs.MA). The abstract page records a venue: **accepted to the NeurIPS 2026 Meta-Agents Workshop**, "Managing Agents that Manage Agents: Workshop on Responsible Use of Meta-Agents". The paper is CC BY 4.0.

The artifact is a **retrospective case study of one production deployment**, not a controlled comparison and not a benchmark. The setting is a healthcare platform built through coding agents and governed by an operator who has no formal software-engineering training. The paper's thesis is narrow and negative: coding agents let people without formal training build systems they could not otherwise implement, and simultaneously produce more code than even experts can meaningfully inspect — so exhaustive code review is not a reliable basis for human control. The report's contribution is a description of what the operator substituted for review, and of the ways that substitute failed.

The reported failure modes are the paper's most consequential content: some monitors measured proxies rather than outcomes, some audits failed silently, missing checks disappeared from reported results, and one automated repair caused operational disruption. The paper's stated conclusion is that human control in this case depended on tying four things to the same objective — the intended outcome, the evidence used to judge it, the agents' permissions, and the final human decision.

Everything below is drawn from the arXiv abstract page and the complete HTML full text including Appendix A. The paper links no code, data or repository artifact; the only link in the full text besides its references is to the arXiv HTML conversion build log.

## Mechanism

**What was done.** The study combines two structured interviews with the operator, conducted in June and August 2026, with project records spanning six months: decision logs, audit reports, incident records, check inventories and working notes. The authors reconstructed the development and assurance workflow from these sources and identified incidents in which an assurance mechanism produced incomplete or misleading evidence. Interview claims were cross-checked against available project records where possible. The paper states this is retrospective and observational.

**The setting.** The platform supported the business operations of a healthcare practice — note-taking support, scheduling and payroll workflows — alongside background functions such as access control, backups and audits. The operator could directly inspect some properties by trying a page or workflow in staging and judging whether it behaved as intended. Other properties were largely hidden from her: she could not directly see whether a backup was usable, or whether an audit had run completely. Requirements of a regulated healthcare setting (US health-privacy law) applied, **although the paper explicitly does not assess compliance**; HIPAA Security Rule and NIST SP 800-66 are cited only for context. Coding agents could access repositories, test data and staging systems, but production data was kept outside their reach through the system architecture and file and folder permissions.

**The session loop.** At the start of each session the primary coding agent re-read a versioned project rulebook, the current task and issue lists, and reusable skill files, so that "lessons and unfinished work stick even though each session starts fresh". The operator described the feature she wanted and approved or revised the proposed approach before implementation. Changes then passed project tests, were reviewed by a separate agent in a fresh context, and were deployed to private staging for human inspection. The separate reviewer functioned as an LLM critic. Production data stayed inaccessible to the agents, and changes reached production only after staging and explicit operator approval.

**Meta-audits and council.** The operator could also commission broader fresh-context meta-audits not tied to any particular code change: newly instantiated agents, with no access to the development conversation, inspecting wider parts of the system and its records for problems missed by the normal development loop. Their findings entered the same process of remediation, regression testing and reusable lessons. For difficult decisions the operator could invoke a multi-model council in which models from several providers independently answered the same brief without seeing one another's responses, returning recommendations, reasons and risks for her to weigh.

**Failure to lesson.** When a problem was confirmed, the agent was asked to fix it, look for similar problems elsewhere, and record any lesson that should carry forward. Agents could also propose reusable lessons at the end of a session; approved lessons were stored for later sessions.

**The one assurance technique that was tested.** The operator became concerned with whether the tests could genuinely detect the failures they claimed to cover — "I don't trust a test just because it passes." Tests were checked by deliberately recreating targeted failures and confirming that the corresponding checks failed. The paper relates this to the fault-seeding intuition behind mutation testing, and notes it matters particularly for LLM-generated tests, because incorrect code in the prompt can substantially reduce test accuracy and bug-detection effectiveness.

**Where control resided (RQ1).** The pattern the authors report is asymmetric delegation: the operator delegated implementation and much of its technical review, but not the authority to make consequential changes. Worker and reviewing agents could propose code, findings and persistent lessons; the operator controlled what became durable project context and what entered production. Control was concentrated at the points where agent outputs became persistent or operationally consequential, rather than exercised continuously through line-level inspection. The authors relate this to Barnes et al.'s framing of agentic CI/CD as an authority-transfer problem, with control-plane authority separated from bounded data-plane work, and to architectural tactics such as checkpoints, tool fencing and write staging for high-consequence actions. They also note a second-order effect: adding another reviewer moved rather than removed part of the oversight problem, because the operator then had to judge the reviewer's evidential scope and authority.

**Models (Appendix A).** Building, pre-merge review and meta-audits used Anthropic Claude models invoked through the Claude Code command-line agent. The multi-model council additionally queried Google Gemini and OpenAI GPT models through their APIs. Reviews and meta-audits were run by separately started agent instances with no access to the development conversation. The reviewing agents shared the builder's model family, so shared blind spots are possible — a limitation the authors state themselves.

## Evidence

Everything in this section is **author-reported from a single short workshop paper** and is observational. Nothing has been independently replicated, and no research artifact is released.

**The one quantitative result.** The authors mapped the check inventory accumulated through incidents and adversarial reviews against four external references that had not been consulted during its construction: the OWASP Top 10, OWASP Top 10 API Security Risks, CWE Top 25 and relevant HIPAA Security Rule provisions. Of **84 mapped items, 69 (82.1%) were covered by the pre-existing checks**. The paper is careful about what this establishes: it suggests the checks addressed many concerns represented in established security guidance; it does **not** establish full platform security, and it does not demonstrate model generalization, because the standards are public and independence from model training cannot be assumed — a benchmark-contamination concern the authors cite.

**The assurance failures.** These are the paper's substantive findings. They are described qualitatively, without dates, counts, or a prevalence estimate:

| Failure described by the source | What the source says happened | Why the reassuring signal was wrong |
|---|---|---|
| Proxy measurement | Several backup monitors checked whether intermediate events occurred | The check never established that a usable backup actually existed |
| Silent failure | An audit stopped running without producing a failure | Absence of a failure signal was not distinguished from absence of the audit |
| Denominator drift | Another report calculated its pass rate only from checks that emitted results | Missing checks disappeared from the total rather than counting as failures |
| Unsafe authority | A monitor misclassified legitimate long-running work as a failure and repeatedly attempted an automated repair | An incorrect result immediately triggered a harmful action, causing operational disruption |

The authors connect these to the test-oracle problem: even when a check executes, its verdict may not establish the intended outcome. The operational-disruption incident is described as "the most consequential incident" in the paper.

**What the paper does not report.** There is no count of defects before and after the workflow, no timeline of incidents, no comparison condition (no without-supervision arm and no without-agents arm), no measurement of review accuracy against human judgment, no cost figure, and no list of which project records were inspected. The single number (84 / 69 / 82.1%) is a coverage ratio of a self-assembled inventory against external taxonomies, not a measure of system quality.

## Limitations

**Stated by the authors.** This is a single case involving one operator, one platform and an evolving workflow. The operator was directly involved in creating both the system and its governance process, which may have led to an overly favourable interpretation; the authors reduced this risk by comparing the interview account with project records and focusing on concrete failures, but the evidence remains observational. The study does not establish that the workflow caused fewer defects, that the platform was secure or compliant, or that the same approach would be sufficient for other users or systems.

**Assessed from the reporting.**

- **No control group and no baseline.** The paper compares the workflow to nothing. There is no pre-agent state, no alternative supervision arrangement, and no measure of how many of the discovered failures would have been caught by ordinary review.
- **n = 1 operator, interviewed by the authors.** The main source is one person's account of a six-month period, reconstructed partly from memory, with records used only where available. The operator is also the sole judge of the workflow's success.
- **Failures are not enumerated.** The four incident classes are given as types, not as counts over a period. No denominator exists, so the reader cannot distinguish a rare catastrophic pattern from a routine one. The only rate-like figure in the paper is the security-coverage ratio.
- **Coverage is self-assessed.** Deciding that a check "covers" a CWE or OWASP item is a judgement by the authors from project records; the paper does not publish the mapping, the check inventory, or the criteria for a covered item.
- **The model caveat cuts both ways.** Reviewers shared the builder's model family, so correlated blind spots are plausible — and the multi-model council is the only mechanism in the workflow that would have broken that correlation, for a subset of decisions.
- **Review accuracy is unmeasured.** The paper uses LLM critics and agent meta-audits but reports no agreement between their findings and human judgment, and no count of findings that were false.
- **The most-cited security framing is context, not a compliance claim.** HIPAA and NIST are named to establish that safeguards were expected; the paper says plainly that compliance was not assessed.
- **Format constraints.** A workshop paper with an appendix for implementation details carries no artifacts, no supplementary data, and no preregistration. The 84-item mapping cannot be re-derived by a third party.
- **The visible/invisible asymmetry is the case's finding, not a measurement of it.** Staging worked well for observable behaviour; the clearest assurance failures occurred in less visible properties (backups, audit execution, monitoring completeness, automated recovery). The paper establishes where assurance broke, not how often.

## Competing approaches

Only alternatives the source itself names.

**Assurance precedents from software history.** The paper opens with the FORTRAN transition: as checking every generated machine instruction became impractical, assurance moved toward correctness proofs (McCarthy and Painter), conformance test suites (Holberton and Parker), per-translation validation (Pnueli et al.), verified compilers (Leroy) and randomized differential testing (Yang et al.). The authors state the analogy's limits explicitly — coding agents are not compilers, because they infer underspecified intent, act in stateful environments, and may modify their own tests — but keep the precedent as motivation for moving assurance elsewhere.

**Control by prompting and validation rather than inspection.** Recent work suggests experienced developers control coding agents through prompting, planning approval and validation (Huang et al.), and that practitioners' patterns are captured by evaluation-driven development (Xia et al.; Lyu et al.). The paper cites practitioner reports of a week's commits growing from a few hundred lines to 10–20K after coding agents, pull-request backlogs from generation outpacing review (Lyu et al.), and an initial task-completion advantage that largely disappeared on a later extension task done without the agent (Balepur et al.).

**Meta-agent oversight research.** The paper positions the case against guard agents that check other agents (Xiang et al.), critic models that help humans identify mistakes (McAleese et al.), and execution systems that preserve structured, reversible traces for meta-agent inspection and replay (Yu et al.). Its stated contribution is a complementary issue: once supervision itself is delegated, human oversight must also account for what the supervisor observed, what its output supports, and what authority follows from it.

**Architectural framings.** Agentic CI/CD as an authority-transfer problem (Barnes et al.) and architectural tactics for regulated contexts — checkpoints, tool fencing, write staging (Safin and Balta) — are cited as the design vocabulary the observed workflow resembles.

Within this knowledge base, the case is a direct instance of [[concepts/verified-completion-vs-apparent-success]] (a proxy or missing check reported as a pass) and of [[concepts/preservation-aware-agent-improvement]] (checks accumulated from incidents, and lessons carried forward between sessions). It is an analyst-level **compares_with** counterpart to [[projects/cheme-as-code]] and [[projects/agent-orchestrator]] — cross-study comparisons, not verified dependency or implementation links — and it feeds [[evaluations/briefing-synthesis-2026-11-03-to-09]] and [[case-studies/index]].

## Implications

The following is analysis by the KB maintainers, not a claim of the authors.

The most transferable output is the four-question checklist the paper's incidents imply, which generalises to any delegated assurance mechanism: does the check observe the intended outcome or a convenient proxy; is there evidence it actually ran; do missing or empty results remain visible; and is its authority limited enough that an incorrect result cannot immediately trigger harmful action. Each maps to one observed failure in the case, which is what makes the checklist memorable rather than generic.

Second, the denominator bug is the most transferable engineering lesson. A pass rate computed over checks that emitted results will improve as coverage shrinks — missing checks vanish from the total instead of appearing as failures. Any assurance reporting should compute over *expected* checks and treat an absent result as an unknown, never as a pass. The case supplies a concrete failure of this kind, which is rarer than a failure of the check itself.

Third, on authority: the operational-disruption incident is the paper's costliest finding and it is an architecture failure, not a detection failure. A monitor that cannot distinguish a long-running legitimate job from a failure, and that is permitted to act on its own verdict, converts a small evidence error into an operational one. The implication is to separate *detect* from *act*: monitors report, humans or a second, differently-informed component authorise, and any repair that can change production behaviour requires an independent gate.

Fourth, the visible/invisible split suggests where to spend assurance effort. Staging plus human inspection exercises the properties a person can see; backups, audit completeness and monitoring coverage are exactly the properties that survived to production unchecked. Restore drills and explicit completion receipts are therefore worth more per unit effort than additional staging scenarios.

Finally, the shared-model-family caveat generalises past this case: independent *context* for a reviewer is not independent *judgement*. If the builder and the reviewer run the same model family, correlated blind spots are plausible, and a second opinion only helps when it is genuinely differently sourced. This is also why the multi-model council matters as a pattern even though its results are not reported.

## Reproducible experiment

The paper releases no artifact, so any check means reimplementing the assurance stack and injecting the failure classes it reports. A concrete protocol:

1. **Reconstruct a minimal supervised pipeline.** One coding agent, a rulebook and session state, a separate fresh-context reviewer, deterministic pre-steps that assemble evidence, a set of ~20 outcome checks, and a regression-test store fed by confirmed incidents. Run it on 20 staged tasks in a sandbox, with an explicit operator-approval gate before any change is applied. This mirrors the case's structure at small scale.
2. **Inject the four documented failure classes.** (a) Replace one backup check with a proxy that observes an intermediate event but not a usable artifact. (b) Disable one audit so it stops running without failing. (c) Configure one report to compute its pass rate only over checks that emitted results. (d) Add a monitor that classifies a deliberately long-running (10-minute) legitimate job as a failure and attempts an automated repair.
3. **Conditions and controls.** Two arms: the pipeline as built, and the same pipeline with the four protections the paper implies — absent-result counted as failure, denominator over expected checks, repair gated on an independent authorisation, and a monitor whose scope excludes long-running jobs. Both arms run on the same 20 tasks with the same model and prompts; each injected failure is reproducible.
4. **Pass/fail criterion.** For the unprotected arm, the paper predicts that (a) the proxy check reports success while no usable backup exists, (b) the stopped audit produces no failure signal at all, (c) the report's pass rate is *higher* than the true rate over expected checks, and (d) the monitor triggers a repair against the long-running job — reproducing the operational-disruption class. For the protected arm, a replication would fail if any of these still occurs: a missing check must appear as an unknown, the denominator must stay fixed, and no repair may execute without an independent authorisation. Report per-failure detection and false-positive counts, not a single success rate.
5. **Secondary check — reviewer independence.** Run the reviewer with the same model family and once with a different provider, and record whether findings correlate. The paper predicts correlated blind spots within a family and greater disagreement across families; a large drop in agreement across families would weaken the independence argument for multi-model review.

Cost, elapsed time and tokens should be recorded per run, and any failure to detect an injected fault must be published as a negative result rather than a tuned configuration.

## Evidence status

This page is grounded in a full read of the primary source — the arXiv abstract page (https://arxiv.org/abs/2610.08651) and the complete HTML full text including Section 5 "Limitations and responsible use" and Appendix A "Implementation Details" (https://arxiv.org/html/2610.08651v1) — fetched on 2026-11-10. Every factual statement about the deployment, the workflow and the incidents is **author-reported** from a single v1 preprint accepted to a workshop; nothing was independently replicated and no artifact, dataset or repository is linked by the paper. Claim types are separated in the text: the workflow description, the incidents, the 84/69 coverage figure and the stated limitations are the authors'; the items under "Assessed from the reporting" and the whole Implications section are analysis by the KB maintainers, as is the reproducible experiment, which is proposed and not executed. Nothing on this page was reproduced, executed, cloned or tested by the KB maintainers, and no independent replication is known.

## Historical coverage

- [[briefings/2026/11/2026-11-09]] — dated full-fidelity research briefing; finding 5 selected this case study.
