# Engineering Status
Last updated: 2026-05-18 16:15 GMT

## Current focus

0. **BLOCKED: AC hosted MCP OAuth selected-org fix is NOT production-ready.**
   Juan says the current solution is likely incomplete; Athena will not
   bless or forward to Hestia. Grace/Mia/Dave/Hestia have been notified.
   Required before any bless: Grace surfaces pushed AC branch/commits,
   Q2 targeted-handoff fail-closed fix + tests, Mia review, Athena
   invariant review, and explicit resolution of the incomplete-solution
   concern.
1. **Federation completion wave shipped.** aweb 1.23.0, awid 0.5.6,
   and AC v0.5.42 are verified-live per Hestia: app.aweb.ai
   reports `release_tag=v0.5.42`, `git_sha=7ca6ce62`,
   `aweb_version=1.23.0`, `awid_service_version=0.5.6`.
2. **Pi integration is ready in this workspace.** `@awebai/pi`
   channel awakenings + canonical aweb skills are installed; first
   session produced the synthetic welcome and the prescribed startup
   loop was run from Athena's Pi session.
3. **Pi first-session welcome (aweb-aaov.12)**: Dave implemented
   c675c44, docs-link follow-up 1944e3d, Iris tone nudge 37c9bb1;
   local aweb main now includes follow-up polish through 48cee5e.
   Task still shows claimed by Dave.
4. **Channel / skills packaging remains active.** `aweb-aaox.16` is
   the P0 license metadata correction for `@awebai/claude-channel`;
   Hestia owns publish. Hestia's status notes channel-v1.4.1 tag
   exists but npm publish failed on the channel-core install gap.

## Dev team work in flight

- **aweb-aaov.12 — Pi first-session synthetic welcome**: Dave owns;
  implemented and voice-passed. Next signal is final task close or
  release/publish handoff.
- **aweb-aaou.13 — messaging federation e2e matrix**: Grace owns;
  federation completion shipped through v0.5.42, but the active claim
  remains visible.
- **aweb-aalr.2 — AWID ensure-team endpoint + AC persist refactor**:
  Mia still has a stale claim from the older readiness epic.
- **AC hosted MCP OAuth selected-org regression**: Grace reportedly has
  a fix, but no branch/commit has reached Athena yet after repeated
  `git fetch --all --prune`. Blocked from production by Juan's
  incomplete-solution concern. Athena design calls sent: generic `/mcp/`
  may allow non-personal new-agent only after explicit org-first /
  team-second UI selection + server-side creation-authority revalidation;
  targeted dashboard handoff remains strict; invalid/stale/inaccessible /
  already-bound targeted handoff must fail closed and clear the bad
  cookie, never silently degrade to generic/personal flow.
- **aweb-aaox.16 — claude-channel license metadata P0**: ready work;
  Hestia publish-owner per task, engineering available if the release
  workflow/tooling fix needs code review.

## Non-feature work in flight

- No new non-feature code claimed in this wake-up.
- Historical open item remains the **multi-team agent_id-vs-did
  comparison grep**; the 1.20.7 strict-walk closed the known routing
  symptom, but the broader codebase grep has not been banked as done.

## Release-ready state (handoff to Hestia)

- **Do not deploy the selected-org OAuth fix.** No bless-and-run exists;
  Hestia was explicitly told to treat any release signal for this fix as
  blocked unless Athena sends an explicit reviewed bless.
- Latest verified-live chain per Operations: awid-service-v0.5.6,
  awid-v0.5.6, aweb 1.23.0, AC v0.5.42.
- Pi package release path appears to be in the aaov/aaox release lane;
  do not duplicate Hestia's publish work without an explicit handoff.

## Pending engineering artifacts owed

- **KI#1 closure decision record technical content** remains old debt
  unless Sofia has superseded it. Source:
  `agents/athena/aale-trust-contract.md` + aweb commit `7759abc`.
- **Playwright-MCP reproducer for Add-Existing dialog** remains old
  non-feature backlog. AC checkout is available at
  `/Users/juanre/prj/awebai/ac` (symlink to aweb-cloud), main clean at
  7b33fba9 as of 16:15 GMT.

## Risks

- **Channel publish drift**: channel-v1.4.1 tag exists but npm publish
  did not complete; public npm metadata may still show Proprietary
  until aaox.16 is closed.
- **Mail-delivery/auto-ack signal**: Hestia reports channel push
  auto-ack may hide mail from default inbox; treat inbox-empty as
  weaker signal until the second independent attestation/design call
  resolves the class.
- **Selected-org OAuth fix incomplete risk**: the reported fix may only
  partially address the dashboard → consent → OAuth POST contract. Do
  not let validation-count summaries substitute for code review of the
  actual handoff and server-side authority checks.

## Next checks

- Selected-org OAuth P0: wait for Grace to push/surface branch/commits;
  then review Q2 fail-closed stale-targeted-handoff fix + tests; wait for
  Mia approval before Athena bless.
- Sofia is drafting narrow claim-shape framing for this OAuth fix; loop
  her in before any customer-facing claim.
- Watch `aweb-aaov.12` for Dave's close/handoff and `aweb-aaox.16` for
  Hestia's publish result.
- If asked to act on Pi release, review the current aweb diff/commits
  against the aaov brief and preserve the Hestia publish boundary.
- If a channel event wakes this session, inspect event metadata and
  sender verification before acting; use mail for handoffs/status and
  chat only for blocking questions.

## Banked release-discipline (through 2026-05-07)

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
23. Test failures recurring at specific clock windows + reruns clean
    later are date/timezone-math signals, NOT transient-flake signals.
    "It passed on rerun" is not a diagnosis. Check whether the rerun
    delay corresponds to a UTC-vs-local-midnight crossing or other
    clock-based window before declaring transient.
24. Documented workarounds must be empirically attested against the
    actual customer surface AND the predecessor states they apply on
    top of, not just the surface they claim to work around.
25. When the empirical surface contradicts a hypothesis, that's a
    refutation, not a "transient." Don't double down on the
    hypothesis. Test against a known-OK case before narrowing scope.
26. "Affects only one customer in current base" is not a scope claim
    about the bug class — it's an observation about THIS customer base
    AT THIS MOMENT. Reproduce against an internal pair you control to
    distinguish customer-data class from product class.
27. Cut-the-deploy-only-if-functional-change. Don't cut a deploy
    release purely to keep a pin-in-tagged-release synced. Pin bump on
    main is valid state; tags should track functional changes.
27a. For CLI-only releases, don't bump server/pyproject.toml. The tag
    carries the CLI version (goreleaser uses GITHUB_REF_NAME). Source
    pkg state stays aligned with what's on PyPI for the server.
28. Tool-driven destructive git-state mutation is never acceptable as
    a side effect of a non-git-management command, even with loud
    warnings. Refuse + remediate, don't auto-fix the customer's repo.
