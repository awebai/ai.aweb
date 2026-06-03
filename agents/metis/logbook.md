# Metis logbook

Curated history of my surface. Tells the story behind what `handoff.md`
summarizes as current state. Each entry is one substantive moment with
the artifacts (message IDs, commits, file paths) that prove it. Newest
on top.

When something happens worth remembering, add an entry here AND update
the relevant section of `handoff.md` if it changes current state. Don't
duplicate prose between the two — handoff is summary, logbook is record.

---

## 2026-06-02 — Bertha-pipeline takeover absorbed into Hestia's script bank

Juan to Hestia (banked in commit `3c12ff4` message):
> "we really need to have pre-made scripts for the questions that you
> get from bertha and from me, and they should be a clear part of your
> agents.md."

Hestia banked `agents/hestia/scripts/` with `signups.py`,
`user_activity.py`, `multi_agent_active.py`, `team_probe.py`, `_db.py`,
plus README + AGENTS.md "Analytics & probe scripts" section.

**What this means for my surface.** The Bertha-pipeline takeover I
proposed 2026-05-10 (admin entrypoints + DB-backed state + launchd /
apscheduler service) is effectively cancelled. The team chose YAGNI:
at 0-row-most-days volume, reusable read-only scripts beat scheduler
infrastructure.

Do not re-litigate. Pre-made scripts ARE the right answer at current
volume. If volume rises and signal cadence needs to become reliable
rather than opportunistic, the architectural call re-opens.

The `default-aaae` architectural call (Option B run-scheduler service)
remains parked in Sofia's lane via Athena's task comment.

## 2026-05-19 — Two probe mails from Hestia (silent receipt)

`MATRIX-PROBE-70452` and `RE-MATRIX-64031`, both single-char `p` body.
Delivery-probe shape. Per channel semantics, delivery itself acks; no
reply needed. Banked posture: probes get silent receipt; do not
respond.

## 2026-05-15 — First signal brief shipped (closes aals.4)

`agents/metis/briefs/2026-05-15-adoption-state-first-brief.md`.

**Headline finding**: `mcp_oauth_grants_total = 7` was the working
team number, but true external population is **n=1**. Of 7 grants: 4
internal team + 2 Juan-testing + 1 real external (`gptstars12@gmail.com`,
2026-05-05). With `consumer_contact_invites_total = 0`, conversion
baseline is 0/1, not 0/7. External signup rate 2-5/week steady for 7
weeks; no observable lift from pain-narrative deploy 2026-05-13 22:28Z
in its first 36h.

Routed to Sofia (`ce87ea44`), Iris (`bdf77013`), Athena (`ff265a3d`).

Responses:
- **Sofia** (`1fa25379`): banked sibling discipline
  `feedback_verify_baseline_before_claiming_rate.md`; standing-line
  wording "insufficient grant volume to compute conversion rate; will
  re-baseline at n>=10" routed to Juan for bless. Sibling to the
  deployed-surface-spot-check rule under the broader "verify before
  claiming" principle.
- **Athena** (`7171dd6f` → `cc28132a`): confirmed both instrumentation
  gaps real; routed to Grace via dev-team chat. `default-aaad` cleared
  for Grace immediately; `default-aaae` gated on Hestia disambiguation.
- **Iris** (`8fdf6c01`): surfaced the interpretability-cost framing to
  Juan in his blog / Twitter edit window so he could call sequencing.

Filed two aw tasks:
- `default-aaad` (P1, feature, OPEN): referrer/source at signup.
- `default-aaae` (P2, bug, OPEN): workspace-facts aggregation.

## 2026-05-15 — Aggregation-job dead-letter discovery (Hestia)

Hestia (`01b3196b`): `aweb_cloud.daily_active_workspace_facts` has 0
rows total ever — not last-7d empty, never populated. Root cause:
`JobScheduler` only instantiated in `cli.py` for list-jobs / run-job;
`main.py:lifespan` never calls `scheduler.start()`; no Procfile or
Render cronJob. Apscheduler loop never runs in production.

Same shape as Task #109 (Render runtime ≠ code intent).

Hestia banked two fix options: (A) wire JobScheduler into FastAPI
lifespan startup — concurrency hazard on multi-replica; (B) separate
Render service running `python -m aweb_cloud.cli run-scheduler` —
cleanest, scales independently of API.

**Architectural coupling I surfaced** (mail to Athena `76b55fce`):
Option B is also the run-host answer to my parked Bertha-pipeline
design call. One architectural call closes both problems.

Athena (`cc28132a`) routed `default-aaae` architectural call to Sofia.
Sofia's call: still open as of 2026-06-03.

## 2026-05-14 — Bertha pipeline stop-gap leaking; OAuth-onboarding signal queued

**Hestia** (`f822ad07`): daily sign-up export firing on schedule;
hourly milestone-check intermittent (8h gap 03:22Z → 11:30Z that day,
~8 missed firings). Root cause: session-driven not real cron. Net
signal impact zero (population at 0).

Mailed Bertha (`b7dd0b5f`) with framing-correction so Eugenie doesn't
develop false confidence in "no mail = no candidates": absence of
milestone-alert mail ≠ zero candidates; daily batch IS the durable
signal; hourly is opportunistic.

**Athena** (`7223708e`) queued post-OAuth-onboarding signal:
- Numerator: new `mcp_oauth_grants` rows producing
  `consumer_contact_invites` row within N=15 min.
- Denominator: new `mcp_oauth_grants` rows in the period.
- Period: daily rolling.
- Surface: company-dashboard signal-inventory entry.

Empirical-zero-tolerance: no team claim that OAuth onboarding "is
working" until instrumented.

Athena (`e60a0d1c`) confirmed: OAuth ship not imminent (2-3 days
wall-clock); ordering held (Bertha cutover first, OAuth second);
banked schema (both tables in `aweb_cloud`, join on `user_id +
team_id`, `created_at` + `accepted_count` present). Also surfaced
my parked-four-days Bertha proposal to Juan separately.

## 2026-05-10 — Identity online; Bertha-pipeline handoff from Hestia

Workspace identity bootstrapped: `metis` alias, `default:aweb.ai` team,
developer role.

Hestia handoff brief (`e8bf1afe`, conv `b690dca3`): she'd been running
two session-cron stop-gaps on altair for Bertha (daily sign-up export
08:13 CEST, hourly multi-agent milestone check). CronCreate
`durable=true` doesn't actually persist; lives only in active Claude
session.

Juan's redirect: "we are going to task metis, who is responsible for
analytics, for the regular check of the database... she will need to
design and write admin entrypoints to do the tasks."

I proposed (in conversation with Juan, same day): extend `aweb-admin`
Click CLI in ac with `daily-signup-export` and `milestone-check`
commands; lift SQL into `services/admin_analytics.py`; DB-backed state
via new `aweb_cloud.analytics_milestone_alerts` migration; mail
decoupled from CLI (CLI emits stdout, wrapper pipes to `aw mail send`);
launchd plists on altair for cutover.

Three pinned open questions to Juan:
1. Run-host (altair launchd vs AC server-side apscheduler/cron).
2. Mail-from identity to Bertha (lean metis).
3. Cutover handshake with Hestia (parallel-run vs hard cutover).

Acked Hestia (`c8e94011`). No answer from Juan; design parked for 24
days; Hestia's 2026-06-02 script bank superseded.
