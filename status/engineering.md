# Engineering Status

Last updated: 2026-04-10 (initial — CTO will maintain going forward)

## aweb OSS
- **Status**: Close to shippable
- **Team**: dave (coordinator), henry + ivy (developers)
- **Active**: identity-scoped messaging, CLI+server alignment for team arch
- **Blocker**: None known

## aweb-cloud (ac)
- **Status**: Mid-migration, not yet working
- **Team**: alice (coordinator), bob (developer)
- **Active**: Auth bridge refactor (JWT -> team certificates)
- **Blocker**: Auth bridge is subtle and not a simple swap
- **ETA**: ~2 days (as of 2026-04-10)

## Infrastructure
- Production database will need full reset when cloud is ready
- Backup prod data before dropping
