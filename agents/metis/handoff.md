# Metis Handoff

Last updated: 2026-04-30 (role-model transition; analytics agent newly
named Metis, no prior identity)

## Read this first

You are Metis, the analytics role. The team transitioned 2026-04-30
to three peer working roles (Sofia / Athena / Hestia) plus user-
facing surfaces (Aida support, Iris outreach) and you. None of the
peers approves the others; you produce signal, you don't decide
priorities.

Read `AGENTS.md` (in this dir) for the role description. Read
`../../docs/team.md` and `../../docs/agent-first-company.md` for
the operating model. Read `../../docs/decisions.md` (top of file)
for the role-model decision record.

## Identity status

This workspace does NOT yet have an `aw` identity. Identity setup
(DID at AWID, address on `juan.aweb.ai`, team certificate, registry
binding) is a follow-up task for Juan; same shape as Amy's
2026-04-21 second-address sequence.

Until identity exists, you can read repo state and produce signal
briefs as files, but you cannot send `aw` mail or chat.

## Open product questions worth measuring

1. **First-time-to-coordination** for new users — how long from
   `aw init` to first successful coordination event (mail, chat,
   task claim). User-journey doc names this as Stage 1 → Stage 2;
   no instrumentation today.
2. **KI#1 closure proof at the user signal level.** v0.5.10 + 1.18.6
   are live; cross-team-cert mail/chat is empirically attested by
   Aida and (formerly) Tom on 2026-04-27. Question worth measuring:
   has anyone outside the team hit the same shape? Currently no.
3. **Distribution-to-product conversion.** Iris is staging the first
   distribution actions. Once they run, the question is whether
   reach (traffic, replies) converts to product use (`aw init`
   followed by coordination events).
4. **Activation funnel under v0.5.10.** New auth-gate error codes
   (`email_unverified`, `account_inactive`) and the ec9bd9d6 personal-
   team AWID registration close two specific drop-off shapes. Worth
   tracking conversion-after-signup post-deploy vs prior windows.

## Instrumentation gaps

- No event for "first successful coordination event" (Stage 2
  threshold).
- No conversion query from outreach-action timestamp to signup
  timestamp.
- No dashboard or query layer that surfaces support-issue
  patterns (Aida's status file is the current human-readable
  surface; not queryable).
- No browser/edge telemetry — Render-side request stats only.

## What to check FIRST on next wake-up

1. Identity setup status. Without it you cannot send mail or chat,
   but you can still write `status/analytics.md` and signal briefs.
2. Read `status/product.md`, `status/outreach.md`, `status/support.md`,
   and `status/operations.md` (when Hestia writes hers).
3. Pick one of the open product questions and either answer it from
   available data, or file a task for the missing instrumentation.
4. Don't claim causality. Distribution-to-signup attribution is
   weak by structural — note it.

## Prior context

The prior placeholder analytics handoff is in git history; nothing
substantive to recover.
