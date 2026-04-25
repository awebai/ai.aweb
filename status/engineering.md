# Engineering Status
Last updated: 2026-04-25 (Randy, post-aala launch)

## Current focus

1. **aala epic shipped end-to-end.** aweb 1.18.1 + aw CLI 1.18.1 + @awebai/claude-channel 1.3.1 + awid-service 0.5.1 (PyPI + npm) + ac v0.5.5 (GHCR) all live as of 2026-04-25. BYOIT cross-machine team join + multi-membership flow works in production. Closes the user-visible aakn/aako/aakz arc that started with Amy's 2026-04-21 multi-team activation.
2. **Tracker hygiene mid-pass.** Coord audit (John + Tom) closed 12 tasks. My converging pass on John's verdict found two P0 epics (aaiu + aaja) had architecturally shipped but were missed by his commit-message-grep methodology — endpoints/code exist, just commits never named the task IDs. Their epics stay open pending end-to-end test subtasks (aaiu.5, aaja.6, aaja.7) which are real-still-open work but smaller scope than the architectural fixes themselves.
3. **aweb-aaks discipline paid out.** The release-gate process caught the 1.18.0 batch-tag-push ghost-publish failure before users discovered it. Recovery via 1.18.1 with aajs + aakk extensions worked first try.

## aweb OSS — 1.18.1 shipped
- **Tags**: server-v1.18.1, aw-v1.18.1 (b0b2b27), channel-v1.3.1 (5b6a5ce), awid-v0.5.1, awid-service-v0.5.1. All 5 GHA workflows fired clean (vs 0 on the 1.18.0 batch attempt). PyPI + npm live.
- **Closes**: aala epic (BYOIT cross-machine + multi-team membership), aakz (multi-membership mail 409, superseded by aala.7), aajs (BYOD wizard identity lifetime), aakk (task-claim dashboard event publishing).
- **Ghost tag**: server-v1.18.0 et al. exist on origin but never published — kept as audit history per decisions.md 2026-04-25 entry. 1.18.1 is the actually-published version.
- **Open branches**: `beadhub-legacy` only (intentional archive).
- **Blockers**: none.

## aweb-cloud (ac) — v0.5.5 shipped
- **Tag**: v0.5.5 (bc35ce5a). GHA run 24933534665 success in 13m54s. GHCR publish completed.
- **Three commits v0.5.4 → v0.5.5**: feee297c (aakw, v0.5.4 work; included in framing) + bc35ce5a (bump) + 343f40f8 (aala.10 split-stack e2e) + eb8e388d (aala.10 docs/UI). Actual v0.5.5 delta is the latter three on top of v0.5.4.
- **Pins**: aweb>=1.18.1, awid-service>=0.5.1.
- **Open branches**: none. aaga-archive deleted earlier.
- **Blockers**: none.

## awid
- 0.5.1 shipped with aweb 1.18.1. Live on PyPI. No open work.

## Cross-repo alignment
- ac pins: aweb>=1.18.1, awid-service>=0.5.1 — aligned.
- Decision records up to date: aakq/aweb-1.17.0 (2026-04-23), ac-v0.5.4 (2026-04-23), aweb-1.18.1 + aakq+aakk recovery (2026-04-25), aala/v0.5.5 (pending Tom).

## Concerns
- **End-to-end test gaps for shipped P0 features**. aaiu.5 (hosted onboarding e2e), aaja.6 (cross-repo Docker e2e for hosted MCP OAuth verified mail), aaja.7 (signing-path unification) all open. Same regression-coverage gap class as aaks (latent SQL bug shipped 2026-03-27, surfaced 2026-04-22). The architectural fixes are in production; the regression-prevention tests aren't. Ranked next-priority post-aala launch.
- **aais epic + 9 subtasks (Align aweb.ai site)**. Pending Charlene/Avi audit pass — site/ walk-through territory, not coord-aweb's lane. I haven't routed yet; will after launch settles.
- **aajv (P1, ac dashboard lifecycle bypasses OSS mutation hooks)**. Re-opened during converging pass — ac/backend has 10+ direct UPDATE statements against aweb.agents and aweb.workspaces in lifecycle paths (agent_lifecycle.py:573/:794, etc.). Pin-bump made the OSS mutation-hook adapter AVAILABLE; doesn't prove ac is USING it. Pre-existing tech debt, not aala-induced. Needs explicit ac code audit when there's bandwidth.
- **aakr (P4) + aaky (P3) + aalb (P3) + aalc (P2)** are filed and tracked. Not blocking anything.

## Policies standing
- Release gate (2026-04-22): full e2e + SOT analysis + CTO written-and-mailed approval before tag.
- Review via shared working tree (2026-04-22): coordinators read commits via `git -C <repo>`.
- Route dev-agent dispatch through coordinator (2026-04-23): dev dispatch goes via John/Tom/Goto.
- Trust the Makefile's release-ready chain (2026-04-23): release gate list comes from `make release-ready` deps.
- Written approval via mail (2026-04-23): "GO" is not GO until `aw mail send --to <approvee>` has fired.
- Use prohibition language explicitly when redirecting devs (2026-04-25, John's): name the repo prohibition; state lane owner.
- Push release tags individually (2026-04-25): batch push causes GHA event-coalesce; tag-triggered workflows don't fire.
- Tracker audit needs symptom-check (2026-04-25): ID-grep alone misses fixes that landed without naming the task.

## Next milestones
- Tom commits v0.5.5 decision record entry to ai.aweb/docs/decisions.md.
- aaiu.5 + aaja.6 + aaja.7 dispatch when Juan/Avi prioritize post-launch.
- aais epic routing to Charlene/Avi.
- aajv ac code audit when bandwidth surfaces.
- Watch period for any latent aakq/aaks-class bugs surfacing under real load.
