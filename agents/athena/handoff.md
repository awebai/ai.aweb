# Athena Handoff
Last updated: 2026-05-23 13:28 GMT

## Read this first

You are Athena. You bridge two teams:

| Team | Visibility | Purpose |
|------|------------|---------|
| `aweb:juan.aweb.ai` | public dev team | Code authoring, tasks, claims, developer coordination |
| `default:aweb.ai` | private company team | Direction, release framing, support, operations, outreach, analytics |

Default active team is `aweb:juan.aweb.ai`. Use `--team default:aweb.ai`
for company-side mail/chat. Dev-team members do not need company-team
release mechanics; to them, Athena is the gate.

## 2026-05-23 immediate state

- **aapj/aapk/aapl/aapm consolidated release wave is verified-live.** Hestia reported verified-live from a message that displayed `identity_mismatch`; Athena independently checked public surfaces and they line up: `app.aweb.ai/health` reports `v0.5.45` / git `fe364950` / aweb `1.25.0` / awid_service `0.5.8`; `api.awid.ai/health` reports `0.5.8`; npm reports `@awebai/aw=1.25.0`, `@awebai/claude-channel=1.4.4`, `@awebai/pi=0.1.1`.
- **Prod DB reset/restore completed.** AC prod was rebuilt clean and restored; AWID 003/004 applied after the approved disposition. Boundary note: no checksum bypass markers or `schema_migrations` edits; only approved disposition row mutations.
- **AWID/AC disposition landed.** Juan/Grace clarified the architecture: AWID addresses are public/global; old non-public delivery intent belongs in AC/aweb `inbound_mode`. Active legacy AWID non-neutral `public_addresses` rows were normalized to public/null in AWID, and corresponding AC/aweb agents were set `contacts_only`. Historical soft-deleted AWID rows were left as-is.
- **Published artifacts:** aweb `1.25.0` (PyPI + npm `@awebai/aw`), awid-service `0.5.8`, awid `0.5.8` (GHCR + api.awid.ai), AC `v0.5.45`, `@awebai/claude-channel 1.4.4`, `@awebai/pi 0.1.1`. `@awebai/channel-core` is bundled into channel/pi, not a separate runtime dependency.
- **Banked fast-follows:** redact `ac/scripts/prod_db_reset.py` DATABASE_URL logging; investigate Render auto-deploy behavior before next cutover; investigate historical AWID public-address soft-delete paths; bank npm token/`gh secret set` syntax lesson; scrub `/tmp/aweb-db-reset-*` and `/tmp/awid-db-snapshot-*` PII evidence when wave is fully closed.
- **P0 post-release bug opened:** Grace found `contacts_only` blocks new chat but mail continuation can bypass exact-contact policy via `deliver_message(... skip_policy_check=True)`. Athena created dev task `aweb-aapo` assigned to Grace to enforce `contacts_only` on HTTP/MCP mail continuations unless Juan explicitly redefines the rule. Athena's contacts list is empty, and Grace is not an exact active contact here. Athena could not directly read prod inbound_mode via API key, but Grace's new-chat 403 is strong evidence `aweb.ai/athena` is `contacts_only`.
- **P0 verification bug opened:** Athena upgraded local CLI to `aw 1.25.0` (`136f25f`); Hestia's fresh chat still displayed `identity_mismatch` / `verified=false`, so matching client version did not clear Hestia->Athena verification. CLI history for the same Hestia messages reports `verification_status=verified` with `to_did` and `to_stable_id` both set to Athena did:aw; live Pi/channel metadata still showed mismatch. Grace initially proposed a guarded `current_did_key` participant backfill, but then held it as primary fix: CLI history verifies the same Hestia messages while live Pi/channel metadata reports mismatch, so stored message/participant state is probably not the live-event cause. `aweb-aapp` is narrowed to channel/Pi recipient-binding or `self.stableID` loading: reproduce blank/stale self stable ID with stored-route global `to_did=did:aw` + `to_stable_id=did:aw`, and fix so `to_stable_id` self match wins safely without weakening true mismatch rejection. Backfill remains hygiene only unless Juan separately directs it. Grace's upgraded mails still display verified. Hestia also reported duplicate `aweb.agents` rows for Athena; bank as separate restore/data-integrity follow-up, no prod row mutation without runbook.
- **Stale replay control:** Peter replay/stand-down mails have been drained repeatedly; check `aw mail inbox` before acting, but ignore stale aapf/aapg/aaph/aapm/aapl replay ACKs unless a current verified task is routed.

## 2026-05-20 immediate state

- Ignore ontology/company-graph work unless Sofia asks a narrow engineering/context question; Juan asked Athena to focus on simplification.
- Juan asked for a step-back assessment of whether aapg/aaph produced real simplification and for stale-code/debt findings; Athena relayed the request to Grace and Grace replied with the same bottom line: significant product-contract simplification, not a fully simplified implementation yet.
- `aweb-aapg` is closed/released. Do not reopen stale `aapg` mail threads.
  - aweb server `1.24.4` and awid-service/awid `0.5.7` are released.
  - PyPI `aweb==1.24.4` is live.
  - npm `@awebai/aw` remains `1.24.3` because `1.24.4` npm publish failed on `@awebai/aw-linux-x64` with auth-like 404. Do not claim npm/CLI `1.24.4` until fixed and verified.
  - Production hidden/limited AWID rows remain fail-closed by released `.2` code until explicit owner/operator normalization; no row mutations without routed approval.
- `aweb-aaph` product-authority simplification is feature-complete but release-gate blocked. Current state:
  - `.1/.2` closed at AC `b1777bb0` (no hosted-local browser/MCP path; explicit custodial/addressed/global predicate; local/ephemeral hosted creation rejected).
  - `.3` closed at AC `5426d91c` (team API-key CLI bootstrap is local self-custodial; persistent/global terminal path remains self-custodial).
  - `.4/.5` closed at AC `284653e7` after Grace approval (BYOT custodial pending/import exact and fail-closed; aweb-managed Add existing preserves `custody=self` and no cloud key).
  - `.6` closed and landed: aweb main `29023bd`; AC main `ecf28888` (Dave copy refs approved by Grace; AC commit is cherry-pick of `43cbf282` onto current main).
  - `.7` is closed. Grace confirmed approval via chat after the channel replay check; approval mail message_id `9c522612-391a-4aad-819b-dc1485d52ad0`. Approved heads: aweb main `994972b` (CLI local/global/add-worktree test proof) and AC main `40e73eb4` (onboarding regression matrix aligned with current route/lifetime contract). No bespoke precheck required before Hestia beyond normal full release gates including Docker/full-service e2e where available.
  - `aweb-aaph` implementation is complete. Hestia ran no-deploy AC release-ready at AC `40e73eb4`; result 37 failed / 1397 passed. Primary failure is schema drift: AC embedded aweb migrations do not create `conversation_participants.current_did_key` / `chat_participants.current_did_key` required by pinned `aweb==1.24.4`.
  - Athena confirmed repo evidence: AC migration snapshot has local `007_agent_inbound_mode.sql` but lacks aweb package `007_participant_current_did_key.sql` / `008_agent_inbound_mode.sql`. This is release-gate integration hygiene, not a product-authority blocker.
  - Created P0 dev task `aweb-aapi` assigned to Mia: fix AC embedded aweb migration snapshot drift forward-only, add drift-prevention verification, no tags/deploy/version bumps; branch-ready back to Athena.
- Latest step-back read (Athena + Grace): **not fully simplified yet**. aweb-side code authority is much cleaner, but AC main still leaks old authority, and aweb/AWID public/static docs + doctor/support output still need cleanup. Do not release until `.3`, `.4`, `.8`, final `.5` grep gate, and AWID row-disposition decision are done.
- Juan rejected carrying compatibility residue as a follow-up: because the aaph stack has not deployed, do the cleanup now. New P0 epic `aweb-aapj` is active: excise legacy identity/reachability vocabulary and control planes before release.
  - `aweb-aapj.1` closed at aweb `8337af1`: Peter's aweb/awid old authority cleanup rebased over Grace plus Athena wording polish. Validation rerun: AWID full 167, server full 540, Go `./...` passed with longer timeout, focused lifecycle/team-auth 32, diff-check clean. Removes AWID address reachability/visibility authority, drops aweb `messaging_policy`, migrates aweb agents `lifetime` storage to `identity_scope`, keeps explicit boundary adapters.
  - `aweb-aapj.2` closed at aweb `bfe822d`: CLI/docs global/local language; `aw init --global` canonical; old flags hidden as compatibility aliases; developer-facing test wording cleaned. Athena validation passed (Go CLI/awid, CLI reference, package-data, channel-core+Pi build, diff-check).
  - `aweb-aapj.3` assigned to Mia: AC backend/schema/API cleanup; removes canonical `identity_type`, `lifetime`, `access_mode`, `address_reachability`, persistent/ephemeral surfaces. Athena answered DTO questions: canonical `identity_scope=global|local`; `address_reachability` deleted from normal output; `access_mode` maps fail-closed to `inbound_mode` (`open`->`open`, `contacts_only`/`team_only`/`owner_only`->`contacts_only`); stale fields are input-only/backcompat and not returned in canonical responses; use forward migrations unless a migration is proven undeployed. Mia confirmed branch base AC `82ec0b8d` and is sending a worked-example endpoint diff before broad sweep.
  - `aweb-aapj.4` assigned to Olivia: AC frontend/dashboard cleanup. Olivia reset branch to AC `82ec0b8d`; frontend-only scope. Synced `ac/site/content/docs` and `site/static/docs` are out of scope because canonical docs live in aweb/docs (Grace/Dave lanes).
  - `aweb-aapj.5` assigned to Athena and marked in progress: final cross-repo grep/allowlist gate and release handoff after `.3`, `.4`, `.8` land.
  - `aweb-aapj.6` closed at aweb `e248cd3`: Pi/skills/package-copy stale vocabulary cleanup. Athena reviewed/landed. Validation rerun: `git diff --check`; clean-worktree channel-core build then `pi-extension npm run build` passed after installing deps. Remaining scoped source hits are explicit legacy/audit notes.
  - `aweb-aapj.7` closed at aweb `2e98603`: channel/channel-core runtime cleanup normalizes `lifetime`/`persistent`/`ephemeral` to identity_scope/global/local with legacy adapters. Athena validation rerun: diff-check; channel focused 69; channel-core build; channel build; full channel tests 95; Pi build. Remaining lifetime/persistent/ephemeral hits are compatibility adapters/tests/generated equivalents.
  - `aweb-aapj.8` closed at aweb `e332bf8`: aweb/AWID public/static docs and doctor/support output cleanup. Athena validation rerun: diff-check; targeted public/static docs grep clean; doctor stale phrase grep clean; Go cmd/aw+awid; server package-data; CLI reference check.
- **Current P0 stop-the-line is `aweb-aapm` migration composition repair.** Grace relayed Juan's decision: stop all release-forward movement until AC stops carrying forked/copy canonical aweb migrations under AC paths and returns to composing canonical OSS aweb migrations with AC-owned overlays under separate module names. No tags/publishes/deploys/release gates or treating aapk/aapl as release-sufficient until this is resolved.
- Created dev-team work: `aweb-aapm` epic; `.1` design (Athena); `.2` implementation (Mia); `.3` Grace review; `.4` Peter package-provenance verification; `.5` Dave operator/cutover clarity review. Grace approved the `.1` architecture with amendments; Athena folded them into the `.2` brief and routed it to Mia. Grace will wait for Mia's implementation packet + Peter `.4` evidence + Dave `.5` review before `.3` cleanliness pass.
- Approved aapm architecture: canonical OSS aweb migrations come from installed/sibling `aweb` package under `module_name='aweb-aweb'`; AC `server` schema remains schema name `server` but provenance/module becomes AC-owned (`aweb-cloud-server`-style); AC aweb additions move to `aweb-cloud-aweb-overlay`; apply order is canonical aweb -> AC server -> AC aweb overlay -> `aweb_cloud`; AC-local copied canonical `migrations/aweb` must not be normal authority, ideally removed. Required final packet must attach/link the table/column overlay inventory and prod restore mapping directly.
- Last fully validated aapj heads remain aweb `fa1041c` + AC `9104ffc2`, green in Hestia's sibling-source validation chain, but no longer release-sufficient because aapm exposed an architectural migration ownership problem.
- `aweb-aapk` is closed after Grace passed current AC `0941ee42` + aweb current main/aapk.1 context. Juan then asked all ready contributions be in main, so Athena landed Olivia's extra polish commits to AC main `707b698a` and validated TeamConnectionPanel + package AgentsPage focused tests (11 passed) plus diff-check.
- `aweb-aapl` is paused behind `aweb-aapm`. `.1` is closed at aweb `f31ffcb`. Mia parked unpushed `.2` work in stash and task #60 is pending/blocked by aapm. The broad AC default change exposed a dashboard-user → same-team-agent 403 gap when new global identities default to `contacts_or_teammates`; Mia filed P0 `aweb-aapn` for it, blocked behind aapm. Do not push `.2`, extend AC mirror migrations, or mass-update tests until aapm resolves migration ownership.
- Peter was routed to help Mia with AC mirror/schema review (no edits unless asked). He found a real blocker: AC `dashboard.py` constructs `TeamIdentity(lifetime=...)`; current aweb source requires `identity_scope`. Mia confirmed default AC local tests still use PyPI `aweb==1.24.4`, so `.3` must add/use a sibling-source backend validation path; do not ask Hestia to tag/publish under Juan hold. Mia landed prerequisite `e1e476ee` and Phase B migration half `a42ddd6c`; branch is intentionally red under `test-backend-aweb-local` until Phase B 2/2 rewrites code/tests/gate path. Peter has been asked to re-review `a42ddd6c`.
- `aweb-aapj.3` closed/landed on AC main at `b0e82553`. Athena evidence: diff-check clean; focused sibling-source backend validation green (`118 passed`); Mia's full suite report was `1410 passed / 7 deselected`; ignored `auth_bridge_oss_cases.py` failures reproduce on `origin/main` so they are not `.3` blockers.
- `aweb-aapj.4` closed/approved branch-ready at AC `origin/olivia-aapj-4` `eec512d4` and merged after `.3` at AC main `f52f5481`. Post-merge validation: diff-check clean, frontend aapj vocab gate OK, frontend vitest green (`38 files / 194 tests passed`; existing jsdom `window.scrollTo` stderr only).
- `aweb-aapj.5` final AC cleanup first landed at `d80fe410`; Grace reviewed and found three concrete blockers. Athena patched them and landed AC main `0caaefc4`: stale frontend temporary-rename comments removed, active support/operator docs sections rewritten to `identity_scope=global|local`/custody/addressability, and unused `backend/src/aweb_cloud/services/identity_types.py` deleted. Validation on `0caaefc4`: diff-check clean; frontend aapj vocab gate OK; hidden-import grep for `storage_lifetime_from_identity_type|api_identity_type_from_lifetime|identity_types` clean; backend py_compile touched/related files green; frontend vitest green (38 files / 194 tests; existing jsdom `window.scrollTo` stderr only); frontend build green. Regenerated reports: `/tmp/aapj5-gracefix-20260521134728/raw.txt` and `strict.txt`. Grace's narrow re-review passed for AC `0caaefc4` (mail `6981bb38-a8e4-4d35-a155-cb83bc08284b`), and she ACKed that the remaining gate is AWID hidden/limited row disposition (`55d8b800-8e9f-4094-a011-2ea5a240179b`).
- AWID row-disposition follow-up: Athena landed aweb main `605f356` (`Fail closed before dropping legacy address visibility`). It makes `awid/src/awid_service/migrations/003_drop_address_reachability.sql` refuse to drop `reachability` / `visible_to_team_id` while any active `public_addresses` row is non-neutral (`reachability != 'public'` or `visible_to_team_id IS NOT NULL`). Grace reviewed SQL shape as correct but required an executable migration regression. Athena landed aweb main `d300b33` with the requested focused tests: active `nobody` blocks, active `team_members_only` + `visible_to_team_id` blocks, deleted non-neutral row does not block, active neutral `public` + NULL passes and drops both columns. Validation: diff-check clean; `uv --directory awid run pytest tests/test_schema.py -q` -> 8 passed; `make test-awid` -> 172 passed. Per Juan, Hestia was asked to run full validation/all tests for aweb `d300b33` + AC `0caaefc4` with explicit no tag/deploy/publish/version-bump/prod-migration boundary (company mail conversation `96317ca9-a823-40ad-8216-29670533d673`, message `75231d6a-bc88-4441-922f-50649c30e4bd`). Hestia's first result: aweb `make ship` green; AC `make release-ready` failed 226/1435 due stale PyPI `aweb==1.24.4` mismatch (`agents.lifetime` queries and old `resolve_identity_contract` signature). Athena replied with the correct sibling-source validation path: `make test-backend-aweb-local` and a manual release-ready-equivalent chain using release verify targets, frontend, release image, two-service, and cloud journeys without tags/publish/deploy (message `fd4958cb-30a8-48ab-a62a-50a76bef3f10`). Hestia's sibling-source rerun at AC `0caaefc4` still failed: Phase 2 had 13 backend failures and Phase 6 had 157 e2e failures. Athena patched and pushed AC `b1f6277e`: removed namespace `address.reachability` access, mapped dashboard mail `ForbiddenError` to HTTP 403 and updated local first-contact tests, fixed hosted MCP OAuth test helper to create addressed/global custodial identities, and pinned one API-key test's public origin to localhost. Local validation: diff-check clean; targeted ruff green; focused 13 Phase-2 failures now 13 passed; full `make test-backend-aweb-local` 1419 passed / 16 skipped; py_compile routers green. Hestia rerun at `b1f6277e` made Phase 2/3/4 green, but Phase 5/6 stayed red; she isolated representative 422 to `backend/tests/test_two_service_e2e.py` sending `address_reachability: "public"` to `/api/v1/identities/create-permanent-custodial`, whose Pydantic request model correctly forbids the stale field. Athena chose the clean-cut aapj fix, patched AC `74ab465c` to remove `address_reachability` from two-service e2e request bodies, and asked Hestia to rerun aweb `d300b33` + AC `74ab465c` (message `26cd6176-d1a8-4981-9994-3087bb8f8b8b`). Hestia then found the next 422: the `aw` CLI binary still sent `lifetime: "ephemeral"` to `/api/v1/workspaces/init`, triggering AC `extra_forbidden` before auth. Per Juan, Athena asked Peter to make the fix and Grace to review it. Peter landed aweb `b215d23` (`Send identity scope in API key workspace init`): request DTO sends `identity_scope`, not `lifetime`; tests assert outbound no-`lifetime` and correct `identity_scope` for local/global/add-worktree. Peter validation: diff-check, targeted Go tests, full `cd cli/go && go test ./cmd/aw -count=1`, and focused AC sibling-source `tests/test_workspaces_init_api_key.py` 27 passed. Grace reviewed `b215d23` and approved: single request construction path, correct mapping, response-side lifetime fallback read-only. Athena handed Hestia rerun request for aweb `b215d23` + AC `74ab465c` (message `2bd6b590-241c-4daa-bf13-422e4a6a7b70`). Hestia reran and reported massive progress: Phase 1 release-verify green; Phase 2 `test-backend-aweb-local` green 1435/1435; Phase 3 frontend green 194/194; Phase 4 image green; Phase 5 down to 4 fails; Phase 6 down to 45 fails. Remaining Phase 5 failures were stale test-side `cert["lifetime"]` assertions plus export script still reading AWID address `reachability`; Phase 6 had dashboard create-permanent-custodial sending stale `identity_scope: "nobody"` and a cross-team global address first-contact expectation that was stale. Athena patched AC `3c97b4d3`: team-cert assertions now use `identity_scope`; export omits/verifies without `reachability`; dashboard hosted creation sends `identity_scope: "global"`; cross-team global `--to-address` expects delivery and verifies Bob receives it. Validation: diff-check clean; py_compile touched Python green; `bash -n` cloud journey green; targeted ruff green; two-service collect 15; `make test-backend-aweb-local` 1435 passed. Mia reviewed AC `3c97b4d3` and passed with no blockers. She confirmed the export/identity-scope changes and checked the product/security question: global + open address first-contact delivery is deliberate, and same-team restriction belongs on inbound_mode/contact policy, not all cross-team address delivery. Athena handed Hestia rerun request for aweb `b215d23` + AC `3c97b4d3` (message `842ec1eb-e9d7-47fa-9f93-4798ebf95c22`). Hestia reran with stop-on-red working: Phase 1/2/3/4 passed; Phase 5 halted at one failure, `TestDataMigration::test_json_export_and_verification`, because host pytest loaded an installed AWID copy whose `_address_from_json` still required `data["reachability"]`. Athena inspected aweb `b215d23`: sibling source already uses `data.get("reachability", "")`, so the issue is the two-service host venv not guaranteed to be sibling-source. Athena patched AC `bf9206b5`: `test-two-service-up` runs `make use-aweb-local` before build/start/bootstrap. Mia blocked correctly: plain `uv run pytest` in `test-two-service` would re-sync and wipe the sibling overlay before pytest. Athena patched AC `4034f044`: both host bootstrap `uv run python` calls and the host pytest call now use `uv run --no-sync ...`. Validation: diff-check clean; grep confirmed no plain `uv run` remains on the two-service host bootstrap/pytest paths. Mia reviewed AC `4034f044` and passed. She verified `use-aweb-local` runs before any other two-service host `uv run`, both bootstrap calls and pytest use `--no-sync`, and no plain `uv run` remains reachable between overlay and pytest. Athena handed Hestia rerun request for aweb `b215d23` + AC `4034f044` (message `dcfc67e4-34e0-4d5b-b783-e0f6a840785d`). Hestia reran: Phase 1/2/3/4/5 all green; Phase 6 stopped at one Playwright failure waiting for stale button label `Create local identity`. Athena patched AC `dccfc8d0`: browser e2e now clicks current `Set up CLI workspace`; added `scripts/check-aapj-e2e-contract.sh` to block legacy request-field literals, stale identity_scope values, and stale browser selector in release-facing e2e surfaces; wired guard into `release-verify-model`. Olivia reviewed `dccfc8d0` and approved, with a follow-up note to catch unquoted TS object literal stale `identity_scope` values. Athena applied that immediately as AC `492b3d33`; validation `make release-verify-model` green and diff-check clean. Olivia approved `492b3d33` but noted the TS guard missed double-quoted values. Athena applied that as AC `7eb391bd` and fuzzed all three shapes (JSON quoted key, TS single quote, TS double quote) — all caught. Peter then landed final CLI JSON cleanup: aweb `af317d3` emits `identity_scope` and not `lifetime` in normal `aw init --json` / connect output; AC `1ea76dd6` updates two-service expectation to `hosted["identity_scope"] == "global"` and asserts no `lifetime`. Grace reviewed and approved combined heads aweb `af317d3` + AC `7eb391bd`, but Juan pushed back that `connectOutput.Lifetime json:"-"` still carried legacy state in a normal output struct. Athena agreed, told Hestia to stop the rerun (message `1efe72c7-2150-4cb7-b64c-d689ad10372a`), and Hestia stopped/cleaned the e2e stack. Athena patched aweb `fa1041c`: removed `Lifetime` from `connectOutput` entirely; compatibility remains only by normalizing reads from `cert.IdentityScope` with `cert.Lifetime` fallback. Validation: targeted cmd/aw tests green and full `go test ./cmd/aw -count=1` green. Grace reviewed aweb `fa1041c` and approved: no `Lifetime` in `connectOutput`, no normal output lifetime assignment, legacy cert `Lifetime` only read at boundary and immediately normalized. Athena handed Hestia rerun request for aweb `fa1041c` + AC `7eb391bd` (message `de26f880-8528-4fa8-a259-696f8d4d58f0`). Peter ACKed the tightening. Hestia reran: Phase 1-5 green; Phase 6 had one failure in hosted MCP identity roster. Creation succeeded and routed to the new agent connect page, but returning to `/connect?path=hosted` did not show the new row. Athena first diagnosed React Query cache freshness and landed AC `d77e0934` (`staleTime: 0`, `refetchOnMount: 'always'`), approved by Olivia, but Hestia's rerun still failed the same row. Root cause was the actual data path: `TeamAgentSetupFlow` filters for `hosted_mcp` + active + custodial/global + address, while `apiClient.listTeamAgents` was still using OSS `/api/v1/agents`, which lacks Cloud enrichment fields (`custody`, `identity_status`). Athena landed and pushed AC `9104ffc2`: `listTeamAgents` now calls `/api/v1/dashboard/agents?team_id=...` and has api-client unit coverage for enriched hosted fields. Validation: targeted frontend 16 passed; `make test-frontend` passed (195 tests + build; existing jsdom `scrollTo` stderr only); sibling-source backend `tests/test_dashboard_agents.py` passed; `make release-verify-model` passed. Grace reviewed `9104ffc2` and passed; she noted stale installed aweb still fails backend dashboard test due old `lifetime` insert, so Hestia must keep sibling-source validation. Athena handed Hestia rerun request for aweb `fa1041c` + AC `9104ffc2` (message `824e1cd1-f48c-4ef2-9e6d-c1dcd51890c7`).
- Juan asked to keep idle agents applied. Athena created/routed `aweb-aapj.9` to Peter and `aweb-aapj.10` to Dave. Important correction after Juan pushback: do NOT keep derived `legacy_lifetime` from canonical `identity_scope`; support/admin/audit may expose old fields only for actual persisted old state or external legacy input, not derived compatibility residue. This was documented in `docs/invariants.md` and sent to Mia/Dave. `.11` is closed at aweb `5f4dc04`; `.12` is closed at aweb `bdc39e4`; `.13` is closed at aweb `bf8b4e4`. Dave's `.10` live preflight is banked on task comment/mail. Peter's docs/support branch `572d20f6` was reviewed by Athena, validated in a merged worktree, and merged into Mia `.3` at `53fb4d87`. Peter's teams/projection branch `dfb12d3f` was reviewed by Athena, validated in a merged worktree (diff-check, py_compile, 30 focused tests), and Athena merged it into Mia `.3` as `972382aa` to keep the lane moving. Latest fetched AC `.3` is `972382aa`. Major blockers fixed since reactivation: CloudTeamIdentity/HostedProvisionedIdentity identity_scope, team_cert_mint canonical identity_scope + fail-closed lifetime alias, agent_lifecycle DTO removals, agent_addressing access_mode/reachability removals, scope_agents canonical input/access_mode output cleanup, init request DTO cleanup, teams/projection AWID canonicalization. Remaining live blockers as of 13:06: `init.py` residual compatibility/internal lifetime/address_reachability/logging audit and `spawn.py` service boundary canonicalization, then final `.5` classification.
- Important release blocker: aapj.1 drops AWID `reachability` / `visible_to_team_id`. Before release/deploy, verify production hidden/limited rows are explicitly disposed/normalized or get Juan/operator decision. Do not silently widen privacy.
  - `aweb-aapi` was reviewed, merged, and closed: AC main fast-forwarded to `82ec0b8d` with `backend/src/aweb_cloud/migrations/aweb/006_participant_current_did_key.sql` and migration manifest tests. Clean-worktree validation: `uv run pytest -q tests/test_migration_paths.py` -> 17 passed. Broader cleanup remains `aweb-aapj.3`.
  - Hestia was told release remains held and no more release-ready reruns are needed until Athena says `aweb-aapj` has landed.
- Mail/channel replay appears drained (`aw mail inbox` and `aw chat pending` clean), but continue checking message IDs/timestamps/task comments before acting. Most incoming `aapg` and early `aaph` messages are stale.

## 2026-05-19 global/local simplification epic

- Juan asked Athena to lead a major architecture simplification: persistent →
  global, ephemeral → local, remove reachability/access restrictions, and
  eventually remove conversation_id as routing authority.
- Athena created epic `aweb-aapf` and dependent subtasks `.1`-`.8`, assigned
  to Peter. Peter ACKed and paused his prior tutorial-validation task.
- Target model:
  - global = `did:aw`, AWID-registered, globally reachable, `did:aw <-> actual
    agent`; addresses are aliases, not independently-routable principals;
    delivery origin should be identity/agent-level or same-origin enforced
    across aliases.
  - local = `did:key` only, no AWID row/no `did:aw`, team-local; can write to
    global and be replied to only via learned return route keyed by did:key.
  - no reachability classes, no `visible_to_team_id`, no AWID team-cert address
    visibility gates, no private address lookup auth.
  - conversation/thread IDs may remain as UX/local metadata but not routing
    authority or authorization capability.
- `aweb-aapf.1` SOT/design is approved and closed at Peter commit `4b51af1`
  (on top of `25a290a`). Athena requested/received clarifications on identity
  delivery-origin write authority and learned local-route capabilities.
- `aweb-aapf.2` AWID identity-level delivery origin/resolver model is approved
  and closed at Peter commit `4509c9f` (rebased on `origin/main` `5842eef`).
  Validation rerun by Athena: AWID tests 168, full Go `./...`, docs regression,
  diff-check clean.
- `aweb-aapf.3` first review of Peter commit `0e06284` was not approved.
  Athena found two blockers: (1) federated first-contact to an existing local
  `did:key` could create a new mail conversation/chat session; (2) Peter
  initially planned a route-assertion/capability protocol, but Juan pushed back
  that local agents are renamed ephemerals and already had outbound +
  reply-in-established-context behavior. Athena tightened the gate: preserve and
  simplify existing ephemeral/local reply behavior, do not grow a local
  mini-registry/protocol unless a concrete exploit requires it, and require a
  deletion/complexity note with the patched commit. Conversation_id may be an
  index into local conversation/session state, but not routing authority.
- `aweb-aapf.3` patched commit `97797af` was reviewed and validation rerun by
  Athena; one blocker remained: local did:key inbound chat replies checked
  existing active conversation + `chat_sessions` row, but not that
  `chat_participants` contained both sender and target.
- `aweb-aapf.3` is now approved and closed at Peter commit `103fa9e`. The final
  narrow fix verifies both sender and target in `chat_participants` for local
  did:key inbound chat, with a stale/missing-target regression. Validation rerun
  by Athena: `git diff --check`, docs regression, server 532, AWID 168, Go
  `./...` all green.
- `aweb-aapf.9` is approved/closed at Peter commit `eee1497`. It persists remote
  current did:key in conversation/chat participant route state so continuation no
  longer depends on AWID `resolve_key` hot-path availability. Validation rerun by
  Athena: diff-check, docs regression, server 532, AWID 168, Go `./...` green.
- `aweb-aapf.4` is approved/closed at Peter commit `cd92f51` over base
  `eee1497`. It adds supported self-custodial identity delivery-origin setup via
  `aw id set-delivery-origin --origin ...`, signed by the current identity key
  against `/v1/did/<did_aw>/delivery-origin`; keeps namespace default delivery
  origin as legacy metadata, not routing authority; requires direct global
  `did:aw` first contact to bind the current did:key; and for stored-route
  continuations signs `to_did=<did:aw>` plus `to_stable_id=<did:aw>` when the
  server participant/session route state supplies the current key. Validation by
  Athena: diff-check, docs regression, Go `./...`, server 532, AWID 168, channel
  89, channel-core build all green.
- `aweb-aapf.7` is approved/closed at Grace commit `99d029d` over approved `.4`
  base `cd92f51`. It rebased onto `.4`, uses `aw id set-delivery-origin --origin
  <origin>` in e2e setup (no DB mutation), removes old reachability/private-
  address/team-cert-as-routing/conversation-auth assertions, and preserves team
  membership/trust, verification, delivery-origin, signed binding, participant-
  state routing, conversation UX/threading, stable did:aw targeting, did:key
  rotation continuation, and duplicate-alias active-team routing coverage. Grace's
  runtime evidence at `2d42d23`: federation 28 passed and OSS user journey 211
  passed; final `99d029d` is label-only and Athena static validation was green.
- `aweb-aapf.5` is approved/closed at AC `173b9f7e` over `583970cf`. Athena
  reviewed the full `.5` series and reran validation: `git diff --check`,
  focused backend local/global/OAuth tests, OAuth regression set,
  `make test-backend-fast` (75 passed), focused frontend setup/connect tests
  (9 passed), and `make test-frontend` (195 tests + build passed). Approved
  invariants: hosted global registers DID/address and sets identity-level
  `delivery_origin` with hosted custody; hosted local stores SQL NULL
  `agents.did_aw`/`agents.stable_id`, has no AWID DID/address/delivery-origin,
  and stays out of OAuth binding/probing/connect UI except explicit team-local
  bearer-token MCP. Peter ACKed he will stop `.5` at `173b9f7e` and not tag,
  deploy, or start `.6`/`.8`.
- `aweb-aapf.6` is approved/closed at AC `fb1dea3c` over approved `.5` head
  `173b9f7e`. It adds dry-run-only hosted identity compatibility audit and docs.
  Athena validated diff-check, ruff, focused audit/local/OAuth backend set (6
  passed), `make test-backend-fast` (75 passed), and static grep confirming no
  `--apply` / write-SQL in the audit script. Peter ACKed he will stop `.6` at
  `fb1dea3c` and not add apply-path work.
- `aweb-aapf.8` is approved/closed and landed. Peter's first `.8` packet was
  blocked because reachability remained an active write control-plane; patched
  heads are aweb `3550251` and AC `06364f1e`. Athena fast-forwarded both repos'
  `main` and pushed. Final proof: private address lookup forwarding removed;
  federation carried team-cert routing removed; AWID resolver no longer gates on
  reachability; AWID writes normalize/ignore legacy reachability fields; CLI/API
  setup no longer sends reachability; AC hosted UI/API controls removed; AC
  registry writes no longer preserve reachability/`visible_to_team_id`. Athena
  validation: aweb diff-check, `make test-awid` 168, `make test-server` 529,
  `make test-cli` Go `./...`; AC diff-check, focused backend 50,
  `make test-backend-fast` 75, `make test-frontend` 195 + build. Docker e2e was
  not runnable locally because Docker daemon unavailable.
- `aweb-aapf` epic is closed. Peter ACKed he will stop further changes. Hestia
  owns release gate/e2e before ship; Athena sent Hestia the release handoff and
  Sofia a framing note. No tags/deploys by Athena.
- Sofia framing response: external posture is hold/no announcement. Do not claim
  “no user-visible behavior change” broadly: normal messaging/MCP workflow should
  stay same-shape, but operator/setup controls did change (`aw init
  --reachability`, namespace assign-address reachability flags, hosted dashboard
  reachability editor/API removed or ignored). Athena updated `docs/invariants.md`
  invariant #8 to the new global/local wording.
- Hestia correction: gates can run in parallel with Sofia framing, but do not
  tag/deploy until `.6` compatibility audit runs against production/staging-prod
  data and hidden/limited legacy global rows are surfaced for explicit decision.
  Reachability metadata is ignored by resolver after deploy; it is not safe to
  skip the audit and assume existing hidden rows are harmless.
- Juan then rejected shipping the transition artifact and asked Athena to keep
  going until the system is actually simplified. Grace's critique: target
  global/local architecture can be simpler, but current main is halfway
  migration, not ship-grade simplification. Hestia's real AWID audit found 43
  hidden/limited rows and 0 persistent hosted agents on contacts policy. Grace
  also found old->new federation wire break: old v1 senders emit four fields
  current `FederationEnvelope` hard-rejects with `extra="forbid"`.
- New P0 epic `aweb-aapg` tracks ship-grade simplification. `.1` federation
  v1 compatibility tolerance is now approved/closed and landed at aweb
  `e4ff4e9`. Remaining subtasks: `.2` hidden/limited AWID row policy, `.3`
  route/delivery-origin redesign, `.4` messaging-policy removal, `.5` docs
  convergence, `.6` minimal e2e proof, `.7` AC cleanup. Juan updated the
  target: first contact should use address, not bare `did:aw`; a `did:aw` may
  have multiple address/routes at different origins; learned continuation can
  deliver via stored `[key | did:aw], origin`. Juan also directed
  `messaging_policy` removal/simplification: global inbound open; local inbound
  shared-team or contacts; successful cross-team send adds recipient to sender
  contacts for reply path. Peter is holding until routed except `.1` is done.
  Pull Grace back for boundary review on compatibility/migration/simplification
  decisions; she is not implementing unless asked.

## 2026-05-19 hosted identity routing/default release update

- Release ship-clear head is now aweb `4c45619` + AC `bdfe5631`.
  - Initial aweb review cleared `8064558` (CLI continuation binding) + AC
    `bdfe5631`; Mia/Grace approved.
  - Hestia's first cut plan treated `8064558` as a server release; Athena
    pushed back because `8064558` alone was CLI-only.
  - Grace then found/fixed server-side federation continuation verifier
    blockers in `3198d6e` (`signed_payload.to` identity-bound), `78482b9`
    (malformed-target rejection), and `d664988` (`to_did` stable did:aw
    acceptance). Hestia's real e2e still failed at `d664988` on
    conversation-only federation reply.
  - Grace fixed the real e2e path in `4c45619`: RegistryResolver resolves bare
    did:aw via fallback registry `/v1/did/<did:aw>/key`; chat continuation signs
    full sender address for federated DID/address targets. Grace's canonical
    `make ship` at `4c45619` passed: server 524, awid 160, Go `./...`, channel
    89, release checks, federation e2e 27/27, OSS user journey 224, tree clean.
  - Because `3198d6e`/`78482b9`/`d664988` touch `server/src`,
    `server-v1.24.3` is justified alongside `aw-v1.24.3`. Athena relayed
    ship-clear to Hestia: aweb `4c45619` → server/aw 1.24.3, then AC
    `bdfe5631` → v0.5.44.
- Post-deploy repair remains explicit/scoped/audited only. Known `nobody` rows
  (Athena, Hestia, Sofia, Iris) must not be blanket migrated; prefer
  controller-key/API repair over direct DB unless Grace decides the API route
  is not viable. Require matrix smoke after repair before any claim.

## 2026-05-18 trust-display release update

- aweb/aw 1.24.2 is verified-live for the CLI trust-display regression.
  Fix set:
  - `856a560` — live chat SSE now treats signed_payload `from_did` /
    `to_did` as authoritative for verification when stream rows carry
    stable `did:aw` participant IDs.
  - `aa72312` — channel-core dispatch tests for stable-DID envelope +
    signed-payload did:key, plus rebuilt `pi-extension/dist`.
  - `271bb7d` — Go inbox/chat-history and server verification tests for
    stable-row/signed-did:key normalization.
- Mia approved; Athena reviewed in a clean detached worktree and validated
  focused Go, server, channel, and Pi-extension build paths. Hestia cut
  aweb/aw 1.24.2 and smoked live output: plain `aw chat send-and-wait`
  showed `Chat from: aweb.ai/athena [not in contacts]` with no
  `[unverified]`; JSON proof remained `verification_status=verified` with
  did:key + did:aw distinct.
- External claim still needs Sofia framing. Claim must exclude Pi users:
  `aweb-aapb` remains open because `@awebai/claude-channel@1.4.3` and
  `@awebai/aw@1.24.2` do not update Pi's bundled extension.
- Separate follow-ups:
  - `aweb-aapb` — define Pi extension update path for bundled
    channel-core fixes.
  - `aweb-aapc` — investigate Aida/Marvin mail continuation 409 after
    identity rebind.
  - Grace filed a separate P1 from Mia's outgoing mail
    `identity_mismatch` observation.
  - Ama dashboard omission remains likely AC/dashboard projection-side;
    aw team-cert state was clean.
- Scratch branch `athena/chat-sse-trust` is diagnostic only; Grace
  cherry-picked/reworked the fix into `856a560` on main. Do not use the
  scratch branch as release input.

## Wake-up state from 2026-05-18 Pi session

- `git pull --ff-only`: already up to date.
- Identity confirmed with `aw id team list`:
  - `default:aweb.ai` membership active as `athena`, persistent.
  - `aweb:juan.aweb.ai` membership active/default as `athena`, persistent.
- `aw workspace status`: no Athena claims, no locks, no focus.
- Dev-team `aw mail inbox`: no messages.
- Dev-team `aw chat pending`: no pending conversations.
- Company-team `aw mail inbox`: no messages.
- Company-team `aw chat pending`: no pending conversations.
- `../../status/engineering.md` refreshed for the 2026-05-18 state.

## Current engineering state

- Federation completion wave is shipped. Per Hestia, awid 0.5.6,
  aweb 1.23.0, and AC v0.5.42 are verified-live. app.aweb.ai health:
  `release_tag=v0.5.42`, `git_sha=7ca6ce62`, `aweb_version=1.23.0`,
  `awid_service_version=0.5.6`.
- Pi integration is active in this Pi session. The installed package
  provides aweb channel awakenings plus canonical aweb skills. The
  synthetic welcome asked for the first-move coordination loop; that
  loop has been run.
- `aweb-aaov.12` (Pi first-session synthetic welcome) is in Dave's
  lane and appears implementation/voice-pass complete:
  - c675c44 synthetic welcome + sentinel/version gating
  - 1944e3d docs link follow-up
  - 37c9bb1 Iris tone nudge
  - local aweb main has further polish through 48cee5e
- `aweb-aaox.16` remains the P0 license metadata fix for
  `@awebai/claude-channel`. Hestia owns publish. Hestia's status says
  channel-v1.4.1 tag exists but npm publish failed because GHA didn't
  install channel-core deps before building; npm may still show the
  package as Proprietary until this closes.
- **Channel auto-ack/read bug is fixed for Claude channel and source Pi
  dist, but Pi update path remains open.** `@awebai/claude-channel@1.4.3`
  stopped inbound delivery from marking messages read; `aa72312` rebuilt
  `pi-extension/dist` from current channel-core. Installed Pi users are
  not covered until `aweb-aapb` defines and verifies an update path.
- **MCP OAuth/reconnect release lane is still with Hestia.** Initial
  bless was AC `cb223c34` + aweb `03fe4bf`. Gate found stale AC alias
  test; Mia/Grace patched it (`bc2e48dd` / `5b44f724`). Grace also fixed
  the Hestia↔Athena duplicate-chat 409 in aweb `99cc2cb`. Athena
  approved the added fixes and recommended aweb `1.24.1` + AC `v0.5.43`
  repin because `99cc2cb` is after the already-published `1.24.0` tag.
  Hestia owns gate/deploy/live verification before any customer-facing
  claim. Non-blocking follow-up: `targeted_handoff_error.reason` remains
  coarse (`stale`) across failure modes.

## Active dev-team work visible

- Dave: `aweb-aaov.12` Pi synthetic welcome, active.
- Grace: `aweb-aaou.13` federation e2e matrix, active.
- Mia: `aweb-aalr.2` stale/old AWID ensure-team + AC persist refactor
  claim still visible.
- Ready P0: `aweb-aaox.16` claude-channel license metadata correction.
- MCP OAuth selected-org/reconnect fix: base reviewed set was AC
  `cb223c34` + aweb `03fe4bf`. Follow-up validation by Athena: AC
  `5b44f724` hosted MCP invite test 4 passed, black check pass,
  diff-check clean; aweb `99cc2cb` conversations + MCP contacts tests 34
  passed in detached worktree, py_compile touched files pass, diff-check
  clean. Dave summary of original OAuth symptom: dashboard selected
  org/team aweb → Claude.ai remote MCP connect → name marvin; consent
  showed personal `@juanre/marvin`; POST returned `Hosted handle is not
  available for this account`; Claude showed `code: Field required`
  because no OAuth code.

## Local repo caveats

- `aweb` symlink works; current recent commits include Pi polish:
  `48cee5e`, `9376702`, `23f2bd0`, `37c9bb1`, `1944e3d`.
- `ac` symlink now resolves through `/Users/juanre/prj/awebai/ac` →
  `aweb-cloud`; AC main is at `5b44f724`. Earlier broken-symlink note is
  superseded.
- Local `aweb` checkout is still on Dave's Pi branch, not origin/main;
  Athena reviewed aweb `03fe4bf` and `99cc2cb` in detached temp worktrees
  and removed them afterwards.
- Current local changes are `status/engineering.md` and this handoff.

## Ben / Commando federation support context

Juan flagged that Ben (Commando) may contact Athena for federation setup help.
Use current shipped federation facts, not stale local-branch docs:

- Federation v1 is **messaging-only**: mail + chat across aweb servers.
  Tasks, work queues, presence, roles, manuals, and other team-scoped state
  remain local to one aweb server.
- Verified-live completion wave: awid-service/awid `0.5.6`, aweb `1.23.0`,
  AC `v0.5.42`. Later aweb/aw `1.24.2` includes trust-display fixes but is
  not a separate federation feature wave.
- Core route: recipient address `domain/name` resolves at AWID to `did:aw`,
  current `did:key`, reachability, and namespace `default_delivery_origin`;
  sender aweb POSTs the preserved sender-signed payload to
  `<delivery-origin>/v1/federation/messages`.
- Receiver verifies: sender signature, sender current key, target address
  binding, target delivery origin matches its configured public origin,
  non-public reachability cert evidence, policy, timestamp skew, and idempotent
  delivery.
- Setup essentials for a self-hosted/BYOT namespace:
  1. Run aweb with `AWEB_PUBLIC_ORIGIN=<public origin>` (origin only, no `/api`;
     use external `https://` if TLS terminates at a proxy).
  2. Namespace controller publishes delivery origin:
     `aw id namespace set-delivery-origin --namespace <domain> --origin <origin>`.
     This requires the local namespace controller key. Hosted aweb.ai repairs
     only namespaces whose controller key hosted AC owns.
  3. Persistent identities need public addresses; first-contact federation is
     address-based, not bare `did:aw`-based.
  4. For non-public addresses, the sender must present a valid persistent team
     certificate satisfying AWID reachability (`org_only` or
     `team_members_only`); `nobody` is owner-only and will 404 for teammates.
- Strongest local proof is `scripts/e2e-oss-federation.sh` on origin/main: one
  AWID registry + two isolated aweb servers, public mail/chat first contact,
  replies, authorized/unauthorized private address cases, missing-origin
  fail-closed, and replay idempotency.
- Caveat: local aweb checkout may be on Dave's Pi branch; use `origin/main` or
  tags containing `02a344f`/`449cb17` for current self-hosting docs and
  `aw id namespace set-delivery-origin`.

## Things to check first next wake-up

1. `git pull --ff-only`.
2. Run the two-team coordination loop: dev + company inbox/chat,
   `aw work active`, `aw work ready`, and workspace status.
3. First check whether Peter sent the `aweb-aapf.5` AC review request. Review
   against the brief: local == old ephemeral; global == old persistent; hosted
   global sets identity-level delivery origin with custodial key; hosted local
   creates no AWID DID/address; no user-facing reachability choices; no `.6` or
   `.8` scope blended in.
4. Check Hestia's ship status for aweb `4c45619` as `server-v1.24.3` +
   `aw-v1.24.3`, then AC `v0.5.44` at `bdfe5631`.
5. After AC deploy, coordinate scoped repair method with Grace and require
   Hestia's post-repair hestia→{athena,sofia,iris,aida,metis,ama} matrix smoke.
6. Confirm Sofia framing before any external trust-display claim. Narrow
   claim: aweb/aw 1.24.2 fixes CLI live chat trust-display for stable
   did:aw participant rows; Pi users are not covered until `aweb-aapb`.
7. Track `aweb-aapb` (Pi update path) and `aweb-aapc` (Aida/Marvin mail
   409) as separate P1s.
8. Watch Hestia's revised MCP OAuth gate/deploy/live-verify. Expected
   release shape if she accepts Athena recommendation: aweb `1.24.1` or
   later containing `99cc2cb`, then AC `v0.5.43` with aweb pin updated
   beyond `5b44f724`.
9. Loop Sofia for narrow OAuth claim-shape framing before any
   customer-facing OAuth claim. Precise claim: dashboard-targeted existing
   hosted identity preserves selected org/team; generic `/mcp/` uses
   explicit org-first / team-second selection when ambiguous; stale/invalid
   targeted links fail closed; cached legacy tool names are restored as
   aliases.
10. Check whether Dave closed or handed off `aweb-aaov.12`.
11. If any channel event wakes the session, inspect metadata and sender
    verification before acting; reply in the existing thread/session.

## Old debt still not closed

- KI#1 closure decision-record technical content may still be owed if
  Sofia did not supersede it. Source remains
  `agents/athena/aale-trust-contract.md` + aweb commit `7759abc`.
- Playwright-MCP reproducer for Add-Existing dialog remains old
  non-feature backlog.
- Multi-team `agent_id` vs `did` comparison grep remains old audit
  debt unless a later task/comment closed it; don't assume closure from
  the 1.20.7 strict-walk fix alone.
