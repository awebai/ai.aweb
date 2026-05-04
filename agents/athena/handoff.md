# Athena Handoff
Last updated: 2026-05-04 14:55 CEST

## Read this first

You are Athena. You own the code for aweb and ac: architecture,
invariants, review of every diff that lands on main, and
non-feature code you write yourself.

**You belong to TWO cryptographic teams.** AGENTS.md leads with
this; re-read on every wake-up.

| Team | Visibility | Members | Purpose |
|------|------------|---------|---------|
| `default:aweb.ai` | PRIVATE — company | Sofia, Hestia, Aida, Iris, Metis, you | Direction, decisions, status, release framing, support, distribution |
| `aweb:juan.aweb.ai` | PUBLIC — dev | mia, noah, grace, kate, you | Code authoring on aweb and ac |

You are the only role with feet in both teams. Default active
team is `aweb:juan.aweb.ai`; use `--team default:aweb.ai` for
coordinator chats. Coders do NOT need to know about Hestia — to
them, Athena is the gate; they don't deploy.

## Current critical-path work: aame cutover

We are mid-cutover after the v0.5.19 deploy incident.

**Sequence of events (2026-05-02 → 2026-05-04):**
1. aame epic (aweb-aame, 10 sub-tasks .1-.10): conversations as
   first-class, lazy 30-day TTL, cert-presentation auth on the
   conversation primitive. Grace authored sub-tasks; reviewed by
   Athena + Mia dual-review.
2. Released as aweb 1.19.0 / aw 1.19.0 / awid 0.5.4 / channel
   1.4.0 / ac v0.5.19. Production deploy FAILED:
   - AC's embedded aweb 001 had been edited by AC commit
     133a7d94 (made `tasks.parent_task_id` DEFERRABLE),
     producing a checksum mismatch against prod's recorded
     `f0331940` — pgdbm refused to apply.
   - aweb 1.19.0 added a guard in `RegistryClient.resolve_address`
     that broke the local persistent fallback when AWID resolved
     to None — but unsigned lookups (no signing_key) miss
     private/team-scoped records, so cloud's same-team mail/chat
     broke.
3. Cloud rolled back to v0.5.18 (Render image
   `ghcr.io/awebai/ac:0.5.18` — note no leading `v`,
   `docker/metadata-action` strips it).
4. Grace authored two recovery commits:
   - **a93c69be** (ac): restored AC-embedded 001 to f0331940
     checksum, added 002+003+004 as additive aame migrations.
   - **ff5f2ec** → **ef963ec** (aweb): routing fix with two
     critical security gaps closed in iteration. Now uses
     `address_auth.py` shared helpers: same-team-projected
     team_id-equality (DID-overlap branch removed) +
     cryptographic signature verification before
     signed_payload-binding match.
5. Juan chose cutover over forward-additive: dump prod data,
   DROP SCHEMA, apply consolidated 001 (containing all of
   001+002+003+004 merged), restore data.
6. Grace authored **0423bccf** (ac): consolidated AC-embedded
   001 (single file, 002/003/004 deleted), updated
   `test_migration_paths.py`, added orphan-FK pre-check to
   `verify_db_reset_roundtrip.py` and wired it into
   `prod_db_reset.py` before TRUNCATE.

## Cutover review status (today 2026-05-04)

**0423bccf is currently kicked back to Grace.**

- Code-reviewer subagent: no criticals. Three minor warnings
  (hardcoded `aweb.` schema in trigger function, parser-
  assumption comment, dual-call-site doc gap).
- Hestia's `cutover_schema_equivalence.sh a93c69be 0423bccf`:
  **FAILED** with one drift: `aweb.messages` column physical
  order. Additive chain has `conversation_id` last (ALTER TABLE
  ADD COLUMN appends); consolidated 001 placed it between
  `signed_payload` and `read_at`.
- Functional impact on cutover: zero (pg_dump's COPY blocks
  name columns explicitly, PostgreSQL maps by name). But
  Hestia's policy is "non-trivial diff = reject"; fix is one
  line.
- Mailed Grace (msg `e959ca0a`) the kick-back. Mailed Hestia
  (msg `dc269e72`) holding the AC ship trigger.

**Scratch artifacts preserved at:**
- `/tmp/cutover-schema-eq-20260504T124916Z/` (worktrees)
- DBs `aweb_eq_before_72691`, `aweb_eq_after_72691`

## Next actions when Grace's fixup arrives

1. Pull ac. Confirm her commit moves `conversation_id` to last
   in messages CREATE TABLE.
2. Re-run `cutover_schema_equivalence.sh <new-ref> a93c69be`
   (or whatever the BEFORE ref should be — likely keep
   a93c69be).
3. If IDENTICAL: greenlight Grace; mail Hestia for AC ship.
4. If still drifts: kick back again with the residual finding.

## Cutover ship chain (after equivalence passes)

Coordinated with Hestia (mail `3a6f8591`):
- aweb 1.19.1 + aw 1.19.1 patch ship (the routing fix in
  ef963ec) — Athena initiates.
- AC v0.5.20 with new pin + consolidated 001 — Hestia tags
  after my greenlight.
- Render deploy (Hestia + Juan).
- Cutover phases (Hestia):
  pre-flight → safety dump → cutover dump →
  DROP SCHEMA aweb CASCADE → apply consolidated 001 →
  verify-applied SQL → restore from filtered dump →
  smoke probes → verified-live.

## Banked invariants from this cycle

- **Migrations are immutable once deployed.** Recovery is always
  a NEW forward migration, never editing the old. Banked in
  `aweb/docs/aweb-sot.md` (commit 67f4cfa) per Sofia's routing
  call. Athena AGENTS.md cross-references it.
- **Asymmetric compat-test gap, two categories:**
  (a) wire-shape compat (old-client/new-server,
      new-client/old-server),
  (b) auth-correctness inside new code (cert-presentation
      realism + spoof-rejection).
  Each needs its own test-matrix discipline. Both bit us in
  the v0.5.19 cycle.
- **`uv sync --refresh` after a PyPI publish:** uv's index cache
  lags. Always `--refresh` in the post-publish hour.

## YC artifact (one-off, not load-bearing)

`/Users/juanre/Desktop/grace-athena-security-review.md` —
verbatim 13-message chat history of the ff5f2ec → ef963ec
security-review iteration, for Y-Combinator application.
Untrimmed per Juan's explicit request.

## Pending pre-cutover work

- (Outside the cutover) Task #2: Author Playwright-MCP
  reproducer for Add-Existing dialog. Deferred from 2026-05-01.
  Picks up after cutover lands.
- Task #3: Supply KI#1 closure technical content for Sofia's
  decision record. Pending Sofia framing draft.
- Task #5: Review aweb-aalr.2 when Mia signals branch ready.

## Standing release-discipline (banked through 2026-04-26 + this cycle)

1. Release gate = full e2e + SOT + peer-review approval (mailed)
2. Review via shared working tree (not chat-pasted diffs)
3. Route work through the right peer
4. Trust the Makefile's release-ready chain
5. Written approval / decisions via mail
6. Use prohibition language explicitly when blocking a lane
7. Push release tags individually, never batched
8. Tracker audit needs symptom-check, not commit-message grep
9. Published artifact ≠ deployed service
10. Browser-verify UI-surface releases
11. Closure framing rests on empirical attestation
12. Reproducer-as-gate
13. Code-reviewer subagent for gate-input commits BEFORE
    bless-and-run mail to Hestia
14. **Migration files are immutable post-deploy. Recovery is
    additive. (this cycle)**
15. **Equivalence-test policy: non-trivial diff = reject the
    consolidation, even if functionally invisible. Restore
    correctness ≠ schema equivalence. (this cycle)**

## Working docs in this dir

- `aale-trust-contract.md`: working doc from the 2026-04-26
  architecture pivot. Source for KI#1 technical content.

## Sibling repo symlinks under this dir

- `aweb` → `../../../aweb`
- `ac` → `../../../ac`
- `awid` → `../../../aweb/awid`

Prefer `git -C aweb log` over `cd aweb && git log`. Do NOT run
`aw` from sibling repos.

## What to check FIRST on next wake-up

1. `aw mail inbox` — has Grace responded with a fixup commit?
2. `aw chat pending` — same.
3. If Grace pushed a fix: pull ac, re-run
   `cutover_schema_equivalence.sh` against the new ref.
4. If equivalence passes: greenlight + signal Hestia.
5. `app.aweb.ai/health` — confirm prod is still on
   `release_tag=v0.5.18` (rollback steady state).
6. `aw work active` — check for any new claims.
