# CTO Handoff
Last updated: 2026-04-24 (post-v0.5.4 ship)

## State in one paragraph

aweb 1.17.0 + aw CLI 1.17.0 + @awebai/claude-channel 1.3.0 shipped 2026-04-23. ac v0.5.4 shipped later the same day picking up those versions. GHA green on all four publish runs. `app.aweb.ai/api/health` returns 200; `aw work active` against prod returns active items (confirms aaks 500 fix is live). aakq epic + aaks + aakv + aakt + aakw + aakx all closed via these two releases. End-to-end: Amy's 2026-04-21 multi-team activation bug that kicked off this whole arc is fixed for every user who upgrades their local aw CLI to 1.17.0.

## What's live

- `pypi.org/project/aweb` 1.17.0 + `pypi.org/project/awid-service` 0.4.0.
- `npm @awebai/aw` 1.17.0 + `npm @awebai/claude-channel` 1.3.0.
- GHCR ac-cloud image tagged v0.5.4, deployed to app.aweb.ai.

## Open items

### For me to close
- **Amy's handoff Known Issues** — mailed Amy 2026-04-24 to update her #2 (aakn fix landed; workaround documented is stale) and confirm #1 (IDENTITY-MISMATCH) post-1.17.0 status. Follow up if I don't see a refresh from her within a wake-up or two.

### Filed and tracked, not my work
- **aweb-aakr** (P4, architectural) — membership-field overlap between teams.yaml.memberships and workspace.yaml.memberships. Filed open with both candidate framings. Deferred by agreement, no pending direction; NOT a pending-decision item on Juan.
- **aweb-aaky** (P3, ac Makefile realpath refactor) — symlinked invocations break relative paths in ac/Makefile. Workaround in coord-cloud/AGENTS.md; proper fix tracked. Not urgent.

### Environments
- Each permanent agent (Amy, Avi, Charlene, Enoch, Goto) needs to upgrade their local `aw` CLI to 1.17.0 (and channel plugin to 1.3.0 where used) to actually benefit from the fixes. That's their responsibility; I've documented it in status/engineering.md and it'll surface via Amy-response loop and their own wake-ups reading decisions.md.

## Release-gate discipline — exercised end-to-end, now standing policy

Five rules codified during the 2026-04-22/23 releases, all in memory + docs:
1. Release gate = full e2e user journey green (decisions.md 2026-04-22).
2. Review via shared working tree, no chat-pasted diffs.
3. Route dev-agent dispatch through the coordinator — don't chat devs directly with fix shapes.
4. Trust the Makefile's release-ready chain — not parallel skill-docs.
5. Written approval via mail — "GO" in user conversation ≠ GO in coordinator inbox.

All saved as feedback memories. Real lessons earned during actual release pressure.

## What to check FIRST on next wake-up

1. Amy replied on her Known-Issues refresh?
2. Anything broken post-deploy in app.aweb.ai? `aw work active`, `aw mail`, `aw chat` should all work end-to-end for multi-team agents.
3. Anything open in tracker I'm ignoring? `aw task list --status open --priority P1` — should be empty or close to it.
4. Coordinator handoffs stale again? John's is fresh (2026-04-23); Tom's was refreshed post-v0.5.4; Goto's status I don't have current visibility on — spot-check if aakq-fallout work in awid needs anything.

## Context I don't want to lose

- aaks root cause was latent since 2026-03-27 (commit `6ca98bbe`). The WITH-claims path of `list_active_work` was never tested, so the 500 was invisible in CI. The fix added the WITH-claims test. Similar coverage gaps might exist elsewhere — opportunistic review during quiet weeks would find them.
- Release discipline was stress-tested with two consecutive policy-exception temptations (pnpm version drift + local Docker net issue) and held both times. Shipping late > shipping broken > shipping with workarounds. Juan's no-workarounds posture is why.
- John's independent SOT analysis on both releases caught things my spec missed (doctor-check rename release note; dormant-install migration break; cross-namespace cert-member-address semantics). Coordinator-layer review is earning its keep.
