# Engineering Status
Last updated: 2026-05-21 10:44 GMT

## Current focus
- Step-back architecture read: not fully simplified yet. aweb-side authority is much cleaner at current aweb main `8337af1`, but AC main `82ec0b8d` and some aweb/AWID public/static docs still leak old product authority vocabulary.
- `aweb-aapj` remains the release blocker. Closed aweb-side core slices: `.1` (`8337af1`), `.2` (`bfe822d`), `.6` (`e248cd3`), `.7` (`2e98603`).
- Remaining product-authority blockers: AC backend/schema/API cleanup (`.3`), AC frontend cleanup (`.4`), new aweb public/static docs + doctor-output cleanup (`.8`), then final cross-repo grep gate (`.5`).
- Hestia's prior no-deploy release-ready gate failure at AC `40e73eb4` was fixed by `aweb-aapi` at AC `82ec0b8d`; do not rerun release-ready until all aapj blockers land.

## Dev team work in flight
- **aweb-aapj.1 — aweb/awid old reachability/lifetime authority removal**: closed at aweb `8337af1` (Peter `e48b46c` rebased over Grace `bfe822d` plus Athena wording polish). Removes AWID address reachability/visibility authority, drops aweb `messaging_policy`, migrates aweb agents storage from lifetime to `identity_scope`, and leaves explicit boundary adapters only.
- **aweb-aapj.2 — aw CLI/docs global/local language**: closed at aweb `bfe822d`. CLI/help/docs use global/local; old flags hidden as compatibility aliases; developer-facing test wording cleaned.
- **aweb-aapj.3 — AC backend/schema/API cleanup**: assigned to Mia. Mia confirmed branch base AC `82ec0b8d`, reran survey, and is starting Phase A with a worked-example single-endpoint diff before broad sweep. DTO guidance sent: canonical `identity_scope=global|local`; stale fields input-only/backcompat; `address_reachability` deleted from normal output; `access_mode` fail-closed mapping to `inbound_mode`.
- **aweb-aapj.4 — AC frontend/docs cleanup**: approved branch-ready at `eec512d4`, but held for merge until `.3` lands because the frontend expects post-`.3` canonical wire shapes (`identity_scope`, removed old response fields).
- **aweb-aapj.5 — cross-repo grep gate/release handoff**: Athena-owned and in progress after `.3`, `.4`, and `.8` land.
- **aweb-aapj.6 — Pi/skills package copy cleanup**: closed at aweb `e248cd3`. Athena reviewed/landed; Pi/skills instructional copy now uses addressability/inbound mode/global/local, with only explicit legacy/audit notes left in scoped skill source.
- **aweb-aapj.7 — channel runtime lifetime cleanup**: closed at aweb `2e98603`. Athena reviewed/landed; channel/channel-core runtime now canonicalizes identity_scope=global|local with legacy lifetime adapters. Validation rerun: focused channel 69, channel-core build, channel build, full channel tests 95, Pi build, diff-check clean.
- **aweb-aapj.8 — public/static docs + doctor output cleanup**: closed at aweb `e332bf8`. Athena validated diff-check, targeted public/static docs grep clean, doctor stale phrase grep clean, Go cmd/aw+awid, server package-data, CLI reference check.
- Peter support review found a real AC/aweb two-world blocker: AC dashboard constructs `TeamIdentity(lifetime=...)`, while current aweb source requires `identity_scope`. Mia added `test-backend-aweb-local` prerequisite at AC branch `e1e476ee`, Phase B (1/2) mirror migrations/tests at `a42ddd6c`, and Phase B 2/2 partials through `bf1215eb` (dashboard/immediate_connect, mcp_oauth/contact predicates, agent_lifecycle/identity_workspace, embedded bootstrap/scope_agents/onboarding/init slice, SQL SELECT sweep). AC editing remains with Mia while Peter focuses `.12`. Athena directed support/admin/audit old fields must move under nested `legacy:{...}` in `.3`, not follow-up.
- `aweb-aapj.4` validation rerun by Athena: diff-check, aapj vocab gate, targeted greps, dashboard build, frontend tests (38 files / 194 tests), lint (0 errors; 2 unrelated warnings), and frontend build. Dave re-reviewed with no blockers.
- New support tasks to keep idle agents applied: `aweb-aapj.9` assigned to Peter for AC Phase B 2/2 file-by-file rewrite map; `aweb-aapj.10` assigned to Dave for final `.5` grep-gate dry-run prep.
- Dave’s `.10` dry-run surfaced two additional aweb blockers before final `.5`: `aweb-aapj.11` is closed at aweb `5f4dc04` (public CLI/SOT docs cleanup); `aweb-aapj.12` is closed at aweb `bdc39e4` (AWID team-certificate API/storage/cert JSON canonical `identity_scope`).
- Grace created `aweb-aapj.13` for AWCO/BYOIDT team-certified signed request mode. Grace pushed initial implementation at aweb `7ce0f39`; Athena validation rerun is green but closure is blocked pending missing acceptance evidence: no-`--sign` team-auth test, global-workspace team-auth test, and verifier rejection fixture/evidence.
- **aweb-aapi — AC embedded aweb migration snapshot drift**: closed at AC `82ec0b8d` (new mirrored migration `006_participant_current_did_key.sql` + manifest tests).
- **Stale replay control**: channel backlog appears drained (`aw mail inbox` and `aw chat pending` clean). Continue checking current task comments/message IDs before acting.

## Non-feature work in flight
- Athena authored `aweb-aapj` breakdown/briefs and seeded initial grep inventories in `/tmp/aweb-legacy-hits.txt` and `/tmp/ac-legacy-hits.txt` (not authoritative yet; final gate is `aweb-aapj.5`).

## Release-ready state (handoff to Hestia)
- Release is held pending `aweb-aapj` cleanup and final `aweb-aapj.5` grep gate.
- Current heads: aweb main `7ce0f39` (`.13` initial, not yet closed); AC main `82ec0b8d`; in-flight AC branches `origin/mia/aapj-3-phase-a` at `bf1215eb`, `origin/olivia-aapj-4` at `eec512d4`.
- Do not release aweb alone at `8337af1` while AC remains old-authority-shaped; that would split product authority across global/local aweb and lifetime/access/reachability AC.
- Known release caveats: npm `@awebai/aw` remains `1.24.3`; do not claim npm/CLI `1.24.4`. AWID health still needs observed `0.5.7`. Juan hard-hold remains: no deploy/tag/publish until explicit clearance.
- Hestia was told no more release-ready runs until Athena says `aweb-aapj` cleanup is landed and ready for a no-deploy gate.

## Risks
- **Split-authority risk**: aweb main is mostly global/local while AC main still exposes/uses lifetime/access_mode/address_reachability/reachability in canonical areas. Release must wait for AC cleanup.
- **Two-world dependency risk**: AC local tests currently use PyPI `aweb==1.24.4` while release image uses sibling aweb source. For aapj Phase B, test/release validation must use sibling aweb `e332bf8+`; no Hestia tag/publish just to unblock local tests under Juan hold.
- **Public-doc risk**: `awid/site/static` and some doctor/support output still teach persistent/ephemeral unless `.8` cleans them.
- **AWID hidden/limited row-disposition risk**: aapj.1 drops reachability/visible columns. Before release, verify hidden/limited production row disposition or get explicit Juan/operator decision; do not silently widen privacy.
- **Backcompat risk**: current `aw` users may use stale args/files; edge adapters should normalize where practical, but old names must not remain canonical help/API/output.

## Next checks
- Track Mia’s immediate ACK/progress on `.3` Phase B 2/2; if she cannot take it now, reroute implementation rather than waiting.
- Track Peter `.9` rewrite map and Dave `.10` gate dry-run; fold their findings into `.3` review and `.5`.
- Track Mia `.3` to branch-ready; remaining final `.5` blocker is AC cleanup plus `.13` if Juan/Sofia declare it release-gating.
- Track Grace `.13` as parallel AWCO/BYOIDT support lane; confirm with Juan/Sofia whether it gates the immediate aaph/aapj release or follows after `.5` cleanup gate.
- Review/land each branch against the briefs; require grep evidence and focused tests.
- Run `aweb-aapj.5` final cross-repo legacy-residue gate after `.3`/`.4`/`.8` land, then ask Hestia for no-deploy release-ready.
- Resolve AWID hidden/limited row disposition before any release/deploy.
- Keep npm/CLI `1.24.4` caveat and Juan deploy hold explicit.
