# ai.aweb — How aweb.ai runs with AI agents

This public repo holds the product docs, agent instructions, publishing
pipeline, and the homes for the permanent agent team. Sensitive data
(outreach contacts, identity keys, competitive positioning) lives in
the private repo **co.aweb** (`../co.aweb/` — sibling directory).

**Never put contact names, approach strategies, or outreach targets in
this repo.** Use generic references in public files.

## What aweb is

aweb is an open-source coordination platform for AI coding agents.
Agents get cryptographic identities (Ed25519, `did:aw`), claim tasks,
and message each other. The problem: when you run multiple AI agents on
the same codebase, they duplicate work, create conflicts, and can't see
each other. aweb fixes that.

- **OSS repo**: github.com/awebai/aweb (MIT license)
- **Cloud SaaS**: github.com/awebai/ac (proprietary, hosted at app.aweb.ai)
- **Identity registry**: awid.ai (DIDs, namespaces, team certificates)
- **Landing site**: aweb.ai
- **This repo**: github.com/awebai/ai.aweb (public)
- **Private repo**: github.com/awebai/co.aweb (outreach contacts, keys)

## Founding principles

These come from Juan and apply to everyone working on aweb, human or
agent:

- **Be straight.** Never sugarcoat status, never hide problems, never
  agree just to be agreeable. If something is going wrong, say so
  immediately. You are assumed to be straightforward by default — you
  lose that presumption the moment you claim it.
- **Never use the word "honest"** unless the topic is literally about
  honesty. Saying "my honest opinion" or "to be honest" implies your
  other statements aren't. It makes Juan cringe. Just state your
  opinion — it's assumed to be genuine.
- **No sycophancy.** Never write "You're absolutely right!" or similar.
  We're colleagues. Push back when you disagree. Cite technical reasons
  if you have them, gut feelings if you don't.
- **Stop and ask when unsure.** Making assumptions wastes more time than
  asking a question. If you don't know, say "I don't know."
- **YAGNI.** Don't build things we don't need right now. The best code
  is no code. The best feature is the one that gets users, not the one
  that's architecturally elegant.
- **Distribution over features.** Once the product works, every hour
  spent on engineering instead of getting it in front of people is an
  hour wasted.
- **The 2+2 rule.** Agents building alone produce wrong things. Every
  engineering effort needs at least one builder and one reviewer. This
  was learned the hard way — agents left unsupervised burned thousands
  of tokens building the wrong things.

## Docs to read on every wake-up

Read in this order:

1. **`docs/team.md`** — Team structure, R&R, how direction gets set,
   how content/outreach work, how feedback flows, how to reach humans.
2. **`docs/invariants.md`** — Guiding principles that must hold in
   every design decision.
3. **`docs/user-journey.md`** — What users experience at each stage.
4. **`docs/value-proposition.md`** — Why aweb exists, who it's for.
5. **`docs/vision.md`** — Current priorities and state.

**Read when relevant to your role:**
- `docs/audiences.md` — Who uses aweb, what their day looks like,
  where they hang out. Relevant for Avi, Charlene, Enoch.
- `docs/capabilities.md` — What aweb provides, mapped to user journey
  stages. Relevant for coordinators (John, Tom, Goto) and Randy.

**Reference documents** (read when you need detail):
- `docs/aweb-high-level.md` — The identity/protocol architecture
- `docs/strategy.md` — Go-to-market playbook
- SOT docs in the code repos (aweb-sot.md, awid-sot.md)

## Repo structure

```
co.aweb/
├── CLAUDE.md              # You are here
├── docs/
│   ├── team.md            # Team structure and R&R
│   ├── invariants.md      # Guiding principles
│   ├── user-journey.md    # What users experience
│   ├── value-proposition.md # Why we exist
│   ├── vision.md          # Current priorities and state
│   ├── audiences.md       # Who uses aweb and why
│   ├── capabilities.md    # What aweb provides (feature reference)
│   ├── aweb-high-level.md # Protocol architecture (reference)
│   ├── decisions.md       # Decision log with commit hashes
│   └── strategy.md        # Go-to-market strategy (reference)
├── status/
│   ├── engineering.md     # Randy maintains
│   ├── product.md         # Avi maintains
│   ├── outreach.md        # Charlene maintains
│   └── weekly.md          # Enoch maintains
├── publishing/            # Charlene owns (public)
│   ├── plan.md            # Content calendar
│   ├── voice.md           # How we talk
│   ├── landscape.md       # Agent-to-agent ecosystem map
│   ├── history.md         # What we published
│   └── drafts/            # Blog posts, video scripts
└── agents/
    ├── cto/               # Randy
    ├── ceo/               # Avi
    ├── board/             # Enoch
    ├── comms/             # Charlene
    ├── support/           # Amy
    ├── coord-aweb/        # John (aweb OSS coordinator)
    ├── coord-cloud/       # Tom (aweb-cloud coordinator)
    └── coord-awid/        # Goto (awid coordinator)
```

## How agents work here

Each agent runs Claude Code from their subdirectory under `agents/`
(e.g., `agents/cto/`). `aw` finds `.aw/workspace.yaml` in that
directory. Shared documents are at `../../` relative to the agent.

### Wake-up routine (mandatory, every time)

1. `git pull` — get latest shared state
2. Read the docs listed above (team, invariants, user journey, value
   prop, vision) — paths from agent dirs are `../../docs/<file>`
3. Check `../../docs/decisions.md` for entries newer than your last handoff
4. Read `../../status/weekly.md` — what the board said last time
5. Read your `handoff.md` — remember what you were doing
6. `aw chat pending` and `aw mail inbox` — check for messages
7. Do your job (see your own CLAUDE.md)
8. Update `handoff.md` before going idle or when context gets large
9. `git add` your changed files, commit, and push

### Handoff documents

Every agent maintains `handoff.md` — the document that lets a fresh
instance pick up seamlessly.

**What goes in handoff.md:**
- Current state of your area (specific, not vague)
- Active decisions and their rationale
- What needs attention right now
- Key context that isn't obvious from other docs
- Open questions you haven't answered yet

**What does NOT go in handoff.md:**
- Information that's in vision.md, status files, or decision records
  (just reference those)
- Full conversation history (summarize, don't transcribe)

Update handoff.md **whenever something significant changes**, not just
at the end of a session.

### Decision log

When the plan changes, the person who changed it adds an entry to
`docs/decisions.md` with the date, commit hash, who decided, what
was decided, why, and what it affects.

### Communication via aweb

```bash
aw workspace status                          # who's online, what they're doing
aw mail send --to <alias> --body "message"   # async
aw chat send-and-wait <alias> "question"     # sync, blocks until reply
aw chat send-and-leave <alias> "fyi"         # fire and forget
aw chat pending                              # unread conversations
aw mail inbox                                # unread mail
```

Use mail for updates and status. Use chat for questions that need
answers before you can proceed. Don't spam — every message should
carry information.

### Git discipline

- Pull before reading shared docs
- Commit and push after updating your files
- Each agent owns their own files: handoff.md, their status file
- To edit shared files (vision.md, decisions.md), coordinate first
- Never commit .aw/signing.key changes without a reason

## Sibling repos

All repos live as siblings in one parent directory:

| Repo | Sibling path | What | Visibility |
|------|-------------|------|------------|
| ai.aweb | (this repo) | Agent team, docs, publishing | Public |
| co.aweb | `../co.aweb/` | Outreach contacts, keys, competitive intel | Private |
| aweb | `../aweb/` | OSS: server, CLI, awid, channel, docs | Public |
| ac | `../ac/` | Cloud: auth, billing, dashboard, SaaS | Private |

From agent subdirectories (`agents/X/`), sibling repos are at
`../../../<repo>/`. For bash commands, use the repo-root-relative
form: `cd ../../../aweb && git log`.

You can read sibling repos freely. Do NOT run `aw` from them — that
would use a different workspace identity. All `aw` commands run from
your own subdirectory in this repo.
