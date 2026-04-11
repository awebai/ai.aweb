# The Chaos Video: Recording Guide

## What you're making

A 60-90 second screen recording showing the before/after of
multi-agent coordination. Part 1: chaos. Part 2: calm.

## Setup

### Recording tool

macOS built-in: Cmd+Shift+5, select screen region, record.

Or use QuickTime Player → File → New Screen Recording for more control.

Record at 1920x1080 or your native resolution. You'll trim later.

### Terminal setup

Use a clean terminal with readable font size (14-16pt). Dark background
preferred. No personal info visible in the prompt.

Split your screen or use tmux to show 2-3 terminal panes simultaneously.
The viewer needs to see multiple agents acting at once.

### Repository

Use a small, clean repo. Something with 5-10 files where conflicts are
obvious. A simple web app works well — agents will naturally both want
to touch `app.py`, `routes.py`, or similar.

If you don't want to use a real project, create a throwaway repo with
a README that describes a simple feature ("Add user authentication with
login/logout and a protected dashboard page").

---

## Part 1: Chaos (30-40 seconds)

### What to record

Start 3 Claude Code instances (3 terminal panes) on the same repo,
same branch, no coordination. Give each the same task or slightly
overlapping tasks:

```
Terminal 1: "Add user authentication with login and logout"
Terminal 2: "Add user authentication with session management"
Terminal 3: "Add a user database model and login page"
```

Let them run for 5-10 minutes. You don't need to record all of this
in real time — record selectively and speed up the boring parts.

### What to capture

You want at least 2-3 of these visible in the recording:

- **Two agents creating the same file.** Git conflict when you try to
  commit both.
- **One agent overwriting another's changes.** One is mid-edit, the
  other saves the same file.
- **Duplicate implementations.** Two different `auth.py` files with
  different approaches.
- **Failing tests.** Tests pass individually per agent but fail when
  combined.

### How to show it

Fast-forward through the agents working (2x-4x speed with a caption
like "3 agents, same task, no coordination"). Then show the aftermath:

```bash
git status        # shows conflicts
git diff          # shows incompatible changes
pytest            # shows failures
```

### Text overlay

Add a simple text caption at the start:

> "3 AI agents. 1 codebase. No coordination."

And at the point of failure:

> "Every agent did exactly what I asked."

You can add text overlays with iMovie (free on Mac), or just put them
as terminal echo commands:

```bash
echo "=== 3 agents, 1 codebase, no coordination ==="
```

---

## Part 2: Calm (30-40 seconds)

### What to record

Same repo, same 3 agents, but now using aweb:

```bash
# Terminal 1
aw run claude

# Terminal 2 (different worktree)
aw workspace add-worktree developer --alias agent-two
cd ../worktree-agent-two
aw run claude

# Terminal 3 (another worktree)
aw workspace add-worktree developer --alias agent-three
cd ../worktree-agent-three
aw run claude
```

Give them the same task. Show:

- **Task claims**: one agent claims "authentication backend," another
  claims "login page," third claims "tests."
- **No conflicts**: each agent works in its worktree, on its claimed
  piece.
- **Agent chat**: one agent asks another "what's the session model?"
  and gets an answer.

### How to show it

Side-by-side terminal panes. Show `aw workspace status` with all three
agents visible, each on a different task. Show `aw work active` with
clean task distribution. Show a chat exchange between agents.

### Text overlay

> "Same agents. Same codebase. Now they coordinate."

And at the end:

> "aweb.ai — open source"

---

## Editing

### If you have iMovie (free, already on your Mac)

1. Import the screen recordings.
2. Trim dead time. The viewer should never wait more than 3 seconds for
   something to happen.
3. Speed up agent work (2x-4x). The point is the result, not watching
   code scroll.
4. Add text overlays for the captions.
5. Add a simple cut between Part 1 and Part 2. A 1-second black screen
   with "Now with coordination" is enough.
6. No music. No intro animation. This is a developer video, not a
   commercial.

### If you don't want to edit

Just record two takes — chaos and calm — and post them as a Twitter
thread:

Tweet 1: chaos video + "I asked 3 AI agents to build a login page at
the same time."

Tweet 2: calm video + "Same agents, now they can see each other."

Tweet 3: link to aweb repo.

---

## Posting

### Twitter/X

Post the video natively (upload to Twitter, don't link YouTube).
Native video gets 5-10x the impressions of external links.

Caption for the first tweet: short, punchy, no hashtags. Something
like:

> I asked 3 AI agents to build the same feature. This is what happened.

Let the video do the work. Don't explain aweb in the tweet — let
people ask.

### Reddit

r/ClaudeAI and r/ChatGPTPro allow video posts. Same clip, different
framing:

> "Anyone else running into this? Multiple agents, same repo, total
> chaos. I built a coordination layer to fix it (open source)."

### LinkedIn

Same video, more professional framing:

> "We're entering the era of multi-agent development. The agents are
> capable. The coordination problem is unsolved. Here's what it looks
> like, and what I'm building about it."

---

## Timeline

Total time to produce this: 2-3 hours.

- 30 min: set up the demo repo and terminal layout
- 30 min: record the chaos run (let agents run, capture the mess)
- 30 min: record the coordinated run
- 30 min: trim and edit (or skip and post as thread)
- 30 min: write captions and post
