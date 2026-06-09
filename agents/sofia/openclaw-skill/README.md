# OpenClaw / ClawHub skill for aweb

Decision (2026-06-09, Juan + Sofia): publish a new canonical `aweb`
skill on ClawHub AND push one final corrected update to the existing
`claweb` slug (625 downloads, content broken against aw 1.26.x:
`--to-alias` and `--unread-only` no longer exist). Future maintenance
lands only on `aweb`; `claweb` v0.4.0 carries the same corrected
content plus a rename pointer.

Every command in both SKILL.md files was verified against installed
`aw` 1.26.8 (`aw <cmd> --help`) on 2026-06-09. Setup flows checked
against the canonical skills in `aweb/skills/` (messaging,
team-membership). Privacy-boundary wording follows the standing
E2EE claim discipline (plaintext default, `--e2ee` fails closed,
hosted paths not E2E).

## Layout

```
openclaw-skill/
├── aweb/SKILL.md     # canonical going forward — v1.0.0
└── claweb/SKILL.md   # final update to old slug — v0.4.0 (after v0.3.23)
```

Folder names = ClawHub slugs (`clawhub sync` derives slug from the
folder containing SKILL.md).

## Publish (requires clawhub CLI authenticated as juanre)

```bash
cd agents/sofia/openclaw-skill
clawhub login                          # if not already authenticated
clawhub sync --dry-run --owner juanre  # preview: should show aweb (new) + claweb (update)
clawhub sync --all --owner juanre      # publish both
```

Verify after publish:

- https://clawhub.ai/juanre/aweb exists at v1.0.0
- https://clawhub.ai/juanre/claweb shows v0.4.0 with the rename note
- `openclaw skills search aweb` finds the new skill (was zero results
  before 2026-06-09)

## Known untested items (acceptable for publish, fix on feedback)

- The cron poller block (`openclaw cron add --every 1m ... NO_REPLY`)
  follows current OpenClaw docs but has not been run on a live
  OpenClaw install — no openclaw binary on this machine. The old
  claweb skill shipped a working cron section at 625 downloads, so
  the shape is proven; the exact flags follow current docs.
- `metadata.openclaw` install hint (`kind: node`,
  `package: @awebai/aw`) follows the documented AgentSkills metadata
  format; not validated against a live OpenClaw parser.

## Follow-ups (research ladder, agents/sofia/openclaw-aweb-research.md)

1. Test Level 0 on a live OpenClaw install (npm bundle
   `@awebai/claude-skills@0.2.12`) — separate machine needed.
2. Marketplace relative-source decision for `awebai/claude-plugins`
   (Level 1) — coordinate with Athena/Hestia, do NOT change npm
   sources unilaterally (Claude Code users pin them).
3. Native OpenClaw plugin (Level 4) — deferred until demand.
