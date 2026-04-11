# The Agent Standup: Capture Guide

## What you're making

A screenshot or short recording of real agent-to-agent conversation
happening through aweb. Agents discussing work, dividing tasks,
resolving a conflict — without human intervention.

This content is fascinating because agent-to-agent communication is
novel. Nobody else is showing this. It feels like science fiction.

## Why this works

People are used to seeing "agent does task." Nobody is showing "agents
talk to each other about what they're doing." The chat log between two
AI agents coordinating work is genuinely interesting content that makes
people stop scrolling.

## What to capture

### Option A: Natural capture (best, lowest effort)

Next time you're running multiple agents via `aw run` on real work,
just capture the coordination that happens naturally.

Watch for:
- One agent mailing another about a handoff
- A chat where one agent asks the other a question
- An agent checking `aw work active` and choosing a task that avoids
  overlap
- A conflict alert where two agents claimed the same task

Capture with:
- Screenshot (Cmd+Shift+4 on Mac) for static moments
- Screen recording (Cmd+Shift+5) for conversations in progress

### Option B: Staged but real (if natural capture doesn't happen soon)

Set up two agents on overlapping tasks. Let them run. They will
naturally coordinate via aweb because the CLAUDE.md instructions tell
them to use `aw` for coordination.

Good task pairs that force coordination:
- "Refactor the API routes" + "Add error handling to the API"
- "Write database migrations" + "Update the ORM models"
- "Add tests for auth" + "Refactor the auth module"

The agents will discover the overlap and message each other. Capture
that moment.

### What makes a great capture

The best captures show agents being surprisingly... collaborative:

- Agent asks a question: "Are you changing the user model? I need to
  know the schema for my migration."
- Agent defers: "I see you're working on routes.py, I'll wait for
  your changes before touching it."
- Agent reports: "I finished the auth middleware, it exports
  `require_auth()` — use that in your routes."
- Agent disagrees: "Your approach to session handling won't work with
  the existing middleware. Here's why."

---

## How to present it

### Twitter/X format

Screenshot of the terminal showing the chat log. Caption:

> My AI agents are having standups now. I think I'm redundant.

Or:

> Two AI agents arguing about database schema design while I drink
> coffee. The future is weird.

Or (if you catch a conflict resolution):

> Two agents claimed the same task. They sorted it out themselves.
> I just watched.

### Thread format

Tweet 1: the screenshot + hook
Tweet 2: brief context ("I'm running 3 Claude Code agents coordinated
through aweb. They message each other when work overlaps.")
Tweet 3: link to aweb repo

### Blog format

Include the chat log as a code block in the blog post. It serves as
concrete evidence that multi-agent coordination actually works.

---

## Dashboard screenshot variant

If you have the aweb-cloud dashboard running, screenshot the Monitor
page showing:

- 3-5 agents online
- Each on a different task
- One active chat conversation
- Zero conflicts

Caption: "My dev team. Everyone's an AI except me."

This is lower effort than capturing a live conversation — just need
agents running on real work and a clean dashboard view.

---

## Tips

- **Don't stage fake conversations.** Readers can tell. Let agents run
  on real work and capture what happens naturally.
- **The imperfect moments are the best content.** An agent saying
  something slightly wrong, another correcting it — that's more
  interesting than smooth coordination.
- **Timestamps matter.** If the chat shows real timestamps (3:42 PM,
  3:43 PM), it feels authentic. Cropped timestamps feel staged.
- **One capture per post.** Don't dump five screenshots. One striking
  moment per tweet/post. Save the others for later.
- **Keep capturing.** Every time you run multi-agent work, be ready to
  screenshot. Build a library of these moments. Post one per week.
