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
- Substantial tasks should include the `Work contract:` block from
  `docs/agent-first-company.md`.

## Discrepancies

- Analytics does not yet have an initialized `aw` identity.
  Tracked by `aweb-aals.4`.
- Old repo-manager workspace records may remain server-side until they
  are intentionally retired or ignored. Tracked by `aweb-aals.5`.
- A dashboard/report for stale claims and missing reviewers does not
  exist yet. Initial inventory is `docs/company-dashboard.md` and
  task `aweb-aals.3`.
- Current `aw` task metadata does not expose builder/reviewer or
  feedback fields natively; operations must parse task notes until the
  tool grows first-class fields. Tracked by `aweb-aals.7`.

## Rechecks

- Run `aw workspace status` after re-announcing renamed workspaces.
- Check `aw work active` for stale claims.
- File tasks for missing reviewers and closed tasks with no feedback
  evidence.
- File tasks for malformed or missing `Work contract:` blocks.
- Watch `aweb-aals.6` for the first real builder/reviewer worktree
  dogfood cycle.
