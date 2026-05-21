# Athena Handoff
Last updated: 2026-05-21 09:27 GMT

## Read this first

You are Athena. You bridge two teams:

| Team | Visibility | Purpose |
|------|------------|---------|
| `aweb:juan.aweb.ai` | public dev team | Code authoring, tasks, claims, developer coordination |
| `default:aweb.ai` | private company team | Direction, release framing, support, operations, outreach, analytics |

Default active team is `aweb:juan.aweb.ai`. Use `--team default:aweb.ai`
for company-side mail/chat. Dev-team members do not need company-team
release mechanics; to them, Athena is the gate.

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
- Current heads for next review: aweb main `e332bf8`; AC main `82ec0b8d`; AC in-flight `origin/mia/aapj-3-phase-a` at `7093f693`; AC in-flight `origin/olivia-aapj-4` at `473f74f0`.
- Peter was routed to help Mia with AC mirror/schema review (no edits unless asked). He found a real blocker: AC `dashboard.py` constructs `TeamIdentity(lifetime=...)`; current aweb source requires `identity_scope`. Mia confirmed default AC local tests still use PyPI `aweb==1.24.4`, so `.3` must add/use a sibling-source backend validation path; do not ask Hestia to tag/publish under Juan hold. Mia landed prerequisite `e1e476ee` and Phase B migration half `a42ddd6c`; branch is intentionally red under `test-backend-aweb-local` until Phase B 2/2 rewrites code/tests/gate path. Peter has been asked to re-review `a42ddd6c`.
- `aweb-aapj.4` closed/approved branch-ready at AC `origin/olivia-aapj-4` `eec512d4`. Athena validation: diff-check, aapj vocab gate, targeted greps, dashboard build, frontend tests 38 files/194 tests, lint 0 errors/2 unrelated warnings, frontend build. Dave re-reviewed no blockers. Merge is held until `.3` lands because `.4` expects post-`.3` backend wire shapes (`identity_scope`, removed old response fields).
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
