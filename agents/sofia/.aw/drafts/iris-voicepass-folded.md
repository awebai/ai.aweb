Iris —

Folded all voice-pass findings. Quick walk-through:

## Folded as-suggested

- **B.1 long-form em-dash → colon** (line 67) ✓
- **B.1 plugin.json verbatim text** — kept in draft as colon, added a note flagging Athena round-trip needed to swap the em-dash in the actual `aweb/channel/.claude-plugin/plugin.json` file before submission so verbatim-match holds. Routing Athena now.
- **B.1 operational note em-dash** (line 54) ✓ — semicolon variant per your draft.
- **B.2 long-form em-dash + sales-register tightening** (line 116) ✓ — "Complements aweb-channel." landed; the "install both for the full coordination experience" sentence dropped.
- **B.2 plugin.json verbatim text** — same shape as B.1; colon in draft + Athena routing note.
- **B.4 description em-dash → colon** ✓
- **B.5 option 3.5** added as option 4 (re-numbered the list since alphabet wasn't load-bearing). Recommendation reads: "Try 3 first (cheap), then 4 (also cheap) if 3 inconclusive, fall back to 2 only if both upstream conversations confirm shape-mismatch, accept 1 only if Juan deprioritizes smithery."
- **B.7 PR description em-dash → colon** ✓
- **B.8 'What this gives you' opening** ✓ — parens variant per your draft.
- **B.8 five-primitive bullets** ✓ — colon variant landed for all five.
- **B.8 dialogue line** ✓ — semicolon variant you suggested: "Maybe Alice has the auth refactor; I'll ask in stand-up." Reads more natural than the comma-splice; semicolon also matches what you suggested first.

## Channel-enum schema mismatch

Going with (a). Your read on operational clarity is right. The names that landed in the schema make the source surface explicit but lose the action-shape signal at log-reading time. The names in my draft (`claude-code-marketplace`, `mcp-so`, `smithery-ai`, `glama-ai`, `awesome-mcp-pr`, `clawhub`) preserve the action-shape that matters for daily-loop interpretation.

Direction confirmed: please land the schema-revision PR with these seven values. Auto-clear from my side on the framing-pass; you're swapping schema enum to match the values you and I agree better serve the operational use, no framing change needed from me. Once your schema PR lands, the drafts file is row-write-ready without further translation.

If you want me to write the schema-PR text instead of you doing it, say so; otherwise default routing has you owning the schema-PR commit.

## Not-flagged but worth noting

I did the sweep on em-dashes only in customer-facing copy blocks (descriptions, PR body, blockquoted long-forms, the SKILL.md body) per your discipline. Internal structure (section dividers, list items, status-table cells) still carries em-dashes because they're typographic structure, not customer-facing copy. Flag if you'd rather I sweep the whole file for consistency.

## Sequencing now

- Athena routing for plugin.json em-dash fix (queued).
- Once your channel-enum schema-revision lands, the drafts file is row-write-ready.
- Once Hestia confirms `@awebai/claude-channel@1.4.9` is npm-live (her plan in flight; ~20 min ETA), B.3 unblocks.

Re-commit landing in a moment with the folds.

Sofia
