---
title: "aweb.ai homepage copy refresh — copy bundle for Hestia wire-in"
date: "2026-05-09"
type: "copy-bundle"
status: "ready for Sofia framing pass + Hestia wire-in"
brief: "Bertha chat 53251bb9 (2026-05-08); Athena pre-flight 2f9cd979 (2026-05-09)"
brand: "aweb (lowercase) per existing site convention; Bertha's 'aWeb' brief-shorthand normalizes to 'aweb' here"
---

## Context

Eugenie queued a homepage copy refresh after a non-technical
founder running multiple Claude instances did not recognize
"agents" as describing her situation. The current copy speaks to
people who already understand agent infrastructure; the target
user lives the problem without the vocabulary.

Routing (Juan call, 2026-05-09): **Iris writes, Sofia in framing
loop, Bertha can ask for changes, Hestia deploys.** Athena's
diff review happens via standard ac discipline on the wire-in.

## Constraints applied

- **Brand cap**: existing site uses `aweb` lowercase consistently
  (template: "What aweb does", "Read the agent guide at
  https://aweb.ai/agent-guide.md"). Bertha's brief used `aWeb`
  as shorthand. Bundle normalizes to `aweb` lowercase to match
  the existing surface. If Eugenie/brand has decided to migrate
  to `aWeb`, that is a separate brand-cap pass affecting more
  than this bundle; out of scope here.
- **Voice**: landing-page surface is more declarative /
  conversion-oriented than HN-comment voice. Different surface,
  different conventions. No revolutionary / game-changing
  language. Honest about what aweb does today.
- **Honesty**: Athena's pre-flight (mail 2f9cd979) found four
  human-required steps in the agent-guide flow; the hard claim
  "No developer needed. Ask your agent to set you up" overpromises.
  Tighter framing per Athena's recommendation incorporated below
  ("Sign up at aweb.ai, then ask your agent to set itself up").
  Engineering tickets to close the gaps named at the bottom.

## What's changing

| Section | Change |
| --- | --- |
| Page `<title>` + meta description | Update to match new framing |
| Hero `tagline` (in hugo.yaml params) | Replace with new headline |
| Hero `subtitle` (in hugo.yaml params) | Replace with bridge paragraph |
| Hero CTAs | Unchanged ("Start free" / "Read the docs") |
| Hero trust line | Unchanged ("Free tier · No credit card required") |
| Hero right-side code blocks | Unchanged (install + agent-guide prompt already there) |
| Works-with strip | Move up to sit immediately under hero; confirm 4 items |
| **NEW**: "Sign up. Your agent handles the rest." section | Insert between works-with strip and pillars/features |
| Pillars section heading | Replace "Give each agent an identity. Then let them coordinate." with "Each AI you're running is isolated. aweb changes that." |
| Pillars / feature cards | Unchanged (existing pillar copy stays) |

## Section-by-section copy

### Page `<title>` and meta description

**Where**: in `hugo.yaml` (or homepage front-matter), the page-level
`title` and `description` fields used by SEO + browser tab.

**`<title>`**:

> aweb — Stable addresses for your AI agents. Open-source coordination.

**Meta description (155 chars)**:

> Running multiple AI agents on the same codebase? aweb gives each one a stable address so they find each other, divide work, and stay in sync. Open source.

**Voice note**: keyword-targeted (AI agents, coordination, stable
addresses); honest; mentions OSS up front. Survives shortening to
sub-150-char if Hestia's SEO config has tighter limit.

---

### Hero — `tagline` (Hugo param)

**Where**: `Site.Params.tagline` in `hugo.yaml`. Used by the
hero h1 in `layouts/index.html`.

**Copy**:

> You're already running a team of AIs. They just can't talk to each other.

**Voice note**: pain-recognition opener. "AIs" plural is informal
and matches the founder-feedback vocabulary; do NOT normalize to
"AI agents" — the whole point is that the target user does not
have the word "agents" in their head yet.

---

### Hero — `subtitle` (Hugo param)

**Where**: `Site.Params.subtitle` in `hugo.yaml`. Used by the
hero `.hero-sub` paragraph.

**Copy**:

> Running Claude in multiple windows? Using different AI tools for different tasks? Those are agents. aweb gives each one a stable address so they can find each other, divide work, and stay in sync — without you coordinating every handoff.

**Voice note**: vocabulary-translation bridge. "Those are agents"
is the load-bearing reframing line. The "stable address … find
each other, divide work, stay in sync" maps to capabilities.md
(presence + tasks + messaging) — accurate.

---

### Hero — CTAs (unchanged)

**Where**: `.hero-actions` div in `layouts/index.html`.

- Primary: `Start free` → links to `appUrl/register`
- Secondary: `Read the docs` → links to `docsUrl`

No change.

---

### Hero — trust line (unchanged)

**Where**: `.hero-note` paragraph in `layouts/index.html`.

> Free tier · No credit card required

No change.

---

### Hero — right-side code blocks (unchanged)

**Where**: `.hero-right .hero-code` block in `layouts/index.html`.

The existing hero has two code blocks on the right: install
commands + the "tell your agent" prompt. These already implement
the "ask your agent to set up" pattern at hero level. Keep
as-is. The new dedicated onboarding section below builds on this,
not replaces it.

---

### Works-with strip — CREATE (not move) under the hero

**Update from Hestia's pre-flight (mail 82c9e8ab):** the strip
does NOT currently exist on aweb.ai. Brief assumed it exists +
moves up; reality is the strip needs to be created from scratch.

**Where (new)**: insert as a new section immediately under the
hero, above the new "Sign up. Your agent handles the rest." section.

**Visual treatment options** (Eugenie's call, surfaced via
Bertha):

- (a) **Text-only pills** — ~15min CSS work; cleanest first ship;
  Hestia's recommended default.
- (b) **Text + brand colors** — ~30min; each pill picks up the
  named tool's brand color as accent.
- (c) **Logos** — ~1-2h plus asset-gathering; requires
  brand-kit svg files + Anthropic / OpenAI brand-guideline checks.

**Content-overlap concern**: the existing Hosted MCP section in
`layouts/index.html` already mentions "Claude Desktop, ChatGPT,
claude.ai, and other hosted runtimes" as text. New strip
duplicates. Eugenie's call: strip REPLACES that mention, LINKS to
it, or COEXISTS with it.

**Copy**:

Header label (smaller, before the row):

> Works with

Items in the row (logo or text, per existing visual treatment):

- Claude
- ChatGPT
- Claude Desktop
- Any MCP-compatible AI

**Voice / honesty note**: "Any MCP-compatible AI" is broad but
defensible: aweb has an MCP server and channel plugin (capabilities
.md), so anything that speaks MCP can connect via custodial-agent
or local-process. Keep.

If the existing strip has more or fewer items, take Bertha's 4 as
canonical and adjust the strip; if existing has visual logos for
some, keep visual treatment consistent.

---

### NEW section — "Sign up. Your agent handles the rest."

**Where**: insert as new section between the works-with strip and
the pillars section.

**Section label** (smaller, above heading):

> No developer needed

**Section heading** (Pass-2 revert: aang verified-live per Sofia mail 5e07e713):

> Sign up. Your agent handles the rest.

**Subhead / intro paragraph (one line)**:

> Create an account at aweb.ai, then paste this into one of your AI agents:

**Copyable prompt block** (formatted as a code/prompt block,
copy button to its right per existing `.qs-copy-btn` pattern):

> I have an aweb account. Set me up so my AI agents can coordinate with each other. Follow the guide at https://aweb.ai/agent-guide.md

**`or` divider** (subtle, centered):

> or

**Developer-path link**:

> Install via the CLI — read the developer guide →

Linked to `docsUrl` (or specifically the developer-quickstart anchor
if there's one).

**Voice / honesty note**: heading is Option B ("Sign up. Your
agent handles the rest.") — the bold claim is now empirically
true. Pass-2 dispatch via Sofia mail 5e07e713 (2026-05-10):
aweb-aang verified-live across both single-team (Pepe's class)
and multi-team-agent (Bertha's class) populations; full P0 arc
empirically closed.

**Empirical correction (Hestia chat 10e79936, 2026-05-10):** the
"two-state-transition" framing Sofia used in mail 5e07e713
assumed Pass 1 (Option A interim) had shipped. It had NOT —
the bundle was waiting on gates that did not clear (Eugenie's
5-item call via Bertha + Athena's tech-accuracy reply on works-
with strip integrations). So no customer saw the Option A
interim claim during the aang-fix window; the live aweb.ai
homepage stayed at the pre-refresh state ("Agents want to work
together" + "Run a team of agents...") through that window.

What this means: there is exactly ONE state transition, not
two — old-pre-refresh-homepage → Option-B-shipped-fully. The
"honest interim served customers in the window" framing does
not hold empirically. The Option-A-Option-B-revert mechanic
that Sofia engineered would have served the protective
function as designed, but the gates blocked it from shipping
in time. The realized pattern is simpler: ship the truth in
one move, once it's true.

This does NOT change the wire-in decision. The bundle is correct
to ship Option B now — it's the truth. The lesson is for the
next time we have a planned soft-claim → hard-claim transition:
verify Pass 1 is shipping (not just drafted) before committing
to the two-transition shape; or ship Pass 1 with looser gates
so it actually lands.

**Engineering work in flight** (Juan called all four P0;
Athena's dev team dispatching):

1. Agent-runnable signup flow / cli-signup-returns-API-key
   (aweb-aang) — closes the cold-start gap. THIS is the load-
   bearing fix that gates the Option A → Option B copy revert.
   3-4 day estimate.
2. Plugin install via shell (close the Claude-Code `/plugin
   install` REPL gap)
3. Documented path for shell-less agents (Claude Desktop /
   ChatGPT app via custodial-agent + dashboard)
4. Pepe's fourth friction (named in his autonomous-install
   report; specifics not surfaced to Iris yet)

**Three options on this section heading** (for record):

- Option A (ships now): "Most setup your agent can handle."
  Honest about the engineering gap; matches what an autonomous
  install actually delivers today.
- Option B (post-aang revert): "Sign up. Your agent handles the
  rest." The truth once aang verified-live; Sofia dispatches
  the revert.
- Option C (would-be-ideal): "No developer needed. Ask your
  agent to set you up." End-to-end autonomous, no human signup;
  blocked on the named engineering tickets above.

---

### Pillars section — section heading change

**Where**: `.section-heading` in the `<section class="pillars">`
block of `layouts/index.html`. Currently reads "Give each agent
an identity. Then let them coordinate."

**New copy**:

> Each AI you're running is isolated. aweb changes that.

**Section label above the heading** (currently "What aweb does"):

> What aweb does

(unchanged; if Eugenie wants this updated too, ask)

---

### Pillars / feature cards (unchanged)

**Where**: existing two pillars in `layouts/index.html` — "Give
agents an address" and "Let your agents coordinate".

Note from Iris: Bertha's brief mentioned "three feature cards
(Stable addresses, Agent-to-agent messaging, Shared tasks)
remain unchanged." The current site has TWO pillars (address +
coordinate) rather than three feature cards. Either:
- (i) Bertha was describing a different/older version of the page, OR
- (ii) the three feature cards live in a different section I haven't
  inspected, OR
- (iii) the brief implicitly accepts the existing two-pillar
  structure as "the feature cards" since they cover the same
  three concepts in two cards.

Hestia: when wiring in, surface this discrepancy if the structure
mismatch creates a real change. If existing two-pillar structure
covers the three concepts, no action needed.

---

## Open questions for Bertha / Eugenie / Sofia

1. **Brand cap**: confirm `aweb` lowercase is intended (matches
   existing site). If the visual brand is in transition to `aWeb`,
   that's a wider migration; this bundle does not initiate it.

2. **"No developer needed" headline soften**: confirm Iris's
   recommendation (Athena-honest "Sign up. Your agent handles
   the rest.") is acceptable. Three named alternatives in that
   section. If Eugenie wants to ship the original hard claim
   anyway with the engineering tickets to close the gap later,
   say so explicitly and Athena will queue the tickets.

3. **Pillars structure**: brief says "three feature cards"; site
   has "two pillars". Hestia: surface if wire-in shows a real
   structural mismatch.

4. **Works-with strip position**: confirmed move-to-under-hero.
   If the existing strip has different visual treatment than
   what Bertha is imagining, Hestia surfaces during wire-in.

5. **`or` divider styling**: lowercase "or", centered. Match
   existing visual conventions if any; if not, simple horizontal
   line above and below works.

## Sequencing

- **Today**: this file lands in publishing/drafts/. Sofia framing
  pass; Bertha changes if any.
- **Once Bertha/Sofia land changes**: Hestia takes the bundle,
  wires into ac/site/, decides agent-guide URL routing
  (option a or b per her mail d4910f87), Athena diff review
  per standard ac discipline, deploy via `make deploy-site`,
  verify-live.
- **Verify-live evidence to**: Bertha + Eugenie + Juan via screenshot
  or live URL.
- **Engineering follow-ups** (separate, not blocking): Athena
  queues the three tickets named in the "No developer needed"
  section.

## Sofia framing-pass result (mail 6827f33b, 2026-05-09)

Signed off on the three load-bearing calls: Athena-honest soften
(Option B "Sign up. Your agent handles the rest." preferred; do
NOT ship Option C until the named engineering tickets close);
voice register declarative-without-platform-speak holds the line;
BYOT correctly NOT surfaced at hero level.

Three items raised in Sofia's pass that go to Bertha for Eugenie's
call (mailed):

- **Trust-line position clarification.** Brief said "Trust line +
  works-with strip moved up." Bundle kept the trust line where it
  is (already inside `.hero-note`) and moved only the works-with
  strip. Possibly intentional (trust line is already at hero, so
  "moved up" doesn't apply), possibly Bertha intended a real move
  (e.g., above the CTAs). Confirm.

- **Works-with strip specificity nudge 1: name Cursor / Codex /
  OpenCode.** Brief lists Claude / ChatGPT / Claude Desktop / Any
  MCP-compatible AI. Per audiences.md, Cursor and Codex are tools
  the target customer actively uses. A founder on Cursor who does
  not see Cursor in the strip may assume aweb does not work with
  their setup and bounce — "Any MCP-compatible AI" technically
  covers them but adds a click of cognitive load. Suggest naming
  integrations explicitly if Athena confirms they're factually
  supported.

- **Works-with strip specificity nudge 2: tighten "Any MCP-
  compatible AI".** Same concern, opposite framing — the phrase
  is broad enough to be true but not specific enough to feel like
  inclusion. Athena's tech-accuracy call on which named integrations
  are real beyond the briefed four. Mailed Athena.

Both nudges are Bertha/Eugenie's call. Sofia called them "nudges,
not framing-blockers."
