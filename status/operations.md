# Operations Status

Last updated: 2026-05-06 09:30 CEST (Hestia, post v0.5.23 verified-live + chat-409 spec-lock)

## Current focus

**aame architectural-completion + pagination-fix epic verified-live;
forward-going chat-409 surface diagnosed, fix on Grace's plate for
1.20.3 + AC v0.5.24 next cycle.** Verified-live for 1.20.2 + v0.5.23
pagination fix STANDS — chat-409 is a separate surface, doesn't
retroactively touch the pagination evidence. No urgent release
pressure on 1.20.3 (Zeus has plain send-and-wait as workaround;
no other customer hits surfaced yet).

## Open issue: chat --start-conversation 409 (aweb-aamx P1)

Surfaced 2026-05-06 ~08:20Z by Zeus (gsk.aweb.ai/zeus) on freshly-
upgraded aw 1.20.2 against just-deployed v0.5.23 + 1.20.2.

**Spec lock (Juan, 2026-05-06)**: Sessions are permanent, one per
pair (Slack-style). `--start-conversation` is purely a timing
semantic flag (5min wait vs default short wait); should NOT have
session-creation side effects, must NOT skip existing-session
probe, must NOT generate fresh session_id when active session
exists.

**Bug**: aweb 1.20.2 CLI at `cli/go/chat/chat.go:1137` overreaches:
flag bypasses probe-skip condition, CLI generates fresh session_id
UUID4, server's dedup correctly 409s. Single-line CLI fix —
remove `!opts.StartConversation` from probe-skip condition. Server
correct as-is (find_active_one_to_one_conversation_between +
chat.py:709 + dedup invariant all correct).

**Scope (corrected from earlier framings)**: Forward-going product
failure, NOT backward-compat-only. Affects ANY pair with an
existing active chat session, post-aame included. Confirmed
empirically by Athena against her own athena↔hestia post-aame
active session.

**Customer-impact-now**: Zeus is the only customer surfaced today;
he has working alternative (drop --start-conversation, plain
send-and-wait works — ~80s clean roundtrip per Aida's data). Not
blocking. Other customers hitting this surface: 0 reports as of
2026-05-06 09:30.

**Path forward**: aweb-aamx filed P1, Grace briefed by Athena.
Ships aweb 1.20.3 + AC v0.5.24 next cycle. No prod-DB ops on
Zeus's data (customer history preserved per standing policy).

## Live state (verified 2026-05-06 06:14:33Z)

- `app.aweb.ai/health`: `release_tag=v0.5.23`, `aweb_version=1.20.2`,
  `awid_service_version=0.5.4`,
  `git_sha=7705fc7ce93d17caf2cd7615984e6f0f4412094f`. Started
  2026-05-06T06:14:33Z.
- `api.awid.ai/health`: `version=0.5.4`, redis/db/schema healthy.
- aweb published: server 1.20.2 on PyPI (latest, simple index ✓);
  aw 1.20.2 on npm (dist-tag latest); awid-service 0.5.4 on PyPI;
  channel 1.4.0 on npm.
- Pre-deploy duplicate-1to1 cleanup executed cleanly during v0.5.22
  cycle (195 conversations closed across 16 pairs).

## Empirical attestation — pagination fix (1.20.2 + v0.5.23)

Three smoke probes against deployed v0.5.23 + 1.20.2:

1. **Baseline auto-thread (page-1)** — conversation 96317ca9
   (athena↔hestia). Probe 5707b48e attached cleanly. Athena
   confirmed (mail 20a6bf7e).
2. **Stale-by-recency from default-team** — conversation 878c06b1
   (sofia↔hestia, originated 2026-05-05, pushed off page 1 by
   intervening chat activity). Probe 37c5cb9e attached cleanly.
   Sofia confirmed (mail c2e65335).
3. **Stale-by-recency from cross-team-agent** — conversation
   70f1c868 (sofia↔athena, athena's default-team agent_id active).
   This is the exact 409 case that drove 1.20.2. Athena's probe
   72669b66 attached cleanly (mail 607dc80d).

Pagination fix verified-live on every shape we hypothesized.

## Release pipeline

Cycle (2026-05-04 → 2026-05-06):
- aweb 1.20.0 (aame epic): shipped. Verified-live.
- aweb 1.20.1 (Phase 12 hotfix): shipped. Verified-live.
- AC v0.5.22 (aame uptake + duplicate-1to1 cleanup): shipped.
  Verified-live.
- aweb 1.20.2 (pagination fix): shipped. Verified-live.
- AC v0.5.23 (1.20.2 uptake): shipped. Verified-live.

Verified-live mail sent to athena (362f0be6), sofia (2c69e142),
aida (0c529a82). Athena acknowledged (cc1bf154); Sofia framing
ladder ask is open for her lane.

## Operational discrepancies

- **chat-403 on pre-aame chat sessions (status uncertain).**
  Original framing: W3 protection rejects continuation of pre-aame
  signed messages, workaround = --start-conversation. Aida's
  runbook entry (commit 30c8870, currently held local) carried that
  recommendation. **The recommendation is now known to be wrong**
  (--start-conversation 409s on dedup pre-aamx fix; per spec is
  pure timing flag post-aamx). Open question: is the chat-403
  surface itself even a real customer hit, or theoretical-only?
  Zeus's plain send-and-wait worked on his pre-aame session
  (refutes 'plain CLI continuation 403s'). Action: Aida + me to
  empirically verify chat-403 customer history before deciding
  whether the entry should revise or close. Aida's commit 30c8870
  held from push regardless of Juan's go-call until the chat-403
  half is resolved.
- **Multi-team-agent agent_id-vs-did comparison (open ops follow-up).**
  cp.agent_id is team-scoped; same did_key/did_aw across team
  memberships maps to different agent_ids. Code paths comparing
  on cp.agent_id rather than cp.did/did_aw will misbehave for
  multi-team agents. Athena's lane to grep aweb codebase. Non-
  blocking; surfaced empirically during 1.20.2 diagnosis.
- **admin_analytics test fix at b7e86745 lives on main, ships
  next AC release.** Test-only fix (date-fragility on local-vs-
  UTC midnight); not in v0.5.23 because v0.5.23 was already
  pushed when the fix landed. Disposition: discipline-clean (no
  destructive retag); next AC release picks it up.
- **Iris agent not registered.** Hetzner identity bootstrap
  pending; framing routes via decision record per Sofia.

## Active claims

`aw work active`: zero rows. `aw work blocked`: zero rows.

## Workspace status (company team, default:aweb.ai)

- hestia (me): online, monitoring; epic verified-live, returning
  to ops cadence.
- athena: online, ack'd cycle closure; multi-team agent_id
  follow-up on her plate.
- sofia: online, framing ladder for distribution open in her lane.
- aida: online, runbook PR 3279c973 standalone-cleared.
- iris/metis: not yet registered (Hetzner pending for iris).

Dev team (`aweb:juan.aweb.ai`) members not visible from my workspace —
Athena is the cross-team bridge.

## Next checks

1. Daily `/health` on app.aweb.ai + api.awid.ai. Flag drift.
2. Watch for next release cycle — gate chain remains:
   release-ready (with immutability gate) + browser/journey suite +
   discipline #21 full chain on bless-and-run.
3. Sofia's framing ladder for distribution → when ready, route to
   Iris or Eugenie per her call.
4. Athena's multi-team agent_id grep follow-up — re-surface if
   another customer-shape bug trails the same root cause.
5. admin_analytics test fix at b7e86745 ships with next AC release;
   no separate v0.5.24 for that.

## Standing release-discipline (banked through 2026-05-06)

1. Release gate = full e2e + SOT + peer-review approval (mailed)
2. Review via shared working tree
3. Route work through the right peer
4. Trust the Makefile's release-ready chain
5. Written approval / decisions via mail
6. Use prohibition language explicitly when blocking a lane
7. Push release tags individually, never batched
8. Tracker audit needs symptom-check, not commit-message grep
9. Published artifact ≠ deployed service
10. Browser-verify UI-surface releases
11. Closure framing rests on empirical attestation
12. Reproducer-as-gate
13. Code-reviewer subagent for gate-input commits (Athena pre-flight)
14. Migration-checksum chase covers BOTH OSS wheel and AC embedded copy
15. Run new-client smoke probes against rolled prod before patch tags
16. Destructive cutover with cross-schema FKs requires constraint-diff
    audit (prod vs clean baseline) as explicit verification step
17. Pre-deploy gates with environment-specific prerequisites must
    fail-closed with explicit bypass, not skip-on-missing
18. Verified-live evidence cites the actually-committed SHA, not a
    bumped-but-unreverified SHA
19. Work in flight (uncommitted bumps, in-progress procedures) does not
    count as released until tag is pushed and live-verified
20. Reproducer must match the empirical surface (CLI 409 reproducer
    must surface 409 from production CLI binary against production
    server, not just unit-test logic)
21. Bless-and-run from peer = run the FULL release-ready chain end-to-end,
    don't shortcut to bump+tag
22. Code-reviewer subagent flagged silent-fall-through + the relevant
    scale is realistic for the production trajectory ⇒ blocker, not
    follow-up. Marking such follow-ups as non-blocker requires
    explicit threshold reasoning; absent that, treat as gate-input
    concern.
23. Test failures recurring at specific clock windows + reruns clean
    later are date/timezone-math signals, NOT transient-flake signals.
    "It passed on rerun" is not a diagnosis. When a failing test
    passes on rerun N hours later, check whether N corresponds to a
    UTC-vs-local-midnight crossing or other clock-based window before
    declaring transient. (Banked 2026-05-06 from admin_analytics
    fragility; Juan's pushback closed the loop on the "transient
    seed" framing, fix at b7e86745 lives on main.)
24. Documented workarounds must be empirically attested against the
    actual customer surface AND the predecessor states they apply on
    top of, not just the surface they claim to work around. Same
    family as #11 (closure framing rests on empirical attestation),
    applied at the workaround-documentation step. (Banked 2026-05-06
    from chat-403 + --start-conversation pair documented as
    'customers have user-side workaround' without empirical test
    against actual customer surface; Aida's commit 30c8870 held
    until verified.)
25. When the empirical surface contradicts a hypothesis, that's a
    refutation, not a "transient." Don't double down on the
    hypothesis. The first refutation should lead to test against a
    new shape immediately, not retreat into a narrowed framing of
    the same hypothesis. (Banked 2026-05-06 from two refutation-vs-
    transient confusions in one cycle: pytest-randomly seed framing
    on admin_analytics fragility, then backward-compat-only framing
    on chat-409 dedup. Both got clarified by Juan's "are you sure"
    pushback before downstream work absorbed the wrong frame.)
26. "Affects only one customer in current base" is not a scope claim
    about the bug class — it's an observation about THIS customer
    base AT THIS MOMENT. The product failure can be real for going-
    forward agents even when only one current-base customer hits it
    today. When scoping a bug to a customer-data class, reproduce
    against an internal pair you control to distinguish customer-
    data class from product class. (Banked 2026-05-06 from chat-409
    initial framing as 'pre-aame backward-compat only' — Athena's
    test against her own post-aame athena↔hestia session refuted
    that scope.)

`status/weekly.md` continues as a roll-up until replaced by a proper
dashboard.
