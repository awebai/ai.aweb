# CEO Handoff

Last updated: 2026-04-28 20:43 CEST (Avi, repo + company-agent study pass)

## Where we actually are

The product is live and the previous launch-blocker state is stale.

- **aweb OSS**: local sibling repo is at main `2477dea`; latest release
  tags include `server-v1.18.6`, `aw-v1.18.6`, `awid-v0.5.2`, and
  `awid-service-v0.5.2`. Recent work centers on trust contract,
  identity-equivalent recipient binding, and fail-closed messaging.
- **aweb-cloud**: production health reports `release_tag=v0.5.9`,
  `git_sha=48e0e3ad`, `aweb_version=1.18.6`, awid connected, and
  coordination API mounted.
- **awid registry**: production health reports `version=0.5.2` with
  Redis/database/schema healthy.
- **KI#1**: closed per latest support/cloud handoffs. Amy's 4-of-4
  attestation and Tom's second-shape probe satisfied the empirical
  closure policy on 2026-04-27. Old engineering.md still says launch
  blocked; do not trust it until Randy refreshes it.

## What changed this wake-up

- Answered Amy's support-runbook question on internal-alias-only rename:
  classification **(c) intentional today, possibly reconsidered**.
  Alias-only rename is not supported today; archive + create new is the
  customer-facing path, with history continuity tradeoff.
- Sent Randy an async status request because he is offline and the prior
  chat thread was closed.
- Tried to check with comms via `aw chat send-and-wait charlene`; it
  failed with `agent not found: charlene`. Comms handoff and outreach
  status are still 2026-04-11-era. This is an operating-system bug, not
  just a stale file.
- Rewrote `status/product.md` around current reality: v0.5.9 live,
  KI#1 closed, distribution should restart, and today's Juan-directed
  focus is the agent-first company operating model.

## Agent-first company study notes

Current company structure is conceptually good but operationally split
between markdown and aweb:

- Permanent roles exist: CEO, CTO, Comms, Board, Support, and repo
  coordinators.
- Wake-up routines are explicit and mostly right: pull, read north-star
  docs, read status/handoff, check aweb messages, do work, update status
  and handoff, commit/push.
- The weak point is that active company work is not consistently modeled
  as aweb tasks/claims. Status files say what matters, but they are not
  a live work queue.
- Agent identities are not fully aligned with the role map. Example:
  `charlene` is documented as Comms, but not resolvable in the active
  workspace.
- Board oversight correctly checks claims against git/outreach reality,
  but weekly status is stale and outreach has not started.

My initial product read: the company should organize around the same
primitives aweb sells:

1. **Tasks are the source of active work**, not status prose.
2. **Claims are the conflict-avoidance mechanism**, including for
   strategic/comms/support work, not only code.
3. **Handoff files are durable memory**, not the work queue.
4. **Status files are published state**, not private scratchpads.
5. **Mail is for async decisions and audit**, chat for blocking
   questions, and decision records for durable changes.
6. **Every non-trivial engineering cycle still needs builder+reviewer**;
   for company/process work, the equivalent is author+reviewer or
   proposer+approver.

## Current risks

- Distribution remains at zero published/outreach actions even though the
  product is live. This is now the largest company risk.
- Comms agent identity/process appears broken or incomplete. If Charlene
  cannot be reached, outreach cannot become a reliable company function.
- Engineering status is stale relative to production and support handoffs.
  Randy needs to refresh it so board/comms are not reading a launch-blocked
  world that no longer exists.
- `ac` has active uncommitted work by another agent (Mia, aweb-aalr);
  do not touch or normalize it from CEO context.
- `aweb` has an untracked doc `docs/awid-ensure-team-endpoint.md`; treat
  as someone else's work.

## What to check FIRST on next wake-up

1. Did Randy reply with refreshed engineering status, and did
   `status/engineering.md` move past the stale 2026-04-25 aalf state?
2. Is `charlene` supposed to exist as an aweb identity? If yes, fix or
   escalate the missing identity; if no, update docs/status to the real
   comms alias.
3. Did Juan decide whether the first distribution asset is the blog post
   or collision video?
4. Did any outreach brief or outreach history entry appear?
5. Did the agent-first operating model get turned into a concrete doc or
   task set?

## Reference map

- **ai.aweb**: company docs, status, publishing, permanent agents.
- **aweb** (`../../../aweb`): OSS coordination core, CLI, awid, channel.
- **ac** (`../../../ac`): hosted app, dashboard, auth, billing, cloud
  bootstrap, mounted OSS integration.
- **co.aweb** (`../../../co.aweb`): private outreach and keys. Do not
  put contact names or approach details in public files.
