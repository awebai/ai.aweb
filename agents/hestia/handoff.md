# Hestia Handoff

Crisp wake-up brief. What you need to act NOW, nothing more. For
backstory on anything referenced here, see `logbook.md`. For
operating discipline, see `AGENTS.md`.

**Last updated:** 2026-06-12 (late) UTC

## In flight

**1) AC v0.5.71 verified-live (aaqa.19 team-principal A2A route management). #283 CLOSED.**

- `/health`: release_tag=v0.5.71, aweb_version=1.26.16,
  awid_service=0.5.12, git_sha=980d027f, mode=saas, healthy;
  coordination_schema up_to_date.
- Migration 005_a2a_route_principal_audit.sql applied manually
  (sha256 fe0bd0aa, applied_by hestia_manual_v0.5.71_unblock,
  111ms, id=5) — see logbook 2026-06-12 (late) for full
  pre/post-verify trail.
- Athena ack'd (msg 6eaf9fa6). Grace ack'd (msg ec195c52);
  aaqa.19 stays open pending Rose's positive customer-shape
  exercise of aaqa.18 without `--team-uuid` + `AC_USER_JWT`.

**2) #284 P1: AC migrations must run on Render container start OR via deploy hook.**

- #109 (longstanding) hit in prod for first time on v0.5.71 ship —
  container failed lifespan startup on pending 005. v0.5.70 served
  through; manual apply unblocked; Manual Deploy clicked v0.5.71
  live.
- Athena lane. Bank into pre-deploy step from now on: "if ship
  adds a new SQL migration, plan manual apply between GHA-green
  and Render-flip" until #284 closes.

**3) Today's wave (all verified-live + closed):**

pi-extension 0.1.21 → AC v0.5.69 → a2a-gw-v1.26.14 → aw 1.26.15 →
/a2a/ site → aw 1.26.16 → AC v0.5.70 → AC v0.5.71. Server-tag-missing
recurrence trap caught + fixed twice (server-v1.26.14 at 4518c85c,
server-v1.26.16 at 12d08390).

**4) HN pre-check burst capacity (#275) — Olivia ready, Juan firing word pending.**

Adversarial smoke 8/8 + P9 autonomous escalation passed
(aaqe.7 fully closed). Burst test staged behind a Juan trigger.

**5) HAL-130226 (tomj.aweb.ai) intermittent timeouts — RENDER_API_KEY blocker.**

24h+ open. Still on `~/.aweb-ops/render.env` — Juan needs to drop
the key for me to pull Render logs (also Athena hackathon
PATCH-timeout log diagnosis). Independent of release waves.

## Open holds (don't trip these)

- **HOLD aaqa.20 / AC 356b0325** (Grace explicit msg
  4a2a75a7, 2026-06-12 late). Do NOT release this SHA. Rose
  approved a narrow compatibility patch but Olivia's
  first-principles review raised the bar: .20 needs shared/
  versioned v2 team-auth envelope spec + shared OSS aweb
  verifier consumed by both aweb server and AC + Go-generated
  vectors + mounted/root_path/aud/raw-path tests + security
  sign-off. Wait for Grace's fresh reviewed release handoff.
- **#245 aw 1.26.3 workspace-cleanup regression.** Don't ship a
  CLI release that extends `cli/go/cmd/aw/workspace*` cleanup
  behavior until Athena + Mia decide the fix-forward shape.
- **#239 aw 1.27.0 E2EE-default Phase 2.** Don't tag aw-v1.27.0
  without Grace re-route; gated on channel/Pi adoption.
- **#284 AC-migration-runner-not-wired.** Until closed, any AC
  ship with a new SQL migration needs manual apply between
  GHA-green and Render-flip-live (or container will lifespan-fail
  on `_assert_coordination_schema_ready`).

## Live matrix (one line)

AC v0.5.71 prod (980d027f) • aweb PyPI 1.26.16 + aw npm 1.26.16
• a2a-gw GHCR 1.26.14 • pi-extension 0.1.21 • awid-service PyPI
0.5.12 + awid GHCR 0.5.12, api.awid.ai verified-live • a2a.aweb.ai
gateway in run state per aaqa.17 publish handoff • aweb.ai site
30b90815 (/a2a/ live) + c983ff27 • channel 1.4.12 • skills 0.2.12.

## Juan-action queue (real-time)

1. **RENDER_API_KEY** drop into `~/.aweb-ops/render.env`
   (blocks HAL-130226 + Athena hackathon diagnosis).
2. **HN pre-check burst firing word** when ready
   (Olivia primary, Hestia analyzes).

## Wake-up checklist

1. `git pull` in ai.aweb and your sibling repos (aweb, ac).
2. `aw chat pending && aw mail inbox`.
3. `curl -sS https://app.aweb.ai/health` — confirm AC v0.5.71 +
   aweb_version=1.26.16 + git_sha=980d027f.
4. `curl -sS https://api.awid.ai/health` — confirm 0.5.12.
5. `curl -sS https://a2a.aweb.ai/health` — gateway health.
6. `aw task list --status pending --owner hestia` — open ops
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
- `~/.aweb-ops/` — chmod 600 secrets directory.

## Discipline you'll regret skipping

- **Never echo full DATABASE_URL or AWEB_CUSTODIAL_E2EE_KEY** to
  chat — secrets land in `~/.aweb-ops/` files chmod 600 then get
  referenced by env-name only.
- **Don't hallucinate live state.** Anchor every production
  claim to a `curl` or Render dashboard read.
- **Bare aliases (grace, olivia) fail.** Use full namespace form
  (`juan.aweb.ai/grace`, `juan.aweb.ai/olivia`). Sofia is
  `aweb.ai/sofia`, Athena is `aweb.ai/athena`.
- **Rose inbound-filter**: `juan.aweb.ai/rose` rejects mail
  from me with 403 'Local recipient only accepts same-team,
  exact-contact, or stored-route continuation delivery'. Route
  Rose loops through Grace.
- **Push release tags individually**, never batched (banked
  policy #7).
- **Render Static Site publish-dir staleness is real** (#266).
- Per-version `/pypi/aweb/X.Y.Z/json` is canonical signal after
  publish; use `uv lock --refresh-package aweb` when PyPI cache
  lags.
- Verified-live mails MUST enumerate (1) what fixed (2) what NOT
  fixed (3) evidence (4) live check — missing #2 is the recurring
  slip.
- **Server-tag-missing recurrence trap**: after each `make ship`,
  double-check `git tag -l "server-v$NEW"` exists before
  declaring server-side verified-live.
- **`aw` cwd-bound identity foot-gun**: every `aw` invocation
  signs as whatever workspace `.aw/workspace.yaml` resolves from
  CWD. Always run from `agents/hestia/` for ops.
- **Mail body size**: very long bodies (multi-section >2KB) can
  trip edge blocks (HTTP 403 'Blocked' page). Keep terse; split
  into multiple mails if needed.
- **AC-migration manual-apply pattern (until #284 closes)**:
  any AC ship with a new `backend/src/aweb_cloud/migrations/*.sql`
  will lifespan-fail at Render. Between GHA-green and clicking
  Manual Deploy: read the SQL, substitute `{{schema}}` →
  `aweb_cloud`, apply body + insert `aweb_cloud.schema_migrations`
  row (filename, sha256 checksum, module_name='aweb_cloud',
  applied_by) inside a single transaction with pre/post-verify
  guards. v0.5.71 sequence is the worked example
  (logbook 2026-06-12 late).
