# Engineering Status
Last updated: 2026-05-20 22:31 GMT

## Current focus
- `aweb-aaph` implementation is complete: `.1/.2/.3/.4/.5/.6/.7` are closed.
- Final conformance heads: aweb `994972b` (CLI local/global/add-worktree test proof; current aweb `fed2391` adds unrelated channel cleanup) and AC `40e73eb4` (onboarding regression matrix aligned to current route/lifetime contract).
- Juan rejected carrying compatibility residue as a follow-up: because the aaph stack is not deployed yet, we are excising old identity/reachability/access vocabulary and control planes now.
- New P0 epic `aweb-aapj` is active: remove or quarantine `access_mode`, `address_reachability`, `reachability`/`visible_to_team_id`, `identity_type`, `persistent`/`ephemeral`, `messaging_policy`, and stale CLI flags before release.
- Hestia's no-deploy AC release-ready gate failed at AC `40e73eb4`: 37/1434 failures, primarily missing `current_did_key` on `chat_participants` / `conversation_participants`. Mia fixed this slice; Athena reviewed, fast-forwarded AC main to `82ec0b8d`, validated migration-path tests, and closed `aweb-aapi`. Broader AC cleanup continues in `aweb-aapj.3`.

## Dev team work in flight
- **aweb-aapj.1 — aweb/awid old reachability/lifetime authority removal**: assigned to Peter; ACKed. Scope: remove `messaging_policy` as active field, remove AWID reachability/visibility public authority, normalize old lifetime inputs at boundaries, add grep/allowlist tests.
- **aweb-aapj.2 — aw CLI/docs global/local language**: assigned to Grace; ACKed. Scope: replace `--persistent`/persistent/ephemeral/reachability user-facing help/docs with global/local; preserve stale args as compatibility aliases where practical.
- **aweb-aapj.3 — AC backend/schema/API cleanup**: assigned to Mia. Mia confirmed branch base AC `82ec0b8d`, reran survey, and is starting Phase A with a worked-example single-endpoint diff before broad sweep. DTO guidance sent: canonical `identity_scope=global|local`; stale fields input-only/backcompat; `address_reachability` deleted from normal output; `access_mode` fail-closed mapping to `inbound_mode`.
- **aweb-aapj.4 — AC frontend/docs cleanup**: assigned to Olivia. Olivia reset branch to AC `82ec0b8d`, reran frontend survey, and is proceeding frontend-only; synced `site/content/docs` stays out of scope (Grace/aweb owns canonical docs).
- **aweb-aapj.5 — cross-repo grep gate/release handoff**: Athena-owned and in progress after `.1`-`.4` land.
- **aweb-aapj.6 — Pi/skills package copy cleanup**: closed at aweb `e248cd3`. Athena reviewed/landed; Pi/skills instructional copy now uses addressability/inbound mode/global/local, with only explicit legacy/audit notes left in scoped skill source.
- **aweb-aapj.7 — channel runtime lifetime cleanup**: assigned to Dave after aapj.6 exposed `lifetime`/`persistent`/`ephemeral` strings in channel-core/channel runtime and generated Pi dist. Scope: normalize runtime to identity_scope/global/local with legacy lifetime adapters; branch-ready to Athena.
- **aweb-aapi — AC embedded aweb migration snapshot drift**: closed at AC `82ec0b8d` (new mirrored migration `006_participant_current_did_key.sql` + manifest tests).
- **Stale replay control**: channel backlog appears drained (`aw mail inbox` and `aw chat pending` clean). Continue checking current task comments/message IDs before acting.

## Non-feature work in flight
- Athena authored `aweb-aapj` breakdown/briefs and seeded initial grep inventories in `/tmp/aweb-legacy-hits.txt` and `/tmp/ac-legacy-hits.txt` (not authoritative yet; final gate is `aweb-aapj.5`).

## Release-ready state (handoff to Hestia)
- Release is held pending `aweb-aapj` cleanup and final `aweb-aapj.5` grep gate.
- Previous gate heads were aweb product-authority head `994972b` (current origin/main `fed2391` includes unrelated channel cleanup) and AC `40e73eb4`; AC main is now `82ec0b8d` with the aapi migration-drift fix. Heads will continue changing as `aweb-aapj` lands.
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
