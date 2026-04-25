# Coordinator aweb-cloud (Tom) — Handoff

Last updated: 2026-04-25 (v0.5.5 tagged + GHA in flight)

## Current state

**ac v0.5.5 tagged** at `bc35ce5a` and pushed. GHA aweb-cloud CI/CD
run `24933534665` is in progress (started 2026-04-25T14:52:40Z;
v0.5.4 took 12m13s, expecting similar for the GHCR publish).

Origin/main HEAD is `bc35ce5a`. Pinned `aweb>=1.18.1`,
`awid-service>=0.5.1`.

**Production is still on v0.5.4** as of this handoff (auto-deploy
runs on its own schedule a few hours after image publish). Next
coord-cloud should verify v0.5.5 reached prod via:

```bash
curl -sS https://app.aweb.ai/health | python3 -m json.tool
```

Expect `release_tag: v0.5.5`, `git_sha: bc35ce5a...`,
`aweb_version: 1.18.1`, `awid_service_version: 0.5.1`.

## v0.5.5 ship summary

Three-commit delta from v0.5.4 (the canonical scope per Randy):

| SHA       | Ticket          | Purpose                                           |
|-----------|-----------------|---------------------------------------------------|
| `eb8e388d` | aweb-aala.10   | BYOIT certificate pickup documented (UI + docs)   |
| `343f40f8` | aweb-aala.10   | Split-stack BYOIT e2e (3 HOMEs + bonus seed fix)  |
| `bc35ce5a` | (release bump)  | aweb 1.18.1 + awid-service 0.5.1 + version 0.5.5  |

Closes `aweb-aala.10` (P1, ac alignment with the BYOIT cross-machine
cert contract). Picks up via the aweb pin bump:
- aala epic (BYOIT cross-machine cert lifecycle: awid stores full
  signed cert blobs; authenticated GET fetch endpoint; identity-scoped
  mail tolerates multi-team DID membership)
- aweb-aajs (BYOD wizard identity-lifetime prompt fix; CLI-side, zero
  ac surface impact)
- aweb-aakk (task-claim dashboard event publishing fix; positive ac
  inherit on the dashboard event feed)

Full narrative in `ai.aweb/docs/decisions.md` 2026-04-25 entry.

## Coord-borrow precedent set this release

aala.10 implementation was authored by Grace (John's dev) under
Tom's coord-borrow. Sequence:
1. Grace started ac changes unsupervised (lane incursion).
2. John redirected once; she partially complied, then continued.
3. John relayed to Tom; Tom proposed insight-option (text-only
   writeup, code stashed).
4. Juan pushed back: "is it not better to let Grace just do ac
   work as well and you code review?"
5. Randy concurred: "authorized cross-coord borrow is not what the
   dispatch-via-coord memory was banked against."
6. Tom briefed Grace explicitly (Juan-greenlit, Tom is ac-lane
   coord, ac questions to Tom + aweb questions to John).
7. Grace unstashed and worked under Tom's delta-review.
8. Same gate discipline (per-gate log + SOT + CTO mailed approval)
   as v0.5.4. Worked clean.

The pattern is now established: **authorized cross-coord borrow is
fine**; **unauthorized cross-coord work is not**. Difference is
explicit founder/CTO greenlight + the lane coord taking review
ownership.

Banked as `feedback_close_the_loop_at_tag_time.md` lesson on the
sender side and `feedback_dispatch_via_coordinator.md` clarification
on the receiver side.

## Release protocol locked in (v0.5.4 + v0.5.5 confirms it)

Every future release from here on:

1. Verify PyPI has the dep versions before bumping pyproject.toml.
2. Bump commit (pyproject.toml + uv.lock).
3. `uv sync` to pull post-bump deps into `.venv`.
4. `make release-ready` against post-bump `.venv`. Per-gate log
   mailed to Randy as a single composite (or per-gate if any go
   red).
5. SOT analysis mail to Randy — walk aweb-sot, awid-sot,
   trust-model, ac/sot for drift; name operator-visible edges in
   release notes; check vs prior version for regression.
6. CTO written-and-mailed approval. Prose in conversation does not
   count.
7. Explicit `git push origin main` + `git tag -a vX.Y.Z` + `git
   push origin vX.Y.Z`. Do NOT use `make ship` (auto-pushes tag,
   short-circuits approval).
8. Verify GHA green after tag push. If red, stop and mail Randy.
9. Tag-time ping to John (close-the-loop) and any other affected
   coord. Don't make peers git-log to find out.
10. Decision record to `ai.aweb/docs/decisions.md` mirroring
    aweb-side structure.

## Memory file count for next coord-cloud

Eight feedback memories accumulated in
`/Users/juanre/.claude/projects/-Users-juanre-prj-awebai-ai-aweb/memory/`:
- aweb_cross_namespace_membership.md (reference)
- feedback_review_via_symlink.md (review via shared tree)
- feedback_spec_scope_all_consumers.md (grep all file types)
- feedback_gut_over_confident_agent.md (verify before approving)
- feedback_dispatch_via_coordinator.md (route through coord)
- feedback_reproduce_exact_invocation.md (run the same harness)
- feedback_approval_via_mail.md (CTO approval via mail not prose)
- feedback_makefile_is_authoritative_gate_chain.md (Makefile wins
  over skill-doc gate lists; corollary on target body vs name)
- feedback_close_the_loop_at_tag_time.md (ping cross-coord peers)
- feedback_mail_body_escaping.md (heredoc-single-quote for mail
  bodies; backticks get command-substituted otherwise)

## Dev agents (ephemeral, in the ac repo)

| alias | last seen   | notes                                              |
|-------|-------------|----------------------------------------------------|
| grace | active today | Authored eb8e388d + 343f40f8 under Tom's borrow.  |
| mia   | offline 2d   | Closed aakv/aakt/aakw/aakx in v0.5.4 cycle.       |
| bob   | offline 9d+  | aweb-aakh stale claim; un-claim if still stale.   |
| leo   | offline 5d+  | (none)                                             |
| ivy   | offline 6d+  | (none)                                             |
| eve   | offline 8d+  | (none)                                             |

Mia's queued surface-walk dispatch was made moot by Grace's borrow;
her queue still has it, but she should treat it as stand-down on
return.

## Open ac branches

- `main` at `bc35ce5a` (v0.5.5).
- `aaga-archive` — remote-only; preserved per Randy's note.

## Known follow-up (carried from v0.5.4 handoff, still time-bound)

GHA workflow uses several actions still on Node.js 20:
`actions/checkout@v4`, `docker/build-push-action@v6`,
`docker/login-action@v3`, `docker/metadata-action@v5`,
`docker/setup-buildx-action@v3`, `docker/setup-qemu-action@v3`.
GitHub forces Node 24 by **2026-06-02** and fully removes Node 20
on **2026-09-16**. Pre-2026-06 task: bump action versions in
`.github/workflows/*.yml`. v0.5.5 GHA run still triggered the
deprecation annotation; not blocking.

## What to check FIRST on next wake-up

1. GHA run `24933534665` outcome — did v0.5.5 publish cleanly to
   GHCR? If red, diagnose and escalate to Randy.
2. Prod deploy state — is v0.5.5 serving `app.aweb.ai`?
3. Mail Randy + Juan + John with "v0.5.5 fully published" once both
   GHA and prod-roll are confirmed green. John specifically asked
   for this signal to close the aala epic on his side.
4. After prod-roll: spot-check the BYOIT flow against hosted prod
   (the new fetch-cert command, ByoitIdentitySetupFlow dashboard
   page, accept-invite same-machine framing).
5. `bob` stale claim on aweb-aakh.
6. Anything new on Juan/Randy side (mail inbox first).
