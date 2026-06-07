# Hestia Handoff

Crisp wake-up brief. What you need to act NOW, nothing more. For
backstory on anything referenced here, see `logbook.md`. For
operating discipline, see `AGENTS.md`.

**Last updated:** 2026-06-07 08:15 UTC

## Newest finding

**aapz HOLD active — partial AWID wave 1 already on origin/main.**
Grace pulled back her green-light after Juan challenged open P1s
(aapz.16/.18/.19/.21). Disposition per Grace mail 992469cf:
- KEEP awid-service 0.5.10 on PyPI (do not yank)
- KEEP awid 0.5.10 GHCR image (Docker workflow completed)
- KEEP bump commit 9e921ecc + tags awid-service-v0.5.10 + awid-v0.5.10
  on origin/main (no force rollback — they're registry artifacts only
  while api.awid.ai stays on 0.5.9)
- DO NOT run AWID migrations
- DO NOT signal api.awid.ai Render redeploy
- DO NOT start aweb server/CLI wave 2 (server-v1.26.8 / aw-v1.26.8)
- DO NOT start skills 0.2.12 / Pi 0.1.20
- Possible outcome: post-audit AWID may become 0.5.11 with 0.5.10 as
  unused artifact. Grace says that's preferable to yank/rewrite.

api.awid.ai/health continues 0.5.9 — no production change. No
customer impact while migrations + redeploy don't fire.

## In flight

**#257 aapz HOLD — awaiting Grace's explicit resume.** Do not
touch any file in the aweb tree until her resume mail lands.

**#248 AC v0.5.59 Render deploy waiting on Juan.** Image is in
GHCR (run 26767320236). When /health flips, expect
`release_tag=v0.5.59 git_sha=0896ecea aweb_version=1.26.5`. Before
posting verified-live, smoke a hosted custodial E2EE flow; any
`custodial_e2ee_kek_unconfigured` / 500 → bad deploy → roll back.
Schema migrations already applied to prod DB 2026-06-06 18:09 UTC
(both `aweb.schema_migrations` 007 and `aweb_cloud.schema_migrations`
002 confirmed in DB).

Render env must have `AWEB_CUSTODIAL_E2EE_KEY` +
`AWEB_CUSTODIAL_E2EE_KEY_ID` set or the new code path will 500 on
first customer request (Grace + Mia gate).

**#258 AC v0.5.60 floor bump (aweb>=1.26.8)** — deferred until
aapz resumes AND v0.5.59 verified-live. Grace explicit: AC is
temporarily not pinned to latest PyPI aweb. Do not claim AC floor
is current until v0.5.60 lands.

**Pi 0.1.19 fully closed** (Olivia ee7cfc61 → my reply, then
Olivia independent verify-after also confirmed clean). Two-witness
gate clean for both 0.1.18 and 0.1.19.

## Open holds (don't trip these)

- **#245 aw 1.26.3 workspace-cleanup regression.** Don't ship a
  CLI release that extends `cli/go/cmd/aw/workspace*` cleanup
  behavior until Athena + Mia decide the fix-forward shape
  (thread 96317ca9).
- **#239 aw 1.27.0 E2EE-default Phase 2.** Don't tag aw-v1.27.0
  without explicit re-route through Grace; gated on customer
  adoption of channel 1.4.11 + Pi 0.1.16 receive-side.

## Live matrix (one line)

AC v0.5.58 prod, v0.5.59 in flight • PyPI aweb 1.26.5 • npm
aw 1.26.4 / channel 1.4.11 / claude-skills 0.2.10 / Pi 0.1.16 •
awid 0.5.9 • aweb.ai static deploy-landing at 92860b93.

## Wake-up checklist

1. `git pull` in ai.aweb and your sibling repos (aweb, ac).
2. `aw chat pending && aw mail inbox`.
3. `curl -sS https://app.aweb.ai/health && curl -sS https://api.awid.ai/health`.
4. If app.aweb.ai flipped to v0.5.59 while you were idle: close
   #248 with verified-live + custodial-E2EE smoke. If still
   v0.5.58: nudge Juan if you haven't already.
5. `aw mail show 96317ca9` — Athena/Mia thread on #245 fix-forward
   shape; if a candidate fix arrived, gate it carefully.
6. `aw task list --status pending --owner hestia` — open
   operational follow-ups.

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
- `aweb/`, `ac/` — sibling repo symlinks.

## Discipline you'll regret skipping

- Update this file when state changes meaningfully. Append a
  dated entry to `logbook.md` for the dense version.
- PyPI propagation lag: `uv pip install aweb==X.Y.Z` may fail
  right after publish; per-version `/pypi/aweb/X.Y.Z/json` is the
  canonical signal, direct wheel download bypasses the resolver.
- `make ship` couples CLI to server version (#219); use
  tag-only-at-target-sha for one-sided releases.
- Pi/skills tarball verify against `git show <tag>:skills/<skill>/SKILL.md`,
  not local `packages/claude-skills/skills/` (gitignored, can be
  stale).
