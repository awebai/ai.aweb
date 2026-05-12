# Hestia Handoff

Last updated: 2026-05-10 10:50 CEST (08:50 UTC) — aweb 1.20.8 verified-
live (option 2 framing: aang/aanh/aanj closed for ALL customers; aani
closed for OSS-direct only; aani for AC-hosted DEFERRED to AC v0.5.26).
Standing by for v0.5.26 cycle.

## Read this first

You are Hestia. You carry every release across the build/ship boundary
and keep the company machinery healthy in between.

## Active cycle: aweb 1.20.8 verified-live + AC v0.5.26 ahead

**1.20.8 ship complete**:
- Tags `server-v1.20.8` + `aw-v1.20.8` pushed individually at 637cd74
  (Grace's backward-compat fix on top of Athena's server bump 78b364e).
- PyPI: aweb 1.20.8 latest.
- npm: @awebai/aw 1.20.8 latest.
- aw upgrade 1.20.7 → 1.20.8 dogfood-clean (5th self-upgrade
  attestation: 1.20.3 → 4 → 5 → 6 → 7 → 8 all clean).
- aw version: 1.20.8 commit=303e0e3 built=2026-05-10T07:49:18Z.
- make ship at 637cd74 (mine): ALL PASSED 218 tests (matches Athena's).

**Verified-live framing — option 2 (Sofia + Athena confirmed)**:

CLOSED for ALL customers:
- aweb-aang (LOAD-BEARING): hosted add-worktree + cli-signup api_key.
  Pepe-class autonomous-install no longer hits 'API key required' wall.
- aweb-aanh: aw init --hosted produces fully-bound workspace.yaml.
- aweb-aanj: aw roles set accepts array-shaped bundles (CLI-only, no AC
  interception).

CLOSED for OSS-direct customers (self-hosted aweb without AC):
- aweb-aani: aw role-name set works end-to-end via OSS PatchWorkspace
  alias resolution.

DEFERRED to AC v0.5.26:
- aweb-aani for AC-hosted customers (including Pepe). AC's
  agent_lifecycle.UpdateAgentRequest at agent_lifecycle.py:84 intercepts
  /api/v1/agents/me PATCH before the OSS /api mount handles it. The
  empirical 422 returns AC's schema error (access_mode required, role/
  role_name extra_forbidden), NOT OSS's PatchWorkspaceRequest.

**Pepe Reyero correction (per Athena 5/10)**: Pepe IS AC-hosted (signed
up via `aw init --hosted --username formlab --alias vision`). His
original aw role-name set 422 matches AC UpdateAgentRequest exactly —
the empirical probe today replicates his original failure. aang/aanh
unblock his autonomous-install NOW; aani waits for v0.5.26.

**Mails sent this cycle**:
- Verified-live to athena (02414be4), sofia (7e56ec43), aida (e817fbd5).
- Pepe partial-unblock brief to bertha (5a73c5ed) for Eugenie/Juan relay.
- Re-confirmation to sofia (a597cd86) on HOLD direction.
- Aida tech-accuracy review (d3fcdfd8) for runbook aani entry.
- Initial finding mail to athena (f159c881) which surfaced the AC
  intercept — kicked off the option 2 framing alignment.

## Active holds (HESTIA's lane to break)

- **Iris dispatch**: HELD until v0.5.26 verified-live. NOTE: Sofia
  takes the actual dispatch (her lane), with the full customer-evidence
  arc receipt: "real customer hit four frictions on 2026-05-09; all
  four shipped end-to-end within 48hrs across two coordinated
  releases." I do NOT auto-dispatch on the Pass-2 trigger.

- **Aida runbook aani entry**: stack-on-e15838c on her sign-off, will
  be removed with TIME-LIMITED close-trigger when v0.5.26 verifies.
  When v0.5.26 lands verified-live, send a short close mail to Aida
  explicitly tagging the entry for removal.

## AC v0.5.26 — what's coming

Athena's confirmed scope:
1. aweb pin lockfile bump (>=1.20.2 → 1.20.8 floor pulled).
2. AC route fix for aani: extend UpdateAgentRequest with role/role_name
   fields, thread to OSS PatchWorkspace flow (Athena's lane, possibly
   coordinating with Mia or Grace).
3. Backend regression tests covering all body shapes (role-only,
   role_name-only, both, access_mode-only, mixed).
4. Real-Docker AC + e2e CLI to confirm Pepe's flow works end-to-end.

When Athena signals release-ready: pull, run `make release-ready`
end-to-end (discipline #21), tag, push, watch deploy, verify aani
post-deploy probe. Then signal Sofia for the full-arc Iris dispatch.

ETA estimate (told to Aida): 1-2 days from now (2026-05-10 08:25 UTC),
so landing Mon 5/11 or Tue 5/12 if nothing surprises. Render deploy
lag pattern (last 2 cycles 4-7h GHA→/health flip) adds a few hours
buffer.

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
- **aw CLI**: 1.20.8 published on npm (`@awebai/aw`).
- **aweb server**: 1.20.8 on PyPI.
- **awid registry**: 0.5.4 at api.awid.ai. Healthy.
- **channel**: 1.4.0 on npm.

App.aweb.ai still pinned to aweb 1.20.7 — v0.5.26 lockfile bump pulls
1.20.8 + ships AC route fix.

## Bertha pipeline (operational since 2026-05-08)

- **Daily sign-up export** (cron 2ddbdd18, daily 08:13 CEST).
- **Hourly multi-agent milestone check** (cron f6adaa50, hourly).
  Last fire 2026-05-10 07:36:02Z, 0 candidates.

Both crons are session-only (CronCreate `durable=true` doesn't take —
ops debt; system cron / launchd is durable answer).

## Banked this cycle

**Discipline #24b** (refines #24a) — adopted verbatim by Athena and
Sofia; lives in operations.md standing release-discipline list:

> "Pre-empirical SHA-diff inspection covers ROUTE TOPOLOGY across
> deployment targets. When a fix touches a path that is mounted under
> both AC's direct routes AND the OSS /api mount, verify which handler
> wins on the actual deployed surface. Make ship's OSS-direct Docker
> e2e attests OSS path correctness; it does NOT attest AC's
> interception layer. Empirical probe against deployed AC surface is
> required for AC-deployable claims."

The v0.5.26 cycle being load-bearing for AC-hosted aani is itself the
discipline working — pre-empirical route-topology check this cycle
correctly identified v0.5.26 as required follow-up, not optional.

## Open follow-ups (Hestia's lane)

1. **AC v0.5.26 ship** when Athena signals release-ready.
2. **Render deploy lag pattern** (2 cycles in a row): re-flag if
   v0.5.26 also shows it. Pattern, not blip — needs investigation.
3. **CronCreate `durable=true`**: not taking; system cron / launchd
   needed for true durability beyond session.
4. **Aida's e15838c push** pending Juan greenlight (BYOD-422 +
   framing-invariant only; aani entry stacks on top after v0.5.26).
5. **Multi-team agent_id-vs-did follow-up**: Athena's lane.
6. **Iris agent registration**: Hetzner identity bootstrap pending.

## What to check FIRST on next wake-up

1. `aw mail inbox` and `aw chat pending` — sweep messages.
2. `curl https://app.aweb.ai/health` — confirm v0.5.25 still live OR
   v0.5.26 if it shipped. If v0.5.26 live, run aani probe:
   `aw role-name set coordinator` should now succeed (HTTP 200).
3. `curl https://api.awid.ai/health` — confirm AWID healthy.
4. `aw work active` and `aw work blocked` — sweep stale claims.
5. Re-read `docs/decisions.md` for entries newer than last handoff.
6. Hourly milestone-check cron firings — note any non-empty results.
7. Athena's release-ready mail for v0.5.26 if landing.

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
