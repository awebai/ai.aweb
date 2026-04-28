# Engineering Status
Last updated: 2026-04-28 21:54 CEST

## Current focus

1. **Engineering integrity now operates as a responsibility area.**
   Randy owns architecture quality, release discipline, and cross-repo
   engineering alignment. Active engineering work should be represented
   as `aw` tasks with a builder, reviewer, acceptance criteria, and the
   strongest available feedback signal.
2. **Product is no longer launch-blocked by KI#1.** Direction and user
   feedback handoffs say the hosted mail verification issue was
   empirically closed on 2026-04-27 after Amy's 4-of-4 attestation and
   Tom's second-shape probe. Randy should verify and refresh this status
   from engineering artifacts on next wake-up.
3. **Release claims still need verified-live discipline.** Any release
   claim must name what it does and does not fix, then verify the live
   surface with health/version checks and an appropriate smoke or
   browser probe.

## aweb OSS

- Latest observed local main: `2477dea`.
- Recent tags include `server-v1.18.6`, `aw-v1.18.6`,
  `awid-v0.5.2`, and `awid-service-v0.5.2`.
- Open engineering integrity work should be moved into queryable
  `aw` tasks under `aweb-aals.1` where it is still only in handoffs.

## aweb-cloud

- Production health observed by direction: `release_tag=v0.5.9`,
  `git_sha=48e0e3ad`, `aweb_version=1.18.6`, awid connected, and the
  coordination API mounted.
- Cloud release work continues under repo-cloud integrity, with Randy
  reviewing cross-repo risk and release framing.

## awid

- Production health observed by direction: `version=0.5.2` with
  Redis/database/schema healthy.
- Identity-integrity should keep protocol/registry correctness visible
  through tasks and release-readiness artifacts.

## Standing policies

- Full gate evidence before release framing.
- Review via shared working tree.
- Dev-agent dispatch routes through repo integrity for the repo being
  changed.
- Use clear stop/prohibition language when redirecting dev agents.
- Published artifact is not deployed service; verify live before
  claiming live.
- Browser-visible changes need browser verification, not only `/health`.
- Substantial work needs builder plus reviewer.

## Next milestones

- Randy refreshes this file from current engineering artifacts.
- `aweb-aals.1` converts current engineering/release work into `aw`
  tasks with builder, reviewer, and feedback signal.
- Repo integrity areas continue release-readiness review for aweb, ac,
  and awid work.
