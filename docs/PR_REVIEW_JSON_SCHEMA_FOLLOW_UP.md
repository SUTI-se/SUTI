# Follow-up Technical Board Review — XSD-First JSON Schema

Date: 2026-08-13
PR: adding missing messages to json
Branch: `fix/patch-json-with-missing-message-types`
Review result: **Further changes recommended before calling the JSON schema an XSD-derived representation.**

## What improved

The previous decisions were applied correctly at the message-routing level:

- All 123 JSON examples validate (122 main-schema examples and one legacy example).
- All 136 XSD `msgType` values have a JSON conditional branch.
- No message branch requires its payload; this now respects the XSD `msg` choice's
  `minOccurs="0"` members.
- The 1023, 2030, 4000, 4012, 4041, 4042, and 5021 mappings were corrected in the
  direction of the XSD.

The remaining findings are inside shared definitions. They affect existing and newly
covered message families even when their top-level message branch is correct.

`bulkLocation` is intentionally excluded from this review. It is an established,
separately adopted JSON part of the standard and was deliberately kept unchanged by this
message-completion work.

## Resolution (implemented 2026-08-13)

All findings below were implemented and validated after this review:

- `driverSessionReject` now represents the XSD-required `driverSession`,
  `attributesReject`, and `changelog` members; a complete 2102 sample was added.
- 4010/4040 now use a dedicated `pickupConfirmation` definition rather than the
  distinct XSD `event` type.
- `referencesTo.idOrder` is now an array, as required by XSD `maxOccurs="unbounded"`;
  examples were mechanically migrated only inside `referencesTo` groups.
- 2060 now uses the XSD enum value `cancelation`.
- The identified nested cardinality constraints now follow the XSD: `order.idOrder`
  is optional, authorization contents may be empty, and an empty `requestItem` is not
  rejected solely by the JSON schema.
- The identified XSD-required fields for manual descriptions, geographic locations,
  and organization identifiers are enforced, and examples were updated accordingly.

Validation after the implementation: the schema passes Draft 2020-12 schema validation
and all 124 JSON examples validate against their referenced main or legacy schema.

## Findings

### P1 — `driverSessionReject` does not preserve the required XSD structure

The JSON definition at [schemas/SUTI_Message.schema.json](../schemas/SUTI_Message.schema.json#L3248-L3260)
uses only optional `idDriverSession` and a non-XSD `rejectReason` string.

The XSD `driverSessionReject` type at [schemas/SUTI_Message.xsd](../schemas/SUTI_Message.xsd#L2990-L3020)
requires three child elements, in order:

1. `driverSession`;
2. `attributesReject`; and
3. `changelog`.

Those are not optional in the XSD. The JSON currently cannot transmit the XSD-mandated
rejected driver-session representation, rejected attributes, or rejected changes. It
instead accepts an untyped text field that has no XSD counterpart.

**Action required:** redefine `driverSessionReject` as a JSON-idiomatic projection of the
XSD:

```json
{
  "driverSession": { "...": "..." },
  "attributesReject": [ { "src": "...", "id": "..." } ],
  "changelog": [
    {
      "change": "updated",
      "orderIds": [ { "src": "...", "id": "..." } ]
    }
  ]
}
```

Apply JSON naming/array conventions consistently, but preserve all three required XSD
members and remove `rejectReason` unless the XSD is formally extended. Add a 2102 example
that exercises the full structure.

### P1 — `pickupConfirmation` is still modeled through the wrong JSON definition

The XSD assigns messages 4010 and 4040 to the `pickupConfirmation` type
([schemas/SUTI_Message.xsd](../schemas/SUTI_Message.xsd#L225-L233)). That type has:

- optional `eventType`; and
- optional `nodeConfirmed`.

The JSON routes 4010/4040 to `$defs.event`, which is a different XSD concept (`event`
inside `eventReport`). The JSON version requires `eventType` and uses `eventNode`. This
makes the JSON stricter than `pickupConfirmation` (the XSD permits it to be absent) and
conflates `nodeConfirmed` with `eventNode`.

**Action required:** add a dedicated JSON definition for `pickupConfirmation`, for example
`pickupConfirmation` with optional `eventType` and optional `nodeConfirmed` (`node`), and
route 4010/4040 to it. Do not reuse `$defs.event` unless the XSD itself is changed to
unify the two types.

### P1 — `referencesTo.idOrder` loses the XSD's repeatable cardinality

The XSD declares `referencesTo/idOrder` as `minOccurs="0" maxOccurs="unbounded"`
([schemas/SUTI_Message.xsd](../schemas/SUTI_Message.xsd#L744-L750)). The JSON definition
at [schemas/SUTI_Message.schema.json](../schemas/SUTI_Message.schema.json#L1903-L1905)
models it as a single identifier object, unlike `idDriverSession`, `idVehicle`,
`idDriver`, and `idSuborder`, which are arrays.

A valid XSD message may carry several equivalent order IDs in one `referencesTo` group.
The JSON schema rejects that representation or forces an implementation to split one XSD
reference group into multiple JSON objects, altering its grouping semantics.

**Action required:** make `referenceToMsg.idOrder` an array of `id`, matching the XSD
cardinality and the nearby JSON pattern. Update examples that use order references to
show one group containing multiple equivalent IDs where appropriate.

### P2 — The 2060 update-type value is misspelled relative to the master

The XSD enumerates `cancelation` (one `l`) for `providerorderUpdate/@updateType`
([schemas/SUTI_Message.xsd](../schemas/SUTI_Message.xsd#L2810-L2825)). The JSON schema
accepts `cancellation` (two `l`s) at [schemas/SUTI_Message.schema.json](../schemas/SUTI_Message.schema.json#L3268-L3277).

This is an interoperability break: a valid XSD value is rejected and a non-XSD value is
accepted.

**Action required:** use `cancelation` in the XSD-compatible schema. If the two-`l`
spelling is desired, correct and version the XSD first; do not add it only in JSON.

### P2 — Several nested JSON definitions still impose stricter cardinality than their XSD source

The top-level message branches are now optional, but a few nested shapes still need the
same XSD-first scrutiny:

- `authorizationAccept.contents` uses `minItems: 1`, while the XSD requires the
  `contents` wrapper but permits zero `content` children (`content minOccurs="0"`).
- `infoRequestItem` uses `oneOf` to require exactly one request alternative. In the XSD,
  `requestItem` is present, but every branch inside its `choice` has `minOccurs="0"`.
  Confirm the intended XSD particle semantics and do not make JSON stricter if
  `<requestItem/>` is valid.
- `order.idOrder` is required in JSON, while XSD `order/idOrder` is `minOccurs="0"`.
  This is pre-existing but becomes more visible now that 2000, 2900, 4001, 4020, 7100,
  and 7101 all use the shared definition.

**Action required:** make a deliberate full cardinality audit: for every new or reused
`$defs` field, map XSD `minOccurs`, `maxOccurs`, and attribute `use` to JSON
`required`/array constraints. This should be a mechanical review table, not an
example-driven approximation.

### P2 — Fidelity gaps that are permissive rather than restrictive still need a documented policy

The current board rule prevents JSON from being stricter than the XSD, but being much
more permissive can also make implementations incompatible. Examples include:

- `manualDescription` does not require XSD-required `manualText`, `sendtoInvoice`,
  `sendtoVehicle`, `sendtoOperator`, or `vehicleConfirmation`.
- `geographicLocation` requires only latitude/longitude, while the XSD also requires
  `typeOfCoordinate` and `precision`.
- `organization.ids` permits an empty array although XSD `idOrg` has the default
  minimum occurrence of one.

**Board decision requested:** decide whether the JSON schema should be **exactly as
restrictive as the XSD where JSON can express the constraint**, while never introducing
additional constraints. That is recommended. If a deliberately permissive migration
mode is needed, publish it separately as a compatibility schema rather than weakening
the normative XSD-derived schema.

## Lower-priority documentation and example work

- The examples are correctly described as schema samples, but the repository still needs
  a compact README/index explaining that they are not full resolvable protocol flows.
- Coverage remains payload-family based: 113 of 136 codes have a dedicated example.
  Add a code-to-canonical-example matrix so implementers can find the intended example
  for the remaining 23 codes.
- The `priceValue` rename for XSD attribute `price` is sensible to avoid an ambiguous
  `price.price` property, but it should be documented in the XSD-to-JSON mapping table.

## Recommended next implementation order

1. Correct `driverSessionReject` and add a complete 2102 example.
2. Add a dedicated `pickupConfirmation` definition for 4010/4040.
3. Correct `referencesTo.idOrder` and the 2060 `cancelation` value.
4. Complete the mechanical nested-cardinality audit, then update fixtures and mapping
   documentation.

No files other than this follow-up review were changed in this pass.
