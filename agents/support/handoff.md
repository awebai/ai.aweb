# Support (Amy) Handoff

Last updated: 2026-04-24

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
cosmetic — no trust or identity change. With aw 1.17.0, the switch
is a single command:

```
aw id team switch <team_id>
```

teams.yaml, workspace.yaml, and the cert served by `aw id cert show`
all update together. (Pre-1.17.0 required a manual workspace.yaml
edit; that workaround is no longer needed — see decisions.md
2026-04-23 aakq epic.)

See `../../docs/decisions.md` 2026-04-21 for the full setup procedure.

## Local versions (this workspace)

- `aw`: 1.17.0 (commit e275743) ✓
- channel plugin: **1.1.0** ✗ (need 1.3.0; pending `/plugin update`
  by Juan + session restart). Until upgraded, channel events still
  exhibit the pre-1.3.0 address-signing context that may be the root
  cause of Known Issue #1.

## Known issues

1. **IDENTITY MISMATCH on outbound messages** — Amy's messages arrive
   at other agents marked `verified=false` / `IDENTITY MISMATCH`.
   Re-tested 2026-04-24 against Randy: still reproduces, but my
   channel plugin is **1.1.0** (pre-aakq.1 fix to channel
   address-signing context). Randy's hypothesis: 1.1.0 signs with
   identity.yaml.address while the cert binds aweb.ai/amy, producing
   the mismatch. Pending plugin upgrade to 1.3.0 + re-test before
   declaring resolve-or-reproduce.

2. **Channel plugin auto-acks mail** — The aweb channel plugin
   acknowledges mail on delivery, so `aw mail inbox` shows nothing.
   Workaround: use `aw mail inbox --show-all` or read mail from
   channel events in real time. Dave flagged as design question for
   Juan. Two options discussed: (a) channel stops auto-acking, agent
   acks explicitly; (b) add a "recently delivered" view.

3. **`aw mail send` returns 409 for me** (aweb-aakz, P2, filed by
   Randy 2026-04-25) — `aw mail send --to-address <full-address>`
   returns `http 409: Authenticated DID matches multiple active
   local agents`. Reproduces with and without `--team` override.
   Chat path works fine. Hypothesis: server resolves my did:key to
   two active local-agent rows (one per membership in
   workspace.yaml) and the mail auth path doesn't disambiguate via
   team header while chat does. **Workaround until fixed:** route
   any agent-to-agent updates through `aw chat send-and-leave`
   instead of mail. Affects routing feedback to Avi, Tom, Randy,
   etc. Discovered 2026-04-24 trying to mail Randy a handoff-update
   confirmation.

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

4. **`aw id team switch` left workspace.yaml stale** (aakn, fixed in
   aweb 1.17.0 / aakq epic 2026-04-23) — `runTeamSwitch` now also
   loads and saves workspace.yaml. Confirmed 2026-04-24:
   workspace.yaml.active_team and teams.yaml.active_team both
   `aweb:aweb.ai`, in sync since 2026-04-21.

5. **`aw whoami` printed self-inconsistent address/domain** (aako.2,
   fixed in aweb 1.17.0 / aakq.2 — Go CLI now derives address from
   the selected cert, not identity.yaml). Confirmed 2026-04-24:
   `aw whoami` shows Address=aweb.ai/amy, Domain=aweb.ai (consistent).
   Note: identity.yaml.address itself is still stale on disk
   (juan.aweb.ai/amy) — that's the input shape for the channel-plugin
   side of aako, which channel 1.3.0 fixes.

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
