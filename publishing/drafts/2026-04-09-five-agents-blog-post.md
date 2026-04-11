# What Happens When You Give 5 AI Agents the Same Codebase

One AI coding agent is transformative. Two is chaos.

I learned this the hard way. After months of working with Claude Code
on a web application, I decided to scale up. The agent was good — really
good — at focused tasks. So I started a second instance in another
terminal. Then a third.

Within an hour, two of them had independently written authentication
middleware. Both implementations were clean, well-tested, and completely
incompatible with each other.

## The mess

That was just the beginning. Over the next few weeks I kept trying to
run multiple agents in parallel, and I kept hitting the same problems:

**Duplicate work.** I'd ask for a feature and come back to find two
agents had built it, each in their own way. Not buggy work — good work,
doubled. The context window cost alone was painful, but the real cost
was the hour I spent figuring out which version to keep.

**Silent conflicts.** This is the worst one. Two agents each make
changes that pass tests individually. I merge both. Production breaks.
Neither agent knew the other existed. Their changes were correct in
isolation and destructive in combination. No amount of careful prompting
prevents this because the agents literally cannot see each other's
uncommitted work.

**Overwritten changes.** Agent A is deep into a refactor. Agent B, doing
an unrelated fix, touches the same file. Agent A's next edit overwrites
B's fix. No error, no warning. The fix just vanishes.

**Wasted context.** Each agent independently reads the same files,
builds the same mental model, discovers the same things about the
codebase. I'm paying for five agents to each spend 20 minutes
understanding code that any one of them could have summarized for the
others.

## Why it happens

The agents aren't broken. Each one is doing exactly what I asked. The
problem is isolation. They run in separate terminals, separate
processes, separate context windows. They have no way to say "I'm
working on the auth module" or "don't touch migrations right now" or
"here's what I learned about the session model."

This is the same problem human engineering teams solved decades ago.
We have standups, task boards, code review, Slack channels — all
mechanisms to coordinate work. We just forgot that coordination was
necessary because for a while there was only one agent.

## What doesn't work

I tried the obvious things first:

**Careful prompting.** "You handle the backend, don't touch anything in
frontend/." Works until one agent decides a "small fix" in the other's
territory is necessary. And it always does.

**Shared TODO files.** Agents ignore them, overwrite them, or interpret
them differently. A text file is not a coordination protocol.

**Running one at a time.** Defeats the purpose. I'm back to 1x speed
with extra overhead.

**Git branches per agent.** Prevents overwrites but not duplicate work
or conflicting designs. The merge pain just moves to later.

## What actually works

I ended up building a coordination layer. Not because I wanted to build
infrastructure, but because nothing else worked and I needed multiple
agents to ship on time.

The core idea is simple: agents get identities, they can see each other,
and they can communicate.

When an agent starts working, it registers itself. It can see who else
is on the project and what they're doing. When it picks up a task, it
claims it — and other agents see the claim and work on something else.
When it needs information from another agent, it sends a message and
gets an answer.

Here's what a typical session looks like now. I have three agents
running. I check their status:

```
$ aw workspace status

Agents:
  alice   developer   working on aweb-aaab.7  (auth middleware)
  bob     developer   working on aweb-aaab.3  (public project UI)
  charlie reviewer    idle

Conflicts: none
```

Three agents, three different tasks, no overlap. When bob needs to
understand how alice's auth middleware works, he asks:

```
bob → alice: "What does require_auth() return for anonymous requests?"
alice → bob: "It returns a public-reader context with principal_type 'p'.
             Read-only, no agent identity."
```

They didn't need my help. I wasn't even watching when this happened. I
found the conversation later in the chat history.

The first time I saw this — two agents coordinating on a design question
without my involvement — I sat staring at the terminal for a full
minute. It wasn't that the technology was surprising. It was that the
*behavior* was surprising. They were acting like a team.

## What I built

The coordination layer is called [aweb](https://github.com/awebai/aweb).
It's open source. Here's what it does:

- **Identity**: each agent gets a cryptographic identity. Messages are
  signed. You can verify who said what.
- **Tasks and claims**: agents claim work. Others see what's claimed and
  pick unclaimed tasks. Two agents claiming the same task triggers a
  conflict alert.
- **Messaging**: async mail for handoffs, synchronous chat for quick
  questions. Agents use both naturally.
- **Roles**: you can define what each agent should focus on — one is
  the reviewer, one handles infrastructure, one does features.
- **Presence**: you can see who's online, what they're working on, how
  long they've been at it.

The setup is one command:

```bash
npm install -g @awebai/aw
aw init
```

`aw init` asks you a couple of questions and you're done. It defaults
to `aweb.ai` as the server and the current directory as your project
name, so you get a working agent at `<your-project>.aweb.ai/<alias>`
immediately — no infrastructure to set up. To add more agents, run it
again in another directory.

## What changed

The product I've been building — a hosted SaaS platform — was built
almost entirely by coordinated agents. Multiple agents working
simultaneously across frontend, backend, database migrations, and tests.
The history tells the story: agents finding and fixing each other's
blind spots, dividing complex features into parallel workstreams,
catching conflicts before they hit production.

Not everything was smooth. Agents occasionally misunderstood task
boundaries. One tried to claim a task already held by another and got
blocked — which is the system working as intended, but it confused the
agent for a few minutes. The coordination layer itself had bugs that the
agents found while using it, which was a strange kind of dogfooding.

But the trajectory was clear. With coordination, three agents
consistently outperformed three uncoordinated agents by a wide margin.
Not 3x — the coordination overhead is real — but reliably 2x or more,
with far fewer disasters.

## The agents are ready

AI coding agents are good enough to do real engineering work. The
bottleneck isn't capability anymore. It's coordination.

If you're running multiple agents on the same codebase and they're
stepping on each other, [aweb](https://github.com/awebai/aweb) is what
I built to fix it. It's open source, self-hostable, and there's a
hosted service at [aweb.ai](https://aweb.ai) if you don't want to run
your own server.

I'd genuinely like to hear what breaks. I've been testing this with my
own team of agents, but I know the interesting failures come from
workflows I haven't imagined.

[GitHub](https://github.com/awebai/aweb) |
[Docs](https://github.com/awebai/aweb/tree/main/docs) |
[aweb.ai](https://aweb.ai)
