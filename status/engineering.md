# Engineering Status
Last updated: 2026-05-21 14:12 GMT

## Current focus
- `aweb-aapj.3` landed on AC main at `b0e82553`; `aweb-aapj.4` merged after it at AC main `f52f5481`. No tag/deploy/release.
- Grace's narrow re-review passed for AC `0caaefc4`; the three `.5` AC cleanup blockers are closed.
- aweb main is now `d300b33`: added Grace-requested migration regression proving AWID hidden/limited row disposition fails closed for active non-neutral rows and passes for deleted/neutral rows.
- Per Juan, Hestia has been asked to run full validation/all tests for aweb `d300b33` + AC `0caaefc4`, with explicit no tag/deploy/publish/version-bump/prod-migration boundary (mail `75231d6a-bc88-4441-922f-50649c30e4bd`).

## Dev team work in flight
- **aweb-aapj.1 — aweb/awid old reachability/lifetime authority removal**: closed at aweb `8337af1` (Peter `e48b46c` rebased over Grace `bfe822d` plus Athena wording polish). Removes AWID address reachability/visibility authority, drops aweb `messaging_policy`, migrates aweb agents storage from lifetime to `identity_scope`, and leaves explicit boundary adapters only.
- **aweb-aapj.2 — aw CLI/docs global/local language**: closed at aweb `bfe822d`. CLI/help/docs use global/local; old flags hidden as compatibility aliases; developer-facing test wording cleaned.
- **aweb-aapj.3 — AC backend/schema/API cleanup**: closed and landed on AC main at `b0e82553`. Athena review evidence: diff-check clean; focused sibling-source backend validation green (`118 passed`); Mia full-suite report was `1410 passed / 7 deselected`; direct run of ignored `auth_bridge_oss_cases.py` still fails but the representative failure reproduces on `origin/main`, so it is not a `.3` blocker.
- **aweb-aapj.4 — AC frontend/docs cleanup**: closed earlier, now merged to AC main at `f52f5481`. Post-merge validation: diff-check clean, `frontend/scripts/check-aapj-vocabulary.sh` OK, frontend vitest green (`38 files / 194 tests passed`; existing jsdom `window.scrollTo` stderr only).
- **aweb-aapj.5 — cross-repo grep gate/release handoff**: Grace found three final AC blockers on `d80fe410`; Athena patched and landed AC `0caaefc4`; Grace's narrow re-review passed. Validation: diff-check clean; frontend aapj vocab gate OK; hidden-import grep for deleted `identity_types.py` helpers clean; backend py_compile touched/related files green; frontend vitest 38/194 green; frontend build green. Reports: `/tmp/aapj5-gracefix-20260521134728/{raw.txt,strict.txt}`.
- **AWID hidden/limited row disposition**: Athena landed aweb `605f356` so migration `003_drop_address_reachability.sql` refuses to drop legacy visibility columns while active non-neutral address rows exist. Grace said SQL shape was correct but required focused migration evidence. Athena landed aweb `d300b33` with that regression; validation: aweb diff-check clean; `uv --directory awid run pytest tests/test_schema.py -q` 8 passed; `make test-awid` 172 passed.
- **aweb-aapj.6 — Pi/skills package copy cleanup**: closed at aweb `e248cd3`. Athena reviewed/landed; Pi/skills instructional copy now uses addressability/inbound mode/global/local, with only explicit legacy/audit notes left in scoped skill source.
- **aweb-aapj.7 — channel runtime lifetime cleanup**: closed at aweb `2e98603`. Athena reviewed/landed; channel/channel-core runtime now canonicalizes identity_scope=global|local with legacy lifetime adapters. Validation rerun: focused channel 69, channel-core build, channel build, full channel tests 95, Pi build, diff-check clean.
- **aweb-aapj.8 — public/static docs + doctor output cleanup**: closed at aweb `e332bf8`. Athena validated diff-check, targeted public/static docs grep clean, doctor stale phrase grep clean, Go cmd/aw+awid, server package-data, CLI reference check.
- Peter support review found a real AC/aweb two-world blocker: AC dashboard constructs `TeamIdentity(lifetime=...)`, while current aweb source requires `identity_scope`. Mia added `test-backend-aweb-local` prerequisite at AC branch `e1e476ee`, Phase B (1/2) mirror migrations/tests at `a42ddd6c`, and Phase B 2/2 partials through `78eefd02`. AC editing remains with Mia. Athena directed support/admin/audit old fields must move under nested `legacy:{...}` in `.3`; Mia applied this to archive/replace/replacement audit envelopes and was told to rename internal SQL aliases to `legacy_lifetime`.
- `aweb-aapj.4` validation rerun by Athena: diff-check, aapj vocab gate, targeted greps, dashboard build, frontend tests (38 files / 194 tests), lint (0 errors; 2 unrelated warnings), and frontend build. Dave re-reviewed with no blockers.
- New support tasks to keep idle agents applied: `aweb-aapj.9` assigned to Peter for AC Phase B 2/2 file-by-file rewrite map; `aweb-aapj.10` assigned to Dave for final `.5` grep-gate dry-run prep.
- Dave’s `.10` dry-run surfaced two additional aweb blockers before final `.5`: `aweb-aapj.11` is closed at aweb `5f4dc04` (public CLI/SOT docs cleanup); `aweb-aapj.12` is closed at aweb `bdc39e4` (AWID team-certificate API/storage/cert JSON canonical `identity_scope`).
- `aweb-aapj.13` is closed at aweb `bf8b4e4`: AWCO/BYOIDT team-certified signed request mode with verifier evidence. Athena reran diff-check, focused team-auth tests, and Go cmd/aw+awid tests.
- **aweb-aapi — AC embedded aweb migration snapshot drift**: closed at AC `82ec0b8d` (new mirrored migration `006_participant_current_did_key.sql` + manifest tests).
- **Stale replay control**: channel backlog appears drained (`aw mail inbox` and `aw chat pending` clean). Continue checking current task comments/message IDs before acting.

## Non-feature work in flight
- Athena authored `aweb-aapj` breakdown/briefs and seeded initial grep inventories in `/tmp/aweb-legacy-hits.txt` and `/tmp/ac-legacy-hits.txt` (not authoritative yet; final gate is `aweb-aapj.5`).

## Release-ready state (handoff to Hestia)
- Hestia has the no-publish validation request for aweb `d300b33` + AC `0caaefc4` (conversation `96317ca9-a823-40ad-8216-29670533d673`, message `75231d6a-bc88-4441-922f-50649c30e4bd`).
- Current heads: aweb main `d300b33`; AC main `0caaefc4` (includes `.3` `b0e82553`, `.4` merge `f52f5481`, final cleanup `d80fe410`, and Grace-blocker patch `0caaefc4`).
- Do not release yet: Juan asked for tests only; hard hold remains on tag/deploy/publish/version bump/prod migration.
- Known release caveats: npm `@awebai/aw` remains `1.24.3`; do not claim npm/CLI `1.24.4`. AWID health still needs observed `0.5.7`.

## Risks
- **Gate risk**: Hestia may find failures in full validation; stop on red and fix before any release discussion.
- **Two-world dependency risk**: AC release validation must use sibling-source aweb/awid, not PyPI-only `aweb==1.24.4`; no Hestia tag/publish just to unblock local tests under Juan hold.
- **Residual grep risk**: regenerated strict reports still contain compatibility/audit/history/storage hits; AC blocker classes are closed, but final Hestia gate may still surface release issues.
- **AWID hidden/limited row-disposition risk**: deployment must not silently widen existing hidden/limited address rows. aweb `d300b33` encodes and tests fail-closed disposition; any live/prod action still needs explicit release clearance.
- **Backcompat risk**: current `aw` users may use stale args/files; edge adapters should normalize where practical, but old names must not remain canonical help/API/output.

## Next checks
- Wait for Hestia's no-publish validation results for aweb `d300b33` + AC `0caaefc4`.
- If Hestia reports red, fix the failure shape before any release/deploy discussion.
- Keep npm/CLI `1.24.4` caveat and Juan tag/deploy/publish hold explicit.
