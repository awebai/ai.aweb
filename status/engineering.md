# Engineering Status
Last updated: 2026-05-21 13:51 GMT

## Current focus
- `aweb-aapj.3` landed on AC main at `b0e82553`; `aweb-aapj.4` merged after it at AC main `f52f5481`. No tag/deploy/release.
- `aweb-aapj.5` Grace-blocker patch landed on AC main at `0caaefc4`: stale frontend comments removed, active support/operator docs rewritten to `identity_scope=global|local`, and unused `identity_types.py` deleted.
- aweb main remains `bf8b4e4`. Regenerated grep reports for Grace: `/tmp/aapj5-gracefix-20260521134728/{raw.txt,strict.txt}`; narrow re-review packet sent in conversation `7ba3858c-dd3c-4b4d-9895-0e0e2d7903dd` (message `0ba3342f-9110-4cd8-bb16-0660080ce61f`).
- Hestia's prior no-deploy release-ready gate failure at AC `40e73eb4` was fixed by `aweb-aapi` at AC `82ec0b8d`; do not ask Hestia to rerun release-ready until `.5` is clean and AWID row disposition is resolved.

## Dev team work in flight
- **aweb-aapj.1 — aweb/awid old reachability/lifetime authority removal**: closed at aweb `8337af1` (Peter `e48b46c` rebased over Grace `bfe822d` plus Athena wording polish). Removes AWID address reachability/visibility authority, drops aweb `messaging_policy`, migrates aweb agents storage from lifetime to `identity_scope`, and leaves explicit boundary adapters only.
- **aweb-aapj.2 — aw CLI/docs global/local language**: closed at aweb `bfe822d`. CLI/help/docs use global/local; old flags hidden as compatibility aliases; developer-facing test wording cleaned.
- **aweb-aapj.3 — AC backend/schema/API cleanup**: closed and landed on AC main at `b0e82553`. Athena review evidence: diff-check clean; focused sibling-source backend validation green (`118 passed`); Mia full-suite report was `1410 passed / 7 deselected`; direct run of ignored `auth_bridge_oss_cases.py` still fails but the representative failure reproduces on `origin/main`, so it is not a `.3` blocker.
- **aweb-aapj.4 — AC frontend/docs cleanup**: closed earlier, now merged to AC main at `f52f5481`. Post-merge validation: diff-check clean, `frontend/scripts/check-aapj-vocabulary.sh` OK, frontend vitest green (`38 files / 194 tests passed`; existing jsdom `window.scrollTo` stderr only).
- **aweb-aapj.5 — cross-repo grep gate/release handoff**: Grace found three final AC blockers on `d80fe410`; Athena patched and landed AC `0caaefc4`, then sent Grace the narrow re-review packet. Validation: diff-check clean; frontend aapj vocab gate OK; hidden-import grep for deleted `identity_types.py` helpers clean; backend py_compile touched/related files green; frontend vitest 38/194 green; frontend build green. Reports: `/tmp/aapj5-gracefix-20260521134728/{raw.txt,strict.txt}`.
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
- Release is held pending Grace's narrow `.5` re-review approval and AWID hidden/limited row disposition.
- Current heads: aweb main `bf8b4e4`; AC main `0caaefc4` (includes `.3` `b0e82553`, `.4` merge `f52f5481`, final cleanup `d80fe410`, and Grace-blocker patch `0caaefc4`).
- Do not release yet: Grace narrow re-review is pending and AWID hidden/limited row disposition is still unresolved.
- Known release caveats: npm `@awebai/aw` remains `1.24.3`; do not claim npm/CLI `1.24.4`. AWID health still needs observed `0.5.7`. Juan hard-hold remains: no deploy/tag/publish until explicit clearance.
- Hestia was told no more release-ready runs until Athena says `aweb-aapj` cleanup is landed and ready for a no-deploy gate.

## Risks
- **Review risk**: Grace's three concrete `.5` blockers are patched at AC `0caaefc4`, but approval is still pending her narrow re-review.
- **Two-world dependency risk**: AC release validation must use sibling-source aweb/awid, not PyPI-only `aweb==1.24.4`; no Hestia tag/publish just to unblock local tests under Juan hold.
- **Residual grep risk**: regenerated strict reports still contain compatibility/audit/history/storage hits; Grace is reviewing whether the three blocker classes are fully resolved before Hestia is asked for gates.
- **AWID hidden/limited row-disposition risk**: aapj.1 drops reachability/visible columns. Before release, verify hidden/limited production row disposition or get explicit Juan/operator decision; do not silently widen privacy.
- **Backcompat risk**: current `aw` users may use stale args/files; edge adapters should normalize where practical, but old names must not remain canonical help/API/output.

## Next checks
- Wait for Grace's narrow re-review of aweb `bf8b4e4` + AC `0caaefc4`; fix any blockers she finds.
- After Grace review is clean, resolve AWID hidden/limited row disposition explicitly; only then ask Hestia for no-deploy release-ready.
- Keep npm/CLI `1.24.4` caveat and Juan deploy hold explicit.
