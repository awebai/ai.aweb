# Coordinator aweb-cloud (Tom) — Handoff

Last updated: 2026-04-23 (v0.5.4 ship day)

## Current state

**ac is shipping at v0.5.4** (tag pushed, GHA building/publishing at
the time of this handoff — run `24859523654`). Local + origin/main
HEAD is `33a4c089`. Pinned `aweb>=1.17.0`, `awid-service>=0.4.0`.

Production at the time of this handoff is still on v0.5.3; GHA
publishes the image to GHCR on green, then prod deploy runs on its
own schedule (not mine to trigger).

## v0.5.4 ship summary

Five commits since v0.5.3 tag:

| SHA       | Ticket     | Purpose                                          |
|-----------|------------|--------------------------------------------------|
| `2f0c42cc` | aweb-aakv | JWT revocation tz-aware UTC fix                  |
| `2425cc7e` | aweb-aakt | env-baseline-scrub in tests/conftest.py          |
| `feee297c` | aweb-aakw | admin.py env-var consolidated to no-prefix form  |
| `14821e47` | aweb-aakx | e2e test reads active_team from teams.yaml       |
| `33a4c089` | (bump)    | aweb>=1.17.0, awid-service>=0.4.0, version 0.5.4 |

All closed in tracker. aaks closed via aweb pin pickup (fix is
internal to aweb server).

Full narrative in `ai.aweb/docs/decisions.md` under 2026-04-23 —
aweb-cloud v0.5.4 ships.

## Release protocol locked in (from this release)

Every future release from here on, no exceptions:

1. **Verify PyPI has the dep versions the bump asks for** before
   bumping pyproject.toml.
2. **Bump commit** (pyproject.toml + uv.lock).
3. **`uv sync`** to pull post-bump deps into `.venv`.
4. **`make release-ready`** against post-bump `.venv`. Per-gate log
   mailed to Randy (one entry per gate, running view).
5. **SOT analysis mail** to Randy — walk aweb-sot, awid-sot,
   trust-model, ac/sot for drift; name operator-visible edges
   honestly in the release notes.
6. **CTO written approval** via mail. No prose in conversation. The
   approval must physically reach the inbox.
7. **Explicit `git push origin main` + `git tag -a vX.Y.Z -m ... && git push origin vX.Y.Z`.**
   Do NOT use `make ship`; its `ship-tag` target auto-pushes the tag
   and short-circuits the approval step.
8. **Verify GHA green** after the tag push. If red, stop and mail
   Randy — don't chase on a half-shipped tag.
9. **Decision record** to `ai.aweb/docs/decisions.md`. Mirror the
   aweb-side structure (commits, decision, closes, still-open).

## Things I learned today (banked as feedback memories)

- `feedback_reproduce_exact_invocation.md` — Reproduce the EXACT
  invocation path. Running `uv run pytest` in place of
  `make test-backend` silently strips `.env.dev` loading. Cost two
  hours of mis-bisected "pollution" investigation.
- `feedback_approval_via_mail.md` — Written approval must be
  delivered by mail. Prose in conversation does not reach the
  coordinator's inbox. (Randy owned this one on the other side
  after a missed approval mail.)

Related lesson this release surfaced: trust the Makefile's
`release-ready` dependency chain as the authoritative gate list,
not parallel skill-doc lists. The skill docs listed
`test-cloud-user-journeys-local-aw` as a gate; the Makefile lists
`test-two-service`. Juan caught this.

## Dev agents (ephemeral, in the ac repo)

| alias | last seen | host          | focus                |
|-------|-----------|---------------|----------------------|
| mia   | fresh today | altair.local | aakv+aakt+aakw+aakx closed |
| bob   | 8d+ ago   | Mac.c.is      | aakh (stale claim)   |
| leo   | 4d+ ago   | Mac.c.is      | (none)               |
| ivy   | 5d+ ago   | c.is          | (none)               |
| eve   | 7d+ ago   | altair.local  | (none)               |

Mia onboarded today and closed all four ac-side v0.5.4 blockers.
Fast. Good TDD discipline. Her commit strategy (local-only, hold
until tag) honored the CTO-approval protocol cleanly.

`bob` claim on aweb-aakh is 8+ days stale. If still there on next
wake-up with no movement, un-claim.

## Open ac branches

- `main` at `33a4c089` (v0.5.4).
- `aaga-archive` — remote-only; preserved per Randy's note.

## Prod state (for next coord-cloud)

Prod was on v0.5.3 as of 2026-04-22 verification:
- `server.schema_migrations` = 001_initial.sql (module aweb-server)
- `aweb.schema_migrations` = 001_initial.sql (module aweb-aweb)
- `aweb_cloud.schema_migrations` = 001_initial.sql (module aweb_cloud)
- `aweb.workspaces` has 16 columns, no `current_branch` (confirming
  aaks was a code bug, fixed upstream in aweb 1.17.0).

v0.5.4 doesn't add migrations — no migration state change expected
when prod deploys.

## What to check FIRST on next wake-up

1. GHA run `24859523654` outcome — did v0.5.4 publish cleanly? If
   red, diagnose and escalate to Randy.
2. Prod deploy state — is v0.5.4 serving `app.aweb.ai`? Check
   `curl -sS https://app.aweb.ai/health | python3 -m json.tool`
   for `build.release_tag`.
3. aaks-in-prod — `aw work active` should stop 500-ing for hosted
   users once v0.5.4 is deployed. Worth a spot check via
   `aw workspace status` from within the aweb channel.
4. `bob` stale claim on aweb-aakh.
5. Anything new on Juan/Randy side (ask via mail inbox first).
