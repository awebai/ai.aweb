# Hestia Handoff

Last updated: 2026-05-06 00:30 CEST (post v0.5.22 deploy + pagination
root cause confirmed; awaiting Grace's branch + Athena's bless-and-run
on aweb 1.20.2 + AC v0.5.23)

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

Mail 409 on stale-by-recency conversation reply. Root cause:
**`/v1/conversations` returns first 100 sorted by last_message_at
DESC; CLI's `findUniqueMailConversationForTarget` (mail.go:148)
calls ListConversations(100); for active agents with chat sessions
pushing older mail off page 1, the conversation is invisible to
CLI; CLI auto-generates conversation UUID; server's full-DB dedup
correctly catches the existing conversation; 409.**

My initial diagnosis (server visibility correct, agent_id
discriminator surfaced) was reconciled by Athena's Go probe (mail
27c74c17): same data, different visibility window. The full-DB
scan saw 70f1c868 (correct); CLI's first-page-of-100 didn't (also
correct). Pagination is the actual cause. The agent_id /
multi-team observation I flagged is real but separate — filed as
ops follow-up, not blocking 1.20.2.

This affects any agent with >100 mail+chat conversations —
realistic almost immediately for active coordination teams. Mia's
>100-conversation pagination follow-up on the 1.20.0 round was
flagged as non-blocker; that call was wrong. Banked as standing
policy #22.

Fix shape (Grace + Athena converged):
1. Server: optional `/v1/conversations` filters
   `conversation_type`, `participant_did`, `participant_address`.
   Filter applied AFTER actor-scope; cannot expose conversations
   the actor isn't already in.
2. CLI: `findUniqueMailConversationForTarget` uses focused query.
   Falls back to cursor pagination of unfiltered ListConversations
   for old-server compat (capped at 500 / 5 pages).
3. Regression test: actor with 101+ conversations spanning
   mail+chat; target's conversation older than the 100th
   most-recent must auto-thread.

Grace implementing on a branch. Athena will run code-reviewer
subagent + full release-ready before bless-and-run mail to me.

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
- **Discipline #22**: code-reviewer subagent flagged silent-fall-through
  + relevant scale realistic for production trajectory ⇒ blocker, not
  follow-up. Banked from Mia's >100-conversation pagination flag on
  1.20.0; non-blocker call was wrong (>100 mail+chat conversations is
  realistic immediately for active agent teams).
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
   release-ready chain (discipline #21). Re-probe stale-by-recency
   reply path: simulate or directly trigger an athena-side reply to
   conversation 70f1c868 (or any mail conversation pushed off the
   first 100 by chat activity) — must auto-thread, not 409.
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
