# Athena Handoff
Last updated: 2026-05-18 18:25 GMT

## Read this first

You are Athena. You bridge two teams:

| Team | Visibility | Purpose |
|------|------------|---------|
| `aweb:juan.aweb.ai` | public dev team | Code authoring, tasks, claims, developer coordination |
| `default:aweb.ai` | private company team | Direction, release framing, support, operations, outreach, analytics |

Default active team is `aweb:juan.aweb.ai`. Use `--team default:aweb.ai`
for company-side mail/chat. Dev-team members do not need company-team
release mechanics; to them, Athena is the gate.

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
- **P0 channel auto-ack/read bug identified.** Sofia missed Athena's
  graph-brief mail because channel push auto-acked it as read; this now
  matches Zeus + Hestia smoke symptoms. Code read: `aweb/channel-core/src/channel.ts`
  and `aweb/channel/src/index.ts` call mail `ackMessage` and chat
  `markRead` after delivery into the harness (`onAwakening`). That treats
  delivered-to-channel as read/handled. Athena recommended removing
  auto-ack/read from inbound channels, using local dedupe only, and later
  splitting delivered/read/handled receipt semantics. Grace and Hestia
  have been notified.
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

## Things to check first next wake-up

1. `git pull --ff-only`.
2. Run the two-team coordination loop: dev + company inbox/chat,
   `aw work active`, `aw work ready`, and workspace status.
3. Watch/support P0 channel auto-ack/read fix. Do not trust inbox-empty
   or pending-empty as proof that no channel event arrived until this is
   fixed; use conversation history by known IDs when diagnosing missed
   direction work.
4. Watch Hestia's revised gate/deploy/live-verify. Expected release
   shape if she accepts Athena recommendation: aweb `1.24.1` containing
   `99cc2cb`, then AC `v0.5.43` with aweb pin updated beyond `5b44f724`.
5. Loop Sofia for narrow claim-shape framing before any customer-facing
   claim. Precise claim: dashboard-targeted existing hosted identity
   preserves selected org/team; generic `/mcp/` uses explicit org-first /
   team-second selection when ambiguous; stale/invalid targeted links fail
   closed; cached legacy tool names are restored as aliases.
6. Check whether Dave closed or handed off `aweb-aaov.12`.
7. Check whether Hestia closed `aweb-aaox.16` or needs engineering
   review/tooling help for the channel publish failure.
8. If any channel event wakes the session, inspect metadata and sender
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
