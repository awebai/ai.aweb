# Vision and Current Priorities

Last updated: 2026-04-10

## The vision

AI agents will work in teams. They need identity, coordination, and
trust to do that. aweb provides this as open infrastructure.

Two audiences:
1. **Developer teams** running 2-10 agents on the same codebase today.
   They need agents to stop stepping on each other. This is the
   immediate, revenue-driving use case.
2. **Agent society builders** creating systems where agents communicate
   across organizational boundaries. This is the long-term network
   play.

## Current phase: finish the migration, then ship

The product is mid-migration to full public-key cryptographic identity
(Ed25519, `did:aw`, team certificates). The old version worked but the
architecture was wrong — bearer tokens and API keys can't support
cross-organizational trust. The new architecture is vastly more
powerful but not yet ready.

### What's happening right now (2026-04-10)

**OSS (aweb repo):**
- Close to shippable. E2E tests pass.
- Active work: identity-scoped messaging, CLI+server alignment for
  team architecture.
- Dev team: dave (coordinator), henry + ivy (developers).

**Cloud (ac repo):**
- Auth bridge mid-migration (JWT -> team certificates).
- Not yet working end-to-end. Estimated ~2 days.
- When ready: backup prod data, drop database, start fresh.
- Dev team: alice (coordinator), bob (developer).

### Priorities (in order)

1. **Finish the migration.** OSS first, then cloud. No outreach until
   the product works.
2. **Publish the blog post.** "What happens when you give 5 AI agents
   the same codebase" is drafted. Publish when the product is ready
   for people to try.
3. **Contact protocol article authors.** 5-7 people identified in
   outreach/contacts.md. aweb belongs in their MCP/A2A ecosystem maps.
4. **Start the 5-conversations-per-week outreach habit.** Twitter/X,
   Reddit, HN.
5. **Build atext.ai** (after outreach is running). Proves the platform,
   gives every pitch a live demo.

### What not to do right now

- No new features until the migration is done
- No outreach until the product works
- No atext until outreach is running
- No collision video until there's something to link to

## Key decisions

- **Crypto identity over bearer tokens**: Accepted the cost of a full
  rewrite for the long-term architectural win. See docs/decisions.md for details.
- **Two-coder + two-reviewer agent setup**: Agents building alone
  produce wrong things. The 2+2 setup (one pair per repo) works. CTO
  should enforce this structure.
- **Ship OSS before cloud**: The OSS is closer to ready and can stand
  alone. Don't block OSS shipping on cloud readiness.

## Success metrics

- **This week**: OSS repo shippable, cloud auth bridge working
- **Next week**: Blog post published, first 3 contacts reached
- **1 month**: 10 real external users on free tier
- **3 months**: 50 active users, 5 design partners, first external
  mention
