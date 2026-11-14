---
uid: b6a90402-a8d1-4d13-9a40-000000000012
title: "CUA AgentEnv"
summary: "Cua's AgentEnv plugin for macOS VMs: a lume sandbox provider plus cua-driver and three benchmark-arm drivers for computer-use tasks."
type: project
created: 2026-11-09
updated: 2026-11-10
depth: deep
related: [capability-locus, structural-constraint-over-instruction, verified-completion-vs-apparent-success]
sources:
  - https://github.com/trycua/cua/pull/6405
  - https://github.com/trycua/cua/pull/6407
  - https://api.github.com/repos/trycua/cua/pulls/6405
  - https://api.github.com/repos/trycua/cua/pulls/6407
  - https://api.github.com/repos/trycua/cua/pulls/6405/files
  - https://api.github.com/repos/trycua/cua/pulls/6407/files
  - https://raw.githubusercontent.com/trycua/cua/feat/agentenv-macos-plugin/libs/python/agentenv-cua/README.md
  - https://raw.githubusercontent.com/trycua/cua/feat/agentenv-macos-plugin/libs/python/agentenv-cua/pyproject.toml
  - https://raw.githubusercontent.com/trycua/cua/feat/agentenv-macos-plugin/libs/python/agentenv-cua/src/agentenv_cua/lume/provider.py
  - https://raw.githubusercontent.com/trycua/cua/feat/agentenv-macos-plugin/libs/python/agentenv-cua/src/agentenv_cua/drivers/cua_driver_macos/driver.py
  - https://raw.githubusercontent.com/trycua/cua/feat/agentenv-macos-plugin/libs/python/agentenv-cua/src/agentenv_cua/drivers/cua_driver_macos/env.toml
  - https://raw.githubusercontent.com/trycua/cua/feat/agentenv-macos-plugin/libs/python/agentenv-cua/image/provision.sh
  - https://raw.githubusercontent.com/trycua/cua/feat/agentenv-macos-plugin/libs/python/agentenv-cua/smoke/conformance_smoke.py
  - https://raw.githubusercontent.com/trycua/cua/feat/agentenv-macos-plugin/libs/python/agentenv-cua/tests/test_lume_provider.py
  - https://raw.githubusercontent.com/trycua/cua/feat/agentenv-macos-drivers/libs/python/agentenv-cua/README.md
  - https://raw.githubusercontent.com/trycua/cua/feat/agentenv-macos-drivers/libs/python/agentenv-cua/pyproject.toml
  - https://raw.githubusercontent.com/trycua/cua/feat/agentenv-macos-drivers/libs/python/agentenv-cua/src/agentenv_cua/macos-drivers/envs/agent-desktop/macos_computer.py
  - https://raw.githubusercontent.com/trycua/cua/feat/agentenv-macos-drivers/libs/python/agentenv-cua/src/agentenv_cua/macos-drivers/envs/codex-cu/driver.py
  - https://raw.githubusercontent.com/trycua/cua/feat/agentenv-macos-drivers/libs/python/agentenv_cua/src/agentenv_cua/macos-apps/envs/bench-sentinel/sentinel.py
  - https://raw.githubusercontent.com/trycua/cua/feat/agentenv-macos-drivers/libs/python/agentenv-cua/src/agentenv_cua/macos-apps/artifacts/sentinel-macos/run.py
---

# CUA AgentEnv

## What it is

CUA AgentEnv is a Python package, `agentenv-cua`, that plugs into the AgentEnv framework (github.com/scaleapi/agentenv-framework) to run computer-use agent tasks inside macOS virtual machines. It lives inside the `trycua/cua` repository — 32,144 stars, 2,404 forks, MIT licensed, primarily Rust, with a project home at cua.ai — and is developed by a collaborator account, `f-trycua`.

The package's own metadata (`pyproject.toml` on the PR head branch) declares version `0.1.0`, licence MIT, `Development Status :: 3 - Alpha`, `Operating System :: MacOS`, Python 3.11 or 3.12, and a single runtime dependency, `agentenv-framework>=0.9.1425,<0.10`. It registers two AgentEnv entry points: a sandbox provider `lume` bound to `agentenv_cua.lume.provider:LumeSandboxProvider`, and two bundles, `macos-drivers` and `macos-apps`.

The work is delivered as **two stacked, still-open draft pull requests** against `trycua/cua`, both authored by `f-trycua` and both created on 2026-11-03:

- **PR #6405**, "feat(agentenv-cua): AgentEnv plugin for macOS VMs (lume provider, cua-driver macOS driver)", opened 2026-11-03T19:10:21Z, 4 commits, 18 changed files, +11,261 lines, base `main` (27a7f878), head branch `feat/agentenv-macos-plugin` (f2d6f653). `draft: true`, `merged: false`, `mergeable_state: unstable`.
- **PR #6407**, "feat(agentenv-cua): other macOS arms' drivers and the bench's macOS apps (stacked on #6405)", opened 2026-11-03T19:38:18Z, 4 commits, 60 changed files, +11,245/−4, base `feat/agentenv-macos-plugin`, head branch `feat/agentenv-macos-drivers` (51c96bed). Also `draft: true`, `merged: false`.

The package README states the status plainly: "**Status: draft, in progress.** It's being built so that Cua Driver Bench runs on AgentEnv on macOS, the same way it already runs on Linux." PR #6405 says the same: "**Status: draft**".

## Mechanism

Files inspected on the PR head branches: `libs/python/agentenv-cua/README.md` (both PRs), `pyproject.toml`, `src/agentenv_cua/lume/provider.py`, `src/agentenv_cua/drivers/cua_driver_macos/driver.py`, `src/agentenv_cua/drivers/cua_driver_macos/env.toml`, `image/provision.sh`, `smoke/conformance_smoke.py`, `tests/test_lume_provider.py`, `src/agentenv_cua/macos-drivers/envs/agent-desktop/macos_computer.py`, `src/agentenv_cua/macos-drivers/envs/codex-cu/driver.py`, `src/agentenv_cua/macos-apps/envs/bench-sentinel/sentinel.py`, `src/agentenv_cua/macos-apps/artifacts/sentinel-macos/run.py`, plus the two PR metadata endpoints and their changed-file lists.

**The isolation boundary is a macOS VM, not a container.** `provider.py` documents the provider as "macOS VMs on this Mac, run by lume" and defines `PLATFORM = "darwin/arm64"`. Each sandbox is a clone of a pinned base image, booted headless through Cua's own `lume` CLI wrapper. The isolation is therefore the guest OS itself: the agent's desktop, its filesystem and its credentials live inside a virtual machine, and the host Mac runs the driver-side control plane.

**How the guest is configured.** The provider writes the computer's boot settings — driver settings, app settings and a control token — to a JSON file on the host at `~/.agentenv/lume/<name>/agentenv/boot.json`. The directory is created with mode `0o700` and the file with mode `0o600`; `test_lume_provider.py` asserts `boot.stat().st_mode & 0o077 == 0`. The file is then shared into the guest **read-only**, at `/Volumes/My Shared Files/agentenv/boot.json`, via `lume run --detach --shared-dir <dir>:ro`. The README explains the analogy: "This is how a Linux disk form reads its NoCloud seed."

**The credential path.** The boot settings carry the control token, and the guest reads it through the shared directory rather than through an environment variable baked into an image. The provider's `_write_boot` puts the whole settings blob behind a `0600` file in a `0700` directory, and the guest sees it read-only.

**What is inside the guest.** `image/provision.sh` is the in-guest setup script and is specific about what it installs: CuaDriver.app 0.38.0 from the cua-driver release, sha256-verified against `5f71191c082ca07c9dfc13b7c9a6eec60a82818c245a93534cc0eb7911471d72` for the tarball and `b4d974a9c1c92a700cd7be7ede987aea4a1e6835e37039ce3d628b71bd5f0ca8` for the executable inside the bundle; the driver at `/opt/agentenv/drivers/cua-driver` with a venv holding `agentenv-framework-protocol[computer]==0.1.440`; **TCC rows for Accessibility, Screen Capture and PostEvent written directly into `/Library/Application Support/com.apple.TCC/TCC.db`** for the bundle id `com.trycua.driver`, keyed by the app's designated requirement; a recorded screen-capture approval in `ScreenCaptureApprovals.plist`; and two LaunchAgents that start the daemon and the driver in the GUI session. The script refuses to proceed unless it is on Darwin/arm64 and unless `csrutil status` shows SIP disabled, stating "SIP must be off in the VM to seed TCC rows". It also disables the base image's Cua Spacesd window and the login-item banner, because those overlays cover the parts of the screen an agent's clicks would land on.

**The driver.** `drivers/cua_driver_macos/driver.py` declares a `ComputerDriverEnvironment` subclass annotated `@computer_driver(name="cua-driver", supports=[{"os": {"type": "macos"}, "arch": ["arm64"]}])`. It talks to the cua-driver daemon over a Unix socket at `~/Library/Caches/agentenv/cua-driver.sock`, in a directory the daemon creates with mode `0o700`, and it reads requests and writes replies as newline-delimited JSON. The daemon is launched with `--dangerously-bypass-approvals --no-overlay`; the module docstring explains why: "with approvals off (nobody is at the computer to give them) and nothing sent to trycua", with `DO_NOT_TRACK=1`, `CUA_DRIVER_RS_TELEMETRY_ENABLED=false` and `CUA_DRIVER_RS_UPDATE_CHECK=false` in its environment.

**Ready checks are the enforcement surface of the driver.** The driver verifies three things: the sha256 of the pinned executable, the pinned tool list against a committed `mcp.json` (9,125 lines for the cua-driver driver), and the TCC grants — checked *every* time, not once, "so a lost grant shows up as a harness error rather than an agent failure". `tool_list_check` names exactly which tools differ when the running daemon's list does not match the pin; `permissions_check` lists the ungranted permissions and says "the image's TCC rows don't match this CuaDriver.app". The driver's `_pinned_checks` are cached once they pass, while the permission check is recomputed each time.

**Pointer and session handling.** The computer has one pointer, guarded by an `asyncio.Lock`, and pointer actions are delivered with `delivery_mode = "foreground"`, because "a headless computer has nobody whose pointer it could disturb". The drag implementation parks the pointer on the start point and settles 0.2 s before pressing, because "an app reads the pointer's place when it handles the press, not where the press happened".

**The other three benchmark arms (PR #6407).** `macos-drivers/` adds `agent-desktop` (Vercel's CLI, version 1.0.2, 67 derived tools), `macos-harness` (browser-use's macOS harness 0.2.1, eleven tools) and `codex-cu` (OpenAI's `unified-computer-use` plugin `cua_repl` server from ChatGPT app 26.930.51102, exposing `js` and `js_reset`). Each keeps its own pinned version, ready checks and tool manifest, and each runs with the same agent so that "only the tool layer changes".

**The neutral `computer_*` helper.** `macos_computer.py` serves the seven `computer/v1` operations from `/usr/sbin/screencapture` and Quartz events (`CGEventPost`), because "AgentEnv wants the seven operations from every driver, and no arm owns this one". Each env hides it from its agent with its `[tools]` list, "so each arm is scored on its own tools only". The same file is duplicated in each driver's folder "since a driver installs from its own folder; a test checks that".

**The bench apps (PR #6407).** `macos-apps/` ports the bench's own macOS applications from the public Bench v2 in `libs/cua-driver-bench`, each pinned by URL and sha256 in a `files.json`: `benchlab` (an AppKit test bench built from three Swift sources, data in `~/.benchlab`), `bench-sentinel` (a window that "plays the user and logs what disturbs them", data in `~/.bench-sentinel/sentinel.jsonl`), and `cdb-s02` to `cdb-s04` (the shared tasks' windows, opened per each task's `platform/launch.macos.json`).

**The sentinel as a witness.** `bench-sentinel/sentinel.py` starts the app with either the foreground witness condition or the background "User activity" window, and `artifacts/sentinel-macos/run.py` arms and disarms it around the agent: arming "empties the clipboard and activates the sentinel until a sample says its window is active and key, then arms it", and arming fails unless the log says the sentinel armed *and* the window was active and key. The app's own ready check requires a `start` line and a sample in the log.

**Reset semantics.** `reset_vm` deletes the clone and clones the source again under the same name and MAC address, restoring the MAC from the previous VM's `config.json` so lume's DHCP hands back the same address. If the address changes, the provider raises "its URLs would change". The same reset path re-checks the display size (`lume set --display` before the first boot) and re-writes the boot settings, which is why the TCC grants have to be re-checked after every reset.

**Host capacity and egress.** Apple's licence allows two macOS VMs per Mac, so `MAX_RUNNING_PER_HOST = 2` and `create_vm` refuses a third, counting VMs another lume instance is running. `create_vm` refuses a restricted-egress network policy outright with the message "the lume provider can't restrict a macOS VM's egress" — a deliberate refusal rather than an approximation. `create_sandbox` raises `NotImplementedError` because "a lume sandbox is a macOS computer, not an agent's container; run agents on a container provider such as `local`".

## Evidence

**Code-inspected facts.** The provider, driver, image-provisioning, sentinel and app-enablement code above was read directly, together with the offline test file `tests/test_lume_provider.py`, which exercises the provider against a fake lume with no Mac and no VM. Those tests assert concrete properties: the shared directory is passed with `:ro`, the boot file is mode `0600`, the display size is set before the first boot and after a reset, a third running VM is refused with "2 macOS VMs already run", a reset re-clones under the same name and MAC so the URL stays, `terminate` deletes only what the provider made, a failed boot leaves no VM behind, a registry image is pulled exactly once into a local base, `exec` runs over lume's ssh as the image's user, a restricted-egress network policy is refused, and a VM another lume instance runs counts against the limit.

**The change footprint.** PR #6405 adds 18 files: the plugin README, `image/build.sh`, `image/provision.sh`, `image/set-display.swift`, `pyproject.toml`, `smoke/conformance_smoke.py`, the `lume` provider and CLI, the cua-driver macOS driver with its 9,125-line `mcp.json` manifest and `pin_manifest.py`, the driver's `env.toml` and `requirements.txt`, and two offline test files. PR #6407 modifies the README and `pyproject.toml`, adds `image/build-arms.sh`, `image/provision-arms.sh` and `image/install_app.py`, and adds the three arm drivers, the bench apps, the sentinel artifact and four new test modules (`test_agent_desktop.py`, `test_codex_cu.py`, `test_macos_apps.py`, `test_macos_computer.py`, `test_macos_harness.py`).

**Claims made by the pull-request descriptions — not verified by the KB maintainers.** PR #6405 states: "Offline tests pass: 20 tests, with a fake lume and no daemon. `agent-env plugin check` reports the `lume` provider active on agentenv-framework 0.9.1425", and, in the same status block, "**Not yet run on a macOS VM.**" PR #6407 states: "120 offline tests pass (`pytest`), ruff clean on the new files", and that `agent-env plugin check` passes with "13 contributions in effect", and that BenchLab and BenchSentinel were checked to compile on a Mac. No CI run, log, or coverage report for these PRs was inspected; the only automated comment on either PR is a Codecov bot post stating "All modified and coverable lines are covered by tests", which is a coverage summary about the diff and not a functional result.

**What the smoke test would establish.** `smoke/conformance_smoke.py` boots one VM through the provider, waits for the driver's card at `/.well-known/agent-env.json`, runs AgentEnv's computer conformance probe, makes one `get_screen_size` tool call, then resets the VM and repeats the probe at the `basic` level. Its exit codes are fixed: 0 when every check passed, 1 when one failed, 2 when the computer never got ready. The PR states this smoke path has not been run on a macOS VM.

**Threat model the evidence covers.** Guest isolation from the host filesystem and the operator's own session; a single controlled desktop per task, so an agent's misdirected clicks land in a disposable guest rather than on a real desktop; per-task credential scoping through the boot settings file rather than a baked-in image secret; and driver-level drift detection through pinned executable hashes and pinned tool manifests.

**Threat model the evidence does not cover.** Nothing inspected measures what happens when an agent deliberately attempts to escape or subvert the guest, and the driver is explicitly launched with `--dangerously-bypass-approvals`, so the daemon itself will not ask for confirmation. The permission model inside the guest is macOS TCC, seeded by writing directly into `TCC.db` with SIP disabled; the code shows the rows being created, not any adversarial test of them. The provider cannot restrict the VM's egress and says so. There is no independent evaluation of the plugin in the inspected files.

## Limitations

**Stated by the pull requests.** Both PRs are drafts, unmerged, and neither has been run on a macOS VM. PR #6405's status block lists the dependency that blocks core integration: "Core accepts only `os.type = \"linux\"` computers in `container` or `disk` form. A macOS computer needs `os.type = \"macos\"` and a prebuilt VM-image form, which we're coordinating with the AgentEnv maintainers. Until then, `install.macos` in `env.toml` is documentation and `provision.sh` does the install." PR #6407 repeats this: "`install.macos` is still not accepted by core, so the new envs carry no install table; the app envs name placeholder `computer`/`driver` ids until the macOS computer lands (core or the plugin stopgap)." The README's "What's missing" section lists the same three gaps.

**Platform and conformance gaps named by the sources.** The README records that the conformance fixture is X11-specific in four checks: `P6 typed text arrives as key events` expects Tk's X11 keysym `comma` where macOS reports `,`; `P6 a chord selects all` and `P6 a repeated key` use Ctrl+/ where macOS selects all with Cmd+A; and `P7 scrolls ... each arrive` counts X11 wheel buttons 4 and 5 where macOS reports MouseWheel events. "They need a platform-aware fixture in the probe, not changes here." The macOS 15+ one-time direct-capture consent is handled by pre-recording it in the image, and the README states cua-driver "skips captures (`direct_capture_consent_required`) until that answer is recorded". The image also needs a full-tier base: `provision.sh` fails with "the base must be ghcr.io/trycua/macos:26 (full tier)" if `uv` or `swiftc` is missing.

**Prerequisites that are not in the repository.** A ChatGPT account is needed inside the VM for the Codex arm; the driver "needs a ChatGPT login inside the VM. It is an explicit precondition", the ready check runs `codex login status` every time and fails with instructions until it holds, and "an image with the login is private". Apple's licence caps the host at two macOS VMs, which is a throughput limit on any evaluation that wants many concurrent macOS cells.

**Single-host scope.** The provider is declared `ON_THIS_MACHINE = True` and `native_platforms()` returns only `darwin/arm64`. The image depends on `ghcr.io/trycua/macos:26`, a base the plugin does not own.

**Documentation-versus-code gaps.** PR #6407 notes that "The Electron DevTools-opening hook the Linux port logs for the GUI-only check isn't ported (it is not in the public Bench v2 code)", so the macOS port has one fewer observable than the Linux one. The `env.toml` files for the app envs name `computer = "macos-26"` and `driver = "cua-driver-macos"`, which PR #6407 calls placeholders. The `driver.py` for cua-driver and the `provision.sh` script hold the same constants in two places — `EXECUTABLE_SHA256` in the driver and `APP_EXECUTABLE_SHA256` in the script — and the two are equal in the inspected versions; nothing inspected enforces that they stay equal.

**What an evaluation would need to measure.** Whether a task that damages the guest leaves the host untouched; whether a reset really restores a clean, same-address desktop and whether the TCC grants survive it; whether the driver's pinned-tool check fires when the underlying tool changes; whether the driver's own `--dangerously-bypass-approvals` mode introduces a difference the conformance probe does not detect; and whether the sentinel witness behaves identically in the foreground and background conditions.

## Competing approaches

Only alternatives the sources name.

**Running the same bench on Linux.** PR #6405 states the purpose is "the first step toward Cua Driver Bench running on AgentEnv on macOS, the way it already runs on Linux", and the README links the existing Linux port at github.com/earakely-scale/agentenv-cua-driver-bench. The macOS plugin is the counterpart of AgentEnv's Linux `cua-driver` driver.

**AgentEnv core's own computer forms.** The core composes Linux computers in `container` or `disk` form; the plugin's approach is a prebuilt VM-image form booted through `create_vm`, which core does not yet accept.

**The three third-party arms** the plugin wraps rather than reimplements: Vercel's `agent-desktop` (Apache-2.0, a CLI with no MCP server), `browser-use/macos-harness` (MIT, eleven shell commands), and OpenAI's `unified-computer-use` plugin's `cua_repl` MCP server (ChatGPT app 26.930.51102), which the driver runs "unchanged, as the plugin's own `.mcp.json` starts it, except that only the `computer` surface is on (no browser)".

**The neutral helper versus per-arm tooling.** `macos_computer.py` is offered as the alternative to each arm owning the `computer_*` operations: "neither belongs to any arm".

**Two capture mechanisms.** The cua-driver arm captures through the driver's own MCP server, while the neutral helper captures through `/usr/sbin/screencapture`.

## Implications

This section is analysis by the KB maintainers, not a claim of the PR authors.

The transferable pattern is **making the disposable environment a first-class harness artefact**. The provider treats "clone, boot, configure, reset to a known state at the same address" as a provider API, not as scripting. Two details are worth stealing: restoring the MAC address so the sandbox's URLs survive a reset, and refusing a reset that changes the address rather than papering over it. For any evaluation harness that hands a model a computer, address stability is what makes transcripts comparable across runs.

Second, the **ready-check-as-enforcement pattern** is the most transferable idea here. The driver refuses to be used unless its executable hash, its tool manifest and its OS permission grants all match expectations, and it distinguishes "pinned once" from "checked every time" — because a reset can silently lose a permission and turn every subsequent agent action into a silent failure. Turning environment drift into a named, failing check rather than into a mysterious agent error is a genuinely good harness practice, and the failure messages are specific enough to act on.

Third, the **decision to refuse a capability rather than approximate it** deserves attention. When AgentEnv asks for a restricted-egress network policy, the provider raises rather than silently running an unrestricted VM, and `create_sandbox` refuses outright because a macOS VM is not an agent container. Both refusals are correct, and both cost the project functionality. A team adopting VM-backed agents should decide in advance which approximations are acceptable, because the temptation to accept "close enough" is strongest exactly where the guarantee is hardest to test.

Fourth, the **`--dangerously-bypass-approvals` daemon** is the sharpest security trade-off in the inspected code, and it is well reasoned for the setting: a headless guest has nobody to approve an action, so an approval prompt would mean no desktop automation at all. But it means the *guest* is the only boundary; everything inside it, including any software the agent installs, runs without human confirmation. A deployment that needs an in-guest stop signal must supply one — the sentinel is an example of a witness, not a brake.

Finally, the honesty of the draft status is itself informative. Both PR bodies carry an explicit "not yet run on a macOS VM" line and a named list of what core still blocks, and the README's "What's missing" section reads like a plan rather than a pitch. For a KB, the practical consequence is that this page describes a proposal with inspected code, not a shipped capability: the merge state, the AgentEnv core dependency and the absence of any on-VM run are the three facts that would need to change before the page's framing could.

## Reproducible experiment

Proposed, not executed by the KB maintainers. Run on a disposable Apple-silicon Mac with a spare VM slot, using only the plugin's own offline fixtures and a locally built base image; do not use a shared CI host.

1. **Does the provider behave as documented without a Mac?** Run the offline suite the PR describes — `pip install -e '.[test]'` then `pytest` in `libs/python/agentenv-cua` — and check that the tests pass with a fake lume and no daemon. Pass criterion: the suite is green and the file count matches the PR's claim (20 tests in #6405, 120 in #6407) or the difference is explained by the stacked PR. This establishes the offline contract only.
2. **Does a real VM boot, reset and stay at the same address?** On the disposable Mac, build the image with `image/build.sh` and boot one sandbox through the provider. Run the smoke script `smoke/conformance_smoke.py --base <name> --level full`. Pass criterion: the VM boots, the driver's card answers, the conformance probe at `full` level passes, a `get_screen_size` call returns a size, and after `reset_vm` the URL is unchanged, the driver comes back ready, and the `basic`-level probe passes. Record the exact guest OS build, the base image digest and the driver version.
3. **Do the ready checks actually fire?** Two benign negative controls. First, run the driver in a guest whose `CuaDriver.app` is not the pinned build and confirm the ready check fails with the "its executable's sha256 is …, not the pinned …" message rather than proceeding. Second, confirm the permission ready check fails with a message naming the ungranted permission when the TCC rows are absent. Pass criterion: both checks fail closed with a named reason and no tool call succeeds.
4. **Does a reset actually restore a clean desktop?** Write a marker file inside the guest, reset the sandbox, and confirm the marker is gone, the address is unchanged, and the driver's permission check still passes. Pass criterion: the file is absent, the address matches, and the check passes — which is the concrete form of the claim that a reset gives a clean machine.
5. **What does the conformance probe not cover on macOS?** Run the full probe and record exactly which of the four X11-specific checks fail, and whether the driver's own `capture` ready check reports a working capture. The PR predicts specific failures; measuring them confirms whether the fixture is the problem or the driver is.

Report the versions of lume, cua-driver, `agentenv-framework`, `agentenv-framework-protocol` and the guest OS build, plus the probe report as JSON. Do not attempt to escape the guest, and do not attempt to defeat the TCC rows: the purpose is to confirm that the documented checks fire and that a reset restores a known state.

## Evidence status

This page is grounded in reads of the two primary sources over HTTPS on 2026-11-10: the pull-request metadata and changed-file listings (https://api.github.com/repos/trycua/cua/pulls/6405, https://api.github.com/repos/trycua/cua/pulls/6407, and their `/files` endpoints), the two PR landing pages (https://github.com/trycua/cua/pull/6405 and https://github.com/trycua/cua/pull/6407), and, at the PR head branches, the files `libs/python/agentenv-cua/README.md` (on both `feat/agentenv-macos-plugin` and `feat/agentenv-macos-drivers`), `pyproject.toml`, `src/agentenv_cua/lume/provider.py`, `src/agentenv_cua/drivers/cua_driver_macos/driver.py`, `src/agentenv_cua/drivers/cua_driver_macos/env.toml`, `image/provision.sh`, `smoke/conformance_smoke.py`, `tests/test_lume_provider.py`, `src/agentenv_cua/macos-drivers/envs/agent-desktop/macos_computer.py`, `src/agentenv_cua/macos-drivers/envs/codex-cu/driver.py`, `src/agentenv_cua/macos-apps/envs/bench-sentinel/sentinel.py` and `src/agentenv_cua/macos-apps/artifacts/sentinel-macos/run.py`.

Claim types are separated in the text. Code-inspected facts are the provider's semantics, the driver's ready checks and pins, the guest provisioning steps, the sentinel's arming logic, the package metadata and the offline test assertions. Claims are the PR authors' own statements — the 20 and 120 offline test counts, the `agent-env plugin check` results, the compilation check on a Mac, and the "not yet run on a macOS VM" status — none of which the KB maintainers verified; the only automated artifact inspected on either PR is a Codecov coverage comment, which is not a functional result. The Xcode-level environment facts of the guest (TCC rows, SIP, screen-capture consent) are read from the provisioning script, which shows what the script does, not that it ran. The whole of Implications is analysis by the KB maintainers.

Nothing on this page was executed, cloned, built or tested by the KB maintainers; no macOS VM was booted, no image was built, no test suite was run, and no pull request was merged. Both pull requests were open drafts at the time of inspection, and the plugin is not released as a merged capability.

## Historical coverage

- [[briefings/2026/11/2026-11-04]] — dated full-fidelity research and cross-project synthesis.
- [[domains/computer-and-device-use]] — application context this project serves.
- [[projects/browser4]] — analyst-level **compares_with** on the browser-automation axis, not a verified dependency.
- [[evaluations/briefing-synthesis-2026-11-03-to-09]] — cross-project synthesis covering this record.
