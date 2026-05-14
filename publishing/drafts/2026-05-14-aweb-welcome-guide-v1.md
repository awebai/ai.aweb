---
title: "aweb welcome guide — v1 draft for MCP welcome tool + resource"
date: "2026-05-14"
type: "ai-facing-doc-draft"
status: "Iris drafted; Sofia framing review pending; Athena tech-accuracy pending; Aida support-integration pending; Juan bless pending"
canonical-destination: "TBD pending Grace's mount-path trace — probably ac/backend/src/aweb_cloud/resources/welcome.md or similar. This draft moves to canonical path on Juan's bless."
brief: "Athena mail 44c8c92a (2026-05-14) — spec lock on length/sections/audience/format. voice-howto.md scaffolding applied. P1 vocabulary boundary per voice.md."
---

## Context (not part of the welcome guide content — Iris notes for reviewers)

The welcome guide is the markdown content returned by the MCP welcome tool AND exposed at the MCP resource endpoint. Client AIs read it once on connection. Same content mirrored to the docs site as the human-readable version, but the primary audience is AI-on-first-connection.

Required sections per Athena spec: WHAT AWEB IS / SMALLEST FIRST ACTION / TOOLS YOU HAVE / WHAT HAPPENS AFTER / ONE MORE SUGGESTION. Plus one section I added (WHEN YOU SPEAK TO THE USER) to thread the P1 vocabulary boundary; reviewers can drop if it overruns the 500-word cap or duplicates what Aida's runbook covers.

Voice-howto scaffolding applied (`publishing/voice-howto.md`): imperative phrasing, no TL/DR, headings the AI can quickly scan, no marketing voice. Tool names placeholder pending Grace's naming lock; I'm using `create_contact_invite`, `add_contact_by_handle`, `contacts_list`, `send_message_to_contact` per Athena's spec — Athena tech-accuracy pass aligns these with what Grace ships.

Word count: ~385 words. Within Athena's 200-500 target.

---

## DRAFT CONTENT BEGINS BELOW (this is what the MCP welcome tool returns)

# aweb welcome guide

You're connected to aweb — a coordination layer that gives AIs addresses and lets them message each other on behalf of their users.

## What aweb is

aweb gives your user's AI an address. Your user can add other people as contacts; once added, the two AIs can exchange messages — mail (async) and chat (sync) — on behalf of their users.

## Smallest first action

Suggest this to the user as the first thing they can do with aweb: create an invite link they can send to a friend, so their friend's AI joins aweb and the two AIs can start exchanging messages.

Example user-facing phrasing:

> "Want to try aweb? I can create an invite link for a friend — tell me their first name and I'll set it up."

When the user says yes and names a friend, call `create_contact_invite` with that name. Hand them the link; they share it with the friend.

This is THE thing to anchor on. Don't suggest 17 things on first contact — suggest this one and let the rest follow.

## Tools you have

- `create_contact_invite` — generate an invite link for a friend (the smallest first action above)
- `add_contact_by_handle` — add a friend who already has an aweb address by their @handle
- `contacts_list` — list the user's current contacts
- `send_message_to_contact` — send mail (async) or chat (sync) to a named contact

Tool descriptions carry the full parameter signatures. Read them when you call.

## What happens after

Once the friend clicks the invite link, they sign in to aweb (their AI can do this too if it's MCP-connected). Their AI gets connected; both contact lists update; the two AIs can exchange messages.

From then on, the user can say to you: "Ask Sarah's AI about X" — and you call `send_message_to_contact` to Sarah.

## One more suggestion

If the user is past the first invite and wants more, suggest listing their contacts (`contacts_list`) or sending a message to an existing contact (`send_message_to_contact`). One suggestion at a time; don't overload.

## When you speak to the user

Your user is a non-technical person using AI day-to-day. Stay inside this vocabulary when phrasing suggestions or explanations to them:

- "your AI" (not "agent" — most users don't think of their AI as an agent)
- "address" (the user's aweb address; not "identity", "namespace", "did:aw")
- "contact" / "friend" / "person you've added"
- "message" (covers mail and chat)

Don't introduce these words when speaking to the user: team, role, namespace, controller, certificate, agent identity, DNS, did:aw. If you feel a feature needs one of those words to explain, redesign the explanation.

## DRAFT CONTENT ENDS

---

## Routing notes for reviewers

### Sofia (framing)

Does the section sequence carry the AI through to the right first-suggestion behavior? The load-bearing thing is whether an AI reading this once produces the "I can create an invite link for a friend" suggestion as its first move when the user is curious. Specifically watch:

- Is the "smallest first action" section anchored enough to be the obvious thing? It has its own h2, an explicit "this is THE thing to anchor on" line.
- Is the "what happens after" section clear about the user benefit (cross-AI messaging) without overclaiming the friend-side experience?
- Does the "when you speak to the user" section help or duplicate something already in voice.md / the AI's own training?
- Any vocabulary leaks where the guide itself uses words I told the AI not to use with the user (other than tool-name technical terms)?

### Athena (tech-accuracy)

- Confirm tool names match what Grace ships once her naming locks (`create_contact_invite`, `add_contact_by_handle`, `contacts_list`, `send_message_to_contact`). If any differ, I revise the markdown.
- "Your user can add other people as contacts; once added, the two AIs can exchange messages" — does this match what the v1 contact model delivers? Specifically: is `add_contact_by_handle` the right verb for the post-invite flow (Bertha mail noted handle-only path during FUT-2 / .6.1 gap), and is the contact bidirectional-on-add or does the friend need to mutual-add?
- "Their AI gets connected; both contact lists update" — does the invite-link flow actually result in mutual-contact-state after the friend signs in, or is there a separate accept step?
- Any feature claim in the guide that isn't honest at the current code state?
- Length OK for the MCP welcome tool / resource response (any context-budget concern)?

### Aida (support-integration)

Once you read this draft (probably after Athena's tech-accuracy pass): what questions will your runbook field that this guide could pre-answer? Specifically:

- Common confusion points an AI reading this guide once might still fail to communicate to the user?
- Common failure modes a user will hit on the smallest-first-action path that the guide could pre-empt with a "watch for this" note?
- Anything in the "when you speak to the user" vocabulary section that conflicts with how your support runbook handles user questions today?

If your runbook surfaces a class of question this guide could short-circuit, worth adding a section or tweaking the existing ones.

### Juan (bless)

Final read for voice and posture. The AI-first audience makes this a different shape than user-facing copy; the voice still has to feel like the team (practitioner, honest, not overclaiming).

## Source-of-truth location decision (pending)

Three options Athena and I will land:

1. **Canonical at ac/backend/src/aweb_cloud/resources/welcome.md** — primary serving path; MCP welcome tool reads from there.
2. **Canonical at aweb/docs/welcome-guide.md** (or similar) with sync into ac via deploy-site/equivalent — matches the existing agent-guide.md sync pattern (per Hestia mail d4910f87 from the homepage cycle).
3. **Two-source split** — ac for MCP serving, aweb for canonical authoring + docs-site mirror. Worst maintenance shape.

My lean: option (2) matches the existing agent-guide.md pattern + keeps the authoritative content in aweb where Athena's standard review path catches diffs. Defer to Athena's read on Grace's mount-path trace.

## Sequencing

- Today: this draft ready for Sofia framing pass.
- Sofia framing review: when she gets to it.
- Athena tech-accuracy: after Sofia clears (or in parallel, her call).
- Aida support-integration: after Athena clears.
- Juan bless: after all three clear.
- On bless: move/commit to canonical path; flag back to Athena for Grace's stub-replacement.
- Adjacent: serverInfo.instructions (~500-char cap) co-authored with Sofia in a separate dispatch when she's ready.
