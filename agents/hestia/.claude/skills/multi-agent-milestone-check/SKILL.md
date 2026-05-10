---
name: multi-agent-milestone-check
description: Hourly check for external customers crossing the multi-agent coordination milestone (any of mail, chat, contacts, tasks, task_claims between 2+ same-user agents). Mails Bertha when a NEW external user crosses for the first time. State-tracked so each user only triggers alert once.
---

# Multi-agent milestone alert

Eugenie + Juan want to know **immediately** when an external customer first has 2+ agents communicating or coordinating. That's a significant product milestone for aweb. Bertha relays this to Eugenie/Juan via her Gmail connection.

## Authority

Authorized by Juan + Eugenie via Bertha on 2026-05-08 (chat session 4d4383fc, message 2901b3a5). "Anything counts" — mail, chat, tasks, locks, contacts. Internal exclusions: just `juan@aweb.ai`, `juan@juanreyero.com`, `eugenie@aweb.ai`. Cadence: hourly.

## Cadence

- **Fire**: hourly at minute :07 (off-peak), via cron from CronCreate.
- **Window**: full-history on each run. The state file dedupes — each user only triggers an alert once (the first time they cross). State persists in `.claude/state/multi-agent-alerted-users.json`.
- **Cron 7-day expiry**: same constraint as `daily-signup-export`. Re-create on weekly check.
- **Session-only durability**: cron only fires while this Claude session is alive. Real production reliability needs system cron / launchd. Flagged as ops debt.

## Predicate (what counts as "coordinating")

Any of the following between 2+ same-user agents (excluding internal accounts):

1. **Mail** — `aweb.messages` row with from/to between the user's agents.
2. **Chat** — `aweb.chat_sessions` with 2+ same-user `chat_participants`.
3. **Contacts** — `aweb.contacts` row where owner_did is one user-agent and contact_address is another's address.
4. **Tasks** — `aweb.tasks` with different `created_by_alias` and `assignee_alias`, both same user via team match.
5. **Task claims** — `aweb.task_claims` row claiming a task whose creator is a different same-user agent.

All five are checked in `check.py`. Add new surfaces by extending the SQL CTEs.

## Procedure

1. **Run the check**:
   ```
   DATABASE_URL=$(grep '^DATABASE_URL=' /Users/juanre/prj/awebai/ac/.env.production | cut -d= -f2-) \
   uv run --with asyncpg python ~/.claude/skills/multi-agent-milestone-check/check.py
   ```

2. **Parse output**. JSON with:
   - `external_multi_agent_users_total` — current count of external users with multi-agent activity
   - `already_alerted_count` — already in state file
   - `new_candidates` — users to alert this run (list of dicts with user_id, email, full_name, surfaces, first_evidence_at)
   - `all_external_users_with_activity` — full snapshot

3. **If `new_candidates` is non-empty**:
   - Mail Bertha with subject "🚀 Multi-agent milestone — N new external user(s) crossed".
   - Body: per-user breakdown (email, full_name, which surfaces they crossed on, first-evidence timestamp). Encourage Bertha to relay quickly to Eugenie + Juan via Gmail.
   - The script has already updated state file to mark these users as alerted (unless `--dry-run`).

4. **If `new_candidates` is empty**: do nothing (no spam). State file's `last_check` is updated regardless so we know the pipeline ran.

5. **On error** (DB unreachable, SQL fails): log to stderr, exit 0 anyway (don't crash cron). Mail Juan + Athena with "milestone-check pipeline outage" if it persists across multiple runs.

## State file

Path: `/Users/juanre/prj/awebai/ai.aweb/agents/hestia/.claude/state/multi-agent-alerted-users.json`

Format:
```json
{
  "users_alerted": ["uuid1", "uuid2", ...],
  "last_check": "2026-05-08T16:07:00+00:00",
  "last_candidate_count": 0
}
```

If the file goes missing, the next run will treat ALL current external users with activity as "new" — meaning a flood of alerts on first run after restoration. To avoid that, on initial deployment, populate `users_alerted` with empty list (no users have been alerted yet) AND immediately run the check; any current external users with activity will then be flagged as the "first batch" of milestones, which IS the right behavior — they just hadn't been alerted before because the system didn't exist.

As of 2026-05-08 deployment: zero external users with multi-agent activity. State file initialized empty. The first to cross will be the first milestone alert.

## What does NOT count

- **Internal accounts**: hardcoded exclusion list (3 emails). If you add accounts that should be internal-not-external, update `INTERNAL_EMAILS` in `check.py`.
- **Single-agent activity**: a user with 1 agent doesn't qualify. `external_user_agents` requires the join to find 2+ agents anyway.
- **Cross-team messaging within same user**: same-user agents on different teams still count (mail/chat surfaces match on did, not team).

## Adjacent procedures

- **Daily sign-up export** (`~/.claude/skills/daily-signup-export/SKILL.md`): includes a "multi-agent activity status" section as part of the daily mail. The hourly check here handles the immediate-alert case for first-crossings.
- **Bertha's Gmail relay**: out of scope; she sets that up with Eugenie. We mail to her via aweb mail and she forwards.

## Provenance

- Authorization: Juan + Eugenie via Bertha, 2026-05-08 (chat 4d4383fc / 2901b3a5).
- Initial empirical state: 0 external users with multi-agent activity at deployment time. Tahim Pranta has 25 agents but no inter-agent messages (interesting datapoint, not yet a milestone).
- Cron created: see CronList output for the active job ID.
- This skill: created 2026-05-08 by Hestia.
