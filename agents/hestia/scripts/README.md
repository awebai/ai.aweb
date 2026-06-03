# Hestia analytics & probe scripts

Reusable read-only DB scripts for recurring questions from Bertha, Juan, and triage flows.
Each script is self-contained: argparse + asyncpg, run via `uv run --with asyncpg`.

## Invocation

From `agents/hestia/`:

```
uv run --with asyncpg python scripts/<name>.py [args]
```

DATABASE_URL is resolved from `$DATABASE_URL` first, then from `../../../ac/.env.production`
(the `ac` symlink under this dir). Override with `AC_ENV_FILE=/path/to/.env`.

## Scripts

| Script | Answers | Triggered by |
|---|---|---|
| `signups.py --days N` | "how many sign-ups in last N days? CLI vs browser? who?" | Bertha outreach, Juan funnel reads |
| `user_activity.py --email <e>` | "is user X active? agents/messages/last-seen?" | Bertha pre-outreach context, support triage |
| `multi_agent_active.py --days N` | "is anyone actually using aweb multi-agent? who?" | Juan product reads, Metis signal |
| `team_probe.py --team <aweb_team_id>` | "what's the state of team X? agents/workspaces/messages/deletes" | "agent not connected" triage, BYOT audit |

## PII discipline

These probes touch user emails, names, message metadata, and DID controller keys.

- Output is internal-team only. Do not paste raw output to external surfaces.
- Bertha is internal team coordination — emails + names in mail to her are by-design for outreach (per the daily-signup-export skill authorization).
- Sofia / Athena / Aida / Iris / Metis can receive these outputs for analytics, triage, or framing review.
- Do not include emails or controller keys in artifacts checked into the public ai.aweb repo.
- Delete tmp files / pre-PII dumps after use; banked discipline from the awid cleanup artifact pattern.

## Schema notes for future query-writers

- `aweb_cloud.users` is the user table. `signup_method='cli_signup'` users have `email=NULL`.
- `aweb_cloud.organization_members` links users to orgs; org-owned teams come via `server.teams.owner_org_id`.
- `server.teams.aweb_team_id` is TEXT (e.g. `default:pmbah.aweb.ai`), not UUID. The OSS-side `aweb.agents.team_id` matches that string.
- `aweb.messages` has NO `deleted_at` column — mail is never soft-deletable.
- `aweb.chat_messages`, `aweb.chat_sessions`, `aweb.chat_participants` also have no `deleted_at` — chat data can be hard-deleted by cascade but not soft-deleted.
- `aweb.workspaces.last_seen_at` is the heartbeat proxy. NULL means never heartbeated since registration.
- `aweb_cloud.cloud_agent_certificates` is keyed by `workspace_id` (not `agent_id`).
- `aweb.audit_log` is filtered by `team_id` (TEXT) + `event_type`. Cleanup-path DELETEs may not be event-typed; widen if a search returns 0 rows.

## Adding a new script

When a question shape repeats more than twice:
1. Add a script under `scripts/` using the same pattern (argparse + `from _db import resolve_database_url`).
2. Update the table in this README.
3. Update the "Analytics & probe scripts" section in `AGENTS.md` so future Hestia instances find it on wake-up.
4. Smoke-test against prod (read-only) before banking.

Don't write one-off `/tmp/probe.py` files for recurring shapes. Banked from Juan: "we really need to have pre-made scripts for the questions that you get from bertha and from me, and they should be a clear part of your agents.md" (2026-06-02).
