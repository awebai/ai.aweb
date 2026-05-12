---
name: daily-signup-export
description: Pull the previous-24h delta of sign-ups with email from prod and mail the batch to Bertha (Eugenie's agent) for outreach. Daily ops cadence per Juan's brief 2026-05-08.
---

# Daily sign-up export to Bertha

Bertha is Eugenie's personal agent (`aweb.ai/bertha`, default:aweb.ai team). Eugenie is Juan's co-founder; she does outreach to new sign-ups for product feedback. We send her a daily batch of new email-on-record sign-ups via Bertha so the outreach pipeline runs on durable artifacts, not memory.

## Authority

Authorized by Juan on 2026-05-08 (this conversation history). The export is **internal-team coordination**, not customer marketing — sign-ups gave consent at registration to product communication; Eugenie's outreach is product-feedback follow-up, not unrelated marketing.

## Cadence

- **Fire**: daily at ~07:13 UTC (≈ 09:13 CEST), via durable cron from CronCreate.
- **Window**: previous 26 hours (24h + 2h overlap to absorb cron jitter).
- **First-run / catchup pattern**: if this is the first run after a gap, manually broaden the window or send a one-off catchup before the cron resumes normal operation.
- **7-day cron expiry**: CronCreate auto-expires after 7 days. Re-create on each weekly check. If we want longer-term reliability, move to system cron / launchd as a follow-up.

## What gets exported

```sql
SELECT
    email,
    full_name,
    email_verified,
    signup_method,
    provider,
    created_at::date AS signup_date
FROM aweb_cloud.users
WHERE email IS NOT NULL AND email <> ''
  AND deleted_at IS NULL
  AND created_at >= NOW() - INTERVAL '26 hours'
ORDER BY created_at DESC
```

Format: pipe-separated table, one row per user. Columns: `email | full_name | verified | signup_method | provider | signup_date`. Bertha can parse mechanically into a draft-message skill.

## What does NOT get exported

- Soft-deleted users (`deleted_at IS NOT NULL`)
- Password hashes, IPs, internal IDs
- Provider tokens, OAuth identifiers, anything in `provider_data`
- Users without an email on file (no useful outreach target)

If Bertha asks for additional fields (e.g., signup source attribution), validate against minimum-necessary principle before adding.

## Procedure

1. **Pull batch from prod.** Read DATABASE_URL from `/Users/juanre/prj/awebai/ac/.env.production` (line starting with `DATABASE_URL=`). Run the SQL above via asyncpg.

2. **Format inline**. Capture stdout to `/tmp/signup-batch-YYYY-MM-DD.txt` for audit during the run. Header line: `# Daily batch — N new users in last 26h (since CUTOFF_TIMESTAMP)`. Empty days: send a 0-row mail anyway, header `# Daily batch — 0 new users in last 26h` (so Bertha knows the pipeline ran).

3. **Send to Bertha via aweb mail** (NOT chat — mail is durable, has subject lines, persists in her inbox):
   ```
   aw mail send --to bertha \
     --subject "Daily sign-up batch YYYY-MM-DD: N new users" \
     --body "<inline batch + brief context>"
   ```
   Body should be the catchup-mail template Bertha already received on 2026-05-08 (message_id b8eeb3d6) — same shape, just with the new batch.

4. **Delete the scratch file**: `rm /tmp/signup-batch-YYYY-MM-DD.txt`. PII hygiene; the batch lives in Bertha's mail and that's the canonical copy.

5. **Brief log line** in operations.md or handoff.md if anything unusual surfaced (DB query failure, schema change, mail send failure). Don't spam status with successful runs — only the deltas matter.

## Failure modes

- **DB unreachable**: log + retry once after 60s. If still failing, mail Bertha with a "pipeline outage" note (so she knows to expect a make-up batch) and mail Juan/Athena to investigate. Don't silently swallow.
- **Schema changed (e.g., column renamed)**: query will fail with `UndefinedColumnError`. Update the SQL in this skill; don't paper over with try/except. Athena owns server schema; mail her if the change wasn't communicated.
- **Empty batch on a day where users definitely signed up**: cutoff window may have drifted. Check `created_at` distribution for the prior 48h; widen window if needed for that run.
- **Bertha not registered**: mail send to bertha fails with "agent not found." Means her cert lapsed or her workspace is offline. Mail Juan; hold subsequent batches until she's back.

## Multi-agent activity status (added to daily mail body)

Authorized 2026-05-08 by Juan + Eugenie via Bertha (chat 4d4383fc / 2901b3a5). Daily mail to Bertha now also includes a snapshot of multi-agent activity status.

After the sign-ups batch, append a section:

```
## Multi-agent activity status

EXTERNAL_TOTAL users currently have 2+ agents AND cross-agent activity
on at least one surface (mail, chat, contacts, tasks, task_claims).
Internal accounts excluded: juan@aweb.ai, juan@juanreyero.com, eugenie@aweb.ai.

(per-user breakdown if any: email, full_name, surfaces, first_evidence_at)

ALERTED_COUNT users have already triggered milestone alerts (state file).
```

Pull the data the same way the milestone-check skill does:
```bash
DATABASE_URL=$(...) uv run --with asyncpg python ~/.claude/skills/multi-agent-milestone-check/check.py --dry-run
```
The `--dry-run` flag prevents state-file mutation during this snapshot.

The hourly milestone-check skill handles the immediate-alert case for first-crossings; this daily snapshot just gives Bertha/Eugenie/Juan a regular pulse on the population dynamics.

## Adjacent procedures (out of scope here)

- **Hourly multi-agent milestone check** (`~/.claude/skills/multi-agent-milestone-check/SKILL.md`): handles the immediate-alert case when a NEW external user first crosses the multi-agent coordination threshold.
- **Bertha's draft-message skill**: lives in Bertha's workspace, not mine. Coordinate via mail if Bertha needs schema changes here.
- **Eugenie's Gmail connection**: Bertha's lane to set up with Eugenie. We don't proxy mail.
- **Eugenie's 10-min mail-check wakeup**: Bertha's lane.

## Provenance

- Authorization: Juan, 2026-05-08 (this conversation).
- First batch sent: 2026-05-08, message_id b8eeb3d6, 20 catchup users (17 verified + 3 unverified).
- Cron created: see CronList output for the active job ID.
- This skill: created 2026-05-08 by Hestia.
