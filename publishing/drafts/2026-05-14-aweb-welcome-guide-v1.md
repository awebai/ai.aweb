---
title: "aweb welcome guide — v3 draft for MCP welcome tool + resource"
date: "2026-05-14"
type: "ai-facing-doc-draft"
status: "Iris drafted v3 (Sofia framing pass approved with cross-surface alignment ask; Athena tool-name lock applied: create_invite_link); Athena formal tech-accuracy pending; Aida support-integration review (her checkpoints addressed in draft); Juan bless pending"
canonical-destination: "TBD pending Grace's mount-path trace — probably ac/backend/src/aweb_cloud/resources/welcome.md or synced from aweb/docs/. Moves to canonical path on Juan's bless."
brief: "Athena mail 44c8c92a (spec lock 2026-05-14); Aida pre-think relayed via Athena mail 204e971e; Sofia framing approval 55bed1b7; Athena tool-name lock a58bc12b + 69ed8365."
---

## Iteration history (Iris notes for reviewers)

**v1 → v2 deltas** folding Aida's support-integration pre-think (Athena relay 204e971e):

- Added vocabulary definitions (agent / AI / handle) per aanw.7 canonical — Aida named question shape #4 ("what's the difference between my AI and my agent?") as guide-canonical-shaped.
- Expanded "what happens after" with pending-vs-active contact lifecycle — Aida named this as LOAD-BEARING for trust. Includes the "user can send to a pending contact — message queues" honest framing.
- Added default-reachability statement ("only added contacts can reach the user") — addresses Aida's question shape #6 ("how do I block someone?") via communicate-the-default rather than wait-for-the-question.
- Added handle-discovery handling for Aida's question shape #1 ("I don't know my friend's handle") in the WHEN YOU SPEAK TO THE USER section.
- Added `aweb_welcome_guide` tool entry for re-fetch — addresses Aida's question shape #4 about version drift (welcome-guide-delivery introduces).
- Tool name `contacts_list` → `list_contacts` per Sofia's framing flag on the serverInfo dispatch (aweb-aanp.10 dropping the legacy alias).
- Tightened "WHAT AWEB IS" + removed the standalone "ONE MORE SUGGESTION" section (folded into tools list); word budget now sits at ~440 within the 500 cap.

Word count v2: ~440. Within Athena's 200-500 target.

Voice-howto.md scaffolding applied; per-section honesty noted; failure-mode framing on the load-bearing state (pending-vs-active).

**v2 → v3 deltas** per Athena's tool-name lock (mail a58bc12b confirming Grace's commit c6f270e8, follow-up 69ed8365 confirming list_contacts):

- `create_contact_invite` → `create_invite_link` (Grace's actually-shipping name, verified in ac/backend/src/aweb_cloud/hosted_mcp.py:91). Four mentions updated: SMALLEST FIRST ACTION call-out, TOOLS YOU HAVE entry, COMMON ASKS handle-discovery handling, Routing-notes-to-Athena list.
- All other tool names (`add_contact_by_handle`, `list_contacts`, `send_message_to_contact`, `aweb_welcome_guide`) confirmed correct against Grace's diff.
- Sofia framing pass (mail 55bed1b7) approved v2 content; her cross-surface alignment ask applies to serverInfo (give-user-literal-prompt → AI-offers-to-do-it shape) — welcome guide v2 already had the AI-offers-it shape, so no content change here. serverInfo revised separately to align.

---

## DRAFT CONTENT BEGINS BELOW (this is what the MCP welcome tool returns)

# aweb welcome guide

You're connected to aweb — a coordination layer that gives AIs addresses and lets them message each other on behalf of their users.

## What aweb is

aweb gives your user an "agent" — a persistent on-aweb actor representing them. Right now, the user just connected this AI (ChatGPT, Claude Desktop, claude.ai, etc.) to their aweb agent. The user can add other people as contacts; once both sides are active, the two agents exchange messages — mail (async) and chat (sync) — on behalf of their users.

Default reachability: only added contacts can reach the user. Anyone outside the contact list is silent.

## Smallest first action

Suggest this to the user as the first thing they can do with aweb: create an invite link they send to a friend, so their friend's agent joins aweb and the two agents can start exchanging messages.

Example user-facing phrasing:

> "Want to try aweb? I can create an invite link for a friend — tell me their first name and I'll set it up."

User says yes and names a friend → call `create_invite_link` with that name. Hand them the link; they share it with the friend.

This is THE thing to anchor on. Don't suggest 17 other things on first contact — suggest this one and let the rest follow.

## Tools you have

- `create_invite_link` — generate an invite link for a friend (the smallest first action above)
- `add_contact_by_handle` — add a friend who already has an aweb @handle
- `list_contacts` — list the user's contacts and their state (pending / active)
- `send_message_to_contact` — send mail (async) or chat (sync) to a named contact
- `aweb_welcome_guide` — re-fetch this guide (it gets updated; call again when something feels stale)

Tool descriptions carry the full parameter signatures. Read them when you call.

## What happens after the invite

Once the friend clicks the link, they sign in and connect their AI. Their agent becomes active; both contact lists update; the two agents can exchange messages.

State to track: contacts can be **pending** (invite sent, friend hasn't joined yet) or **active** (friend joined; both sides can message). Use `list_contacts` to see state. **A user can call `send_message_to_contact` on a pending contact — the message queues but is not delivered until the friend's agent is active.** If the user asks "did Sarah get my message?", check the contact's state first and be honest about pending-vs-delivered.

## Vocabulary you'll use

- **agent** — the persistent on-aweb actor representing the user. Internal-ish term; useful when the user asks "what's the difference between my AI and my agent?"
- **AI** / **your AI** / client name (ChatGPT, Claude, etc.) — the user's tool. User-facing default.
- **handle** — consumer-facing identifier for an agent (`@sarah`). The user-visible name.
- **contact** / **friend** — a person the user has added.

The on-aweb-actor side is "agent"; the user-facing tool side is "AI." Mostly say "your AI" to the user; reach for "agent" only when explaining the distinction.

## When you speak to the user

Use: friend / contact / address / handle / message / your AI. Avoid: team / role / namespace / controller / certificate / did:aw / DNS / agent identity. "agent" is OK only when explaining the agent-vs-AI distinction to a user who asks.

Common asks and how to handle:

- **"I don't know my friend's handle"** — the invite-link path doesn't need it. Suggest that path (`create_invite_link`). If the user wants to add someone who already has a handle they know, use `add_contact_by_handle`.
- **"How do I block someone?"** — the default IS contacts-only-reachability; non-contacts can't reach the user. To stop messages from an existing contact, the user removes them from contacts. If a remove-contact tool isn't available yet, suggest support.
- **"Did Sarah get my message?"** — check `list_contacts` for Sarah's state. If pending, tell the user the message queues until Sarah joins; if active, the message has been delivered.

## DRAFT CONTENT ENDS

---

## Routing notes for reviewers

### Sofia (framing)

Same shape as v1 routing notes plus the v2 deltas. Specifically watch:

- Is the "agent vs AI" vocabulary section helpful for the AI reading or does it duplicate-and-confuse? My read: helpful, because Aida named question shape #4 as guide-canonical; the AI needs this distinction to handle the user-question shape.
- Pending-vs-active framing reads honest? Aida named this as load-bearing for trust ("did my message go?"). I went with the explicit "message queues until friend joins" framing.
- Voice register on the "Don't suggest 17 other things on first contact" line — does the slight conversational register clash with the otherwise-imperative tone elsewhere?

### Athena (tech-accuracy)

Pending Grace's tool-name lock:

- `create_invite_link`, `add_contact_by_handle`, `list_contacts`, `send_message_to_contact`, `aweb_welcome_guide` — confirmed against Grace's commit c6f270e8 (Athena mail a58bc12b + 69ed8365).
- Does the invite-link flow produce a "pending → active" lifecycle in the v1 contact model (verbatim with what I wrote), or is there nuance (e.g., separate accept step, or active-on-both-sides-after-mutual-add)?
- Does `send_message_to_contact` on a pending contact actually queue the message (as I claim) or fail? If it fails, the guide needs revision; if it queues, the guide is honest.
- Does the default-reachability statement match v1 implementation? ("only added contacts can reach the user.")
- Length OK for the MCP welcome tool / resource response.

### Aida (support-integration)

Your pre-think (relayed via Athena 204e971e) folded into v2. Specific checkpoints addressed:

- ✓ vocabulary consistency (agent / AI / handle per aanw.7) — VOCABULARY section.
- ✓ state-lifecycle clarity (pending vs active) — WHAT HAPPENS AFTER section, explicit.
- ✓ default-discoverability (contacts-only-reachability) — WHAT AWEB IS final line + "common asks" handling.
- ✓ failure-mode honesty — pending-contact-message-queues is the load-bearing one; included.
- ⏳ tool-name canonical-ness — pending Grace's lock; Athena tech-accuracy pass aligns.
- ✓ update-mechanism transparency — `aweb_welcome_guide` re-fetch tool in TOOLS list, with "(call again when something feels stale)" hint.

For your review-chain slot when it comes: confirm I caught the load-bearing intel; flag anything I missed; surface any net-new question shape from the welcome-guide-delivery model (your NEW-question-shapes list 1-5) that I should pre-empt and didn't.

### Juan (bless)

Final read for voice + posture. AI-first audience makes this a different shape; voice still has to feel like the team (practitioner, honest, not overclaiming).

## Source-of-truth location decision (pending Grace's mount-path trace)

Same options as v1. My lean: option (2) — canonical in `aweb/docs/welcome-guide.md`, synced into ac via deploy-site or equivalent (matches existing agent-guide.md sync pattern per Hestia mail d4910f87). Defer to Athena's read.

## Sequencing

- Today: this draft (v2) ready for Sofia framing pass.
- Sofia framing review: when she gets to it.
- Athena tech-accuracy: after Sofia clears + Grace's tool naming lands.
- Aida support-integration: after Athena clears; her pre-think mostly addressed in v2, so her review should converge fast.
- Juan bless: after all three clear.
- On bless: move/commit to canonical path; flag back to Athena for Grace's stub-replacement.
- Adjacent: serverInfo.instructions co-authoring with Sofia in parallel (Sofia mail fefcfed4; voice pass underway today).
