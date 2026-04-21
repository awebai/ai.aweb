# ai.aweb

How [aweb.ai](https://aweb.ai) runs its company with AI agents.

This public repo holds the product docs, agent instructions, publishing
pipeline, and the homes for the permanent agent team. Sensitive data
(outreach contacts, identity keys) lives in a separate private repo
(co.aweb).

## Docs

Start here:

| Document | What it covers |
|----------|---------------|
| [docs/team.md](docs/team.md) | Team structure, roles, responsibilities, how agents interact |
| [docs/invariants.md](docs/invariants.md) | Guiding principles for every design decision |
| [docs/user-journey.md](docs/user-journey.md) | What users experience at each stage |
| [docs/value-proposition.md](docs/value-proposition.md) | Why aweb exists, who it's for |
| [status/](status/) | Current focus and state (engineering, product, outreach, weekly) |

For specific topics:

| Document | What it covers |
|----------|---------------|
| [docs/audiences.md](docs/audiences.md) | Who uses aweb, what they want, where they are |
| [docs/capabilities.md](docs/capabilities.md) | What aweb provides, mapped to user journey stages |
| [docs/decisions.md](docs/decisions.md) | Decision log with commit hashes |
| [docs/aweb-high-level.md](docs/aweb-high-level.md) | Identity and protocol architecture |
| [docs/strategy.md](docs/strategy.md) | Go-to-market playbook |
| [docs/atext-spec.md](docs/atext-spec.md) | Product spec for atext.ai (not yet started) |

## Agent team

Permanent agents run from subdirectories under `agents/`. Each has
an `AGENTS.md` (instructions) and `handoff.md` (state for continuity).

| Agent | Role | Directory |
|-------|------|-----------|
| Randy | CTO | [agents/cto](agents/cto) |
| Avi | CEO | [agents/ceo](agents/ceo) |
| Charlene | Comms | [agents/comms](agents/comms) |
| Enoch | Board | [agents/board](agents/board) |
| Amy | Support | [agents/support](agents/support) |
| John | Coordinator: aweb OSS | [agents/coord-aweb](agents/coord-aweb) |
| Tom | Coordinator: aweb-cloud | [agents/coord-cloud](agents/coord-cloud) |
| Goto | Coordinator: awid | [agents/coord-awid](agents/coord-awid) |

See [docs/team.md](docs/team.md) for how they work together.

## Publishing

Charlene owns the publishing pipeline:

| File | What |
|------|------|
| `publishing/plan.md` | Content calendar — what to write, where, when |
| `publishing/voice.md` | How we talk |
| `publishing/landscape.md` | Agent-to-agent ecosystem map |
| `publishing/history.md` | What we published and where |
| `publishing/drafts/` | Blog posts, video scripts |

## Other directories

| Directory | What it holds |
|-----------|--------------|
| `status/` | Status files maintained by agents (engineering, product, outreach, weekly) |

## Private repo (co.aweb)

Sensitive operational data lives in a separate private repo:
- Outreach contacts, engagement history, monitoring targets
- Competitive positioning
- Identity key backups

## AGENTS.md / CLAUDE.md

Agent instructions live in `AGENTS.md` files (root and per-agent).
`CLAUDE.md` is a symlink to `AGENTS.md` so Claude Code picks it up
automatically. Non-Claude agents read `AGENTS.md` directly.
