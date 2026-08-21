# Technical Board Review — JSON Schema Message Completion PR

Date: 2026-08-13
PR: adding missing messages to json
Branch: `fix/patch-json-with-missing-message-types`
Review stance: **Request changes before approval**

## Scope and checks performed

This review compares the PR with `schemas/SUTI_Message.xsd` as the stated master,
checks the new JSON Schema 2020-12 structure, and reviews the added examples for
interoperability and practical usability.

Checks completed:

- The JSON schema itself passes `Draft202012Validator.check_schema`.
- All 122 non-legacy JSON examples pass the updated main schema.
- No overlapping `msgType` conditional branches were found.
- The JSON enum contains 136 codes, matching the XSD `msgType` enumeration.
- The PR adds 85 example files, but the plan and coverage statements do not match
  the delivered count.

Passing validation is useful, but it currently proves conformance to the new JSON
schema only. It does not prove that the new JSON shapes are faithful to the XSD or
that the examples represent complete SUTI message flows.

## Findings

### P1 — Required payload policy diverges from the XSD without being declared as a JSON profile

The PR makes payloads required for several message branches even though the matching
XSD choice elements are optional (`minOccurs="0"`). Examples include:

- `1010`–`1012` `resourceInformation`
- `1100`–`1102` `bulkLocationRequest`
- `1110`–`1112` `bulkLocation`
- `1500`/`1501` `infoRequest`
- `1600`/`1601` `infoResponse`
- `2000` `order`
- `2531`/`6001` `orderReport`
- `2800`/`2801`/`2541`/`6800` `orderTemplate`
- `2810` `scheduleElementOrderList`

For example, the branch at [schemas/SUTI_Message.schema.json](../schemas/SUTI_Message.schema.json#L90-L116)
requires `resourceInformation`, while the XSD `resourceInformation` choice element is
optional. The same pattern is repeated throughout the `allOf` branches.

This may be a good JSON usability policy, but it is stricter than the stated XSD-master
approach. A valid XSD message can therefore be rejected by the JSON schema. The plan
currently describes this as a payload-purpose decision, but does not define a formal
JSON profile or explain which XSD-valid messages are intentionally excluded.

**Action / choice required:**

1. **Strict JSON profile:** keep the required payloads, explicitly document that this
   schema is a stricter 2026 JSON profile, add a profile/version identifier, and list
   every intentional restriction; or
2. **XSD compatibility:** remove the added payload requirements wherever the XSD has
   `minOccurs="0"`, then use examples and documentation to show the recommended
   payload for each message.

The board should choose one policy before this becomes an interoperability contract.

### P1 — Several accepted payloads are documented as intentional XSD deviations, but there is no compatibility contract

The plan acknowledges these deviations in HC-13, and the schema implements them:

- `2030` accepts an `orderForward` payload although the XSD `msg` choice does not map
  that element to 2030; the XSD instead relies on `referencesTo/idOrderForward`.
- `4000` accepts a `resource` payload although the XSD message choice has no dedicated
  payload for this message.
- `4012` and `4042` accept an `event` payload although the XSD maps 4012 to
  `manualDescriptionMsg` and does not explicitly map 4042.
- `5021` accepts `geographicLocation` while the XSD maps 5021 to `addressLocation`.
- `1023` retains `resourceDispatch` although the XSD places 1023 in the references-only
  area rather than mapping it to the `resourceDispatch` choice.

The rationale is understandable for backward compatibility, but the resulting schema
is neither a strict XSD projection nor a clearly named compatibility profile. A consumer
cannot tell whether these are normative JSON forms, legacy aliases, or tolerated
extensions.

**Action / choice required:**

- Define the JSON representation as a named SUTI JSON profile and document these
  mappings as normative; or
- Add explicit compatibility/deprecation metadata and a migration path; or
- Remove the deviations and preserve compatibility in a separate legacy schema.

At minimum, add a table of all accepted JSON payload aliases and their XSD equivalents,
including whether each alias is preferred, deprecated, or required for existing examples.

### P1 — Message types 1120, 1121, and 1122 are admitted without authoritative semantics

The XSD enum contains `1120`, `1121`, and `1122`, but the message documentation and XSD
`msg` choice do not define their payload or meaning. The PR therefore adds them as
references-only branches and creates bare examples such as [examples/JSON/2026/1120.json](../examples/JSON/2026/1120.json#L1).

The generic XSD comment that an unmentioned message “only uses referencesTo” is a useful
fallback, but it does not establish the business semantics, sender/receiver direction,
required references, or whether these codes are obsolete/reserved. Publishing them as
normal supported messages can cause implementers to treat undocumented codes as stable
protocol features.

**Action / choice required:**

- Keep them in the enum but mark them explicitly as reserved/undocumented and exclude
  them from the supported-message branches and examples; or
- Obtain a Technical Board decision describing their semantics and required references,
  then retain them as supported messages; or
- Move them to a separate experimental/reserved schema.

Do not silently promote enum-only codes to supported protocol messages.

### P1 — The accounting and reporting realignment needs golden interoperability fixtures

The PR replaces several placeholder shapes with substantial new structures, especially
`accounting`, `tour`, `calculationFare`, `orderReport`, `summaryReport`, and
`economyReport`. The new schema validates the supplied examples, but there is no
cross-check against a known-good XML instance converted into the new JSON shape.

This is high risk because these structures contain repeated XSD wrappers, optional
sequences, and renamed fields. For example, the JSON `tour` shape flattens and renames
`referencesToTour`, `statusTour`, `suborderTour`, `calculationsTour`, `eventTour`, and
related fields. A local JSON Schema validator cannot detect an incorrect semantic
rename when both the schema and example use the same invented name.

**Action required:** add at least one paired fixture per high-risk family:

- XML and JSON for 2531/6001 order reports
- XML and JSON for 6500 delivery notes
- XML and JSON for 8000 plus one 80xx accounting message
- XML and JSON for 1501/1601 price request/response
- XML and JSON for 2901 authorization acceptance

Document the conversion mapping and verify that required information survives a
round-trip or an explicitly documented lossy conversion.

### P2 — The completion plan is stale and contains incorrect coverage numbers

[docs/JSON_SCHEMA_COMPLETION_PLAN.md](JSON_SCHEMA_COMPLETION_PLAN.md#L14) says the XSD
defines 128 codes, while the delivered enum and XSD contain 136. The plan also retains
unchecked implementation items at [docs/JSON_SCHEMA_COMPLETION_PLAN.md](JSON_SCHEMA_COMPLETION_PLAN.md#L382-L391)
after the implementation was completed. Its examples section does not reflect the 85
new example files in the PR.

This matters because the plan is the audit trail for a standards change. A reviewer
cannot reliably use it to determine what was implemented, deferred, or intentionally
excluded.

**Action required:** update the plan after the final implementation:

- correct all counts;
- mark completed checklist items;
- list the exact supported message codes and example files;
- distinguish existing examples from new examples;
- state whether 8182 and 1120–1122 are excluded, reserved, or supported.

### P2 — Added examples are syntactically valid but several are not usable protocol fixtures

The generated references-only examples repeatedly reference the synthetic message ID
`2026011500000000`, which is not the `idMsg` of another example in the repository. The
2005–2007 examples illustrate this at [examples/JSON/2026/2005_orderRejectRequest.json](../examples/JSON/2026/2005_orderRejectRequest.json#L28-L38),
[examples/JSON/2026/2006_orderRejectRequestAccepted.json](../examples/JSON/2026/2006_orderRejectRequestAccepted.json#L28-L38),
and [examples/JSON/2026/2007_orderRejectRequestReject.json](../examples/JSON/2026/2007_orderRejectRequestReject.json#L28-L48).

The examples therefore demonstrate schema shape, but not a credible SUTI exchange. The
problem is especially visible for request/response sequences such as 2005 → 2006/2007:
there is no coherent preceding 2002 rejection request or shared message identity.

**Action / choice required:** decide whether the repository examples are:

- **schema samples:** use clearly marked placeholder IDs and say so in the examples
  README; or
- **protocol fixtures:** use a coherent scenario with references that resolve to other
  repository examples, unique IDs, and sender/receiver directions matching the flow.

For a standards repository, protocol fixtures are preferable. At minimum, replace the
repeated `2026011500000000` placeholder with distinct IDs and add a short flow index.

### P2 — Example coverage is still incomplete despite the completion goal

The PR adds examples for 85 files, but 23 of the 136 enum codes still have no JSON
example in `examples/JSON/2026/`, including existing or newly supported codes such as
`1061`, `1100`, `1500`, `1600`, `2012`, `2020`, `2030`, `2060`, `2101`, `2102`, `2541`,
`2800`, `2810`, `4000`, `4001`, `4100`, `6001`, and the remaining 81xx accounting codes.
Some of these have related examples, but a related message is not a substitute for a
message-specific fixture when the goal is complete message coverage.

**Action / choice required:** either add one example per supported code or explicitly
state that coverage is per payload family and provide a matrix mapping each code to its
canonical example. The latter is acceptable, but the current plan should not imply
one-example-per-message coverage when it is not provided.

### P2 — The legacy bulk-location schema change is useful but should be separated or justified

The PR changes [schemas/SUTI_BulkLocation_legacy.schema.json](../schemas/SUTI_BulkLocation_legacy.schema.json#L8-L33)
to allow `$schema`, and changes the legacy example to point to that schema. This fixes a
real validation problem, but it is unrelated to adding missing message types in the main
schema and changes behavior in a legacy contract.

**Action / choice required:**

- Keep it in this PR only if the PR description explicitly identifies it as a required
  validation fix and adds a regression check; or
- split it into a separate maintenance PR to keep the message-completion review
  focused.

## Board decisions requested

Before approval, the Technical Board should record decisions on these points:

1. Is the JSON schema a strict XSD projection or a stricter JSON profile?
2. Are the HC-13 payload deviations normative, deprecated compatibility aliases, or
   errors to remove?
3. Are 1120–1122 supported, reserved, or undocumented enum values?
4. Are examples schema samples or resolvable protocol fixtures?
5. Is one-example-per-message required, or is payload-family coverage sufficient?
6. Should the legacy bulk-location fix remain in this PR?

## Positive aspects

- The PR centralizes the complete XSD message-code enum and gives every code a matching
  conditional branch.
- The use of `unevaluatedProperties: false` provides useful per-message closed-world
  validation.
- The new shared definitions for prices, authorization, order links, reporting, and
  accounting reduce several earlier placeholders.
- The examples consistently include `$schema` and exercise the newly added branches.
- The implementation has a passing local JSON Schema validation baseline, which gives a
  solid foundation for the required semantic and interoperability checks.

## Recommended approval gate

Approve after the board decisions are recorded, the required-payload policy is made
explicit, the undocumented message codes are resolved, the plan is corrected, and
representative XML/JSON golden fixtures are added for the high-risk message families.
