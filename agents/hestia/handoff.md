# Hestia Handoff

Last updated: 2026-05-15 22:55 CEST (20:55 UTC) — AC v0.5.36 verified-live;
site production at Juan-authored homepage (ee2252dc); aweb 1.21.1 release
candidate HALTED at first gate in Phase 15 e2e, awaiting Athena fix.

## Read this first

You are Hestia. You carry every release across the build/ship boundary
and keep the company machinery healthy in between. Hands on code stays
Athena's surface; hands on site source stays Iris's surface; hands on
release-notes framing stays Sofia's; Juan greenlights any production
site push.

## Current live state

- `app.aweb.ai/health`: `release_tag=v0.5.36`,
  `aweb_version=1.21.0`, `awid_service_version=0.5.4`,
  `git_sha=73db479a` (bundled: Business $150 + Free 50/day).
- `api.awid.ai/health`: `version=0.5.4`, all green.
- Site **production** (aweb.ai): Juan-authored homepage at ee2252dc
  (deployed per his directive on 2026-05-14, see Task #146).
- Site **staging** (preview-urw1.onrender.com): in sync with main
  via deploy-landing-staging (cadence is fast / autonomous).

## IN-FLIGHT — aweb 1.21.1 gate HALTED

**State**: First gate at aweb main HEAD `452c755` (CLI comment-only
follow-up on 2ad4fdb) — `make ship` aborted mid-Phase-15 of
`scripts/e2e-oss-user-journey.sh`.

**Root cause**: Mia's empty-bundle bootstrap (server/coordination/routes/team_roles.py:113)
interacts with `aw roles show` defaults:
- CLI defaults to `role_name="developer"`, `only_selected=true`
  (`cli/go/cmd/aw/roles.go:321`).
- Server endpoint (`team_roles.py:419-424`) raises HTTP 400 when
  the resolved role name isn't in the (now-empty) bundle.
- Bash 5.3 `set -euo pipefail` propagates command-substitution
  failure through assignment → e2e script aborts.

**Action taken**:
- Reverted local server/pyproject.toml + server/uv.lock bump
  (1.21.1 → 1.21.0). Working tree clean.
- Mailed Athena with failure shape + three fix-shape options
  (mail 40feddee). My read: option B (server returns 200 with
  empty roles when bundle is empty, even with only_selected=true)
  is the right shape; option C (e2e probe change) just hides the
  regression.

**Next**: When Athena re-signals from her fix HEAD, re-bump server
pyproject to 1.21.1, refresh uv.lock, run `make ship`, then
per-product tag (`release-server-tag` + `release-cli-tag` —
NOT `release-all-tag`, which would try to recreate the unchanged
awid-v0.5.4 + channel-v1.4.0 tags).

## Cycle 2026-05-14 through 2026-05-15 — verified-live ladder

**AC releases shipped this window** (all gate-green + verified-live
mails sent + #30 schema-check applied per migration):

- **v0.5.29** (e7dec3d8): session-recognition fast-follow.
- **v0.5.30 HALTED** then **v0.5.31** (21cb6c23): controller_did
  + OAuth raw-JSON. Triggered P0 INCIDENT 1 — 5 LIVE personal-team
  managed_namespaces rows had diverged controller_did. Resolved
  via backfill script `ac/scripts/backfill_managed_namespace_controllers.py`
  applied 5/5 rows cleanly on branch `hestia/backfill-managed-namespace-controllers`.
- **v0.5.32** (34650a93): Grace email-fix hotfix (superseded same day).
- **v0.5.33** (59ac4c81): post-OAuth onboarding bundle. Triggered
  P0 INCIDENT 2 — claude.ai /oauth/authorize failing. Athena's
  read from Render logs: AliasConflictError on tsm/marvin.
- **v0.5.34**: M1 whitelist 409/422 + preflight alias check.
- **v0.5.35** (d8eeed01): reachability default public + Grace's flip.
- **v0.5.36** (73db479a): bundled Business $150 + Free 50/day —
  source-only behavior changes, no schema motion.

**Site deploys** (staging autonomous; production gate-held):
- Staging 4-15: Iris-authored blog post landing + homepage iterations
  (Eugenie voice edits, mobile fixes, font swaps, tagline v2,
  header rework, SEO bundle).
- Production 15: Juan-authored ee2252dc deployed 2026-05-14 on his
  directive. Sofia's HOLD on Iris's rewrite was based on wrong
  attribution; Juan's directive collapsed the gate.

## Disciplines banked this window

- **#11a** (after v0.5.36 lesson): transitive-evidence-for-source-only-behavior-changes.
  When `git_sha` in /health matches a commit whose only behavior
  change is in source, the source-equivalence is transitive
  evidence — no need for separate empirical query. Independent
  variables (schema/prod-data/env/cache/process-internal/external-API)
  still need their own check.

The full numbered list (now 31 items including #11a's clarification)
lives in `../../status/operations.md`.

## Operational tooling landed this window

- `ac/scripts/backfill_managed_namespace_controllers.py` (167 lines,
  on `hestia/backfill-managed-namespace-controllers`): branch +
  line-by-line review + dry-run → apply protocol for P0 INCIDENT 1.
- `ac/scripts/fetch_render_logs.py` (219 lines, on
  `hestia/render-log-fetch`): Render log ingestion for self-serve
  triage. Awaits RENDER_API_KEY + RENDER_OWNER_ID env vars from Juan.
  Branch cross-contamination from Iris's blog commit was recovered
  via `git rebase --onto e75fbebc 6e432214 hestia/render-log-fetch`
  + `git push --force-with-lease`.

## Task #132 — apscheduler dead-in-prod

Confirmed empirically: `JobScheduler` (AsyncIOScheduler with
MemoryJobStore default) is never instantiated in
`main.py:lifespan`. The session-only cron pattern (Bertha/multi-agent
checks) survives only inside an agent session. Athena chose
**Option B** (separate Render worker service). Checklist sent for
Juan; awaits provisioning OR a wired RENDER_API_KEY so I can audit
which paths fire.

## Crons running this session

- Hourly multi-agent milestone check (state-tracked, only ack new).
- Daily 08:13 CEST sign-up export to Bertha.

Both session-only per Task #132. Metis briefed on admin-entrypoint
architecture for replacement.

## Operational debt — still open

- **OIDC trusted publisher for npm** (Task #104): would eliminate
  the GAT 90-day treadmill. Next forced rotation Aug 11 if we
  stay on GAT.
- **Render image-watcher lag** (Task #109): 4-7h pattern; manual
  deploy trigger bypasses; root cause unknown.
- **Neon DB connection-timeout transients** (Task #89): 2 events
  2026-05-10/12.
- **Soft-deleted-with-divergence managed_namespaces rows** (Task #125):
  juanre latent issue; backfill predicate extension pending.
- **Schema-migration verification in release-verify-live gate** (Task #110).
- **Branch protection on deploy-landing** (Task #88, Juan's lane).

## Release-discipline catalogue

`../../status/operations.md` carries the full numbered list (31
items). Most recently banked: #11a (transitive-evidence-for-source-only).

## Next wake-up checks

1. Athena's fix HEAD for aweb 1.21.1 → re-bump + re-run `make ship`.
2. `app.aweb.ai/health` + `api.awid.ai/health` daily.
3. Hourly milestone-check cron firings (state-tracked, only ack new).
4. Daily 08:13 CEST sign-up export firing.
5. Site staging cadence (autonomous — push when Iris signals new HEAD).
6. Production site changes: gate-held, four-step chain
   (Iris/Bertha-Eugenie/Sofia/Juan).

## How to pick up clean

```bash
cd /Users/juanre/prj/awebai/ai.aweb/agents/hestia
git pull
aw chat pending
aw mail inbox
curl -sS https://app.aweb.ai/health
curl -sS https://api.awid.ai/health
git -C aweb log --oneline -5
git -C aweb status --short    # any local bump still pending?
```

Then read this file, `../../status/operations.md` lead, and any new
entries in `../../docs/decisions.md`.
