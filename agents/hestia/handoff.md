# Hestia Handoff

Last updated: 2026-05-16 12:05 CEST (10:05 UTC) — **1.21.2
+ landing pages bundle + Plausible/robots.txt all LIVE end-to-end**.

- AC v0.5.37 backend live at app.aweb.ai (sha=4ad0e1df).
- aweb 1.21.2 on PyPI + all 6 npm packages + `aw upgrade` clean.
- aweb.ai production: full Iris bundle (homepage rework,
  hero subtitle + brand-mark, .proto-hero-graphic constellation,
  agent-to-agent label, day-in-life mobile carousel + peek,
  Connect-your-AI single CTA) + Grace's introduction.md +
  teams.md (via Makefile docs sync) + d92b001b border fix +
  Plausible analytics + robots.txt AI-bot explicit-allow.
- Production HEAD on deploy-landing: e105d2b0.

## Banked discipline #32 — deploy-target reads working-branch

**Rule**: `make deploy-staging` and `make deploy-site` push from
`git -C ac symbolic-ref --short HEAD`. The repo's CURRENT BRANCH
becomes the source of the push. **Before running either, verify
`git -C ac branch --show-current = main`.**

**Why**: caught this on 2026-05-16. Athena/Mia switched the ac
repo to `mia-aaom-consumer-updates` between my prior cycle's
end (on main) and Iris's next staging signal. My `make
deploy-staging` ran from that branch — pushed Mia's aaom
paired-consumer commit to deploy-landing-staging alongside the
target Plausible commit. Staging was contaminated until I
re-deployed.

**How to apply**:
1. `cd /Users/juanre/prj/awebai/ac && git branch --show-current` →
   confirm `main` before any `make deploy-*`.
2. If on another branch: stash any WIP with a clear label
   (`git stash push -m "<branch>-WIP-handoff: ..."`),
   `git checkout main`, `git pull --ff-only`, deploy, then
   restore (checkout original branch + `git stash pop` if the
   owner needs the WIP back).
3. Mail the branch owner about the stash so they can recover.
4. **Future**: a Makefile guard like
   `test "$$(git symbolic-ref --short HEAD)" = main || (echo "Not on main"; exit 1)`
   would make this structurally safe. Not yet landed; Athena's
   call on whether to add it.

## Note on staging today

`origin/deploy-landing-staging` (099f2e3e) carries Mia's
`8c4c9e3b aaom paired-consumer` commit because of the
branch-trap above. Production `deploy-landing` (e105d2b0) is
clean — pushed from main HEAD only. Mia's branch
(`origin/mia-aaom-consumer-updates`) is intact; she can
recover her WIP via the stash labeled
`mia-WIP-handoff: ... 2026-05-16` (flagged to Athena mail
b88da9b2). Staging will self-correct on the next clean
deploy-staging from main (force-push not needed if the next
deploy is from main HEAD that includes the same Plausible commit
already).

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

## aweb 1.21.1 — VERIFIED LIVE 2026-05-15 21:25Z

**Source HEAD**: 9035252 (Athena's `cli/go/cmd/aw/roles.go` fix)
**Release commit**: 02e992b (server pyproject 1.21.0→1.21.1)
**Tags pushed individually**: server-v1.21.1 + aw-v1.21.1.

**What shipped**:
- Server-side default-zero-roles bootstrap for new teams
  (`server/.../team_roles.py:113` — Mia's 2ad4fdb).
- `aw init` hosted-persistent: always persistent, no prompt
  (Mia's 2ad4fdb).
- `aw init` hosted-persistent: "alice" as canonical default alias
  (Mia's 2ad4fdb).
- `aw roles show`: handles empty bundle without 400 — resolves to
  `only_selected=false`, emits "No roles configured for this team.
  Add roles with `aw roles add`." (Athena's 9035252).

**Gate-failure recovery shape** (banked operational lesson):
First attempt at 452c755 aborted mid-Phase-15 of
`scripts/e2e-oss-user-journey.sh`. Root cause:
- CLI `cli/go/cmd/aw/roles.go:321` defaulted to `role_name="developer"`.
- Server `team_roles.py:419-424` raised HTTP 400 on missing role
  against empty bundle.
- Bash 5.3 `set -euo pipefail` propagates command-substitution
  failure through `x=$(failing_cmd)` assignment (different from
  older bashes).
- e2e script aborted at `roles_out="$(run_aw_in ... roles show 2>/dev/null)"`.

Halted release pre-tag. Reverted local server/pyproject + uv.lock.
Mailed Athena with failure shape + three fix-shape options
(mail 40feddee). Athena chose option A (CLI-side) at 9035252 +
new `TestAwRolesShowEmptyBundleExitsZero` regression test +
code-reviewer subagent pass per #13. My re-run at 02e992b
green — 218 tests (33 more than prior 185 because Phase 15-22
now reach previously-unreachable code).

**Live evidence**:
- PyPI: `aweb==1.21.1` published.
- npm: all 6 platform packages at 1.21.1
  (@awebai/aw{,-darwin-arm64,-darwin-x64,-linux-x64,-linux-arm64,-windows-x64}).
- `aw upgrade` flipped local install 1.21.0 → 1.21.1; `aw version`
  reports commit 294a08d (auto-sync to awebai/aw).
- `aw roles show` against existing non-empty bundle still prints
  "Role: coordinator" — non-regression for membership-role path.

**Per-product tag rationale** (banked):
- Used `release-server-tag` + `release-cli-tag` (not `release-all-tag`).
- `release-all-tag` would try to re-create awid-v0.5.4 and channel-v1.4.0
  even though awid/channel sources didn't change → would fail with
  "tag already exists." Right pattern for server+CLI-only patch
  bumps.

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

## Forward note — AC aweb-pin bump for hosted dogfood

`app.aweb.ai/health` reports `aweb_version=1.21.0` — AC's runtime
still has aweb 1.21.0 pinned in `ac/backend/pyproject.toml`.
The OSS path is fully covered by 1.21.1, but the hosted dogfood
flow needs AC to bump the pin to `aweb>=1.21.1` and redeploy so
that teams created via app.aweb.ai/init seed empty bundles
(Mia's `team_roles.py:113` behavior change). Not blocking
anything today (AC v0.5.36 healthy); flagged as natural fast-follow
when Athena scopes the next AC release that fronts the
introduction.md launch. Will catch this at next AC gate-review
if not already in her plan.

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
