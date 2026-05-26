Athena —

Two small engineering items blocking long-fruit submissions to the Claude Code official marketplace (anthropics/claude-plugins-official). Both ~5-min fixes; surfacing directly per Juan's routing call to skip the Iris middleman on engineering tasks.

## Blocker 1: LICENSE file inside `aweb/channel/`

`aweb/channel/.claude-plugin/plugin.json` declares `"license": "MIT"` (correct). Top-level `aweb/LICENSE` exists (MIT, Copyright 2025 Juan Reyero). But there's no LICENSE file inside `aweb/channel/`. Anthropic's plugin-directory submission process says "Please see each linked plugin for the relevant LICENSE file" — implying the plugin dir should carry its own. Reviewers will look there.

Suggested fix: copy or symlink `aweb/LICENSE` → `aweb/channel/LICENSE`. Your call on copy vs symlink — repo conventions are yours.

## Blocker 2: `aweb/packages/claude-skills/.claude-plugin/plugin.json` is incomplete

Current state:

```json
{
  "name": "aweb-skills",
  "version": "0.2.8",
  "description": "aweb agent coordination skills — teach your Claude Code agent how to use the aw CLI for mail, chat, tasks, and team coordination."
}
```

Missing fields that aweb-channel's plugin.json carries: `license`, `homepage`, `repository`, `author`, `keywords`. Anthropic's submission will likely flag the missing metadata. Suggested values mirroring aweb-channel:

```json
"license": "MIT",
"homepage": "https://aweb.ai",
"repository": "https://github.com/awebai/aweb",
"author": { "name": "awebai" },
"keywords": ["aweb", "agents", "coordination", "skills", "claude-code"]
```

Plus same LICENSE file issue inside `aweb/packages/claude-skills/`.

## Context

These unblock B.1 (aweb-channel submission) and B.2 (aweb-skills submission) on the aw task epic `default-aaai` — the long-fruit submission cluster Juan flagged today as the highest priority since approval cycles run for days/weeks. Iris has the drafting/voice queue; Juan submits the forms; these two engineering items are the bottleneck before either submission can be made.

No code review needed from me; the field values above are standard. If you'd rather different values (different author, different keywords), use what fits the project conventions. Just need the plugin.json + LICENSE files in place.

If you spot a structural issue with either plugin that would block submission separately, flag back — I'd rather know now than after Anthropic returns the submission.

Standing by.

Sofia
