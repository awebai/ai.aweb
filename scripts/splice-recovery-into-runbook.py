#!/usr/bin/env python3
"""Splice ac's agent-identity-recovery.md into runbook.md Section 2.

Reads the synced copy at docs/support/agent-identity-recovery.md and
replaces the content between the BEGIN/END markers in
docs/support/runbook.md.

Source-of-truth for recovery content stays in ac/docs/support/. This
script is the bridge that lifts the synced file into the unified
runbook.md without losing the access-boundary property (Amy's repo
never reads ac directly; the docs-sync target's existing cp does).

Failure modes are loud — missing markers, missing source file, or
markers out of order all exit non-zero with a clear message.
"""

from __future__ import annotations

import sys
from pathlib import Path

BEGIN_MARKER = (
    "<!-- BEGIN: synced-from-ac/docs/support/agent-identity-recovery.md -->"
)
END_MARKER = (
    "<!-- END: synced-from-ac/docs/support/agent-identity-recovery.md -->"
)
DO_NOT_EDIT_NOTE = (
    "<!-- DO NOT EDIT BETWEEN THESE MARKERS — content auto-synced via "
    "make docs-sync -->"
)


def _strip_h1(text: str) -> str:
    """Drop the first H1 heading line from `text`, if present.

    runbook.md provides Section 2's heading (`## Section 2: Recovery
    scenarios`). The synced source file has its own `# Agent Identity
    Recovery Runbook` H1 that would duplicate inside Section 2.
    """
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("# ") and not stripped.startswith("## "):
            # Drop the H1 line and any blank line immediately after it.
            del lines[idx]
            if idx < len(lines) and not lines[idx].strip():
                del lines[idx]
            return "\n".join(lines)
        # First non-blank line wasn't an H1 — nothing to strip.
        return text
    return text


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    source = repo_root / "docs" / "support" / "agent-identity-recovery.md"
    runbook = repo_root / "docs" / "support" / "runbook.md"

    if not source.exists():
        print(f"ERROR: source file missing: {source}", file=sys.stderr)
        print(
            "Run `make docs-sync` (the cp portion) before this script.",
            file=sys.stderr,
        )
        return 1
    if not runbook.exists():
        print(f"ERROR: runbook missing: {runbook}", file=sys.stderr)
        return 1

    runbook_text = runbook.read_text()
    begin_idx = runbook_text.find(BEGIN_MARKER)
    if begin_idx == -1:
        print(
            f"ERROR: BEGIN marker missing from {runbook.name}.",
            file=sys.stderr,
        )
        print(
            "Expected line containing exactly:\n  " + BEGIN_MARKER,
            file=sys.stderr,
        )
        return 1
    end_idx = runbook_text.find(END_MARKER, begin_idx + len(BEGIN_MARKER))
    if end_idx == -1:
        print(
            f"ERROR: END marker missing (or before BEGIN) in {runbook.name}.",
            file=sys.stderr,
        )
        print(
            "Expected line containing exactly:\n  " + END_MARKER,
            file=sys.stderr,
        )
        return 1

    source_body = _strip_h1(source.read_text()).strip()
    new_section = (
        BEGIN_MARKER
        + "\n"
        + DO_NOT_EDIT_NOTE
        + "\n\n"
        + source_body
        + "\n\n"
    )

    prefix = runbook_text[:begin_idx]
    suffix = runbook_text[end_idx:]
    new_text = prefix + new_section + suffix

    if new_text == runbook_text:
        print(f"{runbook.name}: already in sync; no change.")
        return 0

    runbook.write_text(new_text)
    print(
        f"{runbook.name}: spliced {source.name} between markers "
        f"({len(source_body)} bytes)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
