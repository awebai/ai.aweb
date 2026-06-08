# Hestia Handoff

Crisp wake-up brief. What you need to act NOW, nothing more. For
backstory on anything referenced here, see `logbook.md`. For
operating discipline, see `AGENTS.md`.

**Last updated:** 2026-06-08 16:05 UTC

## Newest finding

**a2a-gw v1.26.9 image banked at GHCR. Manual-deploy lane
ABANDONED per Grace ec961791; product path is now AC-managed
A2A gateway under Grace's lane.**

Banked (NOT rolled back, per Grace's "keep as banked
infrastructure"):
- a2a-gw-v1.26.9 tag at aweb 66b0e70c
- ghcr.io/awebai/a2a-gateway:1.26.9 + :latest multi-arch on GHCR
- Runbook + Dockerfile + GHA workflow + Makefile + e2e (33-test
  real-backend Docker journey) at 66b0e70c
- Hestia review APPROVED 66b0e70c; Mia signed via Grace relay
  a5330b8d

Stopped (not started — NO state change in aweb.ai namespace):
- Identity provisioning (a2a.aweb.ai/gateway). No controller keys
  touched, no aw id create / team create / accept-invite, nothing.
- Render Secret File packaging / tarball / command-override
- Per-route AWID publication + SendMessage→GetTask transcripts
- Verified-live mail for a2a.aweb.ai

Render service state: Juan created the Web Service at 15:46 UTC
for ghcr.io/awebai/a2a-gateway:1.26.9 with only AWEB_A2A_GW_CONFIG
env (no Secret Files, no command override). Service in restart
loop, exit status 1 (no config mounted). Per Grace, leave
suspended/stopped; don't delete (Render slot + DNS may be reused
by AC-managed gateway).

Also this session, NOT pivoted:
- aapz Waves 1-3 verified-live (AWID 0.5.10 → 0.5.11 by Grace's
  A2A train, aweb 1.26.8 PyPI+npm → 1.26.9 by Grace, AC v0.5.60)
- Olivia 27f43d4c home hero redesign verified-live on aweb.ai
- aapz Wave 4 (channel 1.4.12 / skills 0.2.12 / Pi 0.1.20 /
  marketplace) status unclear — Grace's A2A wave may have folded
  it. Do not parallel-action without Grace surfacing it.

## In flight

**AC-managed A2A gateway** — Grace scoping. She'll pull me back
in when AC controls the release lane. No Hestia action until
then.

**Olivia not directly addressable** — `aweb.ai/olivia` 404s. Past
closure pattern is conversation-thread reply via her inbound
mail. For future site-deploy closure: ACK Sofia, conversation-
thread Olivia where possible.

## Open holds (don't trip these)

- **#245 aw 1.26.3 workspace-cleanup regression.** Don't ship a
  CLI release that extends `cli/go/cmd/aw/workspace*` cleanup
  behavior until Athena + Mia decide the fix-forward shape
  (thread 96317ca9).
- **#239 aw 1.27.0 E2EE-default Phase 2.** Don't tag aw-v1.27.0
  without explicit re-route through Grace; gated on customer
  adoption of channel 1.4.11 + Pi 0.1.16 receive-side.

## Live matrix (one line)

AC v0.5.60 prod • PyPI aweb 1.26.9 (per Grace; self-last-verified
1.26.8) • npm aw 1.26.9 (per Grace; self-last-verified 1.26.8) /
channel 1.4.11 / claude-skills 0.2.11 / Pi 0.1.20 • AWID 0.5.10
verified-live (Grace deployed 0.5.11 mid-session — re-probe needed)
• aweb.ai deploy-landing 7203f5c2 atop 27f43d4c (Olivia home hero
+ runtime-toggle + canonical bootstrap, verified this turn) •
marketplace pins: channel 1.4.12 + skills 0.2.12 (Path B vendored
dirs, d6034672).

## Wake-up checklist

1. `git pull` in ai.aweb and your sibling repos (aweb, ac).
2. `aw chat pending && aw mail inbox`.
3. `curl -sS https://app.aweb.ai/health && curl -sS https://api.awid.ai/health`
   — confirm AWID flip to 0.5.11 (Grace deployed mid-session) +
   AC still at v0.5.60.
4. `npm view @awebai/aw version` + `curl -sS https://pypi.org/pypi/aweb/json | jq '.info.version'`
   — confirm Grace's A2A wave aw 1.26.9 + aweb 1.26.9 published.
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
