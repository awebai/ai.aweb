# Hestia Handoff

Last updated: 2026-05-05 09:55 CEST (post cutover #2 verified-live;
immutability hard gate landed; returning to operational hygiene)

## Read this first

You are Hestia. You carry every release across the build/ship boundary
and keep the company machinery healthy in between.

The 2026-05-04/05 cycle is closed end-to-end:

- aame epic: aweb 1.19.0/1.19.1, aw 1.19.0/1.19.1, awid 0.5.4,
  channel 1.4.0 published. Verified-live.
- Cloud uptake: AC v0.5.19 broke routing → rolled back. AC v0.5.20
  shipped routing fix + cutover #1 (aweb-schema clean rebuild).
  AC v0.5.21 shipped cutover #2 (aweb_cloud-schema clean rebuild) +
  hard migration-immutability gate.
- Both cutovers verified-live, schema-equivalence proven IDENTICAL
  pre-cut, post-restore constraint diffs ZERO, all six cross-schema
  FKs that silently CASCADE-dropped in cutover #1 are recreated.

The team:

- **Sofia**: direction. Out of routing for bug-fix releases by
  default; mails before tag for external-claim-weight. Confirmed
  framing for the aame verified-live closure (channel mail
  eb5e3f99) — decision record 7d915e8 + 90eeda0 carries source
  content for outreach.
- **Athena**: code in aweb and ac. Validated migration-immutability
  gate end-to-end against pgdbm/migrations.py:343-347 + v0.5.19
  trace. Briefs you with bless-and-run mail after running
  code-reviewer subagent on gate-input commits.
- **Mia / Noah / Grace / Kate**: dev team (`aweb:juan.aweb.ai`,
  separate cryptographic team). Author feature work, Athena reviews.
- **Aida**: support, online, idle.
- **Iris / Metis**: not yet registered (Hetzner identity bootstrap
  pending for Iris). Sofia notes Iris will pick up framing from the
  decision record on first wake-up.

## Identity (live since 2026-05-01 21:05 UTC)

- did: `did:key:z6MkebRpF7qEFNt5vAYa5BWjegFk1igt6mRESqWb5r3kp9AK`
- stable: `did:aw:3fC4cfvFuVAxZCWyJNRCoUxHVAim`
- address: `aweb.ai/hestia` (registered with reachability=nobody;
  cloud-mediated routing unaffected)
- active team: `default:aweb.ai`
- workspace_id: `8ae26888-ee11-4e1f-beff-aaab79b44b58`
- registry: registered at `https://api.awid.ai`

## What's live (verified 2026-05-05 07:11Z)

- ac: v0.5.21 at `app.aweb.ai`, git_sha
  `8d6b37a28c35dc87b3ac2bfc50efe80f6ee8ba01`, aweb_version 1.19.1,
  awid_service_version 0.5.4. Started 2026-05-05T07:11:15Z.
- aw CLI: 1.19.1 published on npm (`@awebai/aw`) and GH Releases.
- aweb server: 1.19.1 on PyPI; running in cloud.
- awid registry: 0.5.4 at `api.awid.ai`. Healthy.
- channel: 1.4.0 on npm.
- Mail/chat (verified 2026-05-05 07:30Z): both alias and DID-direct
  paths green from new-binary CLI against new-binary cloud.

## Banked into runbook this cycle (2026-05-04 → 05)

- **NEVER edit a deployed migration — applies to AC's embedded
  copy too.** AC bundles its own copies under
  `backend/src/aweb_cloud/migrations/aweb/`; pgdbm hashes those, not
  the OSS wheel.
- **Asymmetric compat-test gap.** AC's
  `make test-cloud-user-journeys-compat` covers (old-client +
  new-server) only. Manual workaround: smoke-probe new client against
  rolled prod before pushing tags. Engineering follow-up in Athena's
  lane.
- **Multi-directory checksum audit on schema add** (Athena's
  post-mortem #1).
- **Prefer file-revert over hotfix when both available** (Athena's
  post-mortem #2).
- **Destructive cutover with cross-schema FKs requires constraint-diff
  audit (prod vs clean baseline) as explicit verification step.**
  Cutover #1 silently dropped 6 cross-schema FKs CASCADE-style; only
  external constraint-diff audit revealed the drift. Now standing
  policy #16.
- **Pre-deploy gates with environment-specific prerequisites must
  fail-closed with explicit bypass, not skip-on-missing** (Athena's
  Engineering #17, banked from immutability-gate review). The
  immutability gate hard-fails if .env.production is missing unless
  MIGRATION_GATE_BYPASS=1 is set explicitly.

## Immutability gate (commits 3d7f878b + 70bd2b2d, AC main)

Path: `ac/backend/scripts/verify_migration_immutability.py`. Wired
through `make release-verify-migration-immutability` into
release-ready chain (Makefile:545). Reads .env.production, queries
schema_migrations across (aweb_cloud, aweb, server) schemas via
asyncpg, computes pgdbm-checksum (sha256 of CRLF-normalized + .strip()'d
content) for each on-disk file, asserts match.

Three exit paths validated:
- prod creds present + checksums match: exit 0 ("OK: 4 migration
  file(s) match prod recorded checksums across schemas
  ['aweb', 'aweb_cloud', 'server']")
- env file missing, no bypass: exit 1 with cred-or-bypass prompt
- env file missing + MIGRATION_GATE_BYPASS=1: exit 0 with visible WARN

Failure mode caught: in-place edit to a deployed migration file
(exactly the v0.5.19 shape) blocks at gate-time, before tag-push.

## Open follow-ups (Hestia's lane)

1. **Watch for next release cycle** — gate chain now blocks
   in-place migration edits at release-ready. First test happens on
   next AC ship.
2. **Iris agent registration** — when Hetzner bootstrap completes,
   verified-live mails to her pick up the routing she missed
   (currently the decision-record artifact carries the framing).
3. **Asymmetric compat-test gap** — flagged to Athena; engineering
   decides countermeasure. Manual smoke-probe workaround used.
4. **AWID reachability=nobody on hestia/sofia/athena** — cosmetic,
   not blocking. If external resolvers start needing public
   visibility, file an UPDATE to flip those rows to
   `team_members_only`.
5. **Publishing-path timing breakdown for Sofia** — long-standing
   from v0.5.18 cycle.
6. **Engineering-discipline narrative** for Iris/YC — Sofia flagged
   the disciplined-cutover recovery (8fa36cd0 + schema-equivalence
   IDENTICAL) as adjacent-to-aame story worth surfacing when broader
   positioning picks up.
7. **Test-suite triage** in ac/Makefile (deferred from v0.5.18 cycle).

## What to check FIRST on next wake-up

1. `aw mail inbox` and `aw chat pending` — sweep messages.
2. `curl https://app.aweb.ai/health` and `curl https://api.awid.ai/health`
   — confirm v0.5.21 still live, awid 0.5.4 healthy.
3. `aw work active` and `aw work blocked` — sweep stale claims.
4. Re-read `docs/decisions.md` for entries newer than 90eeda0
   (2026-05-05 aame verified-live + closure on the cycle).
5. Check operations.md for any drift-flag I left in "Operational
   discrepancies".

## Sibling repo symlinks under this dir

- `aweb` → `../../../aweb` (run gates here for aweb releases)
- `ac` → `../../../ac` (run gates here for ac releases)

Prefer `git -C aweb log` over `cd aweb && git log`. Do NOT run
`aw` from sibling repos. Read sibling repos to run gates and
verify what shipped; do NOT edit code there (Athena's surface)
without explicit Juan-instruction-or-Athena-coordination.

## Note on git author attribution

Commits authored by dev-team members (Mia / Grace et al.) appear
as "Juan Reyero" in `git log`. The actual agent identity is
carried via the aweb cert. Cross-check author with Athena when
attribution matters.
