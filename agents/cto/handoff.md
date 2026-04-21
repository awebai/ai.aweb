# CTO Handoff

Last updated: 2026-04-21

## Current state

### aweb OSS — shipping
- v1.16.0 server + CLI, awid-service v0.4.0.
- Six server releases and three awid releases since 2026-04-11.
- Identity/address split (2026-04-18 decision) complete on both aweb and ac sides.
- Per-membership addresses live (v1.16.0) — the `aw init` for a second team auto-provisions a second workspace; the whole aweb.ai/amy activation today exercised this.

### aweb-cloud (ac) — shipping
- v0.5.3, pinned to `aweb>=1.16.0` and `awid-service>=0.4.0`.
- Dashboard nav redesigned; admin cleanup tools are soft-delete + renamed to "retire".
- Replace/Archive multi-address policy partially enforced (scoped to managed-assigned addresses for this release).

### awid
- 0.4.0. Cert member-address validation live. DID registration split from address binding. Address registration idempotent. Migrations consolidated into 001_registry.sql.

### Team structure — reality vs docs
- Git log: every recent commit on both aweb and ac is authored by Juan with Claude Opus co-authorship. Branches (`henry`, `ivy`, `jack`, `bob`, `frank`, `leo`, `eve`) are workstream sandboxes inside Claude Code sessions.
- `docs/team.md` describes a coordinator-oversees-ephemeral-devs structure that git history doesn't reflect. Coordinator handoffs (John/Tom/Goto) are stale to 2026-04-11. Unresolved — worth a conversation with Juan.

## Active concerns

- **runTeamSwitch bug (aweb-aakn, P2)**: Amy reproduced today. Real fix documented (add workspace-cache update after SaveTeamState in `cli/go/cmd/aw/id_team.go:runTeamSwitch`).
- **Branch preservation pending decision**:
  - aweb: `beadhub-legacy` (187 ahead, 1227 behind) — "legacy" in name suggests intentional preservation.
  - ac: `aaga-archive` (107 ahead, 1171 behind) — "archive" in name same.
  - ac: `frank-docs` (8 ahead, 259 behind) — pricing change already re-landed on main via a different commit; remaining site content reshuffled. Probably drop, but not yet deleted.
- **docs/vision.md deletion aftermath — done**: 22 references across 10 files swept 2026-04-21. Wake-up routines now point at `status/engineering.md` / `status/product.md` for current focus; invariants/user-journey/value-proposition remain the north-star reads. Each status file gained a "Current focus" section (3–5 lines, rewritten every wake-up).
- **Cross-repo is aligned** for now. Watch: per-membership address features on the cloud side are only partially exercised yet (e.g. Replace/Archive scope explicitly narrow).

## Actions taken this wake-up (2026-04-21)

- Pruned stale branches: aweb `henry`, `ivy`, `jack`, `fix/apikey-bootstrap-rebuild`, `deploy-awid-landing`; ac `bob`, `deploy-landing`, `eve`, `frank`, `leo` (remote + local).
- Committed `docs/vision.md` deletion (ai.aweb).
- Committed formatter pass on `docs/team.md`, `docs/capabilities.md`, `docs/aweb-high-level.md` (no content change).
- Committed repo-path addition to `agents/coord-aweb/AGENTS.md`.
- Swept all `vision.md` references across 10 files; pointed wake-up routines at `status/engineering.md` / `status/product.md` instead. Each status file gets a "Current focus" section.
- Updated `status/engineering.md` with Current focus section (was stale to 2026-04-10).
- Confirmed Amy's report that the `aw id team switch` bug (aweb-aakn) is real: diagnosis in `id_team.go:408` correct.

## What to check FIRST on next wake-up

1. Has Juan responded on the preserved branches (`beadhub-legacy`, `aaga-archive`, `frank-docs`)?
2. Did the aweb-aakn runTeamSwitch fix ship (or was it deprioritized)?
3. Are the new "Current focus" sections actually being rewritten each wake-up (engineering.md, and did Avi start one in product.md)?
4. Coordinator handoffs still stale? If yes, raise with Juan whether that structure is real or aspirational.

## Key context

- Crypto identity migration is complete end-to-end. The 2026-04-06 decision has landed in full.
- The identity/address split (2026-04-18) is the most subtle recent architectural change — the CLI/cloud flow is two-step now (register_did then bind address) with a local partial-init file for resume-from-partial. Watch for anyone re-bundling these in future work.
