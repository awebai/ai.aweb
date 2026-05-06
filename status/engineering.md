# Engineering Status
Last updated: 2026-05-06 ~09:30 CEST

## Current focus

1. **Messaging-architecture epic VERIFIED-LIVE.** aweb 1.20.0 → 1.20.1
   → 1.20.2 + AC v0.5.22 → v0.5.23 deployed and verified end-to-end
   2026-05-06 06:14:33Z. Pagination fix at conversation 70f1c868 +
   96317ca9. See Hestia closure mail 362f0be6.
2. **aweb 1.20.3 (CLI-only) shipped.** aweb-aamx fix at SHA 809056e:
   `--start-conversation` no longer skips `shouldProbeExistingSession`,
   so the CLI honors existing server-side sessions instead of generating
   fresh UUID4 in conflict with server's dedup. Single-line change at
   cli/go/chat/chat.go:1137 + regression test. Server code unchanged
   between 1.20.2 and 1.20.3. PyPI + npm published; no AC v0.5.24
   needed (banked discipline #27 — don't cut deploy release for non-
   functional changes). AC pin stays at 1.20.2 in main; pin bumps
   only when a functional AC change ships, not as bookkeeping.
3. **aweb-aamy (auto-update-check) ALSO shipped in 1.20.3** — Hestia's
   release-prep commit f8c7bce sits on top of both 809056e (aamx) and
   448a9f5 (aamy). Customers `aw upgrade`-ing to 1.20.3 get both
   fixes together. aamy wires existing `checkLatestVersion` into
   `rootCmd.PersistentPreRun` for user-attention commands; 1h cache
   at $XDG_CONFIG_HOME/aw/update-check.json; skip list (run, heartbeat,
   events, notify, control, log, instructions, upgrade, version, lock
   renew); universal skips (--json, non-TTY, AW_NO_UPDATE_CHECK,
   dev/empty version). Code-reviewer subagent SHIP-OK with one P3
   non-blocker (aweb-aana — atomic temp+rename for cache write to
   prevent concurrent-process race). Closes the distribution-cadence
   gap Juan surfaced after 1.20.2 ship.

## Dev team work in flight

Quiet post-cycle. Grace shipped aweb-aamx (809056e) and aweb-aamy
(448a9f5) within minutes today. aweb-aana (P3 atomic-write follow-up)
+ aweb-aamz (P3 wait-semantics carry-over) on her queue when bandwidth
allows.

## Non-feature work in flight

- **Multi-team agent_id-vs-did comparison grep** (task #20, my plate,
  bandwidth-allowing). cp.agent_id is team-scoped — multi-team agents
  hit asymmetry when code compares on cp.agent_id instead of
  cp.did/cp.did_aw. The 1.20.2 fix bypassed this for the pagination
  case but other code paths in aweb may still have direct cp.agent_id
  comparisons.

## Release-ready state (handoff to Hestia)

Nothing in the release pipeline. Last ships:
- aweb-server-v1.20.3 + aw-v1.20.3: PyPI + npm latest, 2026-05-06 ~09:00Z
  (CLI-only, both aamx + aamy bundled).
- aweb-cloud v0.5.23: app.aweb.ai released, 2026-05-06 06:14:33Z (no
  v0.5.24 cut — aweb 1.20.3 was CLI-only).
- AC pin stays at aweb 1.20.2 in main; bumps only when functional
  AC change ships.
- b7e86745 (admin_analytics test fix) on AC main awaiting next AC
  release cycle.

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
