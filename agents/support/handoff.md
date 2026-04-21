# Support (Amy) Handoff

Last updated: 2026-04-21

## Current state

Amy is `did:aw:2fmi2XKwGxKeLEwMBU4yZPuVyavJ` (persistent, self-custodial).
Two addresses, both `public`:
- `aweb.ai/amy` — ACTIVE sender; team `aweb:aweb.ai`,
  workspace_id `ad83997e-5380-49a8-9867-aea3b31ebbd2`
- `juan.aweb.ai/amy` — inbound still routes here; team
  `aweb:juan.aweb.ai`, workspace_id `f758e6e9-4731-4944-a104-052995c2a3af`

Inbox is per-identity (did_aw), so mail to either address shows up
in `aw mail inbox` regardless of active team. Outbound uses the
active team's cert `member_address`, so messages Amy initiates
now say `from: aweb.ai/amy`.

### Switching sender address

Both addresses point to the same `did:aw`, so switching is
cosmetic — no trust or identity change. But two files must stay in
sync. `aw id team switch <team_id>` updates `.aw/teams.yaml` and the
cert `aw id cert show` serves, but does NOT update
`.aw/workspace.yaml.active_team`. Coordination commands
(`aw mail send`, `aw chat send-*`) read workspace.yaml, so they keep
the old address until workspace.yaml is also edited. Until this is
fixed (see Known issues below), a switch requires:

```
aw id team switch <team_id>
# then edit .aw/workspace.yaml: set active_team to the same value
```

See `../../docs/decisions.md` 2026-04-21 for the full setup procedure.

## Known issues

1. **IDENTITY MISMATCH on outbound messages** — Amy's messages arrive
   at other agents marked `IDENTITY MISMATCH` / `verified=false`.
   Dave suspects stale TOFU pins from a previous key. Not blocking
   but erodes trust signal.

2. **`aw id team switch` leaves workspace.yaml stale** —
   teams.yaml.active_team and the cert served by `aw id cert show`
   flip, but workspace.yaml.active_team does not. Coordination
   commands read workspace.yaml, so the switch is silently partial
   until workspace.yaml is also updated. Filed as task
   `aweb-aakn` (#761, team `aweb:juan.aweb.ai`). Fix: make
   runTeamSwitch also load and save workspace.yaml via
   applyTeamStateToWorkspaceCache.

3. **`aw whoami` prints stale address when active team differs from
   home namespace** — `address` is read from identity.yaml
   (`juan.aweb.ai/amy`) while `domain` is read from the active team
   (`aweb.ai`), producing a self-inconsistent record. Low priority.

4. **Channel plugin auto-acks mail** — The aweb channel plugin
   acknowledges mail on delivery, so `aw mail inbox` shows nothing.
   Workaround: use `aw mail inbox --show-all` or read mail from
   channel events in real time. Dave flagged as design question for
   Juan. Two options discussed: (a) channel stops auto-acking, agent
   acks explicitly; (b) add a "recently delivered" view.

## Resolved issues

1. **Cross-team chat addressing** (fixed 2026-04-20) — Senders from
   other teams now show fully qualified address in
   `aw chat pending --json` `participant_addresses` field. Reply
   using full address: `aw chat send-and-wait <domain>/<alias> "msg"`

2. **Cross-team mail from_address** (fixed 2026-04-21) — Mail
   `from_address` now shows fully qualified address instead of raw
   `did:key`. Root cause was identity-auth path lacking team context;
   henry fixed the derivation.

3. **Channel event from attribute** (fixed 2026-04-21) — Channel
   events now show `from="gsk.aweb.ai/gsk"` instead of bare alias.

## Conversations

### gsk (gsk.aweb.ai/gsk)
- First contact 2026-04-20. Juan asked them to reach out.
- Onboarding stage 1 — getting oriented, no active tasks yet.
- Answered: mail vs chat, workspace status commands, team conventions,
  getting-started steps. Replied to intro mail.
- No open questions.

## Escalation cheat sheet

| Topic | Route |
|-------|-------|
| Bugs / UX / features / stories | Avi |
| Identity / namespace / team recovery | Tom first, Randy if slow |
| Engineering / CLI / protocol | Randy (or dave for OSS) |
| Needs `ac` access | Tom |
| Needs `co.aweb` access | Avi |
| Urgent, no response | Juan |

Amy does API-first triage on identity recovery cases but does not
execute dashboard Replace — that is a human action.

## Knowledge base status

- `agent-guide.md` in aweb is the current path.
- `../../docs/support/agent-identity-recovery.md` synced from ac via
  `make docs-sync`. Re-run after any ac-side edits.
- Identity docs in aweb are v1.8.1+: `identity-guide.md` and
  `trust-model.md` are current sources.

## Patterns to watch

- Cross-team senders must have a registered address at awid to be
  reachable for replies. If `from_address` shows bare alias or
  raw `did:key`, the sender may lack a registered address or be
  running an old CLI.
- Sessions created before server fixes may cache stale data — a fresh
  session may be needed.
- With channel plugin active, always use `aw mail inbox --show-all`
  to see all mail, since the channel auto-acks on delivery.
