"""Behavioral snapshot for one or more users — for Bertha pre-outreach context.

Usage:
  uv run --with asyncpg python scripts/user_activity.py --email thanos@example.com
  uv run --with asyncpg python scripts/user_activity.py --email a@x.com --email b@y.com
  uv run --with asyncpg python scripts/user_activity.py --user-id <uuid>

Answers question shapes:
  - "is user X active since signing up?"
  - "agents created, messages sent, tasks, last active?"
  - "should we reach out to them or have they already churned?"

Per user, prints:
  - identity (signup method, account age)
  - teams owned (directly or via org)
  - agents under those teams (active + deleted)
  - workspaces with last_seen_at + idle days
  - mail/chat/task counts (all-time)
  - most-recent-activity timestamp + idle days
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import asyncpg

from _db import resolve_database_url


async def probe_one(conn, *, email: str | None, user_id: str | None):
    if email:
        user = await conn.fetchrow(
            """SELECT id, email, full_name, email_verified, signup_method, provider,
                      created_at, deleted_at
               FROM aweb_cloud.users WHERE email = $1""",
            email,
        )
        label = email
    else:
        user = await conn.fetchrow(
            """SELECT id, email, full_name, email_verified, signup_method, provider,
                      created_at, deleted_at
               FROM aweb_cloud.users WHERE id = $1::uuid""",
            user_id,
        )
        label = user_id

    print(f"\n========== {label} ==========")
    if not user:
        print("  USER NOT FOUND")
        return

    print(f"  user_id        : {user['id']}")
    print(f"  email          : {user['email']!r}  verified={user['email_verified']}")
    print(f"  full_name      : {user['full_name']!r}")
    print(f"  signup_method  : {user['signup_method']}  provider={user['provider']}")
    print(f"  signed up at   : {user['created_at']}")
    age = await conn.fetchval(
        "SELECT EXTRACT(EPOCH FROM (NOW() - $1::timestamptz))::int", user["created_at"]
    )
    print(f"  account age    : {age/86400:.1f} days")

    teams = await conn.fetch(
        """WITH t AS (
              SELECT t.id, t.slug, t.name, t.owner_type, t.aweb_team_id, t.deleted_at
              FROM server.teams t WHERE t.owner_user_id = $1
              UNION
              SELECT t.id, t.slug, t.name, t.owner_type, t.aweb_team_id, t.deleted_at
              FROM server.teams t
              JOIN aweb_cloud.organization_members om ON om.organization_id = t.owner_org_id
              WHERE om.user_id = $1
           )
           SELECT id, slug, name, owner_type, aweb_team_id FROM t WHERE deleted_at IS NULL""",
        user["id"],
    )
    print(f"\n  teams ({len(teams)}):")
    aweb_team_ids = []
    for t in teams:
        print(
            f"    - slug={t['slug']} aweb_team_id={t['aweb_team_id']} "
            f"owner_type={t['owner_type']}"
        )
        if t["aweb_team_id"]:
            aweb_team_ids.append(t["aweb_team_id"])

    if not aweb_team_ids:
        print("  (no teams)")
        return

    agents = await conn.fetch(
        """SELECT agent_id, alias, address, created_at, deleted_at
           FROM aweb.agents WHERE team_id = ANY($1::text[]) ORDER BY created_at""",
        aweb_team_ids,
    )
    active_ids = [a["agent_id"] for a in agents if a["deleted_at"] is None]
    print(f"\n  agents: {len(agents)} total, {len(active_ids)} active")
    for a in agents:
        mark = f" DELETED={a['deleted_at']:%Y-%m-%d %H:%M}" if a["deleted_at"] else ""
        print(f"    - alias={a['alias']!r:25s} created={a['created_at']:%Y-%m-%d %H:%M}{mark}")

    if not active_ids:
        return

    ws = await conn.fetch(
        """SELECT alias, hostname, last_seen_at, deleted_at
           FROM aweb.workspaces WHERE agent_id = ANY($1::uuid[]) ORDER BY created_at""",
        active_ids,
    )
    last_max = None
    print(f"\n  workspaces ({len(ws)}):")
    for w in ws:
        ls = f"{w['last_seen_at']:%Y-%m-%d %H:%M}" if w["last_seen_at"] else "never"
        if w["last_seen_at"] and (last_max is None or w["last_seen_at"] > last_max):
            last_max = w["last_seen_at"]
        host = w["hostname"] or "(no host)"
        mark = " DELETED" if w["deleted_at"] else ""
        print(f"    - alias={w['alias']!r:25s} host={host:20s} last_seen={ls}{mark}")

    if last_max:
        idle = await conn.fetchval(
            "SELECT EXTRACT(EPOCH FROM (NOW() - $1::timestamptz))::int", last_max
        )
        print(f"\n  last workspace heartbeat: {last_max} (idle ~{idle/86400:.1f} days)")
    else:
        print(f"\n  no workspace has heartbeated since registration")

    mail_total = await conn.fetchval(
        """SELECT COUNT(*) FROM aweb.messages
           WHERE from_agent_id = ANY($1::uuid[]) OR to_agent_id = ANY($1::uuid[])""",
        active_ids,
    )
    mail_sent = await conn.fetchval(
        """SELECT COUNT(*) FROM aweb.messages WHERE from_agent_id = ANY($1::uuid[])""",
        active_ids,
    )
    chat_sent = await conn.fetchval(
        """SELECT COUNT(*) FROM aweb.chat_messages WHERE from_agent_id = ANY($1::uuid[])""",
        active_ids,
    )
    tasks = await conn.fetchval(
        """SELECT COUNT(*) FROM aweb.tasks WHERE team_id = ANY($1::text[])""",
        aweb_team_ids,
    )
    print(f"\n  all-time: {mail_total} mail (touched), {mail_sent} mail sent, "
          f"{chat_sent} chat sent, {tasks} tasks")

    latest = await conn.fetchval(
        """SELECT MAX(t) FROM (
             SELECT MAX(created_at) AS t FROM aweb.messages
               WHERE from_agent_id = ANY($1::uuid[]) OR to_agent_id = ANY($1::uuid[])
             UNION ALL
             SELECT MAX(created_at) AS t FROM aweb.chat_messages WHERE from_agent_id = ANY($1::uuid[])
             UNION ALL
             SELECT MAX(created_at) AS t FROM aweb.tasks WHERE team_id = ANY($2::text[])
             UNION ALL
             SELECT MAX(last_seen_at) AS t FROM aweb.workspaces WHERE agent_id = ANY($1::uuid[])
           ) s""",
        active_ids, aweb_team_ids,
    )
    if latest:
        idle = await conn.fetchval(
            "SELECT EXTRACT(EPOCH FROM (NOW() - $1::timestamptz))::int", latest
        )
        print(f"  ===> most recent activity anywhere: {latest} (idle ~{idle/86400:.1f} days)")
    else:
        print(f"  ===> no activity on any surface since signup")


async def main(emails: list[str], user_ids: list[str]):
    if not emails and not user_ids:
        raise SystemExit("ERROR: provide at least one --email or --user-id")
    db_url = resolve_database_url()
    conn = await asyncpg.connect(db_url)
    try:
        for e in emails:
            await probe_one(conn, email=e, user_id=None)
        for u in user_ids:
            await probe_one(conn, email=None, user_id=u)
    finally:
        await conn.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="User behavioral snapshot")
    p.add_argument("--email", action="append", default=[], help="User email (repeatable)")
    p.add_argument("--user-id", action="append", default=[], help="User UUID (repeatable)")
    args = p.parse_args()
    asyncio.run(main(args.email, args.user_id))
