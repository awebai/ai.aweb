# Engineering Status
Last updated: 2026-05-20 21:35 GMT

## Current focus
- `aweb-aaph` implementation is complete: `.1/.2/.3/.4/.5/.6/.7` are closed.
- Final conformance heads: aweb `994972b` (CLI local/global/add-worktree test proof) and AC `40e73eb4` (onboarding regression matrix aligned to current route/lifetime contract).
- Grace confirmed `.7` approval via chat after channel replay check; approval mail message_id `9c522612-391a-4aad-819b-dc1485d52ad0` may have been missed during the replay burst.
- Next step is final wide/release handoff framing; Hestia must not gate/tag/deploy until Athena sends a fresh release handoff with exact current heads.

## Dev team work in flight
- **aweb-aaph.7 — final conformance**: closed. Grace approved aweb `994972b` + AC `40e73eb4`; focused validation covered aweb Go CLI, AC onboarding matrix, API-key, BYOT, hosted-add-existing, and diff-check clean. No bespoke precheck requested before Hestia beyond normal full release gates including Docker/full-service e2e where available.
- **Stale replay control**: channel backlog appears drained (`aw mail inbox` and `aw chat pending` clean). Continue checking current task comments/message IDs before acting.

## Non-feature work in flight
- None beyond `.7` conformance tests.

## Release-ready state (handoff to Hestia)
- `aweb-aaph` engineering complete. Preparing fresh release handoff for Hestia.
- Gate heads for handoff: aweb `994972b`; AC `40e73eb4`.
- Known release caveat: npm `@awebai/aw` remains `1.24.3`; do not claim npm/CLI `1.24.4` until npm publish is fixed and verified.

## Risks
- **Stale coordination risk**: channel/mail replay is causing peers to act on old aapg/aaph messages. Verify message IDs/timestamps and current git heads before acting.
- **Release-state confusion risk**: aweb server `1.24.4` and awid-service/awid `0.5.7` are already released; current work is AC/aaph completion, not another aweb/aapg gate.
- **Production row-disposition risk**: hidden/limited AWID rows stay fail-closed until owner/operator normalization. No silent widening or broad row-detail mail.

## Next checks
- Prepare/send final Hestia release handoff with aweb `994972b`, AC `40e73eb4`, validation evidence, and caveats.
- Keep npm/CLI `1.24.4` caveat explicit.
- Do not resurrect old review refs; patch forward only if Hestia gate finds a concrete blocker.
