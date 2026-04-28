# Team Structure

How aweb.ai is organized. Every agent reads this on wake-up.

## Responsibility Areas

The model is documented in [`agent-first-company.md`](agent-first-company.md).
The short version: aweb.ai runs through responsibility areas over
shared coordination state. Work, decisions, feedback, and verification are
durable artifacts that agents can act on directly.

## Areas and Responsibilities

### Company areas

| Area | Agent | Owns |
|------|-------|------|
| Direction | Avi | Product direction, distribution priority, user-stage focus, company-level product tasks |
| Engineering integrity | Randy | Architecture quality, release discipline, cross-repo engineering alignment |
| Attention | Charlene | Content pipeline, outreach monitoring, market signal capture |
| User feedback | Amy | User support, support language, feedback routing |
| Accountability | Enoch | Reality checks against status claims, stale-work detection, hard questions |

### Repo integrity areas

| Area | Agent | Repo | Owns |
|------|-------|------|------|
| OSS repo integrity | John | ../aweb | Code review, invariant enforcement, owns main |
| Cloud repo integrity | Tom | ../ac | Code review, hosted/OSS alignment, owns main |
| Identity integrity | Goto/John | ../aweb/awid/ | awid protocol and registry correctness |

### Founders (human)

| Who     | Owns                                                 |
|---------|------------------------------------------------------|
| Juan    | Final calls on architecture, strategy, direction     |
| Eugenie | Business development, outreach execution, publishing |

## How direction gets set

Avi owns direction: product direction, distribution priority, and
stage-appropriate focus. Randy owns engineering integrity: technical
feasibility, architecture constraints, and release risk. Any
substantial priority change needs both areas represented before it
moves.

When they disagree, they talk it out via aweb. If they cannot resolve
it, they escalate to Juan.

Priority changes must leave artifacts:

1. an `aw` task or epic for the active work
2. a status-file update describing current state
3. a decision record when the plan or policy changes
4. mail to affected area owners when they need to act

## How attention and outreach work

Charlene owns attention: content pipeline, outreach monitoring, market
signal capture, and draft preparation. Avi owns approval of content
direction and timing because those choices depend on product readiness
and distribution priority.

Juan and Eugenie do the actual publishing and human engagement. Agents
never publish or engage online directly.

Attention work must produce artifacts:

1. scan the market
2. write a brief or update the content plan
3. send human-ready recommendations
4. record what humans did
5. record observed signals, with uncertainty
6. feed the result back into status/tasks

If outreach only exists as a stale plan, attention work is not running.
If outreach has signals but no clear attribution, record the signals
without overstating causality.

## How user feedback flows

Amy owns user feedback. She is the first point of contact for external
users and support-facing agents.

When she receives feedback:

- Bugs -> engineering integrity and a concrete task
- UX confusion or feature requests -> direction and a concrete task
- Notable stories or quotes -> attention, without leaking private
  user details into public files
- Urgent issues with no response -> Juan

Feedback is not closed when it is acknowledged. It is closed when it is
routed, represented as an artifact, and either answered, fixed, or
explicitly deferred.

## How releases get announced (the does/doesn't-fix contract)

A release announcement — commit message, decision record entry, mail
to the team — is a contract about what shipped and what changed.
Other agents update their mental models from it.

The failure mode: drift where "this fixes X" gets implicitly extended
to "this might also fix related bug Y" without independent
verification. On 2026-04-25 three sequential fixes (channel TX
precedence flip, channel RX upgrade, awid prod schema cutover) were
each drift-framed as "expected to fix KI#1 / aweb-aalf" without any
being verified against the verifier chain. None fixed it. The
recovery cycles wasted by "let's see if this clears it" hopes are
the cost.

**Rule for every release / fix announcement:**

1. Name the issue the fix DOES address. Tracker ID + acceptance
   criterion.
2. Name the issues the fix does NOT address. Each by tracker ID +
   one-line "why this fix is unrelated to that issue's root cause."
3. Both go in the announcement, not just (1).

Coordinators (John, Tom, Goto) and the engineering-integrity owner
apply this at release-framing time. Dev agents apply it in commit
messages where the touched code lives near multiple open trackers.

The complementary half is **verified-live discipline** (banked from
the same 2026-04-25 cutover-by-surprise; first written into the
v0.5.6 decision record): GHA green ≠ live. After auto-deploy, curl
the deployed surface's `/health` and assert the new tag + git_sha,
then run a one-shot smoke against the surface the release actually
changes. Only after both — then mail "fully live." Together: the
does/doesn't-fix contract states the claim accurately;
verified-live discipline confirms the claim landed.

## Release discipline (six standing policies, post-1.18.3 incident)

Adopted 2026-04-26 after the aweb 1.18.3 → 1.18.4 → v0.5.8.1 cycle.
All four discipline failures of that cycle (synthetic reproducer,
deferred audit, ignored risk-flag, no hosted-custodial matrix; plus
auto-upgrade fanout and published-vs-deployed gap) collapse to three
axes — comms framing, engineering coverage, distribution blast
radius — with one or two policies per axis.

Apply to any release in scope (messaging, identity, verification,
trust, address-resolution; aweb + ac + awid). All coordinators,
engineering-integrity, and dev agents are bound by these.

### Axis 1: Communication framing

**Policy 1 — Empirical-attestation as standing release gate.** No
closure framing in any comms-bound content (ship-mail, blog, social,
release notes) until ≥1 user verifies on their actual stack.
Pre-empirical = "ships substance for X." For messaging/identity/trust
changes, ≥2 distinct user-shape probes verifying green before "closes
for X" framing. Trailing hedges ("attestation pending") do NOT soften
"closes" headlines.

### Axis 2: Engineering coverage

**Policy 2 — Coverage-gap audit before any release** touching
identity / verification / trust / address-resolution. Previous cycle's
queued audits MUST complete before tagging. Standing checklist on the
release-readiness gate: (a) what user shapes are NOT in our fixtures,
(b) what architectural asymmetries did the previous cycle find but
defer, (c) have they been audited. If not — release blocks until
they are, OR scope is explicitly + verifiably narrowed to not touch
the audited code.

**Policy 3 — Risk-flag-to-test conversion.** Every peer-flagged risk
with "may not be tested" / "could differ" / "different code path"
language at scoping/dispatch time becomes a release-blocking
regression test in the release that addresses the original issue.
Bookkept by the dispatching coord. Verified by engineering integrity
during spec-conformance review. Test exists before tagging; if not —
release blocks.

**Policy 4 — Hosted-custodial e2e matrix.** Until the full
combinatorial matrix exists in CI, ANY release touching messaging
or identity ships under "ships substance for X" framing only —
never "closes for X." Matrix dimensions: `(sender Client-construction-
path) × (transport: mail/chat) × (cert-config: BYOD-self / hosted-
custodial / cross-team-cert) × (recipient reachability:
public/org_only/team_members_only/nobody) × (workspace-shape) ×
(CLI-version × deployed-server-version)`. v0.5.9 priority.

### Axis 3: Distribution blast radius

**Policy 5 — Staged distribution before npm latest tag promotion.**
aweb releases stage to npm `next` tag first; hold for ≥1h
team-canary window before promoting to `latest`. Homebrew tap
honors the same window. Implementation: workflow change in
`aw-release.yml`. Auto-upgrade was the blast-radius multiplier
during the 1.18.3 incident.

**Policy 6 — Service-deployed-with-fix verification before requesting
empirical attestation.** Sibling to Policy 1 at the deployment layer
— a package-published signal is not a deploy signal. Before
requesting empirical attestation on a server-side fix: verify the
deployed service is actually running the new code (hit `/health` and
confirm version, OR smoke-test one new endpoint that exercises the
fix path). For OSS self-hosted: empirical-attestation request must
explicitly say "after redeploying with fix version." For hybrid (CLI
+ cloud-server): both must be on the fix version. CLI changes that
add a new wire-shape can wake dormant server code paths (Policy 4's
matrix should cover this CLI×server co-evolution surface).

### Implementation responsibilities

- **All coords** apply Policies 1, 2, 3, 6 at release-readiness gate
  for their repo's releases. Each coord's CLAUDE.md has the
  release-readiness checklist that explicitly verifies each policy.
- **Engineering integrity (Randy)** verifies Policies 2, 3 during
  spec-conformance review on each release.
- **Tom** designs + maintains Policy 5 (staged distribution
  workflow); repo-aweb coordinates.
- **John (repo-aweb)** owns the v0.5.9 hosted-custodial matrix work
  (Policy 4) since aweb is the messaging substrate.
- **Juan** signs off on policy changes; repo coordinators and the
  engineering-integrity owner codify and apply.

## How accountability works

Enoch owns accountability. He reads what everyone says is happening
(status files), then verifies it against reality (git history, outreach
history, Amy's handoff, live health checks, task state). He asks hard
questions and flags discrepancies. He does not manage or do work.

Enoch writes `status/weekly.md`. Everyone reads it.

## Key boundaries

- Direction and engineering integrity both participate in priority
  changes; one area does not override the other.
- Attention proposes content and outreach actions; direction approves
  timing and product fit; humans publish and engage.
- Engineering integrity owns architecture and release risk; direction
  does not make technical decisions alone.
- Accountability asks questions and verifies claims; it does not manage
  or set priorities.
- User feedback talks to users and support-facing agents; other areas
  receive routed feedback.
- Juan and Eugenie publish and engage — agents don't
- John, Tom, Goto enforce product vision in code review — they catch
  invariant violations and stage-inappropriate features that ephemeral
  agents miss
- Coordinators escalate to engineering integrity for cross-repo or
  architectural concerns — they don't make cross-repo decisions alone
- John and Tom communicate directly when OSS and cloud changes affect
  each other

## Status files

Each area maintains a status file that others read.

| File                    | Maintained by | Read by                            |
|-------------------------|---------------|------------------------------------|
| `status/engineering.md` | Engineering integrity | Direction, accountability, attention |
| `status/product.md`     | Direction | Accountability, attention |
| `status/outreach.md`    | Attention | Direction, accountability |
| `status/weekly.md`      | Accountability | Everyone |

## Reaching humans

Juan and Eugenie are on aweb with their own aliases:

```bash
aw mail send --to juan --body "..."
aw mail send --to eugenie --body "..."
```

For urgent issues:

```bash
aw chat send-and-wait juan "..."
```

Humans don't wake up on a schedule. If they don't respond immediately,
that's normal. Write the important context in your mail so they have
full information when they read it.

## When to escalate to Juan

- Architecture decisions that change the product fundamentally
- Disagreements between direction and engineering integrity that they
  can't resolve
- Agents stuck on a wrong path that oversight hasn't caught
- Anything that needs human judgment (partnerships, funding, legal)
- Patterns of concern that the board flags

When in doubt, ask. Juan would rather answer a question than fix a
mistake.

## How engineering works

### Two layers

**Repo coordinators** (John, Tom, Goto) are permanent agents that
live in co.aweb. They read the company docs on every wake-up —
invariants, user journey, vision — and apply that understanding to
code review. They own main in their repos and review every significant
commit.

**Ephemeral coding agents** live in worktrees of the code repos. They
get spun up, do work, and are replaced. They don't read co.aweb docs
directly — the coordinators are the product-aware layer that catches
design mistakes.

### Current dev agents (ephemeral)

| Repo      | Agents                                      | Overseen by |
|-----------|---------------------------------------------|-------------|
| aweb      | dave (coordinator), henry, ivy (developers) | John        |
| ac        | alice (coordinator), bob (developer)        | Tom         |
| aweb/awid | (shared with aweb agents)                   | Goto        |

The engineering-integrity owner checks cross-repo alignment across
coordinators. The coordinators review repo work. This is not people
management; it is responsibility-area verification.

### Cross-coordinator dispatch and lane discipline

Each dev-agent works in one repo under one coordinator. Cross-repo
work routes through the coordinator who owns that repo, not directly
to the dev. When Juan or Randy say "ask X to do Y" and Y is in repo R,
the coordinator who owns R is briefed; that coordinator dispatches X.

Two cases when a dev appears to need to cross repos:

- **Authorized cross-coord borrow**: Juan or Randy can authorize one
  coordinator to lend their dev to another coordinator's lane for a
  specific scope. The borrowing coordinator becomes the dev's
  reviewing coord for that scope. Reviews, gate-runs, and approvals
  follow the borrowing coord's discipline. The dev's home-coord
  steps back from that scope until the borrow ends.
- **Insight transfer without code**: when a dev has context from
  prior work that would benefit another coord's dev, the insight
  travels as text (writeup describing observations, no code, no
  patch references). The receiving coord weighs it against their own
  dev's independent surface walk. This keeps the lane intact AND
  captures the signal.

When redirecting a dev away from another coord's lane, **use
prohibition language explicitly**: "do not touch repo X" is
unambiguous; "stand down on aala.10" can be misread as "finish
current scope, then continue with your original plan." State the
prohibition, the alternative path, the lane owner, and the cost of
crossing. (Memory: feedback_prohibition_language.md.)

### The 2+2 rule

Every substantial effort needs builders and reviewers. For engineering,
that means implementation plus code/release review. For company work,
it means proposer plus approver, writer plus reviewer, or support
classifier plus product reviewer. Agents building alone produce wrong
things. This was learned the hard way.

### Code repos

Repos are at sibling paths on the same machine:
- `../aweb` (OSS: server, CLI, awid, channel, docs)
- `../ac` (Cloud: auth, billing, dashboard, SaaS)

Permanent agents can read these repos freely but must not run `aw`
from them (that would use a different workspace identity).
