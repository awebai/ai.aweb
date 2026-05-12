---
title: "Show HN — pinned author comment v3"
date: "2026-05-07"
type: "comment"
draft: true
audience: "HN, Show HN thread, posted within ~2 minutes of submission"
voice: "Juan-as-OP (founder voice, first-person; pending authorship confirm)"
---

## Context

This is the load-bearing artifact for the Show HN. Submission URL is
`aweb.ai`. The reader sees the title, opens the landing site, then
comes back to read this comment. The comment ties the package
together and signposts depth.

Sofia and Bertha converged on the simpler template after the AHK
guest-comment cycle (see `voice-howto-comments.md` for the banked
shape). v3 below is drafted to that template; v1 and v2 are kept
as longer alternatives in case the framing pass wants them.

Honesty constraints applied (from voice.md, the value-prop honesty
pass, and the cycle-log overclaim concern):

- Practitioner voice; lead with experience, not product
- "I built aweb" not "our product / platform"
- No marketing words ("revolutionary," "game-changing")
- No attacks on competing tools
- Honest about evidence: "we used aweb itself to ship the latest
  cycle" (true and verifiable from the cycle log), not "entirely
  on AI agents," not "2x+ with far fewer disasters"
- Open-source first, hosted second
- Invitation, not pitch

## Parallel-draft surface

Athena drafted a Show HN first-comment with Juan directly (~3
iterations, Juan-voice already partially landed) about an hour
before I started drafting. We were drafting in parallel without
knowing. Both drafts now go to Sofia side-by-side; Sofia frames
and picks or merges. Athena's draft has a real head start in
voice match because Juan was hands-on; my draft is offered as
alternative input.

## Current state — v4 (alternative; Juan's own draft is the leading candidate)

v4 below integrates: Sofia's framing pass (drop anecdote, drop
MCP/A2A pre-emption, drop DNS-protocol detail; trust the reader,
let depth-links carry depth) + Athena's tech-accuracy (the install
command produces ONE agent, not two; second agent comes from second
init or invite) + Juan's direction to Athena ("don't reference the
cycle-log post since it doesn't exist publicly yet").

Juan is iterating his own pinned-comment text directly (architectural
para retained, dogfood hook via team-of-agents framing + git log +
public dashboard). My critical notes on his text are in the user
thread, not in this file: the "team is itself a team of agents"
overclaim Sofia named, and the dashboard link privacy review.

If Juan's text becomes the canonical, v4 archives. If Sofia merges
between Juan's text + Athena's parallel draft, v4 is alternative
input.

## Athena's converged-with-Juan draft (the leading candidate)

Athena converged with Juan on the following text after four
iterations in user-conversation. Same text Juan shared with Iris
in user thread.

> aweb came out of running multiple AI coding agents and having
> to copy-paste between them. The OSS — chat, mail and tasks
> for multi-agent, multi-human teams (provider-agnostic) — is
> at https://github.com/awebai/aweb (MIT).
>
> Every agent gets a cryptographic identity (Ed25519, did:aw),
> teams are cert-scoped namespaces, and routing/auth is signed
> all the way down. Trust is rooted at the DNS level: if you
> control a domain name, you can have agents with addresses
> like acme.com/agent_name
>
> We use it ourselves. The team shipping aweb is itself a team
> of agents (direction, engineering, operations, support,
> outreach, analytics) coordinating through aweb. Commits land
> daily and the dogfooding is visible in the git log if you
> want to see it, as well as the public dashboard at
> https://app.aweb.ai/juan/aweb/chat
>
> Happy to take questions on the protocol, the dogfooding
> model, or the rough edges.

Open issues on this draft (Iris notes for Sofia/Juan):

1. **"is itself a team of agents" overclaim.** Sofia's previously
   flagged framing concern. The HN thread will press on it. Suggest:
   "The team shipping aweb pairs me on direction and code review with
   agents in six roles ..." — keeps dogfood punch, stays honest.
2. **Dashboard link needs incognito browser test before submit.**
   Athena curl'd it (HTTP 200, SPA shell, title "aweb."). That tells
   us the URL responds, not what an unauthenticated visitor actually
   sees. If login wall: link backfires. If public team chat: strong.
3. **Athena pushback: rough-edges paragraph.** Juan dropped it; Athena
   argues HN engineers look for honest-frictions sections as
   trust signal. Athena's text:
   > Rough edges: onboarding is still sharp (we shipped 1.20.6
   > today fixing several issues a customer demo surfaced); the
   > cloud control plane at app.aweb.ai is private/proprietary
   > while the core protocol is MIT; there's no GUI — aw is a CLI.
   Iris lean: include a tightened version. Sofia's framing pass
   weighs.
4. **Title check.** Athena's title formulation skips "aweb."
   Suggest: "Show HN: aweb – Chat, mail and tasks for multi-agent
   teams (OSS, provider-agnostic)." Convention puts the name first;
   omitting it costs searchability for "aweb" specifically.
5. **No install command in the post body.** If aweb.ai surfaces
   `npm install -g @awebai/aw && aw init` prominently in the Stage
   1 path, no fix needed. If aweb.ai leads with marketing instead,
   audience-1 reader is one extra click from the entry path.

## Athena's fresh-container pre-flight — RESULT (2026-05-07)

**FAIL** on the "twice in two terminals" line. At 1.20.6 a second
`aw init --hosted --persistent --username <same>` rejects with
"username 'foo' is not available (taken)." The flow we'd been
writing was empirically false.

Measured times (single-agent path):
- npm install -g @awebai/aw: 2s
- aw init (hosted, persistent): 2s
- Total to first persistent agent: ~about a minute including
  network round-trips against production hosted signup.

So "5 minutes" was conservative even for the first-agent path; "1
minute" is more honest. The "second agent" path is `aw workspace
add-worktree` — not tested in this pre-flight, but Athena's
engineering judgment is it's the right path. Worth a separate
5-min verification before submit.

Banked discipline (Iris): every claim in HN-bound text gets a
fresh-container pre-flight before submit. No exceptions. Three of
us (Iris v4, Sofia tightening, Iris first-comment v1) all wrote
"twice in two terminals" without checking. Pre-flight was the
gate that caught it. The cost of pre-flight (≤45 min, one
container) is far below the cost of a wrong claim landing on the
top of HN.

## First-comment recommendation (post-pre-flight)

Companion to Juan's submission body. Body does substance
(description, architecture, dogfood, close); first comment does
the practical bits that didn't fit (try-it command + honest
frictions).

> Two things that didn't fit in the post:
>
> **Try-it:** `npm install -g @awebai/aw && aw init` gets you a
> persistent agent on the hosted free tier in about a minute. To
> add a second agent in a sibling directory, run `aw workspace
> add-worktree`.
>
> **Rough edges:** onboarding still has sharp corners — we
> shipped 1.20.6 today fixing several issues a customer demo
> surfaced; the cloud control plane at app.aweb.ai is private/
> proprietary while the core protocol is MIT; there is no GUI —
> `aw` is CLI-only.

If cycle log goes public before submit, optional fourth bullet:

> **If you want depth:** commit-level walkthrough of one ship
> cycle — [cycle-log link]. We used aweb to ship aweb; the
> receipts are linked.

If `aw workspace add-worktree` pre-flight fails too, drop to
single-agent claim:

> **Try-it:** `npm install -g @awebai/aw && aw init` gets you
> started on the hosted free tier in about a minute.

## Sofia's framing-pass decisions (2026-05-07 c563a77d)

- **Cycle-log link timing: option 3 with 3-day cap.** Hold Show HN
  submit until cycle log is public; if not public by 2026-05-10,
  drop just the cycle-log line and submit anyway. Strongest receipt
  is worth 2-3 days. Don't let it become an indefinite hold.
- **Routing my v4 vs. Athena's draft:** deferred until both are
  in hand. Substance decides.
- **v4 cosmetic note:** "Thanks for taking a look" is pre-emptive
  (the reader has just clicked through, has not yet taken a look).
  HN convention is more direct: "Hi HN — I built X because..." or
  just "I built X because...". Folded into v4 below.

## Draft v4 (recommended)

> Thanks for taking a look. I built aweb because I was running
> multiple AI coding agents on the same codebase and watching
> them collide — duplicate implementations, silent overwrites,
> conflicts at merge time. Open source, MIT.
>
> `npm install -g @awebai/aw && aw init` (twice, in two
> terminals) gets two agents talking on the hosted free tier in
> about 5 minutes.
>
> Two longer reads if you want depth:
>
> - Why coordination is the bottleneck for multi-agent dev:
>   [essay link]
> - One ship cycle in commit-level detail (we used aweb to ship
>   aweb): [cycle-log link — INCLUDE ONLY IF POST IS PUBLIC BY
>   SUBMIT]
>
> Source: [github.com/awebai/aweb](https://github.com/awebai/aweb).
> Hosted at [aweb.ai](https://aweb.ai). Happy to answer questions.

If the cycle-log link can ship: 4 short paragraphs, ~110 words.
Practitioner opening + accurate try-it + depth-links + close.

If the cycle-log post isn't public by submit, the second
depth-link drops and the comment is ~95 words with just the
essay depth-link.

The "(twice, in two terminals)" parenthetical addresses Athena's
tech-accuracy flag without losing the "two agents talking"
punchline. Cleaner alternative if Sofia prefers her original
phrasing without the parenthetical: "`npm install -g @awebai/aw
&& aw init` gets you on the hosted free tier in about 5 minutes;
from there you can spawn another agent or invite a teammate."
(Athena's recommended substitution.)

## Draft v3 (recommended) — matches the AHK-style template, with Athena's tech-accuracy tightenings

Tightenings folded:
- Claim 1: "two agents in 5 minutes" was technically wrong — a
  single `aw init` produces ONE agent. Replaced with Athena's
  verified phrasing that a second agent comes from a second
  init or an invite.
- Cycle-log depth-link removed: Juan's direction to Athena was
  "don't reference the cycle-log post since it doesn't exist
  publicly yet." Same constraint applies here.
- Dogfood hook ("we used aweb itself to ship the latest cycle")
  removed for the same reason — the receipt isn't public yet.
  Save the hook for when the cycle log is public.

> Thanks for taking a look. I built aweb because I kept watching
> multiple AI coding agents on the same codebase collide —
> duplicate implementations, silent overwrites, conflicts that
> pass tests in isolation but fail at merge. With aweb each agent
> gets a cryptographic identity, claims tasks so others don't
> duplicate, and can chat or mail peers; `npm install -g @awebai/aw
> && aw init` gets you on the hosted free tier in about 5 minutes
> (from there you can spawn another agent or invite a teammate).
> Source: [github.com/awebai/aweb](https://github.com/awebai/aweb).
> Happy to answer questions.

Three sentences, ~80 words. Matches the converged template:
warm opener, honest context, install command, source, invitation.
No architecture, no leading questions, no disclosure tags, no
constructed pivots, no claim that exceeds public evidence.

## Routing

- **Sofia (framing):** does this match the converged AHK-style
  template + voice + product-fit?
- **Athena (tech-accuracy):** the three claims that need a verified
  yes (one fewer than v1, since the architecture leg is gone):
  1. `npm install -g @awebai/aw && aw init` produces two seeable
     agents in ~5 minutes on a fresh machine. (Same as Sofia's
     fresh-container-load pre-flight ask.)
  2. "Each agent gets a cryptographic identity, claims tasks so
     others don't duplicate, and can chat or mail peers" —
     accurate at current shipped state (1.20.6 cli + v0.5.23 cloud).
  3. "We used aweb itself to ship the latest cycle" — true per
     the cycle-log receipts, but Sofia flagged the cycle log itself
     has overclaim concerns under review; the link target framing
     should match her final pass.
- **Juan (voice pass + authorship confirm):** posts as OP. v3 is
  drafted in his voice for him to land or reshape.

## Open

- **Authorship.** Sofia recommended Juan-as-OP and surfaced to him
  for confirm.
- **Depth-link URL for the cycle log.** plan.md sequencing has the
  essay on juanreyero.com; cycle log destination TBD. Real URL
  needed before submission.
- **"5 minutes" pre-flight.** Sofia asked Athena for explicit
  confirmation that the Stage 1 path was tested under fresh-
  container load before submit; if it slips, the comment text
  needs to match.
- **Essay link presence.** v3 only signposts the cycle log as
  depth (matching the simpler template). The essay (5-agents
  problem narrative) is now NOT linked in the pinned comment — it
  reaches the audience either via aweb.ai having a link to it, or
  as separate distribution. If Sofia wants both depth-links in
  the pinned comment, that would push v3 toward v2 length.

## Draft v2 (alternative, longer) — adds positioning leg

Cuts the architecture leg from v1 but keeps two depth-links and
the MCP/A2A positioning sentence.

> I have been running multiple AI coding agents on the same codebase
> for months and watching them collide — duplicate implementations,
> silent overwrites, conflicting designs that pass tests in isolation
> but fail when merged. I built aweb to fix this. Open source, MIT.
>
> What it does: each agent gets a cryptographic identity, claims
> tasks so others don't duplicate, and chats or mails the others.
> `npm install -g @awebai/aw && aw init` gets you two agents on the
> hosted free tier in about 5 minutes.
>
> What surprised me using it on real work: agents started asking
> each other questions about interface boundaries I'd forgotten to
> specify, and worked them out on their own. No orchestration —
> just peers that can talk. That changed how I split work between
> them.
>
> Complementary to MCP (agent-to-tool) and A2A (task delegation) —
> different layer.
>
> Two longer reads if you want depth:
>
> - Why coordination is the bottleneck for multi-agent dev:
>   [link to 5-agents essay]
> - One ship cycle in commit-level detail (we used aweb to ship
>   aweb): [link to cycle log]
>
> Source: [github.com/awebai/aweb](https://github.com/awebai/aweb).
> Hosted at [aweb.ai](https://aweb.ai). Happy to answer questions.

## Draft v1 (alternative, longest) — adds architecture leg

Adds DNS-trust-root paragraph back. Likely too much per the
converged template; kept here only in case the framing pass wants
the architecture surface for the Audience-2 reader who is
landscape-shopping.

> I have been running multiple AI coding agents on the same codebase
> for months and watching them collide — duplicate implementations,
> silent overwrites, conflicting designs that pass tests in isolation
> but fail when merged. I built aweb to fix this. Open source, MIT.
>
> What it does: each agent gets a cryptographic identity, claims
> tasks so others don't duplicate, and chats or mails the others.
> `npm install -g @awebai/aw && aw init` gets you two agents on the
> hosted free tier in about 5 minutes.
>
> What surprised me using it on real work: agents started asking
> each other questions about interface boundaries I'd forgotten to
> specify, and worked them out on their own. No orchestration —
> just peers that can talk. That changed how I split work between
> them.
>
> aweb is complementary to MCP (agent-to-tool) and A2A (task
> delegation) — different layer. The identity layer underneath
> uses DNS as the trust root: a TXT record anchors a public key
> per domain, so any organization can run its own namespace
> without trusting a central registry. Self-hostable.
>
> Two longer reads if you want depth:
>
> - Why coordination is the bottleneck for multi-agent dev:
>   [link to 5-agents essay]
> - One ship cycle in commit-level detail (we used aweb to ship
>   aweb): [link to cycle log]
>
> Source: [github.com/awebai/aweb](https://github.com/awebai/aweb).
> Hosted at [aweb.ai](https://aweb.ai). Happy to answer questions.
