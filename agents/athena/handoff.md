# Athena Handoff
Last updated: 2026-05-19 13:41 GMT

## Read this first

You are Athena. You bridge two teams:

| Team | Visibility | Purpose |
|------|------------|---------|
| `aweb:juan.aweb.ai` | public dev team | Code authoring, tasks, claims, developer coordination |
| `default:aweb.ai` | private company team | Direction, release framing, support, operations, outreach, analytics |

Default active team is `aweb:juan.aweb.ai`. Use `--team default:aweb.ai`
for company-side mail/chat. Dev-team members do not need company-team
release mechanics; to them, Athena is the gate.

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
- `aweb-aapf.3` first review of Peter commit `0e06284` is not approved. Athena
  found two blockers: (1) federated first-contact to an existing local `did:key`
  can create a new mail conversation/chat session; local `did:key` targets must
  require an existing participant conversation/session with sender+target; (2)
  Peter initially planned a route-assertion/capability protocol, but Juan
  pushed back that local agents are renamed ephemerals and already had outbound
  + reply-in-established-context behavior. Athena tightened the gate: preserve
  and simplify existing ephemeral/local reply behavior, do not grow a local
  mini-registry/protocol unless a concrete exploit requires it, and require a
  deletion/complexity note with the patched commit. Peter ACKed the pivot.
  CLI/channel/AC work remains gated until `.3` approval.
- `aweb-aapf.7` is assigned to Grace as a second-developer test-contract pass.
  Grace ACKed. She may inventory stale reachability/private-address/team-cert/
  conversation-auth expectations before `.3` approval, but should not change
  assertions until `.3` is approved. Goal is fewer tests/e2e that prove only the
  new contract, plus stale test deletion.

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
3. First check whether Peter sent the patched `aweb-aapf.3` server
   routing/federation review request. Scope must stay limited to aweb server
   routing/federation; no CLI/channel/AC refactors until `.3` is approved.
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
