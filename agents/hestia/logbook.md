# Hestia Logbook

Dense narrative history. Append a new dated section at the top
whenever state changes meaningfully — release waves, incidents,
discipline banked, lessons learned, customer-activity reads, etc.
Each entry is a snapshot at that moment, not a rolling rewrite.

## 2026-06-10 — aw 1.26.14 ship: aweb-aaqi 3-bug stack closed; release-gate-halt-then-resume pattern exercised

### Arc summary

Bug-stack escalation from Juan's aaqe.7 identity-creation attempt
ran the full cycle in one session: Juan's repro → Hestia routes
to Athena → Athena relays Juan's "Olivia/Mia" direction → Olivia
fixes TDD-style with Juan's repro as test cases → Mia + Athena
clearance → merge to main → Hestia release-cli gate → halt on
unrelated conformance vector failure → Athena patches → resume
→ aw 1.26.14 verified-live on npm + GH Releases.

### Sequence

- Juan at terminal hit 3 bugs in aw 1.26.8 trying to provision
  ama identity from his co.aweb checkout on the Hetzner box:
  (1) /v1/connect 422 on repo_origin SSH-alias rejection;
  (2) refusing to overwrite existing .aw/signing.key after the 422;
  (3) DID mismatch after rm -rf .aw/ and retry.
- Juan corrected initial framing: ALL identities are repo-
  independent, not just --global. The CLI should never send
  repo_origin to /v1/connect.
- Routed to Athena urgent (msg 5bed9a81).
- Athena relayed Juan's direction: route to Olivia with Mia as
  reviewer (dev-team P0 aweb-aaqi). Hestia forwarded full repro
  to juan.aweb.ai/olivia (msg e236009c); mia 403'd cross-namespace
  first-contact, so Olivia loops Mia.
- Olivia implemented TDD-style with verbatim repro as test cases.
  Key insight on bug 3 (her framing): deleting key after
  successful workspace init manufactures the mismatch; right fix
  is preserve resumable partial-init AND fail deterministically
  for already-registered names.
- Mia approved d0dcb080. Athena architecture-reviewed, no
  blockers. Mia's O2/O3 follow-ups folded as 70c2395a. Merged to
  origin/main.

### Release-gate halt + resume pattern

- Bumped server/pyproject.toml 1.26.13 → 1.26.14, uv lock clean.
- Ran release-cli skill's prescribed gate (cli/go tests on
  cmd/aw, chat, awid, run, internal/conformance).
- FAIL: TestA2AAWIDPublicationVectors — got − want =
  {a2a_identity_key_history_invalid}. Pre-existing on main from
  Grace's A2A refresh wave (#265 2429c7ff added the conflict code
  to the source set without updating the test vector). NOT from
  aaqi.
- HALTED release per pristine-test-output discipline. Mailed
  Athena (msg 0bbe76a6).
- Athena confirmed code change is intended; provided one-line
  test-vector patch (commit shape: cb9fb8cf "test: sync A2A
  publication conformance conflict codes").
- Hestia applied patch via Edit; gate green on 2nd run (all 5
  packages pass). Conformance commit cb9fb8cf landed on origin/main
  during Hestia's gate run (Athena or her relay pushed; matched
  Hestia's applied patch byte-for-byte).
- Release bump commit 4518c85c pushed to origin/main.
- Tag aw-v1.26.14 created via make release-cli-tag, pushed via
  make release-cli-push (banked policy #7 individual push).
- GHA workflow 27270197173 (aweb 'aw Sync and Release') success.
- Downstream awebai/aw workflow 27270207737 success: goreleaser +
  npm publish.
- npm: @awebai/aw@1.26.14 live.
- GitHub Releases v1.26.14 published 2026-06-10 10:35:05 UTC.
- aw upgrade smoke: local 1.26.13 → 1.26.14 clean, no resolver lag.

### Mail-send foot-gun (banked)

Parallel `aw mail send` calls to multiple recipients (background
& wait pattern) tripped a CloudFlare/anti-bot block (648KB HTML
"Blocked" page returned). Serial sends went through cleanly.
**Bank: send mails serially when batching to multiple recipients,
not in parallel via shell job control.** Wins: no rate-limit
trip, clean message_id capture per send.

### Coordination

- Mail to Athena (msg 42ebbc4b): verify-live + aaqi closure.
- Mail to Olivia (msg 0186b9db): verify-live + her TDD fixes are
  live on npm.
- Mail to Sofia (msg 9219e97c): verify-live + framing.
- Sofia ACK (msg 0770a93a): carrying as verified-live and
  forward-looking — connect rollback/recovery fixed for NEW
  attempts; existing global identity orphan rows still need
  controller-signed AWID DELETE or admin override. aaqe.7
  pi.aweb.ai/ama still blocked on Juan's orphan cleanup.

### Banked discipline

**Release-gate halt-then-resume shape.** When a test gate fails
on something unrelated to the release's own changes:
1. HALT the release (no tag, no push).
2. Mail the unit owner with: failure shape, suspected source
   commit, no-ship rationale, what's local-uncommitted.
3. Wait for owner-provided fix shape (commit/patch/regen
   instructions).
4. Apply, re-run the gate cleanly, resume the release.
This is a recipe instance of standing policy "ALL TEST FAILURES
ARE YOUR RESPONSIBILITY — never ship with red tests, never
delete the failing test, raise with the owner."

### Next-move-if-resumed

1. aaqe.7 pi.aweb.ai/ama orphan cleanup: still pending Juan's
   option-1 go (controller-signed AWID DELETE + #271 server-side
   soft-delete). aw 1.26.14 makes the failure shape cleaner but
   doesn't auto-recover registered identities.
2. #266 Render visit still pending Juan.
3. Watch for Olivia's namespace-ready ping for aaqe.7 (Pi runner
   lane setup once identity provisioned cleanly).

---

## 2026-06-10 — Pepe orphan reviewer-65e1331 server-side cleanup (Athena mail 43e19f14)

### Arc summary

Customer a2am/Pepe ran pre-fix teardown (rm'd local home before
`aw workspace delete` returned 0), leaving an orphaned ephemeral
reviewer workspace with no local `.aw` for retry. Athena asked
for server-side cleanup. Single rogue row; #245 risk shape (any
soft-delete of agent+workspace rows). Mitigation: belt-and-
suspenders WHERE clauses (agent_id + alias + team_id +
workspace_path + deleted_at IS NULL); sanity gate pre-execution;
post-commit verify newer reviewers untouched.

### Verify trail

- Probe: team_probe.py for default:pepe.aweb.ai confirmed the
  orphan shape exactly (agent_id=a25c55e2-..., alias=reviewer-65e1331,
  hostname=athenea.home, workspace_path=/Users/pepe-reyero/a2am/agents/instances/reviewer-65e1331,
  deleted_at=NULL). Two NEWER reviewers (reviewer-067408e,
  reviewer-da2ef3a) post-fix daa7cbf existed and were marked
  do-not-touch.
- Sanity gate (alias + team_id + workspace_path + deleted_at IS NULL)
  passed.
- UPDATE aweb.agents → `UPDATE 1`. UPDATE aweb.workspaces →
  `UPDATE 1`. Transaction-wrapped, committed.
- POST: both rows deleted_at=2026-06-10 09:23:50 UTC.
- Untouched re-verify: newer reviewers deleted_at still NULL.
- aweb.agents.address was NULL — no AWID DID registered, so no
  registry-side delete needed.
- aweb.agents/workspaces 1:1 (workspace_id == agent_id).

### Banked lesson

**Belt-and-suspenders WHERE clauses + sanity gate + transaction
+ post-verify is the right shape for #245-class one-off
cleanups.** Each WHERE clause is independent evidence of target
identity (agent_id, alias, team_id, workspace_path); a wrong-row
delete would require ALL of them to coincidentally match a
different row, which is impossible for the unique target. Adding
to the runbook as an explicit pattern would be premature (Athena
is landing aweb-aaqg platform gap that should obviate one-off
cleanups). If aaqg doesn't fully cover, formalize then.

### Coordination

- Replied to Athena (msg fa5c9178) with full pre+post evidence
  + #245 mitigation framing + offer to route similar one-offs
  through same chain unless she formalizes a dashboard/API.
- Task #271 closed.

---

## 2026-06-10 — Olivia site deploy f4c0fec3: hero copy fix closes ami.aweb.ai/pi defect; pi.aweb.ai ownership picture; runbook discipline #14 banked

### Arc summary

Two-line copy fix from Olivia: hero terminal example + /llms.txt
mirror swap from the 404ing ami.aweb.ai/pi to aweb.ai/aida (a
real teammate confirmed pre-commit by Olivia's cross-team reply
round-trip). Closes the hero-defect half of aweb-aaqe.6.

In parallel, Juan asked (via Olivia msg 5e69b3a4) for ownership
picture on pi.aweb.ai for the aaqe.7 identity-creation step.
Answered: pi.aweb.ai is not registered at AWID, has no DNS
delegation, and is ours to claim as the aweb.ai controller.
Sofia direction (msg 6b558f88) then settled aaqe.7 itself: stay
with aweb.ai/aida, drop the ami/pi provisioning thread, real
teammate > synthetic greeter.

Sofia banked the operational discipline that surfaced from this
arc as a copy-review checklist line; I mirrored it as standing
policy #14 in the Hestia runbook plus added a Site row to the
Verified-live probe pattern table.

### Verify trail (2/2 PASS + intra-team attestation)

- `make deploy-site` from ac main f4c0fec3 → push 7c5d2dcd..f4c0fec3
  main → deploy-landing. Render rebuilt by 08:43:10 UTC.
- Item 1 (home hero terminal): rendered command
  `aw chat send-and-wait aweb.ai/aida ...`; zero 'ami.aweb.ai'
  anywhere on the page.
- Item 2 (/llms.txt mirror): same. Zero 'ami.aweb.ai' anywhere.
- Intra-team attestation: I'm aweb.ai/hestia (same team as aida),
  so my probe is intra- not cross-team. Ran the exact-as-taught
  command shape:
  `aw chat send-and-leave aweb.ai/aida "hestia verify probe ..."`
  → "Message sent to aweb.ai/aida". Confirms resolve+accept layer
  works as copy teaches (the layer that was broken for
  ami.aweb.ai/pi).
- Sofia's independent spot-check (msg 6b558f88): noted a transient
  stale-edge hit on /llms.txt inside the s-maxage=300 window, gone
  on cache-busted re-probe. Worth remembering: probe within 5
  minutes of deploy with cache-bust query string, or wait out
  s-maxage.

### pi.aweb.ai ownership investigation

- `aw id namespace pi.aweb.ai` → `Status: fail / Error:
  target.not_found`. Not registered at AWID.
- `curl https://api.awid.ai/v1/namespaces/pi.aweb.ai` →
  `{"detail":"Namespace not found"}`.
- `dig pi.aweb.ai` → no NS / A / TXT records. Undelegated
  subdomain of aweb.ai.
- aweb.ai controller is did:key:z6Mkgpop9yzY4dK8MA8CgUZevCsNxsAWP4ThHTASKkZsEuVn
  (Juan/ours). As that controller, full authority to register
  pi.aweb.ai.
- No external owner / DNS delegation / AWID registration.
- Adjacent finding: aweb.ai/ama already exists at the registry,
  registered 2026-05-02 08:05:06 UTC, did:aw:28zhbe9P4yS3c9FsKZrBub4SwiDs,
  log seq 1 (single register_did event, never updated). Existing
  alternative if direction prefers it.
- Mailed Olivia (msg 6356d09c) with the full picture.

### Sofia direction settled

Sofia (msg 6b558f88) chose: stay with aweb.ai/aida in the hero
copy; drop the ami/pi provisioning thread; real teammate
answering first-contact chats is stronger proof than a synthetic
greeter, signal lands with Support where it belongs. Revisit
only if hero traffic makes aida's inbox noisy — aweb.ai/ama is
the fallback then. Juan's pending provisioning question is moot
in this branch; Sofia is telling him in session. aweb-aaqe.7
deprioritized.

### Banked discipline — runbook standing policy #14

Source: Sofia mail 499c13cd + 6b558f88 (2026-06-10), my runbook
addition.

> Anything named in marketing/first-touch copy must resolve AND
> respond (or exist and serve) at verify-live time, probed from
> a customer-shaped position. Any address, identity, command, or
> external artifact named in customer-facing copy must be
> verified to (a) resolve / exist via probe (aw id namespace,
> aw mail send, npm/PyPI version page) AND (b) respond / serve
> (chat or mail round-trip, command run from a clean shell,
> artifact returns expected content). Probe from a
> customer-shaped position — same team if intra-, separate team
> if cross-, never assumed from source. Same standing as the
> released-commands rule (published artifact ≠ deployed service;
> copy ≠ live behavior). Applies on every site/marketing deploy
> where a customer-paste claim appears.

Sofia mirrors as a copy-review checklist line on her surface so
it's enforced review-time as well as verify-time. Also added a
Site row to the Verified-live probe pattern table referencing #14.

### Coordination

- Mailed Olivia (msg 6356d09c): verify-live 2/2 + pi.aweb.ai
  ownership.
- Mailed Sofia (msg 8a838019): verify-live 2/2 + ami/pi half
  closure + discipline.
- Sofia ACK (msg 499c13cd) banked the discipline.
- Sofia direction (msg 6b558f88) closed aaqe.7 direction; spot-
  checked f4c0fec3 independently; noted s-maxage=300 stale-edge
  pattern.

### Direction update (later same day, msg 3ffd1fbb)

Juan reversed Sofia's aaqe.7 deprioritization in session with
Olivia. New sequence:

1. Juan registers pi.aweb.ai fresh (controller authority).
2. Identity pi.aweb.ai/ama created.
3. Olivia drafts greeter soul.
4. **Hestia lane**: persistent Pi runner bound to
   pi.aweb.ai/ama. Shape like a2a.aweb.ai gateway service
   (container image + env config + Render web service + DNS +
   verify resolve+respond before copy flip).
5. Hero copy flips to pi.aweb.ai/ama only after policy #14
   verify-live (outside-team send-and-wait) clears.

Adjacent clarification on aweb.ai/ama: NOT a stale registration
as the "log seq 1, single register_did event" data suggested.
It IS a LIVE agent — replied to Olivia's probe within a minute.
Scope: external inbound proxy for YC/investors/press; Makespace
demo 2026-06-04. Juan was shown the name collision with the new
pi.aweb.ai/ama and KEPT pi.aweb.ai/ama anyway — different
namespace, different scope, intentional collision. Existing
aweb.ai/ama untouched.

Bank: **AWID log-seq alone is not sufficient proof of
liveness.** Log seq 1 only means one registration event, which
is the normal steady state — the agent could be live, idle,
gone, or proxying external traffic. Verify liveness requires a
probe (mail/chat send) and inspection of the response shape.

Direction-mail to Sofia (msg 6280dcf3) re-syncing her direction
posture with Juan's decision: aaqe.7 progresses; hero copy
stays aweb.ai/aida in the meantime; "real teammate > synthetic
greeter" rule still holds because pi.aweb.ai/ama is designed
AS the greeter teammate, not synthesized.

### Next-move-if-resumed

1. aweb-aaqe.6 remaining: /docs/team-bootstrap.md 404. Still
   pending Juan's Render clear-build-cache + --cleanDestinationDir
   build-command flag (#266). Periodic re-curl until flip.
2. When Render rebuild lands, mail closure to Olivia + Sofia.
3. aweb-aaqe.7 ACTIVE per Juan reversal. Wait for Olivia's
   namespace-ready ping; then draft the persistent Pi runner
   plan (shape: a2a.aweb.ai gateway service) and route to Juan
   for Render deploy authorization.
4. New site/marketing deploys: enforce runbook policy #14 at
   verify-live, in addition to existing checklists.
5. Policy #14 extension worth tracking (no commit yet, banked
   in arc context): verify probe should answer BOTH "is this
   address live?" AND "what's its scope?". Scope-discovery via
   response shape inspection. Will fold into runbook on the
   next verify-live exercise that surfaces this case.

---

## 2026-06-10 — Olivia site deploy 7c5d2dcd: wake-setup restore 3/3 verify; ami.aweb.ai/pi 404 banked as live-defect P1 (pre-existing on f528b366)

### Arc summary

Olivia's third site change of the cycle. Restores per-runtime
wake-setup content (Claude Code + Codex + Pi) that had dropped
out of the home Skills section, and reorders /llms.txt to match
HTML. Deploy ran clean; verify-live 3/3 PASS.

In the verify-live framing review, Sofia caught a customer
first-touch defect in the hero terminal default panel: the
example command `aw chat send-and-wait ami.aweb.ai/pi "hello
over there"` references an address that doesn't resolve. I
independently confirmed via `aw mail send` probe:

```
aw mail send --to ami.aweb.ai/pi --subject probe --body probe
→ resolve recipient "ami.aweb.ai/pi" for signed mail:
   aweb: http 404: Namespace not found
```

This defect is PRE-EXISTING on f528b366 — it landed in yesterday's
hero-intent-tabs commit, not 7c5d2dcd. Direction (Sofia + Olivia
+ Hestia aligned): ship 7c5d2dcd as-is (no regression here),
treat ami.aweb.ai/pi copy as follow-on P1.

### Verify trail (3/3 PASS)

- `make deploy-site` from ac main 7c5d2dcd → push
  00838640..7c5d2dcd main → deploy-landing. Hugo built 51 pages,
  33 static, 2 aliases, 0 cleaned. Render rebuilt by 08:17:03 UTC.
- Checklist 1/3: id="start-your-agent" anchor renders; "Start
  your agent" heading; claude --dangerously-load-development-channels;
  Codex CLI present; @awebai/pi@latest install present.
- Checklist 2/3: hero terminal panel foot shows "Wake setup ↓"
  and "Two agents talking →" both rendered.
- Checklist 3/3: /llms.txt top-level section order matches spec
  exactly: Get started — pick where you work / What aweb does /
  Team quickstart / Start your agent / Under the hood / Two
  paths to identity / Claude.ai · ChatGPT.com · Claude Desktop /
  Multi-agent coordination / Pricing / Start building with aweb.

### Defect investigation: ami.aweb.ai/pi

- Sofia's framing-review caught it; she ran `aw chat send-and-wait
  ami.aweb.ai/pi` and got resolve 404.
- Hestia independently confirmed via `aw mail send` probe — same
  resolve 404 ("Namespace not found").
- Routed to Olivia via msg 416cfcd7 with the verify command +
  Sofia's option-1/2/3 framing.
- Olivia (msg 7fd9d685) ACK'd defect ownership: "verified
  command surface was released but never that the example address
  resolves — same lesson as verify-cli-surface, one layer deeper
  (addresses are claims too)". She probed candidates:
  - ami.aweb.ai/pi: 404
  - demo.aweb.ai/support: 404
  - aweb.ai/hello: 404
  - aweb.ai/aida: RESOLVES + accepts mail (probe 63e89b4e),
    reply behavior unconfirmed.
- Olivia routing option 1 (provision ami.aweb.ai/pi as live
  greeter) to Juan.
- Sofia preference order:
  1. Provision ami.aweb.ai/pi as real responding agent (best —
     makes hero promise literally true, zero copy change).
  2. Swap to live-responding address (only if comfortable making
     it customer-paste target).
  3. Make unambiguously placeholder (weakest, safer than 404).

### Banked discipline (pending Sofia settle)

**Pre-deploy verify must extend to addresses named in marketing
copy.** Any DID or `<namespace>/<agent>` shown in customer-facing
material must (1) resolve and (2) respond at verify-live time,
same standing as the released-commands rule. Banked once the
ami.aweb.ai/pi fix shape settles — Sofia explicitly chose not to
write the discipline mid-flight while options are still in play.

### Coordination

- Mailed Olivia (msg 904fb07a) + Sofia (msg b63b2602) with
  7c5d2dcd 3/3 PASS evidence + the defect-routed status.
- Sofia ACK (msg 00b335d8): records 7c5d2dcd verified-live 3/3
  for wake-setup; aweb-aaqe.6 stays open because two holds
  remain; do not package site/hero as a distribution beat until
  both close.

### Next-move-if-resumed

1. Re-curl `/docs/team-bootstrap.md` periodically; expect 404
   once Render clear-build-cache + `--cleanDestinationDir` lands.
2. Watch for Olivia's copy fix iteration on the ami.aweb.ai/pi
   defect. If Juan provisions ami.aweb.ai/pi, run the standing
   probe (`aw mail send --to ami.aweb.ai/pi`) and confirm
   resolve+respond before closing.
3. aweb-aaqe.6 closes when BOTH holds clear: /docs/team-bootstrap.md
   404s AND hero terminal panel teaches a working flow (live
   greeter resolve+respond OR explicit placeholder OR swapped
   address with verified resolve+respond).

---

## 2026-06-10 — Olivia site deploy f528b366: hero intent tabs verified-live 3/3 (Playwright-measured no-layout-shift)

### Arc summary

Olivia's second site change in two days — three-tab intent
switcher [In your terminal | As a team | In your browser] in the
home hero card. Rose-reviewed b0907441 + Juan design-approved.
Batches naturally with yesterday's still-pending Render clean
rebuild for /docs/team-bootstrap.md: one Render clear-build-cache
settles both waves.

### Verify trail

- `make deploy-site` from ac main f528b366 → sync commit 00838640
  → push 2facc1e1..00838640 main → deploy-landing clean.
- Hugo built: 51 pages, 33 static files, 2 aliases, 0 cleaned.
- Render rebuilt by 08:07:17 UTC (verified via last-modified on
  fresh paths).
- Checklist 1/3: pill toggle [In your terminal | As a team | In
  your browser] all three labels rendered; default-terminal panel
  has 'npm install' + 'aw init' (3 hits each).
- Checklist 2/3: Playwright-measured layout-shift across tab
  switches:
  * Hero `<section>` = 1200 × 646.75 across all 3 tab states (0px
    delta).
  * Panel container `.hero-code--intent` = ~442px pinned
    (terminal 442.0, team 442.4, browser 442.0; <0.5px subpixel
    jitter).
  * Individual visible panel content varies 232–323px but
    container clamp absorbs.
  * Confirms commit's "Card height pinned so tab switches don't
    shift layout" claim.
- Checklist 3/3: /llms.txt has 'Get started — pick where you
  work' heading + ### In your terminal / ### As a team / ### In
  your browser panel headers in tab order.
- ARIA tablist semantics (commit claim): VERIFIED. 1
  `role=tablist`, 3 `role=tab` (1 `aria-selected=true` on default
  terminal, 2 `aria-selected=false`), 3 `role=tabpanel`, 3
  `aria-labelledby` cross-refs.
- Adjacent yesterday hold: /docs/team-bootstrap.md still
  last-modified Mon 2026-06-08 — Render hasn't done the
  clear-build-cache yet.

### Banked lesson

**Hugo `--minify` strips attribute quotes per HTML5 spec.** When
curl-probing for ARIA / role / data-* attributes, use a
quote-optional regex: `role="?tablist"?` not `role="tablist"`.
Earlier today's first probe scored 0 ARIA hits and looked like a
defect; the markup was correct, my regex was wrong. Verify
infrastructure contract before debating policy is the meta-rule;
verify regex behavior on minified output is its corollary for
site verify-live.

### Coordination

- Mailed Olivia (msg 870b866d) + Sofia (msg 21a86223) with
  3/3 PASS evidence + the yesterday hold reminder.
- Sofia ACK (msg 6ec5ca1a): carries f528b366 verified-live;
  team-bootstrap.md cleanup not fully closed until post-rebuild
  curl confirms 404.
- Task #267 tracks the f528b366 wave; #266 still pending Juan's
  Render-side fix.

### Next-move-if-resumed

1. Re-curl `/docs/team-bootstrap.md` periodically; expect HTTP
   404 once Render clear-build-cache lands.
2. Mail closure to Olivia + Sofia with the post-rebuild evidence,
   closing aweb-aaqe.6 and #266.
3. No further Hestia action on this wave — Juan owns the Render
   dashboard step.

---

## 2026-06-09 — Olivia site deploy 2facc1e1: 5/6 verified-live, Render publish-dir staleness banked as #266

### Arc summary

Cut Olivia's blueprint-voice site deploy from ac main 2facc1e1
("blueprint voice for home hero, teasers, and docs redirect").
Five of six checklist items verified live on aweb.ai cleanly.
Sixth item (/docs/team-bootstrap.md should 404) blocked on
Render-side publish-dir staleness — file deleted from source +
Makefile sync list, local Hugo build doesn't include it, deploy-
landing tree at 2facc1e1 has no team-bootstrap.md anywhere, but
Render still serves the 15KB file with prior-sync mtime. Other
paths show fresh today's mtime. Root cause: Render's publish dir
not cleaned between builds.

### Sequence (all 2026-06-09)

- `make deploy-site` ran clean from ac main 2facc1e1 → built
  Hugo locally (51 pages, 33 static files, 2 aliases, 0 cleaned),
  push 7203f5c2..2facc1e1 main → deploy-landing landed.
- First probe at +30s after deploy: CF Pages still serving stale
  Hugo build (`Hugo 0.124.1` in generator meta), all 6 items
  showed pre-deploy state.
- Second probe at +120s: Render rebuilt. 5/6 items green:
  * Home hero: "Create a team · from a blueprint" present;
    runtime-toggle / hero-runtime CSS classes absent.
  * /mcp: "Create your team from a blueprint" present.
  * /docs/team-bootstrap/: Hugo meta-refresh alias page with
    `<link rel=canonical href=https://aweb.ai/orchestration/>` +
    `<meta http-equiv=refresh content="0; url=https://aweb.ai/orchestration/">`.
    Body has no team-bootstrap content. Olivia ACK: meta-refresh
    acceptable for static host, no hard 30x expected.
  * /llms.txt: 0 "aw agents bootstrap", 7 "blueprint" hits.
  * /mcp/llms.txt: 0 "aw agents bootstrap".
  * Docs sidebar: 0 "Bootstrap a repo-local aweb team" listings.
- 6th item gap: `/docs/team-bootstrap.md` HTTP 200, content is
  full original markdown, `last-modified: Mon 2026-06-08 07:17:01
  UTC` (prior 7203f5c2 sync commit timestamp). Other paths show
  `last-modified: Tue 2026-06-09 22:10:31 UTC` (today's build).
- Source-side audit confirms file genuinely absent:
  * 2facc1e1 deleted `site/static/docs/team-bootstrap.md` (459
    lines per `git show --stat`).
  * Makefile diff removed `team-bootstrap.md` from
    `AWEB_PUBLIC_DOCS` AND `AWEB_HUGO_DOCS` lists.
  * `sync-public-docs` target does `rm -f
    "$(AWEB_STATIC_DOC_DIR)"/*.md` then re-copies AWEB_PUBLIC_DOCS
    — so it won't recreate team-bootstrap.md.
  * Local `ls -la ac/site/static/docs/` and `ls ac/site/public/docs/`
    both have no team-bootstrap.md.
  * `git -C ac ls-tree -r origin/deploy-landing | grep team-bootstrap`
    returns empty.
- Conclusion: Render's publish dir is incremental — files removed
  from source persist in published output. Render's build command
  for aweb.ai static site likely does `hugo --minify` without
  `--cleanDestinationDir`.

### Coordination

- Mailed Olivia (juan.aweb.ai/olivia, msg 6a216fcc) with full
  verify-live report + Render-side hypothesis + ask for Juan
  Clear-build-cache & deploy.
- Mailed Sofia (aweb.ai/sofia, msg 03056d2f) with same +
  framing-review request.
- Tried Juan via `juan`, `juanre`, `juan.aweb.ai/juan`, `aweb.ai/juan`
  — all 404. Sofia replied she's in session with Juan and
  surfacing the Render clear-cache ask directly.
- Olivia replied (msg d51a5424): confirmed /docs/team-bootstrap.md
  should hard 404 (no stub — it was agent-facing copy for
  superseded flow, canonical legacy reference stays in aweb repo);
  meta-refresh acceptable; +1 on #266 Makefile pre-clean as
  durable fix.
- Sofia replied with framing-pass (msg 2c415cd9): mail names
  what-fixes / what-doesn't / evidence chain, all good; she
  independently re-curled and grepped to confirm; will close
  HOLD-B (site setup-framing) once stale .md confirmed gone; +1
  on #266 Makefile pre-clean.
- Sofia second reply (msg 7245b58e): confirmed live hero teaches
  blueprint prompt + aw commands all in released 1.26.8, so
  HOLD-B substance is resolved pending the post-rebuild check.
- ACK'd Sofia (msg 65bb8b26) with closure-condition: post-rebuild
  curl routed to her + Olivia, then HOLD-B closes; Makefile
  pre-clean diff prepped after verify closes.

### Banked discipline

- **Olivia's address is `juan.aweb.ai/olivia`** (cross-namespace
  form). Short `olivia` 404s, `aweb.ai/olivia` 404s. Memory
  already had this; verified again.
- **Juan's aw alias not reachable via short forms.** Loop through
  Sofia when she's in session; else Juan@aweb.ai direct.
- **Render publish-dir staleness is real.** Site-deploy verify-live
  must specifically re-curl URLs of REMOVED static files, not just
  ADDED/MODIFIED ones. Banked as task #266; #266's fix is Makefile
  pre-clean of publish dir before hugo build (both Olivia + Sofia
  +1; doesn't depend on Render config staying correct).

### Task created

- #266 Render publish-dir stale for removed-from-source static
  files (aweb.ai). Pending Juan's Render Clear-build-cache & deploy
  first, then Makefile pre-clean diff lands as the durable fix.

### Next-move-if-resumed

1. Re-curl `https://aweb.ai/docs/team-bootstrap.md` periodically
   until 404 or fresh mtime.
2. Mail Olivia + Sofia closure with the post-rebuild evidence.
3. Cut Makefile pre-clean diff (rm publish dir before hugo) under
   #266 — prep in a branch, mail Athena for review before push.

---

## 2026-06-08 — a2a-gw v1.26.9 lane: image banked, manual-deploy abandoned, pivot to AC-managed gateway

### Arc summary

Full release-chain ran from gate-review through tag-push through
GHCR build through Render Web Service creation. Manual-deploy lane
collapsed at the workspace-state delivery question. Grace pivoted
mid-arc to AC-managed gateway as the product path. Image +
infrastructure stay banked at 66b0e70c; nothing rolled back; no
identity provisioning was started; no controller keys touched.

### Sequence of events (all 2026-06-08)

- Grace pushed bab02eb1 (initial gateway container release + e2e)
  for review. Hestia reviewed: APPROVE structural shape, flagged
  2 P1 gaps (gateway identity provisioning subsection missing;
  /health AWID version-floor advertisement-only, not enforced), 1
  P2 clarification (narrow-gate caveat), 1 decision-confirm
  (Render not Hetzner).
- Grace pushed 66b0e70c with fixes folded credibly: new "Gateway
  Identity Provisioning" runbook subsection (creation, team-cert,
  smoke, AWID publication, gateway.yaml template, Render delivery,
  rotation, compromise procedure), /health Compatible+MinimumVersion
  enforcement with 503 on missing/old AWID, narrow-gate caveat, Render
  decision banked with "Hetzner needs a separate reviewed runbook"
  caveat. e2e bumped 30→33 tests for compatible/minimum/version
  assertions.
- Mia cleared 66b0e70c per Grace relay a5330b8d (Mia review
  request ef106835 was delivered via Grace's mail path).
- Hestia drove release chain at 66b0e70c:
  - branch main / tree clean / no existing a2a-gw tag / Docker up /
    CLI_VERSION=1.26.9 (from SERVER_VERSION coupling, #219 debt)
  - make release-a2a-gateway-check: go tests (4 packages green) +
    production Docker build + in-container --check + real-backend
    Docker e2e PASS 33/33 in ~10 min
  - make release-a2a-gateway-tag: a2a-gw-v1.26.9 at 66b0e70c
  - make release-a2a-gateway-push: tag to origin
  - GHA workflow 27129622205 "A2A Gateway Release (GHCR)" SUCCESS
    in 4m19s — multi-arch image at ghcr.io/awebai/a2a-gateway:1.26.9
    + :latest
- Juan created Render Web Service for the image at 15:46 UTC. Image
  pulled clean (no GHCR auth issue). Container started clean. Exit
  status 1 with `open /config/gateway.yam: no such file or directory`
  — Juan's env-var typo (missing trailing `l` on gateway.yaml).
- Typo fixed; second deploy also exit-status-1 with the corrected
  `gateway.yaml` path — expected, because no config or workspace
  was mounted yet.
- Hestia mailed Grace 86e2be87 surfacing the v1 workspace-state
  delivery question: (a) Render Secret Files read-only, (b) Persistent
  Disk + Render Shell seeding, (c) Dockerfile entrypoint tarball
  expansion in a fresh patch release.
- Grace mail 020fc0bc picked (a)-with-tarball: Render Secret Files
  for gateway.yaml + base64 tarball + command-override doing
  `base64 -d | tar -xz` at startup. Validated /bin/sh, base64, tar,
  mkdir present in the 1.26.9 image. Code-checked gateway workspace
  state is read-only at runtime (only writable thing is optional
  audit JSONL).
- Hestia asked two clarifying questions (team-naming + cert-path
  relative/absolute). Grace mail 9765e48a answered: dedicated NEW
  team; cert paths are RELATIVE (SaveTeamCertificateForTeam writes
  `team-certs/<encoded>.pem`; runtime resolves as
  `<workspace_dir>/.aw/<cert_path>`). Tarball: `tar -czf - .aw |
  base64 > gateway-workspace.tgz.b64`. Exclude controller keys +
  human workspace state. Pre-tarball verify: grep `cert_path` is
  relative `team-certs/*.pem`, files exist under `.aw/team-certs/`.
- Hestia gave Juan the 16-step provisioning + Render setup table.
  Asked: (1) is `a2a.aweb.ai` namespace controller-prepared? (2)
  team name? (3) where do you run controller-key bits from?
- Before Juan answered, Grace mail 5bf40922 pivoted: "Stop manual
  A2A tarball deploy; pivot to AC-managed gateway." Reasoning: Juan
  not demoing this endpoint, tarball flow not product-quality, only
  useful as temp manual endpoint, hosted customers should not handle
  .aw workspace state or tarballs.
- Hestia ACK'd Grace 54d52f02; closed #263 as banked-infrastructure /
  manual-lane-abandoned. Grace ACK'd that closure ec961791.

### What's banked (NOT rolled back, per Grace's instruction)

- aweb tag a2a-gw-v1.26.9 at 66b0e70c
- ghcr.io/awebai/a2a-gateway:1.26.9 + :latest multi-arch on GHCR
- Dockerfile.a2a-gw + .github/workflows/a2a-gateway-release.yml +
  Makefile release-a2a-gateway-* lane
- scripts/e2e-a2a-gateway-docker.sh (33-test real-backend Docker
  journey)
- docs/a2a-release-runbook.md with Gateway Identity Provisioning
  section, /health AWID-compatible enforcement, narrow-gate
  caveat, Render-decision-banked
- cli/go/awid/registry_resolver.go DNS-bypass fix (TestRegistryResolverEmbeddedFallbackBypassesDNSForAddress)
- /health emits build.release_tag + build.git_sha + aweb_version +
  awid_service_version (floor) + awid_registry{url,reachable,compatible,
  status,version,minimum_version,error} + gateway diagnostics; flips
  to 503 when !reachable OR !compatible

### What's stopped (NO state change in aweb.ai namespace)

- Identity provisioning for a2a.aweb.ai/gateway — not started
- No `aw id namespace prepare-controller`, no `aw id create`, no
  team create, no controller-signed cert, no `aw init`
- No Render Secret Files uploaded, no command override set
- No per-route AWID publication
- No verified-live mail for a2a.aweb.ai

### Render service state

Juan's Render Web Service at slot `a2a.aweb.ai` is in restart-loop
(exit-status-1 on each restart). Configured with only
AWEB_A2A_GW_CONFIG env, no Secret Files, no command override. Per
Grace, leave suspended/stopped; don't delete (slot + DNS may be
reused when AC-managed gateway needs it).

### Lessons banked (not yet promoted to runbook)

1. **Render Secret Files mount as /etc/secrets/<filename> by
   default, read-only.** Useful for config-and-workspace delivery
   when workspace state is read-only at runtime; insufficient for
   anything that writes (audit logs, cert renewal, local outgoing-
   mail spool).
2. **Workspace tarball + command-override is the right v1 for
   read-only workspace state** without recutting the image — IF
   `sh`, `base64`, `tar`, `mkdir` are present in the runtime
   image. Alpine base provides all four. Pattern: secret-file
   `*.tgz.b64`, Render command override does `base64 -d | tar
   -xz` into `/tmp/...`, then exec the daemon.
3. **Manual workspace-state surgery is not customer-product.**
   Useful for temporary live endpoints (founder-demo), not for
   hosted customers. When a manual deploy lane starts requiring
   per-customer tarball generation, namespace-controller
   coordination, and Render Secret File uploads, the right move
   is control-plane managed (AC owns identity + cert + config +
   deploy).
4. **DNS-resolution intermittently times out from this machine to
   *.onrender.com origins** (api.awid.ai + app.aweb.ai both saw
   ~10s context-deadline-exceeded multiple times this session;
   non-Render destinations like github.com and pypi.org resolved
   fine). Likely Render origin cold-start lag in GCP-us-west1.
   Mitigation: retry with longer timeout.

### Live state at end of session

- AC: v0.5.60 prod, aweb 1.26.8 client, awid_service 0.5.10
- AWID: api.awid.ai version 0.5.11 (Grace deployed mid-session)
- PyPI aweb: 1.26.9 (Grace's A2A wave; self-last-verified 1.26.8)
- npm aw: 1.26.9 (Grace's wave; self-last-verified 1.26.8)
- aweb.ai: Olivia 27f43d4c hero redesign live
- a2a.aweb.ai: NOT live — Render Web Service exists but suspended
- a2a-gw image: GHCR 1.26.9 + :latest, banked

### Tracking

#262 closed (review complete). #263 closed (release chain complete
on the banked-infrastructure side; manual-deploy lane abandoned).


## 2026-06-08 — Olivia 27f43d4c site deploy verified-live (post-A2A train + aapz wave 3)

Session pulled across two day-boundary turns (UTC midnight rolled
between deploy and verify-live closure).

### What landed this turn
- ac main: 27f43d4c (Olivia home hero redesign merge into main) +
  7203f5c2 (sync-public-docs auto-commit from `make deploy-site`)
- ac deploy-landing: origin pushed; CF Pages built Hugo from
  6da746de (Wave-3 baseline) then this wave's commit set; live
  H1 confirms new "Let agents work together in an open network"
- AC backend: untouched. /health still
  `release_tag=v0.5.60 git_sha=2cf21f23 aweb_version=1.26.8
  awid_service_version=0.5.10`.
- Mail: verified-live sent to Sofia (msg bd6704cd). Two ACK copies
  back from Sofia (4678a10a + cf60b390 — bus retry, identical
  content). Olivia not addressable via short alias OR
  `aweb.ai/olivia` (404); past pattern was conversation-thread
  reply via her inbound mail.

### Live-verify evidence (cache-bypass `?nocache=$(date +%s)`)
- Home H1: `<h1 class=hero-title>Let agents work together in an
  open network</h1>` ✓
- Bootstrap URL canonical: `github.com/awebai/aweb-team-coord-worktrees`
- Runtime-toggle DOM: `hero-runtime` class present
- /llms.txt headers: `# Let agents work together in an open
  network` / `## Get started` / `### 1. Install + bootstrap
  (one-time)` / `### 2. Start an agent in each agent home` /
  `### Claude Code` / `### Codex CLI` / `### Pi`
- /orchestration: 5 `aw agents bootstrap ... --username
  --identity-prefix` hits
- /mcp: 1 hit (orchestration teaser)
- /docs/team-bootstrap: 12 `aw agents bootstrap` hits, 0 stale
  `aw team bootstrap`, 0 stale `aw run claude`
- Stale-string sweep across home/orchestration/mcp/team-bootstrap:
  all zero

### Lesson banked (not yet promoted to runbook)
CF Pages Hugo build version (0.124.1 in meta generator) is older
than local (0.160.1 here). After `make deploy-site` push, CF
Pages takes ~30s to rebuild from source. First probe right after
push may show OLD content even with cache-bypass param. Wait 30s
and re-probe. (Already banked policy #10 covers browser-verify;
this adds: CF-rebuild-window applies even to curl probes because
CF builds from deploy-landing source branch, not from pre-rendered
output.)

### A2A release train (Grace's lane, ran in parallel)
Grace took the release lane mid-session after Juan's "drive it
through" mandate when I attempted to gate Step 1 with AskUserQuestion.
- Cut at aweb 81e8d01c: AWID 0.5.11 + aweb server 1.26.9 + aw CLI
  1.26.9 + new aweb-a2a-gw gateway binary
- Grace confirmed AWID 0.5.11 deployed mid-session
- AWID 0.5.11 has additive migration 007_a2a_publications.sql
  (a2a_bridge_delegations + a2a_route_publications tables w/
  indexes) — additive-only, no live-schema break for AC's
  awid-service 0.5.10 client lib
- AC backend untouched: still on aweb 1.26.8 client lib +
  awid-service 0.5.10 (backward-compat with api.awid.ai 0.5.11)
- aweb-a2a-gw live deployment (a2a.aweb.ai/personal +
  /customer-service + /research routes) pending future
  ubuntu-8gb-nbg1-1 SSH-assist provisioning per Grace
- I picked up the marketplace push (d6034672) as transport-only
  task — Athena's instance lacks GitHub creds, mine has them.
  Bundle transport via 19-chunk base64 channel mail; extraction
  from on-disk JSONL transcript (in-memory transcription had
  boundary-whitespace risk).

### Single-release-owner discipline confirmed
Grace owns A2A. Hestia carried Olivia site only. Marketplace push
(d6034672) was a transport favor, not a release co-ownership.
When Grace takes a lane under Juan's "drive it through" mandate,
hands off cleanly — don't double-tag.


Future-you reads `handoff.md` first to know what to do NOW. You
come HERE when you need depth on something handoff.md only points
at — a referenced incident, a banked decision, a release wave's
backstory.

Format: `## YYYY-MM-DD <short title>` headers. Most recent on top.
Keep entries chronologically accurate — don't merge old entries
with new context. Write them as point-in-time snapshots so they
remain a faithful record.

---

## 2026-06-07 — aapz HOLD mid-AWID-wave (P1 audit)

Grace handed off aapz aw agents lifecycle release at aweb
0f303786 (9626e66d). 5-surface wave: awid 0.5.10 → aweb 1.26.8 →
skills 0.2.12 → Pi 0.1.20, with AC v0.5.60 floor bump deferred
until v0.5.59 verified-live. Scope verified empirically: awid
1484 LOC, server 43 LOC, CLI 5919 LOC, skills/aweb-bootstrap
canonical drift sha 0a29e68 → 52f4c5b.

Mailed planned versions e92c48d1; Grace green-lit with
corrections (d419d930): tag at bump SHA not 0f303786, migration
path is `awid/src/awid_service/migrations/` not
`awid/src/awid/migrations/`, AC deferral OK with explicit
verified-live mention, skills uses workflow not hand-bump, Mia
is aapz reviewer-of-record (no Athena re-loop). Grace short-form
ACK 8190c796 confirmed.

Executed AWID wave 1:
- awid/pyproject.toml 0.5.9 → 0.5.10 + uv sync
- make release-awid-check: 201 tests passed
- Commit 9e921ecc 'release: awid-service 0.5.10 (aapz wave 1 …)'
- Tags awid-service-v0.5.10 + awid-v0.5.10 at 9e921ecc
- Pushed main + both tags individually (per banked policy)
- GHA awid-service PyPI run 27086928868 success: awid-service
  0.5.10 LIVE on PyPI (2 artifacts)
- GHA awid GHCR run 27086931086 success: Docker image in ghcr.io

NOT executed (HOLD landed mid-flight):
- AWID prod migrations (006_identity_encryption_key_custody.sql)
- api.awid.ai Render redeploy signal
- aweb wave 2 (server 1.26.8 + aw 1.26.8)
- skills 0.2.12, Pi 0.1.20

Grace HOLD (a147126b + 992469cf): Juan challenged proceeding
with aapz.16/.18/.19/.21 open. Disposition:
- KEEP 0.5.10 on PyPI (no yank, no force rollback)
- KEEP GHCR image (workflow already completed)
- KEEP bump commit 9e921ecc + tags on origin/main
- All runtime/deployment steps HELD
- Possible outcome: deployed AWID becomes 0.5.11 post-audit,
  with 0.5.10 as unused artifact — Grace says preferable to
  yank or history-rewrite.

api.awid.ai continues serving 0.5.9 — no production change. PyPI
+ GHCR are registry artifacts only until migrations + redeploy
fire.

Lesson banked (will surface next AWID/aweb wave): peer
green-light at the wave gate ≠ closure on epic P1 audit. Before
tagging+pushing registry-permanent artifacts, re-verify open P1s
in the epic even with explicit wave authorization. The aw 1.26.6
lesson covered 'peer-validation ≠ canonical gate at target SHA';
this is its dual: 'wave green-light ≠ epic ready'.

---

## 2026-06-07 — Pi 0.1.19 verified-live (description colon-led tweak)

Olivia mail 93a16ac6 from aweb b7015275: bump 0.1.18 → 0.1.19
with description revision (em-dash → colon-led list of three
clauses, surfaces 'join agent teams' capability). Juan-authored
description, fast-tracked same as 0.1.18.

Bump commit 2b76c804 narrow (only pi-extension/package.json).
WIP in tree (team_bootstrap.go, docs, skills/aweb-bootstrap) not
swept per Olivia heads-up. Tag pi-v0.1.19 pushed individually,
GHA pi-release run 27086086858 success.

Content-verify against b619aca canonical: description matches
spec byte-for-byte; README byte-identical to
b619aca:pi-extension/README.md (no change since 0.1.18, sha256
bfae6902…); all 5 SKILL.md hashes byte-identical to
b619aca:skills/<skill>/SKILL.md (Wave 5 sync intact).
Verified-live mail ce7ab07e to peers + Juan. Olivia ACK
24384f53, then independent verify-after came back clean.

---

## 2026-06-06 — Pi 0.1.18 verified-live (README + marketplace-card rewrite)

Olivia's mail 07ad3f2c arrived: bump @awebai/pi 0.1.17 → 0.1.18 from
aweb b619aca. Scope: pi-extension/README.md fully rewritten for
cold-reader Pi users (no aweb background) + package.json description
field rewrite ("Lets your Pi communicate with other AI agents on an
open network…"). Juan-authored, greenlit directly — Sofia/Athena
framing review chain bypassed explicitly per author. SKILL.md
content unchanged (Wave 5 sync from aapy still canonical).

Discipline notes captured in flight:
- Olivia called out unrelated WIP in working tree
  (atomic-address-claim, team_bootstrap.go, ratelimit.py,
  dns_addresses.py, registry_register_test.go, cli-command-reference.md
  — none hers, scope-creep risk). I confirmed back: ONLY
  pi-extension/package.json staged for the bump. Verified via
  `git diff --cached --name-only` returning that single file before
  commit.
- Bump commit fba2108 is narrow: 1 file, 1 insertion, 1 deletion.
- Tag pi-v0.1.18 pushed individually (banked policy).
- GHA pi-release.yml run 27061497123 success — sync-skills + build +
  version-check + npm publish.

Content-verify against canonical:
- README.md byte-identical to `git show b619aca:pi-extension/README.md`
  (sha256 bfae69022014f6b1085e49c17210114242e545f4fdd88774e7e70f377a3d21fe).
- package.json description matches Olivia's spec verbatim.
- All 5 SKILL.md hashes (aweb-identity, aweb-team-membership,
  aweb-messaging, aweb-bootstrap, aweb-coordination) byte-identical
  to `git show b619aca:skills/<skill>/SKILL.md`. Wave 5 sync intact —
  Pi tarball still carries the aapy in-repo bootstrap content from
  b78fc79.

Verified-live mail 9d1ff678-e0d5-49c8-84dc-9e0830ff270e sent to
Olivia + Grace + Athena + Sofia + Iris + Aida with 4-point standard
shape (fixed / not fixed / evidence / live check) plus full live
matrix. Olivia (mail 9c8fe60e) ACK'd plan and is standing by to run
her independent verify-after — npm pack + diff README + description
+ 5 SKILL hashes against b619aca canonical — to close.

Marketplace.json (claude-plugins repo) NOT bumped — Pi is not a
Claude Code plugin; only @awebai/claude-channel and
@awebai/claude-skills are. Pi installs from npm direct via Pi's own
extension system.

Task #255 closed.

---

## 2026-06-03 — first external multi-agent customer detected (andi.aweb.ai)

Bertha pinged in chat asking how to reach `andi.aweb.ai/coord`
and `andi.aweb.ai/coord-global` because she was getting connection
errors. Ran `scripts/team_probe.py --team default:andi.aweb.ai`.

**What I found:** the andi BYOT team was registered today
2026-06-03 09:44 UTC with 4 active agents (coord, dev, review,
remoteagent) running on a Hetzner host (ubuntu-8gb-nbg1-1) plus
one remote-machine agent on Theresias-MacBook-Air.local. By
10:13 UTC they had 17 mail + 5 chat messages across 6 active
conversations, with coord ↔ dev coordinating on real tasks
(default-aaaa etc).

**Why this matters:** yesterday's customer-activity reality
check (2026-06-02 logbook entry below) said "External adoption
of the multi-agent value prop is still zero." Today: not zero
anymore. Andi is the first observed external team actually
doing the thing we built aweb for — multi-agent coordination in
production, with a remote agent joining a self-hosted team.

**Why Bertha's connection errors:**
- `coord-global` doesn't exist as an alias on this team. Likely
  a customer-typed typo or a mis-remembered alias. `coord` is
  the right one.
- The team's DNS TXT (`_awid.andi.aweb.ai`) shows
  `dns_status='desired'` in our managed_namespaces row. The AWID
  registry knows what they SHOULD publish, but if the customer
  hasn't put the TXT live on their DNS yet, federated DID
  verification fails and the route returns a connection error.
  Worth retrying after a few hours and/or checking with the
  customer that they've published the TXT record.

**Contact path gap:** all 5 org members of the andi
organization are anonymous cli_signup users with `email=NULL`.
Same shape as the default-aaaj observation (Thanos). We have NO
dashboard-side path to the human behind the namespace. Bertha's
only in-system contact route is federated mail/chat to one of
the agents. If Eugenie needs an out-of-band channel (email,
twitter, GitHub) she needs to source it externally.

**Routing to Sofia + Juan as direction-level signal** (mail
sent in same beat). This changes the "is anyone using aweb"
narrative we held for 24h. Not just a flicker either — they
have a Hetzner instance running, cross-machine federation set
up, real task coordination happening. Worth Iris/Sofia
considering whether an outreach (via the federated mail-to-coord
path) makes sense, or whether to leave them to discover us.

**Banked discipline (new):** the `team_probe.py` script paid
back its banking cost immediately. First wake-up after the
scripts shipped, first probe required, produced the answer in
under a minute. Validates the pattern Juan asked for:
pre-made scripts > one-off `/tmp/probe.py`.

**Aida refinement (mail 3be0742f):** "wait for them to come to
us" isn't ONLY a posture choice — it's the current technical
default. With their `_awid.andi.aweb.ai` in `desired` state and
their org all-anonymous cli_signup, we literally cannot reach
them via federation right now. So when Sofia weighs the
proactive-reach-out question, the framing is "we technically
can't yet" as much as "we're choosing not to." If Sofia later
greenlights outreach, Aida offered her lane (`aweb.ai/aida`,
framed "noticed you're running multi-agent — any setup friction
we can help with?") as the least surveillance-y first-touch
shape: question-about-helping > question-about-us-seeing-their-
activity. Routing option, not a push.

---

## 2026-06-02 — restart-ready snapshot after May 26 → June 2 wave

### Live matrix

- AC: app.aweb.ai/health → release_tag=v0.5.58 git_sha=340122ef
  aweb_version=1.26.1 awid_service_version=0.5.9. **In-flight**:
  v0.5.59 image is in GHCR (run 26767320236 success). Awaiting
  Juan Render deploy + AWEB_CUSTODIAL_E2EE_KEY +
  AWEB_CUSTODIAL_E2EE_KEY_ID env confirm (Grace + Mia
  requirement). Expected post-deploy: aweb_version flips to
  1.26.5. Smoke a hosted custodial E2EE flow after the flip; any
  custodial_e2ee_kek_unconfigured / 500 → bad deploy → roll back.
  Task #248.
- PyPI aweb: 1.26.5 (server-v1.26.5 verified-live 2026-05-28;
  wheel contains migrations/aweb/007_agent_encryption_key_custody.sql
  byte-identical to source).
- npm @awebai/aw: 1.26.4 (E2EE opt-in default, --plaintext
  visible, hosted cert-only add-worktree fix). aw 1.26.3 is the
  carrier of the workspace-cleanup regression (#245); 1.26.4 does
  NOT fix it. Anyone still on 1.26.3 who renames a workspace dir
  risks re-triggering the deletion.
- npm @awebai/claude-channel: 1.4.11 (channel-core local-aw
  decrypt for E2EE awakenings).
- npm @awebai/claude-skills: 0.2.10 (em-dash → colon in
  plugin.json description).
- npm @awebai/pi: 0.1.16 (bundles canonical skill content
  byte-identical to aweb main).
- awid-service: 0.5.9 (PyPI + Docker GHCR, api.awid.ai/health
  green).
- Marketplace pins (claude-plugins): aweb-channel 1.4.11,
  aweb-skills 0.2.10. claude-plugins marketplace.json description
  fields still carry em-dashes; per Sofia those don't load-bear
  (banked feedback_discipline_load_bearing), leave as-is.

### Open holds

#### #245 — aw 1.26.3 cleanup regression (P0 customer impact)

8b55181 added `aw workspace status` cleanup that classifies
workspaces with stale last_seen_at or workspace_path not existing
on disk as "gone local" and DELETEs them server-side. Juan hit
this live on 2026-05-28 with the pmbah team: renamed his
workspace parent dir (pmh → pmbah), the next `aw workspace status`
on Mac.c.is saw /Users/juanre/prj/pmh/... paths don't exist, and
the server soft-deleted coord + dev agents + their workspaces
(review survived first sweep due to ordering luck, was re-deleted
on sweep #2).

Recovery state:
- All 3 pmbah agents (coord/dev/review) + their workspaces
  undeleted via targeted UPDATE (deleted_at = NULL only on rows
  whose deleted_at matched the incident windows 2026-05-28
  10:11:33 and 10:41:20-21).
- workspace_path rewritten to actual current on-disk locations:
  /Users/juanre/prj/pmbah/pmbah/agents/coordinator,
  /Users/juanre/prj/pmbah/pmbah/worktrees/possiblymadebyahuman-{dev,review}.
  Juan-confirmed; should now survive the next sweep.
- Mail data was preserved (22 messages in 2 conversations, both
  active); aweb.messages has no deleted_at column. Chat was never
  used by this team.

Fix-forward shape pending Athena + Mia decision (mail thread
96317ca9): (a) cleanup requires multi-signal gone-evidence not
path-existence alone, (b) prompt before auto-DELETE rather than
silent sweep, (c) gate behind --cleanup flag default off. Not yet
authored. ANY ship targeting cli/go/cmd/aw/workspace* should
explicitly address this.

#### #239 — aw 1.27.0 E2EE-default Phase 2

702ccb7 ("cli: default messaging to e2ee") merged into main via
a3d41ec, then the receive-side (channel 1.4.11 + Pi 0.1.16)
shipped on 2026-05-26. 21928a2 then REVERTED the send-side
default for customer-meeting safety (aw 1.26.2: default plaintext,
--e2ee opt-in). Phase-2 ship of aw 1.27.0 with E2EE-default-on is
gated on customer-adoption signal of 1.4.11 / 0.1.16 receive-side.
Grace owns the adoption-threshold call. Do not tag aw-v1.27.0
without explicit re-route through Grace.

### Recent activity

- 2026-05-28 site restructure (Olivia + Athena tech-ACK):
  home/developers swap (new /mcp page, /developers/ → / alias),
  4-tier pricing port, llms.txt mirrors aligned, tagline drops
  "skip the bottlenecks", "Opt-in E2EE" badges tightened, "For
  developers" prefix removed from home eyebrow, /mcp +
  /orchestration teaser panels added on home. All deployed via
  `cd ac && make deploy-site` from main; all verified-live by
  Olivia. Final SHA on deploy-landing: 92860b93.
- 2026-06-01 default-aaaj observation (banked NEUTRALLY per
  Juan's correction, ref feedback_observation_vs_defect memory):
  CLI signup creates an anonymous cli_signup user (email=NULL)
  unlinked from a matching dashboard user. Thanos Diacakis is the
  evidence (2 unlinked aweb_cloud.users rows for one human).
  Filed as default-aaaj priority=P3 type=task (NOT a defect).
  Aida stood down — no support escalation unless a customer
  reports actual confusion. Artifact:
  artifacts/cli-signup-dashboard-user-gap-20260527.md.
- 2026-06-02 analytics scripts banked under scripts/. See AGENTS.md
  "Analytics & probe scripts" section. Triggered by Juan ("we
  really need to have pre-made scripts for the questions that you
  get from bertha and from me"). Scripts cover: N-day sign-ups,
  per-user behavioral snapshot, multi-agent activity check,
  per-team probe.

### Customer activity reality check

External adoption of the multi-agent value prop is still zero:
- 31 external aweb_cloud.users rows have 2+ active agents.
- 2 of 31 show any cross-agent activity in the past 7 days, and
  both look like Juan's own CLI bootstraps (pmbah for sure; the
  noob<random> slug likely also exploration).
- Bertha (Eugenie's outreach agent) was asking about Thanos +
  Di Huang — neither has heartbeated a workspace since signup;
  0 messages, 0 tasks.

This is product reality, not a triage signal. Sofia + Iris own the
direction read. Don't escalate; just keep the scripts current so
the data stays one command away.

### Banked discipline acquired in this cycle

Worth knowing because they'll catch you on the next analog
situation:

- Don't presume defect framing on a first-of-its-kind data shape.
  Observation > defect. From Juan correction on the Thanos
  cli-signup writeup. Memory: feedback_observation_vs_defect.md.
- Don't auto-apply discipline to adjacent surfaces. Check whether
  the rule load-bears there first. From Sofia + Juan on the
  em-dash-in-marketplace.json question. Memory:
  feedback_discipline_load_bearing.md.
- Pi/skills tarball verification: compare against
  `git show <tag>:skills/<skill>/SKILL.md` (the aweb-root skills/
  tree that prepack/sync-skills copies from), NOT against local
  packages/claude-skills/skills/ (gitignored, only populated by
  running sync-skills locally). Earlier verifications of
  claude-skills 0.2.9/0.2.10 happened to pass by luck.
- CLI_VERSION coupling in aweb Makefile (task #219): `make ship`
  bumps both server and CLI in lockstep. Tag-only-at-target-sha is
  the workaround for CLI-only or server-only releases (the pattern
  used for aw 1.26.1-1.26.4 and server 1.26.5).
- PyPI propagation lag: `uv pip install aweb==X.Y.Z` may fail
  immediately after publish even when the per-version
  /pypi/aweb/X.Y.Z/json is canonical. Direct wheel download from
  files.pythonhosted.org bypasses the resolver lag; Grace can use
  `uv sync --refresh-package aweb` for the same purpose.

### Ship summary (May 26 → June 2)

| Date | Artifact | Source | Outcome |
|---|---|---|---|
| 2026-05-26 | AC v0.5.58 | 93454954 | verified-live (activity-card metadata-only) |
| 2026-05-26 | channel 1.4.9 | db9a492 | verified-live (mcpName for MCP registry) |
| 2026-05-26 | channel 1.4.10 + skills 0.2.10 | 848bba5 | verified-live (em-dash → colon plugin.json) |
| 2026-05-26 | channel 1.4.11 + Pi 0.1.16 | ea75b1a | verified-live (E2EE decrypt receive-side) |
| 2026-05-27 | aw CLI 1.26.2 | 21928a2 | verified-live (E2EE opt-in revert for customer mtg) |
| 2026-05-27 | aw CLI 1.26.3 | 8b55181 | verified-live (workspace cleanup; introduced #245) |
| 2026-05-28 | aw CLI 1.26.4 | a3fbc47 | verified-live (hosted cert-only add-worktree) |
| 2026-05-28 | server-v1.26.5 | 54c30fa | verified-live (PyPI; 007 migration for AC E2EE) |
| 2026-06-01 | aweb.ai site restructure | 92860b93 | verified-live by Olivia |
| 2026-06-02 | analytics scripts banked | hestia/scripts/ | committed |
| In flight | AC v0.5.59 | 0896ecea | GHCR ready; awaiting Render deploy |

---

<!-- Earlier entries go below. Append new entries above this line. -->
