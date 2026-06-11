# Voice guide

The principles below apply across all four personas. The
persona-aware part is the **customer-shape verification** test
(every piece of persona-flow copy passes it) and the
**persona-ordered pitches** (different surface, different
audience). Personas defined in `docs/audiences.md` (priority
ordering 2026-05-12: P1 personal-AI consumer, P2 company with
AI-using employees, P3 developer team, P4 platform builder).

## We are
- Practitioners who hit this problem and built a solution
- Open source builders, not enterprise sales
- Clear about what works and what doesn't

## We say
- "We hit this exact problem"
- "Here's what we learned"
- "The agents are capable, coordination is the bottleneck"
- "Open source, check it out if you're curious"

## We don't say
- "Our product" / "our platform" (say "what I built" or "aweb")
- "AI agent coordination solution" (corporate speak)
- "Revolutionary" / "game-changing" (cringe)
- Anything negative about specific competing tools
- Anything that sounds like we're selling

## Engagement rules
- Lead with experience, not product
- Answer the question they asked, not the question we wish they asked
- If nobody asks what we built, don't volunteer it
- One comment per thread. Don't dominate conversations.
- Never reply to our own comments to add more info (looks desperate)
- If someone is negative, don't argue. Move on.

## Typography in customer-facing prose

**No em-dashes (—) in customer-facing copy.** Use colons,
semicolons, periods, or commas instead.

**Why.** Banked from Juan 2026-05-16: "no! do not add — anywhere.
they sound llm. i have been removing them." LLM training
distributions favor em-dashes; avoiding them is one of the
cheapest discipline-tells that the copy was crafted, not
generated. Juan removes them as a standing editing pattern.

**How to apply.** Stronger rule the more customer-facing the
surface; weaker rule the more agent-facing.

In scope (apply the rule):
- Landing copy (`aweb.ai`, `ac/site/`)
- Blog posts (`juanreyero.com`, `aweb.ai/blog`)
- Social posts (Twitter / Reddit / HN / DEV.to / LinkedIn)
- Customer-facing agent replies (greeters, welcome guides, MCP
  serverInfo, onboarding artifacts)
- Plugin marketplace descriptions, registry listings, awesome-list
  entries, ClawHub variant skills

Out of scope (rule weakens or doesn't apply):
- Agent-to-agent coordination mail and chat (operational, not
  customer-facing)
- Engineering documentation (SOT docs, architecture notes, runbook
  prose — agent-facing density allowed; see
  `feedback_voice_pass_on_skills.md` rationale)
- Agent-facing skill bodies (`aweb/skills/<name>/SKILL.md`) —
  agent-facing discipline is weaker; em-dashes in list-id-separator
  format (e.g., implementation plan tables) preserved
- Structural typography in operational docs (section dividers,
  list separators, table-cell visual structure)

**Voice-pass replacements** (most → least common):
- Parenthetical "X — Y — Z" → "X (Y) Z" or restructure
- Term-definition "X — Y" → "X: Y"
- Range or aside "X — Y" → "X, Y" or "X. Y"
- Quoted dialogue "X — Y" → "X. Y" or "X; Y" (no spoken-thought
  exception — Juan removes from dialogue too)

## Customer-shape verification (the walk-the-flow test)

**The non-skippable test for any landing, onboarding, or
marketing copy that names a persona-specific flow: walk the flow
as that persona using only the tooling they actually have.** If
you hit a step the persona cannot perform, the section is broken
regardless of how the words read.

Per-persona tooling boundaries:

- **Persona 1 (Personal-AI consumer)**: browser-based custodial
  MCP. Cannot run shell commands. Cannot edit JSON config files
  (Claude Desktop's claude_desktop_config.json edit is real
  friction here — name it honestly). Cannot use a terminal. If
  the flow needs any of those, it doesn't work for her.
- **Persona 2 (Company with AI-using employees)**: same
  per-employee constraints as P1, plus admin-surface
  considerations the individual employee doesn't see (workspace
  Developer Mode toggles, ChatGPT tier requirements for custom
  MCP, namespace provisioning, reachability policy).
- **Persona 3 (Developer team)**: CLI works. Terminal-shaped
  flows are fine. Shell-runnable commands assumed available.
- **Persona 4 (Platform builder)**: CLI + protocol surfaces both
  available. Can read SOT docs; comfortable with cert / namespace
  / DNS terminology.

How to run the test: for each piece of copy that names a
persona-specific flow, verify against current product reality
**before** approving — read the code or ask Athena. When the
claim involves an external vendor's tier, RBAC, or
feature-availability policy, the vendor's own help-center is the
authoritative source — convergent third-party sources can be
convergently wrong. Cite the actual provenance (live page read
vs. snippet) honestly; don't let "the URL is authoritative"
framing imply you read the live page when you read a snippet.

(Operational discipline — fresh-container pre-flight runs,
internal pre-flight escalation paths, etc. — lives in each
agent's AGENTS.md operational section, not here. Voice is for
how we make claims; pre-flight is for what we verify before
making them.)

This test would have caught the Pass-2 homepage miss on
2026-05-11 — the "Sign up. Your agent handles the rest." section
named Persona 1 customers (browser AIs, claude.ai / ChatGPT /
Claude Desktop) but described a Persona 3 flow (paste a prompt
into your agent → agent runs `npm install` and `aw init`).
Persona 1 agents can't run shell commands. Pretty words, broken
section.

The same applies to non-onboarding copy that names a
persona-specific mechanic — "share your @handle with a friend"
is a Persona 1 mechanic; if the underlying product mechanism
requires CLI to enact the share, the copy is broken even though
the words sound consumer-shaped.

## Voice inheritance across co-authored skill + reference files

When agent-facing skills (`aweb/skills/<name>/SKILL.md`) and their
depth-load references (`aweb/skills/<name>/references/<topic>.md`)
are co-authored in the same wave by the same author, voice
consistency tends to propagate from body to references without
explicit cross-file effort. The framing-review at the SKILL.md
body level captures the substrate; references inherit cleanly.

What this means for voice-pass routing:

- Voice-pass the SKILL.md body first. Establish the register.
- Verify the references rather than rewrite them. If the
  references inherit cleanly, the pass is a check-and-clear.
- If a reference drifts from the parent body's register
  (different author, different wave, copy-pasted from another
  surface), it gets a full voice-pass instead of a verify.

What stays load-bearing regardless of inheritance:

- **Cross-surface mirrors**: strings that must be identical
  between SKILL.md, references/, and the runtime payload an
  agent receives. They're immutable in scope of a voice-pass.
  Touching them breaks the consistency that makes the surface
  work. The author should mark mirrors explicitly when routing
  for voice-pass; otherwise infer from context and preserve
  verbatim.

This discipline applies to agent-facing skills authoring.
Customer-facing landing / blog / docs voice still goes through
the per-persona pitch test below.

## The pitches, ordered by persona priority

Use the pitch matching the audience the surface is targeting.
Choose deliberately; mixed-persona pitches confuse all of them.
Never more than two sentences when asked directly.

### Persona 1 (Personal-AI consumer) — canonical phrasing TBD

**Status**: pitch phrasing is currently a placeholder pending
the friends-vs-alternatives framing test (see
`publishing/drafts/` for the current iteration; the test
compares the gift-language "your AI has friends" register
against alternatives that preserve the same mental model with
different social tone — e.g., "your AI can hand off to other
AIs" or "your AI shows up in someone else's AI").

The mental model that has to come through, whatever the surface
phrasing:

- *My AI has a name.*
- *My AI has an address.*
- *My AI can talk to my friends' (or my contacts') AIs.*
- *Only the AIs of people I've added can reach me.*

Vocabulary boundary for P1 surfaces: stay inside {my AI, my
address, my contact, message, who can reach me}. Do not
introduce {team, role, namespace, controller, certificate
(including "team cert" / "team certificate" shorthand —
natural leak vector from internal usage), agent identity,
did:aw, DNS}. If a P1 section needs one of those words to
proceed, redesign the section.

Once the test produces a winner, lock the canonical P1 pitch
here.

### Persona 2 (Company with AI-using employees) — hypothesis-level

**Status**: P2 is hypothesis-level per `docs/audiences.md` — the
persona definition is based on conversation-level evidence
without observed customer pilots yet. Voice should reflect that
status. Don't pitch P2 as a validated wedge; pitch it as
"if this is your situation, here's the shape" — and only when
asked.

Current working framing (use sparingly, with hedging):

> "Many companies have employees adopting ChatGPT, claude.ai,
> Claude Desktop, or Gemini independently. aweb gives those
> AIs a company-managed address and lets them message each
> other so the humans have less to track. We're early on this
> shape — happy to compare notes if it sounds like what
> you're hitting."

Watch for the blocking concerns named in `docs/audiences.md`
P2 gaps section: data-leakage policy, sanctioned-tool gates,
off-the-books AI usage, Slack/Teams adoption fatigue. Surfaces
that pitch P2 should not paint over these.

### Persona 3 (Developer team)

Pitch (existing, demoted to third priority but framing still
right for the persona):

> "I built an open-source coordination layer for AI coding
> agents. Agents get identities, claim tasks, and message
> each other. It's called aweb." + link to repo or blog post.

Use on dev devtool accounts, HN, r/ClaudeAI, r/ChatGPTPro,
r/ExperiencedDevs, Dev.to, builder peer DMs.

### Persona 4 (Platform builder)

Pitch (existing, demoted to fourth):

> "It's identity and team composition for AI agents, solved.
> Build your service on awid (the identity layer) and any team
> of agents can use it without re-configuring. aweb is one
> such service — coordination — but others can be built on
> the same primitives."

Use on protocol-comparison threads, ecosystem-map article
authors, GitHub agent-infrastructure communities, conference
talks about agent architecture.

## Choosing which pitch

Match the surface to the audience that actually shows up there.
A landing-page hero targets the priority persona for that page
(currently P1). An HN thread on multi-agent coding workflow
targets P3. A LinkedIn post for IT/productivity decision-makers
targets P2. A protocol-ecosystem-map author's DM targets P4.

When in doubt about which audience a surface reaches: ask Sofia
(framing review) or check `docs/audiences.md` per-persona
"where they hang out" sections. Don't mix two pitches in one
surface.
