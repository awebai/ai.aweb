# Engineering Status
Last updated: 2026-04-23 (Randy)

## Current focus

1. **aakq epic in flight** (P1) — Grace implementing, John reviewing. .1, .2, .3, .4 shipped on main. Remaining: .5 (remove applyTeamStateToWorkspaceCache), .6 (doctor migration), .7 (e2e regression against Phase 12d), .8 (coordinated 1.17.0 release, gated by full e2e green per 2026-04-22 policy), .9 (follow-up: surface cert-load errors). ETA 2-4 days based on Grace's pace.
2. **aweb-aaks (P1, live prod bug)** — `aw work active` returns 500 on app.aweb.ai. Root cause diagnosed (tasks_service.py:577 selects `w.current_branch`, column never existed in any migration). Tom verified prod matches disk; it's a code bug, not migration drift. Fix is mechanical (~15 min) and needs dispatch — either bundled into aweb 1.17.0 (if aakq closes within days) or shipped as aweb 1.16.1 patch if aakq drags.
3. **Cross-repo pin hygiene for v0.5.4** — ac currently pins `aweb>=1.16.0, awid-service>=0.3.1`. Needs `aweb>=1.17.0, awid-service>=0.4.0` in v0.5.4. Tom owns the bump, scheduled to follow aweb 1.17.0 tag.

## aweb OSS
- **Status**: Shipping. v1.16.0 server + CLI, awid-service v0.4.0.
- **In flight**: aakq subtasks .5, .6, .7, .9 (Grace); aaks fix (undispatched).
- **Recent commits on main since 2026-04-21**:
  - `fcbcc00` fix(channel): prefer cert member address (aakq.1 closed)
  - `05c46b2` fix(cli): prefer cert member address in selection (aakq.2 closed; also fixed a latent helpers.go sanitization bug surfaced by .2)
  - `e08b609` refactor(cli): move active team selection to teams state (aakq.3/.4 closed; migration bridge preserved, filepath.ToSlash fix)
- **Release history since 2026-04-11**: 1.11.0 → 1.16.0 across six server minors + awid 0.3.0, 0.3.1, 0.4.0. All detailed in `docs/decisions.md`.
- **Open branches on remote**: `beadhub-legacy` only (intentional archive, pending Juan call).
- **Blockers**: None for aakq progress. aaks needs a dispatch decision.

## aweb-cloud (ac)
- **Status**: Shipping. v0.5.3.
- **Actual pins**: `aweb>=1.16.0`, `awid-service>=0.3.1`. (Corrected 2026-04-23 after Tom flagged — earlier version of this doc claimed awid>=0.4.0, which was wrong. aweb ships 0.4.0 now, but ac hasn't tightened its dep pin yet. The tighten is part of v0.5.4.)
- **Next release**: v0.5.4 — bump aweb pin to >=1.17.0, tighten awid-service pin to >=0.4.0. Tom is coord, has baseline-gated v0.5.3 before the 1.17.0 pressure, will ship v0.5.4 when aakq.8 tags aweb 1.17.0.
- **Migrations on disk**: single `001_initial.sql` per schema (server, aweb, aweb_cloud) — post-collapse layout after commit `9e9b42c1` (0.5.0). Prod matches disk; Tom verified via read-only check (2026-04-23) that prod has the collapsed layout applied cleanly.
- **Open branches on remote**: `aaga-archive` only (intentional archive, pending Juan call). `frank-docs` was deleted 2026-04-22.
- **Blockers**: Waiting on aweb 1.17.0 tag for v0.5.4 bump.

## awid
- Shipped under aweb repo. awid-service 0.4.0 current, matches what aweb server/CLI ship together. See aweb OSS above.

## Cross-repo alignment
- 2026-04-18 decisions (identity/address split, idempotent address registration, resume-from-partial bootstrap, Replace/Archive multi-address policy) all landed on both sides.
- 2026-04-21 per-membership address model (aakq surfaced two latent bugs from it: aakn and aako, now being fixed in aakq).
- ac's aweb dep pin will match aweb 1.17.0 once v0.5.4 bumps (Tom's plan).

## Concerns
- **aaks is live in production** — every authenticated user with active claims hits the 500 on `aw work active`. Fix is 15 minutes of server code + a test. Waiting on dispatch decision.
- **Process health good** — Grace, John, Tom all running, reviewing, escalating cleanly. 2+2 loop functioning (Grace and John independently caught the migration break in aakq.3/.4). Tom caught a pin-hygiene mismatch I'd put in this very doc. That's the discipline working.
- **Branch preservation**: `aweb/beadhub-legacy` and `ac/aaga-archive` still pending Juan confirmation on delete vs keep. Not urgent.

## Policies standing

- **Release gate** (2026-04-22 decision): no release of anything without full e2e user journey green. `make test-e2e` in aweb; equivalent gates in ac. No workarounds. Tom is baseline-gating v0.5.3 now to certify the test env under the new policy before the 1.17.0 pressure.
- **Review via shared working tree** (2026-04-22): coordinators read dev commits directly via `git -C <repo>`; no chat-pasted diffs.

## Next milestones

- Dispatch aaks fix (today).
- Grace closes aakq.5, .6, .7, .9 (next 2-3 days).
- Grace + John close aakq.8 (aweb 1.17.0 release, after all gates green).
- Tom ships ac v0.5.4 (after aweb 1.17.0 tags).
- Decide on preserved branches (beadhub-legacy, aaga-archive).
