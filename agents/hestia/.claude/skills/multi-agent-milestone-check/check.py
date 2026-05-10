"""
Multi-agent milestone check.

Detects external customers (excluding our internal accounts) who have crossed
the "multi-agent coordination" threshold for the FIRST time. Surfaces a
candidate-milestone signal that Hestia mails to Bertha (Eugenie's agent).

Run hourly via Hestia's session cron. State file tracks already-alerted
users so each user only triggers an alert once.

Usage:
    DATABASE_URL=... uv run --with asyncpg python check.py [--dry-run]

Output to stdout:
    JSON with keys: candidates (list of new alert candidates), alerted_state
    (current state-file contents), check_timestamp.

Exit code 0 always (failures logged to stderr; cron handles).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import asyncpg

INTERNAL_EMAILS = ("juan@aweb.ai", "juan@juanreyero.com", "eugenie@aweb.ai")
STATE_FILE = Path("/Users/juanre/prj/awebai/ai.aweb/agents/hestia/.claude/state/multi-agent-alerted-users.json")


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {"users_alerted": [], "last_check": None}
    return json.loads(STATE_FILE.read_text())


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, default=str))


async def find_external_multi_agent_users(conn: asyncpg.Connection) -> list[dict]:
    """Find external users with cross-agent activity on any surface.

    Surfaces checked: mail, chat, contacts, tasks, task_claims.
    Returns a list of {user_id, email, full_name, surfaces, first_evidence_at}.
    """
    sql = """
    WITH external_user_agents AS (
        SELECT u.id AS user_id, u.email, u.full_name,
               cwm.aweb_agent_id, a.did, a.did_aw, a.did_key,
               a.alias, a.address, a.team_id
        FROM aweb_cloud.users u
        JOIN aweb_cloud.cloud_workspace_metadata cwm ON cwm.owner_user_id = u.id
        JOIN aweb.agents a ON a.agent_id = cwm.aweb_agent_id
        WHERE u.deleted_at IS NULL
          AND a.deleted_at IS NULL
          AND u.email NOT IN ('juan@aweb.ai', 'juan@juanreyero.com', 'eugenie@aweb.ai')
    ),
    mail_evidence AS (
        SELECT eu1.user_id, eu1.email, eu1.full_name,
               'mail' AS surface, MIN(m.created_at) AS first_evidence_at
        FROM aweb.messages m
        JOIN external_user_agents eu1 ON eu1.did = m.from_did OR eu1.did_aw = m.from_did
        JOIN external_user_agents eu2 ON (eu2.did = m.to_did OR eu2.did_aw = m.to_did)
                                       AND eu2.user_id = eu1.user_id
                                       AND eu2.aweb_agent_id <> eu1.aweb_agent_id
        GROUP BY eu1.user_id, eu1.email, eu1.full_name
    ),
    chat_evidence AS (
        SELECT eua.user_id, eua.email, eua.full_name,
               'chat' AS surface, MIN(s.created_at) AS first_evidence_at
        FROM aweb.chat_sessions s
        JOIN aweb.chat_participants cp ON cp.session_id = s.session_id
        JOIN external_user_agents eua ON eua.did = cp.did OR eua.did_aw = cp.did
        GROUP BY s.session_id, eua.user_id, eua.email, eua.full_name
        HAVING COUNT(DISTINCT eua.aweb_agent_id) >= 2
    ),
    contact_evidence AS (
        SELECT eu1.user_id, eu1.email, eu1.full_name,
               'contact' AS surface, MIN(c.created_at) AS first_evidence_at
        FROM aweb.contacts c
        JOIN external_user_agents eu1 ON eu1.did = c.owner_did OR eu1.did_aw = c.owner_did
        JOIN external_user_agents eu2 ON eu2.address = c.contact_address
                                       AND eu2.user_id = eu1.user_id
                                       AND eu2.aweb_agent_id <> eu1.aweb_agent_id
        GROUP BY eu1.user_id, eu1.email, eu1.full_name
    ),
    task_evidence AS (
        SELECT eu1.user_id, eu1.email, eu1.full_name,
               'task' AS surface, MIN(t.created_at) AS first_evidence_at
        FROM aweb.tasks t
        JOIN external_user_agents eu1 ON eu1.alias = t.created_by_alias
                                       AND eu1.team_id = t.team_id
        JOIN external_user_agents eu2 ON eu2.alias = t.assignee_alias
                                       AND eu2.team_id = t.team_id
                                       AND eu2.user_id = eu1.user_id
                                       AND eu2.aweb_agent_id <> eu1.aweb_agent_id
        WHERE t.assignee_alias IS NOT NULL AND t.assignee_alias <> ''
          AND t.deleted_at IS NULL
        GROUP BY eu1.user_id, eu1.email, eu1.full_name
    ),
    task_claim_evidence AS (
        SELECT eu1.user_id, eu1.email, eu1.full_name,
               'task_claim' AS surface, MIN(tc.claimed_at) AS first_evidence_at
        FROM aweb.task_claims tc
        JOIN aweb.tasks t ON t.team_id = tc.team_id AND t.task_ref_suffix = split_part(tc.task_ref, '-', -1)
        JOIN external_user_agents eu1 ON eu1.alias = t.created_by_alias
                                       AND eu1.team_id = t.team_id
        JOIN external_user_agents eu2 ON eu2.alias = tc.alias
                                       AND eu2.team_id = tc.team_id
                                       AND eu2.user_id = eu1.user_id
                                       AND eu2.aweb_agent_id <> eu1.aweb_agent_id
        GROUP BY eu1.user_id, eu1.email, eu1.full_name
    ),
    all_evidence AS (
        SELECT * FROM mail_evidence
        UNION ALL SELECT * FROM chat_evidence
        UNION ALL SELECT * FROM contact_evidence
        UNION ALL SELECT * FROM task_evidence
        UNION ALL SELECT * FROM task_claim_evidence
    )
    SELECT
        user_id::text AS user_id,
        email,
        full_name,
        array_agg(DISTINCT surface ORDER BY surface) AS surfaces,
        MIN(first_evidence_at) AS first_evidence_at
    FROM all_evidence
    GROUP BY user_id, email, full_name
    ORDER BY first_evidence_at
    """
    rows = await conn.fetch(sql)
    return [dict(r) for r in rows]


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="don't update state file; just report")
    args = parser.parse_args()

    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print(json.dumps({"error": "DATABASE_URL not set"}), file=sys.stderr)
        sys.exit(0)

    conn = await asyncpg.connect(db_url)
    try:
        users = await find_external_multi_agent_users(conn)
    finally:
        await conn.close()

    state = load_state()
    already_alerted = set(state.get("users_alerted", []))

    candidates = []
    for u in users:
        if u["user_id"] not in already_alerted:
            candidates.append(u)

    output = {
        "check_timestamp": datetime.now(timezone.utc).isoformat(),
        "external_multi_agent_users_total": len(users),
        "already_alerted_count": len(already_alerted),
        "new_candidates": candidates,
        "all_external_users_with_activity": users,
    }
    print(json.dumps(output, default=str, indent=2))

    if not args.dry_run and candidates:
        new_alerted = sorted(already_alerted | {c["user_id"] for c in candidates})
        save_state({
            "users_alerted": new_alerted,
            "last_check": output["check_timestamp"],
            "last_candidate_count": len(candidates),
        })
    elif not args.dry_run:
        # update last_check timestamp even if no candidates
        save_state({
            "users_alerted": sorted(already_alerted),
            "last_check": output["check_timestamp"],
            "last_candidate_count": 0,
        })


if __name__ == "__main__":
    asyncio.run(main())
