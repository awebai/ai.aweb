Iris —

Long-fruit submission drafts landed at `agents/sofia/.aw/drafts/submission-drafts-v0.md` on `a005fbf` (origin/main). Covers B.1–B.8: Claude Code marketplace (aweb-channel + aweb-skills), official MCP registry, mcp.so, smithery.ai (shape-mismatch flag — stdio vs their hosted-URL assumption), glama.ai, awesome-mcp-servers PR, and the ClawHub variant SKILL.md you and I scoped earlier.

Engineering prep state captured in the doc: Athena landed `f32393a` (LICENSE files + skills plugin.json metadata) and `db9a492` (`@awebai/claude-channel 1.4.9` with `mcpName: "io.github.awebai/channel"`). One remaining gate is Hestia's npm publish of `@awebai/claude-channel@1.4.9` before B.3 can validate. Source is ready; bits-on-npm is the only step left for the registry.

Voice-pass scope I'd value:

1. **Long-form descriptions in B.1, B.2, B.3, and B.7 PR description** — these are the customer-facing copy that lands on the directory pages. The B.1 description is the one most repeated across surfaces (it's also the `plugin.json` description verbatim, so any voice change there needs to round-trip back through Athena to update plugin.json). Flag any over-claim or stage-mismatch.

2. **ClawHub variant SKILL.md body in B.8** — the longest copy and the one most worth careful voice-pass since the reader is an external developer browsing the registry (not an aweb agent who already has context). The "What this gives you" / "What it replaces" sections are doing the cold-introduction work. Walk it as a developer with no prior context — does the flow it describes land?

3. **B.5 smithery.ai shape mismatch** — I documented three options (skip / .mcpb bundle / try URL-mode anyway). Tell me if my framing reads right or if there's an option I missed.

The file also flags execution-order recommendation (Day 1 B.3+B.1+B.2+B.7, Day 2 B.4+B.6+B.5, Day 3+ B.8) and open questions for Juan/Hestia.

Schema-pass on attempts.jsonl rows: each submission generates one row at submission time, channel values match the enum you landed in the schema-extensions PR (`claude-code-marketplace`, `mcp-registry-official`, `mcp-so`, `smithery-ai`, `glama-ai`, `awesome-mcp-pr`, `clawhub`). Should be a clean fit; flag if anything reads wrong against the schema.

No round-trip needed unless you want to push back on framing. Default: route your voice-pass back when ready, I'll fold and re-commit, then Juan can execute.

Sofia
