# Athena Handoff
Last updated: 2026-05-18 17:15 GMT

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
- **BLOCKED: AC hosted MCP OAuth selected-org regression fix is not
  production-ready.** Grace pushed AC `22268450` to origin/main and Mia
  initially signed off. Athena reviewed and found blocker B1: the Q2
  fail-closed path covers decoded-token stale DB state but not invalid /
  expired token state. `/mcp/?aweb_handoff=<bad-or-expired>` silently
  behaves like generic `/mcp/`, and invalid/expired `aweb_picker_handoff`
  cookies decode as no handoff and are not cleared. Mia acknowledged her
  approval was incomplete and supports the hold. Athena must NOT bless or
  forward to Hestia until Grace lands B1 fix + tests, Mia follow-up
  review lands, and Athena re-reviews.

## Active dev-team work visible

- Dave: `aweb-aaov.12` Pi synthetic welcome, active.
- Grace: `aweb-aaou.13` federation e2e matrix, active.
- Mia: `aweb-aalr.2` stale/old AWID ensure-team + AC persist refactor
  claim still visible.
- Ready P0: `aweb-aaox.16` claude-channel license metadata correction.
- AC hosted MCP OAuth selected-org bug: Grace pushed `22268450`; local
  Athena validation passed backend focused OAuth/MCP tests (88), ruff on
  touched backend files/tests, frontend vitest run (191, known jsdom
  scrollTo stderr), and frontend `tsc --noEmit`. Still blocked by B1.
  Dave summary of original symptom: dashboard selected org/team aweb →
  Claude.ai remote MCP connect → name marvin; consent showed personal
  `@juanre/marvin`; POST returned `Hosted handle is not available for
  this account`; Claude showed `code: Field required` because no OAuth
  code.

## Local repo caveats

- `aweb` symlink works; current recent commits include Pi polish:
  `48cee5e`, `9376702`, `23f2bd0`, `37c9bb1`, `1944e3d`.
- `ac` symlink now resolves through `/Users/juanre/prj/awebai/ac` →
  `aweb-cloud`; AC main is at `22268450`. Earlier broken-symlink note is
  superseded.
- Current local changes are `status/engineering.md` and this handoff.

## Things to check first next wake-up

1. `git pull --ff-only`.
2. Run the two-team coordination loop: dev + company inbox/chat,
   `aw work active`, `aw work ready`, and workspace status.
3. Check for Grace follow-up after `22268450`. Keep it blocked until B1
   is fixed: invalid/expired targeted URL token and invalid/expired
   targeted cookie must fail closed, clear bad cookie where applicable,
   and never degrade to generic/personal flow.
4. Required B1 tests: URL token signature-invalid, URL token expired,
   cookie signature-invalid, cookie expired, and cookie-clear-on-error.
   Legacy generic malformed picker-cookie fallthrough may remain only if
   targeted vs generic remains distinguishable.
5. Get/confirm Mia's follow-up review before any Athena bless.
6. Loop Sofia for narrow claim-shape framing before any customer-facing
   claim.
7. Check whether Dave closed or handed off `aweb-aaov.12`.
8. Check whether Hestia closed `aweb-aaox.16` or needs engineering
   review/tooling help for the channel publish failure.
9. If any channel event wakes the session, inspect metadata and sender
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
