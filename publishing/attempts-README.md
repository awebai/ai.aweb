# Outreach Attempts Log

Per-attempt record of every Show HN / Reddit / Twitter / DEV / direct-mail
outreach attempt, structured for learning across attempts (not just
narrative reading). Complements `history.md` (which is the human-readable
clustered narrative) by giving us a machine-readable, sortable, filterable
record.

## Why this exists

Juan: "I have made several Show HN and Reddit posts, without any impact. I
should have been more strict in keeping track of them, so one of our tasks
is going to be recording them. I want them to be stored in our repo in a
way that we can learn from: date, utctime, content, channel, reaction."
(2026-05-26.)

The pattern this catches: posts get authored, shipped, and observed in
isolation. Without a per-attempt log, we can't:
- Sort attempts by channel and compare what landed in r/ClaudeCode vs HN
- Filter sank-vs-traction attempts and look for shared traits
- Audit our cadence (are we posting too often / not often enough)
- Build a baseline expectation (median upvotes, median comments) so we
  recognize an actual signal when it lands

## The schema

`attempts.jsonl` — one JSON object per line, append-only. Each line is a
complete record; never edited after capture except for `capture_2` and
`capture_long` (later observation passes — see below).

### Required fields (every attempt)

| Field | Type | Example | Notes |
|---|---|---|---|
| `id` | string | `2026-05-26-rclaudecode-two-agents-not-one` | YYYY-MM-DD-channelslug-titleslug; unique |
| `date_utc` | ISO 8601 string | `2026-05-26T15:23:00Z` | When the attempt was posted/sent (UTC, not local) |
| `channel` | enum | see "Canonical channel set" below | Lowercase, hyphen-separated; pick from canonical set, add new with a decision note |
| `channel_url` | string | `https://www.reddit.com/r/ClaudeCode/comments/abc123/...` | Post/thread URL |
| `submitter` | string | `juanre`, `eugenie`, `juanre+eugenie` | Who pressed send |
| `title_or_subject` | string | `"Running two Claude Code agents on the same codebase..."` | Post title or mail subject |
| `content_path` | string | `publishing/drafts/2026-05-26-rclaudecode-two-agents-pair.md` | Path to the source draft of the content; commit it before posting so the snapshot is durable |

### Canonical channel set

**Community-engagement** (post / comment / reply → reaction-in-hours feedback loop):

`hn`, `reddit-r-claudecode`, `reddit-r-cursorai`, `reddit-r-chatgptcoding`, `twitter`, `devto`, `github-discussion`, `direct-mail`, `dev-to-comment`, `hn-comment`

**Submission-surface** (submit metadata to registry → approval-in-days + ongoing-discoverability feedback loop):

`claude-code-marketplace`, `mcp-registry-official`, `mcp-so`, `smithery-ai`, `glama-ai`, `awesome-mcp-pr`, `clawhub`, `nanoclaw-channel`

The naming logic: the official MCP registry keeps the `mcp-registry-` prefix because it's the canonical one (registry.modelcontextprotocol.io); third-party registries use their bare brand names because the brand already identifies the surface. `awesome-mcp-pr` names the action-shape (PR submission against the awesome-list) rather than the surface, because the action-shape is what matters for daily-loop log-reading.

Pi listings (pi.dev/packages/@awebai/pi) are automatic via the `pi-package` npm keyword and are not attempts to log. Pi promotion goes through community-engagement channels (DEV.to article, GitHub Show & Tell, etc.).

### Result variant selection

Each row uses one of two result variants depending on the channel: community-engagement channels use `result_24h` (and optional `result_7d` / `result_30d`); submission-surface channels use `result_submission` (and optional `result_7d` / `result_30d` with the submission-shape fields).

### Result fields — community-engagement variant (initial capture — 24h after post)

For channels like `hn`, `reddit-*`, `twitter`, `devto`, `direct-mail`, etc. The feedback shape is post → reaction-in-hours.

| Field | Type | Example | Notes |
|---|---|---|---|
| `result_24h.outcome` | enum | `sank`, `traction`, `sticky`, `hostile`, `silence`, `pending` | One word read; explain in `notes` if mixed |
| `result_24h.upvotes` | integer | `12` | Whatever the channel calls them; null if N/A |
| `result_24h.comments` | integer | `3` | Threaded comments; null if N/A |
| `result_24h.front_page_or_top` | boolean | `false` | Did it reach a high-visibility surface (HN front, Reddit hot, Twitter trending)? |
| `result_24h.ref_traffic_observed` | boolean | `true` | Did Plausible/analytics show a referral spike attributable to this post? |
| `result_24h.captured_at_utc` | ISO 8601 | `2026-05-27T15:23:00Z` | When the result row was recorded |

### Result fields — submission-surface variant (initial capture — at submit + later check passes)

For channels like `claude-code-marketplace`, `mcp-registry-official`, `mcp-so`, `smithery-ai`, `glama-ai`, `awesome-mcp-pr`, `clawhub`, `nanoclaw-channel`. The feedback shape is submit → approval-in-days → ongoing-discoverability.

| Field | Type | Example | Notes |
|---|---|---|---|
| `result_submission.status` | enum | `submitted`, `under-review`, `approved`, `rejected`, `withdrawn`, `silence`, `pending` | Submission lifecycle state; `silence` if no signal returned and we're past the surface's typical response window |
| `result_submission.listing_url` | string | `https://mcp.so/server/aweb` | Where the listing landed; null if rejected or pending |
| `result_submission.discoverability` | enum | `top-of-search`, `paginated`, `search-only`, `hidden` | Capture-time judgment, not a metric the surface reports. Explain in `notes` when it's borderline (e.g., visible-but-buried-on-page-3) |
| `result_submission.ref_traffic_observed` | boolean | `true` | Did Plausible/analytics show a referral spike attributable to this listing? |
| `result_submission.captured_at_utc` | ISO 8601 | `2026-05-30T15:23:00Z` | When the result row was recorded |

### Optional fields

| Field | Notes |
|---|---|
| `result_7d`, `result_30d` | Same shape as `result_24h` (community-engagement) or `result_submission` (submission-surface) — match the variant used for the initial capture. Capture at 7d/30d if signal is non-zero or if the submission status is still in motion |
| `notes` | Free-form. What you noticed, what surprised you, any context that the metrics miss |
| `cross_links` | Array of other attempt IDs this links to (e.g., a Twitter tweet that referenced this Reddit post) |
| `attribution_caveats` | Free-form. Concurrent factors that could explain any uptick |
| `learnings` | Free-form. After the dust settles. What you'd do differently next time |

## Example entries

### Community-engagement (HN)

```json
{"id":"2026-05-07-hn-aweb-launch","date_utc":"2026-05-07T15:00:00Z","channel":"hn","channel_url":"https://news.ycombinator.com/item?id=XXXX","submitter":"juanre","title_or_subject":"Show HN: aweb — coordination layer for AI coding agents","content_path":"publishing/drafts/2026-05-07-show-hn-attempt.md","result_24h":{"outcome":"sank","upvotes":3,"comments":0,"front_page_or_top":false,"ref_traffic_observed":false,"captured_at_utc":"2026-05-08T15:00:00Z"},"notes":"Pre-fold framing. Submitted Tue 8am PT. Three upvotes in first hour then dropped off. No comments at all.","learnings":"HN doesn't surface a sinking submission; once it falls off the new page the recovery is essentially zero."}
```

### Submission-surface (MCP registry)

```json
{"id":"2026-05-27-mcp-so-aweb-channel","date_utc":"2026-05-27T15:00:00Z","channel":"mcp-so","channel_url":"https://mcp.so/submit/aweb-channel","submitter":"sofia","title_or_subject":"aweb-channel: agent coordination over signed messaging","content_path":"co.aweb/outreach/submissions/mcp-so-aweb-channel.md","result_submission":{"status":"submitted","listing_url":null,"discoverability":null,"ref_traffic_observed":false,"captured_at_utc":"2026-05-27T15:00:00Z"},"notes":"Initial submit. Approval window per mcp.so is typically 3-5 days; check back at 7d."}
```

## How to append a row

Use `jq -c` to flatten or just write the line by hand carefully:

```bash
cat >> publishing/attempts.jsonl <<'EOF'
{"id":"2026-05-26-...","date_utc":"...","channel":"...","channel_url":"...","submitter":"...","title_or_subject":"...","content_path":"...","result_24h":{"outcome":"pending","captured_at_utc":null}}
EOF
```

Initial row should have either `result_24h.outcome: "pending"` (community-engagement) or `result_submission.status: "submitted"` (submission-surface). Update later by finding the row, editing in place, and committing the change. Don't duplicate-append — the `id` is the unique key.

For the captured-later passes (`result_7d`, `result_30d`), edit the
existing line to add those keys. Each edit is a commit so git history
preserves the timeline.

## What goes in here vs. `history.md`

- **`attempts.jsonl`**: per-attempt structured row. Source of truth for
  the data. Cold storage; you don't read it line by line, you query it.
- **`history.md`**: human-readable clustered narrative. "Here's the May
  2026 multi-channel pivot, here's what we tried, here's what we learned."
  Reads top-down. Cites `attempts.jsonl` IDs as the underlying records.

When you're inside a cluster (a week's work, a single push), append to
`attempts.jsonl` as you go. When the cluster closes, write a `history.md`
entry that narrates the cluster and cites the underlying attempt IDs.

## What's missing right now

Past attempts (the ones Juan flagged as poorly tracked) need to be
backfilled from memory and any archive links he has. See
`past-attempts-template.md` for the shape — Juan dumps what he remembers,
Iris and Sofia turn each into a row.

## Coordination

- **Iris** owns the daily loop integration: every Eugenie/Juan post
  produces a row, and every `result_24h` capture pass updates rows.
- **Sofia** owns the schema (this file) and direction calls on
  what-belongs-where. Substantive schema additions go through framing-
  pass.
- **Bertha + Eugenie** are the human-send-side per the operating model;
  the row gets written by whichever agent (Iris in daily loop, Sofia ad
  hoc) is closest to the action.

## Banked discipline this surface protects

> "When a post sinks, the cost isn't just the zero impact — it's that we
> can't tell whether *all* posts of that shape sink, or if this one had
> something specific wrong. Without a structured log, every attempt is
> evaluated in isolation. With one, the pattern becomes legible."

This is the "verify ship state before treating handoff entry as current"
discipline rotated 90 degrees: there it was about preventing stale
predictions; here it's about producing the data we need to learn at all.
