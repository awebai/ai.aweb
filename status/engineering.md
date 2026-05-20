# Engineering Status
Last updated: 2026-05-20 21:46 GMT

## Current focus
- `aweb-aaph` implementation is complete: `.1/.2/.3/.4/.5/.6/.7` are closed.
- Final conformance heads: aweb `994972b` (CLI local/global/add-worktree test proof; current aweb `fed2391` adds unrelated channel cleanup) and AC `40e73eb4` (onboarding regression matrix aligned to current route/lifetime contract).
- Hestia's no-deploy AC release-ready gate failed at AC `40e73eb4`: 37/1434 failures, primarily missing `current_did_key` on `chat_participants` / `conversation_participants` because AC's embedded aweb migration snapshot lags pinned `aweb==1.24.4`.
- Juan/Grace simplification assessment: aaph materially simplified the supported product contract, but implementation still has quarantined compatibility residue that needs a mechanical cleanup follow-up.

## Dev team work in flight
- **aweb-aapi — AC embedded aweb migration snapshot drift**: P0 bug assigned to Mia. Acceptance: forward-only fix so AC embedded/provisioned aweb schema includes the participant `current_did_key` columns expected by pinned `aweb==1.24.4`, plus a drift-prevention verification. No tags/deploys/version bumps; branch-ready to Athena.
- **aweb-aaph.7 — final conformance**: closed. Grace approved aweb `994972b` + AC `40e73eb4`; focused validation covered aweb Go CLI, AC onboarding matrix, API-key, BYOT, hosted-add-existing, and diff-check clean. Full release gate is blocked on `aweb-aapi`.
- **Stale replay control**: channel backlog appears drained (`aw mail inbox` and `aw chat pending` clean). Continue checking current task comments/message IDs before acting.

## Non-feature work in flight
- Simplification/stale-code assessment complete enough for Juan: simple model + quarantined residue, not fully simplified implementation. Cleanup follow-up should be grep-driven: old nouns only in migrations, explicit compatibility/audit/support docs, and tests that name compatibility behavior.

## Release-ready state (handoff to Hestia)
- `aweb-aaph` feature work is complete, but release-ready is red.
- Gate heads: aweb product-authority head `994972b` (current origin/main `fed2391` includes unrelated channel cleanup); AC `40e73eb4`.
- Blocking gate failure: AC embedded aweb migration snapshot missing participant `current_did_key` columns for pinned `aweb==1.24.4`; tracked as `aweb-aapi`.
- Known release caveats: npm `@awebai/aw` remains `1.24.3`; do not claim npm/CLI `1.24.4`. AWID health still needs observed `0.5.7`. Juan hard-hold remains: no deploy/tag/publish until explicit clearance.

## Risks
- **Release-blocking schema drift**: AC's embedded aweb migration snapshot can lag pinned aweb package migrations; `aweb-aapi` must fix and add verification before release-ready can go green.
- **Compatibility-residue risk**: access_mode/address_reachability/reachability/visible_to_team_id/identity_type/persistent/ephemeral remain in many surfaces; must stay quarantined as compatibility/audit/storage until deleted.
- **Release-state confusion risk**: aweb server `1.24.4` and awid-service/awid `0.5.7` are already released; current work is AC/aaph completion, not another aweb/aapg gate.
- **Production row-disposition risk**: hidden/limited AWID rows stay fail-closed until owner/operator normalization. No silent widening or broad row-detail mail.

## Next checks
- Wait for Mia's `aweb-aapi` branch-ready signal; review migration drift fix and verification.
- After `aweb-aapi` lands, ask Hestia to rerun no-deploy AC release-ready.
- Report simplification assessment to Juan: significant product-contract simplification, not yet fully simplified implementation; recommend mechanical compatibility-residue cleanup follow-up.
- Keep npm/CLI `1.24.4` caveat and Juan deploy hold explicit.
