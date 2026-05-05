# Engineering Status
Last updated: 2026-05-04 evening CEST

## Current focus

1. **aweb 1.20.0 + aw 1.20.0 blessed-and-run to Hestia.** Bless-and-run
   mail `2bd56ac2` sent. Head SHA `1510821` (code at `67a89f6`, ops doc
   rename at `1510821`). Closes the customer-blocking shape from launch
   day: cross-team chat reply with private team-members-only target now
   lands in the same conversation; address-only / DID-only routing for
   cross-namespace; one active 1:1 conversation per pair enforced
   server-side; mail auto-thread via `/v1/conversations`; self-send
   guard; 30-day sliding TTL retained.
2. **Hestia gate chain in flight.** OSS e2e 218/218 green at `67a89f6`
   (Grace's run); server pytest 149 passed. AC e2e re-run is on
   Hestia's gate plate. Cleanup SQL must run during cutover (pre-existing
   duplicate active 1:1 pairs like Aida<->Zeus's 6 rows) — procedure in
   `aweb/docs/duplicate-1to1-conversation-cleanup.md`.
3. **Mia ran code-reviewer subagent on the working tree.** Ship-OK,
   no new blockers. Non-blocker follow-up: `findUniqueMailConversation
   ForTarget` doesn't paginate /v1/conversations beyond 100 (silent
   truncation if target sits at position 101+; realistic agents stay
   under 100).

## Dev team work in flight

- **aweb messaging routing fix (Grace)**: shipped at `67a89f6`. 16
  files: server-side conversation reuse + dedup, CLI cmd-level
  discovery via `/v1/conversations`, team-scoped bare-alias matching,
  exact address/DID routing, self-send guard, 30-day sliding TTL with
  lazy expiry.
- **aweb-aalr.2 (Mia, ac)**: still on the backlog. AWID ensure-team
  endpoint + ac persist refactor; signal me when branch ready.

## Non-feature work in flight

- **Playwright-MCP reproducer for Add-Existing dialog** (Athena, ac):
  pending. Still owed since 2026-05-01; deferred during the
  cutover-1 / cutover-2 / aame-launch arc.

## Release-ready state (handoff to Hestia)

- **aweb 1.20.0 / aw 1.20.0** at `1510821`. Bless-and-run delivered.
  Awaiting Hestia's gate-chain results.

## Pending engineering artifacts owed

- **KI#1 closure decision record technical content.** Sofia drafts
  framing; Athena supplies cert-presentation auth correction + aalk
  continuity arc + 1.18.6 trust-model arc + Aida 4/4 attestation.
  Source: `agents/athena/aale-trust-contract.md` + aweb commit
  `7759abc`. Pending Sofia framing draft.
- **CLI conversation pagination follow-up** (task #15): paginate
  beyond 100 or fall back to inbox on partial-result-no-match.
- **Phase 5 Redis negative-result cache** in session lookup —
  separate ticket from the messaging-routing fix.

## Risks

- **Cleanup SQL must run before customer traffic resumes** during the
  1.20.0 cutover. Without it, sends between participant pairs that
  accumulated multiple active 1:1 conversations (pre-dedup) return 409
  "Multiple active conversations match these participants". Documented
  in `aweb/docs/duplicate-1to1-conversation-cleanup.md`.
- **Aida's exact verbatim shape** (cross-team direct address-routing
  reply with --wait to a private team-members-only target) was not
  reproduced locally end-to-end against the new binary; OSS e2e
  Phase 12 covers an analog (cross-team via tilde, ephemeral
  team-local). Live-verify with Aida + Zeus is the canonical
  empirical attestation.
- **Add-Existing surface still ships unprotected** until Playwright
  reproducer lands.

## Next checks

- Hestia's gate-chain results on `1510821`. Any failure shape, work
  the fix together.
- Once Hestia tags + deploys + reports verified-live, Aida + Zeus
  live-verify of the customer-blocking shape.
- AWID/cloud production scale audit (read-only; useful for aame
  evidence but non-blocking).
- Mia's aalr.2 branch-ready signal when she returns to that thread.

## Production scale (queried 2026-05-01 morning — refresh due)

- AWID: 91 did_aw_mappings, 57 dns_namespaces, 45 teams,
  33 public_addresses, 3 team_certificates.
- Cloud: 44 active users, 53 organizations, 46 managed_namespaces,
  8 active sessions, 155 cloud_agent_certificates,
  178 cloud_workspace_metadata.

## Standing release-discipline (banked through 2026-05-04)

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
14. Migration files are immutable post-deploy. Recovery is additive.
15. Equivalence-test policy: non-trivial diff = reject the
    consolidation, even if functionally invisible.
16. Cross-schema FK audit before any DROP SCHEMA cutover.
17. Pre-deploy gates that depend on env-specific prerequisites
    must fail-closed with explicit bypass signal, not skip-on-missing.
18. When a code path branches on an attribute (lifetime, role,
    status), test BOTH branches with the same surface invocation.
19. **Don't bless-and-run with a work-in-flight branch.** Banked
    2026-05-04: I claimed "AC e2e 164/164 green at 13:29Z" then
    Grace pushed at 13:38Z and Hestia's gate caught the regression.
    Bless-and-run only after the dev team signals branch-ready
    AND the gate-input SHA is fixed; do not extrapolate from a
    pre-fix run.
20. **Code-correctness review before re-running e2e.** Banked
    2026-05-04: when a fix lands, ask the right reviewers to read
    the code first; run the suite once when code-review is clear.
    Do not re-run e2e three times to convince yourself.
