# Engineering Status
Last updated: 2026-04-21 (Randy)

## Current focus

1. **Ship the runTeamSwitch fix (aweb-aakn, P2)** — Amy reproduced today during `aweb.ai/amy` activation. Small patch in `cli/go/cmd/aw/id_team.go:runTeamSwitch`. Pre-launch severity; doesn't block v1.16.0 users who only have one team but is a paper-cut for anyone with multiple addresses (which is now a real flow).
2. **Keep cross-repo pin discipline** — ac moved to aweb>=1.16.0 today; watch that per-membership address behavior (new in 1.16.0) gets exercised by ac integration tests, not just pinned.
3. **Coordinator handoffs unfreshed since 2026-04-11** — decide with Juan whether the coordinator structure is real or aspirational before asking John/Tom/Goto to update.

## aweb OSS
- **Status**: Shipping. v1.16.0 server + CLI, awid-service v0.4.0.
- **Recent releases** (since 2026-04-11): 1.11.0, 1.12.0, 1.13.0, 1.14.0, 1.15.0, 1.16.0; awid 0.3.0, 0.3.1, 0.4.0.
- **Landed**:
  - v1.16.0 / awid 0.4.0 — per-membership address model. `aw id namespace assign-address`, CLI cert `--address` flag, multi-team inbox cert-auth fix, awid validates member-address ownership on cert registration. 123 e2e tests including per-membership address phase.
  - v1.15.0 — identity-auth messaging enrichment + e2e ephemeral mail journey.
  - v1.14.0 — ephemeral local routing addresses with review-blocker fixes.
  - v1.13.0 — block local address policy bypass, allow cross-org address messaging, `chat_participants.address` column.
  - v1.12.0 — persist chat/mail sender addresses at write time, `from_address` on messages.
  - v1.11.0 — cross-team chat address rendering, registry-backed TOFU refresh, trust verified registry identities over stale pins.
  - awid 0.4.0 — cert member-address validation; 0.3.1 rate-limit env for e2e/local; 0.3.0 single consolidated `001_registry.sql`, idempotent address registration, address fields dropped from `did_aw_mappings` (identity/address split complete per 2026-04-18 decision).
- **Open branches**: `beadhub-legacy` only (see Concerns).
- **Blockers**: None.

## aweb-cloud (ac)
- **Status**: Shipping. v0.5.3, depends on aweb>=1.16.0 and awid-service>=0.4.0.
- **Recent releases** (since 2026-04-11): 0.4.22 → 0.4.24 → 0.5.0 → 0.5.1 → 0.5.2 → 0.5.3, plus aweb-dep bumps tracking every aweb minor.
- **Landed**:
  - Migrations 016 (timestamps→timestamptz), 017 (user soft-delete active uniques), 018 (user email/username partial unique repair).
  - Identity/address split adoption: `registry_client.register_did` called from `init.py`, `agent_lifecycle.py`, `middleware/auth_bridge.py`, `admin_support.py`.
  - Replace/Archive multi-address policy partially enforced: `agent_lifecycle.py` explicitly refuses non-managed replacement ("Replacement is only available for managed assigned addresses in this release"). `list_did_addresses[0]` cleanup done at the surveyed site.
  - Dashboard nav redesigned: Connect + Identities replace Agents + Identities.
  - Admin cleanup tools reworked to soft-delete and renamed "cleanup" → "retire".
  - Event-feed filtering (epics aakj, aakk): Monitor feed filters agent.online/offline and SSE control events.
  - Cloud migrations collapsed into initial schema; embedded aweb schema sync; production db reset targets added.
  - Pricing updated: Pro $49→$25, Business $149→$250 (landed on main; frank-docs branch's version is superseded).
- **Open branches**: `aaga-archive`, `frank-docs`.
- **Blockers**: None.

## awid
- Shipped under aweb repo. See aweb OSS above — awid-service 0.4.0 current.

## Cross-repo alignment
- ac pin tracks aweb: `aweb>=1.16.0`, `awid-service>=0.4.0`.
- 2026-04-18 decisions (identity/address split, idempotent address registration, resume-from-partial bootstrap, Replace/Archive multi-address policy) all landed on both sides.

## Concerns
- **runTeamSwitch bug (aweb-aakn, P2)**: `cli/go/cmd/aw/id_team.go:408` updates `teams.yaml` + served cert but not `workspace.yaml.active_team`. Coordination commands continue using the old team until workspace.yaml is edited by hand. Reproduced today activating `aweb.ai/amy`. Fix small: after `SaveTeamState`, also load workspace.yaml, call `applyTeamStateToWorkspaceCache`, `SaveWorktreeWorkspace`. Workaround documented in `agents/support/handoff.md` Known Issues #2.
- **Process drift**: coordinator handoffs (John/Tom/Goto) have not been updated since 2026-04-11. Git history shows all commits authored by Juan with Claude Opus co-authorship — the "coordinator oversees ephemeral devs" structure described in `docs/team.md` isn't what the git log reflects. Work flows through branches (`henry`, `ivy`, `jack`, `bob`, `frank`, `leo`, `eve`) driven in Claude Code sessions. The stale ones have been pruned today.
- **Branch preservation**: `beadhub-legacy` (aweb, 187 ahead / 1227 behind) and `aaga-archive` (ac, 107 ahead / 1171 behind) are named like intentional archives; preserved pending Juan confirmation. `ac/frank-docs` has 8 commits, but the pricing change already landed on main via a different commit; remaining content is site-reshuffle work now superseded.

## Next milestones
- Ship the runTeamSwitch fix (aweb patch release).
- Decide on remaining branches (beadhub-legacy, aaga-archive, frank-docs).
