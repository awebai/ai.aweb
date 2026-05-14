# Metis Handoff

Last updated: 2026-05-14 11:25 CEST

## Read this first

You are Metis, the analytics role on the six-role peer team. You
produce signal — you don't decide priorities. Read `AGENTS.md` (in
this dir) for the role description and `../../docs/team.md` +
`../../docs/agent-first-company.md` for the operating model.
Decision-record check: top of `../../docs/decisions.md`.

## Identity status

This workspace HAS an identity now: `metis` alias on `default:aweb.ai`
team, developer role. (Prior handoff said this was pending; it's
done.) You can mail and chat.

## Current work — Bertha pipeline takeover

**Juan redirect 2026-05-10**: "we are going to task metis, who is
responsible for analytics, for the regular check of the database…
she will need to design and write admin entrypoints to do the
tasks." Hestia briefed me with the full operational picture (mail
e8bf1afe, conversation b690dca3) and continues running the
session-cron stop-gap until cutover. Acked back: c8e94011.

The two pipelines:

1. **Daily sign-up export** — previous-26h sign-ups with email →
   pipe-separated batch → `aw mail send --to bertha` daily 08:13
   CEST. Authority: Juan 2026-05-08.
2. **Hourly multi-agent milestone check** — detect external
   customers crossing 2+ same-user agent coordination on any of
   mail / chat / contacts / tasks / task_claims; alert Bertha on
   first-cross. Authority: Juan + Eugenie via Bertha 2026-05-08
   (chat 4d4383fc / 2901b3a5).

Hestia's stop-gap files:

- `agents/hestia/.claude/skills/daily-signup-export/SKILL.md`
- `agents/hestia/.claude/skills/multi-agent-milestone-check/SKILL.md`
- `agents/hestia/.claude/skills/multi-agent-milestone-check/check.py`
- `agents/hestia/.claude/state/multi-agent-alerted-users.json`
  (currently empty, last_check 2026-05-10T10:29Z after my dry-run)

Existing infrastructure I'll extend (in `../../../ac/`):

- `aweb-admin` Click CLI at `backend/src/aweb_cloud/admin.py` (4881
  lines; has DATABASE_URL resolution, `AdminDB` shared-pool with
  cloud/server/aweb schemas, --dry-run conventions, audit options).
- `services/admin_analytics.py` (462 lines; daily-active-workspace
  + message analytics; window helpers).
- `routers/admin_analytics.py`, `admin_support.py`, `admin_activity.py`
  surfaces if we want HTTP later.
- Write-path pattern: `SET LOCAL default_transaction_read_only = off`
  inside a tx (used by retire/delete commands).

Recommended architecture (proposed to Juan; awaiting his call):

- Extend aweb-admin with `daily-signup-export` and `milestone-check`
  commands, not a new aweb-analytics CLI.
- Lift SQL into `services/admin_analytics.py` (testable, reusable).
- New migration for `aweb_cloud.analytics_milestone_alerts`
  (user_id uuid PK, alerted_at timestamptz).
- CLI emits structured stdout; thin wrapper script does
  `aw mail send --to bertha`. Keeps CLI testable, doesn't bind to
  an aweb identity.
- Schedule via launchd plists on altair.local for cutover.
- Mail-from identity for Bertha: lean metis.

Open questions for Juan (pinned in `../../status/analytics.md`):

- Run-host (altair launchd vs AC-server-side apscheduler/cron).
- DB write-path connection shape (existing pattern: relax read-
  only inside a txn via `SET LOCAL default_transaction_read_only
  = off`; the retire/delete commands use it at admin.py:1138,
  1199, 1846). Settled from the code side.
- Mail-from identity to Bertha.
- Cutover handshake (parallel-run vs hard cutover).

## Queued P1 — Athena's OAuth-onboarding signal (2026-05-14)

Mail 7223708e, conversation 7fb1d95b. Athena flagged the
load-bearing signal for the post-OAuth consumer-onboarding
investment (MCP create-invite tool + welcome guide + serverInfo
.instructions + consent-page banner + email already in v0.5.32):

> Fraction of new aweb-MCP-OAuth connections that produce an
> invite-link creation within N minutes.

- Numerator: new `mcp_oauth_grants` rows that trigger downstream
  `consumer_contact_invites` row within window N (N=15 initial).
- Denominator: new `mcp_oauth_grants` rows in the period.
- Period: daily rolling.
- Surface: company-dashboard signal-inventory entry.

Empirical-zero-tolerance: until instrumented, no team claim that
the OAuth onboarding "is working" should land. Acked 579c20ec.

This is queued behind the Bertha-pipeline cutover so I have one
durable scheduling pattern in place before adding new signal
entrypoints under it. If the OAuth investment ships and the
empirical-zero-tolerance line is about to bite, the queue
re-orders.

## What to check FIRST on next wake-up

1. `aw mail inbox` and `aw chat pending` — Juan's design call
   probably came back via mail.
2. Has Juan answered the four open questions above? If yes,
   create aw task and start authoring. If no, follow up.
3. Hestia's session crons — still firing or dead with her
   session? If dead, the daily-signup-export and milestone-check
   have silently stopped; that itself is signal worth flagging
   to Bertha/Juan.
4. Read `../../status/operations.md` and `../../status/product.md`
   for any new ops/direction state.
5. If Bertha pipeline is unblocked and the OAuth investment is
   close to shipping, check whether the queue should re-order
   per Athena's note.

## Pre-existing instrumentation gaps (still open, not yet tasked)

- No event for first successful coordination (Stage 2 threshold).
- No conversion query from outreach-action timestamp to signup
  timestamp.
- No queryable surface over support patterns.
- No browser/edge telemetry beyond Render request stats.

These get follow-up tasks once the Bertha pipeline cutover is
done AND Athena's OAuth signal is in place.

## Prior context

Prior handoff is in git history (2026-04-30 placeholder; identity
not yet bootstrapped, no active work).
