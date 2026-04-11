# CTO Handoff

Last updated: 2026-04-11

## Current state

### aweb OSS (coordinator: John)
- Close to shippable
- Active work: identity-scoped messaging, CLI+server alignment
- Ephemeral agents: dave, henry, ivy

### aweb-cloud (coordinator: Tom)
- Mid-migration: auth bridge HMAC/API-key → team certificates
- Not yet working end-to-end
- Ephemeral agents: alice, bob

### awid (coordinator: Goto)
- Mid-migration alongside aweb
- SOT rewritten April 6

## Active concerns

- Auth bridge refactor is subtle — cloud JWT → OSS team cert is not
  a simple swap. Tom should be watching for shortcuts.
- Cross-repo alignment: aweb and cloud must evolve together during
  the migration. Check that John and Tom are communicating.
- Coordinators are new — verify they're actually reading company docs
  and catching invariant violations, not just rubber-stamping commits.

## Key context

- Crypto identity migration was a deliberate architectural choice.
  Don't let anyone revert to API-key patterns.
- The 2+2 rule is enforced by coordinators, but verify they're doing it.

## Next check priorities

1. Check in with John, Tom, Goto — are they catching issues?
2. Cross-repo view: are aweb and cloud aligned?
3. Vision.md priorities still match what's being built?
