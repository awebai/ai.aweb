# Athena Handoff
Last updated: 2026-06-01

## Purpose of this file
This is the crisp restart handoff: only current state, open loops, and what to check first. Historical detail now lives in `logbook.md`.

## Identity / operating context
- You are Athena, engineering bridge between:
  - dev/code team `aweb:juan.aweb.ai` (default active team)
  - company team `default:aweb.ai` (use `--team default:aweb.ai`)
- Code repos are symlinked here as `aweb/` and `ac/`. Use `git -C aweb ...` and `git -C ac ...`.
- For feature work: devs author, Athena scopes/reviews/lands; Hestia ships. For non-feature diagnostics/tests, Athena may author directly with second-voice review.

## Check first on restart
1. `git pull` in `ai.aweb`, `aweb`, and `ac` as needed.
2. `aw mail inbox`, `aw chat pending`, plus company team inbox/pending.
3. Check for Hestia response on the CLI hotfix handoff (subject: hosted cert-only add-worktree / `aw-v1.26.4`).
4. Check whether any pmbah cleanup/path recovery follow-up is still open before running any pmbah `aw workspace status`.

## Current open loops

### 1) CLI hotfix: hosted cert-only `aw workspace add-worktree`
- Root cause: bootstrap-created hosted worktree parents can be valid cert-only members (team cert + local signing key, no local team controller key, no workspace API key). Generic `aw workspace add-worktree` only handled local-team-key or API-key authority and failed with `no local team key and no workspace API key`.
- Pushed aweb `a3fbc47` (`cli: support hosted cert-only add-worktree`). Authority order is now:
  1. local team controller key;
  2. stored workspace API key;
  3. hosted cert-only current workspace via `addWorktreeViaPrimaryInvite`.
- Pushed AC `a6629b8b` test-script coverage only; no AC production release needed for this hotfix.
- Validation/approvals:
  - Athena: focused tests, full `cd aweb/cli/go && go test ./cmd/aw -count=1`, `bash -n ac/scripts/e2e-cloud-user-journey.sh`, focused Docker hosted-autonomous journey (`ALL PASSED: 39 tests`).
  - Dave approved.
  - Grace approved ship-OK. Her full unfiltered AC cloud journey hit unrelated registry timestamp-skew later; track separately as gate reliability debt, not a blocker.
- Hestia production handoff sent as CLI-only `aw-v1.26.4` candidate from aweb `a3fbc47` (company mail message `bdfb8c65-c986-4c55-9d91-544f618e4489`).
- Next: wait for Hestia publish/tag/live verification or gate issue.

### 2) pmbah incident / cleanup regression
- Juan’s pmbah coordinator saw `403 Agent not connected`; not quota.
- Hestia DB probe found coord/dev agents/workspaces soft-deleted around `2026-05-28 10:11:33 UTC` after stale workspace paths under `/Users/juanre/prj/pmh/...` made cleanup classify them as gone.
- Hestia undeleted after Juan authorization. Local files/keys existed. Be cautious with pmbah `aw workspace status` until server workspace paths are known-correct; stale path cleanup can re-delete.
- Related hotfix above fixes add-worktree from hosted cert-only parents; separate from cleanup auto-delete aggressiveness.

### 3) Site/frontend updates
- Olivia handled site/frontend lane.
- Live verified:
  - home/developers swap: `/developers/` aliases to `/`; new `/mcp/`; tagline shortened.
  - `/llms.txt` mirrors home with pricing and new `/mcp/` + `/orchestration/` teasers.
  - `/mcp/llms.txt` has no pricing and no `/developers/` refs.
  - home eyebrow now `Open network · Opt-in E2EE · MIT`.
- No action unless Olivia/Hestia reports a live issue.

### 4) E2EE release wave
- Keep product/security boundaries:
  - CLI plaintext default remains customer-safe posture unless Juan changes default decision.
  - `--e2ee` explicit opt-in and fail-closed.
  - Self-custodial `encrypted_v2` is E2EE.
  - Hosted custodial MCP/dashboard messaging is managed/server-readable, not E2E.
  - Do not claim live explicit E2EE works against deployed app unless server/AWID compatibility is deployed.
- Final coordinated E2EE release still depends on Juan default-vs-opt-in decision and package sequencing: publish/pin new aweb package before AC release.

### 5) Hermes / GBrain integration context
- GBrain read: optional memory/knowledge layer, not core Stage-1 infra.
- Hermes read: persistent agent runtime/gateway; Dave’s aweb platform plugin prototype reviewed green for external plugin repo. Key invariants: shell through `aw`; exact chat `--session-id`; use `--body-file`; mark read only after successful visible send.
- Real-world Hermes readiness would require separate live app.aweb.ai + real workspace + model/provider smoke.

## Current repo state expectation
- `aweb` main should include `a3fbc47`.
- `ac` main should include site changes through `92860b93` and later `aeb6d0f8`/`c4d28ebe`/`92860b93` sequence as deployed by Olivia/Hestia, plus `a6629b8b` coverage. Pull before relying on exact head.
- `ai.aweb` handoff is now short; historical prior handoff copied to `logbook.md`.

## Do not forget
- Never call hosted custodial messaging E2E.
- Do not relay company-team internals verbatim to the public dev team.
- For any substantial code you author directly, get second-voice review before release handoff.
