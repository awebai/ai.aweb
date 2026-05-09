# Operations Status

Last updated: 2026-05-08 17:15 BST (Hestia, post v0.5.24 verified-live + aweb 1.20.7 server release + Bertha daily/hourly infra)

## Current focus

**aweb 1.20.7 + AC v0.5.24 verified-live** (2026-05-08 17:00:43Z).
Two same-day diagnose-to-ship cycles bundled in one release:
multi-team-agent did_key strict-walk (Mia at 1b55e8e) + chat
fresh-start contract end-to-end (Grace at 1054dd4). Closes the
chat-409 surface from Sofia's reproducer this morning.

Three smoke probes green: mail-attach-to-existing-conv (multi-team
did_key surface), chat baseline send, chat --start-conversation
against active session (the actual Grace fix surface — pre-fix
this 409'd, post-fix clean). Verified-live mails sent to athena
(0ad656f8) + sofia (764c2843) + aida (4b6d2c3e). Sofia ack'd —
will forward to Iris for multi-channel drafts. Aida ack'd — chat-403
runbook entry stays closed; e15838c held pending Juan greenlight.

Bertha's daily/hourly infra (set up earlier today, separate context)
runs independently of any AC version — direct prod-DB queries.

## CLI-only release pattern (established 2026-05-06, validated through 1.20.6)

For the prior CLI-only chain (1.20.4/5/6), pattern was:
- Don't bump server/pyproject.toml. Tag aw-vX.Y.Z directly at fix
  commit; goreleaser reads version from \${GITHUB_REF_NAME#aw-v}.
  No main commit, no server-v tag, no PyPI server publish. Source
  pkg state stays aligned with PyPI's server.

This cycle (1.20.7) was a server release, not CLI-only — full flow
applied (bump pyproject.toml at 106ade2, tag both server-v1.20.7 +
aw-v1.20.7, push both individually, both publish workflows fire).

Verified-live status:
- Pagination fix (1.20.2 + v0.5.23): STANDS, three-probe attestation.
- aamx fix (1.20.3): attested via Athena's make ship at 809056e (218
  e2e tests including Phase 12 chat exercising fixed flag behavior)
  + my own make ship at f8c7bce (same suite, 218/218). Customer-side
  lands via `aw upgrade` / pip / npm.
- aamy auto-update-check (also 1.20.3): rode along at 448a9f5 between
  Athena's bless-and-run SHA (809056e) and my bump (f8c7bce). Same
  make ship attestation. Customers upgrading to 1.20.3 also get the
  auto-update-check on interactive commands going forward.
- init UX cleanup (1.20.4 at 7adfea6): attested via Athena's make
  ship + Grace's code review SHIP-OK + my make ship at bumped tree
  (218 e2e green). Dogfood: aamy auto-update-check from 1.20.3
  detected 1.20.4 available, prompted upgrade; `aw upgrade` 1.20.3 →
  1.20.4 worked clean; banner suppressed post-upgrade. NOT yet
  dogfooded the actual init-output fixes (channel install
  instructions, agent guide URL, hook double-run, claim-human
  suppression) — needs real init run with API key against hosted
  team to replay Juan's customer scenario shape. Make ship test
  suite via init_output_test.go covers the unit-level surface.
- add-worktree refuse-on-tracked-.aw + init writes .git/info/exclude
  (1.20.5 at 394adae): attested via Athena's make ship + code-reviewer
  subagent SHIP-OK + my make ship at unbumped tree (218 e2e green).
  **Dogfood: reproduced Juan's customer-blocking case empirically** —
  scratch repo with tracked .aw/signing.key + `aw workspace
  add-worktree test-role` returned the explicit refusal + complete
  remediation (gitignore append + git rm --cached + commit) without
  any branch/worktree mutation. Customer-impact-now surface verified
  against the actual failure shape from the boscosis-bob demo.
- Grace review-findings cleanup (1.20.6 at 360bfe2): closes 4 review
  findings on 3a251a5 (BYOD wording, doctor_local missing-workspace
  hint, persistent-alias regression, Windows symlink skip). Attested
  via Athena's make ship + Grace re-review SHIP-OK + my make ship at
  unbumped tree (218 e2e green). Dogfood: aamy auto-update 1.20.5→1.20.6
  worked clean; aw doctor runs clean post-upgrade. User-visible flows
  (BYOD prompt + doctor remediation + persistent-alias) are
  interactive/specific-path, covered by unit tests + code review;
  load-bearing dogfood is Phase 21/22 init coverage in e2e.
- Multi-team did_key + chat fresh-start (1.20.7 server release at
  1054dd4 + AC v0.5.24 at 04c21432): full release flow — both
  server-v1.20.7 + aw-v1.20.7 tags, AC pyproject.toml bumped to
  0.5.24 at 106ade2, AC re-deploy required and live 17:00:43Z.
  Three smoke probes green: (1) mail send to athena attached cleanly
  to 96317ca9 (multi-team did_key surface, msg 007f2efd); (2) chat
  baseline send-and-leave clean; (3) **chat --start-conversation
  against the existing athena↔hestia session — clean send, no 409**.
  Pre-fix this hit 'Existing active chat session found' dedup; post-
  fix the server closes existing + creates new signed session as
  designed. Closes the chat-409 surface from Sofia's reproducer
  earlier 5/8.
- **Render deploy lag noted as ops debt** — v0.5.24 GHA finished at
  12:44Z, /health flipped at 17:00Z. Historical baseline ~3 min
  (v0.5.23 was 21:24→21:27Z). GHA workflow only does GHCR build+push,
  Render is auto-polling. Could be Render image-watcher slow or in
  upgrade window — one-time blip, not yet a pattern. Re-investigate
  if next cycle shows similar lag. Juan triggered manual deploy at
  the end ("ok deployed. please check").

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

- **chat-403 entry: CLOSED, no documentation.** Aida's empirical
  check across 5 sources (status/support.md, docs/support/ tree,
  git log --grep, support-mail history, Zeus's actual chat history)
  found zero customer reports. The would-be workaround
  (--start-conversation) would actively mis-route any 1.20.2
  customer with an active session into the aamx 409. Cleanest move:
  no entry. Case 6 ('Bug, Regression, Or Outage') in the runbook
  catches anything that emerges empirically. Aida's commit 30c8870
  reset HEAD~1, drops chat-403 hunk; recommit BYOD-422 + framing-
  invariant only. Banked: discipline #24 caught the shape pre-
  push; banking the operational pattern that diagnosis-as-
  workaround forwards must carry empirical attestation in the same
  mail OR explicit 'untested — verify before documenting' flag.
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
27. Cut-the-deploy-only-if-functional-change. Don't cut a deploy
    release purely to keep a pin-in-tagged-release synced. The
    source-pin spec reflects tested-minimum and should match what
    runs in production; bumping the pin without a deploy that
    exercises that minimum creates source-vs-deploy drift. If you
    bump the pin and there's no deploy, revert the bump and let
    the next functional change bring it forward. Same family as
    released-artifact-≠-deployed-service — this is pinned-in-
    main-≠-deploy-needed. (Banked 2026-05-06 from aweb 1.20.3
    cycle: aweb 1.20.3 was CLI-only, server code byte-identical
    to 1.20.2; AC pin bumped to >=1.20.3 at ab1d978b, then
    reverted at 18dd9c4c per Juan's catch — pin stays at >=1.20.2
    matching deployed v0.5.23, will bump naturally with next
    functional AC change.)
27a. CLI-only release pattern: don't bump server/pyproject.toml.
    Tag aw-vX.Y.Z directly at the fix commit; goreleaser reads
    version from \${GITHUB_REF_NAME#aw-v} per workflow config —
    pyproject.toml not load-bearing for CLI publish path. No
    server-v tag, no main push, no PyPI server publish, no
    Server CI run. Source pkg state stays aligned with PyPI's
    server (matches what's actually deployed). Avoids the
    pyproject-says-X-but-PyPI-aweb-is-Y drift. (Established
    2026-05-06 from aweb 1.20.4 cycle, validated 2026-05-07 on
    aweb 1.20.5 cycle.)
28. Tool-driven destructive git-state mutation is never acceptable
    as a side effect of a non-git-management command, even with
    loud warnings. Refuse + remediate, don't auto-fix the
    customer's repo for them. The tool should give the customer
    the exact commands to run; the customer makes the git/index
    decision. (Banked 2026-05-07 from aweb 1.20.5 add-worktree
    fix: initial 'overwrite .aw/ with warning' instinct was
    wrong; Juan's correction stood; preflight+refuse shape
    shipped.)

`status/weekly.md` continues as a roll-up until replaced by a proper
dashboard.
