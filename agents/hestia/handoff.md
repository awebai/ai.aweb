# Hestia Handoff

Last updated: 2026-05-24 00:25 CEST (22:25 UTC) — **AC v0.5.47 +
aweb 1.25.3 destructive-cutover verified live**. Closes aapq wave.

## Current state

- prod /health: release_tag=v0.5.47, git_sha=9d39f579,
  aweb_version=1.25.3, awid_service_version=0.5.8, all green
- aweb consolidated 001 rebaseline live (was: original 001 + bridge
  002; now: single 001 with final state baked into CHECK)
- Athena formal ack 0323d5cc/4704b86b; Iris ack b21e1511; Sofia
  ack-pending
- Sprint Phase 2 DROP → /health flip: 7m05s within 10-min SLO
- Cutover dump preserved at /tmp/aweb-cutover-20260523T220920Z/ ;
  safety-net dump at /tmp/aweb-safety-net-20260523T220642Z/ (both
  ~56MB / 71 COPY blocks / 23599 rows; sha256 logged in operations.md)

## Immediate follow-ups (small, in-lane)

1. **`prod_db_reset.py` argv leak**: `_run` helper prints full
   pg_dump argv to stdout including DATABASE_URL with Neon password.
   Standing rule "never echo DATABASE_URL". Scrub the print path
   (mask URL with `***` while keeping flags visible). Juan acknowledged
   in-session ("that's fine as long as the dump is complete and
   correct, do not worry about neon").
2. **`aw whoami` 401**: `aw whoami` reports
   `Inbound: unknown (aweb: http 401: Invalid authorization header format)`
   on hestia identity post-cutover. Other surfaces (workspace, mail,
   chat, contacts) all work. Likely an AC endpoint expecting a
   different auth header shape than the inbound-mode probe sends.
   Not blocking; worth a routing-side investigation when Athena or
   Grace has cycles.
3. **`aw mail send --to juan` returns "agent not found: juan"**: the
   juan alias doesn't resolve. Per CLAUDE.md `aw mail send --to juan`
   is the documented escalation path for production incidents. Verify
   contacts list / alias setup so the escalation path is live.
4. **Runbook lesson to bank**: do the constraint-diff audit BEFORE
   entering the sprint window, not during. Today's scope expansion
   (aweb only → all 3 schemas) was decided mid-sprint at the FK
   foot-gun moment. Stayed within SLO but cost ~1 min of mid-sprint
   scrambling. Pre-sprint audit per runbook line 1430-1438 should
   be enforced.

## What just landed (today, 2026-05-23 — full chronology)

Morning (Juan-watching, Grace's translator):
- Destructive cutover for aapj/k/l/m consolidation
- aweb 1.25.0 + awid-service 0.5.8 + AC v0.5.45 verified-live

Mid-day:
- aweb-aapp identity_mismatch debug: closed at aweb 70410c3
  (Dave's JS verifyDidKeyResolution accepting seq=1 register_did)
- AC v0.5.46 (aapq feature: team_and_contacts inbound mode)
  shipped with aweb 1.25.2 + bridge 002 migration
- aw CLI 1.25.2 released

Evening (this session):
- aweb 1.25.3 consolidated rebaseline shipped to PyPI
- AC v0.5.47 destructive cutover: drop 3 schemas, full re-migrate,
  data-only restore, Render-click, /health flip — 7m05s sprint
- Gate `release-verify-migration-immutability` restored in 53215c09

## Next-Hestia start point

- Sofia ack on v0.5.47 verified-live (if not received: mail her with
  evidence summary)
- Address the 3 follow-ups above (each is small, fits between waves)
- Stale items still on operations.md tail: #89 Neon timeouts,
  #104 OIDC npm migration, #109 Render startup migration check,
  #110 release-verify-live schema gate, #125 backfill predicate,
  #132 scheduler worker provision, #169 render orphan-purge,
  #182 federation smoke, #190 MCP OAuth smoke, #191 Sofia loop,
  #203 hestia aw_sk 409 gap, #204 post-cutover to_did history drop
- Tomorrow morning routine: `git pull`, read docs/team.md +
  docs/agent-first-company.md + docs/invariants.md, read
  status/operations.md (this file's parent), curl
  https://app.aweb.ai/health + https://api.awid.ai/health, then
  `aw chat pending` + `aw mail inbox`

---

**Historical:**

Last updated: 2026-05-18 15:25 CEST (13:25 UTC) — **Federation
completion wave aaou.15-18 internally verified live; commando-coord
pending for external claim**. v0.5.42 deployed at 7ca6ce62 with
aweb 1.23.0 + awid-service 0.5.6. Backfill 72/72 hosted child
namespaces updated, 7 drift rows flagged (ac-row-but-no-awid;
non-blocking, pre-existing). Spot-checks confirm via awid.

Gate chain (4 runs) banked: each failure was diagnostic-useful and
fixed by Athena via small targeted commits. Pattern: every new test
stack (docker-compose.test.yml, docker-compose.local-container.yml)
that wires awid needs ENVIRONMENT set; durable Option B (require
ENVIRONMENT explicit at awid startup) banked as fast-follow brief.

Mail-delivery cross-team smoke 13:11 UTC: Athena→Hestia GREEN
(verified=true). Default `aw mail inbox` showed empty because channel
push auto-acks-as-read — same friction Aida just escalated from
customer Zeus. Banked as Task #187, watching for 2nd attestation.

Open: commando-coordination for hosted↔self-hosted federation smoke.
aweb.missionctrl.dev has controller_did but default_delivery_origin=null;
need Ben Ford to set his side. Athena owns the routing decision.

Previous lead:
Last updated: 2026-05-18 14:15 CEST (12:15 UTC) — **Federation
completion wave aaou.15-18 in flight**. awid 0.5.6 shipped FIRST per
Juan's standing policy ('in case of doubt always ship awid service
and awid first'):

- commit dad937a on aweb main
- awid-service-v0.5.6 tag → PyPI workflow 26031767028 ✓
- awid-v0.5.6 tag → GHCR workflow 26031772227 ✓ (1m18s)
- PyPI awid-service@0.5.6 live ✓
- api.awid.ai flipped to 0.5.6 ✓ (Render auto-pulled GHCR image)
- 02a344f's awid changes (dev-mode insecure-delivery-origin helper,
  no migrations, prod-impact nil) now deployed

ac federation completion: **v0.5.42** (Athena correction eef884ad —
v0.5.41 tag already exists at 2a3d0144 from my earlier awid-service
tighten commit; Grace's hosted federation ingress at a3170afb landed
without a bump). HOLDING v0.5.42 tag-push pending Grace's call:
- Option A: include admin backfill command for existing hosted child
  namespaces (alice.aweb.ai etc — without backfill they won't get
  delivery_origin auto-set since only the BASE aweb.ai namespace gets
  repaired at AC startup)
- Option B: ship narrower without backfill, separate v0.5.43 follow-up

Standing by for Grace's decision.

Smoke-walk shape locked (Athena e39c743e + Sofia framing):
- hosted ↔ self-hosted user, mail AND chat both directions
- message-ids + envelope verification receipts in verified-live mail
- preferred peer: commando (aweb.missionctrl.dev) — relationship-respecting +
  best-empirical-story (he triggered the federation arc)
- 1-2-3 sequencing: internal-verified-live → commando-notification →
  public claim
- fallback if commando unavailable: internal-loopback as weaker-empirical
  footnote

Ops discrepancy flagged: sofia awid address resolves 404 from hestia
(`aw mail send --to sofia` AND chat both fail). Athena confirms same
cross-team mail-resolution skew Grace diagnosed — and ac v0.5.42 itself
closes it. Workaround for now: `aw chat-with --start-conversation`
goes through. Mailed Juan + Athena flagged. Design doc v2 routed to
Sofia via git pull instead.

Previous lead:
Last updated: 2026-05-18 12:20 CEST (10:20 UTC) — **Federation 1.23.0
wave VERIFIED LIVE**. Three coordinated deploys today:

1. aweb 1.23.0 server + CLI (PyPI + npm)
2. ac v0.5.40 (aweb 1.23.0 pin) → halt for 4-test gate fail → Mia
   fix at 3853e09d → re-gate green → ship
3. awid 0.5.5 (GHCR + PyPI awid-service)
4. ac v0.5.41 (awid-service 0.5.5 pin + constraint tighten)

Live state at v0.5.41:
- app.aweb.ai: release_tag=v0.5.41, aweb_version=1.23.0,
  awid_service_version=0.5.5, git_sha=2a3d0144
- api.awid.ai: version=0.5.5
- Mail-send confirmed working post-migration (smoke to aida)

## Critical learning from this cycle

**Render startup didn't apply federation mirror migrations.** ac v0.5.40
deployed with federation code BUT ac aweb-schema only had 001+002 (no
003/004/005 federation mirrors). Mail-send 500-ed because runtime tried
to write to federated_message_deliveries / participant.delivery_origin
tables that didn't exist yet. Task #109 (Render startup migrations) is
no longer just an investigate-when-bandwidth item — it directly broke
a customer-facing deploy.

Fix: applied via `cd ac/backend && uv run python -c "..."` invoking
ac's own `database_infra.initialize(run_migrations=True)` against
.env.production. This is the SAME code path Render startup should
run — it just didn't fire on container start. Need to investigate
why (probably AWEB_PUBLIC_ORIGIN env or some other gate condition;
Task #109 still open).

Likewise awid 002 needed manual `make awid-prod-migrate` — same
class of issue.

**Two-commit pattern for ac dep bumps** (banked from Mia + reaffirmed
this cycle): dep bump + version bump in commit A, follow-up constraint
tightening in commit B. Don't amend; let main carry the audit trail.

## Channel 1.4.2 SHIPPED with MIT license

Resolved end-to-end after two compounding gaps:
1. **Tooling gap** (Athena fix at 7776312): channel-core/node_modules
   empty on GHA → esbuild couldn't resolve transitive deps. Fix added
   channel-core npm install + build BEFORE channel build in both
   release-channel-check Makefile and channel-release.yml workflow.
2. **Per-repo NPM_TOKEN drift**: Juan rotated NPM_TOKEN on 2026-05-13
   but only set the new token in some repos (awebai/aw worked, but
   awebai/aweb still had the April 2 token, which had since stopped
   working). GHA failed with E404 PUT on @awebai/claude-channel.

Fixes: Athena's tooling commit; I ran `gh secret set NPM_TOKEN -R awebai/aweb`
with Juan's May 13 token (passed via stdin). Re-fired GHA at
channel-v1.4.2 (commit c31176d) — published 2026-05-18T10:57:52Z.
npm view confirms version=1.4.2, license=MIT.

channel-v1.4.1 tag remains on origin as orphan (no npm publish landed).

## Discipline banked from this cycle

**When npm tokens are rotated, check ALL repos that consume them.**
The NPM_TOKEN secret is per-repo, not org-wide. A rotation event on
2026-05-13 left awebai/aweb's copy stale for 5 days because nothing
exercised channel-release.yml in between. Banking-worthy: when an
auth token is rotated, do a sweep of every workflow that uses it
across every repo in the org and update each individually (or migrate
to OIDC trusted publishing per Task #104 — eliminates the recurring
treadmill).

## Channel 1.4.1 STILL HELD (obsolete — see above)

Earlier:
Last updated: 2026-05-17 10:50 CEST (08:50 UTC) — **Site deploy #24
VERIFIED LIVE**: Wave 1 docs at 53a95476 live on aweb.ai.
/docs/agent-guide/ flipped from March-8 orphan to today's build
via Hugo file-overwrite (Athena's hypothesis confirmed: pages with
NEW source overwrite stale Render artifacts via normal file-upload;
cache-clear only needed for no-source orphans). New template with
kicker "Agent reference", H1 "aweb Agent Guide", Mia's rewrite of
identity/addressing/team/messaging content for 1.22.x. /docs/ landing
got Iris's voice-pass with Primitives + Integrations subsections.
Hugo built 44 pages. Two true no-source orphans persist
(/docs/consumer-onboarding/ + /agent-guide.md root) with May 13
last-modified — these need Juan's Render dashboard cache-clear when
he gets to it. F25 dead-link sweep in aweb/docs gated on root
/agent-guide.md 404. render.yaml IaC deferred to Wave 3.

## Operational learning from this cycle

**File-overwrite vs. artifact preservation are distinct mechanisms.**
For orphan-purge on Render static sites:
- Orphan with NEW Hugo source: Hugo build → file-overwrite at upload
  retires it automatically. No cache-clear needed.
- Orphan with NO source: stays as preserved artifact across deploys;
  needs Render "Clear build cache & deploy" dashboard action.
Diagnosis: curl the URL pre-deploy. If a new source IS being added
in the deploy, expect today's last-modified post-deploy. If no
source ever (or only being deleted), the page persists unchanged
unless cache-clear runs.

I initially gated the Wave 1 deploy on Juan's dashboard probe (good
caution, correct sequencing for a no-source orphan). Athena corrected
the framing for agent-guide specifically — it had a new source in the
Wave 1 bundle. Deploying immediately surfaced the file-overwrite
behavior cleanly. The cache-clear gate stays valid for the remaining
no-source orphans.

Earlier:
Last updated: 2026-05-17 (post-resume) — **Site deploy #23
VERIFIED LIVE**: docs header overhaul at 5a9ac11f live on aweb.ai.
/docs/cli-tutorial + /docs/mcp-tutorial now render Anthropic-style
header (kicker "Agent tutorial" → docs-page-title H1 → description),
pill Copy-page menu with Copy page + View as Markdown only
(Open-in-Claude dropped per Juan), tutorial titles "aweb CLI Tutorial
for agents" / "aweb MCP Tutorial for agents", body H1 deduped on
tutorials + agent-guide. /docs/teams/ correctly 404 (legacy
root-doc sweep). Mailed Athena evidence; status updated.

Earlier:
Last updated: 2026-05-16 21:55 CEST (19:55 UTC) — **aaoq+aaor
wave LIVE end-to-end**: aweb 1.22.0 (MCP tool surface rename:
send_mail/send_chat/check_mail/check_chats/read_chat/
mark_chat_read; doc restructure intro.md→cli-tutorial.md +
mcp-tutorial.md; aaor hosted spawn-invite authority + bare-alias
messaging fix) on PyPI + npm + `aw upgrade` clean. AC v0.5.39
live (sha=8a5a8275; Olivia P0 dashboard fix + aaom paired
consumer test updates + complete roles-optional sweep on
frontend + e2e). Site production at fd0829cd: /docs/cli-tutorial/
+ /docs/mcp-tutorial/ HTML routes + raw .md, /developers hero
drops "aw init" line, getting-started umbrella rewritten,
backend mcp-tutorial.md (welcome.md replaced), legacy
intro/teams.md 404. Many gate halts this wave (Phase 10 mail
fix at 76956ab, docker postgres infra flake, apt-get build
network, ac auth-bridge developer-role assertion, check_inbox
→check_mail sweep miss, 3 more empty-bundle surfaces, Makefile
legacy-path git-add bombing on idempotent run, Cloudflare
s-maxage CDN cache on legacy /agent-guide.md). All recovered;
all artifacts verified-live.

Earlier:
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
