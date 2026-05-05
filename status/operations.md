# Operations Status

Last updated: 2026-05-06 00:30 CEST (Hestia, post v0.5.22 deploy + pagination root cause confirmed)

## Current focus

**aame epic shipped (1.20.0/1.20.1 + AC v0.5.22) + duplicate-1to1
cleanup executed.** One open mail-409 bug — root cause:
`/v1/conversations` first-page-of-100 cap + chat activity pushing
older mail conversations off-page → CLI's
`findUniqueMailConversationForTarget` never sees them → auto-genUUID
→ server-side full-DB dedup → 409. Athena's Go probe (mail 27c74c17)
reconciled my full-DB-scan diagnosis with the empirical 409. Fix
path: aweb 1.20.2 + AC v0.5.23 with optional /v1/conversations
filters (`participant_did`, `participant_address`,
`conversation_type`); Grace implementing. Verified-live mail held
until 1.20.2 + v0.5.23 ship clean.

## Live state (verified 2026-05-05 22:00Z)

- `app.aweb.ai/health`: `release_tag=v0.5.22`, `aweb_version=1.20.1`,
  `awid_service_version=0.5.4`,
  `git_sha=f6c27c619d0c5e37e3aa096c177d11e40a0984a0`. Started
  2026-05-05T21:27:26Z.
- `api.awid.ai/health`: `version=0.5.4`, redis/db/schema healthy.
- aweb OSS published: server 1.20.0/1.20.1 on PyPI; aw 1.20.0/1.20.1 on
  npm + GH Releases. AC v0.5.22 pins aweb-server 1.20.1.
- Migration-immutability gate: passed at release-ready ("OK: 4 migration
  file(s) match prod recorded checksums across schemas
  ['aweb', 'aweb_cloud', 'server']"). First real-world use post-landing.
- Smoke probes 2026-05-05: alias + `--to-address` both attach to
  existing conversation 96317ca9 (athena↔hestia) cleanly,
  `verification_status=verified`.

## Release pipeline

- aame epic: aweb 1.20.0 r1 (1c70821) shipped → Phase 12 chat-reply abort
  diagnosed (CLI stderr-suppression masking 409). Hotfix d666119 + test
  mocks 18b4d75 → r2 (1510821) green. Published 1.20.0 + 1.20.1.
- AC v0.5.22 r1: A.6a 409 on identity-DIDKey passthrough →
  oss_auth.py allowlist fix (commit f6c27c61) → r2 green.
- Pre-deploy duplicate-1to1 cleanup procedure executed cleanly via
  Athena's collapse-only doc — 195 conversations closed across 16 pairs.
  Smoke probe attached to pre-deploy 96317ca9 cleanly post-deploy:
  counterexample to "all pre-deploy 409s" framing.
- Verified-live for v0.5.22 deferred until multi-team-agent bug is
  closed (Juan: "do not ship anything until all is fixed and fully
  e2e tested").

## Operational discrepancies

- **Mail 409 on stale-by-recency conversation reply (open).** Root
  cause: `/v1/conversations` first-page-of-100 cap + sort by
  last_message_at DESC. CLI's
  `findUniqueMailConversationForTarget` (mail.go:148) calls
  `c.ListConversations(ctx, 100)`; for an active agent with chat
  sessions pushing older mail off the first page, the target
  conversation is invisible to the CLI; auto-genUUID
  (awid/mail.go:60); server full-DB dedup correctly catches the
  existing conversation; 409. Affects any agent with >100 mail+chat
  conversations — realistic almost immediately on a coordination
  platform. Fix path: aweb 1.20.2 + AC v0.5.23 with server-side
  `/v1/conversations` filters (`participant_did`,
  `participant_address`, `conversation_type`) + CLI focused query +
  cursor-pagination fallback for old-server compat + regression
  test (101+ conversations, target older than the 100th). Grace
  implementing.
- **Open follow-up (Athena's lane, not blocking 1.20.2):**
  Multi-team-agent agent_id-vs-did comparison. cp.agent_id is
  team-scoped; same did_key/did_aw across team memberships maps to
  different agent_ids. Any code path comparing on cp.agent_id
  rather than cp.did/did_aw will misbehave for multi-team agents.
  Worth a grep across aweb codebase. I flagged this in 1eca135b
  before pagination was confirmed as the actual 409 cause; Athena
  agreed it's worth filing.
- **Pre-aame chat sessions 403 on continuation.** W3 protection
  rejects chat replies on conversations whose signed messages predate
  binding. Workaround: `aw chat send-and-wait <peer> "msg"
  --start-conversation`. DELETE-240 chat_sessions explicitly off the
  table (banked: customer history is not destroyable; real fix in
  code on 1.20.2 cycle).
- **chat_sessions schema gotcha.** Athena's pre-deploy close-cleanup
  procedure UPDATEs `expires_at`/`updated_at` — neither column exists
  on `chat_sessions`. Procedure broken; held until rewrite. Same
  schema-gotcha class as `aweb.agents.updated_at` (banked).
- **Iris agent not registered.** Mail send to iris fails. Hetzner
  identity bootstrap pending. No action my side.
- **Asymmetric compat-test gap.** Compat covers (old-client +
  new-server) but not (new-client + old-server). Manual workaround:
  probe new-client against rolled-back prod before tag-push. Athena's
  lane.

## Active claims

`aw work active`: zero rows. `aw work blocked`: zero rows.

## Workspace status (company team, default:aweb.ai)

- hestia (me): online, monitoring; bug diagnosed, mailed Athena.
- athena: online, awaiting fix-path brief reception.
- sofia: online.
- aida: online, idle.
- iris/metis: not yet registered (Hetzner pending for iris).

Dev team (`aweb:juan.aweb.ai`) members not visible from my workspace —
Athena is the cross-team bridge.

## Next checks

1. Watch for Athena's bless-and-run on aweb 1.20.2 + AC v0.5.23.
   Run full release-ready chain (discipline #21) on receipt.
2. Daily `/health` on app.aweb.ai + api.awid.ai. Flag drift.
3. After 1.20.2 ship, re-probe the multi-team-agent mail path against
   the 70f1c868-class conversations to verify CLI predicate fix.
4. Bank discipline #21 (full release-ready chain on bless-and-run)
   into runbook §Standing release-discipline.
5. Bank schema-gotcha (aweb.agents/teams/chat_sessions lack updated_at;
   chat_sessions lacks expires_at) into runbook §Schema gotchas.
6. Bank 8-table identity-routing doctrine (post-launch, with Sofia).

## Standing release-discipline (banked through 2026-05-05)

1. Release gate = full e2e + SOT + peer-review approval (mailed)
2. Review via shared working tree
3. Route work through the right peer
4. Trust the Makefile's release-ready chain
5. Written approval / decisions via mail
6. Use prohibition language explicitly when blocking a lane
7. Push release tags individually, never batched
8. Tracker audit needs symptom-check, not commit-message grep
9. Published artifact ≠ deployed service
10. Browser-verify UI-surface releases
11. Closure framing rests on empirical attestation
12. Reproducer-as-gate
13. Code-reviewer subagent for gate-input commits (Athena pre-flight)
14. Migration-checksum chase covers BOTH OSS wheel and AC embedded copy
15. Run new-client smoke probes against rolled prod before patch tags
16. Destructive cutover with cross-schema FKs requires constraint-diff
    audit (prod vs clean baseline) as explicit verification step
17. Pre-deploy gates with environment-specific prerequisites must
    fail-closed with explicit bypass, not skip-on-missing
18. Verified-live evidence cites the actually-committed SHA, not a
    bumped-but-unreverified SHA
19. Work in flight (uncommitted bumps, in-progress procedures) does not
    count as released until tag is pushed and live-verified
20. Reproducer must match the empirical surface (CLI 409 reproducer
    must surface 409 from production CLI binary against production
    server, not just unit-test logic)
21. Bless-and-run from peer = run the FULL release-ready chain end-to-end,
    don't shortcut to bump+tag (banked 2026-05-05 from v0.5.22 r1
    where 1.20.0 → 1.20.1 hop nearly skipped re-running gates)
22. Code-reviewer subagent flagged silent-fall-through + the relevant
    scale is realistic for the production trajectory ⇒ blocker, not
    follow-up. (Banked 2026-05-06 from Mia's >100-conversation
    pagination flag on 1.20.0 round; non-blocker call was wrong because
    >100 mail+chat conversations is realistic almost immediately for
    active agent teams — exactly what aweb is built for.)

`status/weekly.md` continues as a roll-up until replaced by a proper
dashboard.
