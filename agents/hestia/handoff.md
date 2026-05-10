# Hestia Handoff

Last updated: 2026-05-10 09:42 CEST (07:42 UTC) — aweb 1.20.8 mid-flight,
Athena bless-and-run received (mail 1b5171ea), make ship started in
background at 637cd74.

## Read this first

You are Hestia. You carry every release across the build/ship boundary
and keep the company machinery healthy in between.

## Active release: aweb 1.20.8 (server + CLI bundle)

**Mid-flight, gate running.** Athena dispatched bless-and-run mail
1b5171ea at 2026-05-10 ~07:38Z confirming her own `make ship` green at
637cd74 with 218 tests including:
- TestInitHostedThenAddWorktreeTwiceUsesStoredWorkspaceAPIKey (aang.3)
- TestRoleNameSetPatchesCurrentWorkspace (Grace's compat coverage —
  both current-server role_name response + legacy 1.20.7 role response)
- Full Phase 0-22 e2e against awid + aweb in Docker

**My gate**: kicked off `make ship` in background (bash ID `bc6hxydzp`,
log `/tmp/aweb-ship-1.20.8-637cd74-hestia.log`). Per discipline #21
(bless-and-run = run FULL chain end-to-end yourself, not shortcut).
Expected ~30-40 min.

### Layered shape (A)+(B), pre-empirical caught via #24a

- (A) **78b364e**: server bump 1.20.7 → 1.20.8, `PatchWorkspaceRequest`
  accepts both `role` and `role_name` with model-validator-driven alias
  resolution.
- (B) **637cd74**: Grace's CLI backward-compat fix — sends BOTH `Role`
  + `RoleName` so any server version accepts. Plus agent-guide doc
  corrections.

The pre-empirical SHA-diff inspection (discipline #24a, banked this
cycle) caught the misclassification: Athena initially framed 1.20.8
as CLI-only #27a, but the diff revealed d3dfb4b modifies
`server/src/aweb/routes/agents.py` with new `role_name` field that
older servers silently drop. Hestia pushed back with two-path mail;
Athena layered (A)+(B).

### Bundle content (four P0 fixes closing Pepe Reyero's case)

1. **aang (LOAD-BEARING)** — hosted add-worktree no longer needs
   dashboard API key. CLI persists workspace-bound `api_key` from
   cli-signup response. Paired with AC v0.5.25's addd3332 (already
   deployed-live).
2. **aanh** — `aw init --hosted` produces fully-bound
   `.aw/workspace.yaml` in single invocation (folded into aang).
3. **aani** — `aw role-name set` wire alignment (server adds
   role_name field with role↔role_name aliases via model_validator;
   CLI sends BOTH per Grace's 637cd74).
4. **aanj** — `aw roles set` accepts array-shaped bundles (no Go
   internals leak).

### Tag plan (when my make ship lands green)

- Tag both `server-v1.20.8` + `aw-v1.20.8` at 637cd74
- Push individually per discipline #7 (no batched tag push)
- Watch GHA workflows fire (server PyPI publish + aw npm publish)
- Verified-live probes (Athena's spec):
  - aamy auto-update from 1.20.7 → 1.20.8 in my workspace
    (5th self-upgrade attestation)
  - `aw role-name set` against deployed v0.5.25 (1.20.7 server) —
    should SUCCEED via backward-compat (CLI sends Role field which
    1.20.7 reads). Positive verification per Mia's recommendation.

### Sequencing

1. aweb 1.20.8 ships now (Pepe unblocks on npm publish).
2. AC v0.5.26 follows: ping Athena when PyPI 1.20.8 publishes; she
   preps lockfile bump + commit, runs release-ready, bless-and-runs.
3. AC v0.5.26 deploys → aani fix reaches prod → end-to-end closure.

### Sign-offs collected

- Sofia: signed off via mail 9144385c — bug-fix shape, no framing
  review needed; Pass-2 trigger gated on aweb 1.20.8 verified-live +
  npm reachable.
- Mia + Grace + Athena: all signed off via the sequence walked.
- Aida brief noted: aani silent-drop window technically eliminated
  by Grace's backward-compat fix (defense-in-depth only).

## Identity (live since 2026-05-01 21:05 UTC)

- did: `did:key:z6MkebRpF7qEFNt5vAYa5BWjegFk1igt6mRESqWb5r3kp9AK`
- stable: `did:aw:3fC4cfvFuVAxZCWyJNRCoUxHVAim`
- address: `aweb.ai/hestia` (reachability=nobody)
- active team: `default:aweb.ai`

## What's live (verified 2026-05-10 07:38:54Z)

- **ac**: v0.5.25 at app.aweb.ai,
  git_sha=`77e60e5bdf7566e2c712cef8cb6462341cdb6ede`,
  aweb_version=1.20.7, awid_service_version=0.5.4. Started
  2026-05-10T07:07:11Z.
- **aw CLI**: 1.20.7 published on npm (`@awebai/aw`).
- **aweb server**: 1.20.7 on PyPI.
- **awid registry**: 0.5.4 at api.awid.ai. Healthy.
- **channel**: 1.4.0 on npm.

## Bertha pipeline (operational since 2026-05-08)

- **Daily sign-up export** (cron 2ddbdd18, daily 08:13 CEST): mail to
  Bertha with prior-26h sign-up batch + multi-agent activity status.
- **Hourly multi-agent milestone check** (cron f6adaa50, hourly):
  state-tracked, alerts Bertha on first-cross. Last fire 2026-05-10
  07:36:02Z, 0 candidates. State file initialized empty 2026-05-08.

Both crons are session-only (CronCreate `durable=true` did not take —
ops debt; system cron / launchd is durable answer).

## Open follow-ups (Hestia's lane)

1. **Render deploy lag** (2 cycles in a row): v0.5.24 GHA→live ~4h,
   v0.5.25 ~7h vs historical ~3min. Pattern, not blip. Investigate
   when bandwidth permits — Render image-watcher poll? Upgrade
   window?
2. **CronCreate `durable=true`**: not taking; system cron / launchd
   needed for durable scheduling beyond session.
3. **Aida's runbook push (e15838c)**: pending Juan greenlight —
   BYOD-422 + framing-invariant only.
4. **Iris agent registration**: Hetzner identity bootstrap pending.
5. **Multi-team agent_id-vs-did follow-up**: Athena's lane.
6. **Brief Bertha** (when 1.20.8 verified-live): Pepe Reyero's
   autonomous-install case unblocked.
7. **Pass-2 trigger to Iris** (when 1.20.8 verified-live + npm
   reachable + aw upgrade works): Sofia's precise trigger.

## What to check FIRST on next wake-up

1. `aw mail inbox` and `aw chat pending` — sweep messages.
2. Background bash `bc6hxydzp` — check make ship status. If green,
   proceed with tag + push. If failed, share failure shape with
   Athena and work the fix together.
3. `curl https://app.aweb.ai/health` and `https://api.awid.ai/health`
   — confirm v0.5.25 still live (or v0.5.26 if AC follow-up shipped).
4. `aw work active` and `aw work blocked` — sweep stale claims.
5. Re-read `docs/decisions.md` for entries newer than last handoff.
6. Hourly milestone-check cron firings (every :07 — or whatever
   schedule matches; check CronList).

## Banked through 2026-05-10

Standing release-discipline through #28 + #24a (pre-empirical
SHA-diff inspection of release framing) + #27a (CLI-only release
pattern). Full list lives in `../../status/operations.md` under
"Standing release-discipline".

## Sibling repo symlinks under this dir

- `aweb` → `../../../aweb` (run gates here for aweb releases)
- `ac` → `../../../ac` (run gates here for ac releases)

Prefer `git -C aweb log` over `cd aweb && git log`. Do NOT run
`aw` from sibling repos. Read sibling repos to run gates and
verify what shipped; do NOT edit code there (Athena's surface).

## Note on git author attribution

Commits authored by dev-team members (Mia / Grace et al.) appear
as "Juan Reyero" in `git log`. The actual agent identity is
carried via the aweb cert. Grace's 637cd74 = dev-team agent.
