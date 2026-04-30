# Operations Status

Last updated: 2026-04-30 (Hestia, post role-model transition; first
operations status under the new model)

## Current focus

The role transitioned today. Hestia now owns the path from clean
main to verified-live production (release-ready gates, tag, deploy,
verify) AND ongoing operational hygiene (stale claims, status
cadence, dashboard). Athena writes code and signals release; Hestia
runs the chain. Athena does NOT tag. Hestia does NOT touch code.

**Two things must happen before the role separation is real:**

1. The ops runbook at `agents/hestia/runbook.md` must be written
   (does not exist yet).
2. A no-op `make release-ready` dry-run must succeed end to end on
   aweb without engineer assistance. If Hestia can't run the chain
   alone, the separation is theater.

## Live state (verified 2026-04-30 morning)

- `app.aweb.ai/health`: `release_tag=v0.5.10`,
  `aweb_version=1.18.6`, `git_sha=bce92c29`,
  `awid_service_version=0.5.1`. db/redis/awid/coordination_api
  healthy. Started 2026-04-30 05:54 UTC.
- `api.awid.ai/health`: `version=0.5.2`, redis/db/schema healthy.
- aweb OSS published tags: `server-v1.18.6`, `aw-v1.18.6`,
  `awid-v0.5.2`, `awid-service-v0.5.2`.
- channel: 1.3.3 published.
- No release candidate in flight.

## Release pipeline

- Athena ready: no current candidate
- Gates run: n/a
- Tagged: n/a
- Deployed: v0.5.10 already live (last deploy 2026-04-30 05:54 UTC,
  pre-transition)
- Verified live: yes (this status entry's live-state section)

## Operational discrepancies

- **Ops runbook missing.** `agents/hestia/runbook.md` does not exist.
  Tracked as Hestia's first-task discrepancy.
- **Identity setup pending.** `agents/sofia/.aw/`, `agents/athena/.aw/`,
  and `agents/aida/.aw/` carry pre-rename identities (avi, randy,
  amy). `agents/hestia/`, `agents/iris/`, `agents/metis/` have no
  `.aw/` at all. Until Juan runs the AWID identity setup, the rename
  is cosmetic at the runtime layer. Sofia's product status flags this
  as priority 2.
- **Stale repo-manager dirs on disk**: `agents/coord-cloud/` and
  `agents/repo-aweb/` are untracked workspace records from the
  pre-narrowed-permanent-set model. Tracked by `aweb-aals.5`.
- **Dashboard implementation**: signal inventory exists in
  `docs/company-dashboard.md` (sofia / aweb-aals.3) but no concrete
  dashboard or report yet. Hestia adoption is the next step.
- **`aw` task metadata native fields**: builder/reviewer/feedback
  fields still parsed from the prose `Work contract:` block. Tracked
  by `aweb-aals.7`; product gap.

## Active claims at transition (snapshot)

`aw work active` shows 5 rows as of role transition. Stale-claim
sweep needed within 24h:

- `aweb-aalr.2` (mia, ac): 36h+ stale at transition. Athena to
  inherit or kick task.
- `aweb-aakj` (kate, aweb): partially landed in main; verify scope.
- `aweb-aals.3` (sofia): in flight; signal inventory done.
- `aweb-aajx` (mia): unknown repo, P0; needs locator.
- `aweb-aaka.30.1` (mia): P2.

## Next checks

1. Write `agents/hestia/runbook.md`. Encode the release-ready chain,
   PyPI cache-lag (`uv sync --refresh` window), make-export
   compose-interpolation foot-gun, per-tag-not-batched push rule,
   live-verify probe pattern, Docker clock-drift symptom.
2. Run a no-op `make release-ready` dry-run in aweb to qualify the
   chain. Mail Athena if any step fails for non-engineer-knowledge
   reasons.
3. Stale-claim sweep on `aw work active` after 24h.
4. Daily `/health` check on `app.aweb.ai` and `api.awid.ai`. Compare
   to `status/product.md` claims; flag drift.
5. Track `aweb-aals.4` (Metis init), `aweb-aals.5` (stale dir
   cleanup), `aweb-aals.7` (native task fields) as ongoing
   operational hygiene items.

## Standing release-discipline (banked through 2026-04-26, enforced by Hestia)

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
13. Code-reviewer subagent for gate-input commits (Athena runs
    before signaling Hestia)

`status/weekly.md` continues as a roll-up until replaced by a
proper dashboard.
