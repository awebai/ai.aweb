# Engineering Status
Last updated: 2026-04-28 22:23 CEST

## Current focus

1. **Engineering is the permanent integrity area.** It owns
   architecture, release discipline, cross-repo alignment, and
   identity/protocol correctness.
2. **Repo implementation should use task-scoped builder/reviewer
   pairs.** Permanent repo-manager agents are no longer the default
   operating shape.
3. **Release claims still need verified-live evidence.** Health/version
   checks, smoke/browser probes, and user/support confirmation remain
   the strongest close loops.

## Active engineering work

- `aweb-aals`: company operating model reorganization.
- `aweb-aals.2`: instruction sweep needs reviewer pass before close.
- `aweb-aals.6`: first real task-scoped builder/reviewer worktree
  cycle.
- `aweb-aals.7`: make builder/reviewer/feedback fields native in `aw`
  tasks after dogfooding the prose contract.
- Current engineering/release work still needs conversion into queryable
  tasks under `aweb-aals.1`.

## Release/live state

- OSS observed at aweb 1.18.6-era local main with recent tags
  `server-v1.18.6`, `aw-v1.18.6`, `awid-v0.5.2`, and
  `awid-service-v0.5.2`.
- Cloud observed live at `release_tag=v0.5.9`,
  `aweb_version=1.18.6`.
- awid observed live at `version=0.5.2`.

## Risks

- Existing handoffs still contain historical repo-coordinator language;
  active instructions now prefer spawned worktree pairs.
- Analytics has no initialized workspace identity yet.
- Operations needs to turn stale-claim/live-check monitoring into a
  concrete dashboard or repeatable report.

## Next checks

- Verify `aw workspace status` after new directory names are
  re-announced.
- Convert active engineering priorities into tasks with builder,
  reviewer, and feedback signal.
- Review the new operating model before closing `aweb-aals.2`.
