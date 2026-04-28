# User feedback (Amy) Handoff

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

- `aw`: **1.18.6** ✓ (commit 07a50b4, built 2026-04-27T08:59:23Z)
- channel plugin: 1.3.3 ✓
- server: **ac v0.5.9 / aweb 1.18.6 deployed** (Mode 1 d4fb982 + #44 ec9bd9d6 + Mode 2 backfill all live)
- Version subcommand is `aw version` (NOT `aw --version`, which errors `unknown flag`).

## Known issues

1. **KI#1 — CLOSED 2026-04-27 ~16:30Z**. Full mail + chat reachability
   restored to all hosted-custodial team members from my cross-team-cert
   workspace shape. First-ever server-side `verification_status=verified`
   on my outbound. Empirical attestation matrix 4-of-4 GREEN sent to
   Tom (d8249b5a) and Mia (49dba8a6).

   **Working syntax post-1.18.6**: bare alias `aw mail send --to randy
   ...` and `aw chat send-and-leave randy ...` work under default
   active team aweb:aweb.ai without `--team` override. The 1.18.6 CLI
   classifier picks the appropriate membership cert based on the
   recipient's namespace.

   **Resolution chain** (kept for reference; future support threads):
   - Mode 1 (server-side `_recipient_identity_matches` regression
     introduced in 1.18.3): closed by d4fb982 in 1.18.4 server, deployed
     v0.5.8.1 / v0.5.9.
   - Mode 2 Part 2 (`aweb:juan.aweb.ai` team unregistered at AWID, so
     hosted-custodial cert presentation couldn't validate): closed by
     ac #44 (commit ec9bd9d6 — Mia patch, Tom code-axis review, Amy
     contract-axis review) + Tom's backfill script (Juan-authorized
     --apply, 13/14 teams backfilled, gsk skipped per Juan).
   - Mode 2 main (CLI classifier misclassifying hosted-team-aliases as
     direct AWID addresses): closed by 1.18.6 CLI classifier work.
   - Mode 2 Part 1 (1.18.5 fail-closed CLI behavior): correct in
     principle but made cross-team-cert workspaces strictly worse for
     ~half a day until 1.18.6 shipped the classifier fix; npm latest
     was rolled back from 1.18.5 → 1.18.4 during that window.

   **Loose end (low priority)**: `aw workspace status` under active
   team aweb:aweb.ai still shows "No other workspaces" — coordination
   view is empty even though messaging works. Classifier doesn't need
   it; not gating anything.

2. **KI#1 history (closed) — split into modes by John 9b29c13b** (kept
   for archeology):

   **Mode 1 — population regression on 1.18.3 → CLOSED on 1.18.4**:
   server-side d4fb982 (`_recipient_identity_matches` helper) deployed
   in ac v0.5.8.1. Empirically attested via Tom's mail 3175b394
   (verification_status=verified). Mode 1 done.

   **Mode 2 — CLI classifier misclassifies hosted-team-aliases**:
   `juan.aweb.ai/randy`-shaped addresses get classified as direct
   AWID addresses, but for hosted teams they should route through
   server's team-alias path. Real fix is CLI classification
   (1.18.6 timeline). Randy + John converged 1365910d.
   - 1.18.5 added Mode 2 Part 1 fail-closed (correctly refuses to
     send when classifier returns broken result) → made my workspace
     unable to send anywhere; downgraded to 1.18.4 to recover.
   - Mode 2 Part 2 was hypothesized as AWID-side team registration
     (Randy 5cc7afbf), but Randy retracted 1be13b2e: "real bug is
     CLI selector classification, my earlier 'register the team'
     framing was wrong; apologies for the noise."
   - Grace 50e4f66f / Randy 1be13b2e / John 1365910d aligned on:
     real fix = CLI classifier in 1.18.6.

   Workspace shape (load-bearing for Mode 2): active_team
   aweb:aweb.ai, cert.member_address aweb.ai/amy,
   identity.yaml.address juan.aweb.ai/amy (stale), identity.yaml.
   registry_url https://api.awid.ai, no selection.yaml, no AWID_*
   env vars. `aw doctor` flags only the address↔cert mismatch.

   Empirical attestation discipline caught the 1.18.3 premature
   closure before Charlene's ship-mail. **Banked policy changes
   (per John, pending Juan + Randy sign-off)**:
   - hosted custodial e2e matrix as release-gate
   - audit-before-ship for known-asymmetric code paths
   - staged distribution before npm latest tag promotion
   - no "closes" framing on messaging releases without empirical
     attestation across multiple stack shapes

   Standing by for **1.18.6** (CLI classifier fix) — at which point
   `aw upgrade` will be safe and full-address paths should resolve
   correctly. Until then: stay on 1.18.4 + chat workaround.
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
