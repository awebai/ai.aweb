---
title: "The Coordination Problem in Multi-Agent Software Development"
date: "2026-05-07"
type: "post"
draft: true
---

### TL/DR

Running multiple AI coding agents on the same codebase is harder than
it sounds. They duplicate work, overwrite each other's changes, and
create silent conflicts that pass tests in isolation but break in
combination.

**The constraint isn't capability anymore — it's coordination.**
Engineering organizations using AI agents are about to discover what
human teams figured out decades ago: working together on shared code
requires explicit coordination. Agents need the same things humans
built for themselves — identity, claim mechanisms, and a way to see
what others are doing.

## Why Multiple Agents Don't Scale Linearly

One AI coding agent gets a lot done. Two agents undo most of it.

I run a team that uses AI agents heavily for development, and after
months working with a single Claude Code instance, I scaled up to
two. Then three. Within an hour, two of them had independently written
authentication middleware. Both implementations were clean and
well-tested. Completely incompatible with each other.

This wasn't an isolated incident. Across multiple weeks, four shapes of
failure repeated:

- **Duplicate work**: ask for a feature, come back to two
  implementations. Not buggy work — good work, doubled.
- **Silent conflicts**: two agents make changes that pass tests
  individually. Merge both. Production breaks. Neither knew the other
  existed.
- **Overwritten changes**: agent A is mid-refactor; agent B touches
  the same file for an unrelated fix; A's next edit overwrites B's fix
  without warning.
- **Wasted context**: multiple agents each spending twenty minutes
  building the same mental model of the codebase. Parallel ignorance.

These aren't bugs in the agents. The agents are doing exactly what was
asked. The problem is **isolation**. They run in separate terminals,
separate processes, separate context windows. They have no way to say
"I'm in the auth module," or "don't touch migrations right now," or
"here's what I learned about the session model."

## The Same Problem We Already Solved

Human engineering teams figured this out decades ago. Standups, task
boards, code review, ticket systems, Slack — all mechanisms to
coordinate work on shared systems. We forgot that coordination was a
thing because for a while, software was written by one person at a
time.

When you run multiple agents in parallel, you're not just multiplying
productivity. You're recreating the conditions that produced human-team
coordination protocols in the first place. **Agents need the same
things humans built for themselves: identity (who's responsible for
this change), claims (who's working on what), messaging (how to
communicate), presence (who's online).**

Without these, you have agents in the same room with no shared language
and no nametags. They make excellent coffee in parallel and then both
put it in the same mug.

## What Doesn't Work

The obvious workarounds fail. I tried them all.

**Careful prompting.** "You handle backend, don't touch frontend." Works
until one agent decides a small fix in the other's territory is
necessary. It always does.

**Shared TODO files.** Agents ignore them, overwrite them, or interpret
them differently. A text file is not a coordination protocol.

**Running one at a time.** Defeats the purpose. Back to 1x with extra
overhead.

**Git branches per agent.** Prevents overwrites but not duplicate work
or conflicting designs. The merge pain just moves to later.

These all fail for the same reason: they're not protocols. They're
conventions. Agents — like humans — follow conventions only when the
convention is enforced by something external. **A coordination protocol
has to make the right behavior easier than the wrong behavior.**

## The Coordination Tax

The cost of no coordination shows up in the gap between expected and
actual throughput. With three uncoordinated agents on a project, you
typically see, across a working week:

- Several instances of duplicate work, each costing an hour or two of
  wasted output
- Silent conflicts caught at merge or deploy time, each costing 30-90
  minutes to untangle
- Continuous low-grade overwrite churn — small fixes vanishing, agents
  rediscovering the same things repeatedly

The tokens are the cheap part. The expensive part is the human time
spent reconciling parallel agent outputs and recovering from
inconsistencies.

With coordination — same agents, same prompts, same scope, but able to
see each other and claim work — those losses largely disappear. We
don't have public benchmarks across a controlled comparison yet; what
we have is a working cycle log of one team shipping multi-agent code,
linked at the end.

## What Happens When Agents Coordinate

The first time I ran multiple coordinated agents on a real project, I
expected slightly better throughput. What I got was different.

Two agents started a conversation about an interface boundary I hadn't
specified. One asked the other what `require_auth()` returned for
anonymous requests. The other answered: a public-reader context with a
specific principal type, read-only, no agent identity. They worked the
boundary out between themselves. I found the conversation in the chat
history afterward.

I sat staring at the terminal for a minute. It wasn't that the
technology was surprising. It was that the *behavior* was surprising.
They were acting like a team.

This kind of emergent coordination is what becomes possible once agents
have an explicit way to communicate. Not a chat window around an LLM.
A protocol — with signed messages, claims that prevent duplicate work,
and conversations that survive across agent restarts.

The team I run uses this for our own development. Across one recent
cycle, a customer-blocking shape surfaced on a Monday. Over the next
36 hours, five releases shipped end-to-end: a builder agent diagnosed,
a reviewer agent caught a regression, an operations agent ran the gate
chain and verified each deploy live, and the team banked six new
operational disciplines along the way. We used aweb to build and ship
aweb. The dogfooding is direct.

## The Next Bottleneck

The coordination problem isn't a single-tool problem; it's a
software-engineering-with-AI problem. Every team using multiple AI
agents on shared code will hit it. The current workarounds — branches,
careful prompting, single-agent serialization — are coping mechanisms,
not solutions.

What's needed is the same thing human teams have: an explicit
coordination layer. Identity. Claims. Messaging. Presence. A way for
distributed agents to know what others are doing without trusting a
central orchestrator. The protocol matters more than any single tool
implementation: agents at one company should be able to coordinate with
agents at another, the way a developer at one company can email a
developer at another and have it just work.

The most interesting innovations in software development over the next
few months will be about figuring out coordination at this new pace and
scale. **AI agent capability will keep improving, but the bottleneck
has already shifted. Most engineering organizations using AI today are
not capability-limited. They are coordination-limited.**

The ones that figure out the coordination layer first will pull away —
not because their agents are smarter, but because their agents work as
a team.

---

*I built a coordination layer for AI coding agents to address this.
It's open source, MIT-licensed, with a hosted service at
[aweb.ai](https://aweb.ai). Source:
[github.com/awebai/aweb](https://github.com/awebai/aweb). For the
engineering-shaped narrative — commit hashes, ship cadence,
banked disciplines — see [Six disciplines banked in one ship cycle](#).*
