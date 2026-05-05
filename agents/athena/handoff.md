# Athena Handoff
Last updated: 2026-05-05 09:20 CEST

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

## Live state at 2026-05-05 09:20 CEST

- `app.aweb.ai/health`: release_tag `v0.5.21`, git_sha
  `8d6b37a2`, aweb_version `1.19.1`, awid_service_version
  `0.5.4`. Started 2026-05-05 07:11:15Z.
- `api.awid.ai/health`: 0.5.4, healthy.
- aweb OSS published tags: `server-v1.19.1`, `aw-v1.19.1`
  (shipped 2026-05-04 evening).
- channel 1.4.0.
- Cutover #2 of aweb_cloud schema closed cleanly.
  Constraint count back to 226 (zero drift); all 6
  cross-schema FKs restored.

## What just happened (2026-05-04 → 2026-05-05)

The full incident-and-recovery arc:

1. **aame epic ship attempt**: aweb 1.19.0 + ac v0.5.19. Two
   distinct production-correctness regressions:
   - Embedded aweb 001 checksum mismatch (133a7d94's DEFERRABLE
     edit to tasks.parent_task_id had been an in-place edit to
     001, never reverted; pgdbm refused).
   - 1.19.0 routing guard broke same-team mail/chat (rejected
     local fallback when AWID returned None; unsigned lookups
     miss private records).
2. **Rollback** to v0.5.18.
3. **Grace authored fixes**: a93c69be (embedded aweb 001
   restoration + additive 002/003/004); ff5f2ec → ef963ec
   (routing fix with two security gaps closed in iteration —
   DID-overlap bypass + parse-before-verify gap).
4. **aweb 1.19.1 + aw 1.19.1** shipped 2026-05-04 evening
   (release commit 6a180d3, Hestia tagged + pushed).
5. **Cutover #1 (aweb schema)**: AC v0.5.20 cut, deployed,
   destructive cutover on aweb schema with consolidated 001
   (Grace's 49b1525c). Schema-equivalence test caught a column-
   order drift on 0423bccf (kicked back, 49b1525c fixed it).
6. **Cutover #1 partial failure**: aweb_cloud:001 ALSO had a
   checksum mismatch from 133a7d94's edit (never reverted).
   Hestia hotfixed via `UPDATE schema_migrations SET checksum`
   to unblock prod. Users restored.
7. **Hestia constraint-diff audit**: 220 prod constraints vs
   226 baseline = **6 missing cross-schema FKs** (cloud_*
   tables → aweb.workspaces / aweb.agents). CASCADE-dropped
   during cutover #1's DROP SCHEMA aweb. Hotfix recovery does
   not restore them. Pre-launch this would have shipped silent
   schema drift; orphan-able rows on rare delete paths.
8. **Grace authored disciplined recovery** (8fa36cd0):
   reverted aweb_cloud/001 to original baseline (pre-edit, no
   DEFERRABLE inline) + added forward-additive
   002_mcp_refresh_token_replaced_by_deferrable.sql.
9. **Athena cut v0.5.21** (release commit 8d6b37a2 on top of
   8fa36cd0, version bump only).
10. **Cutover #2 (aweb_cloud schema)**: DROP SCHEMA
    aweb_cloud CASCADE → apply 001 + 002 → restore from
    safety-net dump → smoke. **All 6 missing FKs restored.
    226 constraints back. Schema drift closed.**

Both cutovers and 1.19.1 routing fix verified-live as of
2026-05-05 07:15Z.

## Banked invariants from this two-day arc

In `aweb/docs/aweb-sot.md` (Migrations section):

- **Deployed migrations are immutable. Recovery is always a
  NEW forward migration, never editing existing.** Banked
  during cutover #1 prep (commit 67f4cfa).

In Hestia's runbook (per her ack):

- **Multi-directory checksum audit on schema add**: when
  adding a new schema or migration directory to a service,
  audit ALL existing migration directories' checksums against
  prod's recorded ones FIRST. The aweb_cloud:001 drift was
  always there (since April 133a7d94); only surfaced when
  v0.5.19+v0.5.20 attempted to apply embedded-aweb migrations
  on top, scanning both chains under one deploy.
- **Prefer file-revert over hotfix when both available**:
  if a forward-additive migration already exists in the tree
  for a constraint change, the disciplined fix is to revert
  the in-place edit + keep the additive migration. Both produce
  the same end-state DDL; the disciplined shape preserves the
  immutability invariant.
- **Cross-schema FK audit before any DROP SCHEMA cutover**:
  run a constraint-diff against baseline; cross-schema FKs
  CASCADE-drop during DROP SCHEMA but do NOT auto-recreate via
  forward-additive migrations on the dropped schema's chain.
  Without the audit, schema drift is invisible until a
  customer-facing delete cascade behaves unexpectedly.
- **Asymmetric compat-test gap**: two distinct categories:
  (a) wire-shape compat (old-client/new-server,
      new-client/old-server),
  (b) auth-correctness inside new code (cert-presentation
      realism + spoof-rejection).
  Each needs its own test-matrix discipline.

## Standing release-discipline (banked through 2026-05-05)

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
14. Migration files are immutable post-deploy. Recovery is
    additive.
15. Equivalence-test policy: non-trivial diff = reject the
    consolidation, even if functionally invisible.
16. Cross-schema FK audit before any DROP SCHEMA cutover.

## Pending pre-launch / post-launch backlog

(Deferred during the two-day cutover arc. Pick up now that
prod is stable on v0.5.21 + aweb 1.19.1.)

1. **Playwright-MCP reproducer for Add-Existing dialog**
   (Athena own non-feature code). Lands as
   `ac/frontend/e2e/add-existing.spec.ts`, wired into
   `make test-cloud-user-journeys`. Targets in
   `status/engineering.md`. Originally deferred from
   2026-05-01.
2. **KI#1 closure technical content for Sofia's decision
   record.** Sofia drafts framing; Athena supplies cert-
   presentation auth correction + aalk continuity arc + 1.18.6
   trust-model arc + Aida 4/4 attestation. Source:
   `aale-trust-contract.md` in this dir + aweb commit
   `7759abc`. Pending Sofia framing draft.
3. **aweb-aalr.2 review** when Mia signals branch ready.
4. **Metis instrumentation ask**: record aw client version on
   requests. Athena to surface.
5. **Address chat-vs-mail signed_payload binding asymmetry**
   that the code-reviewer flagged on 1.19.1. messages.py
   guards `signed_to_did or signed_to_stable_id` non-empty;
   chat.py doesn't. Lower-risk because chat path has same-team
   fallback as primary gate. Track as follow-up tightening.
6. **YC fresh-container `aw init` timing** before they publish
   the five-minute claim externally. Not blocking; YC will
   re-engage when their draft is closer to publish.

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

1. `aw mail inbox` (both teams) — anything new from Hestia,
   Sofia, Mia, Grace post-cutover-2.
2. `app.aweb.ai/health` — confirm prod still on v0.5.21 +
   aweb 1.19.1 + awid 0.5.4. If anything's regressed, dig in.
3. `aw work active` — any new dev-team claims to brief.
4. Standing pending backlog above. Pick up the highest-leverage
   item (probably KI#1 closure content if Sofia's framing
   draft is ready, otherwise Playwright reproducer).
5. Update `../../status/engineering.md` to reflect post-cutover
   stable state.
