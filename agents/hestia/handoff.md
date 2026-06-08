# Hestia Handoff

Crisp wake-up brief. What you need to act NOW, nothing more. For
backstory on anything referenced here, see `logbook.md`. For
operating discipline, see `AGENTS.md`.

**Last updated:** 2026-06-08 00:15 UTC

## Newest finding

**aapz Waves 1-3 verified-live. A2A release train + olivia 27f43d4c
site deploy both moved this session.**

- aapz Wave 1 AWID 0.5.10 → verified-live earlier (api.awid.ai
  flipped, schema migrated)
- aapz Wave 2 aweb 1.26.8 PyPI + aw 1.26.8 npm → verified-live
- aapz Wave 3 AC v0.5.60 → verified-live (Render flipped; site
  canonical at deploy-landing 6da746de)
- aapz Wave 4 (channel 1.4.12 + skills 0.2.12 + Pi 0.1.20 +
  marketplace) was HELD when Grace took the release lane under
  Juan's "drive it through" mandate
- A2A release train at aweb 81e8d01c (AWID 0.5.11 + aweb 1.26.9 +
  aw 1.26.9 + new aweb-a2a-gw gateway binary) — Grace owns lane;
  Grace confirmed AWID 0.5.11 deployed mid-session
- Olivia home hero redesign at ac 27f43d4c → verified-live THIS
  TURN. Site-only deploy (no AC backend bump). CF Pages caught up
  after ~30s build window; live H1 confirms "Let agents work
  together in an open network" with runtime-toggle install panels.
- Sofia ACK'd verified-live mail (two copies — bus retry); Olivia
  not directly addressable from this workspace (`aweb.ai/olivia`
  → 404). Past closure pattern was conversation-thread reply via
  her inbound mail.

## In flight

**A2A wave** — Grace owns. Awaiting her verified-live mail for
aweb/aw 1.26.9 + AWID 0.5.11. Live a2a.aweb.ai routes
(personal/customer-service/research) pending future
ubuntu-8gb-nbg1-1 SSH-assist provisioning that Grace may request.

**aapz Wave 4 closure** — verify status with Grace before any
parallel action; her A2A wave may have folded it.

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
