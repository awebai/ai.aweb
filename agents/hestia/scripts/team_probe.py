"""Full snapshot for a single team — agents, workspaces, deletes, messages, conversations.

Usage:
  uv run --with asyncpg python scripts/team_probe.py --team default:pmbah.aweb.ai
  uv run --with asyncpg python scripts/team_probe.py --team default:thano.aweb.ai

Answers question shapes:
  - "what's the state of team X?"
  - "agent-not-connected debugging — which agents/workspaces/paths"
  - "did cleanup soft-delete anything in this team?"
  - "BYOT namespace audit — controller_did, dns_status, registration_status"

Used during the 1.26.3 pmbah cleanup incident (#245) to trace the deleted rows.
Reuse for any 'team X is broken / agent-not-connected' triage.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import asyncpg

from _db import resolve_database_url


def _truncate(v, n=80):
    if isinstance(v, (bytes, memoryview)):
        return f"<{len(bytes(v))} bytes>"
    s = str(v)
    return s if len(s) <= n else s[: n - 3] + "..."


async def main(team_id: str):
    db_url = resolve_database_url()
    conn = await asyncpg.connect(db_url)
    try:
        print(f"========== team {team_id} ==========")

        st = await conn.fetchrow(
            """SELECT id, slug, name, owner_type, owner_user_id, owner_org_id,
                      aweb_team_id, aweb_team_controller_did, created_at, deleted_at
               FROM server.teams WHERE aweb_team_id = $1""",
            team_id,
        )
        if not st:
            print("  TEAM NOT FOUND in server.teams")
            return

        print(f"\n  server.teams row:")
        for k, v in dict(st).items():
            print(f"    {k:30s} = {_truncate(v)}")

        # managed_namespaces (BYOT detail)
        ns = await conn.fetchrow(
            """SELECT id, namespace_slug, domain, base_domain, is_default,
                      controller_did, dns_txt_name, dns_status,
                      registry_namespace_id, registration_status,
                      created_by_user_id, created_at, deleted_at
               FROM aweb_cloud.managed_namespaces WHERE team_id = $1""",
            st["id"],
        )
        if ns:
            print(f"\n  managed_namespaces row (BYOT):")
            for k, v in dict(ns).items():
                print(f"    {k:30s} = {_truncate(v)}")

        # agents
        agents = await conn.fetch(
            """SELECT agent_id, alias, address, created_at, deleted_at
               FROM aweb.agents WHERE team_id = $1 ORDER BY created_at""",
            team_id,
        )
        active_ids = [a["agent_id"] for a in agents if a["deleted_at"] is None]
        print(f"\n  agents ({len(agents)} total, {len(active_ids)} active):")
        for a in agents:
            mark = f" DELETED={a['deleted_at']:%Y-%m-%d %H:%M:%S}" if a["deleted_at"] else ""
            print(f"    - alias={a['alias']!r:25s} agent_id={a['agent_id']} "
                  f"created={a['created_at']:%Y-%m-%d %H:%M}{mark}")

        # workspaces (full, since these get hit by cleanup)
        ws = await conn.fetch(
            """SELECT workspace_id, agent_id, alias, hostname, workspace_path,
                      created_at, last_seen_at, deleted_at
               FROM aweb.workspaces WHERE team_id = $1 ORDER BY created_at""",
            team_id,
        )
        print(f"\n  workspaces ({len(ws)}):")
        for w in ws:
            ls = f"{w['last_seen_at']:%Y-%m-%d %H:%M:%S}" if w["last_seen_at"] else "never"
            mark = f" DELETED={w['deleted_at']:%Y-%m-%d %H:%M:%S}" if w["deleted_at"] else ""
            print(f"    - alias={w['alias']!r:25s} host={(w['hostname'] or '(no host)'):15s} "
                  f"last_seen={ls}{mark}")
            print(f"        workspace_path={w['workspace_path']!r}")

        if not active_ids:
            print("\n  (no active agents — no messaging probes)")
            return

        # messages
        mail = await conn.fetchval(
            """SELECT COUNT(*) FROM aweb.messages
               WHERE from_agent_id = ANY($1::uuid[]) OR to_agent_id = ANY($1::uuid[])""",
            active_ids,
        )
        mail_sent = await conn.fetchval(
            """SELECT COUNT(*) FROM aweb.messages WHERE from_agent_id = ANY($1::uuid[])""",
            active_ids,
        )
        print(f"\n  mail (all-time): {mail} touching team agents, {mail_sent} sent by team agents")

        # chat
        chat = await conn.fetchval(
            """SELECT COUNT(*) FROM aweb.chat_messages WHERE from_agent_id = ANY($1::uuid[])""",
            active_ids,
        )
        print(f"  chat (all-time): {chat} messages sent by team agents")

        # conversations (mail threads)
        convs = await conn.fetch(
            """SELECT conversation_id, conversation_type, status, created_at, closed_at
               FROM aweb.conversations WHERE team_id = $1 ORDER BY created_at""",
            team_id,
        )
        print(f"\n  conversations ({len(convs)}):")
        for c in convs:
            print(f"    - {c['conversation_id']} type={c['conversation_type']} "
                  f"status={c['status']} created={c['created_at']:%Y-%m-%d %H:%M} "
                  f"closed={c['closed_at']}")

        # recent messages (last 10)
        recent = await conn.fetch(
            """SELECT message_id, from_alias, to_alias, subject, created_at
               FROM aweb.messages
               WHERE from_agent_id = ANY($1::uuid[]) OR to_agent_id = ANY($1::uuid[])
               ORDER BY created_at DESC LIMIT 10""",
            active_ids,
        )
        if recent:
            print(f"\n  recent 10 mail messages:")
            for r in recent:
                subj = (r["subject"] or "")[:50]
                print(f"    {r['created_at']:%Y-%m-%d %H:%M:%S} "
                      f"{r['from_alias']!r:15s} -> {r['to_alias']!r:15s}  subj={subj!r}")
    finally:
        await conn.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Per-team snapshot")
    p.add_argument("--team", required=True, help="aweb_team_id (e.g. 'default:pmbah.aweb.ai')")
    args = p.parse_args()
    asyncio.run(main(args.team))
