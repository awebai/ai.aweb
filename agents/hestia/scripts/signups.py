"""N-day sign-up rollup for Bertha-style outreach + Juan funnel reads.

Usage:
  uv run --with asyncpg python scripts/signups.py            # default 7d
  uv run --with asyncpg python scripts/signups.py --days 1
  uv run --with asyncpg python scripts/signups.py --days 30

Answers question shapes:
  - "how many new sign-ups in the past N days?"
  - "any detail on who they are and how they onboarded (CLI vs browser)?"
  - "anyone with email-on-record I can reach out to?"

Counts active (not deleted) users only. Excludes nothing — all signup_methods
are included (cli_signup, password, google, etc.).
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import asyncpg

from _db import resolve_database_url


async def main(days: int):
    db_url = resolve_database_url()
    conn = await asyncpg.connect(db_url)
    try:
        rows = await conn.fetch(
            f"""
            SELECT id, email, full_name, email_verified, signup_method, provider, created_at
            FROM aweb_cloud.users
            WHERE created_at >= NOW() - INTERVAL '{days} days'
              AND deleted_at IS NULL
            ORDER BY created_at
            """
        )

        total = len(rows)
        with_email = sum(1 for r in rows if r["email"])
        verified = sum(1 for r in rows if r["email_verified"])

        signup_counter = Counter(r["signup_method"] or "unknown" for r in rows)
        provider_counter = Counter(r["provider"] or "unknown" for r in rows)

        print(f"=== {days}-day sign-up rollup ({total} users) ===")
        print(f"  with email-on-record: {with_email}")
        print(f"  email-verified:       {verified}")
        print(f"  no-email-on-record:   {total - with_email}")

        print(f"\n  signup_method:")
        for k, c in sorted(signup_counter.items(), key=lambda x: -x[1]):
            print(f"    {k:25s} {c}")
        print(f"\n  provider:")
        for k, c in sorted(provider_counter.items(), key=lambda x: -x[1]):
            print(f"    {k:25s} {c}")

        print(f"\n=== individual rows ===")
        for r in rows:
            email = r["email"] or "(no email)"
            name = r["full_name"] or "(no name)"
            vmark = "v" if r["email_verified"] else "u"
            method = r["signup_method"] or "?"
            provider = r["provider"] or "?"
            print(
                f"  {r['created_at']:%Y-%m-%d %H:%M} [{vmark}] "
                f"{method:12s} provider={provider:10s} {email:50s} {name}"
            )
    finally:
        await conn.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="N-day sign-up rollup")
    p.add_argument("--days", type=int, default=7, help="Window in days (default 7)")
    args = p.parse_args()
    asyncio.run(main(args.days))
