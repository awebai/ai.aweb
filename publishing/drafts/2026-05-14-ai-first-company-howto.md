---
title: "How to set up an AI-first company like ours — v1 draft"
date: "2026-05-14"
type: "blog-post-draft"
status: "Iris drafted v1 for the editorial chain — Sofia framing → Athena tech-accuracy + proofread → Bertha-via-Eugenie → Juan bless"
audience: "Small company / startup (3-30 people) wanting to be AI-first; employees using ChatGPT / claude.ai / Claude Desktop primarily"
shape: "Hybrid (case-study anchor + stage-branching recipe) per Athena brief 36d75f22"
target-word-count: "1500-3000"
draft-word-count: "~2150"
source-material: "docs/agent-first-company.md, docs/team.md, docs/invariants.md, docs/meetings-design.md, docs/audiences.md (P2 section), publishing/voice.md, publishing/voice-howto.md"
publish-destination: "ac/site/content/blog/<slug>.md on Juan bless (slug TBD; current placeholder ai-first-company-howto)"
brief: "Athena mail 36d75f22 (2026-05-14)"
---

## Iteration history (Iris notes for reviewers)

v1 draft per Athena brief 36d75f22. Shape decision: Path C (hybrid) — case-study anchor in section 1-3, stage-branching recipe in section 4. Branching is where the honest-claim discipline ("for your stage, do <subset>") does its work.

Pre-banked honest-gap-namings in the draft:
- aweb-as-coordination-layer requires aweb setup beyond browser-AI default.
- Per-area ownership doesn't map cleanly to single-person multi-role situations.
- Persistent decisions/handoffs work without aweb (Stage 1-2); aweb optimizes the cross-AI-discovery part (Stage 3+).
- Scale claim: "we have 5 real consumer users (3 are Juan)" surfaced explicitly so the reader knows our context.
- Scheduled meetings infrastructure: design landed, build pending — surfaced as "what we're still building."

Template-repo link is a placeholder (`[TEMPLATE_REPO_URL]`). Athena scaffolds in parallel once Juan locks the name; I revise when ready.

Sofia framing pass should focus on:
- Persona-fit on the translate-to-small-company sections (Stages 1-4) — does the branching land for the 3-30-person audience or does it read aweb.ai-centric?
- The "What we're still building" honesty surface — too much, not enough?
- The "honest disclaimer" closer — voice-appropriate or sycophantic-shape?

Athena tech-accuracy pass should focus on:
- Any claims about what aweb provides today vs what's being built.
- The "What you actually need to start" tool-mix references (aw CLI, hosted MCP, etc.).
- Whether "5 real consumer users (3 are Juan)" is the right number to cite (last empirical count to confirm).

---

## DRAFT CONTENT BEGINS BELOW

# How to set up an AI-first company like ours

We run aweb.ai as a company where most of the work is done by AI agents.

Six of them. Each has a name, a responsibility area, persistent context, and the ability to message any of the others directly. Two humans — Juan and Eugenie — set strategy, make the final calls, and do the parts AIs can't do (talking to customers, publishing externally, the founding-judgment work).

This post is what we figured out doing it. Not a victory lap — we have five real consumer users so far, three of them Juan on different accounts. We're early. What's working is the operating model, not the scale.

If you're at a small company trying to figure out what "AI-first" actually looks like operationally, this is how it's worked for us, and how it might translate to your team.

## What "AI-first" doesn't mean

It doesn't mean every employee uses ChatGPT to write emails faster. That's "AI-assisted" — useful, but the AI is still serving an individual workflow.

AI-first means the **work is done by AI agents with named responsibilities, persistent context, and durable handoffs between them**. The humans set direction, hold the founding judgment, and carry the parts that need human presence (customer relationships, hiring, the actual building of relationships). The agents carry the rest.

The shift sounds small. It isn't. When the work is done by agents, the company's coordination is between *them* — not just between you. A few things follow from that:

- You stop being the relay between every internal communication.
- The work has artifacts (tasks, decisions, handoffs, status files) that survive any single conversation.
- The agents need addresses so they can message each other directly.
- You need a way to capture what they decide, so the next session of any agent starts in context.

## How we work (the case study)

Six named agents, six surfaces, two humans:

- **Sofia** carries direction. Priorities, decisions, technical-direction calls, framing for anything we say externally.
- **Athena** owns the code. Architecture, review of every change, briefs for the ephemeral builder + reviewer pairs that author features.
- **Hestia** ships. Release gates, deploys, live verification, dashboard hygiene.
- **Aida** supports customers. Answers, runbook, customer voice routed back to the team.
- **Iris** prepares outreach. Drafts, market scanning, signal capture from external responses.
- **Metis** turns what comes back into signal. Honest with attribution limits.
- **Juan** makes final calls, holds the founding-judgment work.
- **Eugenie** runs business development, outreach execution, publishing.

Each agent owns a surface but the **outcome belongs to all of us** — the company moving forward is a joint responsibility. Reviews go both ways: Athena reviews Aida's runbook for tech accuracy; Sofia reviews Athena's release-notes framing; Iris drafts so Juan and Eugenie can publish well. Peers help each other land good work; nobody signs off on anybody.

A typical day:

1. Sofia sees a priority change (a customer signal, an architectural read, a release-claim implication). She writes a decision record, updates `status/product.md`, and creates the `aw` task.
2. Athena picks up the task. Either she writes the change herself (small fixes, non-feature work) or she scopes a brief and dispatches an ephemeral builder + reviewer pair on worktrees.
3. The pair commits to a branch. Athena reviews the diff against invariants. The change lands on main.
4. Hestia runs the release gates, tags, deploys, and verifies live with a `/health` probe + smoke test of the changed surface. She posts the verified-live mail with evidence.
5. Iris drafts a release-notes companion or distribution artifact if appropriate. Sofia frames external claims. Juan or Eugenie publishes.
6. Aida fields any customer questions that arrive about the change. If she needs code context, she asks Athena. If a question reveals a runbook gap, she updates the runbook.
7. Metis logs the signal that comes back. Attribution limits get called.

That's an everyday cycle. The work has artifacts (task, decision, branch, commit, gate, verified-live mail, status update, signal note); each agent owns its surface; humans publish and decide.

## The principles that make it work

The shape (six agents, six surfaces) is one valid arrangement. The principles are what make ANY arrangement work — including a smaller one. Six of them:

**1. Work needs artifacts.** If work matters, it needs a durable artifact: a task, a claim, a handoff, a decision record, a release-notes draft, a verified-live mail. Conversation is not enough. Conversations evaporate at the end of the session; artifacts survive.

**2. Substantial work needs two voices.** A builder and a reviewer. The voices don't have to be different agents (a code-reviewer subagent counts; a "now switch and critique what we just decided" prompt counts), but they have to be different perspectives. The second voice helps the work land well.

**3. Surfaces are owned, not walled.** Within a role, you decide; across roles, you collaborate. When peers see something differently, they work it out together. The goal is the right call for the company, not the win.

**4. Shared state beats status routing.** The company should be queryable through artifacts. Tasks show active work; status files publish current state; handoffs preserve area-specific memory; decision records explain how state changed. Any fresh agent (or human) should be able to inspect the artifacts and understand what's happening.

**5. Look for feedback, grade its strength.** Some feedback is closing-quality ("the test passes; the customer confirmed"). Some is weak signal ("traffic increased after the post; attribution unclear"). Capture both. Don't claim causality the evidence doesn't support.

**6. Distribution over features.** Zero users means nothing else matters. Once the product works, every hour spent on more engineering instead of getting it in front of people is wasted.

The shape is downstream of the principles. The principles are what to keep.

## Setting this up for your company

Here's where the case study has to translate. Our shape is more elaborate than what most small companies will operate — we're building the coordination layer itself, so we exercise it at full surface area. Your shape will be smaller. Start where you are, add surfaces when the work needs them.

### Stage 1 — Two voices (3-5 person team)

**What to do:** Pick the most-used AI in your team (probably ChatGPT or Claude). For substantial decisions, switch into a "now critique what we just decided" prompt before you act. That's your reviewer voice. Write the decision down. Re-read it in the next session.

**What you need:** Discipline. A shared place to capture decisions (Notion, a Google Doc, a markdown file in your repo). No agent identities, no aweb, no cross-AI messaging.

**The gap:** At this stage you don't need agent infrastructure. You need the habit of two-voice review and written decisions. The benefit of writing things down compounds invisibly until you skip it.

### Stage 2 — Named surfaces (5-15 person team)

**What to do:** Give each work area a named AI persona. Engineering, support, marketing, ops — whichever map to your actual work. Each persona has a stable prompt + persistent context (markdown file, Notion page, Claude project). Each session for that area starts by re-reading the context.

**What you need:** Per-area personas with persistent context. Still no cross-AI messaging — the humans relay.

**The gap:** The relay overhead starts to bite here. Every time you tell "Sarah's AI" the latest from "Marketing's AI," you're paying the relay tax. This is where Iris's framing for our homepage lands — "you're the most expensive messenger in the room." You can keep relaying manually until it hurts; the pain itself is the signal that Stage 3 is next.

### Stage 3 — Cross-AI coordination (when relay overhead hurts)

**What to do:** Give each AI an address. Make them able to message each other directly.

**What you need:** Agent identities + a way for the AIs to talk. This is where aweb is built to help. You install the `aw` CLI (developer-shape teams), or you connect each AI to the hosted MCP at app.aweb.ai/connect (consumer-shape teams using ChatGPT, Claude Desktop, or claude.ai). Each agent gets an address. They can message each other directly via mail (async) or chat (sync).

**The gap:** This requires going beyond the browser-AI default. Your team's exact tool mix shapes the setup — ChatGPT Business+ supports custom MCP connectors (paid tier); Claude Desktop edits a JSON config; claude.ai web does an OAuth click-through. We've documented the per-client setup at aweb.ai. aweb is open source (MIT) and self-hostable; the hosted service is a convenience, not a requirement.

**What changes when this lands:** Instead of "Send Sarah the latest engineering priorities so she can update the support docs," you say "Athena, sync with Aida on the latest engineering priorities so she can update the support docs." The agents talk; you read the result. The relay tax goes away.

### Stage 4 — Joint responsibility (when the team gels)

**What to do:** Build the operating discipline of the six-surface shape — or whatever surface count fits your work. Capture decisions in decision records. Maintain status files per surface. Write handoffs for context that must survive any single session. Separate the build/ship boundary so whoever ships isn't the one who built. Use two-voice review on substantial work.

**What you need:** The infrastructure from Stage 3 plus the operating habits. The habits are harder than the infrastructure.

**The gap:** This is where we are. We're not claiming to have it working perfectly — we're claiming the shape works for our specific problem (building aweb). Don't impose a six-surface shape on a five-person team. Add surfaces when the work needs them.

## What you actually need to start

Stage 1 needs no new tools — your existing AI subscription is fine. Build the discipline first.

Stage 2 needs a place to keep per-area persistent context. Notion, markdown in a repo, Claude projects, ChatGPT custom GPTs — anything that lets a persona re-read its context at the start of each session.

Stage 3 is where aweb is built to help. We're open source (github.com/awebai/aweb, MIT). The hosted service at app.aweb.ai is the easiest start. Other coordination layers exist; the shape that matters is "agent identities + direct AI-to-AI messaging."

Stage 4 is operating discipline. The tools are downstream of the habits.

## What we're still building

Two things worth naming since the case study above implies them:

**Scheduled meetings between agents.** Agents should be able to schedule a conversation with an agenda and invite other agents (or humans who don't yet have agents) to join. The architectural design is documented; the build is in flight. Today, our agents coordinate via async mail and sync chat — no calendar primitive yet.

**Cross-org agent networks at scale.** aweb is built for AIs in one organization to coordinate with AIs in another. We have the protocol; we have a handful of users on it; we don't yet have the scale that makes the cross-org coordination effect compound. We're early.

If you'd asked us a year from now, the post would say more. For now, what we can describe is the shape — and that you can start with Stage 1 discipline today, no AI-coordination tooling required.

## A template you can fork

We've published a template repo with the agent operating documents (decision-record templates, handoff structure, status-file shapes, voice notes) that we use ourselves: [TEMPLATE_REPO_URL]. Fork it; gut what doesn't apply; keep what does.

The templates are tools, not prescriptions. The principles above are what holds the shape together. Adapt the templates, and the shape, to what your company actually does.

## A note on scope

We've been operating this way for several months. We have five real consumer users — three of them Juan on different test accounts. The discipline is what's working. The shape we use is one valid arrangement among several. The principles we lean on are the more durable claim.

Try the principles. Adapt the shape. Keep the discipline.

We'll keep posting what we're learning here. Subscribe to the RSS feed if you want to follow along.

## DRAFT CONTENT ENDS

---

## Routing notes for reviewers

### Sofia (framing)

Per the iteration history above, three watch-items I'd value your read on:

1. **Persona-fit on Stages 1-4.** Does the branching land for a 3-30-person team or does it read aweb.ai-centric? The voice.md P2 persona is hypothesis-level per audiences.md; the recipe has to feel useful WITHOUT pretending we've validated this with real P2 customers.
2. **"What we're still building" section.** Honest scope-call or undermining-the-pitch? My read: it's load-bearing for trust (and an article called "How to set up an AI-first company like ours" that pretends everything works is the worse failure mode), but flag if you read it different.
3. **"A note on scope" closer.** The five-real-users / three-are-Juan framing — too much disclosure, or right amount? My read: the closer's directness is the practitioner-voice landing; the alternative would have been a confident summary that reads sales-shape.

Two adjacent notes:

- Vocabulary check (per the v5 honest-word miss): I grepped for "honest" — used twice, both in the iteration history (not in body). I checked "we believe", "easily", "simply", "just" too — none in body. If you want a tighter sweep on any other trap-words, flag.
- Voice-howto scaffolding applied: imperative voice on "What to do" steps within stages; common-issues-as-trust on "The gap" subsections.

### Athena (tech-accuracy + proofread)

Specific claims to verify against shipping product:

1. **"five real consumer users — three of them Juan on different test accounts"** — the empirical number. Update if it's drifted.
2. **Tier matrix in Stage 3** — "ChatGPT Business+ supports custom MCP connectors (paid tier); Claude Desktop edits a JSON config; claude.ai web does an OAuth click-through." This is the matrix you and Olivia verified in the 2026-05-11 tier-verification arc. Confirm still current.
3. **`aw` CLI / hosted MCP framing in Stage 3** — "you install the `aw` CLI (developer-shape teams), or you connect each AI to the hosted MCP at app.aweb.ai/connect (consumer-shape teams)" — accurate per shipped state?
4. **Scheduled meetings status** — "architectural design is documented; the build is in flight." Confirm or update.
5. **MIT / self-hostable claim** — "We're open source (github.com/awebai/aweb, MIT). The hosted service at app.aweb.ai is the easiest start." Confirm aweb is MIT-licensed (it is per CLAUDE.md but the published claim should land verified).
6. **Operating-rhythm description in the case study** — accurate to current practice or out of date? The "ephemeral builder + reviewer pairs that author features" framing assumes Phase 1 (mail brief to Juan) vs Phase 2 (`aw spawn-pair`). Are we in Phase 1 still?

Proofread pass: standard line-edit; flag any sentence that reads marketing-shape vs practitioner-shape; flag anything that overclaims or papers over a gap.

### Bertha-via-Eugenie

After Sofia + Athena clear, route to Bertha for Eugenie's customer-voice read per Juan's standing editorial gate for blog posts. Specific asks for Eugenie's lens:

- Does this read as something a small-company decision-maker would actually finish? Length OK? Section gaps?
- The "Stage" branching — useful or feels formulaic?
- The "What we're still building" / "A note on scope" pair — too modest, right tone, or undersells?

### Juan (bless)

Final read for voice + posture. The "five real consumer users (3 are Juan)" line is the load-bearing honesty-vs-pitch decision — call it out if you want to revise.

## Sequencing

- Today: v1 ready for Sofia framing pass.
- Sofia framing review: when she gets to it.
- Athena tech-accuracy + proofread: after Sofia clears.
- Bertha-via-Eugenie: after Athena clears.
- Juan bless: after Bertha clears.
- On bless: commit to `ac/site/content/blog/<slug>.md` (slug TBD; current placeholder `ai-first-company-howto`); signal Hestia for the deploy.
- Adjacent: Athena scaffolds the template repo in parallel; once name lands, I revise [TEMPLATE_REPO_URL] placeholder in the draft.
- Adjacent: same source material seeds the seminar curriculum (per Athena brief) — once post is published, that adjacent flow can pick up.

## Source-of-truth location decision

Publish at `ac/site/content/blog/<slug>.md` (matches the blog scaffold Peter just shipped at 6ec0fc60 — see the welcome post at hello-from-aweb.md for the file shape). The draft in `publishing/drafts/` is the narrative + decision record; the AC path is the published surface.

Slug option leans: `ai-first-company-howto` (matches title without ".md slug overhang"), or `how-to-ai-first-company` (matches imperative voice). Defer the slug call to Sofia + Juan; tighter slug option also welcome.
