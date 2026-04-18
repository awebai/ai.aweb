# Support (Amy) Handoff

Last updated: 2026-04-18

## Current state

Not yet active. Activation preconditions:

1. aweb-cloud operational (custodial identity for Amy at `aweb.ai/amy`) — in progress pre-launch
2. OSS shippable so `aw init` works for requesters — on track; aweb main is post-v1.9.0
3. Trigger model: claude channels (confirmed with Juan)
4. At least one requester to exist

Amy is contacted by agents, not by humans directly. Reply format
accordingly: lead with the CLI command or doc ref, prose follows.

## Knowledge base status

- `agent-guide.txt` was renamed to `agent-guide.md` in aweb — CLAUDE.md
  now points at the correct path.
- Added `../../docs/support/agent-identity-recovery.md`, synced from
  `../ac/docs/support/` via `make docs-sync` at the ai.aweb root.
  Re-run after any ac-side edits to the runbook.
- Identity docs in aweb are newly rewritten (v1.8.1+): `identity-guide.md`
  and `trust-model.md` are the current sources.

## Escalation cheat sheet

| Topic | Route |
|-------|-------|
| Bugs / UX / features / stories | Avi |
| Identity / namespace / team recovery | Tom first, Randy if slow |
| Engineering / CLI / protocol | Randy |
| Needs `ac` access | Tom |
| Needs `co.aweb` access | Avi |
| Urgent, no response | Juan |

Amy does API-first triage on identity recovery cases but does not
execute dashboard Replace — that is a human action.

## When requesters start arriving, track

- Common questions (patterns suggest doc or product improvements)
- Bugs reported and whether they reached Avi
- Identity recovery cases and whether they reached Tom or Randy
- Feature requests reported and whether they reached Avi
