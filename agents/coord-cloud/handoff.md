# Coordinator aweb-cloud (Tom) — Handoff

Last updated: 2026-04-25 (v0.5.6 tagged + GHA in flight)

## Current state

**ac v0.5.6 tagged** at `e5f58ce5` and pushed (closes
`aweb-aaja.6` P0 launch blocker — cross-repo Docker e2e for hosted
MCP OAuth verified mail; custody.py canonical_payload SIGNED_FIELDS
filter alignment). GHA aweb-cloud CI/CD run `24937821668` in
progress; v0.5.5 went 13m54s, expecting similar.

**ac v0.5.5 prod-roll status:** as of this handoff, prod was still
on v0.5.4 per /health (auto-window pending). v0.5.5 may auto-roll
or v0.5.6 may roll directly — depends on the deploy mechanism's
"latest tag" vs "tag-by-tag" behavior. Either way, the next coord
should verify against /health.

Origin/main HEAD: `e5f58ce5` (v0.5.6 bump on top of Grace's
`18021ff9`). Pinned `aweb>=1.18.1`, `awid-service>=0.5.1`.

## Verified-live discipline (NEW 2026-04-25, banked from awid cutover)

For v0.5.6 onwards, GHA-green is NOT the same as feature-live. The
release sequence now ends with:

1. After GHA green + auto-deploy: curl `app.aweb.ai/health`. Assert
   `release_tag` matches the just-tagged version, `git_sha` matches
   the bump commit, dep versions match the pin.
2. One-shot smoke against the surface the release actually changed
   (for v0.5.6: hosted MCP OAuth + send_mail signed-payload-verifies
   path against deployed prod).
3. Only AFTER both: mail Randy + Juan + John "v0.5.6 fully live."

This was banked because the awid-prod 0.3.1 stale-deployment incident
(earlier today) showed that PyPI publish + tag push + GHA green can
all be true while the running service is on a much older version. The
trust-the-running-service step is what catches that gap.

## v0.5.6 ship summary

Single-commit functional delta from v0.5.5:
| SHA       | Ticket          | Purpose                                        |
|-----------|-----------------|------------------------------------------------|
| `18021ff9` | aweb-aaja.6     | Hosted MCP OAuth signed mail e2e + custody.py canonical_payload swap |
| `e5f58ce5` | (release bump)  | version 0.5.5 → 0.5.6, no pin change           |

Pre-bump bisect: tested against pure aweb 1.18.1 sibling (`b0b2b27`
checkout, dropping 2e6156b aajg/aajh + ed4fa89 awid tooling) — 10
passed. The aajg `canonical_signed_payload` alignment in 2e6156b is
real and ships in aweb 1.18.2 (John's timeline), but ac's hosted MCP
signing path doesn't depend on it. Symmetric canonicalization on
either side of the wire converges; cleaning up either end alone is
sufficient.

Full narrative in `ai.aweb/docs/decisions.md` 2026-04-25 entry titled
"aweb-cloud v0.5.6 ships; closes aaja.6 (P0 launch blocker)".

## Coord-borrow precedent extends to v0.5.6

Grace authored 18021ff9 under continuing coord-borrow. Same pattern
as v0.5.5 (aala.10) — Juan-greenlit cross-coord borrow, Tom owns
ac-side review + gate discipline, John remains aweb-coord for
Grace's other tracks. The borrow is now a first-class operating
mode, not an exception.

## Pending verification chain

1. GHA `24937821668` green for v0.5.6.
2. Auto-deploy of v0.5.6 (and v0.5.5 if it hasn't rolled — though
   deploy might skip straight to v0.5.6 as the latest tag).
3. /health verification.
4. Hosted MCP OAuth + send_mail smoke against deployed prod.
5. Mail Randy + Juan + John "v0.5.6 fully live."
6. John fires his queued prod-awid BYOIT smoke (controller add-member
   uploads cert blob → joining-machine fetch via authenticated GET +
   wrong-DID 403). One mail to Randy with both legs confirmed.

## Release protocol locked in (3 cycles, v0.5.4 + v0.5.5 + v0.5.6)

For every future release:

1. Pre-bump bisect when pin decisions are ambiguous.
2. Bump commit (pyproject.toml + uv.lock).
3. `uv sync` post-bump.
4. `make release-ready` against post-bump `.venv`. Per-gate log
   mailed to Randy.
5. SOT analysis mail. Walk aweb-sot, awid-sot, identity.md, ac/sot
   for drift; check vs prior version for regression; map acceptance
   criteria for any tickets being closed.
6. CTO written-and-mailed approval.
7. Explicit `git push origin main` + `git tag -a vX.Y.Z` + `git
   push origin vX.Y.Z`. Do NOT use `make ship`.
8. Verify GHA green.
9. Tag-time pings to all coords whose work fed the release.
10. **Verified-live**: /health + smoke against deployed prod.
11. Final "fully live" mail when verified.
12. Decision record entry to `ai.aweb/docs/decisions.md`.

## Memory bank for next coord-cloud

11 feedback memories in
`/Users/juanre/.claude/projects/-Users-juanre-prj-awebai-ai-aweb/memory/`:
- aweb_cross_namespace_membership.md (reference)
- feedback_review_via_symlink.md
- feedback_spec_scope_all_consumers.md
- feedback_gut_over_confident_agent.md
- feedback_dispatch_via_coordinator.md
- feedback_reproduce_exact_invocation.md
- feedback_approval_via_mail.md
- feedback_makefile_is_authoritative_gate_chain.md (with corollary
  on target body vs name from 2026-04-25)
- feedback_close_the_loop_at_tag_time.md
- feedback_mail_body_escaping.md

Pending bank candidates from today's incidents:
- "GHA-green ≠ feature-live" / verified-live discipline. Could fold
  into close_the_loop_at_tag_time as a corollary, or stand alone.
- "404 ≠ data missing; verify endpoint shape against a known-good
  record before drawing inferences." Same family as
  reproduce_exact_invocation; could fold there.
Decision deferred to next handoff cycle.

## Dev agents (ephemeral, in the ac repo)

| alias | last seen     | notes                                                 |
|-------|---------------|-------------------------------------------------------|
| grace | active today  | Authored eb8e388d + 343f40f8 + 18021ff9 under borrow. |
| mia   | offline 2d+   | aakv/aakt/aakw/aakx via v0.5.4. Stand down still.     |
| bob   | offline 9d+   | aweb-aakh stale claim; un-claim if no movement.       |
| leo   | offline 5d+   | (none)                                                |
| ivy   | offline 6d+   | (none)                                                |
| eve   | offline 8d+   | (none)                                                |

## Open ac branches

- `main` at `e5f58ce5` (v0.5.6).
- `aaga-archive` — remote-only; preserved per Randy's note.

## Time-bound follow-up (carried)

GHA workflow uses Node.js 20 actions. GitHub forces Node 24 by
**2026-06-02** and removes Node 20 by **2026-09-16**. Pre-2026-06
task to bump action versions in `.github/workflows/*.yml`.

## What to check FIRST on next wake-up

1. GHA `24937821668` outcome. Diagnose if red.
2. Prod /health: `curl -sS https://app.aweb.ai/health`. Confirm
   `release_tag: v0.5.6`, `git_sha: e5f58ce5...`. If still on
   v0.5.4 or v0.5.5, deploy is lagging — check Render dashboard
   indirectly via Juan if needed.
3. Hosted MCP OAuth smoke against deployed prod. Replicate the
   key path of TestHostedMCPOAuth manually: register an OAuth
   client, complete the PKCE flow, send_mail via /mcp/, fetch
   the message, verify the signature against the canonical
   bytes. If any step fails, escalate to Randy before signaling
   live.
4. Mail Randy + Juan + John "v0.5.6 fully live" once steps 2+3
   pass. That's the signal John waits for to fire his queued
   prod-awid BYOIT cross-machine smoke.
5. v0.5.5 prod-roll status — if v0.5.5 was skipped in favor of
   going direct to v0.5.6, no action; if both deployed in
   sequence, the v0.5.5 fully-live mail is pending too (could
   bundle with v0.5.6 mail).
6. `bob` stale claim on aweb-aakh.
7. Anything new from Juan/Randy/John (mail inbox first).
