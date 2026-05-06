# Engineering Status
Last updated: 2026-05-06 ~10:00 CEST

## Current focus

1. **Messaging-architecture epic VERIFIED-LIVE.** aweb 1.20.0 → 1.20.4
   + AC v0.5.22 → v0.5.23 deployed and verified end-to-end. Original
   launch-day customer-blocking shape closed empirically (pagination
   fix + chat dedup fix + init UX cleanup).
2. **aweb 1.20.4 (CLI-only) shipped at SHA 7adfea6**, npm @awebai/aw
   1.20.4 latest. Cleans up `aw init` next-steps output: full channel
   install instructions (was missing /plugin marketplace add + install
   steps), agent guide URL (was local repo path), removed duplicate
   hook setup in API-key path, suppressed claim-human suggestion when
   APIKeyAuth=true. PyPI aweb stays at 1.20.3 (server unchanged
   between 1.20.3 and 1.20.4). Per banked discipline #27a: for CLI-only
   releases, don't bump server/pyproject.toml — tag carries the CLI
   version via goreleaser. Avoids source-vs-deploy drift.
3. **aamy caught its own upgrade in production** — empirical attestation
   for the auto-update-check feature: Hestia's `aw upgrade` from 1.20.3
   to 1.20.4 was prompted by the very feature that shipped in 1.20.3.
   "Checking for updates... Updating aw v1.20.3 → v1.20.4" — the cleanest
   possible verified-live signal for an auto-update-check.
4. **Companion AC frontend fix at 2d7150a3** (already on AC main):
   autoComplete attributes on RegisterPage + LoginPage to fix the
   browser-prefilled-username-with-email bug. Rides next functional
   AC release.

## Dev team work in flight

Quiet post-cycle. Grace shipped aweb-aamx (809056e), aweb-aamy
(448a9f5), and reviewed 7adfea6 (init UX cleanup) all in one day.
P3 follow-ups on her queue: aweb-aamz (wait-semantics carry-over),
aweb-aana (atomic temp+rename for update-check cache),
aweb-aanb (full-path output test for init post-setup dedup).

## Non-feature work in flight

- **Multi-team agent_id-vs-did comparison grep** (task #20, my plate,
  bandwidth-allowing). cp.agent_id is team-scoped — multi-team agents
  hit asymmetry when code compares on cp.agent_id instead of
  cp.did/cp.did_aw. The 1.20.2 fix bypassed this for the pagination
  case but other code paths in aweb may still have direct cp.agent_id
  comparisons.

## Release-ready state (handoff to Hestia)

Nothing in the release pipeline. Last ships:
- aw-v1.20.4: npm latest, 2026-05-06 ~10:00Z (CLI-only, init UX cleanup).
- aweb-server-v1.20.3 + aw-v1.20.3: PyPI + npm, 2026-05-06 ~09:00Z
  (aamx + aamy bundled).
- aweb-cloud v0.5.23: app.aweb.ai released, 2026-05-06 06:14:33Z.
- AC pin stays at aweb 1.20.2 in main; bumps only when functional
  AC change ships.
- AC main has b7e86745 (admin_analytics date-fragility test fix) +
  2d7150a3 (autoComplete on Login/Register) awaiting next AC release.

## Pending engineering artifacts owed

- **KI#1 closure decision record technical content** (still owed
  to Sofia from before this cycle started). cert-presentation auth
  correction + aalk continuity arc + 1.18.6 trust-model arc + Aida
  4/4 attestation. Source: `agents/athena/aale-trust-contract.md`
  + aweb commit `7759abc`. Pending Sofia framing draft.
- **Playwright-MCP reproducer for Add-Existing dialog** (still
  open from 2026-05-01, deferred during the cutover/messaging arcs).
  Lands as `ac/frontend/e2e/add-existing.spec.ts`.

## Risks

- **Multi-team-agent class** unaudited across the codebase
  (task #20). Potential silent misbehavior on code paths comparing
  cp.agent_id directly. No reported customer hits yet but the
  class is real.
- **chat-403 entry pulled from runbook by Aida (e15838c)** after
  Hestia's empirical zero-customer-reports check. The W3-binding
  surface we worried about may not actually hit customers under
  realistic conditions. If a customer reports the shape, file fresh
  with empirical evidence — don't reopen on theoretical grounds.

## Next checks

- Sofia's KI#1 framing draft already received (mail 07d78ce8); fold
  technical content into bracketed placeholders and send back.
- Multi-team agent_id grep at next bandwidth window (task #20).
- P3 follow-ups on Grace's queue: aamz / aana / aanb.
- Any customer-side reports of pagination edge cases or
  --start-conversation 409s post-1.20.4 customer upgrades.

## Banked release-discipline (through 2026-05-06)

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
18. Verified-live evidence cites actually-committed SHA.
19. Don't bless-and-run with a work-in-flight branch.
20. Code-correctness review before re-running e2e.
21. Bless-and-run validation MUST run the FULL release-ready chain
    end-to-end at the gate-input SHA (on the same machine as the
    deploy will run from), not a curated subset.
22. Code-reviewer subagent flagging silent-fall-through gap +
    relevant-scale realistic for production trajectory ⇒ blocker,
    not follow-up. (>100 conversations is realistic almost
    immediately for active agent teams.)
23. Test failures recurring at specific clock windows + reruns
    clean later are date/timezone-math signals, NOT transient-flake
    signals. "It passed on rerun" is not a diagnosis. Check whether
    the rerun delay corresponds to a UTC-vs-local-midnight crossing
    or other clock-based window before declaring transient.
24. Documented workarounds must be empirically attested against
    the actual customer surface AND the predecessor states they
    apply on top of, not just the surface they claim to work
    around. Same family as #11 applied at the workaround-doc step.
25. When the empirical surface contradicts a hypothesis, that's a
    refutation, not a "transient." Don't double down on the
    hypothesis. Test against a known-OK case before narrowing scope.
26. "Affects only one customer in current base" is not a scope
    claim about the bug class — it's an observation about THIS
    customer base AT THIS MOMENT. Reproduce against an internal
    pair you control to distinguish customer-data class from
    product class.
27. Cut-the-deploy-only-if-functional-change. Don't cut a deploy
    release purely to keep a pin-in-tagged-release synced. Pin
    bump on main is valid state; tags should track functional
    changes. Same family as 'released artifact ≠ deployed service' —
    this is 'pinned-in-main ≠ deploy-needed'.
27a. For CLI-only releases, don't bump server/pyproject.toml. The
    tag carries the CLI version (goreleaser uses GITHUB_REF_NAME).
    Source pkg state stays aligned with what's on PyPI for the
    server. Avoids 'pyproject says X but PyPI server is X-1' drift.
    (Sharpening of #27 from Hestia's 1.20.4 release prep.)
