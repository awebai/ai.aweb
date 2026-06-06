# Hestia Handoff

Crisp wake-up brief. What you need to act NOW, nothing more. For
backstory on anything referenced here, see `logbook.md`. For
operating discipline, see `AGENTS.md`.

**Last updated:** 2026-06-06 12:05 UTC

## Newest finding

**@awebai/pi 0.1.18 verified-live (2026-06-06).** Cold-reader Pi
README + marketplace-card description rewrite from b619aca. Bump
commit `fba2108` was narrow (only pi-extension/package.json
staged); unrelated WIP in tree (atomic-address-claim,
team_bootstrap.go, ratelimit.py, dns_addresses.py — flagged by
Olivia as not hers) NOT swept. Content-verify against
`git show b619aca:pi-extension/README.md` and
`git show b619aca:skills/<skill>/SKILL.md` all byte-identical;
Wave 5 sync intact. Sofia/Athena framing review chain bypassed
per explicit Juan author. Verified-live mail
`9d1ff678-e0d5-49c8-84dc-9e0830ff270e` sent to Olivia + Grace +
Athena + Sofia + Iris + Aida; Olivia standing by to run her
independent verify-after diff to close. Logbook entry appended.

**First observed external multi-agent customer in production:**
`default:andi.aweb.ai` BYOT team, registered 2026-06-03 09:44 UTC.
4 agents (coord, dev, review, remoteagent) actively coordinating
across a Hetzner host + one remote-machine federation. 17 mail +
5 chat messages in first hours. See `logbook.md` 2026-06-03
entry for the full read. Mailed Sofia (direction-level signal).

## In flight

**#248 AC v0.5.59 Render deploy waiting on Juan.** Image is in
GHCR (run 26767320236). When /health flips, expect
`release_tag=v0.5.59 git_sha=0896ecea aweb_version=1.26.5`. Before
posting verified-live, smoke a hosted custodial E2EE flow; any
`custodial_e2ee_kek_unconfigured` / 500 → bad deploy → roll back.

Render env must have `AWEB_CUSTODIAL_E2EE_KEY` +
`AWEB_CUSTODIAL_E2EE_KEY_ID` set or the new code path will 500 on
first customer request (Grace + Mia gate).

**Pi 0.1.18 close-out**: Olivia's independent verify-after diff
expected; nothing for you to do unless she surfaces a hash
mismatch (none expected — all 6 file hashes already confirmed
identical to b619aca pre-mail).

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
