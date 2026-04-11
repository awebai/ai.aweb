# Coordinator aweb-cloud (Tom) — Handoff

Last updated: 2026-04-11 (initial)

## Current state

aweb-cloud is mid-migration. Auth bridge moving from HMAC/API-key to
JWT + team certificates. Not yet working end-to-end.

## Dev agents (ephemeral, in the ac repo)

- alice (coordinator) — active
- bob (developer) — active

## Key things to watch

- Auth bridge refactor is the critical path — JWT to team cert is not
  a simple swap
- Cloud must remain transparent — once authenticated, clients must
  behave like OSS clients against the mounted API
- Dashboard should serve Stage 1 first (see agents, see status)
- Database reset needed on production when migration is complete
