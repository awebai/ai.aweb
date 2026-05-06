# Hestia Handoff

Last updated: 2026-05-06 08:30 CEST (post v0.5.23 verified-live + epic
closed; all three pagination probes green including 70f1c868)

## Read this first

You are Hestia. You carry every release across the build/ship boundary
and keep the company machinery healthy in between.

The 2026-05-04 → 2026-05-06 cycle is **closed end-to-end**:

- aame epic shipped: aweb 1.20.0 + 1.20.1 (PyPI), aw 1.20.0 + 1.20.1
  (npm + GH Releases), AC v0.5.22 (deployed).
- Pagination fix shipped: aweb 1.20.2 (PyPI + npm), AC v0.5.23
  (deployed at app.aweb.ai 2026-05-06 06:14:33Z).
- Verified-live on three probe shapes including 70f1c868 (the
  exact 409 case that drove 1.20.2). Athena, Sofia, Aida ack'd.

The team:

- **Sofia**: direction. Mid-cycle confirmed both v0.5.22 and v0.5.23
  framing. Distribution-framing-ladder ask is in her lane post-cycle.
- **Athena**: code in aweb and ac. Open ops follow-up: grep aweb
  codebase for direct cp.agent_id comparisons (multi-team agent
  class). Bandwidth-allowing. Acknowledged epic closure (cc1bf154).
- **Mia / Noah / Grace / Kate**: dev team (`aweb:juan.aweb.ai`).
  Grace authored the 1.20.2 fix per Athena's brief.
- **Aida**: support, online. Local commit 30c8870 (chat-403 +
  BYOD-422 entries + name-the-answer-not-the-team-set invariant)
  held awaiting Juan's go-to-push. Two triage hints from this cycle
  banked for her discipline pass.
- **Iris / Metis**: not yet registered (Hetzner identity bootstrap
  pending for Iris).

## Identity (live since 2026-05-01 21:05 UTC)

- did: `did:key:z6MkebRpF7qEFNt5vAYa5BWjegFk1igt6mRESqWb5r3kp9AK`
- stable: `did:aw:3fC4cfvFuVAxZCWyJNRCoUxHVAim`
- address: `aweb.ai/hestia` (reachability=nobody)
- active team: `default:aweb.ai`

## What's live (verified 2026-05-06 06:14:33Z)

- **ac**: v0.5.23 at app.aweb.ai,
  git_sha=`7705fc7ce93d17caf2cd7615984e6f0f4412094f`,
  aweb_version=1.20.2, awid_service_version=0.5.4. Started
  2026-05-06T06:14:33Z.
- **aw CLI**: 1.20.2 published on npm (`@awebai/aw`) and GH Releases.
- **aweb server**: 1.20.2 on PyPI (latest, simple index ✓).
- **awid registry**: 0.5.4 at api.awid.ai. Healthy.
- **channel**: 1.4.0 on npm.

## Banked into runbook this cycle (2026-05-04 → 2026-05-06)

Six new disciplines (#18-23):

- **#18**: verified-live cites actually-committed SHA, not bumped-
  but-unreverified SHA.
- **#19**: work in flight (uncommitted bumps, in-progress procedures)
  ≠ released until tag pushed + live-verified.
- **#20**: reproducer must match empirical surface (CLI 409
  reproducer must surface 409 from prod CLI vs prod server, not
  just unit-test logic).
- **#21**: bless-and-run from peer = run FULL release-ready chain
  end-to-end. Don't shortcut to bump+tag.
- **#22**: code-reviewer subagent flagged silent-fall-through +
  scale realistic for production trajectory ⇒ blocker, not
  follow-up. Banked from Mia's >100-conversation pagination flag
  on the 1.20.0 round.
- **#23**: test failures recurring at specific clock windows +
  reruns clean later are date/timezone-math signals, NOT transient-
  flake signals. "It passed on rerun" is not a diagnosis. Banked
  from admin_analytics local-vs-UTC midnight; Juan's pushback
  closed the loop on the "transient seed" framing.

Schema-gotcha class also banked (not numbered — runbook §Schema
gotchas pending): `aweb.agents`, `aweb.teams`, `aweb.chat_sessions`
lack `updated_at`. `aweb.chat_sessions` also lacks `expires_at`.
Verify column existence before any cleanup procedure assumes
pgdbm-style timestamps.

## Empirical attestation — pagination fix (verified-live)

Three smoke probes against deployed v0.5.23 + 1.20.2:

1. **Baseline auto-thread** — 96317ca9 (athena↔hestia, page-1).
   Probe 5707b48e attached. Athena ack mail 20a6bf7e.
2. **Stale-by-recency from default-team** — 878c06b1 (sofia↔hestia,
   originated 2026-05-05, pushed off page 1). Probe 37c5cb9e
   attached. Sofia ack mail c2e65335.
3. **Stale-by-recency from cross-team-agent** — 70f1c868
   (sofia↔athena, athena's default-team agent_id). The exact 409
   case driving 1.20.2. Athena's probe 72669b66 attached. Mail
   607dc80d.

## Open follow-ups (Hestia's lane)

1. **Watch for next release cycle.** Gate chain holds; immutability
   + #21 + #23 disciplines all live.
2. **Sofia's distribution-framing ladder.** When she signals ready,
   route to Iris (when registered) or Eugenie per her call.
3. **Multi-team agent_id-vs-did follow-up** — Athena's lane;
   surface re-flags this if another customer bug trails the same
   root cause.
4. **admin_analytics test fix at b7e86745** — lives on main, ships
   with next AC release. No separate v0.5.24 for that.
5. **Aida's runbook PR (commit 30c8870)** — pushed when Juan OKs.
   When pushed, cite ref in operations.md.
6. **Iris agent registration** when Hetzner bootstrap completes.
7. **Asymmetric compat-test gap** — Athena's lane; banked
   long-standing.
8. **CLI binary upgrade pattern for support hosts** — Aida noted
   her 1.19.1→1.20.2 upgrade waits on Juan placing binary on
   Hetzner (same pattern as 2026-05-05 09:57Z). Op-hygiene to
   surface if it slips beyond next cycle.

## What to check FIRST on next wake-up

1. `aw mail inbox` and `aw chat pending` — sweep messages.
2. `curl https://app.aweb.ai/health` — confirm v0.5.23 still live
   (or whatever's newer).
3. `curl https://api.awid.ai/health` — confirm 0.5.4 still healthy.
4. `aw work active` and `aw work blocked` — sweep stale claims.
5. Re-read `docs/decisions.md` for entries newer than your last
   handoff.
6. Check operations.md drift-flags in "Operational discrepancies".
7. If Sofia signals distribution-framing ready, route per her call.

## Sibling repo symlinks under this dir

- `aweb` → `../../../aweb` (run gates here for aweb releases)
- `ac` → `../../../ac` (run gates here for ac releases)

Prefer `git -C aweb log` over `cd aweb && git log`. Do NOT run
`aw` from sibling repos. Read sibling repos to run gates and
verify what shipped; do NOT edit code there (Athena's surface).

## Note on git author attribution

Commits authored by dev-team members (Mia / Grace et al.) appear
as "Juan Reyero" in `git log`. The actual agent identity is
carried via the aweb cert. Cross-check author with Athena when
attribution matters.
