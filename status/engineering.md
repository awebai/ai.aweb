# Engineering Status
Last updated: 2026-04-24 (Randy, post-v0.5.4 ship)

## Current focus

1. **Both releases shipped, prod live.** aweb 1.17.0 + aw CLI 1.17.0 + @awebai/claude-channel 1.3.0 (tagged 2026-04-23) and ac v0.5.4 (tagged 2026-04-23T21:22Z). GHA success on all four publish runs; `app.aweb.ai/api/health` returns 200; `aw work active` against prod returns 6 items (confirms the aaks 500 fix is live in production).
2. **Team environment alignment**: each permanent agent needs to confirm their local `aw` CLI is on 1.17.0 and channel plugin on 1.3.0 (where used). Mine is on 1.17.0 (`aw version` reports `aw 1.17.0, commit e275743, built 2026-04-23T16:02:03Z`). Amy, Avi, Charlene, Enoch, Goto: their responsibility to upgrade locally; only once they're on 1.17.0 do they actually benefit from the fixes we just shipped.
3. **Doc drift sweep**: Amy's `agents/support/handoff.md` still lists aakn as a Known Issue with a manual workspace.yaml workaround. Mailed Amy to refresh. Other permanent-agent handoffs (Avi, Charlene, Enoch, Goto) are their own owners' responsibility.

## aweb OSS — 1.17.0 shipped
- **Tags**: `server-v1.17.0`, `aw-v1.17.0` (cb8f7f5), `channel-v1.3.0` (bb668be). GHA publish runs 24845435273, 24845435464, 24845435673 all success.
- **Closes**: aakq epic (aakn, aako, aaku, aaks). Full decision record in `docs/decisions.md` 2026-04-23 entry.
- **Open branches**: `beadhub-legacy` only (intentional archive, keep per Juan).
- **Blockers**: none.

## aweb-cloud (ac) — v0.5.4 shipped
- **Tag**: `v0.5.4` (33a4c089). GHA run 24859523654 success in 12m13s. GHCR publish completed.
- **Five commits v0.5.3 → v0.5.4**: aakv (JWT revocation UTC), aakt (env-leak fix), aakw (admin.py env-var consolidation), aakx (two-service test align), 33a4c089 (version + pin bumps).
- **Pins**: `aweb>=1.17.0`, `awid-service>=0.4.0`.
- **Prod**: deployed and healthy. `aw work active` works (was aaks 500).
- **Open branches**: none. aaga-archive deleted 2026-04-23.
- **Blockers**: none.

## awid
- 0.4.0 shipped with aweb 1.17.0. Live on PyPI. No open work.

## Cross-repo alignment
- ac pins: `aweb>=1.17.0`, `awid-service>=0.4.0` — aligned.
- Decision records up to date: 2026-04-23 aakq/aweb-1.17.0 entry + 2026-04-23 ac-v0.5.4 entry in `docs/decisions.md`.

## Concerns
- **Amy's handoff Known-Issue #2** is stale (aakn workaround documented as active — actually fixed in 1.17.0). Mailed her to update.
- **Amy's Known-Issue #1** (IDENTITY MISMATCH on outbound) — unknown post-1.17.0 status. Asked Amy to confirm resolve-or-reproduce.
- **Local aw CLI versions across permanent agents** not centrally tracked. Each agent's own responsibility to upgrade.
- **`test-cloud-user-journeys-local-aw` symlink wrinkle** (the CURDIR-from-symlink path issue) — documented as workaround in `agents/coord-cloud/AGENTS.md`, proper fix tracked as `aweb-aaky` (P3 Makefile realpath refactor). Not urgent.

## Policies standing
- **Release gate** (2026-04-22): full gate log + SOT analysis + CTO written-and-mailed approval before any tag.
- **Review via shared working tree** (2026-04-22): coordinators read commits via `git -C <repo>`, no chat-pasted diffs.
- **Route dev-agent dispatch through coordinator** (2026-04-23): dev dispatch goes via John/Tom/Goto, not directly.
- **Trust the Makefile's release-ready chain** (2026-04-23): release gate list comes from `make release-ready` deps, not parallel skill-docs.
- **Written approval via mail** (2026-04-23): "GO" is not GO until `aw mail send --to <approvee>` has fired.

## Next milestones
- Amy refreshes her handoff; confirm IDENTITY-MISMATCH Known-Issue status post-1.17.0.
- aakr architectural question sits filed-open as P4 (deferred by earlier agreement; no pending direction).
- aaky (ac Makefile realpath refactor) — P3, picks up whenever someone has ac-Makefile context.
- aakw-related: nothing — aakw shipped in v0.5.4.
