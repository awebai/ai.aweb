# Support (Amy) Handoff

Last updated: 2026-04-25

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

- `aw`: 1.18.1 (commit ff8161c) ✓ (upgraded 2026-04-25 via `aw upgrade`)
- channel plugin: **1.1.0** ✗ (need 1.3.1; pending `/plugin update
  aweb-channel@awebai-marketplace` by Juan + session restart). 1.3.1
  carries both aakq.1 (precedence flip — likely fix for KI#1) and a
  .mcp.json shape fix that was broken in 1.1.0-1.3.0.

## Known issues

1. **IDENTITY MISMATCH on outbound — CLI cross-team-cert residual
   (separate from v0.5.7 dashboard fix).** Status 2026-04-25
   evening: v0.5.7 closes the ac dashboard mail TX path (Grace's
   RCA, fix in ac/backend f5db375a). My reproductions are NOT on
   that path — all 4 banked instances (4b4468ff, 9f426014,
   d5e80f3b, 335a4c2b) are CLI `aw mail send`. Randy revised the
   decision-record framing to "TX-shape root cause closed (dashboard);
   CLI cross-team-cert empty-string signing_key_id residual
   identified" and dispatched the CLI investigation to John.
   - Empirical differential (this workspace, 2026-04-25): 18/18
     inbound mails to me show `signing_key_id` ABSENT and verify
     fine. Mine outbound shows `signing_key_id` EMPTY-STRING and
     downgrades to `identity_mismatch`. Empty-string is exclusive
     to my outbound — sender-side specific.
   - Likely triggered by my cross-team config: active team's
     cert.member_address (aweb.ai/amy) ≠ identity.yaml.address
     (juan.aweb.ai/amy — stale home). Hypothesis points at signEnvelope
     in aweb/cli/go/awid/client.go:40-97 — either the early return
     at line 41 fires on this config and a downstream layer fills
     FromDID without filling SigningKeyID, or a non-signEnvelope
     path produces my wire envelope. John has the OSS contract
     authority to dig.
   - Local↔awid binding INTACT (no rotation, both addresses bind
     to same did:key — ruled out as cause).
   - Operational impact: my outbound mail arrives readable but
     unverified to recipients. Chat path unaffected.
   - Investigation packet mailed to Randy 2026-04-25 (msg
     83b35955) — self-contained for forwarding to John.
   - Closure protocol: after CLI residual fix ships, send Randy
     fresh CLI mail unchanged config; verified → closes; still
     identity_mismatch → still residual scope.

2. **Channel plugin auto-acks mail** — The aweb channel plugin
   acknowledges mail on delivery, so `aw mail inbox` shows nothing.
   Workaround: use `aw mail inbox --show-all` or read mail from
   channel events in real time. Dave flagged as design question for
   Juan. Two options discussed: (a) channel stops auto-acking, agent
   acks explicitly; (b) add a "recently delivered" view.

3. **Channel plugin 1.1.0 mail-event header renders verified=false
   on server-verified mail** (aweb-aale, P3, filed by Randy
   2026-04-25). Observed on Randy's release-announcement mail.
   Initial diagnosis suspected sender-side or trust failure; root
   cause is RX rendering only. Verified by `aw mail inbox
   --show-all --json`: all 16 inbox mails carry server
   `verification_status: "verified"` with valid signatures,
   including the one whose channel header read `verified="false"`.
   Plugin 1.1.0 chat-events render the correct header on the same
   plugin/sender/hour — only mail events misrender. Likely cause:
   1.1.0 mail-event renderer reads a header field whose name
   changed in the aakq.1 schema and defaults to false on missing.
   **Resolves on /plugin update to 1.3.1.** Not a wire/trust bug;
   surface display only. aale also tracks the forward-compat policy
   (channel header schema changes should keep old field names
   populated for at least one minor so stale plugins don't
   silently downgrade trust signals).

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
   side of aako, which channel 1.3.1 fixes.

6. **`aw mail send` 409 multi-membership** (aakz, fixed in aweb 1.18.1
   / aala.7 — identity_auth_deps.py identity-scoped path now tolerates
   persistent did:aw rows with multiple active team memberships).
   Confirmed 2026-04-25: `aw mail send --to-address juan.aweb.ai/randy`
   succeeded (message_id 9f426014-8d27-4c53-bae6-84339a028d84). The
   chat-fallback workaround documented yesterday is no longer needed.

## Cross-machine BYOIT — answer for stage 4+ users

When a user describes "team controller on machine A, agent on machine
B" or asks how to add a remote agent to a team they own, the canonical
flow as of aweb 1.18.1 is:

1. **Joining agent (machine B):** `aw id team request` — prints the
   command the controller needs to run, including the joining agent's
   `did:key`.
2. **Controller (machine A):** `aw id team add-member --did <member-did:key>`
   — approves the remote member; output now includes the fetch-cert
   hint for the joiner.
3. **Joining agent:** `aw id team fetch-cert --namespace <domain> --team <team> --cert-id <id>`
   — pulls the issued cert from awid.
4. **Joining agent:** `aw init` (or re-init the workspace) — comes
   online in the team.

Sources: `aweb/docs/awid-sot.md` (Issuance flow) and
`aweb/docs/identity.md` (BYOIT cross-machine paragraph). Read these
when a user goes deep — don't paraphrase from memory.

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
