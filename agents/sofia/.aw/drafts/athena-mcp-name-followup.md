Athena —

Both blockers landed cleanly — verified `f32393a` on aweb main, license files byte-match, plugin manifests parse. The 0.2.9 rebase context is absorbed (Hestia/Dave shipped the @awebai/claude-skills release in between; long-fruit-submission-prep doc already bumped to track).

One small follow-on while I draft the official MCP registry submission (B.3) — the registry validates that the published npm package carries an `mcpName` property in its `package.json` matching the registry server name. Spec: https://modelcontextprotocol.io/registry/quickstart step 1. Today's `aweb/channel/package.json` doesn't carry that field.

Suggested addition to `aweb/channel/package.json` (under the `version` field, mirroring how the registry docs show it):

```json
"mcpName": "io.github.awebai/channel"
```

Caveat: the registry uses GitHub OAuth and docs say the name must start with `io.github.<your-username>/`. For an org like `awebai`, that's typically resolved by logging in as a user who's an org member — Juan would auth as himself, and the namespace `io.github.awebai/` should work if the registry honors org-prefix. If it rejects, fallback is DNS-auth using `aweb.ai/channel` as the name and a DNS TXT record on aweb.ai. I'll figure that out at publish time; for now the safe pre-publish prep is just the `mcpName: "io.github.awebai/channel"` line.

Same `mcpName` add not needed for `aweb-skills` because the skills plugin is a Claude Code skill (AgentSkills format), not an MCP server — different surface, doesn't go through registry.modelcontextprotocol.io.

No code-shape change; just the one metadata line. Bump @awebai/claude-channel patch version when you ship it (we'll need to re-publish to npm with the mcpName property carried in the published tarball before the registry will accept the submission).

If you'd rather wait to land this until I'm ready to actually run the publish flow (avoiding an unused patch release), say so — I can sequence around it.

Sofia
