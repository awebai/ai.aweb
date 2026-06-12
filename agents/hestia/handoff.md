# Hestia Handoff

Crisp wake-up brief. What you need to act NOW, nothing more. For
backstory on anything referenced here, see `logbook.md`. For
operating discipline, see `AGENTS.md`.

**Last updated:** 2026-06-12 ~20:00 UTC

## In flight

**1) AC v0.5.70 verified-live (aaqa.17 self-custodial A2A publish handoff). #282 CLOSED.**

- `/health`: release_tag=v0.5.70, aweb_version=1.26.16,
  awid_service=0.5.12, git_sha=32ad3495, mode=saas, healthy;
  coordination_schema up_to_date.
- release-ready: 306 passed, 2 pre-existing E2EE chat e2e flakes
  (same shape as v0.5.69, tracked separately).
- focused `test_a2a_gateway_routes.py` 33/33 green — covers
  self-custodial publish-shows-local-handoff, hosted-custodial
  audit row, no-live-copy-implies-AWID-published-until-Refresh.
- Athena independently verified `/health` + `/dashboard/a2a`
  HTTP 200, accepted as verified-live with noted limits
  (msg 1ee295f9, 2026-06-12).
- Closure mails sent to athena (a37c29c8), juan.aweb.ai/grace
  (1db7922d), juan.aweb.ai/olivia (2fbe2aa4).

**2) Today's earlier release wave (all verified-live + closed):**

- pi-extension 0.1.21 (Pi runtime; aweb 1e8025be).
- AC v0.5.69 (A2A bridge live blocker fix + aweb 1.26.14 pin).
- a2a-gw-v1.26.14 GHCR image (aaqa.11 follow-on).
- aw 1.26.15 (A2A CLI task-token persistence).
- /a2a/ site page (ac 30b90815, Olivia A2A product preview).
- aw 1.26.16 (aweb-aaqm venue WiFi/NAT hardening).
- AC v0.5.70 (above).

Server-side gap closures (recurrence trap): server-v1.26.14 and
server-v1.26.16 tags missing on first push, retroactively tagged
at 4518c85c + 12d08390 respectively. Watch this on next ship.

**3) HN pre-check burst capacity (#275) — Olivia ready, Juan firing word pending.**

Adversarial smoke 8/8 + P9 autonomous escalation passed
(aaqe.7 fully closed). Burst test staged behind a Juan trigger;
when Juan fires the word, Olivia executes and I analyze.

**4) HAL-130226 (tomj.aweb.ai) intermittent timeouts — RENDER_API_KEY blocker.**

24h+ open. Still on `~/.aweb-ops/render.env` — Juan needs to drop
the key for me to pull Render logs (also Athena hackathon
PATCH-timeout log diagnosis). Independent of release waves.

## Open holds (don't trip these)

- **#245 aw 1.26.3 workspace-cleanup regression.** Don't ship a
  CLI release that extends `cli/go/cmd/aw/workspace*` cleanup
  behavior until Athena + Mia decide the fix-forward shape.
- **#239 aw 1.27.0 E2EE-default Phase 2.** Don't tag aw-v1.27.0
  without Grace re-route; gated on channel/Pi adoption.

## Live matrix (one line)

AC v0.5.70 prod (32ad3495) • aweb PyPI 1.26.16 + aw npm 1.26.16
• a2a-gw GHCR 1.26.14 • pi-extension 0.1.21 • awid-service PyPI
0.5.12 + awid GHCR 0.5.12, api.awid.ai verified-live • a2a.aweb.ai
gateway in run state per aaqa.17 publish handoff • aweb.ai site
30b90815 (/a2a/ product preview page live) + c983ff27 (em-dash
voice sweep) • channel 1.4.12 • claude-skills 0.2.12.

## Juan-action queue (real-time)

1. **RENDER_API_KEY** drop into `~/.aweb-ops/render.env`
   (blocks HAL-130226 log pull + Athena hackathon diagnosis).
2. **HN pre-check burst firing word** when ready
   (Olivia primary, Hestia analyzes).

## Wake-up checklist

1. `git pull` in ai.aweb and your sibling repos (aweb, ac).
2. `aw chat pending && aw mail inbox`.
3. `curl -sS https://app.aweb.ai/health` — confirm AC v0.5.70 +
   aweb_version=1.26.16 + git_sha=32ad3495.
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
- **Push release tags individually**, never batched (banked
  policy #7 — coalescing event silently drops triggers).
- **Render Static Site publish-dir staleness is real** (#266).
  Don't trust "site mod removed" without re-curling.
- Per-version `/pypi/aweb/X.Y.Z/json` is canonical signal after
  publish; `uv pip install aweb==X.Y.Z` may lag; use
  `uv lock --refresh-package aweb` when cache lags.
- Verified-live mails MUST enumerate (1) what fixed (2) what NOT
  fixed (3) evidence (4) live check — missing #2 is the recurring
  slip.
- **Server-tag-missing recurrence trap**: after each `make ship`
  cycle, double-check `git tag -l "server-v$NEW"` exists before
  declaring server-side verified-live.
- **`aw` cwd-bound identity foot-gun**: every `aw` invocation
  signs as whatever workspace `.aw/workspace.yaml` resolves from
  CWD. Always run from `agents/hestia/` for ops; never from
  sibling repos.
- **Mail body size**: very long bodies (multi-section >2KB) can
  trip edge blocks (HTTP 403 'Blocked' page). Keep terse; split
  into multiple mails if needed.
