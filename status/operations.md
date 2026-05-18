# Operations Status

Last updated: 2026-05-18 14:05 CEST (12:05 UTC) — **Federation
completion wave aaou.15-18 in flight**. awid 0.5.6 shipped FIRST per
Juan's standing policy ('in case of doubt always ship awid service
and awid first'): commit dad937a on aweb main, tags awid-service-v0.5.6
(PyPI workflow 26031767028 success) + awid-v0.5.6 (GHCR workflow
26031772227 success 1m18s). PyPI 0.5.6 verified live; api.awid.ai
flipped to 0.5.6 (Render auto-pulled). 02a344f's awid changes (dev-mode
insecure-delivery-origin helper, no migrations, prod-impact nil) now
deployed.

ac federation completion ship target: **v0.5.42** (per Athena eef884ad —
v0.5.41 already exists at 2a3d0144). Per Juan: ship v0.5.42 now, backfill
of existing hosted child namespaces is a one-off script run by Hestia
post-deploy, not a release-blocking item.

**v0.5.42 VERIFIED LIVE** at 7ca6ce62. Gate runs 1-3 failed in
diagnostic-useful ways (mock-Registry gap → docker-compose.test.yml
ENVIRONMENT → docker-compose.local-container.yml ENVIRONMENT). Gate
run #4 GREEN: ALL PASSED 264 tests. Tag pushed, GHA 26033745194
success, Render deployed. /health: release_tag=v0.5.42,
git_sha=7ca6ce62, aweb_version=1.23.0, awid_service_version=0.5.6.

Backfill applied 2026-05-18: 72 hosted child namespaces updated (71
first-run + 1 retry of xmythosx99x.aweb.ai after rate-limit), 0
remaining failures, 7 blocked_awid_namespace_missing (ac DB has row,
awid does not — separate cleanup thread). Spot-checks via awid:
xanerp.aweb.ai + xglasswings99.aweb.ai both show default_delivery_origin=https://app.aweb.ai.

Grace prod spot-check follow-ups (analyzed in full report to Athena
4331abdb):
- juan.aweb.ai + gsk.aweb.ai = updated (matches our JSON)
- juanre.aweb.ai null = NOT in backfill scope (pre-existing Task #125
  class — soft-deleted-with-divergence predicate gap; juanre.aweb.ai
  is Juan's personal namespace from v0.5.31/v0.5.33 P0 era)
- aida.aweb.ai + athena.aweb.ai 'namespace not found' = agent aliases,
  not user-level namespaces; expected absence outside federation model.

Open: commando-coordination step for the empirical hosted↔self-hosted
smoke walk. aweb.missionctrl.dev controller registered, but
default_delivery_origin is null (his side hasn't declared). Routing to
Athena/Juan for Ben Ford coordination; 3 options laid out (loop in
Ben for strongest claim / package internal-only and footnote /
internal-loopback weaker-empirical).

Banked signal: channel push auto-ack hides mail from default inbox
(Zeus@gsk.aweb.ai customer-attested via Aida; same symptom hit me
during Athena's mail-delivery smoke 13:11 UTC). Holding for 2nd
independent customer attestation per strength-of-feedback discipline
before escalating design question to Juan. Aida tracking on her side
as discipline #28.

Mail-delivery cross-team: Athena→Hestia smoke GREEN
(message_id f427d408, verified=true, in inbox). Grace's 'never landed'
case may be same flavor (auto-ack-as-read). Athena diagnosing.

**HOLD (2c7d8087)**: hosted MCP OAuth selected-org fix is BLOCKED. Juan
flagged solution likely incomplete; Athena has not blessed. Any release
signal pointing at this fix → treat as blocked until Athena mails
explicit bless-and-run with reviewed commit SHA + tests + release notes.
No tag pushes, no deploys, no /health flips without that bundle. Honored
by all Hestia instances.

Sofia closures (3149c5dc):
- Validator v1 framing: Sofia's call is AFTER aaou.15-18 (diverges from
  Athena's earlier 'before'). Validator hardens next cycle. Don't wait on
  her framing for the design doc.
- Commando sequencing confirmed: 1-2-3 = internal-verified → commando
  smoke → public claim. Option (A) if Ben loop-able, (B) with footnote
  if not. Decision-record on Sofia post-Ben.
- Mail-routing 404: noted, chat-with workaround; revisit after v0.5.42
  dust settles.
- Selected-org OAuth P0: Sofia framing the narrow customer-facing claim
  shape in parallel; release blocked behind framing + Athena bless +
  Grace authoring + Mia review.

Daily-messages reset 2026-05-18 ~15:40 UTC: default:aweb.ai team
counter cleared (was 69, well over Free-tier 50/day) for Juan's live
demo. Recurring risk: agent team is on tier=free; tier-bump
conversation deferred but on the table.

**P0: channel push auto-ack/read bug** (Athena 5f63c7b7, Sofia 8b7011b2
escalation). Three attestations now: Zeus@gsk customer + my smoke + Sofia
missing Athena's literate-company-graph pilot brief in conv 70f1c868.
Root cause (Athena's code read): channel-core mail.ackMessage +
chat.markRead mutate server state on push delivery — BEFORE the harness
surfaces the message to the agent. If harness drops/delays/fails, the
mail is gone from server-unread anyway. Delivery-to-channel ≠
delivery-to-agent. Athena routed to Grace as P0. When her fix commits,
channel 1.4.3 release path is independent of the OAuth v0.5.43 cut —
both can land in parallel.

**WORKAROUND for all agents until fix lands**: treat `aw mail inbox`
default (unread-only) as unreliable. Use `aw mail inbox --show-all` for
canonical state. Every Hestia/Athena/Sofia/Iris/Aida/Metis session
should honor this until channel 1.4.3 verified-live.

**[2026-05-18 ~19:26 UTC] Channel 1.4.3 VERIFIED LIVE EMPIRICALLY**.
After /plugin marketplace update + /plugin update aweb-channel +
/reload-plugins, Athena sent POST-1.4.3-INBOX-PROOF-MARKER mail
(message_id 7891897a) via channel push. Default `aw mail inbox`
showed MAILS: 1 with the marker visible — pre-1.4.3 this would have
been auto-ack'd to read-state on delivery and default inbox would
say "No messages." Athena ACK'd (chat d88b5a29). P0 closed.
Each agent needs to run `/plugin marketplace update awebai-marketplace
&& /plugin update aweb-channel@awebai-marketplace` + relaunch to pick
up the fix in their own session.

**[2026-05-18 ~18:53 UTC] ac v0.5.43 deployed**: release_tag=v0.5.43,
git_sha=05e65689, aweb_version=1.24.1, awid_service_version=0.5.6.
Includes Athena bless 625c769a: cb223c34 (Harden targeted MCP OAuth
reconnect flow) + aweb 03fe4bf (MCP legacy tool aliases) + Grace's
99cc2cb (newest-duplicate 1:1 chat continuation, fixed the
Hestia↔Athena 409s that bit this very release cycle).

OAuth smoke per Athena's 5-item checklist (Phase 3 of bless):
- Item 4 partial: stale aweb_handoff with full OAuth params → 401
  invalid_client (endpoint refuses gracefully, no 500, no leaked
  state). Cookie-clear semantics need browser to fully verify.
- Items 1, 2, 3, 5 need browser + claude.ai-account-session-bearer.
  Deferred until a session is available.

External claim (Sofia framing + Iris distribution) gated on remaining
smoke items.

**[2026-05-18 ~20:50 UTC] aweb 1.24.2 trust-display regression fix
VERIFIED LIVE**. Athena bless 96aa3b2a → ACK eb4f0431 → ACK 59a7f294
(boundary noted: do not claim Pi until aweb-aapb closes).
- PyPI aweb@1.24.2 + npm @awebai/aw@1.24.2 + local aw upgrade 1.23.0
  → 1.24.2 clean (commit d522f67).
- Smoke green both halves:
  (i) Plain output: aw chat send-and-wait athena shows '[not in
      contacts]' only, NO '[unverified]' on stable-DID reply. Earlier
      today on 1.23.0 the same agent's reply rendered as '[unverified]
      [not in contacts]' — empirical regression confirmation + fix.
  (ii) JSON: POST-1.4.3-INBOX-PROOF-MARKER mail in aw mail inbox --json
       shows verification_status=verified, from_did=did:key
       (signed_payload DID) + from_stable_id=did:aw distinct, signature
       and signed_payload present.

**Sofia direction-framing handoff** (Sofia routing 404'd from me both
mail and chat; banked here for git-pull visibility + relayed via
Athena 7453a580):

Today's verified-live cuts ready for claim shape:
- (A) Trust-display fix aweb 1.24.2 — cleanest customer-facing story
  this cycle. Regression that hosted users would see in plain output
  ('why does this say [unverified]?'). Doesn't require Pi update or
  commando coord. Decoupled, ready.
- (B) Channel auto-ack 1.4.3 — internal correctness. Suggest
  'recommended upgrade via marketplace pin' note (auto-prompts on next
  /plugin update) rather than external announcement.
- (C) MCP OAuth selected-org hardening ac v0.5.43 — customer-facing
  potential but waits on browser smoke items 1-3+5 (need claude.ai
  bearer from Juan's session).
- (D) Federation completion wave aaou.15-18 — still gated on commando
  coord per Sofia's earlier 1-2-3 sequencing.

Sofia framing call: which subset (A/B/C/D) becomes external this cycle?
Which distribution lane (Iris / Bertha-via-Eugenie / release-notes
post on aweb.ai)?

Also Sofia channel-upgrade reminder: her installed channel likely
still 1.4.2 (auto-ack bug — why direction mail was silently disappearing
in her inbox earlier). Run /plugin marketplace update awebai-marketplace
&& /plugin update aweb-channel@awebai-marketplace + relaunch to pick
up 1.4.3.

Smoke-walk shape (per Athena e39c743e + Sofia framing): hosted ↔
self-hosted user, mail AND chat both directions, message-ids + envelope
verification receipts. Preferred peer: commando (aweb.missionctrl.dev)
— relationship-respecting + best-empirical-story. 1-2-3 sequencing:
internal-verified-live → commando-notification → public claim.

Ops discrepancy flagged: sofia awid address resolves 404 from hestia
(`aw mail send --to sofia` and chat both fail). Athena confirms same
cross-team mail-resolution skew Grace diagnosed — and ac v0.5.42 itself
closes it (per Grace's diagnosis). Workaround: `aw chat-with --start-conversation`
goes through. Mailed Juan + Athena flagged.

Previous lead:
Last updated: 2026-05-18 12:20 CEST (10:20 UTC) — **Federation 1.23.0
wave VERIFIED LIVE end-to-end**. aweb 1.23.0 on PyPI + npm + `aw
upgrade` clean (server-v1.23.0 + aw-v1.23.0 individually tagged at
eb779c3). ac v0.5.41 live at app.aweb.ai (release_tag=v0.5.41,
aweb_version=1.23.0, awid_service_version=0.5.5, git_sha=2a3d0144).
awid 0.5.5 live at api.awid.ai (Docker GHCR + awid-service@0.5.5 on
PyPI). Coordinated three-deploy chain: aweb 1.23.0 → ac v0.5.40 (Mia
test-fix at 3853e09d resolved 4-test gate fail) → awid 0.5.5 → ac
v0.5.41 (awid-service dep bump 0.5.4→0.5.5, constraint tightened to
>=0.5.5 per Grace via Athena).

Critical migration gap surfaced + fixed: deployed ac v0.5.40 had
federation code but Render startup didn't apply the 003/004/005
federation mirror migrations to ac aweb schema (Task #109 latent).
Mail-send was 500-ing post-deploy. Applied via ac's own
database_infra.initialize() against .env.production; mirror migrations
landed; mail-send confirmed working. awid 002_namespace_delivery_origin
likewise needed manual `make awid-prod-migrate`.

Channel 1.4.1 release-tooling gap surfaced: GHA Channel Release fails
because channel-core/node_modules empty on GHA (no npm install in
channel-core/ before channel build). Tooling fix landed at aweb 7776312
(Athena). channel-v1.4.1 tag exists on origin but no npm publish;
license still "Proprietary" on registry. Re-fire when bandwidth allows
— Athena said either re-run same tag GHA or rev to 1.4.2.

Previous lead:
Last updated: 2026-05-17 10:50 CEST (08:50 UTC) — **Site deploy #24
VERIFIED LIVE**: Wave 1 docs (agent-guide promotion + /docs/ landing
rewrite) live at 53a95476. /docs/agent-guide/ flipped from March-8
orphan to today's fresh build (kicker "Agent reference", H1 "aweb
Agent Guide", new docs-page-header template, Mia's rewrite covering
1.22.x identity/addressing/team/messaging). /docs/ landing: Iris's
voice-pass with Primitives + Integrations subsections. Hugo built
44 pages. Athena's file-overwrite hypothesis confirmed empirically:
pages with NEW source overwrite stale Render artifacts via normal
upload; no cache-clear needed for replacements. Two true no-source
orphans persist (/docs/consumer-onboarding/, /agent-guide.md root)
with May 13 last-modified — these legitimately need Juan's Render
dashboard "Clear build cache & deploy" when he gets to it. F25
dead-link sweep in aweb/docs gated on root /agent-guide.md 404.
render.yaml IaC deferred to Wave 3.

Previous lead:
Last updated: 2026-05-16 11:35 CEST (09:35 UTC) — **Site deploy #23
VERIFIED LIVE**: docs header overhaul live on aweb.ai at 5a9ac11f.
/docs/cli-tutorial + /docs/mcp-tutorial now carry Anthropic-style
header (kicker "Agent tutorial" → H1 → description), pill Copy-page
menu with Copy page + View as Markdown (Open-in-Claude dropped per
Juan), tutorial titles "aweb CLI Tutorial for agents" / "aweb MCP
Tutorial for agents", body H1 dedup across tutorials and agent-guide.
Legacy /teams.md / /agent-guide.md / /introduction.md root paths
removed (404 on legacy URLs). Mailed Athena verified-live evidence.
Open Render/migration follow-ups (#109, #110) unchanged.

Previous lead:
Last updated: 2026-05-16 10:15 CEST (08:15 UTC) — **1.21.2
coordinated cut VERIFIED LIVE end-to-end**. AC v0.5.37 at
`app.aweb.ai/health` (sha=4ad0e1df) — backend half: empty-bundle
bootstrap + role_name Optional, gates green after 2 sweep-miss
halts (test_two_service_e2e + e2e-cloud-user-journey.sh). aweb
1.21.2 on PyPI + all 6 npm packages + `aw upgrade` 1.21.1→1.21.2
clean — CLI half: ephemeral default for hosted-persistent, alice
canonical alias on Enter, server bootstrap empty bundle (aligned
with ac/embedded). Grace's introduction.md + teams.md rewrites
+ Codex Step 9 correction live via Makefile docs sync. End-to-end
introduction.md flow now serves the designed shape.

Render image-watcher lag observation: GHA build completed
07:01:31Z; /health flipped 07:58:51Z = ~13h delay until Juan
manual trigger. Task #109 root-cause still open.

Previous lead:
Last updated: 2026-05-15 23:25 CEST (21:25 UTC) — **aweb 1.21.1
VERIFIED LIVE end-to-end**. PyPI (`aweb==1.21.1`) + npm (all 6
platform packages flipped) + `aw upgrade` 1.21.0 → 1.21.1 clean +
218-test e2e green (up from 185 — Phase 15 Roles now reachable
plus Phases 16-22 which were never reached before). Ships Mia's
onboarding rework (2ad4fdb): server-side default-zero-roles
bootstrap + CLI hosted-persistent no-prompt + alice canonical
default alias, plus Athena's roles.go fix at 9035252 (`aw roles
show` handles empty bundle without 400). Release tags
server-v1.21.1 + aw-v1.21.1 pushed individually per #7. ac
introduction.md sync (5ae400be) still pending site deploy —
independent of this aweb tag.

**Gate-failure halt + recovery this cycle**: First attempt at
452c755 aborted mid-Phase-15 of `scripts/e2e-oss-user-journey.sh`
(`aw roles show` hit server 400 on empty bundle due to CLI default
of role_name="developer" + only_selected=true; bash 5.3 errexit
propagated through command substitution in assignment). Halted
release, reverted local bump, mailed Athena with three fix-shape
options (40feddee). Athena landed option A (CLI-side) at 9035252
with new `TestAwRolesShowEmptyBundleExitsZero` regression test +
code-reviewer subagent pass per #13. Re-bumped from her HEAD and
shipped.

Last updated previously: 2026-05-15 21:10 CEST (19:10 UTC) — **aweb.ai
production deployed at 13a5da63** (19:06:46Z). Full bundle live:
Eugenie chunks 1+2, tagline v2 'Spin a web of agents, skip the
bottlenecks', font swap to system stacks, header 3-zone rework,
375px overflow fix, $150 Business display, 50 msg/day Free display,
full SEO bundle (robots/sitemap/OG/JSON-LD/og-default/apple-touch/
theme-color/enableGitInfo), Juan-authored "How to set up an
AI-native organization" first real blog post. Gate-collapse
narrative: Sofia surfaced ee2252dc as voice-shape rewrite assumed
to be Iris-going-around-chain; Juan clarified authorship +
directive "ship as I left it" → Sofia's axis closed; Athena Rich
Results validation cleared on staging (edb7e0e3) carries through
to production unchanged (template-driven schema).
**AC v0.5.36 deploy-verified-live** at 73db479a (Business
$250→$150 Stripe env-var refresh + Free 100→50 msg/day) — public
$150 display now coherent with backend charge. Stripe Checkout
visual walk still pending Juan per Athena bde3a525.
**v0.5.32 and v0.5.34** remain halted-entry images in GHCR.

**Sofia OPEN QUESTION** (mail 574185f5): v0.5.28 release notes
overclaim — the site portion of the aanv-pain-narrative iteration is
NOT yet on production aweb.ai. Three options for Juan to call: push
site / reframe notes / split verified-live framing.

**Schema-migration silent-gap discovery (2026-05-13)**: v0.5.25 → v0.5.29
all shipped without startup migrations firing on Render. 4 pending
migrations (aweb 002_contacts_handle_state +
aweb_cloud 003_byot_custodial_pending_identities,
004_mcp_oauth_connection_metadata, 005_consumer_contact_invites)
silently accumulated unrun. Caught by Juan asking "have all the
migrations run?" — empirical query of `schema_migrations` across
three schemas found the drift. Resolved via
`PROD_ENV_FILE=.env.production make prod-migrate-direct` at 19:49Z.
Banking discipline #30 (next section). Render startup-migration
mechanism root-cause investigation: Task #109.

## Current focus

**AC v0.5.28 + aweb 1.21.0 — verified-live (backend) 2026-05-13**

aweb 1.21.0 end-to-end:
- PyPI publish: ✓ (server, ManyLinux+macOS wheels)
- npm publish: ✓ via fresh GAT (banked 90-day expiration foot-gun:
  Feb 12 + 90 = May 13; old token hit exact-day cap, 404-on-anonymous-PUT
  is npm's misleading shape — diagnosed via Athena + research agent
  after Juan's pushback "you are assuming they have changed something.
  why?")
- `aw upgrade` clean against released artifact.

AC v0.5.28 end-to-end:
- aweb >= 1.21.0 pin in pyproject.toml at d64ce84c.
- First release-ready: 2 fails — `ContactView` `extra='forbid'`
  rejected new aweb 1.21.0 fields (reference_type, status,
  handle_namespace, target_agent_name). Athena landed fix at 00064992
  using Path A (Literal types for enums).
- Tag v0.5.28 pushed individually at 00064992.
- GHA + Render: Juan manual trigger to bypass image-watcher lag.
- /health: release_tag=v0.5.28, git_sha=00064992,
  aweb_version=1.21.0, awid_service_version=0.5.4.

Sofia's catch (mail 574185f5): release notes claim aanv full receipt
but the site iteration portion is staging-only as of this writing.
Three Juan-call options open: push site / reframe notes / split
verified-live framing into backend-now + site-pending.

## Site staging — deploy 3 (2026-05-13)

Just pushed: `make deploy-staging` from main HEAD `0a9b1654`
(9093a225..0a9b1654 → `deploy-landing-staging`). Site diff vs prior
staging tip (ce2bf922): 4 files in `site/` only — `hugo.yaml`,
`layouts/index.html`, `layouts/index.llms.txt`, `static/css/main.css`.
Hugo build local: 33 pages, 13 static, clean. Render rebuild of
preview-urw1.onrender.com triggered. Athena signaled (mail a0bf1a1d)
for fresh walk; Bertha/Eugenie sign-off pass to follow.

## Prior arc — full P0 close 2026-05-09 → 2026-05-10

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

## Live state (verified 2026-05-15 17:43Z)

- `app.aweb.ai/health`: `release_tag=v0.5.36`, `aweb_version=1.21.0`,
  `awid_service_version=0.5.4`, `git_sha=73db479a20cd6d614f9ad2a3f7c7123a4ce94291`.
  Fresh deploy 17:43:40Z. Stripe `STRIPE_BUSINESS_PRICE_ID` env var
  picked up on process restart.
- Prod data: `aweb_cloud.managed_namespaces` controller alignment
  backfill (2026-05-13 22:18Z) holds. Predicate re-run = 0 rows.
- Schema: 8 migration files = 8 applied rows across server (1),
  aweb (2), aweb_cloud (5). No drift.
- juanre soft-deleted managed_namespaces row remains diverged (latent
  issue caught during v0.5.33 incident triangulation, Task #125). Not
  currently hit but would fire if juanre attempts new_agent flow.
- Render apscheduler still not started in prod (Task #132 + Metis
  default-aaae triage); daily_active_workspace_facts still empty.
  Pending Juan path choice (dashboard provision vs RENDER_API_KEY).
- Schema-migration state empirically current across all 3 schemas:
  - `server.schema_migrations`: 001 (1 row)
  - `aweb.schema_migrations`: 001 + 002_contacts_handle_state (2 rows)
  - `aweb_cloud.schema_migrations`: 001 + 002 + 003_byot_custodial_pending_identities
    + 004_mcp_oauth_connection_metadata + 005_consumer_contact_invites (5 rows)
- `api.awid.ai/health`: `version=0.5.4`, redis/db/schema healthy.
- Site production (aweb.ai): pain-narrative live at 22:28Z
  (deploy-landing tip = 21cb6c23). Hero: "You're still doing the
  work / your AI should be doing". CTA: "Connect your AI" →
  app.aweb.ai/connect. 17 "relay" mentions in rendered HTML.
- Site staging (preview-urw1.onrender.com): same content as prod now.

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
| aweb 1.20.8 (aang/aanh/aani/aanj bundle) | shipped + verified-live |
| AC v0.5.26 (1.20.8 uptake) | shipped + verified-live |
| AC v0.5.27 | paused at tag — Render not triggered (Task #91) |
| **aweb 1.21.0** (aanv pain-narrative + protocol refresh) | shipped + verified-live (PyPI ✓ npm ✓) |
| AC v0.5.28 (1.21.0 uptake + ContactView schema fix) | shipped + backend verified-live; site iteration staging-only |
| AC v0.5.29 (session-recognition fast-follow: /connect + /login + Google OAuth verified_email) | shipped + backend verified-live; schema brought current via prod-migrate-direct (4 pending migrations applied) |
| AC v0.5.30 (controller_did reuse first-pass + OAuth raw-JSON wrap) | **HALTED** at tag-push — Grace surfaced 4 invariant gaps post-tag; GHA cancelled, no image, no deploy. Tag at 8c3d9dc1 stays as halted entry. |
| AC v0.5.31 (invariant-correct controller_did reuse + OAuth defensive tightening M1/M2/m1) | shipped + verified-live at 21cb6c23 + P0 prod-data backfill (5 rows aligned) |
| AC v0.5.32 (Grace returning-consumer email hotfix at 34650a93) | tagged + GHA SUCCESS; never deployed (superseded by v0.5.33 forward-progress) |
| AC v0.5.33 (post-OAuth onboarding bundle: MCP invite tool + welcome resource + consent banner + welcome guide v5 + serverInfo) | shipped + verified-live at 59ac4c81 + #30 schema check green |
| AC v0.5.34 (Olivia 409 alias-conflict UX fix at 299cb185) | tagged + GHA SUCCESS; never deployed (superseded by v0.5.35 forward-progress) |
| AC v0.5.35 (Grace reachability nobody→public for new consumer users + welcome.md content updates) | shipped + verified-live at d8eeed01 |
| **AC v0.5.36** (bundled: Business $250→$150 Stripe env-var refresh + Free tier 100→50 msg/day) | shipped + deploy-verified-live at 73db479a; behavior smokes pending Athena probe |

## Site deploy protocol (Juan-authorized 2026-05-10)

**Surface separation (build/ship boundary applied to site)**:
- Iris owns authoring `ac/site/` source (hugo.yaml, layouts/, css/).
- Hestia owns deploy execution + verification.
- Same shape as Athena → Hestia for code.

**Production deploy gate** — every deploy needs:
1. Iris signal: 'staging green at <preview URL>; ready for production deploy. Bundle covers <scope>.'
2. Bertha validation (non-technical-founder framing match — Eugenie's read).
3. Sofia framing review.
4. Juan explicit per-deploy greenlight.

Only after all four: Hestia runs `make deploy-site` from ac/.

**Staging architecture** (operational as of 2026-05-10):
- `deploy-landing-staging` branch → Render staging service → preview-urw1.onrender.com (preview.aweb.ai DNS pending).
- agent-guide sync identical to prod (true parity).
- Iris runs `make deploy-staging` (Athena landed at 36a9e442).

**Production architecture** (operational as of 2026-05-10):
- `deploy-landing` branch → Render production service → aweb.ai.
- Render reconfigured to watch `deploy-landing` (not main) — gate is now real.
- `make deploy-site` from ac/ pushes current branch → deploy-landing.
- For mid-cycle force-push case: `git push -f origin deploy-landing-staging:deploy-landing` — used in cycle 1 because Pass-3 lived on staging branch only.

**Rollback authority**: only Hestia.

**Branch protection** (open, Juan's lane, Task #88): PR-based with Juan + Sofia as approvers. Closes the structural gap — without protection, anyone with main push rights can update deploy-landing too. Latency cost acceptable for homepage frequency.

**First deploy gate run — closed 2026-05-10 14:39Z**: Iris's bundle 58ed6c53 bypassed gate (Pass-1; Render was watching main; reverted). Sofia-authored Pass-3 (60be8f4e) ran the gate cleanly: Bertha/Eugenie validation on staging ✓, Sofia framing-pass ✓ (substantive customer-shape correction), Juan explicit per-deploy greenlight ✓, Hestia deploy + verify-live ✓. Verified-live mails dispatched: iris (f0ac616f), bertha (5379880c), sofia (ab09f148). Sofia independent live-check confirmed (mail c6b73992).

**Customer-shape discipline** — adopted cross-team (Sofia mail c6b73992):
- Doc: `docs/audiences.md` (Personas 1-4 + Tier 1/2). The earlier
  `customer-onboarding-flows.md` (Shape A/B/C) was deleted 2026-05-12
  at commit 47a9558 — persona model is now the single source. Sofia
  flagged my stale reference 2026-05-13 (mail 985be5c2).
- Site copy review starts with: 'which persona is this section addressing?'
- Discipline that should have prevented Pass-2's wrong-persona-labeling miss.
- Adopted by Iris (mail cbd2aacb) + Sofia + Hestia. Aida's adoption is the natural next ask for customer-support runbook triage.

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

1. Athena fresh-walk preview-urw1.onrender.com post-Render-rebuild,
   then Bertha/Eugenie sign-off pass on iterated pain-narrative.
2. Sofia's open release-notes-reframing question (mail 574185f5):
   Juan must call — push site / reframe notes / split verified-live.
3. After Sofia/Juan call: production site deploy (`make deploy-site`)
   if push-site path; otherwise update release notes.
4. Daily `/health` on app.aweb.ai + api.awid.ai.
5. Hourly milestone-check cron firings; act only if non-empty.
6. Daily 08:13 CEST sign-up export to Bertha.
7. Branch protection on deploy-landing (Task #88, Juan's lane).
8. OIDC trusted publisher migration for npm (eliminate GAT 90-day
   treadmill — currently May 13 → next forced rotation Aug 11).
9. Monitor Neon DB connection-timeout transients (Task #89).

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
11a. **Transitive evidence is sufficient for source-only behavior changes;
    independent variables need separate empirical query.**
    Closure attestation depends on the change class:

    - **Source-code behavior** (functions, constants, conditionals, code
      paths within a single deterministic build): empirical attestation
      is transitive — git_sha → source equivalence + release-ready
      tests-passing at that SHA + `/health` reporting that
      `release_tag`. No separate end-to-end probe needed. The image is
      functionally equivalent to source at git_sha for Python-runtime
      behavior: uv.lock pins direct + transitive Python deps, source is
      COPYed verbatim, and tests at that SHA asserted the behavior. The
      chain closes.
    - **Independent variables** drift independently of code. These DO
      need separate empirical query at verify-live:
      - schema state → #30 (`schema_migrations` query)
      - prod-data state → #31 (predicate against the new invariant)
      - env vars (e.g. `STRIPE_BUSINESS_PRICE_ID`, `DATABASE_URL`,
        feature flags) → behavior probe preferred (implicitly attests
        restart by observing new behavior); `/health` restart shape
        alone is necessary-but-not-sufficient (proves reload, not the
        new value)
      - cache state (Redis: rate-limit counters, daily-message usage,
        session caches) → service count-getter probe against a known
        billing_id / session-id
      - process-internal state (in-memory schedulers, in-process
        caches — apscheduler MemoryJobStore is the canonical example
        per Task #132 + Metis default-aaae) → scheduler list-getter
        OR evidence the expected job fired post-restart
      - external API state (AWID registry, Stripe, npm registry) →
        query the external surface

    Catalyst: v0.5.36 bundled Business $250→$150 (env-var refresh —
    independent variable, needs Juan visual walk OR a probe) with Free
    tier 100→50 messages/day (source-only TIER_LIMITS change —
    transitive sufficient). Started by demanding empirical probes for
    both; Athena pointed out the asymmetry. Banking the axis explicitly
    avoids over-engineering future smokes for source-only changes and
    avoids under-engineering future env-var / cache / process-state
    changes.

    Tied to: #11 (closure rests on empirical attestation), #18
    (verified-live cites actually-committed SHA), #30 (schema check),
    #31 (prod-data state).
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
29. **Refuse interpretive-doc-only wire-ins.** A draft markdown that
    describes what to change is incomplete. Hestia cannot deploy from
    narrative. The author commits actual edits to the source surface;
    markdown serves as narrative around them, not substitute. Same
    shape as #2 (review via shared working tree, not chat-pasted
    diffs) extended to the site-author surface. (Banked 2026-05-10
    from homepage-refresh slip: Iris's first bundle was a copy-bundle
    narrative in publishing/drafts/; Hestia started wiring it into
    ac/site/. Juan caught it. Iris re-authored on ac main as 58ed6c53
    — proper shape. Banking the rule for future bundles.)
30. **Schema-migration verification is part of verify-live, not /health.**
    `/health` only probes connectivity. A service can be green on /health
    while running against a stale schema — features keyed to missing
    tables/columns will 500 in handlers, not at startup. Verify-live
    must include `SELECT filename FROM <schema>.schema_migrations` across
    all schemas (server, aweb, aweb_cloud) compared against the migration
    files in the deployed image. (Banked 2026-05-13 from v0.5.29 cycle:
    4 pending migrations from v0.5.25→v0.5.29 accumulated unrun across
    4 release cycles; only caught by Juan's "have all the migrations
    run?" question. Root-cause investigation of why Render
    startup-migration default failed is Task #109. Discipline shape:
    even if startup migration runs reliably, verify-live still queries
    `schema_migrations` empirically — same shape as #18, verified-live
    cites empirical state, not assumed defaults.)
31. **Pre-existing prod-data state can fail an invariant introduced by
    a fresh release even when gate tests pass.** Release-ready exercises
    fresh provisioning against a clean DB; it does not see corruption
    that accumulated under earlier code paths. When a release adds an
    invariant check over existing data (Grace's controller_did equality
    on existing managed_namespaces rows is the canonical example), the
    gate has a structural blind spot. Mitigation: empirical prod-data
    scan against the invariant predicate is a release-ready input,
    same shape as #18/#30 — empirical state, not assumed defaults.
    Banked 2026-05-13 from v0.5.31 cycle: Juan hit ChatGPT-connect
    OAuth error within minutes of verified-live; DB triangulation
    found 5 LIVE personal-team rows with controller_did diverged from
    org AWID-registered source-of-truth. v0.5.31 invariant correctly
    refused the diverged state; the data was already wrong. Backfill
    script (SHA 37a3f406) closed the gap, but the discovery path was
    customer-hits-error, not pre-release-empirical-check.

`status/weekly.md` continues as a roll-up until replaced by a proper
dashboard.
