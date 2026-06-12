# Lesson: verify "released binary" claims against the binary, not a stale checkout

**2026-06-12.** I told rose twice that `AWEB_HTTP_TIMEOUT` was "not honored /
not plumbed in any format" based on a repo-wide grep that found zero references.
rose corrected me with runtime evidence from the installed binary. I was wrong.

**Root cause:** my local `aweb` sibling checkout was **20 commits behind**
origin/main and never had the aaqm transport-hardening commits (`be6db091`,
`acda65fd`) that add the env read. The released `aw 1.26.18` (commit `e071f63`)
ships them; my grep ran against stale source. I correctly followed "verify
against source, not memory" — but the *source tree itself* was stale relative to
the released artifact, so the verification was hollow.

**The rule:** for any "does the RELEASED binary / deployed service do X?"
question, ground truth is the **artifact**, not my local working tree:
1. Run the actual binary (`AWEB_HTTP_TIMEOUT=bogus aw whoami` reproduced it in
   one command) and/or check `aw version` for the commit.
2. Read `origin/main` or the release tag (`git show origin/main:path`,
   `git grep origin/main`), not just `HEAD`, after confirming how far behind
   `HEAD` is (`git rev-list --count HEAD..origin/main`).
3. My agent CLAUDE.md wake-up routine pulls *this* repo (ai.aweb) but I do NOT
   routinely pull the `aweb`/`ac` sibling repos — so they drift. Pull or
   `git fetch` the sibling before citing its source as current.

**Why it matters:** I'm the global A2A expert fielding inbound questions; wrong
guidance off a stale tree steers hackathon teams wrong. Runtime reproduction is
cheap and decisive — prefer it for binary-behavior claims.

Linked from [[a2a-system-map]] (HTTP timeouts) and [[a2a-hackathon-bringup]].
