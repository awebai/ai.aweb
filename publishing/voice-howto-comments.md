# Voice guide — comments and engagement

How to write comments that engage on someone else's thread (HN, Reddit,
dev.to, blog, etc.) and the pinned author comment on our own Show HN.

For essay-shaped artifacts, see `voice.md` and `sample.md`.
For step-by-step how-tos, see `voice-howto.md`.

## The template (banked from the AHK + Show HN cycle, 2026-05-07)

Field-tested by Juan and Eugenie. Verbatim:

- Keep it simple, genuine, short.
- No constructed pivots, no leading questions, no "disclosure" tags.
- Just a warm reaction, one honest sentence about what aweb does in
  context, and a link.
- Trust the reader to follow up.
- Complexity is the enemy.

The reference shape Juan landed on for an AHK comment:

> "This is very cool. We have been working on a communication layer
> that would be, I believe, complementing it by allowing the agents
> to actually talk to each other and to agents in other teams:
> https://github.com/awebai/aweb"

Three sentences. Warm opener + honest one-sentence context + link.
That is the canonical shape for engagement comments going forward.

## Engagement comment shape (commenting on someone else's thread)

- One warm reaction line — genuine, not constructed.
- One honest sentence about what aweb does in context. "We have
  been working on a layer that would, I believe, complement it
  by ..." reads humble. "We've solved" reads pitchy.
- One link to the load-bearing artifact. Usually
  `github.com/awebai/aweb`.
- That is all. Trust the reader.

## What we don't do

- No "disclosure" tags. They read manipulative. The link itself is
  disclosure.
- No leading questions. Even a soft "would be curious whether you
  considered making them configurable" reads as critique-disguised-
  as-question and pulls the other person defensive.
- No architecture critique on someone else's thread. It is their
  thread, not a comparison thread.
- No constructed "you have gap X, here is what we built that fills
  it" pivots. Reads as setup-for-pitch.
- No closer like "either way, nice work." From a competing-founder
  voice this reads condescending.

## Pinned author comment shape (on our own Show HN)

The pinned author comment is the same template with slightly more
work because the author has to set context that the guest commenter
does not. But the spirit is the same: simple, genuine, short.

What the pinned author comment does:

- Warm opener acknowledging the reader is here. ("Thanks for taking
  a look." is fine.)
- One honest practitioner-voice sentence on why we built this and
  what it does. Lead with experience, not product.
- One try-it command line so a curious reader can move from "what is
  this" to "let me try" in one step.
- Depth-link signposts (one or two) for skeptics who want receipts.
- Source link.
- Invitation to questions.

Length: 3–4 short paragraphs, ~100–150 words. Not 3–4 paragraphs of
architecture. Anyone who wants protocol depth clicks the depth-link.

## Pinned-comment honesty checklist

Before a pinned comment goes out, every claim in it must be
verifiable today:

- Install command produces what the comment claims it produces (run
  the fresh-machine pre-flight; do not gloss the "what if a single
  init produces only one agent" detail).
- Capabilities named are shipped at the current released version,
  not roadmap.
- Depth-link targets are public by submit time. A pinned comment
  cannot link to a draft.
- No quantitative claim ("2x+", "5x faster", "in 5 minutes") without
  the receipt.
- No "entirely on AI agents" / "fully autonomous" framing —
  honest framing names where humans are in the loop.

If a claim cannot pass the checklist, the claim comes out, not the
draft.

## Engagement rules (forward)

The same engagement rules from `voice.md` apply, plus:

- One comment per thread. Even if someone replies asking a follow-up
  question, do not pile on architecture context.
- Never reply to your own comment to add more info. Looks desperate.
- If the thread surfaces a comparison question (MCP, A2A, ANP,
  AHK, etc.), answer briefly and factually with the layer framing,
  no positioning argument.
- If someone is negative, do not argue. Move on.
