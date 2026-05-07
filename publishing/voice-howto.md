# Voice guide — how-to-shaped artifacts

How-tos have different voice constraints than essays. Use this when
writing onboarding guides, setup walkthroughs, recovery runbooks, or
anything where the reader is mid-task with a goal in front of them.

For essay-shaped artifacts (problem → narrative → claim), see
`voice.md` and the sample template at `sample.md`.

## We are
- A peer who has done this and is showing the steps
- Telling readers what to expect, what to verify, what to do when it
  breaks
- Not selling them on why to do it — they're already doing it

## Shape
- **Open with the outcome.** "What you'll have at the end" or
  equivalent. No TL/DR; the reader is here to do the thing.
- **Prerequisites listed plainly.** Versions named. Tools named.
- **Numbered steps.** Each step does one thing. Verification follows.
- **Common Issues section near the end.** This is the trust-building
  part: name the actual error text + the actual fix.
- **What's next as soft pointer.** Optional further reading. No
  oversell.

## We say
- "Run this."
- "You should see this." / "Should print 1.20.2 or higher."
- "If you see X, run Y."
- "This blocks until …"
- "Verify with …"
- "On a fresh machine, this completes in about N minutes."

## We don't say
- "Welcome!" / "Congratulations!" / "You're now ready to…"
- "Simply run …" — everything is "simply" until it isn't.
- "Don't worry, …"
- Marketing voice in the middle of a step. "This unlocks the power of
  coordination" is wrong; "This makes both agents visible to each
  other" is right.
- Claims about what comes next that aren't in the next step.

## Engagement rules
- Answer the question the reader is currently doing, not the question
  we want them to do later.
- If a step has multiple paths (BYOD vs managed, etc.), name them
  upfront and split the steps clearly.
- Never assume the reader read the essay first. Some did, most
  didn't.
- Verification steps are not optional content. They tell the reader
  the step worked. Skip them and the reader has to guess.
- The Common Issues section is most of why how-tos build trust. Be
  specific. Use the actual error text.

## What success looks like

A reader can copy the commands top to bottom, hit one of the named
common issues, fix it from the named remediation, and end up at the
named outcome — without ever having to ask us a question.

If a reader would have to read the essay first to follow the how-to,
the how-to is wrong.
