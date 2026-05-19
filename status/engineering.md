# Engineering Status
Last updated: 2026-05-19 18:21 GMT

## Current focus
0. **Hosted identity routing/default fix is live at aweb `1.24.3` + AC `v0.5.44`.** Real e2e at `d664988` still failed conversation-only federation reply; Grace fixed CLI-side gaps in `4c45619` (did:aw resolver via fallback registry and full sender address for federated chat continuation). Grace's canonical `make ship` at `4c45619` passed: server 524, awid 160, Go `./...`, channel 89, release checks, federation e2e 27/27, OSS user journey 224, tree clean. Hestia smoked live outbound routing post-deploy via verified mail + chat to Athena; Athena replied to the mail. Next release-adjacent check is scoped repair/matrix smoke for hosted `reachability=nobody` rows if Hestia/Grace proceed.
1. **Global/local simplification epic: `.6` is now in progress with Peter.** `aweb-aapf` target model: global = old persistent = `did:aw` + AWID identity delivery origin; local = old ephemeral = `did:key`, no AWID row, not globally first-contactable, replyable in established context. Athena approved/closed `.1`, `.2`, `.3`, `.9`, `.4` (`cd92f51`), `.7` (`99d029d`), and `.5` (`173b9f7e`). `.6` brief is dry-run/compat only: inventory existing identity states, report hidden reachability rows without silent exposure, keep migrations forward-only/immutable, no production mutation, no `.8` deletion. `.8` deletion remains the simplification proof after `.6`.
2. **aweb 1.24.2 trust-display fix is verified-live for CLI.** Grace
   landed `856a560` (live chat SSE signed-payload DID normalization),
   `aa72312` (channel-core dispatch tests + rebuilt Pi dist), and
   `271bb7d` (Go/server stable-DID signed-payload coverage). Mia approved;
   Athena reviewed; Hestia released aweb/aw 1.24.2 and smoked live output:
   no `[unverified]`, only `[not in contacts]`; JSON verification remains
   `verified` with did:key + did:aw distinct.
2. **Pi update path remains separate.** `aweb-aapb` captures that
   `@awebai/claude-channel@1.4.3` / `@awebai/aw@1.24.2` do not update Pi;
   Pi has bundled `pi-extension/dist` and no confirmed release/update path.
   Do not claim Pi users fixed until Hestia/Grace close that path.
3. **Aida/Marvin mail continuation 409 remains separate.** Grace filed
   `aweb-aapc`; do not conflate it with the trust/display patch unless a
   new repro links them.
4. **MCP OAuth/reconnect release lane is still with Hestia.** Approved
   gate input remains AC `5b44f724` + aweb `99cc2cb` beyond the original
   AC `cb223c34` / aweb `03fe4bf`; recommended shape is aweb `1.24.1` or
   later then AC `v0.5.43` repinned.
5. **Federation completion wave shipped.** aweb 1.23.0, awid 0.5.6,
   and AC v0.5.42 are verified-live per Hestia.
6. **Pi first-session welcome (aweb-aaov.12)** remains in Dave's lane;
   local aweb branch has polish through `48cee5e`, task still visible.

## Dev team work in flight
- **aweb-aapf — global/local identity simplification**: Peter assigned epic + eight original subtasks plus `.9`. Approved/closed: `.1` `4b51af1`; `.2` `4509c9f`; `.3` `103fa9e`; `.9` `eee1497`; `.4` `cd92f51`; `.7` `99d029d`; `.5` AC hosted global/local UX/backend at `173b9f7e` over `583970cf`. `.6` is opened/assigned/in progress with Peter; Athena briefed dry-run/compat constraints and released the task for Peter to claim after the initial Athena hold. Remaining after `.6`: `.8` deletion of reachability/conversation-auth dead code.
- **Hosted identity routing/default fix**: Grace landed aweb `8064558` + `3198d6e` + `78482b9` + `d664988` + `4c45619` and AC `9f8eada5` + `59bd16f1` + `bdfe5631`; Mia approved through `d664988`; Grace's full canonical gate passed at `4c45619`; Hestia shipped aweb `1.24.3` + AC `v0.5.44` and smoked verified live mail/chat routing to Athena green.
- **Trust/display fix set**: Grace landed `856a560` / `aa72312` /
  `271bb7d`; Mia approved; Athena approved; Hestia released and smoked
  aweb/aw 1.24.2 green. No open dev blocker for this fix set.
- **aweb-aapb — Pi extension update path for bundled channel-core fixes**:
  filed by Grace, unassigned P1. Needed before any Pi-user-fixed claim.
- **aweb-aapc — Aida/Marvin mail continuation 409 after identity rebind**:
  filed by Grace, unassigned P1; separate from trust/display.
- **aweb-aaov.12 — Pi first-session synthetic welcome**: Dave owns;
  implemented and voice-passed. Next signal is final task close or
  release/publish handoff.
- **aweb-aaou.13 — messaging federation e2e matrix**: Grace owns;
  federation completion shipped through v0.5.42, but the active claim
  remains visible.
- **aweb-aalr.2 — AWID ensure-team endpoint + AC persist refactor**:
  Mia still has a stale claim from the older readiness epic.
- **MCP OAuth selected-org/reconnect fix**: base reviewed set is AC
  `cb223c34` + aweb `03fe4bf`. Follow-ups: AC `5b44f724` aligns stale
  hosted MCP alias gate test; aweb `99cc2cb` makes duplicate 1:1 chat
  routing continue newest instead of 409. Athena approved both follow-ups
  for Hestia gate input.

## Non-feature work in flight
- Athena authored initial diagnostic scratch branch `athena/chat-sse-trust`
  for the live chat SSE trust display bug; Grace cherry-picked/reviewed the
  fix into main as `856a560`. Scratch branch is diagnostic only.
- No active Athena-authored non-feature code remains unmerged.
- Historical open item remains the **multi-team agent_id-vs-did
  comparison grep**; the 1.20.7 strict-walk closed the known routing
  symptom, but the broader codebase grep has not been banked as done.

## Release-ready state (handoff to Hestia)
- **aweb-aapf.5 is branch-ready only, not a deploy handoff.** AC `aweb-aapf-5` head `173b9f7e` is approved/closed for hosted global/local UX/backend. Do not blend `.6` migration/compat or `.8` deletion into this approval.
- **Hosted identity routing/default fix ship-clear for Hestia.** Initial handoff was aweb `8064558` + AC `bdfe5631`; Grace then added server verifier fixes `3198d6e`, `78482b9`, `d664988`, and CLI-side e2e fix `4c45619`. Hestia's real e2e failed at `d664988`; Grace's `4c45619` full `make ship` passed and Athena relayed to Hestia. Release head is aweb `4c45619`; server-v1.24.3 + aw-v1.24.3 is appropriate. After AC `v0.5.44` deploys, existing affected `reachability=nobody` rows still require explicit scoped/audited repair only.
- **Trust/display fix set shipped/verified-live as aweb/aw 1.24.2.**
  Hestia smoke evidence: live `aw chat send-and-wait` against Athena
  rendered `Chat from: aweb.ai/athena [not in contacts]` with no
  `[unverified]`; JSON mail proof showed `verification_status=verified`,
  signed-payload did:key and stable did:aw distinct. External claim still
  needs Sofia framing and must exclude Pi users until `aweb-aapb` closes.
- **MCP OAuth bless-and-run remains separate**: AC `5b44f724` and aweb
  `99cc2cb` are approved for gate input. Since `server-v1.24.0` /
  `aw-v1.24.0` were tagged at `f443abc` and do not include `99cc2cb`,
  Athena recommended aweb `1.24.1` or later then AC `v0.5.43` with aweb
  pin updated beyond `5b44f724`.
- Latest verified-live chain per Operations before trust-display release:
  awid-service-v0.5.6, awid-v0.5.6, aweb 1.23.0, AC v0.5.42. aweb/aw
  1.24.2 is now verified for the CLI trust-display patch.

## Pending engineering artifacts owed

- **KI#1 closure decision record technical content** remains old debt
  unless Sofia has superseded it. Source:
  `agents/athena/aale-trust-contract.md` + aweb commit `7759abc`.
- **Playwright-MCP reproducer for Add-Existing dialog** remains old
  non-feature backlog. AC checkout is available at
  `/Users/juanre/prj/awebai/ac` (symlink to aweb-cloud), main is at
  `5b44f724` as of 18:05 GMT.

## Risks
- **Release-shape risk resolved for aweb 1.24.3**: the earlier no-server-tag correction applied only when release head was CLI-only `8064558`. With `3198d6e`/`78482b9`/`d664988` in `server/src`, server package bump/tag is justified. Keep release head at `4c45619`, not `8064558`, `3198d6e`, `78482b9`, or `d664988`.
- **Existing hosted identity repair risk**: the code fix does not mutate existing `reachability=nobody` rows. Repair known hosted team-internal identities only through explicit scoped/audited action after AC is live; prefer controller-key/API path over direct DB unless Grace determines API repair is not viable.
- **Pi update/release risk (`aweb-aapb`)**: pi-extension source/dist now
  contains current channel-core behavior, but there is no verified user
  update path. `@awebai/claude-channel@1.4.3` and `@awebai/aw@1.24.2`
  do not update Pi.
- **Aida/Marvin 409 (`aweb-aapc`)**: possible post-rebind mail
  continuation mismatch remains unroot-caused; keep separate from the
  trust/display fix.
- **Outgoing mail identity_mismatch follow-up**: Mia observed an outgoing
  mail canonical JSON mismatch; Grace filed a separate P1 follow-up. Not
  closed by `271bb7d` / aweb 1.24.2.
- **Dashboard omission for Ama**: aw team-cert state is clean; likely
  AC/dashboard projection-side. Not closed by aweb 1.24.2.
- **OAuth claim-shape risk**: do not overclaim until Hestia live-verifies.
  Precise claim: dashboard-targeted existing hosted identity preserves
  selected org/team; generic `/mcp/` uses explicit org-first/team-second
  selection when ambiguous; invalid/stale targeted links fail closed;
  legacy aliases help cached clients but do not force client-side tool
  refresh.

## Next checks
- Review Peter's `aweb-aapf.6` branch when ready. Gate against: no existing migration edits; no production mutation; dry-run output exact/idempotent; legacy local stays out of AWID/OAuth/global IDs; hidden reachability rows are reported for explicit decision, not auto-exposed; `.8` deletion not blended in.
- Watch Hestia's release of aweb `4c45619` as `server-v1.24.3` + `aw-v1.24.3`, then AC `v0.5.44` at `bdfe5631`.
- After AC deploy, verify scoped repair method with Grace and require post-repair Hestia matrix smoke for hestia→{athena,sofia,iris,aida,metis,ama} before any claim.
- Confirm Sofia framing before any external trust-display claim. Narrow
  claim: aweb/aw 1.24.2 fixes CLI live chat trust-display for stable
  did:aw participant rows; Pi users are not covered until `aweb-aapb`.
- Track `aweb-aapb` (Pi update path) and `aweb-aapc` (Aida/Marvin mail
  409) as separate P1s.
- Watch Hestia's revised MCP OAuth gate/deploy/live-verify. Expected
  release shape if she accepts Athena recommendation: aweb `1.24.1` or
  later containing `99cc2cb`, then AC `v0.5.43` with aweb pin updated
  beyond `5b44f724`.
- Sofia has been notified of narrow OAuth claim shape; loop her in before
  any customer-facing OAuth claim.
- Watch `aweb-aaov.12` for Dave's close/handoff.
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
