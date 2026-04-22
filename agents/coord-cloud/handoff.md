# Coordinator aweb-cloud (Tom) — Handoff

Last updated: 2026-04-22

## Current state

ac is **shipping** at v0.5.3 on main (9249b5b2, clean tree), pinned
`aweb>=1.16.0`. Production is running this tag, DB migration layout
matches disk (see below). No unreleased commits on main; no active
branches other than the preserved `aaga-archive`.

Auth-bridge migration from HMAC/API-key to JWT + team certificates
that the pre-2026-04-11 handoff called out as mid-migration is done:
identity-auth messaging, identity/address split, per-membership
addresses all landed (see `status/engineering.md` 2026-04-21 and
`docs/decisions.md` entries through 2026-04-21).

## Dev agents (ephemeral, in the ac repo)

| alias | last seen | host | focus |
|-------|-----------|------|-------|
| bob   | 6d ago     | Mac.c.is       | aakh (stale claim) |
| leo   | 2d ago     | Mac.c.is       | (none)            |
| ivy   | 3d ago     | c.is           | (none)            |
| eve   | 6d ago     | altair.local   | (none)            |

None are active right now. `bob`'s claim on aweb-aakh is 2d+ stale —
watch on next wake-up; if still stale, message him or un-claim.

## Release policy (NEW 2026-04-22, from Juan)

No release of anything (aweb or ac) without the full e2e user-journey
test passing. For ac, that means `make test-backend` +
`make test-frontend` + e2e journey (docker) must all be green before
cutting any tag. John mailed me about this; apply on every future ac
release.

## aweb dependency state (per John, 2026-04-22)

- aweb main is at 05c46b2 post-v1.16.0. Commits 05c46b2 / fcbcc00 /
  9e97b40 are NOT going to a 1.16.1; they're queued for aweb 1.17.0
  with the rest of `aweb-aakq` (.3–.7, .9). Expect 1.17.0 over the
  next few days, not today.
- DO NOT bump ac's aweb pin to 1.17.0 until John explicitly mails.
- 1.17.0 drops `workspace.yaml.active_team`. **ac-side impact: zero.**
  Audit 2026-04-22 shows ac backend has no code that reads or writes
  `active_team`. Only references to `workspace.yaml` in ac are two
  user-facing error strings in `routers/oss_workspaces.py` and one
  explanatory sentence in `frontend/.../ByoitIdentitySetupFlow.tsx` —
  all still accurate post-1.17.0.

## Pin hygiene issue (minor, non-blocking)

`backend/pyproject.toml` pins `awid-service>=0.3.1` while the v0.5.3
commit message and Randy's `status/engineering.md` both claim
`awid-service>=0.4.0`. Lockfile resolves 0.4.0 correctly (pulled in
transitively by aweb 1.16.0), so runtime is fine, but the stated pin
is weaker than reality. If we cut a v0.5.4 for any reason, tighten the
pin to `>=0.4.0` in the same commit.

## Open branches in ac

- `main` — v0.5.3, shipping.
- `aaga-archive` — remote-only; preserved per Randy's note.
  `frank-docs` already deleted (pricing landed via main).

## Migration state on prod (verified 2026-04-22 for Randy's aaks diagnosis)

Three schemas, single-file layout each, applied 2026-04-20:
  - `server.schema_migrations`:     001_initial.sql  (module aweb-server)
  - `aweb.schema_migrations`:       001_initial.sql  (module aweb-aweb)
  - `aweb_cloud.schema_migrations`: 001_initial.sql  (module aweb_cloud)

On-disk matches. No pending migrations. The "001–018" file list in
older notes is stale — the 0.5.0 collapse commit (9e9b42c1) folded
everything into per-schema `001_initial.sql`.

`aweb.workspaces` columns on prod (16): workspace_id, team_id,
agent_id, repo_id, alias, human_name, role, hostname, workspace_path,
workspace_type, focus_task_ref, focus_updated_at, last_seen_at,
created_at, updated_at, deleted_at. No `current_branch` — confirmed
the aweb-aaks P1 is a server code bug (selecting a column that never
existed), not a migration lag.

## Unresolved (pending Juan)

- Verify-only vs. cut v0.5.4: v0.5.3 is live and clean; nothing new
  on main since the tag. Waiting on Juan to say whether to (a) just
  run the full gate against main to re-certify v0.5.3 or (b) cut a
  v0.5.4 that tightens the awid-service pin. Leaning (a) — pin fix
  alone doesn't justify a release per YAGNI.

## What to check FIRST on next wake-up

1. Juan's direction on the verify-only vs. v0.5.4 question above.
2. John's mail for aweb 1.17.0 tagged — at that point, cut an ac
   release with the bumped aweb pin.
3. Randy's aweb-aaks fix landing — once dispatched, the
   `aw work active` 500 should clear; watch for a follow-up.
4. `bob` stale claim on aweb-aakh — if still 2d+, message him or
   un-claim.
