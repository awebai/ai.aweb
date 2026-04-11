# Content Plan

See the 2026-04-11 entry in docs/decisions.md for the publishing split.

**juanreyero.com** — personal stories, first-person experience, what
gets shared on HN/Reddit/Twitter. Brings people to Juan, links to aweb.

**aweb.ai/blog** — technical deep dives, protocol explanations, project
updates. For people who are already interested. Builds domain authority.

---

## Posts

### 1. What happens when you give 5 AI agents the same codebase
- **Where**: juanreyero.com
- **Status**: Draft ready (publishing/drafts/2026-04-09-five-agents-blog-post.md)
- **When**: Publish when OSS is shippable — the post links to the repo
  and `aw init`, so it needs to work when people try it
- **Distribution**: HN ("Show HN"), Reddit (r/ClaudeAI, r/ChatGPTPro),
  Twitter thread version, LinkedIn
- **Notes**: Needs Juan's final voice pass. The draft is solid but
  Juan should add his real stories and make it his.

### 2. Agent Web: how identity works
- **Where**: aweb.ai/blog
- **Status**: Source material ready (docs/aweb-high-level.md)
- **When**: After post #1 is published. This is for people who read
  #1 and want to understand the architecture.
- **Distribution**: Twitter (for protocol-interested people), link
  from aweb docs, share with protocol article authors from
  outreach/contacts.md
- **Notes**: Needs to be rewritten from the high-level doc into a
  blog post format. Less "spec", more "here's how we think about
  agent identity and why."

### 3. We rebuilt everything around public-key crypto — here's what happened
- **Where**: juanreyero.com
- **Status**: Not started — write after migration is complete
- **When**: When the migration is done and we have real data: how
  long it took, what worked, what didn't, what the agents got wrong
- **Distribution**: Same as #1 — HN, Reddit, Twitter
- **Notes**: The rearchitecture story. Includes the lesson about
  agents building the wrong thing, the 2+2 rule, the decision to
  eat the migration cost before having users. This is the most
  interesting story because it's about the meta-problem: using
  agent coordination to build agent coordination infrastructure.

### 4. aweb vs MCP vs A2A — different layers of the stack
- **Where**: aweb.ai/blog
- **Status**: Not started
- **When**: After posts #1 and #2. This is the positioning piece
  for protocol-comparison audiences.
- **Distribution**: Share directly with protocol article authors
  (see co.aweb contacts) — this is the post that makes the case
  for including aweb in ecosystem maps
- **Notes**: MCP is agent-to-tool. A2A is task delegation. aweb is
  identity and coordination. They're complementary. Keep it factual,
  not competitive.

### 5. Running a company with AI agents (working title)
- **Where**: juanreyero.com
- **Status**: Not started
- **When**: After the co.aweb agent team (CTO, CEO, board) has been
  running for a few weeks and we have real experience
- **Distribution**: HN, Reddit, Twitter. This has broad appeal beyond
  the multi-agent coding audience.
- **Notes**: The story of co.aweb itself: permanent CTO and CEO agents,
  a board member that keeps them accountable, handoff docs, invariants.
  What works, what doesn't. Dogfooding at the company level.

---

## Content not yet shaped into posts

- The collision video (strategy.md calls it "highest priority single
  asset") — record 3 uncoordinated agents making a mess, end with
  "what if they could talk to each other?" Post to Twitter, Reddit.
- Agent-to-agent chat logs and coordination screenshots — "build in
  public" content for Twitter. Novel because nobody else is showing
  real agent-to-agent conversations.

---

## Infrastructure needed

- [ ] Add blog section to Hugo site (ac/site/) for aweb.ai/blog posts
- [ ] Juan's publishing setup on juanreyero.com (already exists?)
