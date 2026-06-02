"""Shared DB connection helper for hestia analytics scripts.

Resolves DATABASE_URL in this order:
  1. $DATABASE_URL env var (set explicitly by caller)
  2. read from $AC_ENV_FILE (default: ../../../../ac/.env.production relative to this file)

PII discipline: these probes touch user emails, names, and message metadata.
Never echo raw output to external surfaces. Internal coordination + Bertha
outreach pipeline only. Delete tmp files / dumps after use.
"""

from __future__ import annotations

import os
import re
from pathlib import Path


INTERNAL_EMAILS = {"juan@aweb.ai", "juan@juanreyero.com", "eugenie@aweb.ai"}


def resolve_database_url() -> str:
    explicit = os.environ.get("DATABASE_URL")
    if explicit:
        return explicit
    env_file = os.environ.get("AC_ENV_FILE")
    if not env_file:
        here = Path(__file__).resolve()
        # hestia/scripts/_db.py -> hestia/scripts -> hestia -> agents -> ai.aweb -> awebai -> ../ac
        # Use the ac symlink under hestia/ as the canonical path.
        candidates = [
            here.parent.parent / "ac" / ".env.production",
            here.parent.parent.parent.parent.parent / "ac" / ".env.production",
        ]
        for c in candidates:
            if c.exists():
                env_file = str(c)
                break
    if not env_file or not Path(env_file).exists():
        raise SystemExit(
            "ERROR: cannot find DATABASE_URL. Set $DATABASE_URL or $AC_ENV_FILE."
        )
    with open(env_file) as fh:
        for line in fh:
            m = re.match(r"^DATABASE_URL=(.*)$", line.strip())
            if m:
                return m.group(1)
    raise SystemExit(f"ERROR: DATABASE_URL not found in {env_file}")
