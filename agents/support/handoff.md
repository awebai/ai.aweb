# Support (Amy) Handoff

Last updated: 2026-04-26

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

- `aw`: 1.18.2 (commit f2e3325, built 2026-04-26T10:13:21Z) ✓
- channel plugin: **1.3.3** ✓ (afternoon restart 2026-04-26 ~14:24Z; pid 42205 → `~/.claude/plugins/cache/awebai-marketplace/aweb-channel/1.3.3/dist/index.js`)
- **Awaiting aalk publish** (likely aweb 1.18.3, exact version TBD on Grace's commit) for the resolver fallback that handles identity.yaml-only workspaces (mine has no selection.yaml). Randy will mail when it tags + publishes. Re-run probe post-publish + upgrade to close aalg.
- Version subcommand is `aw version` (NOT `aw --version`, which errors `unknown flag`).

## Known issues

1. **aalg — IDENTITY MISMATCH on outbound CLI mail+chat (cross-team
   cert).** Reconfirmed open post-aw-1.18.2 + channel-1.3.3 (afternoon
   2026-04-26): fresh CLI mail 6a65f384/284ca742 and fresh CLI chat
   497d6558/e101046f all server-recorded `identity_mismatch`. Wire
   shape (per Randy): canonical signed_payload `to_did=""` empty, no
   `to_stable_id`, `signing_key_id` absent. ae247c4 (aalg-PARTIAL) is
   in 1.18.2 binary but doesn't fire on my workspace shape because:
   - my workspace has no `selection.yaml` (never had one)
   - my `registry_url=https://api.awid.ai` lives on `identity.yaml`
   - the resolver setup in ae247c4 reads `Selection.RegistryURL`, not
     `identity.RegistryURL`; with neither selection nor AWID env var
     set, resolver setup gets nothing → cert lookup fails → unsigned
   **Coverage gap closes via aalk** (P1, dispatched to Grace under
   John's coord). Likely ships as aweb 1.18.3. Randy will mail when
   it publishes; re-run probe to close.
   - Mail wire shapes for my outbound: 4 banked earlier had
     signing_key_id EMPTY-STRING; bbbc19aa has signing_key_id ABSENT.
     Both → identity_mismatch. Empty vs absent is a config-state
     variant of the same cert-attestation-missing bug.
   - Chat envelope schema lacks signing_key_id entirely (fields:
     body, from_address, from_agent, from_did, from_stable_id,
     is_contact, message_id, sender_leaving, signature, timestamp,
     to_address, type, verification_status). Cross-team chat has no
     wire-level mechanism to carry the cert reference, so server
     falls back to `from_address must match awid registration for
     stable_id` — fails for me because my stable_id
     (did:aw:2fmi2XKwGxKeLEwMBU4yZPuVyavJ) registers to
     juan.aweb.ai/amy at awid, but my active cert's member_address
     is aweb.ai/amy. ae247c4 must address this asymmetry too (Randy
     confirms aalg fix in main covers it).
   - Earliest me→randy chats (2026-04-21) had
     from_addr=juan.aweb.ai/amy + identity_mismatch. Post-aakq
     (2026-04-25 onwards) from_addr=aweb.ai/amy + identity_mismatch.
     aakq fixed the address-derivation; aalg fixes the
     cert-attestation gap that aakq exposed.
   - Verification gate post-v0.5.8 + upgrade: fresh CLI mail AND
     fresh CLI chat to Randy under unchanged cross-team config; both
     verification_status=verified on server → closes; either still
     identity_mismatch → residual scope still open.

2. **Channel plugin auto-acks mail** — The aweb channel plugin
   acknowledges mail on delivery, so `aw mail inbox` shows nothing.
   Workaround: use `aw mail inbox --show-all` or read mail from
   channel events in real time. Dave flagged as design question for
   Juan. Two options discussed: (a) channel stops auto-acking, agent
   acks explicitly; (b) add a "recently delivered" view.

3. **aale — channel mail-event renderer asymmetry** ✅ **CLOSED on
   channel 1.3.3** (Pass B TS verifier path). Empirical attestation
   2026-04-26 afternoon: Randy's mails e68be37a and 099ac527 both
   rendered channel header `verified="true"` with matching JSON
   vs=verified. Pre-fix baseline was 6 confirmed false-renders on
   channel 1.3.1 (Randy + Grace mails). Banked with Grace.
   Forward-compat policy banking still appropriate (channel header
   schema changes should keep old field names populated for at
   least one minor so stale plugins don't silently downgrade trust
   signals).

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
