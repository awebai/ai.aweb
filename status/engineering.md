# Engineering Status
Last updated: 2026-05-06 ~08:30 CEST

## Current focus

1. **Messaging-architecture epic VERIFIED-LIVE.** aweb 1.20.0 → 1.20.1
   → 1.20.2 + AC v0.5.22 → v0.5.23 deployed and verified end-to-end
   2026-05-06 06:14:33Z. The launch-day customer-blocking shape from
   2026-05-03 (cross-team chat reply / address-routed mail) is closed
   empirically. See Hestia closure mail 362f0be6 for full attestation.
2. **Pagination fix on /v1/conversations** (the load-bearing 1.20.2
   delivery): server-side filter (conversation_type, participant_did,
   participant_address) applied AFTER actor-scope; CLI uses focused
   query in findUniqueMailConversationForTarget. Closes the
   stale-by-recency 409 class for any agent with >100 mail+chat
   conversations. Verified at conversation 70f1c868 (athena↔sofia,
   originally bug-causing pre-deploy) AND 96317ca9 (athena↔hestia,
   page-1 baseline).
3. **CLI auto-update-check filed P1** (aweb-aamt, dev team). On any
   `aw <command>` invocation, if newer GitHub release exists, print
   "Upgrade available: vX → vY" hint to stderr (rate-limited via
   24h cache, opt-out via AW_NO_UPDATE_CHECK=1, --json safe). Wires
   the existing checkLatestVersion infra into rootCmd.PersistentPreRun
   beyond just `aw version` callsite. Closes the distribution-cadence
   gap surfaced by Juan after the 1.20.2 ship.

## Dev team work in flight

(quiet post-cycle; Grace's last commit was b7e86745 test fixture
fix landing on AC main for next-cycle ship)

## Non-feature work in flight

- **Multi-team agent_id-vs-did comparison grep** (task #20, my plate,
  bandwidth-allowing). cp.agent_id is team-scoped — multi-team agents
  (same did_aw, multiple team memberships, multiple agent_id rows in
  aweb.agents) hit asymmetry when code compares on cp.agent_id
  instead of cp.did/cp.did_aw. The 1.20.2 fix bypassed this for the
  pagination case but other code paths in aweb may still have direct
  cp.agent_id comparisons. Grep server/src/aweb/ + cli/go/, assess
  each callsite. Non-blocking.

## Release-ready state (handoff to Hestia)

Nothing in the release pipeline. Last ships:
- aweb-server-v1.20.2 + aw-v1.20.2: PyPI + npm latest, 2026-05-06 ~05:50Z
- aweb-cloud v0.5.23: app.aweb.ai released, 2026-05-06 06:14:33Z

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

- **CLI distribution gap** until aweb-aamt ships. Customers on
  pre-1.20.2 `aw` will hit the pagination 409 in production with
  no in-band hint to upgrade. Affects support-cycle cost more
  than user functionality (workaround: customers run `aw upgrade`
  manually if they think to).
- **Multi-team-agent class** unaudited across the codebase
  (task #20). Potential silent misbehavior on code paths comparing
  cp.agent_id directly. No reported customer hits yet but the
  class is real.
- **chat-403 on pre-aame chat sessions** unchanged. Customers
  use `aw chat send-and-wait <peer> "msg" --start-conversation`
  as workaround. Aida documented in support runbook. Threshold
  for code-fix priority: 2nd customer report in rolling 7d.

## Next checks

- aweb-aamt P1 review when Mia/Grace claim it from the dev team
  task queue.
- Sofia's KI#1 framing draft when ready (to supply technical
  content).
- Multi-team agent_id grep at next bandwidth window.
- Any customer-side reports of chat-403 or pagination edge cases.

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
