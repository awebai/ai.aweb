"""Traction rollup for Bertha/Eugenie/Juan investor- and product-style asks.

Promoted from inline asyncpg probes after the question shape repeated:
Bertha 2026-05-08, PearX/Eugenie 2026-06-13, Bertha-for-Eugenie 2026-06-22.
Extended 2026-06-27: --by-week (weekly buckets) + --external (filter internal
team/Juan/atext) after week-bucketed and external-only asks each repeated.

Usage:
  uv run --with asyncpg python scripts/traction.py                 # snapshot, full rollup
  uv run --with asyncpg python scripts/traction.py --quick         # users + past-7d signups only
  uv run --with asyncpg python scripts/traction.py --days 7        # window for "new" metrics
  uv run --with asyncpg python scripts/traction.py --by-week       # weekly buckets, 3 months back
  uv run --with asyncpg python scripts/traction.py --by-week --weeks 12
  uv run --with asyncpg python scripts/traction.py --by-week --external  # external only
  uv run --with asyncpg python scripts/traction.py --json          # machine-readable

Answers question shapes:
  - "how many active users right now?"
  - "how many signups in past N days?"
  - "weekly activity for past 3 months?"
  - "external-only activity (exclude internal team noise)?"
  - "what's the current state of the company in numbers?"
  - "give me figures for the [investor/accelerator/HN] read"

Counts active (not-deleted) only. Internal accounts (juan@aweb.ai,
juan@juanreyero.com, eugenie@aweb.ai) excluded from email-based
metrics where it matters (per daily-signup-export skill convention).

PII discipline: internal team only. Don't paste raw output to
external surfaces. Bertha mail is by-design authorized for
outreach via daily-signup-export skill.

Internal namespace filter (--external):
  Excludes activity where the team_id's namespace part matches the
  internal team, Juan-side, atext, or test/probe patterns. See
  INTERNAL_NAMESPACES + TEST_NS_PATTERNS below for the exact list.
  Banked 2026-06-27 from Juan's flag that totals were
  internal-team-dominated.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import asyncpg

from _db import resolve_database_url, INTERNAL_EMAILS


# Namespace exclusion for --external mode. The team_id format on agents is
# "<team-slug>:<namespace>", and the namespace is what tells us whether it's
# internal team activity. Banked 2026-06-27 from Juan-flagged review.
INTERNAL_NAMESPACES = (
    "aweb.ai",                # team agents (sofia, athena, aida, iris, metis, bertha, ama, hestia, ...)
    "juan.aweb.ai",           # Juan's personal team (grace, mia, olivia, rose, peter, dave, ...)
    "atext.aweb.ai",          # ac instance team (ac-coordinator, ac-operations, ac-developer-*, ...)
    "juanreyero.com",         # Juan's secondary domain
    "london.juanreyero.com",  # Juan's other server
    "pepe.aweb.ai",           # Juan-side internal
    "team.aweb.ai",           # internal test/team
)
# Test/probe namespace patterns (SQL LIKE).
TEST_NS_PATTERNS = (
    "a2am-probe-%",
    "preflight-%",
    "wt%-%-athena.aweb.ai",  # Athena worktree spawns
    "tpl-test-%",
    "sandboxtester%",
    "aweb-xan.aweb.ai",
    "erp-2401f81c.aweb.ai",
    "xdcloud-development.aweb.ai",
)


def _external_predicate(team_id_col: str) -> str:
    """Returns SQL fragment for external-only filter on a given team_id column."""
    parts = [
        f"split_part({team_id_col},':',2) NOT IN ({','.join(repr(n) for n in INTERNAL_NAMESPACES)})"
    ]
    for p in TEST_NS_PATTERNS:
        parts.append(f"split_part({team_id_col},':',2) NOT LIKE '{p}'")
    return " AND ".join(parts)


async def gather(days: int, quick: bool) -> dict:
    db_url = resolve_database_url()
    conn = await asyncpg.connect(db_url)
    out: dict = {}
    try:
        out["users"] = await _users(conn)
        out["signups_window"] = await _signups_window(conn, days)
        if not quick:
            out["agents"] = await _agents(conn, days)
            out["namespaces"] = await _namespaces(conn)
            out["messages"] = await _messages(conn, days)
            out["billing"] = await _billing(conn)
            out["federation"] = await _federation(conn)
    finally:
        await conn.close()
    return out


async def _users(conn) -> dict:
    total = await conn.fetchval(
        "SELECT COUNT(*) FROM aweb_cloud.users WHERE deleted_at IS NULL"
    )
    with_email = await conn.fetchval(
        "SELECT COUNT(*) FROM aweb_cloud.users WHERE deleted_at IS NULL AND email IS NOT NULL"
    )
    verified = await conn.fetchval(
        "SELECT COUNT(*) FROM aweb_cloud.users WHERE deleted_at IS NULL AND email_verified = true"
    )
    deleted = await conn.fetchval(
        "SELECT COUNT(*) FROM aweb_cloud.users WHERE deleted_at IS NOT NULL"
    )
    return {
        "total_active": total,
        "total_inc_deleted": (total or 0) + (deleted or 0),
        "with_email": with_email,
        "email_verified": verified,
    }


async def _signups_window(conn, days: int) -> dict:
    rows = await conn.fetch(
        f"""
        SELECT id, email, full_name, email_verified, signup_method, provider, created_at
        FROM aweb_cloud.users
        WHERE created_at >= NOW() - INTERVAL '{days} days'
          AND deleted_at IS NULL
        ORDER BY created_at DESC
        """
    )
    new_with_email = [
        {
            "email": r["email"],
            "full_name": r["full_name"],
            "verified": r["email_verified"],
            "signup_method": r["signup_method"],
            "provider": r["provider"],
            "created_at": r["created_at"].isoformat(),
        }
        for r in rows
        if r["email"] and r["email"] not in INTERNAL_EMAILS
    ]
    return {
        "window_days": days,
        "total": len(rows),
        "with_email": sum(1 for r in rows if r["email"]),
        "external_with_email": [
            r for r in new_with_email if r["email"] not in INTERNAL_EMAILS
        ],
    }


async def _agents(conn, days: int) -> dict:
    total = await conn.fetchval(
        "SELECT COUNT(*) FROM aweb.agents WHERE deleted_at IS NULL"
    )
    new_window = await conn.fetchval(
        f"""
        SELECT COUNT(*) FROM aweb.agents
        WHERE created_at >= NOW() - INTERVAL '{days} days'
          AND deleted_at IS NULL
        """
    )
    return {"total_alive": total, f"new_in_{days}d": new_window}


async def _namespaces(conn) -> dict:
    managed = await conn.fetchval(
        "SELECT COUNT(*) FROM aweb_cloud.managed_namespaces WHERE deleted_at IS NULL"
    )
    members = await conn.fetchval(
        "SELECT COUNT(*) FROM aweb_cloud.team_members"
    )
    return {"managed": managed, "team_members": members}


async def _messages(conn, days: int) -> dict:
    mail_total = await conn.fetchval("SELECT COUNT(*) FROM aweb.messages")
    chat_total = await conn.fetchval("SELECT COUNT(*) FROM aweb.chat_messages")
    chat_sessions = await conn.fetchval("SELECT COUNT(*) FROM aweb.chat_sessions")
    mail_window = await conn.fetchval(
        f"SELECT COUNT(*) FROM aweb.messages WHERE created_at >= NOW() - INTERVAL '{days} days'"
    )
    chat_window = await conn.fetchval(
        f"SELECT COUNT(*) FROM aweb.chat_messages WHERE created_at >= NOW() - INTERVAL '{days} days'"
    )
    return {
        "mail_total": mail_total,
        "chat_total": chat_total,
        "coordination_total": (mail_total or 0) + (chat_total or 0),
        "chat_sessions": chat_sessions,
        f"mail_in_{days}d": mail_window,
        f"chat_in_{days}d": chat_window,
    }


async def _billing(conn) -> dict:
    rows = await conn.fetchval("SELECT COUNT(*) FROM aweb_cloud.billing")
    paid_active = await conn.fetchval(
        """
        SELECT COUNT(*) FROM aweb_cloud.billing
        WHERE tier != 'free'
          AND (subscription_ends_at IS NULL OR subscription_ends_at > NOW())
        """
    )
    stripe_customers = await conn.fetchval(
        "SELECT COUNT(DISTINCT stripe_customer_id) FROM aweb_cloud.billing WHERE stripe_customer_id IS NOT NULL"
    )
    return {
        "total_rows": rows,
        "paid_active": paid_active,
        "stripe_customers": stripe_customers,
    }


async def _federation(conn) -> dict:
    cross_server = await conn.fetchval(
        "SELECT COUNT(*) FROM aweb.federated_message_deliveries"
    )
    return {"cross_server_deliveries": cross_server}


async def gather_weekly(weeks: int, external: bool) -> dict:
    """Weekly buckets for the past N weeks. Optionally external-only."""
    db_url = resolve_database_url()
    conn = await asyncpg.connect(db_url)
    out: dict = {"weeks": weeks, "external": external, "rows": []}
    try:
        if external:
            ep_a = _external_predicate("a.team_id")
            ep_b = _external_predicate("team_id")
            ns_in = ",".join(repr(n) for n in INTERNAL_NAMESPACES)
            ns_like_excl = " AND ".join(
                f"mn.domain NOT LIKE '{p}'" for p in TEST_NS_PATTERNS
            )
            mail_q = f"SELECT date_trunc('week', m.created_at AT TIME ZONE 'UTC')::date AS w, COUNT(*) AS n FROM aweb.messages m JOIN aweb.agents a ON a.agent_id = m.from_agent_id WHERE m.created_at >= NOW() - INTERVAL '{weeks} weeks' AND ({ep_a}) GROUP BY w ORDER BY w"
            chat_q = f"SELECT date_trunc('week', c.created_at AT TIME ZONE 'UTC')::date AS w, COUNT(*) AS n FROM aweb.chat_messages c JOIN aweb.agents a ON a.agent_id = c.from_agent_id WHERE c.created_at >= NOW() - INTERVAL '{weeks} weeks' AND ({ep_a}) GROUP BY w ORDER BY w"
            agents_q = f"SELECT date_trunc('week', created_at AT TIME ZONE 'UTC')::date AS w, COUNT(*) AS n FROM aweb.agents WHERE created_at >= NOW() - INTERVAL '{weeks} weeks' AND ({ep_b}) GROUP BY w ORDER BY w"
            ns_q = f"SELECT date_trunc('week', mn.created_at AT TIME ZONE 'UTC')::date AS w, COUNT(*) AS n FROM aweb_cloud.managed_namespaces mn WHERE mn.created_at >= NOW() - INTERVAL '{weeks} weeks' AND mn.deleted_at IS NULL AND mn.domain NOT IN ({ns_in}) AND {ns_like_excl} GROUP BY w ORDER BY w"
        else:
            mail_q = f"SELECT date_trunc('week', created_at AT TIME ZONE 'UTC')::date AS w, COUNT(*) AS n FROM aweb.messages WHERE created_at >= NOW() - INTERVAL '{weeks} weeks' GROUP BY w ORDER BY w"
            chat_q = f"SELECT date_trunc('week', created_at AT TIME ZONE 'UTC')::date AS w, COUNT(*) AS n FROM aweb.chat_messages WHERE created_at >= NOW() - INTERVAL '{weeks} weeks' GROUP BY w ORDER BY w"
            agents_q = f"SELECT date_trunc('week', created_at AT TIME ZONE 'UTC')::date AS w, COUNT(*) AS n FROM aweb.agents WHERE created_at >= NOW() - INTERVAL '{weeks} weeks' GROUP BY w ORDER BY w"
            ns_q = f"SELECT date_trunc('week', created_at AT TIME ZONE 'UTC')::date AS w, COUNT(*) AS n FROM aweb_cloud.managed_namespaces WHERE created_at >= NOW() - INTERVAL '{weeks} weeks' AND deleted_at IS NULL GROUP BY w ORDER BY w"

        signups_q = f"SELECT date_trunc('week', created_at AT TIME ZONE 'UTC')::date AS w, COUNT(*) AS n FROM aweb_cloud.users WHERE created_at >= NOW() - INTERVAL '{weeks} weeks' GROUP BY w ORDER BY w"

        buckets: dict[str, dict] = {}
        for key, sql in [("mail", mail_q), ("chat", chat_q), ("agents_new", agents_q), ("namespaces_new", ns_q), ("signups", signups_q)]:
            rows = await conn.fetch(sql)
            for r in rows:
                buckets.setdefault(str(r["w"]), {})[key] = r["n"]
        for w in sorted(buckets):
            out["rows"].append({"week_start": w, **buckets[w]})
    finally:
        await conn.close()
    return out


async def gather_cli_funnel() -> dict:
    """CLI-signup → activation → engagement conversion funnel.

    Banked from 2026-06-30 Bertha-for-Eugenie ask. The non-obvious join:
        users → organization_members.user_id → organizations.aweb_namespace_domain
              → match aweb.agents.team_id (split_part on ':')

    `aweb_cloud.principals.user_id` and `principals.agent_id` are NEVER both
    set on the same row (polymorphic type table — human OR agent, never link).
    `aweb.api_keys` had 0 rows for CLI users.
    The org→namespace→team_id chain is the canonical path.
    """
    db_url = resolve_database_url()
    conn = await asyncpg.connect(db_url)
    try:
        row = await conn.fetchrow(
            """
            WITH cli_users AS (
                SELECT u.id, u.created_at,
                       EXTRACT(EPOCH FROM (NOW() - u.created_at)) / 86400 AS days_since
                FROM aweb_cloud.users u
                WHERE u.signup_method = 'cli_signup' AND u.deleted_at IS NULL
            ),
            user_orgs AS (
                SELECT cu.id AS user_id, cu.days_since, o.aweb_namespace_domain AS ns
                FROM cli_users cu
                LEFT JOIN aweb_cloud.organization_members om ON om.user_id = cu.id
                LEFT JOIN aweb_cloud.organizations o ON o.id = om.organization_id AND o.deleted_at IS NULL
            ),
            user_agents AS (
                SELECT uo.user_id, a.agent_id, a.created_at AS agent_at
                FROM user_orgs uo
                JOIN aweb.agents a ON split_part(a.team_id, ':', 2) = uo.ns AND a.deleted_at IS NULL
            ),
            mail_counts AS (
                SELECT ua.user_id, COUNT(m.message_id) AS n, MAX(m.created_at) AS last
                FROM user_agents ua LEFT JOIN aweb.messages m ON m.from_agent_id = ua.agent_id
                GROUP BY ua.user_id
            ),
            chat_counts AS (
                SELECT ua.user_id, COUNT(c.message_id) AS n, MAX(c.created_at) AS last
                FROM user_agents ua LEFT JOIN aweb.chat_messages c ON c.from_agent_id = ua.agent_id
                GROUP BY ua.user_id
            ),
            agent_counts AS (
                SELECT user_id, COUNT(DISTINCT agent_id) AS n FROM user_agents GROUP BY user_id
            ),
            per_user AS (
                SELECT cu.id, cu.days_since,
                       COALESCE(ac.n, 0) AS agents,
                       COALESCE(mc.n, 0) AS mail,
                       COALESCE(cc.n, 0) AS chat,
                       GREATEST(mc.last, cc.last) AS last_active
                FROM cli_users cu
                LEFT JOIN agent_counts ac ON ac.user_id = cu.id
                LEFT JOIN mail_counts mc ON mc.user_id = cu.id
                LEFT JOIN chat_counts cc ON cc.user_id = cu.id
            )
            SELECT
                COUNT(*) AS cli_total,
                COUNT(*) FILTER (WHERE agents > 0) AS with_agents,
                COUNT(*) FILTER (WHERE mail + chat = 0) AS zero_msgs,
                COUNT(*) FILTER (WHERE mail + chat BETWEEN 1 AND 5) AS bucket_1_5,
                COUNT(*) FILTER (WHERE mail + chat BETWEEN 6 AND 50) AS bucket_6_50,
                COUNT(*) FILTER (WHERE mail + chat > 50) AS bucket_50plus,
                COUNT(*) FILTER (WHERE last_active >= NOW() - INTERVAL '14 days') AS active_14d,
                COUNT(*) FILTER (WHERE last_active >= NOW() - INTERVAL '7 days') AS active_7d,
                AVG(mail + chat)::int AS avg_msgs,
                MAX(mail + chat) AS max_msgs,
                AVG(days_since)::int AS avg_age_days
            FROM per_user
            """
        )
        return dict(row)
    finally:
        await conn.close()


def _print_cli_funnel(data: dict):
    print("=== CLI-signup → engagement funnel (all-time) ===")
    total = data["cli_total"]
    activated = data["with_agents"]
    sent_any = total - data["zero_msgs"]
    sent_6 = data["bucket_6_50"] + data["bucket_50plus"]
    sent_50 = data["bucket_50plus"]

    def pct(n):
        return f"{100*n/total:.0f}%" if total else "—"

    print(f"Signed up via CLI                      {total:>4}   100%")
    print(f"└─ Activated (≥1 agent)                  {activated:>4}   {pct(activated)}")
    print(f"   └─ Sent ≥1 message ever               {sent_any:>4}   {pct(sent_any)}")
    print(f"      └─ Sent ≥6 messages (light)        {sent_6:>4}   {pct(sent_6)}")
    print(f"         └─ Sent ≥50 messages (engaged)   {sent_50:>4}   {pct(sent_50)}")
    print(f"            └─ Active in past 14 days     {data['active_14d']:>4}   {pct(data['active_14d'])}")
    print(f"               └─ Active in past 7 days     {data['active_7d']:>4}   {pct(data['active_7d'])}")
    print()
    print(f"avg messages/user: {data['avg_msgs']}  |  max: {data['max_msgs']}  |  avg age (days): {data['avg_age_days']}")


def _print_weekly(data: dict):
    scope = "external-only" if data["external"] else "all activity"
    print(f"=== weekly traction (past {data['weeks']} weeks, {scope}) ===")
    if data["external"]:
        print("Excluded namespaces:", ", ".join(INTERNAL_NAMESPACES))
        print("Excluded test patterns:", ", ".join(TEST_NS_PATTERNS))
    print()
    cols = ["mail", "chat", "agents_new", "namespaces_new", "signups"]
    print("week-start | " + " | ".join(f"{c:>14}" for c in cols))
    for row in data["rows"]:
        print(f"{row['week_start']} | " + " | ".join(f"{row.get(c, 0):>14}" for c in cols))


def _print_text(data: dict, days: int):
    u = data["users"]
    s = data["signups_window"]
    print(f"=== aweb traction (active = not-deleted) ===")
    print(f"users: {u['total_active']} active ({u['total_inc_deleted']} inc deleted) | {u['with_email']} with email | {u['email_verified']} verified")
    print(f"past {days}d signups: {s['total']} ({s['with_email']} with email; {len(s['external_with_email'])} external email)")
    for r in s["external_with_email"]:
        v = "v" if r["verified"] else "u"
        print(f"  [{v}] {r['created_at'][:10]}  {r['signup_method']:12s}  {r['email']:40s}  {r['full_name'] or '(no name)'}")
    if "agents" in data:
        a = data["agents"]
        print(f"agents: {a['total_alive']} alive (+{a[f'new_in_{days}d']} in {days}d)")
    if "namespaces" in data:
        n = data["namespaces"]
        print(f"namespaces: {n['managed']} managed | {n['team_members']} team members")
    if "messages" in data:
        m = data["messages"]
        print(f"coordination: {m['mail_total']} mail + {m['chat_total']} chat = {m['coordination_total']} cumulative | {m[f'mail_in_{days}d']} mail / {m[f'chat_in_{days}d']} chat in past {days}d | {m['chat_sessions']} chat sessions")
    if "billing" in data:
        b = data["billing"]
        print(f"billing: {b['total_rows']} rows | {b['paid_active']} paid active | {b['stripe_customers']} stripe customers")
    if "federation" in data:
        f = data["federation"]
        print(f"federation: {f['cross_server_deliveries']} cross-server deliveries")


def main():
    p = argparse.ArgumentParser(description="Traction rollup")
    p.add_argument("--days", type=int, default=7, help="Window for new-metric counts (snapshot mode; default 7)")
    p.add_argument("--quick", action="store_true", help="Users + signups only (skip messages/billing/federation)")
    p.add_argument("--by-week", action="store_true", help="Weekly buckets instead of snapshot")
    p.add_argument("--weeks", type=int, default=13, help="Number of weeks back for --by-week (default 13 = ~3 months)")
    p.add_argument("--external", action="store_true", help="With --by-week: exclude internal team / Juan / atext / test patterns")
    p.add_argument("--cli-funnel", action="store_true", help="CLI-signup → activation → engagement funnel (all-time)")
    p.add_argument("--json", action="store_true", help="Machine-readable output")
    args = p.parse_args()

    if args.cli_funnel:
        data = asyncio.run(gather_cli_funnel())
        if args.json:
            print(json.dumps(data, indent=2, default=str))
        else:
            _print_cli_funnel(data)
        return

    if args.by_week:
        data = asyncio.run(gather_weekly(args.weeks, args.external))
        if args.json:
            print(json.dumps(data, indent=2, default=str))
        else:
            _print_weekly(data)
    else:
        data = asyncio.run(gather(args.days, args.quick))
        if args.json:
            print(json.dumps(data, indent=2, default=str))
        else:
            _print_text(data, args.days)


if __name__ == "__main__":
    main()
