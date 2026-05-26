# Publishing History

What we published, where, and when. Newest first.

Per `publishing/runbook.md` Case 6: each entry captures date,
channel, public link, artifact used, humans who acted, observed
signal, attribution caveat.

---

## 2026-05-08 · "Pair Your Coding Agent with a Reviewer" — Juan published on juanreyero.com (captured retroactively 2026-05-26)

> **Tracking gap (banked):** this post shipped 2026-05-08 but was not captured in publishing/history.md at the time. The outreach side (Iris) was tracking it as "still pending" in entries dated 2026-05-11, 2026-05-12, 2026-05-13 — those entries are accurate-for-their-date in voice but factually wrong about ship state. The 2026-05-26 outreach pivot audit (step 2 parked-artifact review) surfaced the actual ship. Banked discipline for next time: before treating a handoff entry as current, verify the ship state of any "awaiting commit/push" or "on X's plate" item — author-owned surfaces (juanreyero.com here) can move underneath the handoff. The "still pending" mentions in subsequent entries reflect the gap, not a re-assessment.

**Channel**: juanreyero.com (Juan's personal site, blog format)
**Public link**: https://juanreyero.com/article/ai/two-agents-not-one/ (URL slug preserves original "Two Agents Not One" working title; page title is "Pair Your Coding Agent with a Reviewer")
**Artifact**: Juan-authored long-form post. Draft chain captured in earlier publishing/drafts/ history; final shipped under Juan's own voice from his own surface. Not in publishing/drafts/ because the publication path was his own repo.
**Audience**: P3 (developer team) primary — practitioners running 1+ coding agent who are ready for the pair shape. Adjacent overlap with P1 if a daily-AI-user discovers the post.
**Voice**: founder first-person; no marketing-shape; "the simplest improvement you can make"; ends with concrete next step.

### Live shape

Lead with the move: "The simplest improvement you can make to your agentic programming workflow is to run two agents instead of one." Pair-shape (builder + reviewer in parallel worktrees, shared task list, post-TDD-cycle handoff). Names aweb explicitly: "open-source coordination layer for AI coding agents." Links to aweb.ai + github.com/awebai/aweb.

### Signal (post-ship, deferred — outreach didn't track at the time)

Empirical signal not captured at ship time. Plausible was not live on juanreyero.com (it tracks aweb.ai), so no referral or page-view data on the post itself. Any referral traffic from juanreyero.com → aweb.ai would have shown in Plausible after 2026-05-16 (Plausible live date); pre-2026-05-16 referrals are unobservable from our side.

Signal worth retro-capturing if available:
- juanreyero.com analytics on the post (if Juan tracks anything on his own site)
- Cross-channel discussion: was the post linked anywhere (Reddit, HN, Twitter, dev.to)?
- Any signups attributable to juanreyero.com referral after Plausible went live 2026-05-16

### Cross-channel promotion (not done)

The post was not promoted to Reddit / HN / Twitter from the outreach side. The Twitter thread P1 draft (2026-05-13) was an independent track, not a promotion-of-the-post track. Post-publish promotion is a deferred follow-up question for the outreach pivot.

### Attribution caveat

If any signups, signal, or signal-on-the-blog arrived between 2026-05-08 and 2026-05-26 that's attributable to this post, the outreach side missed the attribution window for direct capture. Future outreach signal that mentions the post can cite it as one upstream factor.

---

## 2026-05-14 · aweb welcome guide v5 — committed to AC-canonical path (Juan blessed)

> **SUPERSEDED 2026-05-16 by AC commit `052530aa`** (aaoq + aaor paired wave). `welcome.md` deleted; customer-facing surface migrated to `ac/backend/src/aweb_cloud/resources/mcp-tutorial.md` (aweb-canonical, synced via Makefile). `load_welcome_guide()` in `hosted_mcp.py` reads `mcp-tutorial.md` from that commit forward. `AWEB_HOSTED_MCP_INSTRUCTIONS` rewritten in the same wave; the v5 serverInfo string quoted below was replaced. Both live surfaces are free of the deprecated `send_message_to_contact` / `read_messages_from_contact` aliases referenced in the v5 tools list. This entry stands as accurate-for-its-date record of what shipped 2026-05-14; do not treat it as current customer surface.

**Channel**: `aweb_welcome_guide` MCP tool + `aweb://welcome` MCP resource (hosted MCP server at app.aweb.ai/mcp/)
**Public link**: returned at runtime by the MCP tool; not a public URL
**Artifact**: `ac/backend/src/aweb_cloud/resources/welcome.md` (ac commit `95481339`, main; **deleted 2026-05-16 by `052530aa`**)
**Source draft**: `publishing/drafts/2026-05-14-aweb-welcome-guide-v1.md` (ai.aweb commit `80cb00d`; superseded marker added 2026-05-23)
**Audience**: AI clients on first connection (ChatGPT / Claude Desktop / claude.ai) — semi-spec, AI-facing
**Word count**: ~440 (within Athena's 200-500 target)

### Cross-cutting review chain (1 day)

- v1 → v2 (Iris): folded Aida's pre-think relayed via Athena `204e971e`
- Sofia framing review: approved (mail `55bed1b7`) with cross-surface alignment ask
- v3 (Iris): Athena tool-name lock — `create_contact_invite` → `create_invite_link` per Grace's commit `c6f270e8` (mails `a58bc12b`, `69ed8365`)
- v4 (Iris): Athena tech-accuracy revisions — lifecycle two-paths (invite-link bilateral-active; pending only on handle-add); send-on-pending errors (not queues; verified at `contacts.py:101+`); `read_messages_from_contact` added; source-of-truth path locked AC-canonical (mail `dfeb103a`)
- v5 (Iris): Athena v4 clear + `contacts_remove` nit folded (mail `6b88d7bb`)
- Aida support-integration clear (mail `e197415a`) — all 6 pre-think checkpoints satisfied; one runbook-intake question shape banked, not authored
- Juan bless: 2026-05-14 (relayed via Athena mail `39b75bbd`)

### Parallel artifact: serverInfo.instructions v5 (495 chars)

Same review chain, same bless. Ready to wire by Grace into the FastMCP constructor.

> aweb gives the AIs you use addresses; they message each other directly. The user just connected this AI. To start: offer to create an invite link for a friend — ask for their first name, then call `create_invite_link`. Tools: create_invite_link, add_contact_by_handle, contacts_remove, list_contacts, send_message_to_contact, read_messages_from_contact, aweb_welcome_guide (call for fuller context). When phrasing to the user, use friend/contact/address/message — not team, role, namespace.

### Signal (post-ship, deferred)

Empirical signal pending. Hosted-MCP-agent-to-hosted-MCP-agent flow had zero exercises in production over the past two weeks (Athena query 2026-05-13 in tweet-3 tech-accuracy mail `366ca36e`). The welcome guide is part of the surface that converts new MCP-connect events into first-action attempts. Signal to watch: invite-link create attempts within N minutes of OAuth grant on hosted custodial consumer agents; replies-to-friend-invites; mutual-active contact pairs created.

### Attribution caveat

The welcome guide is AI-context priming, not user-facing copy. Direct attribution to specific user actions is structurally weak — the AI mediates. Signal-strength judgment goes through Metis when she's active.

---

## 2026-05-13 · aweb.ai homepage — pain-narrative rewrite verified-live

**Channel**: aweb.ai (landing page)
**Public link**: https://aweb.ai/
**Artifact**: `deploy-landing` commit `21cb6c23` (also `main` HEAD —
same SHA carries v0.5.31 backend + Peter's pain-narrative + Eugenie's
rewrite + the staging-iteration commits).
**Verified-live**: 2026-05-13 22:28:03Z (Hestia mail `01e7154d`).
**Source-of-truth doc**: `docs/audiences.md` (persona model, P1
priority per decisions.md 2026-05-12)
**Voice principles**: `publishing/voice.md` (persona-aware update
2026-05-12)

### Live copy as shipped

- **`<title>`**: "aweb — AI coordination, without you"
- **Hero kicker**: "For the AIs you already use"
- **Hero h1**: "You're still doing the work / your AI should be doing"
- **Hero subhead**: "You copy. You paste. You relay. You chase.
  Every time your AI needs something from someone else's AI, you
  step in the middle — as the most expensive messenger in the
  room. aweb lets your AIs talk to each other directly. You give
  the direction. They do the coordination."
- **Primary CTA**: "Connect your AI" → `app.aweb.ai/connect`
- **Secondary CTA**: "Get started" → `app.aweb.ai/register?source=consumer`
- **Hero note (trust + works-with merged)**: "Works with ChatGPT,
  Claude, and other AIs · Free to start · No credit card required."

### Cycle arc to current ship

- **2026-05-08**: Bertha brief from Eugenie's non-technical-founder
  observation (chat `53251bb9`).
- **2026-05-09 → 2026-05-11**: Iris-authored Pass-1 (commit
  `58ed6c53`) deployed-and-reverted; Sofia-authored Pass-3
  customer-shape correction (`60be8f4e`) on `deploy-landing-staging`;
  Pass-3 verified-live briefly on 2026-05-11 then reverted same day
  per Juan's small-technical-error call (Bertha chat `4a4a0573`).
- **2026-05-12**: Juan resets persona priorities to P1 (personal-AI
  consumer) first, P3 (developer team) third. `docs/audiences.md`
  rewritten; `publishing/voice.md` updated to persona-aware framing
  with customer-shape verification + four persona-ordered pitches.
- **2026-05-13**: Peter-authored pain-narrative rewrite + Eugenie
  iteration ships via staging gate. Different shape from Pass-3 —
  pain-recognition opener now leads with "you're still doing the
  work" (the human-as-messenger framing) rather than "you're already
  running a team of AIs." Same persona target (P1), different
  framing register.

### What carried from earlier cycles vs what changed

**Carried**:
- The customer-shape verification discipline (P1 = browser-custodial-
  MCP audience that cannot run shell commands) — banked
  2026-05-11, refined into voice.md 2026-05-12, applied in this
  rewrite's structure.
- Honest framing of what works today (no "your agent handles the
  rest" overclaim that survived through Pass-3).
- "Connect your AI" CTA → `/connect` (the AC frontend picker route
  Athena flagged on 2026-05-11; Grace's aweb-aanp.8).

**Changed**:
- Hero hook: "You're already running a team of AIs" (Pass-3) →
  "You're still doing the work your AI should be doing" (live).
  Both target P1; latter foregrounds the human-as-messenger pain
  more concretely.
- "Sign up. Your agent handles the rest." onboarding section: gone
  from the live shape. The pain-narrative carries the messaging-
  layer rather than a separate signup walkthrough.
- Works-with strip (4 text pills) dropped. Replaced by inline
  "Works with ChatGPT, Claude, and other AIs" in the hero-note.
- Pillars section heading change preserved-in-spirit but the
  specific "Each AI you're running is isolated. aweb changes
  that." phrasing not on the live page per current curl.

### Humans who acted

- Bertha relayed Eugenie's brief + customer-voice direction
- Peter authored the pain-narrative rewrite
- Eugenie iterated on Peter's draft
- Juan reset persona priorities + greenlighted the technical fix
  + greenlighted the production deploy
- Sofia framing review across cycles + the persona reorder doc
- Athena (+ Olivia) consumer-flow corrections (ChatGPT-tier matrix,
  Pepe-anonymous, provider-agnostic signup, handle-only add-a-friend)
- Iris early-cycle authoring + Pass-1 ship-and-revert + voice.md
  persona-aware update
- Hestia deployed via the staging gate (eat-our-own-dog-food shape;
  first cycle's gate failure → fix → second cycle's clean gate run)

### Observed signal

Signal-observation window opens at 2026-05-13 22:28:03Z verified-live.
Signal categories to watch over the coming days/weeks:

- Direct traffic to aweb.ai (week-over-week from the Hestia-deploy
  moment)
- Signup conversion at `app.aweb.ai/register?source=consumer`
  (source query param enables attribution if Metis instruments it)
- `/connect` route entry rate (CTA "Connect your AI" engagement)
- Inbound conversations from P1-shape customers (personal-AI users
  asking how to connect their AI to a friend's AI)
- Repo stars / inbound on github.com/awebai/aweb
- Direct-outreach response signal (5 drafts queued in
  `co.aweb/outreach/daily/2026-05-07-direct-outreach-post-show-hn.md`;
  none sent yet)

Metis is the signal-strength reviewer when she's online;
attribution claims gate through her.

### Attribution caveat

This live ship is one event in a longer arc — Pass-1 ship-and-
revert + Pass-3 brief-live + persona reorder + pain-narrative
rewrite together inform any signal observed in the days following.
Concurrent factors include the (still pending) "Two Agents Not One"
juanreyero.com article + 5 queued direct-outreach drafts + any
organic discovery + the Show HN sink on 2026-05-07 still
contaminating any HN re-discovery. Capture correlation; don't
claim causation.

---

## 2026-05-11 · aweb.ai homepage refresh (Pass-3) — verified-live, then reverted

**Channel**: aweb.ai (landing page)
**Public link**: https://aweb.ai/ (currently serving pre-refresh
content; Pass-3 was live ~few hours then reverted same day)
**Artifact**: `deploy-landing` commit `60be8f4e` (Pass-3) live
from ~14:36Z 2026-05-11 to revert commit `f1a07f93` (no
verified-revert-time in my receipts; Bertha relay 2026-05-11
confirmed revert was Juan's call). Pass-3 stays preserved on
`deploy-landing-staging` branch.
**Source-of-truth doc**: `docs/customer-onboarding-flows.md`
(customer-shape model, Shape A / Shape B / Shape C, established
2026-05-11 by Sofia)
**Narrative record**: `publishing/drafts/2026-05-09-homepage-copy-refresh.md`

### Revert (2026-05-11, same day)

Pass-3 was reverted from production a few hours after the
verified-live signal. Bertha relay (chat `4a4a0573`, 2026-05-11
evening): "Juan found a small technical error — that's the only
reason for the revert. He's fully on board with the Pass-3
framing. Once the fix is in, it should be straightforward to
re-deploy."

What this means for the record:
- The Pass-3 framing decisions (customer-shape correction, hero
  reframe, MCP-connector card, three-step walkthrough, pillars
  heading change) remain validated by Eugenie + Juan greenlight.
  The revert is technical, not framing.
- A future re-deploy with the technical fix in place will return
  Pass-3 (or a Pass-3+fix variant) to production. The disciplines
  banked from this cycle hold for that future re-deploy.
- The earlier-published version of this history entry described
  Pass-3 as continuously live; that was Iris's pre-revert-aware
  capture (commit `069c415`). Corrected here in-place once the
  revert + reason became visible.

### Signal observation window during the brief Pass-3 live period

Pass-3 was live for ~few hours. Too short for week-over-week
traffic comparison; too short for signup-conversion movement
to register meaningfully. No signal claim from this window.

The next Pass-3 re-deploy (with technical fix) restarts the
signal-observation window from the new verified-live date.

### What changed

Hero h1 + subhead reframed around concrete customer surfaces
(Claude Desktop / ChatGPT / claude.ai) instead of vocabulary-
translation framing ("those are agents") that confused vs. served
the audience.

NEW works-with strip between hero and pillars (text pills,
4 items: Claude / ChatGPT / Claude Desktop / Any MCP-compatible
AI). NEW "Sign up. Add aweb to your AI client." section with
honest 3-step walkthrough (signup + hosted identity → copy MCP
URL → add to client + approve OAuth) targeting Shape A custodial-
MCP customers. Per-client snippets for claude.ai web /
ChatGPT web / Claude Desktop.

Pillars section heading text replaced from "Give each agent an
identity. Then let them coordinate." to "Each AI you're running
is isolated. aweb changes that."

Team-quickstart section relabeled "For developers" — the
agent-guide-paste prompt (CLI-shape onboarding) lands there
as the Shape B customer entry point. Hosted MCP block
repurposed as MCP technical-detail callout.

### Cycle arc

- **2026-05-08**: Bertha brief (chat `53251bb9`) — Eugenie
  observed a non-technical founder running multi-Claude not
  recognizing "agents" as describing her situation.
- **2026-05-09**: Iris-authored bundle in publishing/drafts/.
  Sofia framing-pass landed; Athena agent-guide pre-flight
  flagged four human-required steps in the autonomous-install
  flow. Two-state-transition framing engineered (Option A
  interim → Option B post-aang).
- **2026-05-10**: aweb-aang (worktree-creation-on-hosted) +
  three other P0 frictions verified-live across single-team and
  multi-team-agent populations (Pepe Reyero customer-evidence
  arc, banked at `co.aweb/outreach/customer-evidence/2026-05-09-pepe-autonomous-install.md`).
  Iris-authored bundle commit `58ed6c53` to ac main — Pass-1
  briefly deployed and reverted; gate gap caught by Juan
  (Render watching main produced an unintended ship; staging
  gate didn't yet exist).
- **2026-05-10 → 11**: Athena seeded `deploy-landing-staging`
  branch + `make deploy-staging` target. Juan configured Render
  staging service. Sofia caught a Pass-2 customer-shape mismatch
  (Shape A customers given Shape B flow) and authored Pass-3
  corrective edits directly under time pressure (commit
  `60be8f4e`). Customer-shape model persisted in
  `docs/customer-onboarding-flows.md`.
- **2026-05-11**: Bertha relay confirmed Eugenie validated Pass-3
  on staging (chat `47e3b6bd`); Juan greenlighted; Sofia framing
  review long-since done. Hestia ran `make deploy-site`,
  verified live at aweb.ai (mail `f0ac616f`).

### Humans who acted

- Bertha relayed Eugenie's brief and validation
- Eugenie reviewed Pass-3 on staging
- Juan greenlighted production
- Sofia authored Pass-3 customer-shape correction directly
  (lane-cross under time pressure; re-routed back to Iris
  for Pass-4 if needed)
- Hestia deployed + verified live

### Observed signal

Not yet observed at history-capture time (deploy ~14:36-14:39Z
2026-05-11). Signal categories to watch over the coming weeks:

- Direct traffic to aweb.ai (week-over-week)
- Signup conversion at app.aweb.ai/register
- Inbound conversations from custodial-MCP customers (Shape A;
  the audience the refresh now actually serves)
- Repo stars / inbound on github.com/awebai/aweb

Metis is the signal-strength reviewer when an action runs;
attribution-strength claims gated through her.

### Attribution caveat

This is one event in a multi-channel pivot following the
2026-05-07 Show HN sink. Any signups / traffic / engagement
movement in the days following this deploy is correlated with
the homepage refresh, not solely caused by it — concurrent
factors include the (still pending) "Two Agents Not One"
juanreyero.com article, the queued direct-outreach drafts
(co.aweb/outreach/daily/), and any organic discovery. Capture
correlation; don't claim causation.

### Disciplines banked from this cycle

In `agents/iris/AGENTS.md`:

- Submit-state changes surface to direction same-shift
  (banked 2026-05-07)
- Verify Pass 1 is shipping (not just drafted) before
  committing to a two-transition framing (banked 2026-05-09)
- Surface gate-stalls to direction explicitly (banked 2026-05-09)
- `publishing/drafts/*.md` is narrative, not a wire-in spec
  (banked 2026-05-10)
- Customer-shape verification before authoring landing-copy
  (banked 2026-05-11; source-of-truth `docs/customer-onboarding-flows.md`)

In Sofia's surface (her banking pending): verify the empirical
customer-facing surface before claiming a state transition or
triggering downstream dispatches based on it.

### Operational firsts

- First cycle through the new staging-first deploy gate
  (Render: deploy-landing for production, deploy-landing-staging
  for staging). The gate caught one out-of-order deploy mid-cycle
  (Pass-1 hit production via Render-watching-main before staging
  branch existed); the gate fix landed and Pass-3 ran through
  cleanly.
- First entry in this `publishing/history.md` artifact.
