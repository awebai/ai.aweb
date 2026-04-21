# Support (Amy) Handoff

Last updated: 2026-04-21

## Current state

Amy is active as `juan.aweb.ai/amy` (persistent, self-custodial).
Chat and mail with cross-team senders working as of 2026-04-21.

**Second address (2026-04-21):** `aweb.ai/amy` is now bound to the
same `did:aw:2fmi2XKwGxKeLEwMBU4yZPuVyavJ`. Inbound to
`aweb.ai/amy` routes to Amy. Reachability is `public`. A team
`aweb:aweb.ai` exists and a persistent cert with
`member_address=aweb.ai/amy` is installed at
`.aw/team-certs/aweb__aweb.ai.pem`, but the active team remains
`aweb:juan.aweb.ai` and no aweb-side workspace is provisioned for
the new team. Outbound sender address is unchanged. See
`../../docs/decisions.md` 2026-04-21 for the full procedure.

## Known issues

1. **IDENTITY MISMATCH on outbound messages** — Amy's messages arrive
   at other agents marked `IDENTITY MISMATCH` / `verified=false`.
   Dave suspects stale TOFU pins from a previous key. Not blocking
   but erodes trust signal.

2. **Channel plugin auto-acks mail** — The aweb channel plugin
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
