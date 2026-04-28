# Product Status

Last updated: 2026-04-28 20:43 CEST (Avi)

## Current focus

**The product is live enough for distribution again; the remaining gap is
company operating rhythm.** The 2026-04-25 product status is stale:
KI#1 is no longer launch-blocking. Cloud is live on v0.5.9 with aweb
1.18.6, and Amy/Tom attestation in the latest support/cloud handoffs
marks the mail/chat identity issue closed.

Today Juan asked for a company-organization pass: how to run aweb
agent-first. Product implication: dogfooding is no longer just "agents
use chat." The company needs a clearer operating system around tasks,
claims, status, handoffs, gates, and human decision points, using the
same primitives we sell.

This week:
1. Turn the "agent-first company" study into a concrete operating model:
   which agents exist, what they own, what every wake-up produces, and
   what must be represented as aweb tasks/claims instead of only markdown.
2. Restart distribution now that the live blocker is closed: blog post
   voice pass, first outreach brief, and first human-led conversations.
3. Fix the comms execution gap: `status/outreach.md` and Charlene's
   handoff are still 2026-04-11-era, and `aw chat ... charlene` does
   not resolve in the active workspace.

## Product readiness

- **OSS aweb**: Shipping. Local repo is at aweb 1.18.6-era main;
  tags include `server-v1.18.6`, `aw-v1.18.6`, `awid-v0.5.2`, and
  `awid-service-v0.5.2`. Current focus in recent commits is trust
  contract enforcement, identity-equivalent recipient matching, and
  hosted-custodial matrix coverage.
- **aweb-cloud**: Live. `https://app.aweb.ai/health` reports
  `release_tag=v0.5.9`, `aweb_version=1.18.6`, database/Redis/awid
  healthy, and mounted coordination API healthy.
- **awid registry**: Live. `https://api.awid.ai/health` reports
  `version=0.5.2`, Redis/database/schema healthy.
- **Landing site (aweb.ai)**: Live. Blog section still listed as needed
  for aweb.ai/blog posts; first personal/problem post remains planned
  for juanreyero.com.

## Outreach state

- **Blog post "5 agents"**: Draft ready since 2026-04-09; still not
  published per `publishing/history.md`.
- **Contacts**: Public status still says identified but uncontacted.
  Private outreach files show no daily briefs and no recorded outreach
  actions.
- **Daily scanning**: Not running.
- **Conversations joined**: 0.

## User feedback

- Amy asked for product classification on internal-alias-only rename.
  Answer sent 2026-04-28: classify as **intentional today, possibly
  reconsidered**. Customer-facing line: alias-only rename is not
  supported; archive + create new is the current path, with history
  continuity tradeoff.
- No external user feedback surfaced in the public handoffs beyond
  internal attestation and support-runbook shaping.

## Priorities

1. **Define the agent-first operating model** — Juan asked for this
   today, and it directly supports the "running a company with AI
   agents" dogfooding story.
2. **Reactivate distribution** — blocker is closed; the board's
   engineering-to-distribution concern is now acute again.
3. **Repair comms execution path** — Charlene needs a live workspace
   identity or a documented replacement alias, current outreach status,
   and a first daily brief.
4. **Keep engineering in release-discipline mode, not feature-expansion
   mode** — recent v0.5.9 work is exactly the kind of correctness
   discipline needed before inviting users, but the next product step
   is usage, not more hidden polish.

## Open questions for Juan

- For the agent-first operating model, should company work use the
  current permanent-agent roster as-is, or should we create explicit
  operational teams/workspaces by function (exec, engineering, comms,
  support)?
- Do we still want the collision video before the first blog post, or
  should the blog post publish first now that v0.5.9 is live?
- Who owns fixing the comms identity gap if `charlene` is not resolvable
  in the active aweb workspace?
