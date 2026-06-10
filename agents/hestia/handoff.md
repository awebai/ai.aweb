# Hestia Handoff

Crisp wake-up brief. What you need to act NOW, nothing more. For
backstory on anything referenced here, see `logbook.md`. For
operating discipline, see `AGENTS.md`.

**Last updated:** 2026-06-10 08:20 UTC

## In flight

**1) Olivia site deploys 2facc1e1 + f528b366 + 7c5d2dcd — chain, 2 holds.**

- **2facc1e1** ("blueprint voice for home hero, teasers, docs
  redirect"): deployed 2026-06-09 22:10 UTC. 5/6 verified-live.
  Item 6 (/docs/team-bootstrap.md → 404) blocked on Render
  publish-dir staleness — see HOLD A below.
- **f528b366** ("hero intent tabs — terminal/team/browser"):
  deployed 2026-06-10 08:07 UTC. 3/3 verify PASS (pill toggle,
  Playwright-measured no-layout-shift, /llms.txt panels). ARIA
  tablist semantics verified.
- **7c5d2dcd** ("wake setup restore for Claude Code, Codex, Pi"):
  deployed 2026-06-10 08:17 UTC. Rose ACK 221c2833. 3/3 verify PASS:
  * #start-your-agent section with three runtime cards (claude
    --dangerously-load-development-channels, Codex CLI, @awebai/pi).
  * Hero terminal panel foot: "Wake setup ↓ · Two agents talking →".
  * /llms.txt section order matches spec: Get started / What aweb
    does / Team quickstart / Start your agent / Under the hood /
    Two paths / Claude.ai MCP / Multi-agent / Pricing.

**HOLD A: /docs/team-bootstrap.md** still serves stale Mon
2026-06-08 markdown. Render's publish dir not cleaned between
builds. Sofia surfaced ask to Juan in session — Clear-build-cache
+ persistent `--cleanDestinationDir` build-command flag. Tracked
as **#266**. After Juan triggers, re-curl:

```
curl -sI "https://aweb.ai/docs/team-bootstrap.md" | grep -i 'http\|last-modified'
```

Expect HTTP 404 (Olivia: no stub). Then mail closure; aweb-aaqe.6
closes when this AND HOLD B both clear.

**HOLD B: hero terminal panel teaches a failing flow.**
`aw chat send-and-wait ami.aweb.ai/pi "hello over there"` at
site/layouts/index.html:34. Independently confirmed: namespace
404 at AWID resolve. Pre-existing on f528b366, NOT introduced by
7c5d2dcd. Direction: ship 7c5d2dcd (no regression), copy fix is
follow-on P1. Routed to Olivia (msg 416cfcd7). Olivia probed
candidates: aweb.ai/aida RESOLVES + accepts mail (probe
63e89b4e); demo.aweb.ai/support + aweb.ai/hello also 404. Olivia
recommends option 1 (provision ami.aweb.ai/pi as live greeter),
routed to Juan. Follow-on iteration through Rose gate.

Sofia pending bank: pre-deploy verify must extend to addresses
named in marketing copy — must RESOLVE and RESPOND at verify-live
time, same standing as released-commands rule. Settles after
ami.aweb.ai/pi fix shape lands.

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

AC v0.5.68 prod (a68dd55a) • aweb PyPI 1.26.13 + aw npm 1.26.13 /
channel 1.4.12 / claude-skills 0.2.12 / Pi 0.1.20 • awid-service
PyPI 0.5.12 + awid GHCR 0.5.12, api.awid.ai verified-live • a2a.aweb.ai
daemon-pending (waiting on Grace first AC route) • aweb.ai
deploy-landing 7c5d2dcd (wake-setup-restore 3/3 atop hero-intent-tabs
3/3 atop blueprint-voice 5/6; HOLDs on team-bootstrap.md staleness +
ami.aweb.ai/pi 404) • marketplace pins: channel 1.4.12 + skills 0.2.12.

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
