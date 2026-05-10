# Operations Status

Last updated: 2026-05-10 10:25 CEST (08:25 UTC) — aweb 1.20.8 verified-
live (option 2 framing: aang/aanh/aanj closed for ALL customers,
aani closed for OSS-direct only; aani for AC-hosted DEFERRED to AC
v0.5.26). Verified-live mails sent to athena (02414be4) + sofia
(7e56ec43) + aida (e817fbd5). Bertha brief (5a73c5ed) sent for
Pepe partial-unblock.

## Current focus

**aweb 1.20.8 verified-live (option 2 framing)**

CLOSED for ALL customers:
- aweb-aang (LOAD-BEARING): hosted add-worktree + cli-signup api_key
  persistence chain. Paired with AC v0.5.25's addd3332 already
  deployed-live. Pepe-class autonomous-install no longer hits the
  'API key required' wall after init --hosted.
- aweb-aanh: aw init --hosted produces fully-bound workspace.yaml in
  single invocation (folded into aang).
- aweb-aanj: aw roles set accepts array-shaped bundles. CLI-only,
  hits team-roles endpoints not agent_lifecycle — no AC interception.

CLOSED for OSS-direct customers only:
- aweb-aani for self-hosted aweb (no AC layer). CLI sends both role +
  role_name; OSS PatchWorkspaceRequest at server-v1.20.8 has
  model_validator alias resolution.

DEFERRED to AC v0.5.26 (AC-hosted customers including Pepe):
- aweb-aani end-to-end against AC. AC's agent_lifecycle.router PATCH
  /{agent_id} (UpdateAgentRequest with access_mode required, role/
  role_name extra_forbidden) intercepts /api/v1/agents/me before the
  mounted OSS aweb_app at /api can handle it. Athena's confirmed v0.5.26
  scope: lockfile bump + AC route fix (extend UpdateAgentRequest with
  role/role_name fields, thread to OSS PatchWorkspace flow OR delegate
  the role surface to OSS keeping access_mode locally — unified handler
  cleanest).

**Pepe Reyero's case** — partial unblock: aang/aanh closed (his
original autonomous-install blocker, the 'add-worktree wants API key'
wall). aani's 422 on `aw role-name set` still landing for him until
AC v0.5.26 ships. Bertha briefed (mail 5a73c5ed) so Eugenie/Juan can
follow up with him precisely. Per Athena's correction: Pepe IS
AC-hosted (signed up via `aw init --hosted --username formlab --alias
vision`); his original 422 shape matches AC UpdateAgentRequest exactly
— my probe replicates his original failure.

**Empirical evidence chain**:
- make ship 637cd74: ALL PASSED 218 tests (matches Athena's run; same
  pass count, same test list).
- Tags pushed individually per #7: server-v1.20.8 (17s) + aw-v1.20.8
  (11s).
- awebai/aw mirror 'aw Release': 3m8s success (matches historical
  baseline 3m1s-3m13s).
- PyPI: aweb 1.20.8 latest, in releases.
- npm: @awebai/aw 1.20.8 latest, in versions.
- aamy auto-update banner detected v1.20.7 → v1.20.8 (5th self-
  upgrade attestation: 1.20.3 → 4 → 5 → 6 → 7 → 8 all dogfood-clean).
- aw upgrade v1.20.7 → v1.20.8 clean. Post-upgrade banner suppressed.
- aw version: 1.20.8 commit=303e0e3 built=2026-05-10T07:49:18Z.

**Empirical probe — aani against deployed v0.5.25** (1.20.7 server):
```
$ aw role-name set coordinator
setting role name: aweb: http 422: {"detail":[
  {"type":"missing","loc":["body","access_mode"],"msg":"Field required",
   "input":{"role_name":"coordinator","role":"coordinator"}},
  {"type":"extra_forbidden","loc":["body","role_name"]},
  {"type":"extra_forbidden","loc":["body","role"]}
]}
```
That's AC's UpdateAgentRequest schema (`access_mode: str = Field(...,
min_length=1, max_length=64)`, `model_config = ConfigDict(extra="forbid")`)
at `ac/backend/src/aweb_cloud/routers/agent_lifecycle.py:84-92`. Direct
curl against `app.aweb.ai/api/v1/agents/me` confirms — interception
is at AC, not awid or middleware.

## Iris Pass-2 trigger — HELD

Sofia's precise trigger (mail earlier): "1.20.8 verified-live + npm
reachable + aw upgrade works". All three met for aang/aanh/aanj.
Asked Sofia (mail 7e56ec43) whether the aani-AC partial coverage
changes the trigger framing — holding Iris dispatch until she calls.

## Live state (verified 2026-05-10 07:38:54Z)

- `app.aweb.ai/health`: `release_tag=v0.5.25`, `aweb_version=1.20.7`,
  `awid_service_version=0.5.4`. Started 2026-05-10T07:07:11Z.
- `api.awid.ai/health`: `version=0.5.4`, redis/db/schema healthy.

Pre-1.20.8: AC v0.5.25, aweb 1.20.7, AWID 0.5.4. Post-1.20.8 PyPI/npm
reachable, deployed surface (app.aweb.ai) still pinned to 1.20.7
pending v0.5.26 lockfile bump.

## Live state (verified 2026-05-10 07:38:54Z)

- `app.aweb.ai/health`: `release_tag=v0.5.25`, `aweb_version=1.20.7`,
  `awid_service_version=0.5.4`,
  `git_sha=77e60e5bdf7566e2c712cef8cb6462341cdb6ede`. Started
  2026-05-10T07:07:11Z (uptime ~31 min).
- `api.awid.ai/health`: `version=0.5.4`, redis/db/schema healthy.

## Recent verified-live history (post 2026-05-08 cycle close)

- aweb 1.20.7 + AC v0.5.24 verified-live 2026-05-08 17:00:43Z.
  Multi-team-agent did_key strict-walk + chat fresh-start contract.
- AC v0.5.25 verified-live ~2026-05-09 (cli-signup api_key surface
  ride-along + admin_analytics test-fix). Render deploy lag re-
  observed: GHA→/health flip ~7h vs historical ~3min. Pattern logged.

Render deploy lag (2 cycles in a row) is now operational debt to
investigate. Hypothesis: Render image-watcher poll interval changed
or upgrade-window held. Athena/Juan to investigate when bandwidth
permits.

## Bertha pipeline (operational since 2026-05-08)

- **Daily sign-up export** (cron 2ddbdd18, daily 08:13 CEST): mail to
  Bertha with prior-26h sign-up batch + multi-agent activity status.
- **Hourly multi-agent milestone check** (cron f6adaa50, hourly):
  state-tracked, alerts Bertha on first-cross. Last fire 2026-05-10
  07:36:02Z, 0 candidates. State file initialized empty 2026-05-08.

Both crons are session-only (CronCreate `durable=true` did not take —
flagged as ops debt; system cron / launchd is the durable answer).

## Release pipeline

| Cycle | Status |
|-------|--------|
| aweb 1.20.0 (aame epic) | shipped + verified-live |
| aweb 1.20.1 (Phase 12 hotfix) | shipped + verified-live |
| AC v0.5.22 (aame uptake + 1to1 cleanup) | shipped + verified-live |
| aweb 1.20.2 (pagination fix) | shipped + verified-live |
| AC v0.5.23 (1.20.2 uptake) | shipped + verified-live |
| aweb 1.20.3 (aamx + aamy auto-update) | shipped + verified-live (CLI-only #27a) |
| aweb 1.20.4 (init UX) | shipped + verified-live (CLI-only #27a) |
| aweb 1.20.5 (add-worktree refuse) | shipped + verified-live (CLI-only #27a) |
| aweb 1.20.6 (Grace review cleanup) | shipped + verified-live (CLI-only #27a) |
| aweb 1.20.7 (multi-team did_key + chat 409) | shipped + verified-live (server release) |
| AC v0.5.24 (1.20.7 uptake + chat 409 close) | shipped + verified-live |
| AC v0.5.25 (cli-signup api_key + admin_analytics fix) | shipped + verified-live |
| **aweb 1.20.8** (aang/aanh/aani/aanj bundle) | **mid-flight, awaiting Athena re-make-ship at 637cd74** |
| AC v0.5.26 (1.20.8 uptake) | pending PyPI 1.20.8 publish |

## Operational discrepancies

- **Render deploy lag** (2 cycles): v0.5.24 GHA→live ~4h, v0.5.25
  ~7h vs historical ~3min. Now a pattern, not a one-time blip.
  Re-flag at next cycle.
- **CronCreate `durable=true` not taking**: scheduled_tasks.json
  not written; crons survive only inside this Claude session.
  System cron / launchd is the durable answer. Banked as ops debt.
- **Aida's runbook push (e15838c)** held pending Juan greenlight.
  BYOD-422 + framing-invariant only; fada3dd dropped after aani
  window eliminated by Grace's coordination-side fix.
- **Multi-team-agent agent_id-vs-did comparison**: Athena's lane,
  open follow-up, non-blocking.
- **Iris agent not registered**: Hetzner identity bootstrap pending.

## Active claims

`aw work active`: zero rows. `aw work blocked`: zero rows.

## Workspace status (default:aweb.ai team)

- hestia (me): online, 1.20.8 standby + cron-driven hygiene.
- athena: cross-team bridge to dev team (juan.aweb.ai).
- iris/metis/sofia/aida: see workspace status.

Dev team (`aweb:juan.aweb.ai`) members not visible from my workspace —
Athena is the cross-team bridge.

## Next checks

1. Athena's re-make-ship green at 637cd74 → tag both server-v1.20.8 +
   aw-v1.20.8 individually + push, watch GHA, verify-live.
2. Daily `/health` on app.aweb.ai + api.awid.ai. Render deploy-lag
   pattern if v0.5.26 ships next.
3. Hourly milestone-check cron firings; act only if non-empty.
4. Daily 08:13 CEST sign-up export to Bertha.
5. Brief Bertha (when 1.20.8 verified-live): Pepe Reyero's
   autonomous-install case unblocked.
6. Pass-2 trigger to Iris when 1.20.8 verified-live + npm reachable
   + aw upgrade works (Sofia's precise trigger).

## Standing release-discipline (banked through 2026-05-10)

1. Release gate = full e2e + SOT + peer-review approval (mailed)
2. Review via shared working tree
3. Route work through the right peer
4. Trust the Makefile's release-ready chain
5. Written approval / decisions via mail
6. Use prohibition language explicitly when blocking a lane
7. Push release tags individually, never batched
8. Tracker audit needs symptom-check, not commit-message grep
9. Published artifact ≠ deployed service
10. Browser-verify UI-surface releases
11. Closure framing rests on empirical attestation
12. Reproducer-as-gate
13. Code-reviewer subagent for gate-input commits (Athena pre-flight)
14. Migration-checksum chase covers BOTH OSS wheel and AC embedded copy
15. Run new-client smoke probes against rolled prod before patch tags
16. Destructive cutover with cross-schema FKs requires constraint-diff
    audit (prod vs clean baseline) as explicit verification step
17. Pre-deploy gates with environment-specific prerequisites must
    fail-closed with explicit bypass, not skip-on-missing
18. Verified-live evidence cites the actually-committed SHA, not a
    bumped-but-unreverified SHA
19. Work in flight (uncommitted bumps, in-progress procedures) does not
    count as released until tag is pushed and live-verified
20. Reproducer must match the empirical surface (CLI 409 reproducer
    must surface 409 from production CLI binary against production
    server, not just unit-test logic)
21. Bless-and-run from peer = run the FULL release-ready chain
    end-to-end, don't shortcut to bump+tag
22. Code-reviewer subagent flagged silent-fall-through + the relevant
    scale is realistic for the production trajectory ⇒ blocker, not
    follow-up.
23. Test failures recurring at specific clock windows + reruns clean
    later are date/timezone-math signals, NOT transient-flake signals.
24. Documented workarounds must be empirically attested against the
    actual customer surface AND the predecessor states they apply on
    top of, not just the surface they claim to work around.
24a. **Pre-empirical SHA-diff inspection of release framing.** Before
    accepting a release classification (CLI-only, server-only, full),
    diff the actual SHAs against the predecessor and confirm the
    classification matches the change shape. The framing in the
    handoff mail is the author's intent; the diff is the truth.
    Catches mis-classifications where wire-protocol changes are
    framed as CLI-only. (Banked 2026-05-10 from aweb 1.20.8 cycle:
    Athena framed as CLI-only #27a; SHA-diff against 1.20.7 found
    d3dfb4b modifies server/src/aweb/routes/agents.py with new
    `role_name` field that older servers silently drop. Hestia
    pushed back with two-path mail; Athena layered (A) server bump
    + (B) backward-compat fix.)
25. When the empirical surface contradicts a hypothesis, that's a
    refutation, not a "transient." Don't double down on the
    hypothesis.
26. "Affects only one customer in current base" is not a scope claim
    about the bug class — it's an observation about THIS customer
    base AT THIS MOMENT.
27. Cut-the-deploy-only-if-functional-change. Don't cut a deploy
    release purely to keep a pin-in-tagged-release synced.
27a. CLI-only release pattern: don't bump server/pyproject.toml.
    Tag aw-vX.Y.Z directly at the fix commit; goreleaser reads
    version from `${GITHUB_REF_NAME#aw-v}` per workflow config.
28. Tool-driven destructive git-state mutation is never acceptable
    as a side effect of a non-git-management command, even with
    loud warnings. Refuse + remediate, don't auto-fix the
    customer's repo for them.

`status/weekly.md` continues as a roll-up until replaced by a proper
dashboard.
