# Coordinator aweb OSS (John) — Handoff

Last updated: 2026-04-22

## Current state

aweb OSS is shipping aggressively. Since 2026-04-11 the repo landed
six server/CLI minors (1.11.0 → 1.16.0) plus awid 0.3.0–0.4.0, and
the team is now cleaning up drift surfaced by the per-membership
address model (1.16.0).

Current head: `fcbcc00 fix(channel): prefer cert member address` on
main. Only `beadhub-legacy` remains as a named archive branch.

## Active work: aweb-aakq (P1 epic)

Grace is the active dev agent. Focus `aweb-aakq` — "Collapse duplicate
sources of truth for active-team and active-address." Two bugs
(aweb-aakn workspace.yaml vs teams.yaml; aweb-aako identity.yaml.address
vs cert.member_address) are the same pattern: a cached copy duplicates
an authoritative source and drifts. The per-membership address model
made the drift user-visible.

**Shipping order:**
1. Surgical precedence flip in channel plugin (aakq.1) — **landed as
   fcbcc00** 2026-04-22. Reviewed: 2-line config change + regression
   test. Good.
2. Same flip in Go CLI (aakq.2) — **in progress**, grace active.
3. Refactor: drop `workspace.yaml.active_team` entirely, teams.yaml
   becomes SoT (aakq.3–.6).
4. E2E regression for Amy's 2026-04-21 two-team scenario (aakq.7).
5. Release aweb 1.17.0 / CLI 1.17.0 / channel 1.3.0; bump ac pin
   (aakq.8).

**Why Shape A matters for invariants.** Randy's engineering.md listed
a surgical patch (write workspace.yaml from runTeamSwitch). The epic
chose deeper: eliminate the duplicate cache. This is the right call —
invariant #1 (the four primitives are independent) applies recursively:
cached copies of authoritative state that can drift are the same
coupling mistake at the implementation layer. Keep watching that
aakq.3–.6 actually delete `ActiveTeam` from `WorktreeWorkspace` rather
than re-introduce a "safer" cache.

## Dev agents (live snapshot 2026-04-22)

| Alias | Status | Focus | Notes |
|-------|--------|-------|-------|
| grace | active (8m) | aweb-aakq | On .2 (Go CLI precedence fix) |
| kate  | offline 3d  | aweb-aakj | Claim stale (46h). aakj presumed done via Randy merges. |
| bob   | offline 6d  | aweb-aakh | ac repo, not aweb. Stale claim. |

The "dave / henry / ivy" line-up in my previous handoff is obsolete.
Randy's engineering.md notes agents don't follow the team-doc
structure: work actually lands as `henry` branch merges driven from
Claude Code sessions. Treat team.md's dev-agent table as aspirational.

## SOT / code alignment

- `aweb/docs/aweb-sot.md` — per-membership address model documented
  (§458). But lines 835–1040 still describe `workspace.yaml` carrying
  `active_team`. **That section will be wrong when aakq.3–.6 lands**
  (Shape A removes the field). Flag for update in the aakq.8 release
  PR.
- `aweb/docs/awid-sot.md` — aligned with 0.4.0 per Randy's status.
  Decisions 2026-04-18 (identity/address split, idempotent address
  registration, Replace/Archive multi-address policy) all in.

## What to check FIRST next wake-up

1. Did aakq.2 land? If yes, read the diff against the shape in the
   task description — watch for anyone adding a `MemberAddress` field
   to `WorktreeMembership` (the task description explicitly forbids
   it; cert stays single source).
2. Did aakq.3–.6 start? If yes: are `ActiveTeam` references actually
   going away, or did someone rewrite them into a "cache that syncs"?
   The latter is the invariant violation.
3. Did grace (or successor) open the aweb-sot.md update for
   workspace.yaml? If not, flag it before aakq.8 release.
4. `git -C aweb log --oneline fcbcc00..HEAD` — what landed.

## Open questions / things I haven't resolved

- **Coordinator structure reality check.** Randy's 2026-04-21 status
  noted that coordinator handoffs have been stale and git reality
  differs from the doc'd structure (everything commits as Juan with
  Claude Opus co-author). Mine was also 11 days stale. Worth a direct
  conversation with Juan about whether John/Tom/Goto are real roles
  or the company doc is aspirational. For now: I act as if real,
  watch for invariant violations in the aweb diff stream, and report
  via mail rather than assuming I have a dev-agent team to manage.
- **beadhub-legacy** (187 ahead / 1227 behind). Preserved pending
  Juan confirmation per Randy's status. Not my call to delete.

## Messages sent this cycle

None. No blocking concerns in grace's aakq.1 work.

## Reference — invariant checks I applied

- fcbcc00 (aakq.1): ✓ Invariant #1 honored — eliminates
  identity.address coupling over per-membership address.
- aakq epic framing: ✓ Catches the same-team-messaging-class mistake
  at implementation layer (a cached copy that claims to be the same
  as its source, but isn't).
- No new coupling between primitives observed in 1.11.0–1.16.0
  commits. Address work is strictly inside the address primitive.
