# Review: JSON 2026 Draft vs Schema

Date: 2026-02-09
Scope: examples/JSON/draft_2026/ and schemas/SUTI_Message.schema.json
Method: Read plans in plans/, sampled key examples, compared to 2026 schema definitions, and validated all draft_2026 examples against the 2026 schema using jsonschema Draft 2020-12.

## Validation Results (draft_2026 vs 2026 schema)

All 11 examples validate successfully against the current 2026 schema.

Pass/Fail Matrix:
- 1111_bulkLocationResponse.json: PASS
- 2000_order.json: PASS
- 2001_orderConfirmation.json: PASS
- 2002_orderReject.json: PASS
- 3003_dispatchConfirmation.json: PASS
- 4010_eventVehicle.json: PASS
- 5000_messageToVehicle.json: PASS
- 5020_locationRequest.json: PASS
- 5021_locationResponse.json: PASS
- 7000_keepAlive.json: PASS
- 7001_keepAliveConfirmation.json: PASS

Important: These passes are not necessarily meaningful. Many $defs do not restrict additional properties (no additionalProperties: false), so a wide range of mismatched structures still validate. This means the schema currently allows both the intended 2026 JSON-idiomatic shape and legacy-style structures, which masks incompatibilities.

## Findings (Highest Impact)

1) Schema and examples drift on resource modeling
- Schema expects a flat resource object (idVehicle, idDriver, capacity, driverContacts).
- Examples use nested vehicle/driver objects with idVehicleList, attribute lists, and vehicleStartLocation.
- Why it is risky: this creates two competing shapes for the same concept. Clients built against the schema will not model the richer structure that examples (and XSD) imply.
- Why it still validates: the schema does not forbid extra properties in resource and related types, so the nested blocks are ignored by validation.
- References:
  - schemas/SUTI_Message.schema.json (resource)
  - examples/JSON/draft_2026/3003_dispatchConfirmation.json

2) Content payloads in examples exceed schema shape
- Schema content only allows contentType, contentSeqNo, idContent, nameContent, contacts, mobilityAids.
- Examples include attributeListContent, economyContent.paymentList, resourceContent, contactInfoListContent, subOrderContent.
- Why it is risky: this under-models the XSD content model and creates false confidence that JSON is aligned. Implementers will likely omit key substructures (economy/resource/contact details).
- Why it still validates: content has no additionalProperties constraint, so extra fields pass.
- References:
  - schemas/SUTI_Message.schema.json (content)
  - examples/JSON/draft_2026/2000_order.json

3) Enum casing mismatches are legacy examples vs planned corrections
- paymentType in examples uses prepaidsocialfee (legacy lowercase), while schema requires prepaidSocialFee per the 2026 plan for text-only enums and camelCase.
- messageTo example uses sendtoInvoice/sendtoOperator/sendtoVehicle (legacy casing), while schema uses sendToInvoice/sendToOperator/sendToVehicle per the casing normalization in plans.
- This is not a schema defect; it indicates examples still carry legacy naming and need migration to the planned JSON conventions.
- Why it still validates: those fields are not constrained in schema at the locations where examples put them (extra fields are allowed), so enum rules do not apply.
- References:
  - schemas/SUTI_Message.schema.json (paymentType, messageTo)
  - examples/JSON/draft_2026/2000_order.json
  - examples/JSON/draft_2026/5000_messageToVehicle.json

4) time object in schema omits dwellTime
- XSD time supports dwellTime; examples include it.
- Schema time only allows timeType and time.
- Why it is risky: dwellTime is a meaningful operational parameter in XSD and is used in examples. Dropping it in JSON loses fidelity.
- Why it still validates: time items allow extra properties, so dwellTime passes silently.
- References:
  - schemas/SUTI_Message.schema.json (time)
  - examples/JSON/draft_2026/2000_order.json
  - examples/JSON/draft_2026/4010_eventVehicle.json

5) Message gating is incomplete for unknown msgType
- Root schema does not require any if/then branch to match.
- Unknown msgType can pass with arbitrary properties as long as msg matches the base header shape.
- Why it is risky: validation does not prove a message is structurally correct for a specific msgType.
- References:
  - schemas/SUTI_Message.schema.json (root and allOf blocks)

## Notes from Plans That Affect Review

- The 2026 strategy is hybrid: XSD is authoritative, JSON is idiomatic with explicit mapping.
- Enumerations should be text-only; numeric codes removed.
- Anomalies should be corrected in JSON (naming and spelling fixes).
- Flat structure (msg + payload) is the intended 2026 format.

Relevant plan files:
- plans/json-schema-strategy-2026.md
- plans/json-schema-2026-changelog.md
- plans/xsd-anomalies-for-json.md

## Review Direction (Next Steps)

- Validate all 11 draft_2026 examples against the 2026 schema and produce a pass/fail matrix.
- Decide whether schema should expand to match the XSD-accurate structures used in examples, or update examples to the flattened schema model.
- Resolve the enum casing and naming drift with a single canonical convention and update both schema and examples accordingly.
- Add dwellTime to the schema time definition if XSD compatibility is required.
- Enforce that exactly one msgType branch matches (to reject unknown types).

## Per-Example Discrepancies (Detailed)

1111_bulkLocationResponse.json
- Appears aligned with schema. bulkLocationList matches expected fields and vehicleLocation entries align with status enum and lat/lon.
- No obvious mismatches found in this example.

2000_order.json
- resourceOrder uses nested vehicle with idVehicleList and capacity.seats.noOfSeats, while schema expects resource.idVehicle and capacity.seats as a number.
- node.contents includes attributeListContent, economyContent.paymentList, resourceContent, contactInfoListContent, subOrderContent. These are not defined in schema content.
- time entries include dwellTime, which is not defined in schema time.
- paymentType uses prepaidsocialfee (legacy casing) while schema defines prepaidSocialFee. This is a planned correction per the 2026 naming rules; the example should be updated.
- Result: example matches schema only because extra properties are allowed in content, time, and resource objects.

2001_orderConfirmation.json
- No obvious mismatches. This is a header-only message in the schema and the example matches that structure.

2002_orderReject.json
- orderReject.attributesReject aligns to schema (array of id). No obvious mismatches.
- The example is minimal; schema allows more fields such as orderSentBefore or orgNewProvider, but they are optional.

3003_dispatchConfirmation.json
- resource is nested as vehicle/driver objects with idVehicleList, attributeListVehicle, attributeListDriver, and contactInfoListDriver. Schema expects flattened resource fields and driverContacts.
- capacity.seats is an object with noOfSeats; schema expects an integer for capacity.seats.
- vehicleStartLocation is present but schema only allows geographicLocation on resource.
- Result: structural drift from the schema and XSD, currently masked by permissive typing.

4010_eventVehicle.json
- eventNode.contents uses attributeListContent, resourceContent, contactInfoListContent, subOrderContent, which are not in schema content.
- time entries include dwellTime, which is not defined in schema time.
- capacity.seats uses object with noOfSeats; schema expects integer.
- Result: passes because node/content/time allow extra properties.

5000_messageToVehicle.json
- messageTo uses sendtoInvoice/sendtoOperator/sendtoVehicle (legacy casing), but schema uses sendToInvoice/sendToOperator/sendToVehicle. This is a planned correction per 2026 casing normalization; the example should be updated.
- Result: passes because schema does not forbid extra properties and does not require those exact fields beyond manualText.

5020_locationRequest.json
- locationRequest is empty in the example. Schema allows this because all fields are optional.
- Risk: the schema currently allows a message with no request parameters, which is likely invalid per XSD intent.

5021_locationResponse.json
- geographicLocation aligns with schema (lat/lon required, precision optional).
- No obvious mismatches, but confirm whether additional vehicle data should be included per XSD in this message type.

7000_keepAlive.json
- Header-only message aligns with schema (msg only). No obvious mismatches.

7001_keepAliveConfirmation.json
- Header-only message aligns with schema (msg only). No obvious mismatches.

## Open Questions

- Are draft_2026 examples intended to fully validate against the 2026 schema, or are they transitional?
- Should the 2026 schema keep the flattened resource and content model, or adopt nested vehicle/driver structures from XSD?
- Should JSON treat msgType as a strict enum of known types rather than only a pattern?
