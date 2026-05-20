# Engineering Status
Last updated: 2026-05-20 21:58 GMT

## Current focus
- `aweb-aaph` implementation is complete: `.1/.2/.3/.4/.5/.6/.7` are closed.
- Final conformance heads: aweb `994972b` (CLI local/global/add-worktree test proof; current aweb `fed2391` adds unrelated channel cleanup) and AC `40e73eb4` (onboarding regression matrix aligned to current route/lifetime contract).
- Juan rejected carrying compatibility residue as a follow-up: because the aaph stack is not deployed yet, we are excising old identity/reachability/access vocabulary and control planes now.
- New P0 epic `aweb-aapj` is active: remove or quarantine `access_mode`, `address_reachability`, `reachability`/`visible_to_team_id`, `identity_type`, `persistent`/`ephemeral`, `messaging_policy`, and stale CLI flags before release.
- Hestia's no-deploy AC release-ready gate failed at AC `40e73eb4`: 37/1434 failures, primarily missing `current_did_key` on `chat_participants` / `conversation_participants`; this is now folded into `aweb-aapj.3` while `aweb-aapi` remains visible as the concrete gate failure.

## Dev team work in flight
- **aweb-aapj.1 — aweb/awid old reachability/lifetime authority removal**: assigned to Peter; ACKed. Scope: remove `messaging_policy` as active field, remove AWID reachability/visibility public authority, normalize old lifetime inputs at boundaries, add grep/allowlist tests.
- **aweb-aapj.2 — aw CLI/docs global/local language**: assigned to Grace; ACKed. Scope: replace `--persistent`/persistent/ephemeral/reachability user-facing help/docs with global/local; preserve stale args as compatibility aliases where practical.
- **aweb-aapj.3 — AC backend/schema/API cleanup**: assigned to Mia. Scope: remove canonical `identity_type`, `lifetime`, `access_mode`, `address_reachability`, persistent/ephemeral API/schema surfaces; includes fixing AC embedded aweb migration drift (`aweb-aapi`).
- **aweb-aapj.4 — AC frontend/docs cleanup**: assigned to Olivia. Scope: dashboard/site copy and TS API types use custody/addressability/global/local; no normal UI controls for old access/reachability terms.
- **aweb-aapj.5 — cross-repo grep gate/release handoff**: Athena-owned and in progress after `.1`-`.4` land.
- **aweb-aapi — AC embedded aweb migration snapshot drift**: still open as concrete Hestia gate failure, but superseded/expanded by `aweb-aapj.3` per task comment.
- **Stale replay control**: channel backlog appears drained (`aw mail inbox` and `aw chat pending` clean). Continue checking current task comments/message IDs before acting.

## Non-feature work in flight
- Athena authored `aweb-aapj` breakdown/briefs and seeded initial grep inventories in `/tmp/aweb-legacy-hits.txt` and `/tmp/ac-legacy-hits.txt` (not authoritative yet; final gate is `aweb-aapj.5`).

## Release-ready state (handoff to Hestia)
- Release is held pending `aweb-aapj` cleanup and final `aweb-aapj.5` grep gate.
- Previous gate heads were aweb product-authority head `994972b` (current origin/main `fed2391` includes unrelated channel cleanup) and AC `40e73eb4`; these will change as `aweb-aapj` lands.
- Known release caveats: npm `@awebai/aw` remains `1.24.3`; do not claim npm/CLI `1.24.4`. AWID health still needs observed `0.5.7`. Juan hard-hold remains: no deploy/tag/publish until explicit clearance.
- Hestia was told no more release-ready runs until Athena says `aweb-aapj` cleanup is landed and ready for a no-deploy gate.

## Risks
- **Scope risk**: this is now a cross-repo cleanup, not a narrow release-gate patch. Watch overlap between Peter/Grace shared aweb structs and Mia/Olivia AC API shapes.
- **Backcompat risk**: current `aw` users may use stale args/files; edge adapters should normalize where practical, but old names must not remain canonical help/API/output.
- **Release-state confusion risk**: aweb server `1.24.4` and awid-service/awid `0.5.7` are already released; current work is pre-release cleanup before AC/aaph completion, not a deploy clearance.
- **Production row-disposition risk**: hidden/limited AWID rows stay fail-closed until owner/operator normalization. No silent widening or broad row-detail mail.

## Next checks
- Track ACK/branch-ready from Peter (`aweb-aapj.1`), Grace (`aweb-aapj.2`), Mia (`aweb-aapj.3`), Olivia (`aweb-aapj.4`).
- Review/land each branch against the briefs; require grep evidence and focused tests.
- Run `aweb-aapj.5` final cross-repo legacy-residue gate after `.1`-`.4` land, then ask Hestia for no-deploy release-ready.
- Keep npm/CLI `1.24.4` caveat and Juan deploy hold explicit.
