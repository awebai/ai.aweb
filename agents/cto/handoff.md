# CTO Handoff

Last updated: 2026-04-22

## Current state

### Active epic: aweb-aakq (Collapse duplicate SoTs for active-team and active-address)

Filed 2026-04-21. 9 subtasks (.1–.9). Grace (juan.aweb.ai/grace) owns implementation; John (juan.aweb.ai/john, coord-aweb) owns code review.

- **.1, .2 shipped** on main (commits fcbcc00, 05c46b2): channel-plugin + CLI precedence flips. aako-half is fixed pending the 1.17.0 / channel 1.3.0 release.
- **.3, .4 in flight, NO-GO from John**: Grace's initial refactor deleted `migrateTeamStateFromWorkspace` from `LoadTeamState`. That's the upgrade bridge for users on 1.11.0-1.15.0 with only workspace.yaml. Grace is reinstating the migration path; workspace.yaml.active_team parsed for migration only, not runtime authority; positive test asserts upgrade flow works. John delta-reviews on her signal.
- **.5, .6** (runTeamSwitch cleanup, doctor migration) depend on .3/.4.
- **.7** (e2e): spec tightened 2026-04-22 after John flagged that Phase 12d's `aw init`-after-switch masks aakn. Target is `scripts/e2e-oss-user-journey.sh` Phase 12d or 12e; must-fail-on-1.16.0 + must-pass-on-full-Shape-A as acceptance.
- **.8** (release): acceptance now requires `make test-e2e` green per Juan's 2026-04-22 standing release-gate policy.
- **.9** (follow-up from John's review of .2): surface cert-load errors in finalizeWorkspaceSelection instead of silent fallback. P2, blocks .8.

### Policies codified today

- `docs/decisions.md` entry (commit 8f5baf3): release gate — no release of anything without full e2e user journey green. Standing rule, all repos, all agents.
- `agents/coord-*/AGENTS.md` + `agents/cto/AGENTS.md` (commit de9d11c): review workflow uses the symlinked shared working tree (`git -C aweb/ac/awid log|show`), not chat-pasted diffs. Dev commits locally, coordinator reads from their own agent dir, chats go/no-go, dev pushes on approval.

### New open question (not blocking anything)

John surfaced a follow-on architectural concern: teams.yaml.memberships and workspace.yaml.memberships share four fields (team_id, alias, cert_path, joined_at). Same class of drift risk as aakq.active_team, lower impact because nothing routinely mutates them after join. I asked John to file as a P4 task-candidate (not epic) on the aweb tracker, with both framings open (drop-from-teams.yaml vs. workspace-becomes-derived-view). Architectural commit needs Juan buy-in before spec-writing. John writes the task.

### Team dynamics observed today

- 2+2 loop functioning: Grace and John both independently caught the migration-path break in aakq.3/.4.
- John's review rigor: caught a real spec defect (aakq.9, cert-load error swallow), verified architectural claim I made against awid-sot.md (found I was wrong in one direction — cross-namespace membership is designed-for, not validation-blocked), flagged the membership-field overlap one level up.
- Grace's TDD discipline: failing tests first on every subtask; scope-clean commits; honest commit messages (explicitly called out the adjacent helpers.go fix in .2).
- Both agents respect the aweb repo convention (no WIP branches, stay on main, self-review + sync).

## Active concerns

- **Migration bridge for aakq.3/.4**: Grace is restoring `migrateTeamStateFromWorkspace`. Must verify on delta-review that the second LoadTeamState after upgrade still works (teams.yaml actually written to disk, not just in-memory).
- **aakq.8 release gate**: coordinator (John) must own verifying `make test-e2e` green before the release commit lands. Not yet set up; note to raise with John when we're closer to .8.
- **Coordinator reality**: John is running and working well. Tom (coord-cloud) and Goto (coord-awid) status unknown — haven't seen activity from them in this session. When aakq work touches ac (it doesn't directly; only ac's aweb dep pin bumps), Tom needs to be online. Flag if we hit .8 without Tom around.

## Actions taken this session (2026-04-22)

- Filed epic aweb-aakq + 8 subtasks + all dependencies.
- Added aakq.9 after John's review of .2 surfaced the cert-load error swallow.
- Tightened aakq.7 and aakq.8 descriptions after John identified Phase 12d masks aakn.
- Committed `docs/decisions.md` entry for Juan's release-gate policy (commit 8f5baf3).
- Committed review-via-symlink workflow corrections across four AGENTS.md files (commit de9d11c).
- Briefed John (now coord-aweb), handed off full review authority to him starting .3.
- Responded to Grace's pre-commit question on .2 (helpers.go sanitized-return fix), approved.
- Responded to John's architectural check on domain/address consistency (cross-namespace membership is designed-for; saved as project memory).
- Responded to John's NO-GO flip (Grace adjusting; reiterated the removal-of-compat-shim is Juan-level framing).
- Asked John to file the membership-field overlap observation as P4 task-candidate.

## What to check FIRST on next wake-up

1. `aw task list | grep aakq` — status of all 9 subtasks. Expected: .1, .2 closed; .3, .4 open or in_progress pending Grace's migration-path fix.
2. `git -C aweb log --oneline -10` — what shipped on main today (after this handoff writes).
3. John's handoff — any delta-review he did on Grace's adjusted .3/.4.
4. Grace's status in the task tracker — any new subtask claims.
5. Any new aweb-aak* tasks John filed for the membership-field overlap.

## Key context

- aakq is Shape A (architecturally clean, correct over fast), not Shape B (read-through cache). Juan chose correct.
- Per-membership address model (aweb 1.16.0, 2026-04-21 decision) is what made aakn/aako user-visible. Same class of bug exists latent in the membership-fields overlap (flagged by John).
- Cross-namespace team membership is designed-for: cert.member_address is NOT constrained to team namespace. When reviewing anything that equates team-namespace with member-address, check it holds for cross-namespace members (memory: aweb_cross_namespace_membership.md).
- Review workflow: shared working tree via symlink, no diff-paste (memory: feedback_review_via_symlink.md).
- Juan's standing release-gate: full e2e user journey green before any release. Applies to every repo (decisions.md 2026-04-22).
