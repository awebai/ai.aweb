# Hestia Handoff

Last updated: 2026-05-05 22:00 CEST (post v0.5.22 deploy + multi-team-agent
bug pinned to CLI; awaiting Athena's 1.20.2 brief)

## Read this first

You are Hestia. You carry every release across the build/ship boundary
and keep the company machinery healthy in between.

The 2026-05-05 launch-day cycle is **mostly closed**:

- **Shipped**: aweb 1.20.0 + 1.20.1 (PyPI), aw 1.20.0 + 1.20.1 (npm +
  GH Releases), AC v0.5.22 deployed at app.aweb.ai. Migration-immutability
  gate passed end-to-end at release-ready (first real-world use).
- **Pre-deploy cleanup**: Duplicate-1to1 collapse executed cleanly via
  Athena's collapse-only procedure. 195 conversations closed across
  16 pairs.
- **Verified-live evidence**: alias + `--to-address` smoke probes both
  attach to existing conversation 96317ca9 (athena↔hestia) cleanly,
  verification_status=verified. Conversation 96317ca9 was pre-deploy —
  counterexample to "all pre-deploy conversations 409" framing.

**Open bug** (Juan's launch-hold still in effect):

Multi-team-agent mail 409 on some pre-deploy conversations. athena
(member of `default:aweb.ai` and `aweb:juan.aweb.ai`) gets 409 on
reply via `aw mail send --to <peer>` for some conversations but not
others. Diagnosis pinned to **CLI `mailConversationMatchesTarget`
(mail.go)**, not server visibility:

- Empirical /v1/conversations probe with both athena agent_ids
  (d75fe9d3 default, fdeb842d aweb-juan) returned 83 distinct
  conversation_ids each run.
- BOTH 70f1c868 (broken, sofia↔athena) AND 96317ca9 (works,
  hestia↔athena) surfaced in BOTH runs.
- Participant rows API returns: identical shape — athena (did=yumP9TQf,
  address=aweb.ai/athena) paired with sofia/hestia. transport_hint is
  NOT in the API response.

Server visibility is correct. Bug is in CLI's matching predicate
deciding 70f1c868 doesn't match. Mailed Athena (4752259d) with the
diagnosis. Fix path: aweb 1.20.2 + AC v0.5.23 with Grace's CLI fix.

## The team

- **Sofia**: direction. Out of routing for bug-fix releases by default.
- **Athena**: code in aweb and ac. Just received the bug-pinning mail;
  expected to brief Grace and signal bless-and-run on 1.20.2 + v0.5.23.
- **Mia / Noah / Grace / Kate**: dev team (`aweb:juan.aweb.ai`).
- **Aida**: support, online, idle.
- **Iris / Metis**: not yet registered (Hetzner pending for Iris).

## Identity (live since 2026-05-01 21:05 UTC)

- did: `did:key:z6MkebRpF7qEFNt5vAYa5BWjegFk1igt6mRESqWb5r3kp9AK`
- stable: `did:aw:3fC4cfvFuVAxZCWyJNRCoUxHVAim`
- address: `aweb.ai/hestia` (reachability=nobody)
- active team: `default:aweb.ai`

## What's live (verified 2026-05-05 22:00Z)

- **ac**: v0.5.22 at `app.aweb.ai`,
  git_sha=`f6c27c619d0c5e37e3aa096c177d11e40a0984a0`,
  aweb_version=1.20.1, awid_service_version=0.5.4. Started
  2026-05-05T21:27:26Z.
- **aw CLI**: 1.20.1 published on npm and GH Releases.
- **aweb server**: 1.20.1 on PyPI.
- **awid registry**: 0.5.4 at api.awid.ai. Healthy.
- **channel**: 1.4.0 on npm.

## Banked into runbook this cycle (2026-05-05)

- **Discipline #18**: verified-live cites actually-committed SHA, not
  bumped-but-unreverified SHA.
- **Discipline #19**: work in flight (uncommitted bumps, in-progress
  procedures) does not count as released until tag pushed + verified.
- **Discipline #20**: reproducer must match empirical surface (CLI 409
  reproducer must surface 409 from prod CLI vs prod server, not just
  unit-test logic).
- **Discipline #21**: bless-and-run from peer = run FULL release-ready
  chain end-to-end. Don't shortcut to bump+tag — re-run gates each
  time. Banked from v0.5.22 r1 where the 1.20.0→1.20.1 hop nearly
  skipped re-running gates.
- **Schema gotcha (banked, runbook §Schema gotchas pending)**:
  `aweb.agents`, `aweb.teams`, `aweb.chat_sessions` lack `updated_at`.
  `aweb.chat_sessions` also lacks `expires_at`. Athena's close-cleanup
  procedure tried to UPDATE these and broke. Verify column existence
  before any cleanup procedure assumes pgdbm-style timestamps.
- **Customer-history-not-destroyable**: DELETE-240 chat_sessions /
  close-9-mail-conversations explicitly OFF the table. Real fix in
  code, not data — even when convenient. Juan's stake: "remember we
  have customers".

## Open follow-ups (Hestia's lane)

1. **Watch for Athena's 1.20.2 + v0.5.23 bless-and-run.** Run full
   release-ready chain (discipline #21). Re-probe multi-team-agent
   mail path against 70f1c868-class conversations after deploy.
2. **Bank discipline #21 into runbook** — first real session post-launch
   when ops cadence resumes.
3. **Bank schema-gotcha into runbook §Schema gotchas** — pgdbm-style
   timestamp assumptions don't hold on aweb.agents/teams/chat_sessions.
4. **Bank 8-table identity-routing doctrine** (Sofia agreed; post-launch).
5. **Iris agent registration** when Hetzner bootstrap completes.
6. **Asymmetric compat-test gap** flagged to Athena (engineering lane).
7. **Verified-live mail for 1.20.0/1.20.1/v0.5.22 epic** held until
   the multi-team-agent bug is closed. Once 1.20.2 + v0.5.23 ship
   and re-probe is green, post the full epic verified-live mail.

## What to check FIRST on next wake-up

1. `aw mail inbox` — Athena's reply on the bug diagnosis (might
   contain bless-and-run for 1.20.2 + v0.5.23).
2. `aw chat pending` — sweep messages.
3. `curl https://app.aweb.ai/health` — confirm v0.5.22 still live
   (or v0.5.23 if it shipped). Compare `release_tag` and `git_sha`
   to claims.
4. `curl https://api.awid.ai/health` — version 0.5.4 healthy.
5. `aw work active` and `aw work blocked` — sweep stale claims.
6. Re-read `docs/decisions.md` for entries newer than 90eeda0.
7. Check operations.md drift-flags in "Operational discrepancies".

## Sibling repo symlinks under this dir

- `aweb` → `../../../aweb` (run gates here for aweb releases)
- `ac` → `../../../ac` (run gates here for ac releases)

Prefer `git -C aweb log` over `cd aweb && git log`. Do NOT run
`aw` from sibling repos. Read sibling repos to run gates and
verify what shipped; do NOT edit code there (Athena's surface).

## Note on git author attribution

Commits authored by dev-team members (Mia / Grace et al.) appear
as "Juan Reyero" in `git log`. Cross-check author with Athena
when attribution matters.
