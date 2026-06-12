# docs/a2a.md edit proposal — align card examples with digest vectors

For Grace/Athena to apply (contract is dev-team-owned; a2a proposes, does not
self-apply). Rationale: the `card_digest` canonical function omits empty optional
maps/lists and default scalars. The doc's example cards must match what we hash,
or readers will generate cards that don't verify.

## Edit 1 — §5.1 Required Interface Shape (per-address card example)
Remove the two empty-optional lines:
```
-  "securitySchemes": {},
-  "securityRequirements": [],
```
(Card keeps `capabilities`, `defaultInputModes`, `defaultOutputModes`,
`supportedInterfaces`, `skills`, etc. — only the two empty optionals drop.)

## Edit 2 — §5.2 Root Router Card example
Same removal:
```
-  "securitySchemes": {},
-  "securityRequirements": [],
```

## Edit 3 — add a sentence after the §5.1 example (presence semantics)
> Absence of `securityRequirements` (and `securitySchemes`) means an
> unauthenticated route. Empty optional maps/lists and default scalars
> (e.g. a `false` `extendedAgentCard`) are omitted from generated cards so the
> `card_digest` canonical form is unambiguous. `streaming` and
> `pushNotifications` are included only when the agent deliberately advertises
> them (they are `optional bool`, so an explicit `false` is part of the
> canonical bytes; an unset capability is omitted entirely).

## Edit 4 — §3.1 task-state list: add AUTH_REQUIRED
Add `TASK_STATE_AUTH_REQUIRED` to the enumerated wire states (it is a real
interrupted state in the proto). Note in prose that it is typically
gateway-generated, not agent-asserted, so it is NOT added as an `a2a-reply`
`state` alias in §10.2 for now.

## Not changed
- `version: "1.0.0"` (agent version) stays — distinct from interface
  `protocolVersion: "1.0"` (A2A protocol version). Both are correct.
- `capabilities.extensions` (awid-publication) stays — non-empty, intentional.
