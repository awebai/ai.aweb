# Operations Status

Last updated: 2026-05-10 12:25 CEST (10:25 UTC) — AC v0.5.26 verified-
live. **Full P0 arc empirically closed end-to-end across two coordinated
releases (aweb 1.20.8 + AC v0.5.26) within ~24h.** Verified-live mails
sent to athena (5fc87592), sofia (ae05039f), aida (96f74b81).
Aida REMOVE-trigger fired for runbook entry e6b1303.

## Current focus

**FULL P0 ARC RECEIPT — 2026-05-09 → 2026-05-10**

Pepe Reyero surfaced four frictions on 2026-05-09. All four closed
empirically across two coordinated releases:
- **aweb-aang** (LOAD-BEARING autonomous-install): aweb 1.20.8 +
  AC v0.5.25.
- **aweb-aanh** (init --hosted single-invocation workspace.yaml):
  aweb 1.20.8 (folded into aang).
- **aweb-aanj** (aw roles set array bundles): aweb 1.20.8 (CLI-only).
- **aweb-aani** (role-name set + AC route fix): aweb 1.20.8 (CLI +
  OSS server) + AC v0.5.26 (route fix at agent_lifecycle.UpdateAgentRequest
  accepting role/role_name aliases).

Pepe-class population fully unblocked end-to-end. Sofia dispatching
Iris with full-arc receipt + Pass-2 wire-in trigger to revert
homepage bundle from Option A back to Option B.

## v0.5.26 ship attestation (2026-05-10 09:30Z → 10:13Z)

GATE CHAIN
- Athena's release-ready at 1ce7d6a9: 164 PASSED including new
  test_cloud_role_name_set_updates_current_workspace real-Docker e2e
  probe (#24b shape baked into AC release-ready chain).
- My release-ready at 1ce7d6a9: 164 PASSED (matches Athena's,
  identical test list).
- Tag v0.5.26 pushed individually at 1ce7d6a9 per discipline #7.
- GHA aweb-cloud CI/CD: SUCCESS in 14m44s (run 25625745592).
- Render → /health flip: ~1 min (Juan's manual deploy trigger
  bypassed the 4-7h pattern from last 2 cycles).

LIVE STATE (verified 2026-05-10 10:13Z)
- /health: release_tag=v0.5.26, git_sha=1ce7d6a97a (matches gate-input),
  aweb_version=1.20.8, awid_service_version=0.5.4. Started 10:12:36Z.
- /awid: 0.5.4 healthy.

LOAD-BEARING aani PROBE (single-team, default:aweb.ai)
- Pre-fix (yesterday): HTTP 422 with AC UpdateAgentRequest schema
  (access_mode required, role/role_name extra_forbidden).
- Post-deploy: 'Role name set to coordinator' clean. Round-trip
  coordinator → developer → coordinator: both transitions clean.
  CLI workspace.yaml + DB aweb.workspaces.role both updated.

MULTI-TEAM-AGENT PROBE — discipline #24b empirical attestation
(Athena ran via chat 2756e6db)
- Active-team (juan.aweb.ai dev team): aw role-name set → 200 clean.
- Cross-team override (--team default:aweb.ai): 200 clean.
- DB: two distinct rows for same did_aw, different team_ids, both
  updated within ~504ms. Multi-team workspaces handled cleanly —
  each team's row updates independently when --team override targets.
- Server-side role validation reachable: invalid role 'engineering'
  returns structured 'available roles: backend, coordinator,
  developer, frontend, reviewer'. Wire contract clean end-to-end.
- Route-interception class fully gone — server validates, responds
  with structured errors, CLI parses cleanly.

## Discipline #24b — banked across this cycle

"Pre-empirical SHA-diff inspection covers ROUTE TOPOLOGY across
deployment targets. When a fix touches a path that is mounted under
both AC's direct routes AND the OSS /api mount, verify which handler
wins on the actual deployed surface. Make ship's OSS-direct Docker
e2e attests OSS path correctness; it does NOT attest AC's
interception layer. Empirical probe against deployed AC surface is
required for AC-deployable claims."

- Banked verbatim by Athena and Sofia.
- Applied through v0.5.26 release-ready chain (real-Docker CLI-driven
  e2e test_cloud_role_name_set_updates_current_workspace added before
  tag-push).
- aank ticket scope still stands for extending coverage to
  aang/aanh/aanj surfaces; aanl established the pattern this cycle.

## Render deploy lag — open ops debt

Last 2 cycles (v0.5.24, v0.5.25): GHA→/health flip 4-7h vs historical
3min. v0.5.26 ~1 min thanks to Juan's manual deploy trigger (bypass).
Pattern unresolved. Hypothesis: Render image-watcher poll interval
changed or upgrade-window held. Re-flag if v0.5.27 shows it again.

## Live state (verified 2026-05-10 10:13Z, post v0.5.26 deploy)

- `app.aweb.ai/health`: `release_tag=v0.5.26`, `aweb_version=1.20.8`,
  `awid_service_version=0.5.4`,
  `git_sha=1ce7d6a97a92f41dfeed7163fc3d67a50f48827a`. Started
  2026-05-10T10:12:36Z.
- `api.awid.ai/health`: `version=0.5.4`, redis/db/schema healthy.

## Bertha pipeline — HANDOFF TO METIS (ANALYTICS) PER JUAN 2026-05-10

Juan (2026-05-10): "we are going to task metis, who is responsible for
analytics, for the regular check of the database... she will need to
design and write admin entrypoints to do the tasks."

Until Metis ships admin entrypoints + takes over the cadence:
- **Daily sign-up export** (cron 2ddbdd18, daily 08:13 CEST): operational.
- **Hourly multi-agent milestone check** (cron f6adaa50, hourly):
  operational, state-tracked.
- Both crons are session-only (CronCreate `durable=true` does not take —
  the durability gap is part of why Metis taking this is right; admin
  entrypoints + system cron / launchd is the proper architecture).

Hestia briefing Metis with full context, SQL, state-file design, Bertha
integration shape, durability constraints, and pitfalls — see mail to
metis (sent this cycle).

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
