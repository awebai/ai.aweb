# Metis handoff

Last updated: 2026-06-03 (server-restart prep at Juan's direction).

Crisp current-state. For history — how we got here, who said what when,
artifact IDs — read `logbook.md`.

## Who you are

Metis — analytics surface on the six-role peer team (Sofia direction,
Athena code, Hestia operations, Aida support, Iris outreach, you).
Workspace identity: `metis` on `default:aweb.ai` team, developer role.
Path: `agents/metis/` in this repo.

You produce signal briefs with attribution limits made explicit.
Discipline: state the question first, separate direct evidence from
correlation, say when attribution is unknown, file tasks for missing
events.

## What's in flight on your surface right now

**Nothing.** The world moved during a 2-week silent gap (2026-05-19 →
2026-06-02). Current state of the workstreams you owned:

| Item | State | Notes |
|---|---|---|
| First signal brief (`aals.4`) | DONE | `briefs/2026-05-15-adoption-state-first-brief.md`; routed and absorbed. |
| Bertha-pipeline takeover | SUPERSEDED | Juan directed Hestia 2026-06-02 to bank reusable read-only scripts (`agents/hestia/scripts/`). YAGNI-correct at 0-row-most-days volume. The architectural-call thread (Option B run-scheduler service) is parked in Sofia's lane via `default-aaae`. |
| `default-aaad` referrer/source at signup | OPEN, P1 | Filed 2026-05-15; Grace's lane via Athena; no movement visible. |
| `default-aaae` workspace-facts aggregation | OPEN, P2 | Filed 2026-05-15; sharpened to scheduler-never-starts via Hestia's empirical; Sofia owns architectural call (Option A vs B) before Grace executes. |
| OAuth-onboarding signal (Athena queue) | QUEUED | Numerator: `mcp_oauth_grants` → `consumer_contact_invites` within N=15min. Baseline at last check was n=1; re-baseline at n>=10. Schema bank in logbook. |

## What you're waiting on

- **Sofia**: architectural call on Option A vs B for the run-scheduler
  service. If Option B lands, your Bertha-pipeline proposal could
  un-park as apscheduler jobs registered in that process. But don't
  re-propose — wait for the call.
- **Juan**: bless or revise Sofia's standing-line wording for the n=1
  baseline ("insufficient grant volume to compute conversion rate;
  will re-baseline at n>=10"). Sofia was in flight with him 2026-05-15.

## First reads on restart

1. `git pull` (always first).
2. `aw mail inbox` and `aw chat pending`.
3. `../../status/operations.md` and `../../status/product.md` — for
   what's shipping right now.
4. `../../docs/decisions.md` — entries newer than 2026-06-03.
5. `../../agents/hestia/scripts/README.md` — Hestia's banked analytics
   scripts. These ARE your read-only analytics surface for routine
   questions. Exercise `signups.py --days 7` and
   `multi_agent_active.py --days 7` as the first smoke read to refresh
   your view of the population. PII discipline in that README is
   binding on you too.
6. `logbook.md` only if you need the history behind the table above.

## Server-restart verification

Juan is restarting you on a server (2026-06-03). On first wake-up:

- `aw workspace status` should show `metis` alias on `default:aweb.ai`
  team. If identity didn't survive the move, stop and ask Juan.
- DB read access via `DATABASE_URL` in `../../../ac/.env.production`.
  Smoke: run one of Hestia's scripts. If you can't reach the DB, mail
  Athena.
- If server-restart now means you have real durable scheduling
  available, that COULD un-park the Bertha-pipeline architectural
  call. Don't re-propose; surface to Sofia + Juan with the new
  capability context and let them call.

## Standing posture

- Probe mails (e.g. `MATRIX-PROBE-*`) get silent receipt. Delivery
  acks; no reply needed.
- Don't ack-of-ack peer routing confirmations — that's noise.
- Brief cadence is decision-window-driven, not schedule-driven. Next
  natural trigger after a distribution action (Twitter thread,
  long-fruit submission cluster reach) — pre/post comparator against
  the 2-5/week external-signup steady-state baseline.
- Don't write briefs without a decision-relevant question they
  inform. "Activity report" briefs are noise.
- Internal exclusion list when querying external users:
  `juan@aweb.ai`, `juan@juanreyero.com`, `eugenie@aweb.ai`. Hestia's
  scripts already handle this; preserve it in any new query.

## How peers reach you

Per the role's communication table in `AGENTS.md`. Mail for non-urgent
updates, chat-and-wait for blocking questions.
