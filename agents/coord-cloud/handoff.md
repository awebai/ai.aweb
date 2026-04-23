# Coordinator aweb-cloud (Tom) — Handoff

Last updated: 2026-04-23

## Current state

ac is **shipping** at v0.5.3 on main (9249b5b2, clean tree), pinned
`aweb>=1.16.0`. Production is running this tag. No unreleased commits
on main; only remote branch is `aaga-archive`.

**v0.5.4 is on HOLD.** Two P1 tracker tasks block it (see "Release
blockers" below). Do NOT ship while they're open.

Auth-bridge migration from HMAC/API-key to JWT + team certificates is
done: identity-auth messaging, identity/address split, per-membership
addresses all landed (see `status/engineering.md` 2026-04-21 and
`docs/decisions.md` entries through 2026-04-21).

## Release blockers (BOTH block v0.5.4)

**aweb-aakv (P1, NEW 2026-04-23)** — `test_user_revoke_before_rejected_with_db`
in `tests/test_jwt_service.py` fails **in isolation** (not pollution).
Real code or test bug. Investigation suspects handed to dev agent:
  - JWT `iat` claim encoding mismatch (datetime via `additional_claims`
    → jose encoding → decoded shape)
  - `{{tables.jwt_user_revocations}}` template rendering between INSERT
    and SELECT under the test fixture
  - `aweb_cloud_db` fixture persistence across two `JWTService()`
    instances in the same test

**aweb-aakt (P1, NARROWED 2026-04-23)** — 37 cumulative test-ordering
pollution failures in `make test-backend`. Bisect shows NO single
polluter file: running either half alone (files 1-60 or 61-120) plus
a failing target leaves the target passing; only the full 120-file
set reproduces. Pollution is cumulative state, most likely the
session-scoped `aweb_cloud_db` fixture. Fix path: pytest-randomly →
--forked → audit conftest.py session fixture teardown. Dev-agent
territory, not coord.

Dev dispatch: Juan bringing up a builder in the ac repo (same pattern
as Grace in aweb). Coord-cloud role: stay in posture, help reproduce
when a dev claims aakv or aakt.

## Release protocol (LOCKED 2026-04-23, from Juan + Randy)

Every future release from here on, no exceptions:

1. **Per-gate log** — mail Randy one entry per gate as it completes
   (name, exact command, pass/fail/skipped with reason, duration,
   timestamp). Running view, not batched. Stop on a red.
2. **Gates all green** — full `make test-backend` + `make test-frontend`
   + Docker user journey + two-service e2e. Run aggregated, not per-file.
   No workarounds. Docker daemon down = no-go, not defer. If Docker
   stays down with otherwise-ready code, add dated hold note in
   `docs/decisions.md` and wait.
3. **SOT analysis** — after gates green, before tag. Pull
   aweb-sot.md + awid-sot.md + trust-model.md (aweb/docs/), walk the
   user-facing surface, cross-check code↔SOT drift, flag regressions
   from previous tag. Mail findings to Randy (even "nothing found" is
   a finding).
4. **CTO approves in writing** — Randy's explicit go before tag.
5. **Tag + make ship.**

## Dev agents (ephemeral, in the ac repo)

| alias | last seen | host | focus |
|-------|-----------|------|-------|
| bob   | 7d ago     | Mac.c.is       | aakh (stale claim) |
| leo   | 3d ago     | Mac.c.is       | (none)            |
| ivy   | 4d ago     | c.is           | (none)            |
| eve   | 7d ago     | altair.local   | (none)            |

None active right now. `bob`'s claim on aweb-aakh is a week stale —
un-claim on next wake-up if still no movement.

## aweb dependency state (per John, 2026-04-22 + 2026-04-23)

- aweb main is at 05c46b2 + e08b609 post-v1.16.0. aakq.3 AND .4 landed
  in `e08b609`. Remaining in aakq: .5, .6, .7, .8, .9. ETA to 1.17.0
  tag: 24-48h if Grace is hot, per John 2026-04-23.
- 1.17.0 scope: aweb server 1.16.0 → 1.17.0, aw CLI 1.16.0 → 1.17.0,
  @awebai/claude-channel 1.2.0 → 1.3.0. **awid-service stays at 0.4.0.**
- DO NOT bump ac's aweb pin until John mails 1.17.0 is tagged.
- 1.17.0 drops `workspace.yaml.active_team`. ac-side impact: zero
  (audit 2026-04-22 shows ac has no code that reads or writes it).
- Possible detour: if aakq drags 2-4 days, aweb may cut a 1.16.1 patch
  for aaks (P1 server bug in `tasks_service.py:577`). ac would bump
  to 1.16.1 first (v0.5.4 covers that), then 1.17.0 after (v0.5.5).
  If aakq lands in time, single v0.5.4 covers both. Randy will flag
  which path.

## v0.5.4 content (when blockers clear + 1.17.0 tags)

Per Randy 2026-04-23, single commit is preferred:
  - `backend/pyproject.toml`: `aweb>=1.16.0` → `aweb>=1.17.0`
  - `backend/pyproject.toml`: `awid-service>=0.3.1` → `>=0.4.0`
    (pin-hygiene fix — lockfile already resolves 0.4.0, just making
    the stated pin match)
  - `uv lock` from `backend/`
  - Commit: "release: v0.5.4, aweb 1.17.0 + awid-service 0.4.0 deps"

## Migration state on prod (verified 2026-04-22)

Three schemas, single-file layout each, applied 2026-04-20:
  - `server.schema_migrations`:     001_initial.sql  (module aweb-server)
  - `aweb.schema_migrations`:       001_initial.sql  (module aweb-aweb)
  - `aweb_cloud.schema_migrations`: 001_initial.sql  (module aweb_cloud)

On-disk matches. No pending migrations.

`aweb.workspaces` columns on prod (16): workspace_id, team_id,
agent_id, repo_id, alias, human_name, role, hostname, workspace_path,
workspace_type, focus_task_ref, focus_updated_at, last_seen_at,
created_at, updated_at, deleted_at. **No `current_branch`** —
confirmed aweb-aaks P1 is a server code bug, not a migration lag.

## Open branches in ac

- `main` — v0.5.3, shipping.
- `aaga-archive` — remote-only; preserved per Randy.

## Environment watch

Docker daemon on altair.local: **DOWN** as of 2026-04-23. Juan to
decide whether to bring it up or bring it up himself. It's a ship
blocker (Docker user journey is a required gate). If it stays down
at ship time, we wait — no workaround.

## Test-backend state (known to carry hidden isolation debt)

Per Randy 2026-04-23: v0.5.3 shipped without `make test-backend`
running clean aggregated (finding 2 above). That's at least v0.5.3-old.
Product correctness is not implicated (isolated tests pass), but test
infra has fixture-leakage debt. Worth flagging in v0.5.4 SOT analysis
even after the tests are green.

## What to check FIRST on next wake-up

1. Status of aweb-aakv and aweb-aakt — have dev agents claimed?
   Any fixes pushed? Re-run `make test-backend` aggregated when a fix
   lands; report per-gate log to Randy.
2. John's mail for aweb 1.17.0 tagged.
3. Randy's mail on aaks patch path — 1.16.1 patch detour or bundled
   in 1.17.0.
4. Docker daemon status on this host — green-light from Juan to run
   the journey + two-service gates.
5. `bob` stale claim on aweb-aakh.
