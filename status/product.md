# Product Status

Last updated: 2026-04-28 22:23 CEST (Avi)

## Current focus

**The product is live enough for distribution again; the remaining gap
is company operating discipline.** KI#1 is no longer launch-blocking.
Cloud is live on v0.5.9 with aweb 1.18.6, and Amy/Tom attestation in
the latest support/cloud handoffs marks the mail/chat identity issue
closed.

Juan refined the company model again. The permanent areas are now
direction, engineering, outreach, support, operations, and analytics.
Repo work should happen through task-scoped builder/reviewer pairs
created with `aw workspace add-worktree`, not permanent repo-manager
agents. Every archetype owns a feedback loop.

This week:
1. Update `aweb-aals.2`: responsibility-area instruction sweep now
   reflects the smaller permanent set and task-scoped repo pairs.
2. Continue `aweb-aals.1`: convert current company priorities into `aw`
   tasks with builder, reviewer, and strongest available feedback
   signal.
3. Restart distribution now that the live blocker is closed: blog post
   voice pass, first outreach brief, and first human-led conversations.

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

## Support / user feedback

- Amy asked for product classification on internal-alias-only rename.
  Answer sent 2026-04-28: classify as **intentional today, possibly
  reconsidered**. Customer-facing line: alias-only rename is not
  supported; archive + create new is the current path, with history
  continuity tradeoff.
- No external user feedback surfaced in the public handoffs beyond
  internal attestation and support-runbook shaping.

## Priorities

1. **Finish the responsibility-area reorg (`aweb-aals`)** — permanent
   areas are now direction, engineering, outreach, support, operations,
   analytics; remaining work is review and task conversion.
2. **Reactivate distribution** — blocker is closed; operations should
   now flag distribution loops that are not running.
3. **Repair outreach execution path** — outreach needs a reachable
   workspace identity, current outreach status, and a first daily brief.
4. **Keep engineering in release-discipline mode, not feature-expansion
   mode** — recent v0.5.9 work is exactly the kind of correctness
   discipline needed before inviting users, but the next product step
   is usage, not more hidden polish.

## Open questions for Juan

- Do we still want the collision video before the first blog post, or
  should the blog post publish first now that v0.5.9 is live?
- What is the first distribution action, and what feedback signal do we
  record after it runs?
