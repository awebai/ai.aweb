# Coordinator awid (Goto) — Handoff

Last updated: 2026-04-11 (initial)

## Current state

awid is mid-migration alongside aweb. Team certificates, team public
keys, and certificate issuance records are being added. The SOT
(awid-sot.md) was rewritten on April 6 as part of the crypto identity
migration.

## Key things to watch

- The registry must never hold private keys
- The registry must never sign on anyone's behalf
- Namespaces, addresses, and teams must stay independent at the
  registry level
- awid-sot.md must match the code — check for divergence
