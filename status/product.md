# Product Status

Last updated: 2026-04-21 (Avi)

## Current focus

**The product has shipped. Distribution has not started.** The
engineering-to-distribution ratio the board flagged on 2026-04-07 is
now the active gap — not a future concern. Every further hour spent
polishing the stack without users is wasted by our own invariants.

This week:
1. Push Juan through the blog-post voice pass and publish
   `publishing/drafts/2026-04-09-five-agents-blog-post.md` on
   juanreyero.com. 12 days old in draft; longer is waste.
2. Have Charlene start the daily scan and open the first 1-2 of the 8
   identified outreach contacts. The "wait for product readiness"
   gate has been met.
3. Decide with Randy: is the collision video still the highest-priority
   asset, or is the blog post enough to carry Stage 1 awareness?

## Product readiness

- **OSS aweb**: Shipping. v1.16.0 server + CLI, awid-service v0.4.0.
  `aw run claude` and `aw init` work end-to-end, hosted and
  self-hosted. e2e journey script passes. One P2 paper-cut
  (runTeamSwitch, aweb-aakn) pending a small patch — not a ship
  blocker.
- **aweb-cloud**: Shipping. v0.5.3. Identity migration complete.
  Dashboard feature-complete for launch (Monitor / Tasks / Mail /
  Chat / Agents / Settings / Onboarding / Connect). Billing live,
  Stripe wired, pricing aligned with strategy doc
  ($0 / $25 / $250).
- **awid registry**: Live at api.awid.ai. Hard dependency of the
  hosted cloud.
- **Landing site (aweb.ai)**: Live. Needs a blog section in Hugo to
  host aweb.ai/blog posts (per 2026-04-11 publishing split). Not a
  launch blocker — first post goes to juanreyero.com.

## Outreach state (from co.aweb)

- **Blog post "5 agents"**: Drafted 2026-04-09. Awaiting Juan's
  voice pass. Not published.
- **Contacts**: 8 identified (7 protocol-article authors + Addy
  Osmani + Yeachan Heo), 0 contacted, 0 replies.
- **Daily scanning**: Not running. Infrastructure built, execution
  not started.
- **Conversations joined**: 0.
- **History.md**: Empty.

## User feedback (from Amy)

None yet. Amy activated `aweb.ai/amy` today (2026-04-21) as the
canonical public support address — support surface is now ready for
external users. No external users yet.

## Priorities

1. **Publish the blog post this week** — longest pole, blocks the
   rest of the outreach sequence.
2. **Start the 5-conversations-per-week habit** (strategy.md Pillar
   1) — Charlene monitors, humans engage.
3. **Open the first 3-5 direct contacts** once the blog post is
   live (so the outreach points at something real).
4. **Ship the runTeamSwitch patch** (Randy) — small but visible
   paper-cut for any multi-team user.
5. **Decide on the collision video** — produce or cut from the
   plan.

## Strategy-doc reconciliation

`docs/strategy.md` lists a "known gap" that live pricing doesn't
match the doc ($25/$250 vs $49/$149 live). That gap has closed —
cloud v0.5.3 enforces $25/$250. The known-gaps note in strategy.md
is stale; will fix in a later pass.

## Open questions for Juan

- Blog-post voice pass — when?
- Collision video — still highest-priority asset, or drop?
- Amy's second address (`aweb.ai/amy`) is wired; do we announce
  aweb.ai/amy as the public support contact in the blog post footer?
