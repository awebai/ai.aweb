# Outreach Playbook v0

*Sofia draft, 2026-05-26. For Juan's execution. Pending Iris's
framing-pass on specific text where she's the voice authority. The
prioritization and sequencing below are direction-shaped (Sofia
surface); the wording of specific messages is voice-shaped (Iris
surface). Treat exact text as starter scaffolds, not final copy —
Iris refines before send for any item not marked "send as-is."*

---

## How to use this

Each action below is a discrete unit. Do one, capture signal, then
move on. The order optimizes for: lowest-effort first, existing
assets first, most-targeted audience first.

Per-action shape: **Where** (URL or channel), **What** (text or
text scaffold), **When** (timing window), **Capture** (signal to
record afterward), **Status** (ready / pending-X).

Standing rules (from `publishing/voice.md` + the BeadHub-era
strategy in `co.aweb/outreach/source-material/beadhub-era/`):

- **Be useful or stay silent.** Every post helps the reader.
  Promotion is a side effect of being genuinely helpful.
- **Lead with experience, not product.** First-person ("I built
  this", "we use this"). Never marketing-speak.
- **One comment per thread.** Don't reply to your own comment to
  add more. Don't dominate.
- **Never argue with negative responses.** Move on.
- **Standing post window**: Tue-Thu morning US Pacific (14:00-17:00
  UTC roughly). Mondays and Fridays are noisier; weekends sink.

---

## Action 1 — r/ClaudeCode text post promoting "Pair Your Coding Agent with a Reviewer"

**Priority**: HIGH. r/ClaudeCode is 395K weekly visitors, primary
fit for the article's P3 (developer team) audience. The article
has been live 3 weeks at juanreyero.com/article/ai/two-agents-not-one/
without promotion — three weeks of free signal lost.

**Where**:
- Go to https://www.reddit.com/r/ClaudeCode/ and click "Create Post."
- Pick "Text" post type (not Link). Text posts get more engagement
  on Reddit than link-only.

**What** (starter scaffold — Iris framing-pass before send):

**Title** (pick one; lead with experience, not promotion):

> Option A: "Running 2 Claude Code agents on the same codebase — pair one as the reviewer"
> Option B: "After 3 months running multi-agent Claude Code: the second agent should be a reviewer, not another coder"
> Option C: "Why I run Claude Code in coder + reviewer pairs instead of two coders"

**Body** (starter scaffold; Iris voice-pass before posting):

```
I've been running 2 Claude Code agents on the same codebase for a few
months now. The first instinct is to run them as two coders — one on
the frontend, one on the backend, or split feature work. That works
for ~a week, then they start duplicating effort or stepping on each
other.

The shape that's been working: pair them. One agent writes code, the
other reviews diffs before they land. The reviewer catches things the
coder missed for the same reason a human reviewer would — fresh eyes
without the original framing.

Wrote up what we learned at:
https://juanreyero.com/article/ai/two-agents-not-one/

We coordinate them through aweb (https://aweb.ai — open source MIT
coordination layer). Cryptographic identity per agent, persistent
task claims, mail/chat between agents so they don't step on each
other. Repo at https://github.com/awebai/aweb.

Happy to answer questions about specific setups. What patterns have
worked for others running multi-agent coding?
```

**When**: Tue/Wed/Thu, 14:00-17:00 UTC. Earlier in this window is
better — early Reddit comments get more visibility.

**Capture**:
- Reddit upvotes / comments at +1h, +6h, +24h.
- Plausible referral traffic to juanreyero.com and aweb.ai
  (segment: "reddit" source).
- New GitHub stars on github.com/awebai/aweb in the 24h window.
- Any inbound on the post — reply ONCE if substantive technical
  question. Do not reply to your own comment to add more.
- If a hostile comment arrives, don't argue. Move on.

**Status**: READY pending Iris voice-pass on title + body.

---

## Action 2 — Twitter single-tweet reference

**Priority**: Medium. Riding on the Reddit post — Twitter
amplifies once the Reddit post has some social proof.

**Where**: Juan's personal account (joanmg per past notes), Twitter web.

**What** (one tweet, ~250 chars):

> wrote this on running two AI coding agents instead of one — the
> reviewer catches things the coder misses, in the same way a human
> reviewer would. https://juanreyero.com/article/ai/two-agents-not-one/

**When**: 24-48h after the Reddit post lands, ideally when the
Reddit post is showing some engagement (>10 upvotes, comments).
Reverse the order if Reddit sinks fast — Twitter still benefits.

**Capture**:
- Twitter impressions, link clicks (visible in tweet analytics).
- Plausible referral from t.co / x.com.
- Replies — engage once per thread if substantive.

**Status**: READY. No voice-pass needed (single sentence; Juan's
voice).

---

## Action 3 — HN read-only watch setup

**Priority**: Background; ongoing. Not a "post HN" action — the
article is 3 weeks old, no news hook, would sink. Watch for
opportunities to reply on someone else's relevant thread.

**Where**: https://hn.algolia.com/?q=multi-agent+coding (and
related searches per `co.aweb/outreach/watch.md`):
- multi-agent coding
- Claude Code coordination
- AI agents same repo
- agent-to-agent
- MCP coordination

**What**:
- Set up Algolia HN search alerts (account-bound; email when
  matching post appears) OR check the search URLs above daily for
  ~5 min.
- When a relevant thread appears, read it. Decide if there's
  substantive value to add by sharing your experience. If yes,
  reply ONCE — lead with experience, mention aweb only if directly
  relevant. If no value, don't engage.

**When**: Daily 5-min scan, ~5pm UTC (catches both EU and US
posts from that day).

**Capture**: When you reply to a thread, log it (date, link, what
you said, observed response). Track in
`co.aweb/outreach/history.md`.

**Status**: READY. No content to author; just monitoring discipline.

---

## Action 4 — 5 direct-outreach mails to protocol-ecosystem-map authors

**Priority**: HIGH. Pre-drafted 2026-05-07; recipients are
ecosystem-map authors where inclusion compounds. Held three weeks.

**HOLD pending Iris re-author**. Per her step 2 audit (commit
`aec45ed`), the pre-drafted text uses trinity-shape framing
("aweb for the identity + coordination layer those leave out of
scope"). Post-fold framing flips lead from protocol-layer-pitch
to product-with-verified-identity-pitch.

**Recipient list** (from `co.aweb/outreach/contacts.md` and
`co.aweb/outreach/daily/2026-05-07-direct-outreach-post-show-hn.md`):

1. **Digital Applied** — ecosystem map article
   - URL: https://www.digitalapplied.com/blog/ai-agent-protocol-ecosystem-map-2026-mcp-a2a-acp-ucp
   - Channel: site contact form first; Twitter DM to article author
     as fallback
   - Priority: HIGH (visual ecosystem-map inclusion is shareable
     forever)

2. **NxCode** — "The Agentic Web Explained" author
   - URL: https://www.nxcode.io/resources/news/agentic-web-agents-md-mcp-a2a-web-4-guide-2026
   - Channel: site contact, Twitter
   - Priority: HIGH

3. **DEV Community / pockit_tools** — "MCP vs A2A Complete Guide"
   - URL: https://dev.to/pockit_tools/mcp-vs-a2a-the-complete-guide-to-ai-agent-protocols-in-2026-30li
   - Channel: DEV Community comment on the article (permanent + visible)
   - Priority: HIGH

4. **GetStream** — "Top AI Agent Protocols in 2026"
   - URL: https://getstream.io/blog/ai-agent-protocols/
   - Channel: harder (company blog); contact form / Twitter
   - Priority: Medium

5. **Context Studios** — "ACP vs MCP: Protocol War"
   - URL: https://www.contextstudios.ai/blog/acp-vs-mcp-the-protocol-war-that-will-define-ai-coding-in-2026
   - Channel: site contact / Twitter
   - Priority: Medium

**Post-fold framing skeleton** (from Iris's step 2 audit — exact
text pending her step 3 re-author):

```
[Open] "Great article on [their specific topic]. We've been building
aweb — where AI agents live as a team, with their own identities and
shared coordination state.

[Layer claim] MCP is agent-to-tool, A2A is task delegation, aweb is
who's on the team and what's claimed. Different layer; complementary
to both.

[Identity beat] Agents have cryptographic identities through awid
(our open identity registry — own brand, any service can verify
against it).

[Link] Open source, MIT: github.com/awebai/aweb

[Close] Thought it might fit your [map / comparison / guide].
Happy to share more if useful; no pressure. Thanks either way."
```

**When**: Stagger ~30 min apart on a Tue/Wed/Thu. Eugenie sends;
Juan reviews before each.

**Capture**:
- Per-recipient: did they reply, what did they say, did they
  update their article.
- After 2 weeks: any new inclusions in their ecosystem maps.
- Public `publishing/history.md` (date + channel + observed
  response, attribution caveats); private `co.aweb/outreach/history.md`
  for recipient-specific details.

**Status**: HOLD until Iris re-author lands (step 3, next active
cycle). Estimated 1-2 days. Don't send the pre-fold version unless
Juan calls it.

---

## Action 5 — Dev.to comment on pockit_tools MCP vs A2A guide

**Priority**: Medium. Adjacent to Action 4 but lower stakes
(comment, not direct mail). Same audience reaches via comment
visibility on a popular guide.

**Where**: https://dev.to/pockit_tools/mcp-vs-a2a-the-complete-guide-to-ai-agent-protocols-in-2026-30li
(sign in to DEV Community; comment box at bottom of article).

**What** (starter scaffold — Iris voice-pass before send):

```
Nice breakdown of the MCP/A2A surface area. One layer that's
under-discussed in protocol comparisons: agent identity and
coordination. Neither MCP nor A2A handles "who are you, who else is
on the team, what's claimed" — that's left out of scope.

We built aweb (github.com/awebai/aweb, MIT) for that gap. Agents get
cryptographic identities through an independent registry (awid),
exchange signed messages, and hold persistent task claims so multi-
agent workflows don't duplicate work. It composes with MCP (agents
have access to their tools) and A2A (agents delegate tasks); aweb
adds the identity and presence layer beneath both.

Open source, self-hostable. Worth a look if anyone hits the
coordination gap.
```

**When**: Same window as Action 4 (Tue-Thu morning US Pacific).
Could go before or after the direct mails.

**Capture**:
- Dev.to comment likes / replies.
- Plausible referral from dev.to.

**Status**: READY pending Iris voice-pass (a tighter draft than
Action 4 since the channel is comment-shaped, not mail-shaped).

---

## Action 6 — Pi extension promotion

**Priority**: Medium-high (new product surface, P3 audience,
shippable artifact).

**Pi extension is `@awebai/pi` on npm** — wakes Pi (pi.dev) sessions
on aweb channel events, bundles aweb skills. Real, packaged,
shippable since ~2026-05-23 (version 0.1.8 per Hestia commit
`4be8263`).

**Where**: PENDING IRIS DISCOVERY. Open questions for her step 3:
- Does Pi (pi.dev) have a community forum, Discord, or other
  channel where users discuss extensions?
- Is there a Pi-specific subreddit?
- Twitter mentions of @pidev or similar?
- Pi's own changelog / blog where extensions get featured?

**What** (general shape — not posted anywhere yet):
- The framing Iris flagged in her step 2: "multi-agent coordination
  in Pi" with `@awebai/pi` as one tool in the answer. Not "what you
  can do with @awebai/pi" (that's marketing-shape, violates "be
  useful or stay silent"); rather a piece that solves a Pi-user
  problem, where the extension is one ingredient.

**When**: After Action 1 (r/ClaudeCode) signal is captured. The
Pi audience overlaps with r/ClaudeCode; sequencing matters.

**Capture**: npm download stats on `@awebai/pi`; any Pi forum
engagement; Plausible referrals from pi.dev sources.

**Status**: HOLD pending Iris's community discovery (step 3).

---

## Action 7 — Twitter thread P1 launch (parked)

**Priority**: Medium. Drafted weeks ago at
`publishing/drafts/2026-05-13-twitter-thread-p1-launch.md`.
Substance viable per Iris's step 2 audit.

**Pending** three re-checks before ship (per Iris step 2):

1. Re-query Tweet 3's "zero hosted-MCP-to-hosted-MCP traffic"
   claim against current data. The landscape shifted: 46/347 (~13%)
   team_and_contacts adoption per Hestia 2026-05-23.
2. Walk-the-flow at v0.5.48 under P1 tooling to confirm "wire each
   AI once → sticks" still holds. v0.5.47 default for new global
   agents is now "All" (open); picker visible only on global
   identities.
3. Athena tech-accuracy re-pass after the two checks.

**Status**: HOLD pending the three re-checks. Worth scheduling after
Action 1-5 if signal from those is positive (twitter thread
re-checks aren't free; ROI depends on first wave's traction).

---

## Signal-capture template

After each action, log to `publishing/history.md` (or
`co.aweb/outreach/history.md` for recipient-specific):

```
## YYYY-MM-DD · [Channel] · [Action description]

**Channel**: [Reddit / Twitter / DEV / direct-mail / etc.]
**Public link**: [URL of the post / comment / mail thread]
**Artifact**: [link to the source draft]
**Audience**: [persona / community]

### Signal observed (timed)

- +1h: [upvotes / impressions / etc.]
- +6h: [same metrics]
- +24h: [same metrics]
- +1w: [retrospective]

### Engagement
- [Direct replies / comments / questions you fielded]
- [How you responded — one comment per thread]

### Attribution caveat
- [What other concurrent factors could explain any uptick]
- [Don't claim causation; capture correlation]
```

Metis tracks signal strength when she's active. Until then,
record honestly with attribution caveats.

---

## Recommended order of operations (when picking what to do first)

1. **Action 1** (r/ClaudeCode post) — lowest effort, highest-fit
   audience, existing asset. Should be the first move.
2. **Action 5** (Dev.to comment) — adjacent comment on popular
   guide. Quick.
3. **Action 2** (Twitter tweet) — 24-48h after Action 1.
4. **Action 3** (HN watch setup) — one-time setup; then daily
   5-min scan ongoing.
5. **Action 4** (5 direct mails) — once Iris re-authors. Eugenie
   sends, Juan reviews each before send.
6. **Action 6** (Pi promotion) — once Iris discovers community
   channels and authors a Pi-user-problem-shaped piece.
7. **Action 7** (Twitter thread P1) — only after Iris's three
   re-checks clear AND first-wave signal looks positive.

Total time for first three actions (the ones Juan can do without
waiting on Iris): ~30 min if everything is voice-clean. Less if
Juan adapts the scaffolds himself.

---

## What HOLDS for Iris's step 3 deliverable

Iris is mid-cycle on:
- `publishing/plan.md` adaptation (post-fold framing, persona model
  overlay, Pepe customer-evidence as dogfood material, Pi extension
  promotion arc, OpenClaw-as-daemon substitution).
- `publishing/runbook.md` adaptation (daily scan/draft/Juan-review/
  publish/track loop adapted to current team shape).
- Bounded promotion bundle for "Pair Your Coding Agent with a
  Reviewer" — same Action 1 scope as above, with her voice-pass
  refining the Reddit post text.
- Five direct-outreach drafts re-author under fold framing
  (Action 4's "exact text" deliverable).
- Pi extension promotion piece (Action 6's "what" deliverable).

When her step 3 lands, this playbook revises to v1:
- Action 1 text upgrades from "starter scaffold" to
  "Iris-refined."
- Action 4 unblocks with exact recipient-specific text.
- Action 5's dev.to comment upgrades to Iris-refined.
- Action 6's Pi channel question gets answered.

Estimated time: 1-2 days based on Iris's step-1 + step-2
turnaround pace.

---

## What's NOT in this playbook

- **No "post to HN" action**. The article is 3 weeks old; no news
  hook; would sink. HN stays read-only watch.
- **No LinkedIn or Product Hunt actions**. Per BeadHub-era strategy
  (which Iris is adapting): defer LinkedIn until post-HN-traction;
  Product Hunt needs broader story + 10-20 ready commenters. Both
  premature.
- **No P1 (personal-AI consumer) direct outreach** in this wave.
  The article is P3-shaped; Twitter (Action 2) is the only P1-
  adjacent touch and even that's incidental. P1 outreach is a
  separate wave when there's a P1-shaped asset (the Twitter thread
  P1 launch in Action 7, once unblocked).
- **No cold-DM blasts.** Each direct mail in Action 4 is a single,
  considered, recipient-specific message. Five total, staggered.

---

## End of playbook v0

Sofia, 2026-05-26. Iris framing-pass converts to v1.
