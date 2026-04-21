#!/usr/bin/env bash
# Move each agent's Ed25519 signing key out of the public ai.aweb repo
# into the private co.aweb repo, replacing it with a relative symlink.
# Idempotent — already-secured and uninitialized agents are skipped.
#
# Usage: bin/secure-agents.sh

set -euo pipefail
shopt -s nullglob

REPO="$(cd "$(dirname "$0")/.." && pwd)"
CO_REL="../co.aweb"
CO="$REPO/$CO_REL"
[ -d "$CO" ] || { echo "FAIL: sibling co.aweb not found at $CO"; exit 1; }
CO="$(cd "$CO" && pwd)"

# Preflight: .gitignore must cover signing.key before we touch anything.
if ! git -C "$REPO" check-ignore -q "agents/_probe_/.aw/signing.key"; then
    echo "FAIL: .gitignore does not cover agents/*/.aw/signing.key"
    echo "  Add this line to $REPO/.gitignore:"
    echo "    agents/*/.aw/signing.key"
    exit 1
fi

secured=()
already=()
skipped=()
warnings=()

for agent_dir in "$REPO"/agents/*/; do
    role="$(basename "$agent_dir")"
    aw="${agent_dir}.aw"
    key="$aw/signing.key"

    if [ ! -d "$aw" ]; then
        skipped+=("$role (no .aw/)")
        continue
    fi
    if [ ! -e "$key" ] && [ ! -L "$key" ]; then
        skipped+=("$role (no signing.key)")
        continue
    fi
    if [ -L "$key" ]; then
        already+=("$role")
        continue
    fi

    co_role_dir="$CO/aw/$role"
    co_key="$co_role_dir/signing.key"

    if [ -e "$co_key" ]; then
        echo "FAIL: $co_key already exists — refusing to overwrite."
        echo "  (role: $role) Move it aside manually if stale."
        exit 1
    fi

    mkdir -p "$co_role_dir"
    chmod 700 "$co_role_dir"
    mv "$key" "$co_key"
    chmod 600 "$co_key"
    ln -s "../../../../co.aweb/aw/$role/signing.key" "$key"

    if [ ! -L "$key" ] || [ ! -f "$key" ]; then
        echo "FAIL: symlink for $role is not resolving"
        exit 1
    fi
    if ! git -C "$REPO" check-ignore -q "agents/$role/.aw/signing.key"; then
        echo "FAIL: agents/$role/.aw/signing.key not gitignored after move"
        exit 1
    fi

    ws="$aw/workspace.yaml"
    if [ -f "$ws" ] && grep -Eq '^[[:space:]]*api_key[[:space:]]*:[[:space:]]*[^"'"'"'[:space:]]' "$ws"; then
        warnings+=("$role: workspace.yaml has a non-empty api_key — review before committing")
    fi

    secured+=("$role")
done

fmt_list() { [ $# -eq 0 ] && echo "(none)" || echo "$*"; }

echo
echo "Secured now:      $(fmt_list "${secured[@]}")"
echo "Already secured:  $(fmt_list "${already[@]}")"
echo "Skipped:          $(fmt_list "${skipped[@]}")"

if [ ${#warnings[@]} -gt 0 ]; then
    echo
    echo "Warnings:"
    for w in "${warnings[@]}"; do echo "  $w"; done
fi

if [ ${#secured[@]} -eq 0 ]; then
    echo
    echo "Nothing new to commit."
    exit 0
fi

ai_paths=""
co_paths=""
for role in "${secured[@]}"; do
    ai_paths+=" agents/$role"
    co_paths+=" aw/$role"
done

echo
echo "To commit (private repo first so public push can't reference a missing key):"
echo
echo "  cd $CO && git add$co_paths && git commit -m 'Add signing keys' && git push"
echo "  cd $REPO && git add$ai_paths && git commit -m 'Add agent identities' && git push"
