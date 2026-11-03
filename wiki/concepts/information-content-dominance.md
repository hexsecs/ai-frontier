---
uid: 910c4aaa-5ba9-4db1-94c7-0d2df131c57c
title: "Information content dominates pipeline structure"
summary: "In controlled contrasts, what information reaches the agent — elicited answers, the current value, rubric criteria — beats the pipeline structure around it."
type: concept
depth: full
created: 2026-11-02
updated: 2026-11-02
related: [seq-k, intent-loss-in-smart-contract-synthesis, dynarev, skillcompiler]
sources:
  - url: https://arxiv.org/abs/2610.37859
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.37830
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.40133
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.39508
    retrieved: 2026-11-02
---

# Information content dominates pipeline structure

## What it is

Agent pipelines are full of loops: ask the client questions before generating, iterate against feedback after a failure, revise when the goal changes. The natural assumption is that the loop is the improvement — that more iterations, or a more adaptive loop, means a better result. This concept records the opposite finding, repeated across the KB's deepened project pages in three independent settings: **a loop's value tracks the diagnostic information it delivers, not its existence, its iteration count, or its adaptivity.** Answers to questions, the current value of a changed field, the specific rubric criteria a failed attempt missed — these move performance. Being told only "that failed," being reminded to go and check, or being given another iteration of the same loop, move it by approximately nothing.

This is the constructive counterweight to the mining pass's sceptical concepts. Where *net-negative interventions* warns that an added stage is not evidence of improvement, this concept says what the evidence points to instead: when studies varied information and structure independently, information won. It is distinct from *verification is load-bearing*: that concept concerns checkers and gates carrying a system's quality claims, whereas this one concerns the content flowing through elicitation, feedback, and revision loops, whether or not any verification is involved.

## Evidence for

**Elicitation before generation ([[projects/intent-loss-in-smart-contract-synthesis]]).** In the smart-contract synthesis study, answers obtained *before* generation were worth roughly twenty points of implementation fidelity, while everything after generation was worth at most about one. Checklist answers raised fidelity by +19.0 points (Claude Sonnet 5) and +22.7 points (Gemini 3.5 Flash) across model families, and the elicitation-first pipeline reached 72.9% at scale against 53.9% for one-shot generation. The decomposition is the sharpest part: verification plus client triage added +0.1 points without the answers and +0.5 with them, against roughly +21.0 for the answers themselves — the stages around the information contributed two orders of magnitude less than the information. Adaptivity contributed nothing either: a fixed ten-question checklist recovered the full reference-model gap (89.4% of planted mistakes caught, against 88.9% from the complete requirements document), while a targeted interviewer that asked about whatever it judged unclear recovered only part of it (80.4%). The questions' content did the work; the loop's cleverness did not.

**Disclosure at the decision point ([[projects/envos]]).** EnvOS's stale-value experiments hold the world change constant in every condition and vary only what the agent is shown at review. In clinic booking, success ran 0/16 when nothing extra was shown, 2/16 when the agent was reminded to re-check and given a source link, and 15/16 when the updated value was shown directly. The middle arm is the control this concept needs: exhortation is a pointer to information, not information, and it barely helped — only 1 of 16 reminder trajectories even followed the supplied link. What worked was the value itself arriving in context.

**Feedback content after failure ([[projects/seq-k]]).** Seq@K's feedback-mode contrasts isolate content inside an identical loop. Binary feedback — told only "that failed" — differed from plain resampling by −2.1 points with a confidence interval including zero: verdict-only feedback repairs no more than drawing a fresh sample. Rubric-aware critics, feeding back *which criteria* failed, repaired 73.8% of first-attempt-failed criteria, versus 34.4% under binary feedback. Same iterations, same models, same budget; the roughly forty-point spread is the feedback's content.

**Revision under a changed goal ([[projects/dynarev]]).** Of DynaRev's revision-handling strategies, the one that helps is the one that reorganises content: consolidating the accumulated instructions into a rewritten goal while preserving browser state raised the score from 0.647 to 0.718. Clearing history was roughly neutral for quality (0.648), and resetting was harmful. Re-presenting the requirements as a single coherent text — changing what information the agent is working from — beat every strategy that merely restarted or truncated the loop.

**Compilation versus iteration ([[projects/skillcompiler]]).** SkillCompiler's ablations put a number on the two kinds of component. Removing the revision loop or the skill skeleton cost ~2.7 points each (98.26% → 95.52%). Removing the Programmer — the component that changes *what is executed*, compiling well-specified operations into deterministic programs instead of re-interpreting text each run — collapsed success from 98.26% to 53.48%. The structure that iterates was worth single digits; the component that changed the content of execution was worth forty-five points.

## Evidence against and bounds

**The informant in the elicitation study is an oracle.** Intent-loss's simulated client answers the checklist by reading the original contract — the very artifact fidelity is scored against. The authors themselves frame the resulting gains as an optimistic estimate of what a real author would provide. A human client who does not know the answers, or answers them wrongly, may deliver far less than +19 to +23 points, and no page in this set measures elicitation against a genuinely uninformed informant.

**EnvOS's disclosure is the experimenter's interface choice, not the agent's achievement.** The study varies what the harness pushes in front of the agent at review time. It licenses a design prescription — build interfaces that surface the current value at the decision point — but it does not show agents acquiring information for themselves, and its own reminder arm shows the opposite: told to go and fetch the value, agents mostly did not (1 of 16 followed the link). In deployed systems without an experimenter arranging disclosure, the information still has to come from somewhere.

**The before/after ordering does not transfer.** Intent-loss's "everything after generation is worth at most about one point" is contradicted, apparently, by seq-k, where post-failure feedback produces large gains. The register records this as an apparent contradiction, resolved on both pages' own terms: intent-loss's post-generation loops were verdict-only in effect, because their instruments lacked ground truth — its repair reference model sides with the original contract only 31.6% of the time on real defects, so its feedback carried little diagnostic content to begin with. What survives is the shared claim, not the ordering: post-generation loops are worth a great deal when their content is rich, and ≈ 0 when it is a bare verdict, in both studies.

**Structure is not worth zero — it is worth what it preserves.** SkillCompiler's skeleton and revision loop still cost ~2.7 points each when removed, and seq-k shows a purely structural choice destroying value: replacing full attempt history with a summary cost up to −14.4 points on HealthBench. Both are consistent with this concept read precisely — structure matters insofar as it delivers or retains information, and a structure that compresses content away (summarisation) or discards it (resetting, in dynarev) is exactly the failure mode the concept predicts. DynaRev's winning strategy also entangles this concept with *accumulated state as asset*, since rewriting the goal helped while preserving browser state; the two contributions are not separated in that experiment.

## Relations

- [[projects/intent-loss-in-smart-contract-synthesis]] —contradicts (apparent)→ [[projects/seq-k]]: "everything after generation is worth at most about one point" against 73.8% of failed criteria repaired post-failure. Recorded in the register because a reader of either page alone would mispredict the other; this concept is the resolution both pages' terms support.
- [[projects/dynarev]] —supports→ [[projects/seq-k]]: delivering identical final requirements progressively changes outcomes in model-dependent directions, converging with seq-k's finding that gains from independent samples say little about gains from feedback (Δ-correlation −0.08). Independent designs, same underlying claim about revision.
- [[projects/intent-loss-in-smart-contract-synthesis]] —same-failure-mode→ [[projects/seq-k]], and [[projects/dynarev]] —same-failure-mode→ [[projects/seq-k]]: repair and revision can break what already worked — the risk side of acting on feedback, which bounds how aggressively content-rich loops should be applied.
- [[projects/envos]] carries the register's single-page pattern *disclosure beats exhortation* (15/16 shown the value, 2/16 reminded, 1 of 16 following the link), this concept's interface-design instance; envos is cited here as supporting evidence though it is not one of the register entry's four listed pages.
- Sibling concepts, named in plain text: *verification is load-bearing* (distinguished above), *net-negative interventions* (the sceptical counterpart — stages are not evidence), and *accumulated state as asset* (entangled in the dynarev result).

## Open questions

- Does the elicitation advantage survive a real informant? Every large before-generation gain in this set was measured against a simulated client reading the answer. The size of the effect with human clients — who omit, hedge, and err — is unmeasured.
- What is the dose–response curve for feedback content? Seq-k brackets the extremes (bare verdict ≈ 0; full rubric criteria ≈ 73.8% repaired) but nothing here maps the middle: partial criteria, failed-test names without rubric text, or a single most-relevant criterion.
- Can agents be made to fetch information rather than needing it pushed? EnvOS's reminder arm failed almost completely, yet deployed agents cannot rely on a harness arranging disclosure. Whether prompting, tooling, or training closes that gap is open.
- Is there any setting where loop adaptivity itself beats fixed content delivery? The checklist-versus-interviewer result says not yet, in one testbed; a domain where the right questions genuinely cannot be known in advance would be the place to look.

## Evidence status

This concept is the KB's own analytical construct, synthesized on 2026-11-02 in mining pass 1 from the KB's deepened project pages; it is not a term or claim from any single source paper. The register grades it **medium** (four supporting pages, one cluster, plus the envos disclosure pattern). Every underlying result is author-reported in its source preprint, none independently replicated, and the cross-study synthesis — in particular the resolution of the intent-loss / seq-k tension — is the KB's inference, labelled as such wherever it appears.
