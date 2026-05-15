# Analytics Status
Last updated: 2026-05-15 14:00 CEST

## First signal brief shipped

`agents/metis/briefs/2026-05-15-adoption-state-first-brief.md`
closes aweb-aals.4. Headline: external signup rate steady at 2-5/
week for last 7 weeks; no observable lift from pain-narrative deploy
2026-05-13 22:28Z in first 36h; mcp_oauth_grants table has counting
trap — true external population is n=1 (2 of 3 "external" grants
are Juan testing), so OAuth-onboarding-investment baseline is
effectively absent. Empirical-zero-tolerance framing: do NOT claim
"0% conversion"; correct framing is "insufficient grant volume to
compute conversion rate; will re-baseline at n>=10."

## Current focus

**Bertha pipeline ownership transfer (Juan redirect 2026-05-10) — still
blocked on Juan's design call.** Hestia handed off the daily sign-up
export and hourly multi-agent milestone check to me 2026-05-10
(mail e8bf1afe, conversation b690dca3). I proposed the admin-
entrypoint architecture back to Juan the same day, with three pinned
open questions. As of 2026-05-14 there is no answer in mail or in
this conversation. Hestia's session crons presumably still firing
(or dead with her session — uncertain; needs follow-up).

**Queued P1: post-OAuth onboarding signal (Athena mail 7223708e,
2026-05-14)**. Investment shipping in the consumer-onboarding arc
(MCP create-invite tool + welcome guide + serverInfo.instructions
+ consent-page banner; email already in v0.5.32). Load-bearing
signal Athena flagged: fraction of new aweb-MCP-OAuth connections
that produce an invite-link creation within N minutes (N=15
initial). Numerator = new `mcp_oauth_grants` rows that trigger
a downstream `consumer_contact_invites` row within window N;
denominator = new `mcp_oauth_grants` rows in the period; period
daily rolling. Empirical-zero-tolerance: until instrumented, no
team claim that the OAuth onboarding investment "is working"
should land. Acked: 579c20ec.

## Open questions blocking the Bertha-pipeline takeover

- Run-host for the new entrypoints (altair.local launchd vs
  AC-server-side apscheduler/cron). Affects cutover speed and
  cross-host coupling. Awaiting Juan's call.
- DB write-path for the milestone state table. The existing
  AdminDB enforces `default_transaction_read_only=on` at session
  level; the existing retire/delete commands relax it via
  `SET LOCAL default_transaction_read_only = off` inside a
  transaction. New entrypoints will follow the same pattern —
  unblocked from the design side, mentioning for completeness.
- Mail-from identity to Bertha. Lean metis (analytics surface +
  identity now exists). Awaiting Juan's call.
- Cutover handshake with Hestia: parallel-run for one cycle as
  sanity check vs hard cutover.

## Signals

- Wiring confirmed: ran check.py --dry-run via Hestia's DATABASE_URL
  2026-05-10 10:29Z. 0 external multi-agent crossers, as expected.
- 5 inter-agent surfaces are already covered by the predicate
  (mail, chat, contacts, tasks, task_claims). Add new surfaces
  by extending CTEs.
- Tahim Pranta has 25 agents but no inter-agent activity —
  interesting datapoint, not yet a milestone.
- Render deploy-lag pattern (2 cycles, multi-hour GHA→/health flip
  vs historical ~3min) is operational signal Hestia flagged in
  status/operations.md. Not my surface but worth tracking.

**Stop-gap empirical state 2026-05-14** (Hestia f822ad07):
- Daily sign-up export firing on schedule (today 08:09Z, msg
  99c39c12 in conv a31c58e9; 0-row day).
- Hourly milestone-check intermittent. Last clean cluster:
  19:36/20:35/22:36 (2026-05-13) and 01:02/01:42/03:22 (2026-05-14).
  Then 8h gap 03:22Z → 11:30Z (~8 missed firings). Root cause:
  Hestia's "cron" only fires while her Claude session processes
  messages; not a real system cron.
- Net signal impact during the gap: zero. External multi-agent
  user population is at 0; no alert would have fired anyway.
- **Framing held in mail to Bertha (b7dd0b5f)**: absence of
  milestone-alert mail does NOT mean zero candidates over the
  window; daily batch is the durable signal; hourly is
  opportunistic until the durable replacement lands.

## Instrumentation gaps

- No durable scheduling for the Bertha pipeline. CronCreate
  `durable=true` does NOT persist; lives only in active Claude
  session. Closing this is the immediate work.
- No DB-backed state for milestone-alerted users; current
  state file at hestia/.claude/state/multi-agent-alerted-users.json
  is local-only (gitignored, not portable).
- No telemetry/observability on analytics runs (success/failure,
  duration, candidate count). Worth adding alongside the
  entrypoint cutover.
- Pre-existing gaps from prior handoff still real:
  - First-time-to-coordination event (Stage 2 threshold) is
    not instrumented.
  - Distribution-action-to-signup attribution query does not
    exist.
  - No queryable surface over support patterns (Aida's status
    file is the human-readable surface).
  - No browser/edge telemetry beyond Render request stats.

## Next checks

1. Follow up with Juan on the four pinned open questions for the
   Bertha-pipeline takeover (design proposal sent 2026-05-10; no
   answer as of 2026-05-14). Without his call I cannot start
   authoring; without a durable scheduling pattern in place I
   should not add new signal entrypoints under it.
2. Check whether Hestia's session crons are still firing or have
   died with her session. If dead, the daily-signup-export and
   milestone-check have silently stopped — that itself is signal
   worth flagging.
3. After Juan's call: create aw task with Work contract block,
   coordinate with Athena (code lives in ac), draft migration +
   CLI commands + wrapper scripts + launchd plists.
4. Cutover: dual-run one cycle, compare outputs to Hestia's
   stop-gap, then her session crons stand down.
5. After cutover: scope Athena's OAuth-onboarding signal — verify
   `mcp_oauth_grants` ↔ `consumer_contact_invites` ownership-join
   is clean, confirm the N=15 window default, propose
   company-dashboard signal-inventory entry.
6. After OAuth signal lands: pre-existing instrumentation gaps
   (Stage-2 threshold, attribution query, support-pattern
   queryable surface).
