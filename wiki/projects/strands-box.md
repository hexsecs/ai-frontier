---
uid: 43f5e5d7-9c80-4250-98e6-48b6c493bdb5
title: "Strands Box — Stateful policy sandbox for agents"
summary: "Rust sandbox that combines OS containment with a default-deny Dogwood policy engine, so file, network and MCP decisions can depend on earlier agent actions."
type: project
created: 2026-11-10
updated: 2026-11-10
depth: deep
related: [structural-constraint-over-instruction, secure-agent-operations, verified-completion-vs-apparent-success]
sources:
  - https://github.com/strands-agents/box
  - https://api.github.com/repos/strands-agents/box
  - https://api.github.com/repos/strands-agents/box/releases
  - https://api.github.com/repos/strands-agents/box/git/trees/main?recursive=1
  - https://raw.githubusercontent.com/strands-agents/box/main/README.md
  - https://raw.githubusercontent.com/strands-agents/box/main/SECURITY.md
  - https://raw.githubusercontent.com/strands-agents/box/main/crates/box/README.md
  - https://raw.githubusercontent.com/strands-agents/box/main/crates/policy/README.md
  - https://raw.githubusercontent.com/strands-agents/box/main/crates/egress-gateway/README.md
  - https://raw.githubusercontent.com/strands-agents/box/main/crates/containment/README.md
  - https://raw.githubusercontent.com/strands-agents/box/main/docs/design/architecture.md
  - https://raw.githubusercontent.com/strands-agents/box/main/docs/design/security.md
  - https://raw.githubusercontent.com/strands-agents/box/main/docs/design/policy.md
  - https://raw.githubusercontent.com/strands-agents/box/main/docs/design/tenets.md
  - https://raw.githubusercontent.com/strands-agents/box/main/docs/design/limitations.md
  - https://raw.githubusercontent.com/strands-agents/box/main/docs/design/credentials.md
  - https://raw.githubusercontent.com/strands-agents/box/main/docs/design/egress.md
  - https://raw.githubusercontent.com/strands-agents/box/main/docs/user/security.md
  - https://raw.githubusercontent.com/strands-agents/box/main/docs/user/tool-grammars.md
  - https://raw.githubusercontent.com/strands-agents/box/main/test-workload/README.md
  - https://raw.githubusercontent.com/strands-agents/box/main/.github/workflows/ci.yml
---

# Strands Box — Stateful policy sandbox for agents

## What it is

Strands Box is an open-source sandbox engine for AI agents, written in Rust, in the `strands-agents` GitHub organisation and published under the Apache License 2.0 with a project home page at strandsagents.com. Its own description in the repository metadata is "Run AI agents in a sandbox that restricts what they can execute, read, write, and reach on the network. Box combines OS isolation with default-deny Dogwood policies and credential injection that keeps secrets outside the agent."

The repository was created on 2026-10-02 and the GitHub API reported `pushed_at` 2026-11-11T01:18:33Z, 526 stars, 46 forks, 112 open issues (63 issues and 49 pull requests at the top-level tabs) and 173 commits, with Rust as the primary language. Releases are published by `github-actions[bot]`: v0.1.0 on 2026-10-07, v0.2.0 on 2026-11-05, v0.2.1 on 2026-11-06 and v0.2.2 on 2026-11-10. v0.2.2 ships `box-v0.2.2-aarch64-apple-darwin.tar.gz`, `box-v0.2.2-linux-arm64.tar.gz` and `SHA256SUMS.txt`; its notes state that "Linux x86-64 remains a build artifact and is not a published package", and the download instructions carry the line "Package availability does not establish security acceptance."

The README labels the project a **Preview**: "Box supports local execution on Linux ARM64 and macOS with Apple silicon. We welcome feedback through GitHub issues." It is therefore a pre-1.0 project with a named version series and a published changelog, not a released production boundary.

The security posture is documented rather than assumed. `SECURITY.md` states that Box is pre-1.0 and under active development, that security fixes apply to the latest `main`, that a bypass of any control the box enforces is a security issue, and that reports go to the AWS Vulnerability Disclosure Program via HackerOne rather than to public issues. It also names what is explicitly **out of scope**: speculative-execution and side-channel attacks, multi-tenant isolation within one OS process, a workload reading files or hosts it was explicitly granted, and resource consumption within externally configured limits.

The distinguishing design claim is that the *decision* is not a static allowlist. The README states that Box's interpreters and gateways "share an event history, so rules can use earlier actions and elapsed time to decide what is allowed next. For example, a file read through Shell or Python can cause the gateway to deny a later outbound HTTP request."

## Mechanism

A box has three kinds of part, and the boundary between them is the whole design. Files inspected: `README.md`, `SECURITY.md`, `crates/box/README.md`, `crates/policy/README.md`, `crates/egress-gateway/README.md`, `crates/containment/README.md`, `docs/design/architecture.md`, `docs/design/security.md`, `docs/design/policy.md`, `docs/design/tenets.md`, `docs/design/limitations.md`, `docs/design/credentials.md`, `docs/design/egress.md`, `docs/user/security.md`, `docs/user/tool-grammars.md`.

**Where the boundary sits.** `docs/design/architecture.md` describes "the box's trusted process", which is `strands-box run` or a host application calling the Box library. It runs outside every sandbox and holds the policy engine, the four enforcement points, the certificate authority and the resolved secrets. Inside the sandbox is only the agent application. The OS enforcement layer bounds the workload's own system calls; the policy layer decides each request the workload sends to the trusted process. `docs/design/security.md` states the direction plainly: "Box assumes the workload is hostile, including when it runs an agent that follows malicious instructions" and "Box aims to protect the operator's files, credentials, and connected systems by restricting that workload's access. It does not protect the workload's contents from the surrounding OS."

**What is mediated.** `docs/design/architecture.md` gives the parts table: Strands Shell (Box's shell interpreter) decides `shell:exec` or `shell:spawn` per command line plus an `fs:*` action per file operation; Monty (Box's Python interpreter) decides `fs:*` per `os` call; the egress gateway decides `net:connect`, `http:request` and `mcp:call` for remote servers; the MCP broker decides `shell:spawn` to start a local stdio server and `mcp:call` for requests to it. The broker itself "does not authorize requests itself" and treats the alias as hostile input.

**The alias.** The workload has no host shell. `crates/box/README.md` records that the profile permits exec on granted literals "and nothing else, so `/bin/sh` and `/bin/zsh` are refused by the kernel", and that the box instead installs five aliases on the workload's `PATH` — `zsh`, `bash`, `sh`, `python3`, `python` — each forwarding to an interpreter hosted by the trusted process over `run/box.sock`. `argv[0]` selects the interpreter. The alias derives its socket from its own path so the workload cannot aim a request at a socket it controls, and it has no serving role at all, so the workload cannot start its own unmediated shell.

**How policy is expressed.** The language is Dogwood (documented at dogwood-policy.github.io/dogwood/), described in `docs/design/policy.md` as extending Cedar with temporal rules that use recorded events within a time window; `crates/policy/README.md` states the engine "uses the published `dogwood-language` and `dogwood-local-engine` crates" and that the engine is pinned to an exact version. Cedar `permit`/`forbid` text loads unchanged, and `when temporal { … }` adds a verdict that depends on recorded history. The action vocabulary is closed and strict-validated at load: `fs:read`, `fs:write`, `fs:delete`, `fs:move` and a reserved `fs:other`, plus `net:connect`, `http:request`, `shell:exec`, `shell:spawn` and `mcp:call`, with per-tool MCP actions for discovered tools and `Tool::<name>` actions for tool grammars. `crates/policy/README.md` records the composition rule: "Permits combine by permit-overrides, so a second `permit … when temporal { count < N }` scoped to a whole action grants everything the narrower rules excluded" — a cap must therefore be written as a `forbid`. The engine is the only authorizer: "Other checks can refuse an operation, but they cannot grant one that policy denies", and "an empty or absent policy denies everything."

**How policy is evaluated.** `docs/design/policy.md` describes one `PolicyEngine` per box, inside the trusted process, with one durable history file at `<box_dir>/private/dogwood.redb`. Each decision appends the request to history *before* evaluating the rules and writes the append to disk before returning the verdict; the caller then records how the operation ended. The engine timestamps events from the system clock, and "if the clock steps backwards, timestamps keep moving forward, so rolling the clock back doesn't free a budget". If an append fails, "the engine denies that request and every subsequent request."

**History semantics.** Three event kinds exist: `::request` for every durably submitted attempt, allowed or denied; `::response` for an operation that happened or may have happened; `::error` for one that definitely did not. The docs are emphatic about the consequence: "Because a denied attempt is still a `::request`, asking and being refused satisfies a precondition keyed on `::request`. Key a precondition on `::response` instead." A `::response` count can be overspent by concurrent in-flight requests, while a `::request` count is exact but a refused attempt spends from it. Every event carries a nonempty `requestId` allocated from the next durable log offset, and history is pruned outside the longest window, which is capped at 24 hours — "a longer window refuses to load".

**Where enforcement actually happens on the network.** `docs/design/egress.md` states the gateway "terminates every connection so it can inspect the requests inside it": it decides `net:connect` on the host and port before DNS, resolves once and pins the addresses, then decides `net:connect` again per pinned address before dialling, and only afterwards decides `http:request` on the method and path. One HTTPS call is therefore two decisions. The sandbox blocks direct network access so a client that ignores the proxy variables cannot connect. Cloud instance metadata has **no built-in block**: "Policy provides the only check on metadata endpoints. The gateway has no built-in block", and `docs/user/security.md` gives the two `forbid` rules an operator must write by hand.

**Credentials.** `docs/design/credentials.md` describes the phantom mechanism: at startup Box reads the real secret from its own environment, keeps it in the trusted process, and gives every contained process a placeholder — `strands_box_` plus 64 random hex characters, optionally with a route-specific prefix. The gateway swaps the placeholder for the real value on a permitted request to a bound destination, over TLS only ("It refuses a plain `http://` request to a bound destination before it adds anything"), and redacts every copy of the secret from the response, refusing a compressed credentialed response because it cannot scan one. `aws://` routes are signed with SigV4 by the trusted side, and a profile using `credential_process` is refused because that would make the trusted process run a program named by a config file.

**Containment.** `crates/containment/README.md` records the two backends: on macOS a checked-in Seatbelt profile (`src/backend/macos/seatbelt-agent.sb`) with one rule block per grant; on Linux ARM64 a namespace launcher that unshares a PID namespace, forks twice (a reaper as namespace PID 1, the workload as PID 2) and builds the filesystem view the workload sees. Landlock was "considered as the Linux mechanism and rejected: it restricts the calling process in place and expresses no right that denies all network". Linux on any architecture other than ARM64 returns `ContainmentError::PlatformUnsupported`. `Containment::apply` "either contains the process or returns a `ContainmentError`", and callers are told to treat every error as incomplete containment.

**Failure handling.** A denied command exits `126` with no output; a Shell failure exits `125`. On macOS a process that applies a sandbox to itself cannot remove it, so the trusted process starts `strands-box-contain-trampoline` to apply the sandbox in a separate process which then becomes the target program. `crates/containment/README.md` records that the trampoline starts with an empty ambient environment, unlinks its config file, verifies a SHA-256 digest before parsing, and only after `apply` succeeds installs the target environment and executes the command.

**Records.** The README states Box "records policy decisions in OTLP JSON. By default, records go to `<box_dir>/private/telemetry/records.jsonl`." `docs/user/security.md` documents the marker fields for a refusal that policy could have permitted: `strands.box.policy.cause` set to `enforcement` and `strands.box.policy.rule` set to `enforcement:reach-floor`.

## Evidence

Everything in this section is **code- and documentation-inspected fact** unless marked otherwise; the KB maintainers ran none of it.

**Repository structure.** The recursive tree of `main` contains 1,403 paths. The workspace crates are `box`, `containment`, `credentials`, `egress-gateway`, `ingress`, `policy`, `shell`, `telemetry` and `box-bench`. Documentation is split into `docs/user/` (install and operate), `docs/design/` (architecture, containment, credentials, decisions, egress, limitations, linux-enforcement, macos-enforcement, mcp, monty, platform-differences, policy, security, shell, telemetry, tenets) and `docs/dev/` (releases, fuzzing, macos-release, site-manifest, linux target tests).

**Tests present in the tree.** `test-integ/` holds a large numbered containment suite — `tests/containment/cn_b_01.rs` through `cn_x_04.rs`, plus named cases such as `cn_mcp_tool_policy.rs`, `cn_native_egress.rs`, `cn_linux_future_deny_refusal.rs` — together with `tests/policy/po_*.rs`, `tests/shell/sh_*.rs` and `tests/monty/mo_*.rs`. `crates/box/tests` holds `box_shell.rs`, `box_credentials.rs`, `box_filesystem.rs` and `site_manifest.rs`. `test-workload/verdict/src/jailbreak/` holds a Rust harness with `canary.rs`, `creds.rs`, `validity.rs`, `coverage.rs`, `verdict.rs` and `upload.rs`. `test-native-filesystem/` holds `tests/bridge.rs` and `tests/enforcement.rs`. The crate README states the shell test "runs `/bin/bash` as its workload, because it resolves `zsh` off `PATH` exactly as an agent harness does", and that the credential and filesystem suites "assert what the kernel, the proxy, and the shim actually did, not what a rendered profile says".

**CI.** `.github/workflows/ci.yml` defines path-filtered jobs: `packaging` (runs `python3 -m unittest discover -s scripts -p 'test_*.py' -v`), `rust`, `site-manifest`, `containment` (via `containment-deterministic.yml`), `verdict` (via `verdict-hermetic.yml`) and a `ci-gate` job that uses `re-actors/alls-green` with `allowed-skips` for the four filtered legs. The gate explicitly refuses a draft as merge evidence: "Draft run: containment and verdict did not run."

**The agent-driven workload suite.** `test-workload/README.md` describes a second, larger body of evidence: "when a real coding agent does real work inside a box, does the box let the work through, and does it hold the boundary?" It holds fourteen dimensions and three agents (Claude Code, Codex CLI, a Strands SDK agent), giving 68 cells across Linux and macOS, and it separates verdicts from model calls — "Agent B is not a model call. It reads the artefacts and applies the dimension's rules. A model must not grade its own run." The adversarial `network-egress` case plants canary TCP listeners on 169.254.255.254 ports 80 and 443 and on a free loopback port, each answering with a per-run token, and grades the run as `PASS / CONTAINED`, `FAIL / BREACHED` or `FAIL / INVALID`; the token or the instance's `AccessKeyId` appearing in the transcript is a breach. Its README is candid about coverage: "The canaries test that the policy and the gateway hold; they do not cover every covert channel."

**Threat model the evidence covers.** The suite and the integration cases exercise: direct filesystem reach against the grants the box declares; egress policy on connect and request legs; credential placement, redaction and route binding; MCP tool-call authorization for local and remote servers; native-egress exceptions; history durability across restarts; and the decision record format.

**Threat model the evidence does not cover.** Per `SECURITY.md` and `docs/design/tenets.md`: kernel-exploit resistance is a stated non-goal ("A kernel escape defeats operating system enforcement"), cross-tenant isolation is the hosting platform's responsibility, side channels "never reach operating system enforcement or policy", and resource exhaustion is out of scope. `docs/design/limitations.md` adds what Box cannot do at all: "A box does not limit process creation, CPU, or disk use", and "Box relies on the kernel to enforce the sandbox. An exploit that defeats the kernel defeats the box." It also states that the trusted process's own defects are unprotected, and that a box "does not sign records or chain them together. Anything that can write the records file can edit it afterwards."

**Claims versus code.** Two performance figures in `docs/design/tenets.md` are explicitly not measurements: "Policy enforcement: < 1 ms per decision, locally with no network hop. **This target is asserted but not yet benchmarked.**" The same table lists a < 50 ms sandbox cold-start target and a < 20 MB resident-memory target. The v0.2.2 release notes contain a candid behavioural caveat: "Linux filesystem queries return zero capacity and free-space counts. Programs that interpret those values as a full filesystem can reject operations."

## Limitations

**Stated by the project.** `docs/design/limitations.md` is unusually explicit and is the best available statement of the boundary. Its "Protections Box doesn't provide" list covers the above non-goals and adds: Box "cannot contain a remote service or control what it does with an allowed request"; the trusted components "run outside any sandbox. Their defects have no sandbox protection"; and "A box records every decision it makes, but it does not sign records or chain them together." It also notes that "History is not an audit record and has no tamper evidence" (`docs/design/policy.md`) and that the operation and its recorded outcome "do not commit together".

**A gap the two authorities read differently.** `crates/policy/README.md` states that for the Monty (script) boundary path resolution is lexical — "it closes `.` and `..` and requires an absolute path, but performs no I/O and so does not follow symlinks. With `/workspace/link -> /secret`, a rule permitting `/workspace/*` permits reading `/secret` through the link. Containment — a subtree with no links leading out — is the only control covering this today." `docs/user/security.md` describes the same area from the operator's side and says that when a path goes through a symlink, "policy decides on the link's spelling … The operation is then refused, because Monty acts on the canonical path only." These two sentences describe different outcomes for the same case. The KB maintainers did not resolve the discrepancy and did not execute either path; an evaluation would need to establish which behaviour the code actually produces before any claim about interpreter-level path handling can be made.

**Policy-language limitations.** From `docs/user/security.md`: a broad `fs:read` permit with no path condition reaches `~/.aws` and `~/.ssh`, because "no credential check sits beneath the interpreters"; Box "does not check that the rules of a policy agree with one another"; a rule keyed on `::request` "sees refused attempts too"; and a temporal macro such as `count_within` "loses its accumulated state when the text before the call changes, even by a comment". `docs/design/policy.md` adds that a verdict is only allow or deny — "No rule can pause a request for human approval" — and that "A refusal reveals policy details. It names the component, the reason, and the rule, so a workload can learn the shape of the policy from what fails."

**Where the mediation does not reach.** `docs/user/security.md` and `docs/design/limitations.md` both record that direct filesystem grants in `box.toml` produce no `fs:*` decision and cannot be revoked by a policy refusal, and that a tool's or local MCP server's own file operations produce no policy decision either. `docs/design/limitations.md` tabulates seven configuration choices that widen reach without a per-access decision, including an operator-declared `contain_egress = false` exception on which "its traffic bypasses the gateway and its policy checks", and a program with no tool table that "gets the agent's grants plus the wider reach of a tool's sandbox, and the startup report doesn't show the wider part."

**Platform coverage.** Linux is ARM64-only for the namespace backend; x86-64 Linux is not a published package; the workload suite states "Linux must be arm64 … Linux containment uses the namespace mechanism, and that mechanism is aarch64-only." Tool grammars are experimental, off by default, and their format "can change before 1.0.0".

**No independent security evaluation.** No third-party audit, penetration test or independent replication of containment was found in the inspected files. The repository's own README, release notes and `SECURITY.md` are the maintainers' statements about their own work.

**What an evaluation would need to measure.** Whether a policy denial is enforced at the kernel and gateway boundary and recorded; whether a history rule actually fires across interpreters after a restart; whether the credential phantom is never recoverable from a contained process's memory or environment; whether the decision records survive a hostile write to the records file; and whether the residual process-fork path is bounded in practice — `crates/containment/README.md` records that `process-fork` "is unscoped, and SBPL cannot scope it … a contained process can create processes without limit, and process exhaustion is an unbounded residual."

## Competing approaches

Only alternatives the project's own sources name.

**MicroVM instead of OS sandboxing.** `docs/design/architecture.md`: "Box uses the surrounding OS's sandboxing so the workload can use the operator's existing environment and paths. It does not boot a guest operating system. A microVM would provide stronger isolation, but it would require a separate environment." The tenets table keeps a MicroVM tier as a performance reference.

**Landlock on Linux.** `crates/containment/README.md` records it as considered and rejected because it "expresses no right that denies all network, which is the default mode, so a contained child would keep unrestricted network"; the namespace launcher was built instead.

**Seatbelt on macOS** is used rather than a cross-platform sandbox, with a single checked-in profile file.

**Cedar versus Dogwood.** `docs/design/policy.md` states "Dogwood extends Cedar, a declarative policy language, with temporal rules that use recorded events within a time window", and `crates/policy/README.md` confirms that plain Cedar `permit`/`forbid` text loads unchanged, so a Cedar-only policy is a valid subset.

**Harness-side approval prompts and allowlists.** `docs/design/architecture.md` argues for deciding outside the harness: "A harness may have its own allowlist and approval prompt. Those checks run inside the untrusted agent process and judge tool calls. Box checks the resulting operations in the trusted process, where the agent cannot change the checks."

**Compiled-in cloud-metadata blocking.** `docs/design/policy.md` explicitly rejects a built-in floor ("Cloud metadata protection comes from the operator's policy") in favour of two authored `forbid` rules; the project's own example policies carry them.

**Tool grammars versus raw argument rules.** `docs/user/tool-grammars.md` contrasts a grammar, which reads a whole command line as one action such as `Tool::git::Action::"push"` with effects like `force_push`, against raw-word rules on `shell:spawn`, where "a rule over raw words must list each spelling" — `git push -f`, `git push --force-with-lease`, `git push origin +main`. The grammar feature is experimental.

## Implications

This section is analysis by the KB maintainers, not a claim of the project.

The transferable idea is not "sandbox the agent" but **put the decision outside the agent's reach and give it a memory**. Box's two-tier design — OS grants fixed before the first process starts, policy decisions made in a trusted process — makes the enforcement path auditable in a way that a harness-side allowlist is not. The shared-history design goes further: it makes an *action sequence* the unit of authorization rather than an action, which is the difference between "this agent may read this file" and "this agent may not reach the network after it has read that file".

The second idea worth borrowing is the **fail-closed vocabulary**: an empty policy denies everything, a `forbid` overrides a `permit`, a cap must be a `forbid` because permits compose permissively, and a rule that provably can never fire is refused at load rather than silently enforcing nothing. For teams writing their own policy languages, the load-time refusal of inert rules is the single highest-leverage feature inspected here, because a policy that appears to protect a resource while permitting everything is the most common silent failure mode of declarative authorization.

Third, the **phantom credential** pattern is worth copying even without the rest of the system: the agent holds a placeholder, the trusted boundary holds the secret and substitutes it at the last moment, and the placeholder is matched by value so the gateway can prove the request came through the box's own binding. The documented cost — that every process in the box can use every route, because the gateway cannot tell which process opened a connection — is a real limitation and the project is explicit that a process which must not hold a credential belongs in a separate box.

Fourth, the **refusal transparency** choice is instructive in both directions. Naming the rule that refused an operation makes operator debugging possible and makes the policy shape learnable by a hostile workload. A deployment that wants the second effect prevented would need a two-tier design the project does not have.

Finally, the project's own honesty about its residual risk is a model for this corpus: it publishes, in one file, what its protection does not cover, and it declines to publish performance numbers it has not measured. That discipline is the difference between a security control and a security claim.

## Reproducible experiment

Proposed, not executed by the KB maintainers. Run in a disposable macOS or Linux-ARM64 virtual machine with no credentials of value and no production network path; use a local echo server, not a third-party host.

1. **Does a denial actually deny?** Write a `box.toml` with a narrow `filesystem` grant (one scratch directory) and a `policy.dw` that forbids `fs:read` on one named file in that directory. Have the workload attempt to read that file through each mediated route in turn — the Shell, the Python interpreter, and a direct read that the OS grant would otherwise allow. Pass criterion: every mediated attempt fails, the direct attempt succeeds if and only if the OS grant covers it, and each refusal appears in `<box_dir>/private/telemetry/records.jsonl` with the reason and the rule. A mediated read that succeeds is a boundary failure.
2. **Does the cross-tool history rule fire?** Add a temporal rule that forbids `net:connect` for five minutes after the Python interpreter reads a designated marker file, and a second policy without the rule. Have the workload read the marker and then attempt a request to the local echo server, once with the rule and once without. Pass criterion: the request is refused with the temporal rule under the first policy and permitted under the second, and the refusal is recorded. This tests the feature the README leads with, and it exercises only a local server.
3. **Does the history survive a restart?** Repeat step 2 but restart the box between the read and the request. Pass criterion: the refusal still occurs, because `docs/design/policy.md` states history is durable per box and "that's what stops a restart from resetting a budget". A permission that reappears after a restart is a budget bypass.
4. **Does the phantom stay phantom?** Configure an `env://` route to a local endpoint that echoes the received `Authorization` header, and separately dump the workload's environment. Pass criterion: the echo shows the real secret only on the permitted request, the workload's environment shows only the placeholder, and no copy of the real secret appears in the response the workload receives.
5. **Does the decision record survive a hostile write?** As a separate, clearly destructive sub-test in a disposable VM only, modify the records file after a run and check what the box reports. Pass criterion for the *record's* properties: the project states records are not signed or chained, so the expected result is failure of tamper-evidence — documenting that outcome is the point of the test, and it should be reported as a known limitation rather than a defect.

Report the exact Box version, the OS and architecture, the policy text, the decision records, and the observed outcomes. Do not attempt to escape the sandbox or find a bypass path; the purpose is to confirm enforcement and logging of an ordinary denial, not to probe for weaknesses.

## Evidence status

This page is grounded in reads of the primary source over HTTPS on 2026-11-10: the repository landing page and README (https://github.com/strands-agents/box), the GitHub REST endpoints for the repository metadata (https://api.github.com/repos/strands-agents/box), its releases (https://api.github.com/repos/strands-agents/box/releases) and its full file tree (https://api.github.com/repos/strands-agents/box/git/trees/main?recursive=1); and the following files at `main` under https://raw.githubusercontent.com/strands-agents/box/main/ — `README.md`, `SECURITY.md`, `crates/box/README.md`, `crates/policy/README.md`, `crates/egress-gateway/README.md`, `crates/containment/README.md`, `docs/design/architecture.md`, `docs/design/security.md`, `docs/design/policy.md`, `docs/design/tenets.md`, `docs/design/limitations.md`, `docs/design/credentials.md`, `docs/design/egress.md`, `docs/user/security.md`, `docs/user/tool-grammars.md`, `test-workload/README.md` and `.github/workflows/ci.yml`.

Claim types are separated in the text. Code-inspected facts are the file layout, the action vocabulary, the crate APIs and their documented semantics, the CI job graph, the workload-suite structure and the released version series. Claims are the project's own statements about its security properties, its measured coverage, the workload-suite verdicts and the agent-driven containment results — none of which the KB maintainers verified. The two performance targets in `docs/design/tenets.md` are the project's own and are marked there as unbenchmarked. The Monty path-resolution discrepancy between `crates/policy/README.md` and `docs/user/security.md` is reported unresolved.

Nothing on this page was executed, cloned, built, installed or tested by the KB maintainers; no Box binary was run, no policy was loaded, and no sandbox was entered. No independent security evaluation of Box is known from the inspected files.

## Historical coverage

- [[briefings/2026/11/2026-11-10]] — dated full-fidelity research and cross-project synthesis.
