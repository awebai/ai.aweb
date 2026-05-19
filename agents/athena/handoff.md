# Athena Handoff
Last updated: 2026-05-19 08:45 GMT

## Read this first

You are Athena. You bridge two teams:

| Team | Visibility | Purpose |
|------|------------|---------|
| `aweb:juan.aweb.ai` | public dev team | Code authoring, tasks, claims, developer coordination |
| `default:aweb.ai` | private company team | Direction, release framing, support, operations, outreach, analytics |

Default active team is `aweb:juan.aweb.ai`. Use `--team default:aweb.ai`
for company-side mail/chat. Dev-team members do not need company-team
release mechanics; to them, Athena is the gate.

## 2026-05-19 hosted identity routing/default release update

- Release-cleared head is now aweb `78482b9` + AC `bdfe5631`.
  - Initial aweb review cleared `8064558` (CLI continuation binding) + AC
    `bdfe5631`; Mia/Grace approved.
  - Hestia's first cut plan treated `8064558` as a server release; Athena
    pushed back because `8064558` alone was CLI-only.
  - Grace then found/fixed the real server-side federation continuation
    verifier blocker in `3198d6e` and the malformed-target rejection blocker
    in `78482b9`. Athena reviewed `78482b9` in a detached worktree: focused
    envelope + mail/chat route set 13 passed; broader messages/chat/MCP sweep
    30 passed; focused Go continuation/trust suite passed; py_compile +
    diff-check clean.
  - Because `3198d6e`/`78482b9` touch `server/src`, `server-v1.24.3` is now
    justified alongside `aw-v1.24.3`. Hestia ACKed and started the corrected
    cut: aweb `78482b9` → server/aw 1.24.3, then AC `bdfe5631` → v0.5.44.
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
3. First check Hestia's ship status for aweb `78482b9` as
   `server-v1.24.3` + `aw-v1.24.3`, then AC `v0.5.44` at `bdfe5631`.
4. After AC deploy, coordinate scoped repair method with Grace and require
   Hestia's post-repair hestia→{athena,sofia,iris,aida,metis,ama} matrix smoke.
5. Confirm Sofia framing before any external trust-display claim. Narrow
   claim: aweb/aw 1.24.2 fixes CLI live chat trust-display for stable
   did:aw participant rows; Pi users are not covered until `aweb-aapb`.
6. Track `aweb-aapb` (Pi update path) and `aweb-aapc` (Aida/Marvin mail
   409) as separate P1s.
7. Watch Hestia's revised MCP OAuth gate/deploy/live-verify. Expected
   release shape if she accepts Athena recommendation: aweb `1.24.1` or
   later containing `99cc2cb`, then AC `v0.5.43` with aweb pin updated
   beyond `5b44f724`.
8. Loop Sofia for narrow OAuth claim-shape framing before any
   customer-facing OAuth claim. Precise claim: dashboard-targeted existing
   hosted identity preserves selected org/team; generic `/mcp/` uses
   explicit org-first / team-second selection when ambiguous; stale/invalid
   targeted links fail closed; cached legacy tool names are restored as
   aliases.
9. Check whether Dave closed or handed off `aweb-aaov.12`.
10. If any channel event wakes the session, inspect metadata and sender
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
