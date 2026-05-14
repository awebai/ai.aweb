---
title: "aweb welcome guide — v5 draft for MCP welcome tool + resource"
date: "2026-05-14"
type: "ai-facing-doc-draft"
status: "Iris drafted v5 (Athena v4 cleared 6b88d7bb with contacts_remove nit folded); routing to Aida for support-integration; Juan bless after"
canonical-destination: "ac/backend/src/aweb_cloud/resources/welcome.md (AC-canonical per Athena tech-accuracy read; Grace's load_welcome_guide() reads from that path via importlib.resources). Moves on Juan's bless."
brief: "Athena spec lock 44c8c92a; Aida pre-think 204e971e; Sofia framing approval 55bed1b7; Athena tool-name lock a58bc12b + 69ed8365; Athena tech-accuracy revisions dfeb103a; Athena v4 clear + contacts_remove nit 6b88d7bb."
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

**v3 → v4 deltas** per Athena's tech-accuracy revisions (mail dfeb103a):

- **Lifecycle two-paths corrected**: invite-link creates contacts ACTIVE on both sides simultaneously (no pending state on this path); pending state only exists for the handle-add path when the friend isn't on aweb yet. WHAT HAPPENS AFTER THE INVITE section restructured to make the two-paths distinction explicit.
- **send_message_to_contact on pending errors, doesn't queue**: previous v2/v3 claim of "message queues until friend joins" was wrong (verified against aweb/server/src/aweb/mcp/tools/contacts.py:101+ — returns ValidationError "No active agent found for handle contact"). Revised WHAT HAPPENS AFTER paragraph + "Did Sarah get my message?" common-ask handler to be honest about the error + what to suggest (create_invite_link or wait for friend to accept).
- **Added read_messages_from_contact** to TOOLS YOU HAVE list — registered MCP tool (verified in aweb/server/src/aweb/mcp/server.py); Sofia's question landed; needed because the welcome guide covers post-first-turn flow and the AI will need to read replies once the friend joins.
- **Source-of-truth location locked**: ac/backend/src/aweb_cloud/resources/welcome.md (AC-canonical per Athena's read — consumer-cloud-product content lives in cloud-product code; the aweb/docs/welcome-guide.md option lean was wrong). Grace's load_welcome_guide() in hosted_mcp.py reads from that path via importlib.resources.
- **Default-reachability claim verified correct** by Athena's pass — no change.

**v4 → v5 deltas** per Athena's v4 clear + small nit (mail 6b88d7bb):

- v4 cleared on all three substantive items (lifecycle two-paths; send-on-pending errors-not-queues; read_messages_from_contact addition); default-reachability retained.
- Folded `contacts_remove` (registered MCP tool per server.py) into:
  - TOOLS YOU HAVE list (between `add_contact_by_handle` and `list_contacts`).
  - "How do I block someone?" common-ask handler — revised to call `contacts_remove` directly; dropped the "if a remove-contact tool isn't available yet, suggest support" stale fallback.

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
- `contacts_remove` — remove a contact (closes the messaging channel since reachability defaults to contacts-only)
- `list_contacts` — list the user's contacts and their state (active / pending)
- `send_message_to_contact` — send mail (async) or chat (sync) to a named contact
- `read_messages_from_contact` — read incoming mail or chat from a saved contact
- `aweb_welcome_guide` — re-fetch this guide (it gets updated; call again when something feels stale)

Tool descriptions carry the full parameter signatures. Read them when you call.

## What happens after the invite

Once the friend clicks the link, they sign in and connect their AI. The two agents become active contacts on both sides simultaneously, and the agents can exchange messages immediately.

How contacts get created (two paths):

- **Invite-link** (`create_invite_link`) — creates the contact bilaterally and active once the friend signs up. No pending state on this path.
- **Handle-add** (`add_contact_by_handle`) — creates a **pending** contact if the friend isn't on aweb yet; the contact flips to active once their agent is active.

Use `list_contacts` to see state. Pending contacts on the handle-add path do not yet have a deliverable target — sending a message to a pending contact errors with "No active agent found for handle contact" (the friend isn't on aweb). The friend has to join aweb first.

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
- **"How do I block someone?"** — the default IS contacts-only-reachability; non-contacts can't reach the user. To stop messages from an existing contact, call `contacts_remove`. Reachability is contacts-only by default, so removing them closes the channel.
- **"Did Sarah get my message?"** — check `list_contacts` for Sarah's state. If active, the message has been delivered (and the user can call `read_messages_from_contact` to see any reply). If pending, sending fails — Sarah isn't on aweb yet. Tell the user honestly: the friend needs to join aweb before messages can reach them. If the user hasn't already invited Sarah, suggest `create_invite_link`; otherwise wait for her to accept the existing invite.

## DRAFT CONTENT ENDS

---

## Routing notes for reviewers

### Sofia (framing)

Sofia v2 framing pass approved (mail 55bed1b7). All three watch-items resolved:

- ✓ Agent-vs-AI vocabulary section: keep (canonical-shaped per Aida #4).
- ✓ Pending-vs-active framing: honest pending Athena verification — Athena's v3 tech-accuracy revealed v2 was WRONG on this; rewritten in v4 (invite-link is bilateral-active immediately; pending state only on handle-add path; send-on-pending errors).
- ✓ Voice register on "17 other things": keep (concept landing > tonal uniformity).

Sofia's cross-surface alignment ask (give-user-literal-prompt → AI-offers-it shape) applied to serverInfo separately; welcome guide already had the right shape.

### Athena (tech-accuracy) — v3 pass dfeb103a; v4 re-read pending

Five claim-verifications:

- ✓ Tool names — `create_invite_link`, `add_contact_by_handle`, `contacts_remove`, `list_contacts`, `send_message_to_contact`, `read_messages_from_contact`, `aweb_welcome_guide` — confirmed against Grace's commit c6f270e8 + server.py registration (contacts_remove added v5 per Athena's nit 6b88d7bb).
- ✓ Default-reachability ("only added contacts can reach the user") — verified accurate (mechanism is address_reachability="nobody" + bilateral contact routing, but user-facing framing is right).
- ✗ → fixed in v4: invite-link "pending → active" lifecycle claim was wrong — invite-link is bilateral-active immediately; pending state only exists on the handle-add path.
- ✗ → fixed in v4: send_message_to_contact on pending "queues" claim was wrong — it errors with "No active agent found for handle contact" (verified at aweb/server/src/aweb/mcp/tools/contacts.py:101+). LOAD-BEARING for trust per Aida — revised to honest "sending fails; suggest invite link or wait for accept" handling.
- ✗ → fixed in v4: `read_messages_from_contact` was missing from tools list (registered tool in aweb/server/src/aweb/mcp/server.py); Sofia raised the omission and Athena confirmed registration; added.

Athena v4 re-read should converge in 5-10 min per her sequencing.

### Aida (support-integration)

Your pre-think (relayed via Athena 204e971e) folded into v2 then sharpened in v4 after Athena's tech-accuracy pass:

- ✓ vocabulary consistency (agent / AI / handle per aanw.7) — VOCABULARY section.
- ✓ state-lifecycle clarity (active default for invite-link; pending only for handle-add) — WHAT HAPPENS AFTER section, restructured v4 with two-paths distinction.
- ✓ default-discoverability (contacts-only-reachability) — WHAT AWEB IS final line + "common asks" handling.
- ✓ failure-mode honesty — v4 fixes load-bearing trust claim: send_message_to_contact on pending ERRORS (doesn't queue); revised "did Sarah get my message?" handler is honest about failure + suggests the right next action (`create_invite_link` or wait for accept).
- ✓ tool-name canonical-ness — Athena tool-name lock applied; `create_invite_link` is shipping name.
- ✓ update-mechanism transparency — `aweb_welcome_guide` re-fetch tool in TOOLS list, with "(call again when something feels stale)" hint.

For your review-chain slot: confirm I caught the load-bearing intel after the v4 corrections; flag anything I missed; surface any net-new question shape from the welcome-guide-delivery model (your NEW-question-shapes list 1-5) that I should pre-empt and didn't.

### Juan (bless)

Final read for voice + posture. AI-first audience makes this a different shape; voice still has to feel like the team (practitioner, honest, not overclaiming).

## Source-of-truth location decision (locked v4)

`ac/backend/src/aweb_cloud/resources/welcome.md` per Athena's tech-accuracy read (mail dfeb103a). Consumer-cloud-product content lives in cloud-product code; the agent-guide.md sync pattern is for aweb-protocol surface (different audience and authorship). Grace's `load_welcome_guide()` in hosted_mcp.py reads from that path via importlib.resources. Mirror to docs site is a downstream sync if wanted.

## Sequencing

- ✓ v2 draft → Sofia framing review (approved 55bed1b7 with cross-surface alignment ask).
- ✓ v3 → Athena tool-name lock (a58bc12b + 69ed8365): create_invite_link.
- ✓ v4 → Athena tech-accuracy revisions applied (dfeb103a): lifecycle two-paths, send-on-pending errors, read_messages_from_contact added, source-of-truth locked AC-canonical.
- ✓ Athena v4 re-read clear (mail 6b88d7bb) + folded the contacts_remove nit → v5.
- → Aida support-integration pass (her pre-think folded; should converge fast after the v4/v5 trust-line + tool-completeness fixes).
- → Juan bless.
- → On bless: commit to ac/backend/src/aweb_cloud/resources/welcome.md; flag back to Athena for Grace's stub-replacement.
- Adjacent: serverInfo.instructions v4 bundled with welcome-guide v4 to Athena.
