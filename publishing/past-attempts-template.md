# Past attempts — backfill template

Juan: dump everything you remember about past Show HN / Reddit / Twitter
posts here, even if details are partial. Iris and Sofia will turn each
into an `attempts.jsonl` row.

Per attempt, fill in what you remember. Anything unknown — leave blank.
Better partial than nothing.

---

## Attempt 1

- **Approximate date** (UTC if you remember the time):
- **Channel** (HN, r/ClaudeCode, r/CursorAI, Twitter, dev.to, etc.):
- **Title** (or subject if mail):
- **Brief content shape** (what was the pitch — protocol layer? coordination? multi-agent?):
- **Where the post URL was** (if you can find it now):
- **What you remember about the reaction** (upvotes count if rough, any comments, did it sink fast, did anyone reply):
- **What you remember about timing** (Tue-Thu morning PT? Or some other slot?):
- **Was it submitted by you or someone else**:
- **Any guess at why it landed the way it did**:

---

## Attempt 2

(repeat shape)

---

## Attempt 3

(repeat shape)

---

(Add as many sections as you need. No upper limit — better to have 15
partial entries than 3 complete ones.)

---

## What to do with this once filled

1. Juan writes what he remembers above.
2. Iris (or Sofia) reads each entry and tries to recover any missing
   data: actual post URL if findable on HN search / Reddit search, exact
   timestamp from the post if URL recovered, the content from
   `publishing/drafts/` if a draft was committed.
3. Each entry becomes one row in `publishing/attempts.jsonl` with the
   data we can verify, and a `notes:` field explaining what's
   reconstructed-from-memory vs. recovered-from-source.
4. This template file gets archived (move to
   `publishing/archive/past-attempts-backfill-YYYY-MM-DD.md`) once the
   backfill is complete.

---

## Notes from Sofia on the backfill

Don't worry about completeness. The point of the backfill isn't to
recover perfect data on every old attempt — it's to:
1. Capture the count (so we know HOW many attempts have happened)
2. Capture the channel mix (HN-heavy? Reddit-heavy? Mixed?)
3. Capture the rough outcome shape (mostly sink? Some traction?)
4. Anchor going-forward attempts in a baseline so we recognize signal
   when it comes.

Even an entry like "approximate date: late April 2026, channel: HN,
content: about aweb, sank, no comments" is useful data. It tells us at
minimum the channel was tried, the rough timing, and the outcome shape.
The structured log starts being valuable at ~5-10 entries, gets sharper
at 20+.
