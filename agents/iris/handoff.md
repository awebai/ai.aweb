# Iris Handoff

Last updated: 2026-05-26 (outreach pivot: gap diagnosis + hostname-divergence sync + step 1 refresh; next is parked-artifacts audit)

## Operating focus

Use `../../publishing/runbook.md` first. Outreach work is case-based:
classify the situation, read only the references needed for that
case, produce a human-ready artifact, and record action/signal with
attribution limits.

You author. Juan and Eugenie publish. Sofia frames, Athena tech-
accuracy, Aida support-integration where applicable, Hestia deploys.
Sensitive contacts/targets stay in `co.aweb/`.

**Current arc: outreach pivot from authoring → active distribution.**
Sofia mailed brief 2026-05-26 (`e1b6c7d0`) saying Juan asked her to
bring me in on serious outreach work. Sofia's chat-direct paraphrase:
"please stand back, bring in iris, and spend some serious effort
looking for outreach opportunities." Juan-confirmation outstanding;
work unblocked from my side anyway.

## Active work

### 1. Outreach pivot: four-step plan in flight

The lane has been parked since the 2026-05-16 production deploy.
Content production has been healthy (blog post, homepage refresh,
welcome guide, MCP onboarding artifacts); community presence is
zero. No daily scan/draft/post loop running anywhere.

Four-step plan to land:

1. **✅ Refresh status + handoff** (this commit + the
   `status/outreach.md` refresh). Captures state-changes since
   2026-05-16: marketing fold, Pepe customer-evidence, Pi extension
   ship, release cluster cleared, hostname-divergence event.

2. **→ Audit parked artifacts.** Read each, judge fit against
   current state, route revisions or retire:
   - Twitter thread P1 (`publishing/drafts/2026-05-13-twitter-thread-p1-launch.md`)
   - Five 2026-05-07 direct-outreach drafts
     (`co.aweb/outreach/daily/2026-05-07-direct-outreach-post-show-hn.md`)
   - "Two Agents Not One" article (Juan's plate for juanreyero.com)

3. **→ Draft outreach strategy adaptation.** Beadhub-era source
   material is at `co.aweb/outreach/source-material/beadhub-era/`
   (12111-byte outreach-strategy.md, 26030-byte aweb-a2a-interop.md,
   README with provenance). Bones reusable; needs corrective lens
   for current aweb state (persona model from `docs/audiences.md`,
   marketing fold from `agents/sofia/corpus-architecture.md`, Pepe
   customer-evidence, Pi extension as new surface). Adapt into
   `publishing/plan.md` + `publishing/runbook.md`. Route to Sofia
   for framing pass.

4. **→ Pi extension promotion arc.** Add to `publishing/plan.md`
   as Persona-3 (developer team) target. Right shape: a piece that
   solves a real Pi-user problem (multi-agent coordination in Pi),
   with `@awebai/pi` as one tool in the answer. Not a marketing-
   shape "what you can do with @awebai/pi" headline (would cut
   against "be useful or stay silent" voice principle).

### 2. v0.5.48 release-notes pack derivation (queued)

Hestia's v0.5.48 inbound-mode CLI cluster cleared end-to-end
(verified-live 2026-05-23). Six outreach-facing facts banked in
conv `9b8ad2a8`:

1. Customer-facing labels: "All" and "Team and contacts" (literal
   strings; never the slugs `open` / `team_and_contacts`).
2. `contacts_only` is legacy with silent normalize on read; 0
   affected customers — not a migration story to amplify.
3. Default for new global agents: "All" (open).
4. Picker visible only on global identities; local-only aliases
   don't see it. Important for "who can use this" framing.
5. Both dashboard and CLI paths live.
6. BY-ALIAS chat under team_and_contacts works for same-team
   senders (athena→grace, both on dev team, verified). Customer-
   facing framing: "chat works as expected within your team even
   with team_and_contacts on." Load-bearing reassurance line for
   the most likely customer concern.

Components reviewed (Aida's runbook line + Sofia framing). Derive
when I have cycles; Sofia framing-passes before it lands.

### 3. Voice.md trinity-leak pass (parallel, low-cost)

The 2026-05-21 trinity framing (awid / aweb / corpus as three peer
products) is superseded by the 2026-05-26 fold. Sofia did a quick
re-read and reports voice.md is independent of the trinity (no
load-bearing leak), but a full pass when I'm in the file anyway
is cheap insurance.

## Recent shipping history (since last handoff 2026-05-14)

- **2026-05-14**: "AI-first company howto" blog post v3 → Bertha-
  via-Eugenie → Juan bless → live on aweb.ai. Welcome guide v5
  shipped to AC; serverInfo.instructions v5 wired by Grace.
- **2026-05-15**: Site production deploy 15 (SEO bundle + contrast
  bump + first real blog post live).
- **2026-05-16**: Production deploy via gate collapse — full
  expert-feedback rework + 1.21.2 coordinated cut backend+CLI. The
  customer-facing welcome surface migrated from `welcome.md` to
  `mcp-tutorial.md` in AC commit `052530aa` (same wave) — superseded
  the v5 welcome guide draft chain; markers added 2026-05-23.
- **2026-05-19**: Voice-passed Dave's pi-extension welcome
  (`@awebai/pi`); one tone nudge ("for the aw CLI" instead of "for
  using the aw CLI well"). Dave applied at `48bfb5f`.
- **2026-05-19**: Voice-passed aaou.17 docs (self-hosting +
  federation) on aweb main; both cleared as-is; BYOD/BYOIDT/BYOT
  terminology inconsistency flagged to Aida → resolved by Grace
  `449cb17` (federation uses BYOT, self-hosting drops jargon).
- **2026-05-23**: Aida flagged deprecated-alias hygiene on
  `send_message_to_contact` in welcome guide draft + mcp-tools-
  reference. Investigation surfaced (a) welcome.md→mcp-tutorial.md
  migration had already cleaned the live surface, (b) the site-
  docs hit sat inside the Legacy Compatibility Aliases table where
  it belongs. Three-agent banking (Aida status correction `c1737a9`,
  Iris SUPERSEDED markers + iris-AGENTS.md grep-context bank
  `f45e1c1`, cross-agent discipline `docs/agent-first-company.md`
  `4dfe70a` per Sofia framing-pass).
- **2026-05-23**: Hestia v0.5.47 destructive cutover verified-live
  (7m05s for 3-schema cutover). v0.5.48 inbound-mode CLI self-
  serve verified-live same week.
- **2026-05-23**: aapr BYOT cluster shipped + Pi 0.1.8 cross-
  harness table (Hestia `e32d9cd`, `4be8263`).
- **2026-05-26**: Marketing fold landed (Sofia `00c431e`). Trinity
  framing superseded by single-product framing. Hostname-divergence
  event closed; beadhub-era source material now accessible at
  `co.aweb/outreach/source-material/beadhub-era/`.

## Banked disciplines this cycle (in iris AGENTS.md unless noted)

New since last handoff:

- **"Grep-flag work must include section-context, not just the
  file path."** Banked from the 2026-05-23 deprecated-alias arc.
  Same string in different sections of the same doc can mean
  opposite things. Read immediate section header + ±10 lines
  before flagging a grep hit as a problem. Promoted to
  `docs/agent-first-company.md` operating rule "Verify Section
  Context Before Flagging Grep Hits" (`4dfe70a`).
- **"AC commit `052530aa` is the welcome-surface migration
  anchor."** Companion to grep-context. If a future flag references
  the welcome guide path, that SHA is the migration anchor — check
  `mcp-tutorial.md` (and `AWEB_HOSTED_MCP_INSTRUCTIONS` in
  `hosted_mcp.py`) as the live surfaces, not the deprecated draft
  chain.
- **"Keep 'infrastructure divergence I don't understand' higher
  in the hypothesis stack on second-round unambiguous mismatch."**
  Lesson from the 2026-05-26 hostname-divergence event. My push-
  back arc on Sofia's brief was right discipline at each step
  given my surface, but the cause-attribution (hallucination loop)
  was wrong; the cause was env-divergence. The aw workspace
  status was reporting Sofia's host as altair.local when her
  actual hostname was Mac.c.is. When two agents on the "same"
  filesystem return definitive opposite `ls` outputs on the same
  path, the env-divergence hypothesis deserves higher weight
  than I gave it. Not banked as a formal entry; this handoff
  carries the memory.

Carried forward from last handoff (still active):

- "Verify the infrastructure contract before debating policy" —
  AGENTS.md banked-learnings.
- "When launch / public-claim submit-state changes, surface to
  direction same-shift."
- "Verify Pass 1 is shipping (not just drafted) before committing
  to two-transition framing."
- "When planned-transition gates remain open past their assumed
  window, surface explicitly."
- "publishing/drafts/*.md is narrative / framing / decision record —
  not a wire-in spec." Iris authors `ac/site/` directly; Hestia
  deploys; drafts/ is record, not source.
- "For external-vendor policy verification, the vendor's help-
  center IS authoritative" + "cite the provenance accurately
  (snippet vs live page read)."
- "Customer-shape verification before authoring landing-copy."

## Role model context

Sofia (Direction) approves product fit and timing. Athena (Engineer)
reviews technical accuracy on product-behavior claims. Aida sends
user stories + support-integration pre-think. Metis tracks
distribution outcomes when active. Hestia signals when releases are
verified-live.

**Eugenie owns outreach send-side; Bertha is her personal agent.**
Per Juan's directive (2026-05-07): send Bertha a plan-of-action each
wake-up via `aw mail send --to bertha` so Eugenie has a current
packageable summary. After-send capture goes in
`co.aweb/outreach/history.md`; public `status/outreach.md` stays
generic per Case 7.

Juan and Eugenie publish. My drafts are the input; their voice is
the output.

## Open follow-ups (when bandwidth)

- Twitter thread Pass-2 register-variant testing (when Pass-1 is
  posted + signal observed). Pass-1 product-state may need refresh
  before send.
- "Two Agents Not One" article on juanreyero.com — Juan voice-
  passed; awaits his commit/push. Gentle re-prompt when next active
  with him.
- Pepe-anonymous customer-evidence: worth a public piece when the
  friction-to-ship arc is framable. Sofia called Pepe-anonymous
  in public outreach (`2874ded`); the story is the response shape,
  not the customer name.
- Hero-note tier honesty for next homepage iteration (Sofia flagged
  in Twitter-thread Q3 response; not blocking).
- aw workspace status hostname-bug: Sofia routing to Athena with
  cross-surface repro; FYI loop when Athena replies.

## Open questions for Juan

- Pivot framing confirmation (Sofia's chat-quote was paraphrased;
  ground-truth from him).
- Bandwidth for the daily Juan-review slot if we run a daily scan/
  draft/post loop (10-15 min/day per beadhub-era design) vs weekly-
  batch cadence.
- Eugenie send-side capacity for daily posting cadence.
