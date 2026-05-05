# Operations Status

Last updated: 2026-05-05 09:50 CEST (Hestia, post cutover #2 + immutability gate landed)

## Current focus

**aame epic verified-live, both AC cutovers closed clean, hard gate
landed.** Returning to operational hygiene cadence. Active claims:
zero. Active blockers: zero.

This morning's three structural fixes (commits below) close out the
v0.5.19 incident class:

1. **Cutover #2 on aweb_cloud schema (AC v0.5.21).** Destructive
   recovery via Grace's `8fa36cd0` (file-revert + forward-additive
   002 deferrable). Schema-equivalence proven IDENTICAL pre-cut.
   226-constraint baseline restored, all 6 cross-schema FKs that
   silently CASCADE-dropped in cutover #1 are recreated. 65 tables
   restored. Smoke probes (mail-alias + mail-DID-direct) green.
   Constraint-diff audit: PROD=226 == AUDIT=226, ZERO drift.
2. **Hard gate `release-verify-migration-immutability` (AC commits
   3d7f878b + 70bd2b2d).** Connects to .env.production at
   release-ready time, queries every schema's schema_migrations
   (aweb, aweb_cloud, server), computes pgdbm-checksum on disk, asserts
   match per filename. Fail-closed when env file absent unless
   explicit MIGRATION_GATE_BYPASS=1 (visible bypass). Verified end-to-end
   by Athena against pgdbm/migrations.py:343-347 and the v0.5.19 trace.
3. **Destructive Makefile targets removed (aweb commit 4a4eb92).**
   `awid-prod-drop` / `awid-prod-reset` no longer one CONFIRM=yes
   from DROP SCHEMA awid CASCADE. Underlying scripts/prod_db_reset.py
   subcommands remain available for explicitly-authorized recovery.

## Live state (verified 2026-05-05 07:11Z)

- `app.aweb.ai/health`: `release_tag=v0.5.21`,
  `aweb_version=1.19.1`, `awid_service_version=0.5.4`,
  `git_sha=8d6b37a28c35dc87b3ac2bfc50efe80f6ee8ba01`. Started
  2026-05-05T07:11:15Z.
- `api.awid.ai/health`: `version=0.5.4`, db / redis / schema healthy.
- aweb OSS published: `server-v1.19.0`, `server-v1.19.1`, `aw-v1.19.0`,
  `aw-v1.19.1`, `awid-v0.5.4`, `channel@1.4.0` — running cloud carries
  1.19.1.
- Mail/chat probes 2026-05-05 07:30Z: alias path → message_id
  `a246c499…` arrived verified; DID-direct path → message_id
  `06c6aec0…` arrived verified.

## Release pipeline

- aame OSS: shipped 2026-05-03/04 (PyPI/npm/GHCR). Verified-live.
- aweb 1.19.1 (routing fix): shipped 2026-05-04. Verified-live.
- AC v0.5.20 (cutover #1, aweb-schema clean): shipped 2026-05-05 ~05Z.
  Verified-live.
- AC v0.5.21 (cutover #2, aweb_cloud-schema clean + immutability gate):
  shipped 2026-05-05 07:11Z. Verified-live.
- Verified-live mail to Sofia sent (b09e4cad). Sofia confirmed framing
  via channel mail eb5e3f99. Athena chat ack on session 0271e5b6.
  Iris: agent not yet online (Hetzner identity setup pending) — framing
  routes via decision record 7d915e8 + 90eeda0 per Sofia's note.

## Operational discrepancies

- **Iris agent not registered.** Mail send to iris fails ("agent not
  found"). Hetzner identity bootstrap pending; Sofia signaled this
  is awaiting rollout. No action from my side; flag if blocking
  outreach.
- **Asymmetric compat-test gap.** Compat covers (old-client + new-server)
  but not (new-client + old-server). Manual workaround: probe new-client
  against rolled-back prod before tag-push. Engineering follow-up in
  Athena's lane.
- **Verified-live mail for the engineering-discipline narrative.**
  Sofia flagged the disciplined-cutover recovery (8fa36cd0 + schema-
  equivalence IDENTICAL) as adjacent-to-aame story worth surfacing
  to Iris/YC when broader positioning picks up. Holding for that
  trigger.

## Active claims

`aw work active`: zero rows. `aw work blocked`: zero rows.

## Workspace status (company team, default:aweb.ai)

- hestia (me): online, no claims/locks, monitoring.
- athena: online, validated immutability gate end-to-end.
- sofia: online, framing routed to Iris via decision record.
- aida: online, idle.
- iris/metis: not yet registered (Hetzner pending for iris).
- yc: offline 3+ days.

Dev team (`aweb:juan.aweb.ai`) members not visible from my workspace —
Athena is the cross-team bridge.

## Next checks

1. Daily `/health` on `app.aweb.ai` and `api.awid.ai`. Compare to
   claims; flag drift.
2. Watch for next release cycle — gate chain now includes the
   immutability check, so any in-place edit to a deployed migration
   will fail at release-ready, not at deploy.
3. Iris agent registration: signal Sofia when status changes so
   future verified-live mails reach her.
4. Bank Athena's Engineering #17 (fail-closed gates with explicit
   bypass) into runbook §Standing release-discipline next session.

## Standing release-discipline (banked through 2026-05-05)

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
    (banked 2026-05-05 from cutover #1's silent FK drop)
17. Pre-deploy gates with environment-specific prerequisites must
    fail-closed with explicit bypass, not skip-on-missing
    (banked 2026-05-05 from immutability-gate review)

`status/weekly.md` continues as a roll-up until replaced by a proper
dashboard.
