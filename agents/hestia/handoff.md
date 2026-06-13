# Hestia Handoff

Crisp wake-up brief. What you need to act NOW, nothing more. For
backstory on anything referenced here, see `logbook.md`. For
operating discipline, see `AGENTS.md`.

**Last updated:** 2026-06-13 (early UTC) — a2a-gw-v1.26.19 verified-live;
aaqw + aaqx CLOSED via Rose's stock a2a-sdk python 1.1.0 default-flow proof.
14-release wave closed.

## In flight

**0) a2a-gw-v1.26.19 CLOSED LIVE. #294 done.**

- `/health`: release_tag=a2a-gw-v1.26.19, git_sha=d0baafa3,
  aweb_version=1.26.19, build_date=2026-06-12T23:37:14Z, healthy,
  routes=2, gateway.task_execution=true, identity usable.
- GHA 27449252649 SUCCESS; GHCR ghcr.io/awebai/a2a-gateway:1.26.19
  multi-arch (amd64+arm64) live.
- Rose's proof (Grace msg aa25d60a): real a2a-sdk python 1.1.0,
  stock default flow, no aw CLI, no aweb SDK, NO X-A2A-Task-Token.
  Pre-v1.26.14 token-free GetTask → 'task not found'; post-v1.26.19
  same harness SendMessage task `09b0c2ad-d057-4566-9318-a02ebb100e82`
  → WORKING → polling → TASK_STATE_COMPLETED in ~15s. Answer text:
  Lamb & Flag / Covent Garden tube. Autonomous Watson.
- aweb-aaqw + aweb-aaqx CLOSED.
- Non-blocking ops observation: Watson daemon answer-quality
  needed sonnet model pinning; protocol loop completed regardless.
  NOT a gateway/protocol defect; Watson-side config.
- Render-flip lesson re-banked: image-pinned services don't auto-
  bump :latest. Manual Deploy redeployed v1.26.14 first attempt;
  required Settings → Image URL → explicit pin bump
  (1.26.14 → 1.26.19) → Save.
- Sofia verified-live mail sent (msg 3a51587f) with full 4-point
  check.

**1) #288 aaqs P1 (Grace queue).**

aw directory aweb.ai/<alias> → 404 for all team aliases. AWID has
the record (HTTP 200); AC's network-directory projection endpoint
missing entirely (no /v1/network/directory/{domain}/{name} route in
AC backend per `git grep`). Customer-visible. Grace's lane.

**2) #284 P1 (Athena lane, unchanged).**

AC migration runner must run on Render container start OR via deploy
hook. Until then, every AC ship with a new SQL migration needs the
manual-apply pattern (pgdbm normalization per `runbook.md` b9a9448).

**3) aaqv direction halt (Juan).**

AC-side A2A route management surface — Juan said "this is a surface
we need to eliminate at some point." Direction halt, NOT a release
halt: gate result remains the release call. Don't restart route-
management code work without Juan/Sofia direction read.

**4) HN pre-check burst capacity (#275) — Olivia ready, Juan firing word pending.**

**5) HAL-130226 (tomj.aweb.ai) timeouts — RENDER_API_KEY blocker.**

Juan needs to drop into `~/.aweb-ops/render.env`. Today's Render-
flip incident (Manual-Deploy-vs-pin-bump) is a second proof of why
direct Render API access matters for ops.

## Open holds (don't trip these)

- **#245 aw 1.26.3 workspace-cleanup regression.** Don't ship a CLI
  release that extends `cli/go/cmd/aw/workspace*` cleanup behavior
  until Athena + Mia decide the fix-forward shape.
- **#239 aw 1.27.0 E2EE-default Phase 2.** Don't tag aw-v1.27.0
  without Grace re-route; gated on channel/Pi adoption.
- **#284 AC-migration-runner-not-wired.** Until closed, any AC ship
  with a new SQL migration needs manual apply between GHA-green and
  Render-flip-live, using pgdbm normalization per runbook.
- **aaqv direction halt.** No AC route-management lane work without
  Juan/Sofia direction.

## Live matrix (one line)

AC v0.5.74 prod • aweb PyPI 1.26.19 + aw npm 1.26.19 + GH Release
v1.26.19 (cli DefaultTimeout 30s + team-auth envelope v2)
• a2a-gw GHCR 1.26.19 live at a2a.aweb.ai (d0baafa3) •
pi-extension 0.1.21 • awid-service PyPI 0.5.12 + awid GHCR 0.5.12 •
aweb.ai site 30b90815 (/a2a/ live) • channel 1.4.12 • skills 0.2.12.

## Juan-action queue (real-time)

1. **RENDER_API_KEY** drop into `~/.aweb-ops/render.env` (blocks
   HAL-130226 + Athena hackathon diagnosis + Manual-Deploy-
   image-pin-bump pattern).
2. **HN pre-check burst firing word** when ready (Olivia primary,
   Hestia analyzes).
3. **aaqv direction read** — confirm AC route-management surface
   elimination scope before Athena/Grace restart any related work.

## Wake-up checklist

1. `git pull` in ai.aweb and your sibling repos (aweb, ac).
2. `aw chat pending && aw mail inbox`.
3. `curl -sS https://app.aweb.ai/health` — confirm AC v0.5.74 +
   aweb_version=1.26.18 (NOT 1.26.19; AC pin floor is 1.26.18).
4. `curl -sS https://api.awid.ai/health` — confirm 0.5.12.
5. `curl -sS https://a2a.aweb.ai/health` — confirm a2a-gw-v1.26.19
   + git_sha=d0baafa3.
6. `aw task list --status pending --owner hestia` — open ops
   follow-ups.

## Where to look

- `logbook.md` — historical narrative. 2026-06-13 entries carry the
  a2a-gw-v1.26.19 close-out + Rose's transcript shape; 2026-06-12
  entries carry the 14-release wave + emergency metadata repair +
  policy #17/#18 banking.
- `runbook.md` — release-runbook detail. Standing policies #17
  (never ship failing tests) and #18 (identical labels = consistent
  broken) banked verbatim; pgdbm normalization guard in the
  "Manual schema_migrations metadata recording" subsection.
- `AGENTS.md` — operating discipline.
- `scripts/` — reusable read-only DB probes.
- `artifacts/` — sensitive ops dumps, local-only.
- `~/.aweb-ops/` — chmod 600 secrets directory.

## Discipline you'll regret skipping

- **Never ship with failing tests, ever** (policy #17). "Known
  flake", "matches baseline", "non-regression accept" are NOT
  acceptable framings. Red gate = no ship. Send back to
  Grace/Mia/Olivia/Athena to fix.
- **Sofia's #18 complement**: identical failure labels across
  runs = consistent broken, not flake.
- **Direction halt ≠ release halt.** Don't over-halt when peers
  relay an ambiguous "stop this" from Juan; check the specific
  scope (gate result remains the release call). v0.5.73 over-halt
  is the worked example.
- **Render Manual Deploy doesn't auto-bump image tags.** Pinned
  services need Settings → Image URL bump → Save. :latest needs
  Clear-cache + Deploy.
- **Don't hallucinate live state.** Anchor every production claim
  to a `curl` or Render dashboard read.
- **Bare aliases (grace, olivia) fail.** Use full namespace form
  (`juan.aweb.ai/grace`, `juan.aweb.ai/olivia`). Sofia is
  `aweb.ai/sofia`, Athena is `aweb.ai/athena`. Juan is not an aweb
  agent — surface Juan asks in-conversation.
- **Rose inbound-filter**: `juan.aweb.ai/rose` rejects mail from me
  with 403. Route Rose loops through Grace.
- **Push release tags individually**, never batched (policy #7).
- **Render Static Site publish-dir staleness is real** (#266).
- Per-version `/pypi/aweb/X.Y.Z/json` is canonical signal after
  publish; use `uv lock --refresh-package aweb` when cache lags.
- **Manual migration unblocks MUST use pgdbm normalization** (or
  invoke pgdbm directly). Raw file SHA is wrong. v0.5.71 → v0.5.72
  incident is the worked example.
- **release-verify-migration-immutability is your friend.** Trust
  the gate. Fix the manual path.
- **`/health`'s coordination_schema check is row-presence-only**,
  not a checksum check.
- **Don't overclaim from generic 401/redirect probes.** When
  `/health` doesn't expose a config value, say what the probe
  proves and what it doesn't (Grace's precision guard).
- **Dual-review the fix-forward after any release-gate failure.**
- **Verified-live mails MUST enumerate** (1) what fixed (2) what NOT
  fixed (3) evidence (4) live check.
- **Server-tag-missing recurrence trap**: after each `make ship`,
  double-check `git tag -l "server-v$NEW"` exists.
- **`aw` cwd-bound identity foot-gun**: always run from
  `agents/hestia/` for ops.
- **Mail body size**: keep verified-live mails terse; multi-section
  >2KB bodies can trip edge blocks (HTTP 403).
- **AC-migration manual-apply pattern (until #284 closes)**: any AC
  ship with a new `backend/src/aweb_cloud/migrations/*.sql` will
  lifespan-fail at Render. Use pgdbm normalization per runbook.
- **Route IDs aren't well-known**: A2A gateway routes live at
  `/a2a/agents/<route-id>/agent-card.json` — don't guess the route
  ID for verification probes; defer to the SDK-canonical proof
  shape instead.
