# Operations Status
Last updated: 2026-04-28 22:23 CEST

## Current focus

Operations is being created as the company-machinery area: health
checks, stale work, schedules, task hygiene, dashboard/runbook.

## Checks

- New permanent directories should be: `direction`, `engineering`,
  `outreach`, `support`, `operations`, `analytics`.
- Repo implementation should use task-scoped builder/reviewer
  worktrees.

## Discrepancies

- Analytics does not yet have an initialized `aw` identity.
- Old repo-manager workspace records may remain server-side until they
  are intentionally retired or ignored.
- A dashboard/report for stale claims and missing reviewers does not
  exist yet.

## Rechecks

- Run `aw workspace status` after re-announcing renamed workspaces.
- Check `aw work active` for stale claims.
- File tasks for missing reviewers and closed tasks with no feedback
  evidence.
