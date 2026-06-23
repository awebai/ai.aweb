"""Traction rollup for Bertha/Eugenie/Juan investor- and product-style asks.

Promoted from inline asyncpg probes after the question shape repeated
3x: Bertha 2026-05-08, PearX/Eugenie 2026-06-13, Bertha-for-Eugenie
2026-06-22.

Usage:
  uv run --with asyncpg python scripts/traction.py                 # default: full rollup
  uv run --with asyncpg python scripts/traction.py --quick         # users + past-7d signups only
  uv run --with asyncpg python scripts/traction.py --days 7        # window for "new" metrics
  uv run --with asyncpg python scripts/traction.py --json          # machine-readable

Answers question shapes:
  - "how many active users right now?"
  - "how many signups in past N days?"
  - "what's the current state of the company in numbers?"
  - "give me figures for the [investor/accelerator/HN] read"

Counts active (not-deleted) only. Internal accounts (juan@aweb.ai,
juan@juanreyero.com, eugenie@aweb.ai) excluded from email-based
metrics where it matters (per daily-signup-export skill convention).

PII discipline: internal team only. Don't paste raw output to
external surfaces. Bertha mail is by-design authorized for
outreach via daily-signup-export skill.
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
    p.add_argument("--days", type=int, default=7, help="Window for new-metric counts (default 7)")
    p.add_argument("--quick", action="store_true", help="Users + signups only (skip messages/billing/federation)")
    p.add_argument("--json", action="store_true", help="Machine-readable output")
    args = p.parse_args()

    data = asyncio.run(gather(args.days, args.quick))
    if args.json:
        print(json.dumps(data, indent=2, default=str))
    else:
        _print_text(data, args.days)


if __name__ == "__main__":
    main()
