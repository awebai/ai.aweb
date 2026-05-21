# Engineering Status
Last updated: 2026-05-21 08:06 GMT

## Current focus
- Step-back architecture read: not fully simplified yet. aweb-side authority is much cleaner at current aweb main `8337af1`, but AC main `82ec0b8d` and some aweb/AWID public/static docs still leak old product authority vocabulary.
- `aweb-aapj` remains the release blocker. Closed aweb-side core slices: `.1` (`8337af1`), `.2` (`bfe822d`), `.6` (`e248cd3`), `.7` (`2e98603`).
- Remaining product-authority blockers: AC backend/schema/API cleanup (`.3`), AC frontend cleanup (`.4`), new aweb public/static docs + doctor-output cleanup (`.8`), then final cross-repo grep gate (`.5`).
- Hestia's prior no-deploy release-ready gate failure at AC `40e73eb4` was fixed by `aweb-aapi` at AC `82ec0b8d`; do not rerun release-ready until all aapj blockers land.

## Dev team work in flight
- **aweb-aapj.1 — aweb/awid old reachability/lifetime authority removal**: closed at aweb `8337af1` (Peter `e48b46c` rebased over Grace `bfe822d` plus Athena wording polish). Removes AWID address reachability/visibility authority, drops aweb `messaging_policy`, migrates aweb agents storage from lifetime to `identity_scope`, and leaves explicit boundary adapters only.
- **aweb-aapj.2 — aw CLI/docs global/local language**: closed at aweb `bfe822d`. CLI/help/docs use global/local; old flags hidden as compatibility aliases; developer-facing test wording cleaned.
- **aweb-aapj.3 — AC backend/schema/API cleanup**: assigned to Mia. Mia confirmed branch base AC `82ec0b8d`, reran survey, and is starting Phase A with a worked-example single-endpoint diff before broad sweep. DTO guidance sent: canonical `identity_scope=global|local`; stale fields input-only/backcompat; `address_reachability` deleted from normal output; `access_mode` fail-closed mapping to `inbound_mode`.
- **aweb-aapj.4 — AC frontend/docs cleanup**: assigned to Olivia. Olivia reset branch to AC `82ec0b8d`, reran frontend survey, and is proceeding frontend-only; synced `site/content/docs` stays out of scope (Grace/aweb owns canonical docs).
- **aweb-aapj.5 — cross-repo grep gate/release handoff**: Athena-owned and in progress after `.3`, `.4`, and `.8` land.
- **aweb-aapj.6 — Pi/skills package copy cleanup**: closed at aweb `e248cd3`. Athena reviewed/landed; Pi/skills instructional copy now uses addressability/inbound mode/global/local, with only explicit legacy/audit notes left in scoped skill source.
- **aweb-aapj.7 — channel runtime lifetime cleanup**: closed at aweb `2e98603`. Athena reviewed/landed; channel/channel-core runtime now canonicalizes identity_scope=global|local with legacy lifetime adapters. Validation rerun: focused channel 69, channel-core build, channel build, full channel tests 95, Pi build, diff-check clean.
- **aweb-aapj.8 — public/static docs + doctor output cleanup**: newly created and assigned to Grace after reassessment found stale AWID static docs and doctor/support output still teaching persistent/ephemeral as product language.
- **aweb-aapi — AC embedded aweb migration snapshot drift**: closed at AC `82ec0b8d` (new mirrored migration `006_participant_current_did_key.sql` + manifest tests).
- **Stale replay control**: channel backlog appears drained (`aw mail inbox` and `aw chat pending` clean). Continue checking current task comments/message IDs before acting.

## Non-feature work in flight
- Athena authored `aweb-aapj` breakdown/briefs and seeded initial grep inventories in `/tmp/aweb-legacy-hits.txt` and `/tmp/ac-legacy-hits.txt` (not authoritative yet; final gate is `aweb-aapj.5`).

## Release-ready state (handoff to Hestia)
- Release is held pending `aweb-aapj` cleanup and final `aweb-aapj.5` grep gate.
- Current heads: aweb main `8337af1`; AC main `82ec0b8d`; in-flight AC branches `origin/mia/aapj-3-phase-a` at `7093f693`, `origin/olivia-aapj-4` at `473f74f0`.
- Do not release aweb alone at `8337af1` while AC remains old-authority-shaped; that would split product authority across global/local aweb and lifetime/access/reachability AC.
- Known release caveats: npm `@awebai/aw` remains `1.24.3`; do not claim npm/CLI `1.24.4`. AWID health still needs observed `0.5.7`. Juan hard-hold remains: no deploy/tag/publish until explicit clearance.
- Hestia was told no more release-ready runs until Athena says `aweb-aapj` cleanup is landed and ready for a no-deploy gate.

## Risks
- **Split-authority risk**: aweb main is mostly global/local while AC main still exposes/uses lifetime/access_mode/address_reachability/reachability in canonical areas. Release must wait for AC cleanup.
- **Public-doc risk**: `awid/site/static` and some doctor/support output still teach persistent/ephemeral unless `.8` cleans them.
- **AWID hidden/limited row-disposition risk**: aapj.1 drops reachability/visible columns. Before release, verify hidden/limited production row disposition or get explicit Juan/operator decision; do not silently widen privacy.
- **Backcompat risk**: current `aw` users may use stale args/files; edge adapters should normalize where practical, but old names must not remain canonical help/API/output.

## Next checks
- Track branch-ready from Mia (`aweb-aapj.3`), Olivia (`aweb-aapj.4`), and Grace (`aweb-aapj.8`).
- Review/land each branch against the briefs; require grep evidence and focused tests.
- Run `aweb-aapj.5` final cross-repo legacy-residue gate after `.3`/`.4`/`.8` land, then ask Hestia for no-deploy release-ready.
- Resolve AWID hidden/limited row disposition before any release/deploy.
- Keep npm/CLI `1.24.4` caveat and Juan deploy hold explicit.
