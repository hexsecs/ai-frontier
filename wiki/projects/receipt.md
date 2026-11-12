---
uid: 18f9178b-41ac-4d02-aa15-4e510348467f
title: "RECEIPT — Process-aware tool execution"
summary: "Tool-execution protocol that reads from system calls what a process waits for and returns that state to an unmodified agent"
type: project
created: 2026-11-10
updated: 2026-11-10
depth: deep
related: [verified-completion-vs-apparent-success, protocol-relative-scores, capability-locus]
sources:
  - https://arxiv.org/abs/2611.01930
  - https://arxiv.org/html/2611.01930v1
---

# RECEIPT — Process-aware tool execution

## What it is

RECEIPT is a tool-execution protocol and process-state inspector for LLM agents that operate Web infrastructure from a command line. It is reported in the arXiv preprint "RECEIPT: Measuring and Repairing the Return Assumption of LLM Agents in Web Service Operations" (arXiv:2611.01930, submitted 1 November 2026, cs.SE; preprint, no peer-reviewed venue claimed). The paper lists six authors — Boyang Yang, Ziyao Yang, Yu Zhang, Duo Chai, Xiaoming Chen and Haoye Tian — with affiliations at Yanshan University, Tencent, Shenzhen Intelligent Strong Technology Co., Ltd. and Aalto University.

The problem it names is the **return assumption**: that each tool call returns within a bounded time *and* with its requested action finished. The paper argues that both common harness behaviours break it. If the harness closes the command's standard input, a program that asks a question reads end-of-file and takes its default — it may then return status 0 without performing the requested action. If the harness keeps input open, for example as a terminal at which nobody types, the program waits until a time limit and the agent pays in wall-clock time and tokens. A further consequence is that a leaderboard, which scores final state but never records what the process waited for, ends up ranking the harness's input connection alongside the LLM. The authors state, as an author claim "to the best of our knowledge", that this is the first work to measure and repair the return assumption.

The paper's contributions are stated as four items: the problem definition and findings; a measurement of real-world use; three datasets (Litmus, WaitAtlas, Tripwire); and a solution with a model-checked protocol, validated on two harnesses and eight LLMs and released inside a commercial agent runtime.

## Mechanism

RECEIPT wraps each shell command without changing the agent or the program. Its single design principle is that the harness returns to the agent the process state the kernel exposes, and leaves the task decision to the agent. That principle yields three layers.

**Layer 1 — the waited-for object, read from system calls.** RECEIPT keeps the command's input open and supplies no reply, so a program that asks a question waits instead of reading EOF and taking a default. A blocked read alone does not identify an input wait, because a read also waits for a file, a pipe or a socket. RECEIPT therefore samples three kernel facts every 0.1 seconds for each thread *t* of the command's process tree: the system call *s_t*, the set *D_t* of descriptors the call waits on, and the thread's CPU ticks. Let *C* be the descriptors RECEIPT controls (the command's input pipe and terminal) and *F* the "foreign" descriptors another party can make readable. A thread is a *candidate wait* when

> cand(t) ⟺ s_t ∈ S_in ∧ D_t ∩ C ≠ ∅ ∧ D_t ∩ F = ∅

where S_in holds the read and multiplexing calls (read, poll, epoll_wait). C can grow during a scan: a process that relays input through a terminal it holds — sudo and script do this — adds that terminal to C, and the test is re-evaluated. A candidate becomes a *confirmed wait* when it holds for one second during which the tree writes no output and the thread uses at most 5 CPU ticks. For a terminal, RECEIPT also classifies the read into a class κ from the line-discipline flags and the terminal's screen mode: a line with canonical input and echo, a secret without echo, a key-by-key read without canonical input, and a full-screen read on the alternate screen. The receipt names the program, gives the last output line as the prompt, states whether RECEIPT ended the local process tree, and marks earlier effects as unverified. RECEIPT interrupts only the local process tree; a deployment can report a wait without interrupting.

**Layer 2 — the order of intervention, as an automaton.** A persistent terminal needs a fixed order between the agent's keystrokes and RECEIPT's interruptions, otherwise a queued `cd` can be delivered to a script that has just asked a question. Each command is modelled as an automaton whose state σ = ⟨r, seen, ℓ, E, c⟩: r ∈ {blocked, gone} is the reader's state, `seen` records whether the agent has observed the reader's question, ℓ is the lock shared by sender and observer, E is the log of published receipts, and c ≤ |E| is the agent's cursor into E. The knowledge condition K(σ) ⟺ c = |E| ∧ (r = blocked ⇒ seen) guards every step that sends input: input reaches a program only after the agent has read every published receipt, including a blocked reader's question. Algorithm 1 in the paper encodes this. The sender defers the whole keystroke batch while a receipt is unread; when the reader is blocked and its question unseen, it holds the keystroke and publishes it together with the prompt, so the question reaches the agent before any answer does; and it holds an input whose form does not fit κ on first arrival — a key name sent as text, a command sent as a passphrase. The observer interrupts only when no input is in flight, only if the batch schedules no further input, and rechecks s_t before signalling; a reader the agent has just answered is reported again rather than interrupted. Proposition 3.1 states that in every reachable state no input reaches a reader whose question the agent has not observed, no scheduled input is interrupted before delivery, no stale input reaches the shell after an interruption, and no receipt reports the wait of a reader that has exited.

**Layer 3 — model checking and tests on real processes.** Two model checkers verify Proposition 3.1: a finite state explorer and a TLA+ specification checked with TLC, exploring every interleaving of the sender, observer, agent and program steps, with the program allowed to exit between any two steps. Both checkers give the same verdict for every configuration and return the shortest counterexample when a rule is removed. The seven properties are the four of Proposition 3.1 plus three about the order in which the agent observes receipts. Without its rules the protocol violates five of the seven; with its rules it violates none, while a reply to a live program, an interruption, and a fresh command after a report all stay reachable. Appendix B.5 reports TLC checking the seven properties as invariants over 499 states, and a second TLA+ module in which the protocol without the last two rules violates its invariants in 145 states while the final protocol satisfies them in all 114 reachable states. Docker tests with real tmux, real processes and no LLM reproduce four of the seven forbidden orders without the rule and pass with it in 17 cases; a further 13 cases test the other three rules.

**The three artifacts.** *Litmus* is a catalog of 158 checked command-line invocations of 77 programs in seven categories — confirmation, credential, interpreter, editor, pager, wizard and menu — with 123 invocations in Ubuntu 24.04, 2 in WSL and 33 on Windows, which has no terminal condition. Each invocation runs three times per input condition (closed input, an open pipe nobody writes to, and a pseudo-terminal nobody types at) and a post-check decides whether the requested action happened. *WaitAtlas* holds 4,855 commands from 1,151 programs in 668 package families, including 972 input waits, taken from written examples, the tldr-pages repository and NL2Bash; it exists to test whether a wait can be predicted before launch. *Tripwire* is a benchmark of 25 task pairs over database migration, deployment, asset updates, repository operations, cleanup and credential handling; each pair shares task text and a verifier script hidden from the agent, and differs by a single change — a command option, an alias, a configuration file, or the editor git opens — that makes the required program ask a question in the trap variant but not in the control.

## Evidence

All numbers in this section are **author-reported** from this single preprint; none has been independently replicated.

**Measurement setup.** The paper reports three corpora. The production corpus is the local session logs of 6 developers building a commercial document-review agent, using Claude Code and Codex on Windows and remote Linux across 19 repositories: 107 interactive Claude Code sessions over three months, 91,469 tool calls of which 52,953 are shell calls, and 39,985 commands from main agents. The public corpora are the 39 Terminal-Bench 2.0 submissions that record each shell call (23 harnesses, 16,063 trials, 557,909 shell calls, 19 LLMs among the 37 single-LLM submissions), SWE-rebench (111 tasks run five times each, 8,880 trajectories), and 111 SWE-bench Verified repair submissions (64,104 trajectories, 1,819,197 shell calls).

**Litmus outcomes.** With input closed, 18 of 156 prompting invocations return status 0 without performing the requested action — 11.5% of tested invocations. `docker system prune` removes nothing, `rm -i` and `rm -I` leave the files, and `find -ok` and `tar -w` skip every entry. In 12 further invocations the program acts without the confirmation it would have asked for, as `ssh-keygen` does when it writes a key with an empty passphrase. Under a terminal at which nobody types, almost every invocation hangs.

**Harness launch behaviour.** Eight Linux harnesses were tested with a scripted LLM server (Claude Code 2.1.292, Codex CLI 0.160.1, Gemini CLI 0.63.0, OpenCode 1.18.35, mini-SWE-agent 2.4.6, Aider 0.86.2, Goose 1.30.0, Terminus 2 from Harbor 0.24.0):

| Harness | Input under a terminal | At the limit |
|---|---|---|
| Claude Code | closed | background, 120 s |
| Codex CLI | closed | tool returns, 10 s |
| Gemini CLI | own terminal | SIGTERM, 300 s idle |
| OpenCode | closed | SIGTERM, 120 s |
| mini-SWE-agent | user's terminal | SIGKILL, 30 s |
| Goose | closed, user's tty | none |
| Aider | own terminal | none |
| Terminus 2 | terminal multiplexer | none |

Without an attached terminal, seven of the eight harnesses close the input of a plain command. Claude Code also sets `GIT_EDITOR=true`, so `git rebase -i` squashes a commit with status 0 and without interactive confirmation; no harness sets `DEBIAN_FRONTEND` or `CI`. Some harnesses also end a process without notifying the agent: under Claude Code, a sub-agent's `nohup` or `&` launch completes but is not noticed, and a harness-background sub-agent is killed at 2–6 s of 150 s without notice.

**Real-use waits.** Across the three public corpora, 1,345 calls wait for input; Corepack's confirmation before downloading pnpm accounts for 339 and git's password, host-key, user-name or pager input for 127. Of these, 1,064 wait inside a program rather than in the shell, and 616 of those are in a Web-operations tool. In production, the harness ended 81 of 52,953 shell calls at a time limit; two annotators independently classified all 108 calls carrying a timeout marker (Cohen's κ = 0.89) and both identified 27 of the 81 as polling loops the agent wrote to wait for a CI pipeline, a build or a background output file. Agents also issued 2,910 commands that only check whether a process is still alive.

**Terminal-Bench 2.0 interface comparison.** Calls recorded as not returned, by interface type:

| Interface | Submissions | Observed calls | Calls not returned | Trials affected |
|---|---|---|---|---|
| Multiplexer | 12 | 205,500 | 6.0% | 56.1% |
| Pseudo-terminal | 3 | 51,924 | 6.6% | 40.2% |
| Shell session | 5 | 60,074 | 2.3% | 21.8% |
| Pipes | 19 | 138,587 | 0.7% | 8.5% |

Replaying the 123 distinct waits from 39 tasks inside their own container images: 70 wait again, the eight harness environment settings together prevent 30, and closing input ends all 70 — with 41 returning status 0, of which 12 return without doing the command's work and 6 print a failure that a pipe in the command line masks. In none of the 28 tasks whose waits recur does a confirmation question guard the requested action, so the public tasks cannot score what Tripwire scores.

**Task recovery on Tripwire.** mini-SWE-agent runs the first 15 pairs; Terminus 2 runs all 25. Both use Qwen2.5-Coder-32B at temperature 0 with a 30-step limit; mini-SWE-agent limits each command to 30 s and runs each variant three times, Terminus 2 runs each variant once with a 600 s limit.

| Condition (5 LLMs) | Successes | False successes | Median run time | Million tokens |
|---|---|---|---|---|
| Closed input | 153 | 34 | 53 s | 4.4 |
| Terminal | 158 | 28 | 105 s | 10.4 |
| Receipt w/o report | 162 | 20 | 66 s | 7.8 |
| Receipt | 176 | 9 | 62 s | 7.9 |

RECEIPT reduces false claims of success from 34 to 9 across the five LLMs — the paper's 73.5% relative reduction — and uses 24.4% fewer tokens than a plain terminal. Under a plain terminal the trap variants take 2.6 times the total run time and 2.9 times the tokens of the controls. Task-paired resampling (20,000 resamples of the 15 tasks, seed 20261009) puts the 95% interval of the change in false successes below zero against closed input (−11.1 pp, [−20.9, −3.1]), against a plain terminal (−8.4 pp, [−13.8, −3.6]) and against Receipt w/o report (−4.9 pp, [−11.1, −0.4]).

**Ranking effects.** Kendall's τ_b between the closed-input and terminal rankings of eight LLMs is only 0.47. Llama-3.3-70B ranks 7th with input closed and 3rd under a plain terminal; on that model's own runs the trap successes go from 25 to 32 while false successes fall from 14 to 4. Gemma-2-27B moves from 8th to 8th, and three of the eight LLMs (Llama-3.3-70B, Mistral-Small-24B, Gemma-2-27B) were run only for the rankings. On the public benchmark, native Terminus 2 ends 13 trials of the 38 Terminal-Bench 2.0 tasks with recorded waits at a question.

**Detection quality.** On the 120 locally runnable Linux Litmus invocations that wait under a terminal, RECEIPT's report rate is 85.0%, against 66.7% and 68.3% for the two text baselines, at a median report delay of 1.1 s. The 18 waits RECEIPT does not report under a terminal are 15 that exit or act without waiting under its launch and 3 npm commands that draw a spinner while waiting. A 1-second inactivity watchdog is comparably fast but ends 82 of the 119 controls, whereas RECEIPT ends none. Against DeepSeek's process inspector on the same 120 invocations and 119 controls, at 7 seconds RECEIPT alone confirms 37 invocations and the inspector alone reports 1.

**Baselines in detail (Qwen2.5-Coder-32B).**

| Condition | Control successes | Trap successes | False successes |
|---|---|---|---|
| Closed input | 45 | 33 | 6 |
| Terminal | 45 | 40 | 2 |
| Terminal + text hint | 44 | 41 | 2 |
| Outcome monitor (published) | 41 | 30 | 6 |
| DeepSeek inspector (published) | 40 | 35 | 3 |
| Receipt w/o report | 44 | 40 | 0 |
| Receipt | 45 | 40 | 1 |

With all three streams on the same pseudo-terminal, Receipt raises trap successes from 161 to 174 and lowers false successes from 20 to 8 across the five LLMs. On Terminus 2, RECEIPT completes all 25 trap tasks with no false success, against 17 for native Terminus 2 and 20 for Receipt w/o report; the paper's migration example shows native Terminus 2 feeding a queued `cd` to the script's question and rebuilding the database, while RECEIPT reports the held text with the question and the agent answers "n".

**Deployment.** A rule-only monitoring hook ran in one developer's Claude Code from 5 October 2026 over 11,694 shell calls in 41 sessions without changing any command. The detector was ported to Rust for the document-review agent runtime and released on Linux and Windows on 9 October 2026 as an opt-in feature; from 10–25 October, 14 desktop installs belonging to 12 user accounts logged 1,436 shell calls on Windows, and from 11–17 October the web deployment's server logged 149 on Linux. The detector's checks took a median of 0.11 ms per call on Windows and 0.54 ms on Linux.

**Pre-launch prediction.** On 267 held-out test commands from 110 program families absent from training (14 pipe waits, 32 terminal waits), the best predictor is a zero-shot Qwen2.5-32B-Instruct with AUROC 0.900 and average precision 0.477 for pipe waits, and 0.717 and 0.395 for terminal waits; a tuned Qwen3-0.6B reaches 0.761/0.194 and 0.666/0.240, logistic regression 0.737/0.126 and 0.704/0.222, and a rule set 0.603/0.170 and 0.572/0.199. The paper's conclusion from this is that a harness needs to detect waits at run time.

## Limitations

**Stated by the authors.** Appendix A sets out four threats. *Internal validity*: agent runs vary, so the paper fixes temperature at 0, runs each mini-SWE-agent variant three times, and compares conditions on the same task pairs with task-paired resampling; it also notes that the two intervention conditions connect output differently and answers this with the matched-stream comparison of Table 6. *Construct validity*: an agent's completion claim or a status-0 return can misreport what a command did, so the paper logs process behaviour with witnesses independent of the agent and decides success with final-state verifiers hidden from the agent; manual labels could depend on the annotator, so two annotators label the production timeouts independently from a written guideline and only agreed labels are reported. *External validity*: findings may not hold for other harnesses and LLMs, so the paper measures 23 harnesses and 19 LLMs in public trajectories, tests launches under eight Linux and two Windows harnesses, and runs Tripwire with eight LLMs from four families on two harnesses with different terminal designs; it acknowledges that a benchmark written together with the detector could favour RECEIPT and answers this by freezing the detector before writing the last 10 of the 25 task pairs, on which RECEIPT completes all 10 on Terminus 2. *Ethics and safety*: every program that changes a system runs in a container or scratch directory, the WaitAtlas and RECEIPT containers have no network access, and the production session text is not released.

**Assessed from the reporting.**

- **Single source, no public artifact.** Everything rests on one arXiv preprint (v1, 1 November 2026). A full-text search for a code or data link finds only harness repositories (claude-code, goose, aider, gemini-cli, codex, deepseek-harness) and public data references (tldr-pages, SWE-bench experiments); Litmus, Tripwire and WaitAtlas are described but no release URL for them is given, and the detector is described as shipped inside a commercial runtime rather than as an open repository. No third party can therefore rerun the authors' configurations as written.
- **Small absolute counts.** The headline 73.5% is 34 → 9 false successes over five LLMs × 15 trap pairs × three repetitions — nine events in the treated condition. Per model the movement varies: Llama-3.1-70B goes from 6 to 0 false successes while Qwen2.5-72B goes from 10 to 6, and on the pseudo-terminal comparison Qwen2.5-Coder-32B is unchanged at 39/0.
- **The detector, not the receipt, is the smaller half of the gain.** Receipt w/o report — the same detector, interruption rule and hold rule, returning only the output so far plus a one-line interruption notice — already reaches 162 successes and 20 false successes against 153 and 34 for closed input. The full receipt adds 14 successes and removes 11 further false successes.
- **Detection is imperfect and slow enough to matter.** 85.0% report rate means roughly one in six genuine waits is missed, with a median report delay of 1.1 s, and the paper's own deployment reports a wait only after a one-second confirmation window.
- **The ranking claim is thin.** It rests on eight LLMs, of which three were run only for the rankings, and it is a single-model move (Llama-3.3-70B, 7th → 3rd) supported by a rank correlation of 0.47. The paper does not test whether a harness change alters leaderboard positions on a benchmark it did not write.
- **Deployment evidence is thin on outcomes.** The commercial-runtime numbers (1,436 Windows and 149 Linux shell calls) report only latency — a median of 0.11 ms and 0.54 ms per call — with no accuracy, false-success or false-positive measurement from the deployed feature.
- **Scope is shell commands.** The protocol is specified for command-line execution; the paper explicitly does not cover browser or web front-end agents, and the Web-automation framing is applied to services operated from a shell.
- **Baselines are author-run.** The published baselines (DeepSeek's inspector, the outcome monitor of Panthi and Abdelfattah) were executed under the authors' harness; the outcome monitor's contracts cover only 97 of 2,709 commands under strict single-program attribution, and it fires a notice in 8 of the 34 false successes, so the comparison may understate that baseline.

## Competing approaches

The paper's own related work separates command handling into before, during and after execution, and RECEIPT positions itself in the gap it leaves at the moment a tool call returns.

**Directly compared at run time.** *DeepSeek's process inspector* (deepseek-harness) checks standard input and the terminal's foreground process group; RECEIPT instead reads what each process waits for and orders its interventions under a model-checked protocol, so it also reports a program that reads `/dev/tty`. In the head-to-head on Litmus, the inspector alone reported one invocation at 7 s where RECEIPT alone confirmed 37. *Outcome monitors* (Panthi and Abdelfattah, arXiv:2608.19303) check each returned tool result against contracts mined from task-disjoint traces and append a non-binding notice; on Tripwire they completed 30 trap runs with 6 false successes against RECEIPT's 40 and 1. *Text baselines* — a prompt-pattern rule and a character-sequence classifier reading the last 160 characters of a tool result — reach 66.7% and 68.3% report rate. An *inactivity watchdog* ending a command after 1, 3 or 5 seconds without output ends 82 of 119 controls. A *post-hoc trajectory classifier* (Advani et al., arXiv:2606.09863), a TF-IDF classifier over the serialized trajectory trained with the verifier as the label, flags only 6 of the 34 closed-input false successes at a 10% flag rate. A *verification instruction* added to the task ("Before you finish, verify that the task's goal state holds") completes 35 of 45 trap runs with 5 false successes under closed input, against RECEIPT's 39 with 1.

**Cited as related.** *Pre-execution* work includes pre-launch analyses that predict shell effects from system-call traces and annotations (Caruca; ahead-of-time analysis of shell program effects; PaSh), repair of missing non-interactive options in Dockerfiles (Parfum), risk-pattern checking (CARE), and QuoteBench on how matched scores hide command-path failures. *During execution*, non-blocking interfaces that expose debugger or server prompts (EnIGMA), asynchronous execution (AsyncTool, Gaia2) and Terminal-Universe let agents progress during tool calls. *After execution*, state-based tests and developer-written postconditions (AppWorld, verified tool calls under non-atomic failures), trajectory classifiers and mined contracts cover the completed-command case. The authors also cite their own earlier work on intent-execution correspondence (arXiv:2610.04375) for the "correspondence" framing.

Within this knowledge base, RECEIPT is the narrowest of the execution-state controls: [[projects/procgrep]] fingerprints procedures from trajectory patterns, [[concepts/verified-completion-vs-apparent-success]] states the general problem, and [[techniques/verification-and-evidence]] covers the post-hoc checks that RECEIPT explicitly positions against — it offers process-state evidence during execution and claims to need no task-specific postcondition.

## Implications

The following is analysis, not a claim of the authors.

The paper's most transferable move is to treat the harness's input connection as a first-class experimental variable. The evidence that this is not a marginal detail is the rank inversion: with the same model and the same tasks, the input connection alone moves an LLM from 7th to 3rd, and the aggregate rank correlation between the two conditions is only 0.47. Any benchmark that does not state and fix its input connection is measuring a mixture, which is a concrete instance of [[concepts/protocol-relative-scores]] and [[concepts/capability-locus]] — the observed capability of the system is a property of the harness as much as of the model.

The second takeaway is about what to assert. Exit status 0 is a claim by the process about itself, and the paper's own terminology — a *false return* versus a *false success* — is a useful split: the first is a process-level mismatch between status and effect, the second is an agent-level claim that verification contradicts. Any monitoring or scoring layer that treats a status code as evidence of effect is measuring the wrong thing, which is the [[concepts/verified-completion-vs-apparent-success]] failure in its most literal form.

Third, the cost argument is favourable in a way that is easy to miss: the detector's median cost is 0.11–0.54 ms per shell call, so runtime observation of process state is not a performance problem, even in a production runtime with a per-call budget. What is expensive is the alternative — the 2.9× token multiplication of an unanswered question at a terminal, and the 30-second wait in the paper's own running example. That reframes "should the harness observe more?" from a performance question to a correctness one.

Fourth, the model-checked ordering of input, interruption and report is the reusable engineering pattern. The failure it prevents — a queued keystroke answering a question the agent has not seen — is not specific to this paper's detector; it appears in any design where an agent's next action is typed into a persistent session while a program is blocked on a prompt. Expressed as an automaton with an explicit knowledge condition, the invariant is checkable, and the paper's own finding that an unguarded protocol violates five of seven properties gives a concrete template for reviewing such designs.

Finally, the wait-detection result sets a realistic expectation for anyone planning to build this: pre-launch prediction on unseen program families is weak (average precision 0.477 for pipe waits, 0.395 for terminal waits, from a 32B zero-shot model), so a design that relies on predicting interactivity will lose roughly half the cases, and a run-time detector is the load-bearing component. The corollary is that pre-launch prevention of the same failure is a complementary strategy, not a substitute.

## Reproducible experiment

No artifact release exists for the detector or the three datasets, so any check means reimplementation from the method and appendices. A feasible independent test of the core claim:

1. **Instrumented suite under three input conditions.** Build 10–20 invocations covering the categories the paper identifies — a confirmation prompt, a passphrase request, an editor, a pager, an interactive interpreter — using a scripted program that logs its own behaviour (the paper's "witness" idea) rather than trusting the agent's report. Run each three times with (a) stdin closed, (b) stdin an open pipe nobody writes to, (c) a pseudo-terminal nobody types at. For each run record the exit status and a post-check of the requested effect. The pass criterion is the paper's: a status-0 return without the requested effect should appear under closed input at roughly the paper's rate (11.5% of prompting invocations, 18 of 156) and near zero under a terminal. A materially lower rate would mean the failure is rarer than claimed for your command mix.
2. **Detector replication.** Implement Layer 1 only — sample the thread's system call, waited-for descriptor set and CPU ticks every 0.1 s, apply the candidate and confirmation rules, and classify terminal reads by line-discipline flags. Measure the report rate on the waiting invocations, the false-positive count on the control invocations (long computations, sleeps, network waits, pagers that print and exit), and the report delay. The paper's numbers — 85.0% report rate on 120 waiting invocations, zero false positives on 119 controls, 1.1 s median delay — are the reference; a detector with materially more false positives on the controls would show the paper's "one-second watchdog ends 82 of 119" problem reproducing itself.
3. **The persistent-terminal race.** With tmux and no LLM, reproduce the paper's forbidden order: queue a keystroke, then let the program print a question, and check whether the keystroke is delivered as the answer. The paper's Table 15 lists seven forbidden orders with their rules and 30 Docker cases in total (17 reproducing four of the orders without the rule and passing with it, plus 13 for the other three). A pass means no input reaches a reader whose question has not been read by the agent; a failure means the race is real on your terminal stack and the knowledge condition must be implemented.
4. **Does the harness move the ranking?** With two or three open-weight models of differing strength, run one small paired task set under closed input and under a plain terminal, with everything else — model, prompt, image, step limit — fixed, and compare both the absolute trap successes and the rank order. This is the paper's most consequential claim and its least replicated: the paper's own result is a single model moving 7th → 3rd with a rank correlation of 0.47 across eight LLMs. A directionally matching rank movement would be informative; an unchanged rank order under a large enough model set would falsify the ranking claim as stated.

Substituting available models for the paper's 2026 hosted backbones is unavoidable, and the substitutions and any harness version differences should be reported alongside the results.

## Evidence status

This page is grounded in a full read of the primary source — the arXiv abstract page (https://arxiv.org/abs/2611.01930) and the complete HTML full text including appendices A–B.8 and the reference list (https://arxiv.org/html/2611.01930v1) — fetched on 2026-11-10. Every quantitative result is **author-reported**; the baselines were run by the authors; the paper is a single preprint (v1) with no peer-reviewed venue claimed. A full-text search for a code or data link found only third-party harness and corpus URLs, so no artifact for RECEIPT, Litmus, Tripwire or WaitAtlas is publicly linked in the inspected text. Claim types are separated in the text: the first-of-its-kind claim and the "agent builders should report…" recommendations are the authors'; the items under "Assessed from the reporting" and the whole Implications section are analysis by the KB maintainers. Nothing on this page was reproduced, executed, cloned or tested by the KB maintainers, and no independent replication is known.

## Historical coverage

- [[briefings/2026/11/2026-11-10]] — dated full-fidelity research and cross-project synthesis.
