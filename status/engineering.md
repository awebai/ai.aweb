# Engineering Status
Last updated: 2026-04-23 (Randy, post-1.17.0 ship)

## Current focus

1. **ac v0.5.4 — one blocker left**: aakt (37-test cumulative pollution in `make test-backend`). Mia is on it under Tom's coord. Investigation path: pytest-randomly → conftest.py fixture audit → per-test isolation. Tom reports per-gate log when aakt closes and v0.5.4 sequence runs.
2. **aweb 1.17.0 shipped**. Decision record on main (commit `b98a331` in ai.aweb). Downstream consumers pick up via `npm install -g @awebai/aw@1.17.0`, `@awebai/claude-channel@1.3.0`, and (pending) `ac>=0.5.4`.
3. **Post-ship followups pending your call** (not blocking): aakr (P4 membership-field-overlap design question), branch cleanup (`aweb/beadhub-legacy`, `ac/aaga-archive`).

## aweb OSS — 1.17.0 released

- **Tagged**: `server-v1.17.0`, `aw-v1.17.0` (`cb8f7f5`), `channel-v1.3.0` (`bb668be`). GHA handles npm + pypi publish.
- **Closes in 1.17.0**: aakq (epic — SoT collapse), aakn (team switch drift), aako (address split between identity vs cert), aaku (non-Go consumers of workspace.yaml.active_team), aaks (`aw work active` 500).
- **Breaking change** (release-noted): `aw doctor --json` check id renamed from `local.workspace.active_team` → `local.teams.active_team`. Consumers parsing the old id must update.
- **Gate discipline outcome**: two NO-GO rounds on the first tag attempt (first because aaks wasn't in the release; second because gate Grace's initial aakq.3 broke non-Go consumers in the e2e script and channel plugin). Third pass cleared all gates green. SOT analysis caught the mandatory release-note item that would otherwise have shipped un-announced.
- **Open branches**: `beadhub-legacy` only (intentional archive, pending Juan confirmation).
- **Blockers**: None — product is shipping.

## aweb-cloud (ac) — v0.5.4 in flight

- **Status**: unreleased; blocked on aakt.
- **Landed today**: `2f0c42cc` Fix JWT revocation UTC handling (aweb-aakv — closed).
- **Remaining blocker**: `aweb-aakt` — 37-test cumulative pollution in `make test-backend` aggregate. Pre-existing tech debt exposed by the 2026-04-22 release-gate discipline. Mia is investigating under Tom's coord (pytest-randomly → fixture audit path).
- **Ready once aakt clears**: bump `aweb>=1.17.0`, `awid-service>=0.4.0`; full gate run; CTO approval; tag v0.5.4.
- **Team in ac**: Mia (dev, new), Tom (coord-cloud, reviews).
- **Open branches**: `aaga-archive` only (intentional archive, pending Juan confirmation).

## awid
- Shipped with aweb 1.17.0. awid-service 0.4.0 current. No open work.

## Cross-repo alignment

- ac still pins `aweb>=1.16.0`, `awid-service>=0.3.1`. v0.5.4 bumps both.
- After v0.5.4 ships, ac will pull aweb 1.17.0's aakq fixes + aaks fix to hosted users. Until then, hosted app.aweb.ai runs the prior deployment.

## Concerns

- **aakt is pre-existing tech debt, not a regression**. The gate discipline surfaced it on its first full aggregated run — which is exactly what the discipline is for. Not a process critique; a process win.
- **Route-via-coordinator discipline**: I bypassed John twice today (once on aako fix specifics to Grace, once on aaks dispatch to Grace). Juan caught both. Saved as feedback memory (`feedback_dispatch_via_coordinator.md`). Not a recurring risk — the symptom pattern is now named and catchable.

## Policies standing

- **Release gate** (2026-04-22): full e2e user journey green before any release. SOT analysis required before tag. `make test-e2e` green + CTO written approval + coordinator tag. Per-gate log with name/command/outcome/duration, running view not batched.
- **Review via shared working tree** (2026-04-22): coordinators read dev commits via `git -C <repo>`; no chat-pasted diffs.
- **Route dev-agent dispatch through coordinator** (2026-04-23): when directive names a dev, brief the coordinator, not the dev.

## Next milestones

- Mia + Tom close aakt.
- Tom's v0.5.4 per-gate log + SOT analysis → CTO approval → tag.
- Juan: branch-preservation decision (`beadhub-legacy`, `aaga-archive`); aakr architectural direction when ready.
