# Hestia Handoff

Crisp wake-up brief. What you need to act NOW, nothing more. For
backstory on anything referenced here, see `logbook.md`. For
operating discipline, see `AGENTS.md`.

**Last updated:** 2026-06-10 08:20 UTC

## In flight

**1) Olivia site deploys 2facc1e1 + f528b366 + 7c5d2dcd — chain, 2 holds.**

- **2facc1e1** (blueprint voice): deployed 2026-06-09 22:10 UTC.
  5/6 verified-live. Item 6 (/docs/team-bootstrap.md → 404) blocked
  on Render publish-dir staleness — HOLD A below.
- **f528b366** (hero intent tabs): 3/3 PASS (pill toggle,
  Playwright no-layout-shift, /llms.txt panels, ARIA tablist).
- **7c5d2dcd** (wake setup restore): 3/3 PASS (#start-your-agent
  runtime cards, hero foot "Wake setup ↓ · Two agents talking →",
  /llms.txt section order).
- **f4c0fec3** (hero copy fix aweb.ai/aida): 2/2 PASS (aweb.ai/aida
  in home + /llms.txt, zero ami.aweb.ai anywhere). Hero-defect
  half of aweb-aaqe.6 CLOSED.

**HOLD A CLOSED (2026-06-10 ~11:58 UTC).** /docs/team-bootstrap.md
→ HTTP 404 verified after Juan's Render Manual Deploy → Clear
build cache & deploy. Fresh rebuild mtime 10:58:04 UTC. Both
halves of aweb-aaqe.6 now closed. Mailed Olivia (msg d2f0a31c)
+ Sofia (msg d8e4ac03).

**Banked correction**: Hugo `--cleanDestinationDir` is build-local
and does NOT evict files from Render's CDN. Render Static Sites
persist published files across regular deploys; only Clear build
cache & deploy wipes them. Runbook foot-gun section updated.

**HOLD B CLOSED (f4c0fec3, 08:43 UTC).** Hero terminal panel
teaches `aw chat send-and-wait aweb.ai/aida`. Olivia cross-team
reply round-trip + my intra-team resolve+accept probe both pass.
Zero 'ami.aweb.ai' anywhere on home or /llms.txt.

**Discipline banked as runbook standing policy #14 + #15**
(Sofia 2026-06-10).
- #14: Anything named in marketing/first-touch copy must
  RESOLVE AND RESPOND (or exist and serve) at verify-live time,
  probed from a customer-shaped position.
- #15: Customer-facing copy uses FULL namespace addresses —
  never bare-name shorthand (banked from aweb.ai/ama vs
  pi.aweb.ai/ama different-scope collision). Defect even if
  address resolves+responds; address must target INTENDED scope.
Sofia mirrors both as copy-review checklist lines on her
surface; runbook enforces at verify-live.

**Soul-review precedent settled (Juan in session via Olivia
msg 7ba255a9):** Sofia owns the sweep for external-claim
auto-reply surfaces. Initial scope:
- aweb.ai/ama (YC/investors/press inbound proxy; conv
  570d949a as inventory handle since no documented baseline).
- aweb.ai/aida (now the hero-taught address; auto-replies
  across team boundaries — folded into Sofia's sweep per
  Olivia's flag).
Inventory-first posture: ask each identity directly for its
soul/instructions, with Juan as workspace-access escalation
path. Hestia-side precedent: any newly-discovered
external-claim-surface with active auto-reply behavior routes
to Sofia by default.

**pi.aweb.ai ownership + aaqe.7 sequence (Juan reversed Sofia's
deprioritization 2026-06-10 via Olivia 3ffd1fbb):**

- Juan registers pi.aweb.ai fresh (his controller authority).
- Identity pi.aweb.ai/ama created.
- Olivia drafts greeter soul.
- **Hestia lane**: persistent Pi runner bound to pi.aweb.ai/ama
  — shape like a2a.aweb.ai gateway service (container image +
  env config + Render web service + DNS + verify
  resolve+respond before copy flip).
- Hero copy stays aweb.ai/aida until policy #14 verify-live
  passes for pi.aweb.ai/ama (could be days/weeks).

**Adjacent finding banked**: aweb.ai/ama IS LIVE. Replied to
Olivia's probe within a minute. Scope: external inbound proxy
for YC/investors/press; Makespace demo 2026-06-04. Juan was
shown name collision with new pi.aweb.ai/ama and KEPT
pi.aweb.ai/ama anyway — different namespace, different scope,
intentional. Existing aweb.ai/ama untouched.

**Waiting on Olivia's namespace-ready ping** to start the
persistent Pi runner lane.

**HOLD: /docs/team-bootstrap.md still serves stale 15KB markdown**
(last-modified Mon 2026-06-08 from prior 7203f5c2 sync). File is
deleted in 2facc1e1 AND removed from AWEB_PUBLIC_DOCS in Makefile,
local Hugo build (with --cleanDestinationDir) has no team-bootstrap.md,
deploy-landing tree at 00838640 has none either. But Render's
publish dir isn't cleaned between builds so the file persists.

Sofia surfaced ask to Juan in session. Olivia confirmed one clean
rebuild from f528b366 checkout settles BOTH waves. After Juan
triggers Render Clear-build-cache + sets build command to include
`--cleanDestinationDir`, re-curl:

```
curl -sI "https://aweb.ai/docs/team-bootstrap.md" | grep -i 'http\|last-modified'
```

Expect HTTP 404. Then mail closure to Olivia + Sofia; aweb-aaqe.6
closes.

Tracked as task **#266** (Render publish-dir staleness). CORRECTED
fix shape: Render-side `hugo --minify --cleanDestinationDir` build
command, NOT Makefile pre-clean (local already uses it; deploy
pushes source only). Both Olivia + Sofia ACK'd correction.

**2) AC-managed A2A release train (#265) — Wave 3 daemon-pending.**

Last verified-live state from earlier in this session:
- AC v0.5.68 deployed at a68dd55a (dashboard team_id hotfix,
  superseded 0.5.65 which had the deterministic-release-model
  failure)
- a2a.aweb.ai gateway in daemon-pending state per Grace's 1.26.12
  (b4a26a3d) behavior — process stays up on missing AC
  projection, /health "degraded"-pending
- aweb 1.26.13 on PyPI (refresh wave server) + aw 1.26.13 on npm
- awid-service 0.5.12 PyPI + awid 0.5.12 GHCR + api.awid.ai
  verified live
- AWEB_CUSTODIAL_E2EE_KEY set on Render (Hestia generated locally
  chmod 600 at `~/.aweb-ops/ac-custodial-e2ee.env`, value NEVER in
  chat)

**Waiting on Grace** to create the first AC route via the lazy-bind
flow. Once route lands → gateway picks up routes → /health flips
healthy → run route smoke (card + RPC SendMessage→GetTask).

**3) Customer HAL-130226 (tomj.aweb.ai) intermittent timeouts.**

Still on `~/.aweb-ops/render.env` — Juan needs to provide
RENDER_API_KEY for Hestia to pull Render logs for the 05:36-06:36
UTC window. Independent of A2A train. Earlier-session hallucination
acknowledged and retracted (no "43h uptime" claim, no
"GCP-us-west1" cold-start — Render dashboard confirms aweb-cloud is
Virginia). DNS chain explanation: `gcp-us-west1-1.origin.onrender.com`
is shared Render CDN alias for ALL services regardless of region.

## Open holds (don't trip these)

- **#245 aw 1.26.3 workspace-cleanup regression.** Don't ship a
  CLI release that extends `cli/go/cmd/aw/workspace*` cleanup
  behavior until Athena + Mia decide the fix-forward shape
  (thread 96317ca9).
- **#239 aw 1.27.0 E2EE-default Phase 2.** Don't tag aw-v1.27.0
  without Grace re-route; gated on channel 1.4.11 + Pi 0.1.16
  customer adoption.
- **#266 Render publish-dir staleness.** Until Juan does the
  clear-cache rebuild, don't claim "all stale team-bootstrap
  surface gone" externally (Sofia direction).

## Live matrix (one line)

AC v0.5.68 prod (a68dd55a) • aweb PyPI 1.26.13 + aw npm 1.26.14 (aaqi shipped) /
channel 1.4.12 / claude-skills 0.2.12 / Pi 0.1.20 • awid-service
PyPI 0.5.12 + awid GHCR 0.5.12, api.awid.ai verified-live • a2a.aweb.ai
daemon-pending (waiting on Grace first AC route) • aweb.ai
deploy-landing f4c0fec3 (hero-aida 2/2 atop wake-setup 3/3 atop
hero-tabs 3/3 atop blueprint-voice 5/6; ONE hold remains on
team-bootstrap.md Render staleness) • marketplace pins: channel
1.4.12 + skills 0.2.12.

**Pepe orphan cleanup pattern**: 2026-06-10 reviewer-65e1331
(a25c55e2-...) soft-deleted via direct DB UPDATE on
aweb.agents + aweb.workspaces. Athena's aweb-aaqg replaces the
manual path with explicit lifecycle/API/CLI; until then, one-off
orphans go through belt-and-suspenders WHERE (agent_id + alias +
team_id + workspace_path + deleted_at IS NULL) + sanity gate +
transaction + post-verify-newer-untouched. See logbook 2026-06-10
entry for the script shape.

## Juan-action queue (real-time)

1. **Render clear-build-cache rebuild for aweb.ai** (Sofia loop, my #266).
2. **First AC route creation via Grace** to trigger A2A
   gateway identity bind on a2a.aweb.ai (Grace lane, awaiting her
   signal that the route is in).
3. **RENDER_API_KEY** for HAL-130226 log pull (independent).

## Wake-up checklist

1. `git pull` in ai.aweb and your sibling repos (aweb, ac).
2. `aw chat pending && aw mail inbox`.
3. Re-curl `/docs/team-bootstrap.md` — if 404 or fresh-mtime,
   close #266 verify-live arc and mail Olivia + Sofia.
4. `curl -sS https://app.aweb.ai/health` — confirm AC still v0.5.68.
5. `curl -sS https://api.awid.ai/health` — confirm 0.5.12.
6. `curl -sS https://a2a.aweb.ai/health` — has Grace's route landed?
   If healthy, run route smoke (card + RPC SendMessage→GetTask).
7. `aw task list --status pending --owner hestia` — open ops
   follow-ups.

## Where to look

- `logbook.md` — historical narrative, ship summaries, banked
  lessons, customer-activity reads. Append new dated entries here,
  don't bloat this file.
- `AGENTS.md` — operating discipline (release chain, hygiene, peer
  protocols, the scripts table, etc.).
- `scripts/` — reusable read-only DB probes for recurring questions
  from Bertha + Juan + triage. Invocation: `uv run --with asyncpg
  python scripts/<name>.py [args]`. README in `scripts/`.
- `runbook.md` — release-runbook detail.
- `artifacts/` — sensitive ops dumps + writeups, local-only (NOT
  committed; repo PII discipline).
- `~/.aweb-ops/` — chmod 600 secrets directory; AWEB_CUSTODIAL_E2EE_KEY
  and pending render.env live here.

## Discipline you'll regret skipping

- **Never echo full DATABASE_URL or AWEB_CUSTODIAL_E2EE_KEY** to
  chat — Juan-caught this session, secrets land in `~/.aweb-ops/`
  files chmod 600 then get referenced by env-name only.
- **Don't hallucinate live state.** Earlier-session "43h uptime",
  "GCP-us-west1 cold-start" were wrong and Juan called it out.
  Anchor every production claim to a `curl` or Render dashboard
  read.
- **Olivia not directly addressable as `olivia`** — use
  `juan.aweb.ai/olivia` (cross-namespace form).
  Sofia is `aweb.ai/sofia`. Juan-by-aw not reachable; loop via
  Sofia when she's in session, else Juan@aweb.ai direct.
- **Render publish-dir staleness is real** (this session, #266).
  Don't trust "site mod removed" without re-curling the specific
  removed URL.
- Per-version `/pypi/aweb/X.Y.Z/json` is canonical signal after
  publish; `uv pip install aweb==X.Y.Z` may lag.
- `make ship` couples CLI to server version (#219); use
  tag-only-at-target-sha for one-sided releases.
- Verified-live mails MUST enumerate (1) what fixed (2) what NOT
  fixed (3) evidence (4) live check — missing #2 is the recurring
  slip (Sofia caught v0.5.47).
