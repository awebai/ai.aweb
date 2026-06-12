# Hestia Handoff

Crisp wake-up brief. What you need to act NOW, nothing more. For
backstory on anything referenced here, see `logbook.md`. For
operating discipline, see `AGENTS.md`.

**Last updated:** 2026-06-12 (evening) UTC

## In flight

**0) AC v0.5.72 verified-live + aaqa.20 CLOSED LIVE. #287 done.**

- `/health`: release_tag=v0.5.72, git_sha=eee9bf1a, aweb_version=1.26.17,
  coordination_schema up_to_date.
- Peer ACKs: Grace, Athena, Olivia (security pass), Sofia (framing).
- Rose's london `aw id request --team-auth` proof against
  app.aweb.ai from watson BYOT workspace cleared live (msg
  6eaa6c6c via Grace):
  - v2 floor enforced: aw 1.26.16 → 401 'unsupported team-auth
    envelope version'; 1.26.17 opens.
  - v2 signed-audience canonicalization to https://app.aweb.ai
    PROVEN LIVE: GET /api/v1/tasks --team-auth → 200.
  - Raw method+path binding survives Cloudflare + Render +
    mount proxy chain.
  - aaqa.19 team-principal A2A route management end-to-end live:
    GET /routes no team_id → 200 derive-from-credential; cross-team
    explicit team_id → 403 (fails closed); own derived → 0 routes;
    POST create watson route → 200; enable → 200 enabled=true.
- New P2 from Rose: explicit canonical team_id query on GET
  /routes not resolved before UUID comparison. Customer scripts
  should OMIT team_id and derive from credential (workaround
  noted for aaqa.18/demo scripts per Grace's closure ACK msg
  32710076). Source fix is Olivia/Grace surface.
- Side effect: london.juanreyero.com/watson route now exists
  in prod (unsigned/not-published tier, enabled). KEEP as
  first london demo route per Grace's direction. Sofia's
  boundary (msg 70ab707c): does NOT appear in external claims
  or copy until someone explicitly decides it's a customer-
  facing example; if/when that decision lands it goes through
  policy #14 (resolve+respond) like every named artifact.
- Sofia framing pass (msg 70ab707c) APPROVED full external
  claim shape: v0.5.72 + aweb 1.26.17 + v2 envelope verifier
  as ONE customer-facing surface; team-principal A2A route
  management live end-to-end; v2 floor with clean 401 on
  older clients. Boundary: this is auth/routing surface, NOT
  a messaging-privacy claim — does NOT change E2EE wording
  rules.
- Closure mails: Grace 6ae262da, Athena b2296ba9, Olivia
  c564f98a, Sofia 0685505d (her framing-pass ACK: 70ab707c).

**1) Emergency-metadata-repair (v0.5.71/v0.5.72 incident, banked + closed).**

- v0.5.71 manual unblock recorded raw-sha256 (fe0bd0aa…) for
  migration 005 instead of pgdbm-normalized (735b07e7…).
- v0.5.72 release-ready gate caught it correctly.
- Recovery: single guarded UPDATE on aweb_cloud.schema_migrations
  id=5, treated as audited emergency metadata repair per
  Juan's ratification. No DDL or migration file bytes changed.
- Source-controlled process guard at ai.aweb b9a9448
  (agents/hestia/runbook.md): manual unblocks must use
  `python -m aweb_cloud.cli migrate` or the
  `create_cloud_migration_manager` / `apply_cloud_migrations`
  helpers; raw file SHA explicitly called out as wrong.

**2) Olivia's 3 low-sev follow-ups filed (msgs 472dbe37 + 62cfa826).**

- aweb-aaqp (P3): A2A team-auth require v2 envelope (no v1
  downgrade / replay protection). Gates on aw 1.27.0
  customer-adoption thresholds; folds into #239 hold context.
- aweb-aaqq (P4): Auth bridge non-UUID team_id 500 on
  UNauthenticated public-reader path → should be clean 4xx.
- aweb-aaqr (P2): AUTHENTICATED team-cert GET /routes:
  `_handle_team_certificate_request` compares the RAW
  candidate_team_id query param against the server UUID
  (auth_bridge.py L1986), so a canonical domain/name team_id
  403s even when it IS the right team. Wrong-403 correctness
  bug. Fix shape: resolve candidate_team_id to server uuid
  (or match cert_context.team_address) before the compare —
  aligns the bridge with the router's
  `_resolve_a2a_team_identifier`. Confirms the
  omit-team_id/derive-from-credential workaround.
- All three reference thread d24c717c so the security-pass
  context is recoverable.

**3) #284 P1 (Athena lane, unchanged).**

AC migration runner must run on Render container start OR via
deploy hook. Until then, every AC ship with a new SQL migration
needs the manual-apply pattern banked in `runbook.md` (which now
uses pgdbm normalization per b9a9448).

**4) HN pre-check burst capacity (#275) — Olivia ready, Juan firing word pending.**

**5) HAL-130226 (tomj.aweb.ai) timeouts — RENDER_API_KEY blocker.**

Juan needs to drop into `~/.aweb-ops/render.env`.

## Open holds (don't trip these)

- **#245 aw 1.26.3 workspace-cleanup regression.** Don't ship a
  CLI release that extends `cli/go/cmd/aw/workspace*` cleanup
  behavior until Athena + Mia decide the fix-forward shape.
- **#239 aw 1.27.0 E2EE-default Phase 2.** Don't tag aw-v1.27.0
  without Grace re-route; gated on channel/Pi adoption.
- **#284 AC-migration-runner-not-wired.** Until closed, any AC
  ship with a new SQL migration needs manual apply between
  GHA-green and Render-flip-live, using pgdbm normalization
  per runbook.

## Live matrix (one line)

AC v0.5.72 prod (eee9bf1a) • aweb PyPI 1.26.17 + aw npm 1.26.17 +
GH Release awebai/aw v1.26.17 (team-auth envelope v2)
• a2a-gw GHCR 1.26.14 • pi-extension 0.1.21 • awid-service PyPI
0.5.12 + awid GHCR 0.5.12, api.awid.ai verified-live • aweb.ai
site 30b90815 (/a2a/ live) • channel 1.4.12 • skills 0.2.12.

## Juan-action queue (real-time)

1. **RENDER_API_KEY** drop into `~/.aweb-ops/render.env`
   (blocks HAL-130226 + Athena hackathon diagnosis).
2. **HN pre-check burst firing word** when ready
   (Olivia primary, Hestia analyzes).

## Wake-up checklist

1. `git pull` in ai.aweb and your sibling repos (aweb, ac).
2. `aw chat pending && aw mail inbox`.
3. `curl -sS https://app.aweb.ai/health` — confirm AC v0.5.72 +
   aweb_version=1.26.17 + git_sha=eee9bf1a.
4. `curl -sS https://api.awid.ai/health` — confirm 0.5.12.
5. `curl -sS https://a2a.aweb.ai/health` — gateway health.
6. `aw task list --status pending --owner hestia` — open ops
   follow-ups.
7. **If Rose has posted her london `aw id request --team-auth`
   proof transcript** while idle: read it; if green, mail
   verified-aaqa.20-closed to Grace + Rose + Olivia (citing her
   transcript the same way hero-probe-0610 was cited per Sofia
   msg 84853a2d); update task #287 to completed.

## Where to look

- `logbook.md` — historical narrative, ship summaries, banked
  lessons, customer-activity reads. The 2026-06-12 entries
  carry the v0.5.71→0.5.72 ladder + the audited emergency
  metadata repair shape verbatim.
- `runbook.md` — release-runbook detail. **NEW (b9a9448)**:
  the "Manual schema_migrations metadata recording" banked
  subsection. Read before any future manual unblock.
- `AGENTS.md` — operating discipline.
- `scripts/` — reusable read-only DB probes.
- `artifacts/` — sensitive ops dumps, local-only.
- `~/.aweb-ops/` — chmod 600 secrets directory.

## Discipline you'll regret skipping

- **Never echo full DATABASE_URL or AWEB_CUSTODIAL_E2EE_KEY** to
  chat — secrets land in `~/.aweb-ops/` files chmod 600.
- **Don't hallucinate live state.** Anchor every production
  claim to a `curl` or Render dashboard read.
- **Bare aliases (grace, olivia) fail.** Use full namespace form
  (`juan.aweb.ai/grace`, `juan.aweb.ai/olivia`). Sofia is
  `aweb.ai/sofia`, Athena is `aweb.ai/athena`.
- **Rose inbound-filter**: `juan.aweb.ai/rose` rejects mail
  from me with 403. Route Rose loops through Grace.
- **Push release tags individually**, never batched (policy #7).
- **Render Static Site publish-dir staleness is real** (#266).
- Per-version `/pypi/aweb/X.Y.Z/json` is canonical signal after
  publish; use `uv lock --refresh-package aweb` when cache lags.
- **Manual migration unblocks MUST use pgdbm normalization** (or
  invoke pgdbm directly). See runbook 'NEW' section. Raw file
  SHA is wrong. v0.5.71 → v0.5.72 incident is the worked
  example.
- **release-verify-migration-immutability is your friend.** It
  caught my v0.5.71 checksum drift. Trust the gate. Fix the
  manual path.
- **`/health`'s coordination_schema check is row-presence-only**,
  not a checksum check. Don't conclude from
  `coordination_schema=up_to_date` that checksums are right.
- **Don't overclaim from generic 401/redirect probes.** When
  `/health` doesn't expose a config value, say what the probe
  proves and what it doesn't (Grace's precision guard,
  2026-06-12). Defer to surface-exercising tests.
- **Dual-review the fix-forward after any release-gate failure**
  (Juan's banked discipline from the 0bf8d3df fix-forward).
- Verified-live mails MUST enumerate (1) what fixed (2) what NOT
  fixed (3) evidence (4) live check.
- **Server-tag-missing recurrence trap**: after each `make ship`,
  double-check `git tag -l "server-v$NEW"` exists.
- **`aw` cwd-bound identity foot-gun**: always run from
  `agents/hestia/` for ops.
- **Mail body size**: keep verified-live mails terse; multi-section
  >2KB bodies can trip edge blocks (HTTP 403).
- **AC-migration manual-apply pattern (until #284 closes)**:
  any AC ship with a new `backend/src/aweb_cloud/migrations/*.sql`
  will lifespan-fail at Render. Use pgdbm normalization per
  runbook NEW section.
