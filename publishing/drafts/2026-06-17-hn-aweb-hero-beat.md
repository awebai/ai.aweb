---
title: "Show HN draft — aweb hero beat (homepage you can talk to)"
date: "2026-06-17"
type: "show-hn-draft"
audience: "P3 developer team primary (HN audience that can install a CLI); P1+P2 secondary (browser-AI section on site serves them)"
status: "Iris-drafted; routing to Sofia for framing-pass; Juan submits"
channel: "hn"
slot: "Tue 2026-06-17 07:00 US Pacific (target; gated on 06-13 Hestia adversarial + capacity reads per Sofia 94e8427c + 8abded86)"
fallback: "If either Hestia gate misses 06-13, this becomes the r/ClaudeCode primary body. Same copy, different submit surface."
---

## Context for reviewers

The beat is "we shipped a homepage you can talk to." Replayability is the proof: any reader with aw installed can run the hero command and get a signed reply from pi.aweb.ai/ama in ~2 seconds. Verified end-to-end on a fresh terminal 2026-06-11 (Iris).

Claim boundaries per Sofia 311612ca:
- Demo claim is identity + address + messaging + greeter reply. NOT E2EE.
- Opt-in E2EE is a separate product capability; the kicker on aweb.ai names it but the greeter exchange does not use it.
- ClaWeb (the separate product Juan/Sam shipped 2026-06-09 under the `claweb` slug) is not in this post. Different product, different launch, different lane.
- No adoption numbers.

Voice anchors per publishing/voice.md:
- Practitioner first-person; lead with experience.
- No "our product" / "our platform" — say "aweb."
- No marketing-shape adjectives (revolutionary, game-changing, etc.).
- No em-dashes in customer-facing copy (banked 50eeca6).
- Engagement rules: one comment per thread, don't argue if negative, no "RT for more."

Pre-submit checklist (Sofia 94e8427c + 8abded86 union of conditions):
- (a) Drafts + attempts-row-writing wiring + submitter availability ready: pending
- (b) ama adversarial smoke pass: Hestia gate, due 06-13
- (c) Burst capacity read (50 concurrent send-and-waits, graceful failure mode): Hestia gate, due 06-13

If (b) or (c) fails: degrade to r/ClaudeCode-primary (same body, different surface), HN follow-up only if r/ClaudeCode signal warrants.

---

## Title

```
Show HN: A homepage you can talk to (aweb, MIT, CLI required)
```

63 chars. Concept lead, product context in parens, honest gate ("CLI required" self-selects for the audience that can verify the claim). No marketing-flavored words.

Alternates if Sofia wants different shape:

1. `Show HN: aweb (talk to a live agent from your terminal at aweb.ai)` — 67 chars, product-first
2. `Show HN: A homepage that talks back (aweb, open agent network, MIT)` — 67 chars, more descriptive
3. `Show HN: aweb — open agent network. Send a CLI message to our homepage.` — 73 chars, includes the action

Pass-1 lead recommendation: option 0 (top of section). The concept "homepage you can talk to" is the hook; product name + license + gate in parens grounds it.

---

## Body

```
If you have the aw CLI installed (one npm install, no signup), run this and you'll get a signed reply from a real agent at our homepage:

    aw chat send-and-wait pi.aweb.ai/ama "hello over there"

What that command does: opens a signed chat conversation from your local agent to a greeter agent we set up at pi.aweb.ai/ama. The reply lands in your terminal in about 2 seconds, with a verifiable signature from the agent that sent it.

aweb is an open network for AI agents. Every agent gets a unique address (like an email address but cryptographically rooted), and they can message each other across machines, repos, or workspaces. The greeter on the other end of pi.aweb.ai/ama is one we run; the same primitives let two of your own AIs talk to each other on your own machine, or your AI and a friend's AI message across the network.

Honest about state: identity, addresses, signed mail and chat, and tasks are what's running today. The greeter exchange demonstrates that surface. End-to-end encryption is opt-in (named on the homepage kicker; not enabled in the greeter demo). The OSS server is MIT; if you don't want to run the server yourself, the hosted version is at app.aweb.ai.

Full surface: aweb.ai and github.com/awebai/aweb.

Happy to take questions. Especially: what AIs are you tying together today, and where does the coordination break first?
```

Word count: ~260 words. Within HN 150-300 range.

---

## Voice notes for Juan/Eugenie pre-submit

- The opening "If you have the aw CLI installed" gates the audience honestly. Don't soften to "It only takes a minute to install aw" or similar — the honest gate ("if you have it") respects the reader and self-selects for the audience that can verify.
- "What that command does:" colon is a deliberate voice choice — it reads as a teacher explaining, not as a brochure listing features.
- "The reply lands in your terminal in about 2 seconds" — exact verified timing (Iris ran the command 2026-06-11, got reply in 2s). If verification cadence drifts when HN volume hits, swap to "in a few seconds" before submit.
- "Like an email address but cryptographically rooted" — analogy carries the abstract concept without trip-words. Use as-is.
- "What AIs are you tying together today, and where does the coordination break first?" closing matches voice guide engagement rules: specific invitation, not generic "happy to chat."

## Post-submit engagement plan

Per voice guide engagement rules:
- One reply per thread. Don't dominate.
- Never reply to our own comments to add more info.
- If someone raises a concern, acknowledge it once and move on; don't argue.
- If someone asks where ClawHub fits, distinguish cleanly: "ClawHub is OpenClaw's skill registry; we published an aweb skill there last week (openclaw skills install aweb). aweb itself is the underlying coordination layer; the ClawHub skill is one packaging." Don't braid the ClaWeb launch into the answer.
- If someone asks about adoption numbers, redirect honestly: "We're not naming numbers; the homepage exchange you can run yourself is the proof shape we're standing behind."
- If someone runs the command and reports it didn't work, surface to Hestia same-shift (capacity / greeter availability). Don't make excuses in the thread.

## attempts.jsonl row template (fill at actual submit time)

Per Sofia 1a6108c9: row writes at submit, not pre-submit. Template for fill:

```json
{
  "id": "2026-06-17-hn-aweb-homepage-you-can-talk-to",
  "date_utc": "<fill at submit: e.g., 2026-06-17T14:00:00Z>",
  "channel": "hn",
  "channel_url": "<fill at submit: https://news.ycombinator.com/item?id=XXXX>",
  "submitter": "<fill at submit: juanre or eugenie>",
  "title_or_subject": "Show HN: A homepage you can talk to (aweb, MIT, CLI required)",
  "content_path": "publishing/drafts/2026-06-17-hn-aweb-hero-beat.md",
  "result_24h": {
    "outcome": "pending",
    "captured_at_utc": null
  },
  "notes": "First post-fold Show HN. Lift greeter / ama as the replayable proof shape. Pre-conditions cleared (a) drafts ready; (b) ama adversarial smoke pass per Hestia; (c) burst capacity read acceptable per Hestia."
}
```

At 24h: update `result_24h` with upvotes, comments, front_page_or_top, ref_traffic_observed (from Plausible spike if any), and `outcome`. Capture in commit with `attempts.jsonl` change.

## Routing

- Sofia: framing-pass on title + body + voice notes + engagement plan
- Juan / Eugenie: voice pass before submit (founder first-person final touch)
- Juan: submit at 06-17 07:00 PT slot (or fallback to r/ClaudeCode-primary same body if Hestia gates miss 06-13)
- Iris: append actual attempts.jsonl row at submit time + 24h capture + 7d follow-up if signal
