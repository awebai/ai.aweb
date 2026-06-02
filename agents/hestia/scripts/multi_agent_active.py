"""N-day multi-agent activity check: who has 2+ agents AND cross-agent messaging.

Usage:
  uv run --with asyncpg python scripts/multi_agent_active.py            # default 7d external
  uv run --with asyncpg python scripts/multi_agent_active.py --days 30
  uv run --with asyncpg python scripts/multi_agent_active.py --include-internal

Answers question shapes:
  - "is anyone actually using aweb (multi-agent coordination)?"
  - "who has more than one agent AND has them communicating in the past N days?"

External = excludes juan@aweb.ai, juan@juanreyero.com, eugenie@aweb.ai by default.
Activity surface = mail or chat in the last N days.

CAVEAT: due to the cli_signup linkage gap (task default-aaaj), each `aw` CLI
bootstrap creates a separate anonymous user_id. The 'external user count' is
'distinct aweb_cloud.users rows with 2+ agents', not 'distinct humans'. The
same human can show as multiple external rows. Note this when reporting the
number.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import asyncpg

from _db import resolve_database_url, INTERNAL_EMAILS


async def main(days: int, include_internal: bool):
    db_url = resolve_database_url()
    conn = await asyncpg.connect(db_url)
    try:
        rows = await conn.fetch(
            """WITH user_teams AS (
                  SELECT u.id AS user_id, u.email, u.full_name, u.signup_method, t.aweb_team_id
                  FROM aweb_cloud.users u
                  JOIN server.teams t ON t.owner_user_id = u.id
                  WHERE u.deleted_at IS NULL AND t.deleted_at IS NULL
                    AND t.aweb_team_id IS NOT NULL
                  UNION
                  SELECT u.id AS user_id, u.email, u.full_name, u.signup_method, t.aweb_team_id
                  FROM aweb_cloud.users u
                  JOIN aweb_cloud.organization_members om ON om.user_id = u.id
                  JOIN server.teams t ON t.owner_org_id = om.organization_id
                  WHERE u.deleted_at IS NULL AND t.deleted_at IS NULL
                    AND t.aweb_team_id IS NOT NULL
               )
               SELECT ut.user_id, ut.email, ut.full_name, ut.signup_method,
                      a.agent_id, a.alias, a.team_id
               FROM user_teams ut
               JOIN aweb.agents a ON a.team_id = ut.aweb_team_id
               WHERE a.deleted_at IS NULL
               ORDER BY ut.user_id, a.created_at"""
        )

        user_agents = defaultdict(list)
        user_meta = {}
        for r in rows:
            user_agents[r["user_id"]].append(
                {"agent_id": r["agent_id"], "alias": r["alias"], "team_id": r["team_id"]}
            )
            user_meta[r["user_id"]] = {
                "email": r["email"],
                "full_name": r["full_name"],
                "signup_method": r["signup_method"],
            }

        multi = {u: ag for u, ag in user_agents.items() if len(ag) >= 2}

        external = {}
        internal = {}
        for u, ag in multi.items():
            email = (user_meta[u]["email"] or "").lower()
            if email in INTERNAL_EMAILS:
                internal[u] = ag
            else:
                external[u] = ag

        print(f"=== users with 2+ active agents ===")
        print(f"  total: {len(multi)} (external: {len(external)}, internal: {len(internal)})")

        print(f"\n=== EXTERNAL users with 2+ agents — {days}-day cross-agent activity ===")
        any_active = []
        for uid, agents in external.items():
            agent_ids = [a["agent_id"] for a in agents]
            mail = await conn.fetchval(
                f"""SELECT COUNT(*) FROM aweb.messages
                   WHERE (from_agent_id = ANY($1::uuid[]) OR to_agent_id = ANY($1::uuid[]))
                     AND created_at >= NOW() - INTERVAL '{days} days'""",
                agent_ids,
            )
            intra = await conn.fetchval(
                f"""SELECT COUNT(*) FROM aweb.messages
                   WHERE from_agent_id = ANY($1::uuid[])
                     AND to_agent_id = ANY($1::uuid[])
                     AND created_at >= NOW() - INTERVAL '{days} days'""",
                agent_ids,
            )
            chat = await conn.fetchval(
                f"""SELECT COUNT(*) FROM aweb.chat_messages
                   WHERE from_agent_id = ANY($1::uuid[])
                     AND created_at >= NOW() - INTERVAL '{days} days'""",
                agent_ids,
            )
            first = await conn.fetchval(
                f"""SELECT MIN(t) FROM (
                       SELECT MIN(created_at) AS t FROM aweb.messages
                         WHERE (from_agent_id = ANY($1::uuid[]) OR to_agent_id = ANY($1::uuid[]))
                           AND created_at >= NOW() - INTERVAL '{days} days'
                       UNION ALL
                       SELECT MIN(created_at) AS t FROM aweb.chat_messages
                         WHERE from_agent_id = ANY($1::uuid[])
                           AND created_at >= NOW() - INTERVAL '{days} days'
                   ) s""",
                agent_ids,
            )
            if mail > 0 or chat > 0:
                any_active.append((uid, mail, intra, chat, first, agents))

        if not any_active:
            print(f"  none — no external user with 2+ agents had cross-agent activity in {days} days.")
        else:
            for uid, mail, intra, chat, first, agents in any_active:
                email = user_meta[uid]["email"] or "(no email)"
                name = user_meta[uid]["full_name"] or "(no name)"
                method = user_meta[uid]["signup_method"]
                aliases = ", ".join(a["alias"] for a in agents)
                teams = ", ".join(sorted({a["team_id"] for a in agents}))
                print(f"\n  USER {email} ({name})  signup={method}")
                print(f"    agents ({len(agents)}): [{aliases}]")
                print(f"    teams: {teams}")
                print(f"    {days}-day: {mail} mail (intra-team {intra}), {chat} chat")
                print(f"    first activity in window: {first}")

        print(f"\n=== summary ===")
        print(f"  total users with 2+ agents:                  {len(multi)}")
        print(f"  internal (filtered out):                     {len(internal)}")
        print(f"  external with 2+ agents:                     {len(external)}")
        print(f"  external with {days}-day cross-agent activity:  {len(any_active)}")

        if include_internal:
            print(f"\n=== internal context (juan + eugenie teams) ===")
            for uid, agents in internal.items():
                agent_ids = [a["agent_id"] for a in agents]
                mail = await conn.fetchval(
                    f"""SELECT COUNT(*) FROM aweb.messages
                       WHERE (from_agent_id = ANY($1::uuid[]) OR to_agent_id = ANY($1::uuid[]))
                         AND created_at >= NOW() - INTERVAL '{days} days'""",
                    agent_ids,
                )
                chat = await conn.fetchval(
                    f"""SELECT COUNT(*) FROM aweb.chat_messages
                       WHERE from_agent_id = ANY($1::uuid[])
                         AND created_at >= NOW() - INTERVAL '{days} days'""",
                    agent_ids,
                )
                print(f"  {user_meta[uid]['email']}: {len(agents)} agents, "
                      f"{mail} mail, {chat} chat ({days}d)")
    finally:
        await conn.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="N-day multi-agent activity check")
    p.add_argument("--days", type=int, default=7, help="Window in days (default 7)")
    p.add_argument(
        "--include-internal",
        action="store_true",
        help="Also show juan + eugenie team activity for context",
    )
    args = p.parse_args()
    asyncio.run(main(args.days, args.include_internal))
