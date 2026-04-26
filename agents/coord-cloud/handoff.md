# Coordinator aweb-cloud (Tom) — Handoff

Last updated: 2026-04-26 (post-v0.5.8 ship; v0.5.9 cleanup held +
test-infra fix landed)

## Current state

**ac main:** 2 commits ahead of origin/main, both unpushed:
- `4f31e116` — test-infra fix (compose port-collision + bootstrap script)
- `b5b1ee1f` — Grace's v0.5.9 architectural cleanup (parallel-registry
  dead-code removal)
- on top of `0336a2c4` (v0.5.8 release tag, shipped)

**aweb (Grace's side):** `32bb7c6` local, unpushed. Amend of `ee72ee3`
that folds John's N1+N2 wording notes (clearer error message:
"AWID_REGISTRY_URL=local is not supported; set
AWID_REGISTRY_URL=https://api.awid.ai"). Pure text change, no logic
delta — substance identical to ee72ee3.

**Production:** v0.5.8 live since 2026-04-26 ship. Verified-live leg 1
(/health flip + git_sha) confirmed at ship. Legs 2-3 pending (see below).

## Held push state — three commits, all coord-GO'd

| Commit | Repo | Author-coord | Reviewer-coord | Status |
|--------|------|--------------|----------------|--------|
| 32bb7c6 | aweb | Grace | John (3851604d, fd32df1c) | GO, holding |
| b5b1ee1f | ac | Grace | Tom | GO, holding |
| 4f31e116 | ac | Tom (auto) | n/a (test infra) | self-merged, holding |

All three are parked pending verified-live legs 2-3 per Randy's
ship-discipline. Coord-GO chain is complete; waiting only on production
verification.

## What's blocking push: verified-live legs 2-3

Per Randy's 5bd0b2c6 + 7d8f9efb (locked):
1. **Leg 2 (dashboard path)**: Juan triggers a dashboard send from
   app.aweb.ai (he's logged in). Recipient should be a hosted-custodial
   multi-membership identity (juan.aweb.ai/randy works). I read the
   recipient JSON inbox via `aw mail inbox --show-all --json` and
   confirm `verification_status=verified`.
2. **Leg 3 (CLI path)**: Amy upgrades aweb CLI 1.18.2 + channel 1.3.3,
   restarts Claude Code, sends a fresh CLI mail. Same JSON-inbox check.

When both green:
1. I signal Grace (chat) — push GO.
2. Grace pushes aweb 32bb7c6, I push ac (b5b1ee1f + 4f31e116 in same
   `git push origin main`).
3. Randy mails KI#1 wholesale closure (dashboard + CLI paths both
   verified post-v0.5.8).

## Test-infra fix (4f31e116) — context

Today (2026-04-26), Juan asked "are all the docker-backed e2e user
journey scripts working?" + "we have to test all... never say again
that something requires manual-running anything." Surveyed the full
Makefile gate matrix and ran all 7. Outcome:

| Gate | Result |
|------|--------|
| test-backend (full) | 1170 passed |
| test-frontend | 96 passed |
| test-two-service | 11 passed |
| test-cloud-user-journeys-local-aw | 138 passed + 4 Playwright |
| test-cloud-user-journeys-installed-aw | 138 passed + 4 Playwright |
| test-frontend-e2e | 4 Playwright passed |

**Bug 1 (script-fix in 4f31e116)**: `make test-cloud-user-journeys-local-aw`
was broken under make. Root cause: ac/Makefile:16 has bare `export`
which leaks Make's `?=` defaults (`AWEB_CLOUD_PORT=8001`) into the
script's shell. Docker Compose's variable interpolation puts shell-env
> --env-file, so `.env.e2e`'s random-port value was silently ignored;
api bound to 8001, host curl to random port timed out. Direct-run
(no make) was green. Fix: `compose_local()` now explicitly exports
the random ports on every `docker compose` invocation. Banked memory:
`feedback_compose_var_interpolation_make_export.md`.

**Bug 2 (new bootstrap script in 4f31e116)**: `make local-container`
needed a `.env.local-container` that the repo doesn't ship — only
`.env.local-container.example` with `REPLACE_WITH_*` placeholders that
fail config validators. Added `scripts/bootstrap-local-container-env.sh`
which generates a working file: random secrets, blanked optional
secrets (OAuth/Stripe/AWS/Sentry), plus `AWEB_PARENT_CONTROLLER_KEY`
and `AWEB_CUSTODY_KEY` for hosted-identity flows.

**Follow-up not done yet**: `make local-container` still doesn't
auto-bootstrap the AWID parent namespace (the journey script does this
internally via `bootstrap_awid_parent_namespace`). Worth folding into
the Makefile target so frontend-e2e is one command from a fresh
checkout. P3.

## Lane state

- **Grace**: holding push on aweb 32bb7c6. Reachable on chat. No
  active dispatch.
- **John**: GO on 32bb7c6 sent (fd32df1c, ack-mailed back). Likely
  also holding for legs 2-3 verified-live. May have moved on to
  next aweb work.
- **Mia**: still offline; stand-down dispatch from earlier session
  remains moot.
- **Tom (me)**: dormant pending verified-live signals. Watch chat +
  mail.

## What to check FIRST on next wake-up

1. Mail/chat for Juan signaling leg 2 (dashboard send executed).
2. Mail from Amy on leg 3 (CLI re-test result).
3. Mail from Randy if KI#1 closure already happened (would mean
   legs 2-3 already passed and the wholesale closure landed).
4. `aw workspace status` — Grace's state. If she's idle and verified-live
   landed, push.
5. Time-bound carry: GHA Node 20 actions deprecation by 2026-06-02
   (still pending, ~5 weeks out).

## Open ac branches

- `main` at `4f31e116` (local) / `0336a2c4` (origin) — see "ac main"
  above for the 2-commit gap.
- `aaga-archive` — remote-only; preserved per Randy's note.

## Memory file count

20 memories indexed in MEMORY.md (was 19; added
`feedback_compose_var_interpolation_make_export.md` today).

## Joint coord-protocol amendment to Randy (still parked)

Tom + John convergence on the two-layer canonical+degraded coord-borrow
protocol: opt-in handshake + 60s opt-out floor. Plan unchanged: submit
after v0.5.8 + v0.5.9 wholesale close. Anchor: now 4 coord-borrows
(aala.10, aaja.6, aalf, plus the Grace v0.5.9 cleanup which followed
the same shape).
