#!/usr/bin/env bash
# cutover_schema_equivalence.sh
#
# Scaffolding for Athena's architectural-review schema-equivalence proof
# of the aweb-cloud cutover consolidation 001.
#
# Given two AC git refs:
#   REF_BEFORE = the current chain (e.g., main with 001 + 002 + 003 + 004)
#   REF_AFTER  = Grace's consolidated 001 branch (single-file replacement)
#
# This script:
#   1. Creates two scratch git worktrees (one per ref) so each runs its
#      own embedded migrations directory.
#   2. uv-syncs each backend.
#   3. Creates two scratch local Postgres databases.
#   4. Runs `aweb-db --env=development setup` against each, applying each
#      ref's migrations via pgdbm (with template substitution).
#   5. pg_dumps each database's schema (--schema-only).
#   6. Normalizes both dumps (strips timing-sensitive comments) and diffs.
#
# Identical normalized diffs == schema-equivalence proven.
# Any non-trivial diff == consolidation has drift; reject the consolidation.
#
# Usage:
#   ./cutover_schema_equivalence.sh REF_BEFORE REF_AFTER
#
# Prereqs:
#   - Local Postgres running (postgres@17 brew service is fine).
#   - uv installed.
#   - AC sibling repo at the standard relative path.
#   - The provided refs exist in the AC repo.
#
# Cleanup:
#   - Worktrees and DBs are dropped on success. On failure they're left
#     in place for inspection.

set -euo pipefail

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 REF_BEFORE REF_AFTER" >&2
    echo "  e.g.: $0 main feature/aweb-consolidation" >&2
    exit 64
fi

REF_BEFORE="$1"
REF_AFTER="$2"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AC_REPO="${SCRIPT_DIR}/../ac"
SCRATCH_DIR="/tmp/cutover-schema-eq-${TS}"
WORKTREE_BEFORE="${SCRATCH_DIR}/ac-before"
WORKTREE_AFTER="${SCRATCH_DIR}/ac-after"
DB_BEFORE="aweb_eq_before_$$"
DB_AFTER="aweb_eq_after_$$"
DUMP_BEFORE="${SCRATCH_DIR}/schema-before.sql"
DUMP_AFTER="${SCRATCH_DIR}/schema-after.sql"
NORMALIZED_BEFORE="${SCRATCH_DIR}/schema-before.norm.sql"
NORMALIZED_AFTER="${SCRATCH_DIR}/schema-after.norm.sql"

mkdir -p "${SCRATCH_DIR}"
echo "Scratch: ${SCRATCH_DIR}"

# aweb-db setup uses Pydantic Settings which refuses defaults for these
# secrets; worktrees don't inherit ac/backend/.env from the host. Export
# minimal scratch values so setup runs end-to-end. Mirrors the defaults
# verify_db_reset_roundtrip.py uses (script note in script.py:122-148).
export SECRET_KEY="${SECRET_KEY:-cutover-eq-secret-key-32-bytes-ok}"
export SESSION_SECRET_KEY="${SESSION_SECRET_KEY:-cutover-eq-session-secret-32-bytes}"
export JWT_SECRET_KEY="${JWT_SECRET_KEY:-cutover-eq-jwt-secret-32-bytes-ok}"
export AWEB_INTERNAL_AUTH_SECRET="${AWEB_INTERNAL_AUTH_SECRET:-cutover-eq-internal-auth}"
export AWEB_CUSTODY_KEY="${AWEB_CUSTODY_KEY:-$(printf 'aa%.0s' {1..32})}"
export AWEB_PARENT_CONTROLLER_KEY="${AWEB_PARENT_CONTROLLER_KEY:-$(printf '11%.0s' {1..32})}"
export AWID_REGISTRY_URL="${AWID_REGISTRY_URL:-https://awid.invalid}"

cleanup_failure_artifacts_kept() {
    echo "FAILED. Leaving worktrees + DBs for inspection:"
    echo "  Worktrees: ${WORKTREE_BEFORE} ${WORKTREE_AFTER}"
    echo "  DBs:       ${DB_BEFORE} ${DB_AFTER}"
}

cleanup_success() {
    echo "Cleaning up (success path)"
    dropdb --if-exists "${DB_BEFORE}" || true
    dropdb --if-exists "${DB_AFTER}" || true
    git -C "${AC_REPO}" worktree remove --force "${WORKTREE_BEFORE}" 2>/dev/null || true
    git -C "${AC_REPO}" worktree remove --force "${WORKTREE_AFTER}" 2>/dev/null || true
    rm -rf "${SCRATCH_DIR}"
}

trap cleanup_failure_artifacts_kept ERR

echo
echo "=== Phase 1: Git worktrees ==="
git -C "${AC_REPO}" worktree add "${WORKTREE_BEFORE}" "${REF_BEFORE}"
git -C "${AC_REPO}" worktree add "${WORKTREE_AFTER}"  "${REF_AFTER}"

echo
echo "=== Phase 2: uv sync (each worktree) ==="
(cd "${WORKTREE_BEFORE}/backend" && uv sync >/dev/null)
(cd "${WORKTREE_AFTER}/backend"  && uv sync >/dev/null)

echo
echo "=== Phase 3: Scratch databases ==="
createdb "${DB_BEFORE}"
createdb "${DB_AFTER}"

echo
echo "=== Phase 4a: Apply ${REF_BEFORE} migrations ==="
(cd "${WORKTREE_BEFORE}/backend" && \
    DATABASE_URL="postgresql:///${DB_BEFORE}" \
    uv run aweb-db --env=development setup)

echo
echo "=== Phase 4b: Apply ${REF_AFTER} migrations ==="
(cd "${WORKTREE_AFTER}/backend" && \
    DATABASE_URL="postgresql:///${DB_AFTER}" \
    uv run aweb-db --env=development setup)

echo
echo "=== Phase 5: pg_dump schema-only ==="
pg_dump --schema-only --no-owner --no-privileges \
    --schema=aweb --schema=aweb_cloud --schema=server \
    "${DB_BEFORE}" > "${DUMP_BEFORE}"
pg_dump --schema-only --no-owner --no-privileges \
    --schema=aweb --schema=aweb_cloud --schema=server \
    "${DB_AFTER}"  > "${DUMP_AFTER}"

echo
echo "=== Phase 6: Normalize and diff ==="
# Strip pg_dump's "-- Dumped by..." / "-- Dumped from..." headers and any
# SET / metadata that varies between runs:
# - SET (search_path quoting, transaction_timeout from PG17, etc).
# - \restrict / \unrestrict <random-token> emitted by pg_dump 17+;
#   tokens differ between every run and produce noisy diffs.
# Keep DDL.
normalize() {
    grep -vE '^-- Dumped (by|from) ' "$1" \
        | grep -vE '^SET (transaction_timeout|search_path|idle_in_transaction|lock_timeout|client_min_messages|row_security|standard_conforming_strings|client_encoding|check_function_bodies|xmloption|default_tablespace|default_table_access_method|statement_timeout) ' \
        | grep -vE '^\\(restrict|unrestrict) ' \
        | grep -vE '^-- (Name: schema_migrations|Data for Name:)' \
        | sed -E 's/[[:space:]]+$//' \
        | awk 'NF || prev { print; prev = NF }'
}

normalize "${DUMP_BEFORE}" > "${NORMALIZED_BEFORE}"
normalize "${DUMP_AFTER}"  > "${NORMALIZED_AFTER}"

echo
echo "Normalized dumps:"
echo "  ${NORMALIZED_BEFORE} ($(wc -l < "${NORMALIZED_BEFORE}") lines)"
echo "  ${NORMALIZED_AFTER}  ($(wc -l < "${NORMALIZED_AFTER}") lines)"

echo
if diff -u "${NORMALIZED_BEFORE}" "${NORMALIZED_AFTER}"; then
    echo
    echo "✅ Schema-equivalence: IDENTICAL"
    trap - ERR
    cleanup_success
    exit 0
else
    echo
    echo "❌ Schema-equivalence: DRIFT detected (see diff above)"
    echo "   Worktrees and DBs preserved at ${SCRATCH_DIR}"
    cleanup_failure_artifacts_kept
    trap - ERR
    exit 1
fi
