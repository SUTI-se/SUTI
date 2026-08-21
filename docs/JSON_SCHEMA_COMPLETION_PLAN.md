# JSON Schema Completion Plan — Missing SUTI Message Types

Date: 2026-08-12 (implemented and corrected 2026-08-13)
Status: Implemented (decision record; see status note below)
Master: [schemas/SUTI_Message.xsd](../schemas/SUTI_Message.xsd)
Target: [schemas/SUTI_Message.schema.json](../schemas/SUTI_Message.schema.json)

> **Status note (2026-08-21):** This document is the decision record for the
> 2026-08 completion work. Its coverage matrix (§3) and hard-choice sections (§4)
> describe the state *before* the Technical Board decisions in the box below and
> are intentionally left unchanged. The normative message mapping, the list of
> JSON extensions, and the naming rules are maintained in
> [SUTI_JSON_Mapping.md](SUTI_JSON_Mapping.md) — use that document, not §3/§4,
> as the reference.

> ## Implementation decisions applied (Technical Board senior advisor, 2026-08-13)
>
> Guiding rule: **the JSON schema must never be stricter or more specific than the
> XSD; the XSD is the master.** The following decisions were applied to the
> implementation and supersede any conflicting "required payload" or "kept deviation"
> language elsewhere in this document:
>
> 1. **No payload is required.** Every XSD `msg` choice element is optional
>    (`minOccurs="0"`), so no JSON branch requires its payload. Examples and
>    documentation show the recommended shape; the schema never rejects an XSD-valid
>    message for omitting a payload.
> 2. **Deviations from the XSD are errors, not aliases.** Corrected: `2030` is
>    references-only (the invented `orderForward` payload was removed); `1023` is
>    references-only (removed `resourceDispatch`); `4012` uses `messageTo`
>    (XSD `manualDescriptionMsg`) instead of `event`; `4041`/`4042` are
>    references-only; `4000` is references-only (removed from the `resource` branch);
>    `5021` gained the XSD-correct `addressLocation` payload alongside
>    `geographicLocation`.
> 3. **1120–1122 remain supported as references-only.** They are in the XSD enum and
>    the XSD states that messages not named in the choice "only use referencesTo";
>    rejecting them would make the JSON stricter than the master. They are documented
>    as reserved/undocumented.
> 4. **Examples are schema samples, not full protocol fixtures.** Reference IDs are
>    unique per flow (no shared `2026011500000000` placeholder) but examples are not a
>    complete resolvable scenario web.
> 5. **Coverage is per payload family**, not one-example-per-message. 113 of 136 codes
>    have an example; the remainder are covered by their shared payload-family examples.
> 6. **The legacy bulk-location `$schema` fix stays** — it is a pure bug fix (the
>    legacy schema rejected its own example) and makes the JSON no stricter.
> 7. **Nested constraints follow the XSD where JSON can express them.** Required
>    fields, arrays, and enum values mirror XSD `use`, `minOccurs`/`maxOccurs`, and
>    enumerations without adding extra constraints. This includes repeatable
>    `referencesTo.idOrder`, `pickupConfirmation`, `driverSessionReject`, and the
>    XSD spelling `cancelation` for 2060.

## 1. Method

The XSD `msgType` enumeration (the master list of all SUTI message types) was compared
against `msgTypeEnum` in the JSON schema. Message names were verified against
`docs/SUTI_Messages.pdf` and the `msgName` attributes in the XML examples.

- XSD defines **136** message type codes.
- The JSON schema now covers all **136** codes (each has a matching conditional branch).
- `8182` (Accounting Revaluate Client Fines) exists in the PDF documentation but **not**
  in the XSD enumeration — it is excluded (XSD is master).
- `1120`, `1121`, `1122` exist in the XSD enumeration but are **not documented** in
  SUTI_Messages.pdf — they are included as references-only messages (see HC-12 and the
  decisions above).

## 2. Established JSON conventions (to keep applying)

Observed from the current JSON schema and the `examples/JSON/2026/` files:

1. **One message per document**: `{ "msg": {...}, <payload>: {...} }`. The XSD root-level
   `orgSender`/`orgReceiver` were moved into `msg` (JSON has no separate envelope);
   `sutiMessages: [ ... ]` provides batch transmission instead of the XSD `msg` repetition.
2. **XSD attributes become JSON properties**; XSD elements keep their names, but redundant
   prefixes are dropped (`vehicle/idVehicle` → `vehicle.id`, `node/@nodeSeqno` →
   `node.nodeSeqNo`).
3. **Wrapper containers are flattened to arrays**: `timesType/time*` → `times[]`,
   `contactInfosType/contactInfo*` → `contactInfo[]`, `contents/content*` → `contents[]`,
   `attributesType/attribute*` → `attributes[]`.
4. **Numeric enumeration codes are dropped**; the human-readable value is kept and
   normalized to camelCase (`notrequested` → `notRequested`, `mobaidpickup` →
   `mobAidPickup`).
5. **Per-message validation** uses `allOf` + `if`/`then` on `msg.msgType`; messages that
   share a payload share one branch via `enum`; each branch ends with
   `unevaluatedProperties: false`; a catch-all `then: false` rejects unknown msgTypes.
6. **References-only messages** (the XSD `msg` choice has no payload element for them —
   the XSD states "If a message is not explicitly mentioned in XSD it only uses
   referencesTo") get a branch allowing only `msg` (+ `$schema`).
7. **Payload required-ness**: the primary payload is `required` for messages whose purpose
   is to deliver new data (2000 `order`, 1100 `bulkLocationRequest`, 5021 location,
   6500 `deliveryNote`, 8000 `accounting`, ...); it stays optional for
   confirmations/acks/rejects (4011/4012 `event`, 1020 `resourceDispatch`, ...).

## 3. Coverage matrix

Legend: ✅ covered · 🆕 missing, planned · 🔁 covered but realigned (see hard choices)

| Msg | Name (SUTI_Messages.pdf) | XSD payload element | JSON plan |
|-----|--------------------------|---------------------|-----------|
| 1000 | SingleResourceRequest | `resourceInformation` (resourceType) | 🔁 realign to `resourceInformation` (HC-1) |
| 1001 | AgreementResourcesRequest | `resourceInformation` | 🆕 `resourceInformation` |
| 1002 | AllResourcesRequest | `resourceInformation` | 🆕 `resourceInformation` |
| 1010 | SingleResourceResponse | `resourceInformation` | 🆕 `resourceInformation` |
| 1011 | AgreementResourceResponse | `resourceInformation` | 🆕 `resourceInformation` |
| 1012 | AllResourceResponse | `resourceInformation` | 🆕 `resourceInformation` |
| 1020 | Resource Login | `resourceDispatch` | ✅ |
| 1021 | Resource Login Confirmation | — (referencesTo) | ✅ |
| 1022 | Resource Login Reject | `manualDescriptionMsg` | 🔁 add optional `messageTo` (HC-13) |
| 1023 | Resource Logoff | — (referencesTo) | ✅ (keeps `resourceDispatch`, HC-13) |
| 1024 | Resource Logoff Confirmation | — (referencesTo) | 🆕 references-only |
| 1025 | Resource Logoff Reject | `manualDescriptionMsg` | 🆕 optional `messageTo` |
| 1060 | RatingRequest | — (referencesTo) | 🆕 references-only |
| 1061 | RatingResponse | `ratings` | ✅ |
| 1062 | RatingRequestReject | — (referencesTo) | 🆕 references-only |
| 1100 | SingleBulkLocationRequest | `bulkLocationRequest` | ✅ |
| 1101 | AgreementBulkLocationRequest | `bulkLocationRequest` | 🆕 join 1100 branch |
| 1102 | AllBulkLocationRequest | `bulkLocationRequest` | 🆕 join 1100 branch |
| 1110 | SingleBulkLocationResponse | `bulkLocation` | 🆕 join 1111/1112 branch |
| 1111 | AgreementBulkLocationResponse | `bulkLocation` | ✅ |
| 1112 | AllBulkLocationResponse | `bulkLocation` | ✅ |
| 1120 | (undocumented) | — | 🆕 references-only (HC-12) |
| 1121 | (undocumented) | — | 🆕 references-only (HC-12) |
| 1122 | (undocumented) | — | 🆕 references-only (HC-12) |
| 1500 | NodeListRequest | `infoRequest` | 🔁 realign `infoRequest` def (HC-5) |
| 1501 | PriceRequest | `infoRequest` | 🆕 join 1500 branch |
| 1600 | NodeListResponse | `infoResponse` | 🔁 realign `infoResponse` def (HC-5) |
| 1601 | PriceResponse | `infoResponse` | 🆕 join 1600 branch |
| 1920 | Resource Allocation | `resourceAllocation` | 🔁 realign def (HC-6) |
| 1921 | Resource Allocation Accept | — (referencesTo) | 🆕 references-only |
| 1922 | Resource Allocation Reject | — (referencesTo) | 🆕 references-only |
| 2000 | Order | `order` | ✅ |
| 2001 | Order Confirmation | — (referencesTo) | ✅ |
| 2002 | Order Reject | `orderReject` | ✅ |
| 2003 | Order Reject Confirmation | — (referencesTo) | 🆕 references-only |
| 2005 | Order Reject Request | — (referencesTo) | 🆕 references-only |
| 2006 | Order Reject Request Accepted | — (referencesTo) | 🆕 references-only |
| 2007 | Order Reject Request Reject | — (referencesTo) | 🆕 references-only |
| 2010 | Order Cancellation Request | — (referencesTo) | ✅ |
| 2011 | Order Cancellation Accepted | `cancellationConsequence` | 🔁 move to `cancellationConsequence` branch (HC-4) |
| 2012 | Order Cancellation Accepted w/ Consequence | `cancellationConsequence` | ✅ |
| 2013 | Order Cancellation Reject | — (referencesTo) | 🆕 references-only |
| 2020 | Node Cancellation Request | `nodeCancellation` | ✅ |
| 2021 | Node Cancellation Accepted | `cancellationConsequence` | 🆕 join 2012 branch |
| 2022 | Node Cancellation Accepted w/ Consequence | `cancellationConsequence` | 🆕 join 2012 branch |
| 2023 | Node Cancellation Reject | — (referencesTo) | 🆕 references-only |
| 2030 | Order Forward | — (referencesTo: `idOrderForward`) | ✅ (keeps `orderForward` payload, HC-13) |
| 2031 | Order Forwarded Reject | — (referencesTo) | 🆕 references-only |
| 2032 | Order Forwarded Received | — (referencesTo) | 🆕 references-only |
| 2040 | Order Linked | `orderLink` | 🔁 move off `driverSession` branch to new `orderLink` (HC-2) |
| 2050 | Order Freeze | — (referencesTo) | 🆕 references-only |
| 2060 | Provider Update Order | `providerOrderupdate` | ✅ |
| 2061 | Confirmation Provider Update Order | — (referencesTo) | 🆕 references-only |
| 2100 | DriverSession | `driverSession` | ✅ |
| 2101 | DriverSession Confirmation | `driverSession` | ✅ |
| 2102 | DriverSession Reject | `driverSessionReject` | ✅ |
| 2103 | DriverSession Reject Confirmation | — (referencesTo) | 🆕 references-only |
| 2104 | DriverSession Synchronization Request | — (referencesTo) | 🆕 references-only |
| 2105 | DriverSession Reject Request | — (referencesTo) | 🆕 references-only |
| 2106 | DriverSession Reject Request Accepted | — (referencesTo) | 🆕 references-only |
| 2107 | DriverSession Reject Request Reject | — (referencesTo) | 🆕 references-only |
| 2110 | DriverSession Cancellation Request | — (referencesTo) | 🆕 references-only |
| 2111 | DriverSession Cancellation Accepted | (analogy w/ 2011) | 🆕 `cancellationConsequence` (HC-9) |
| 2112 | DriverSession Cancellation Accepted w/ Consequence | (analogy w/ 2012) | 🆕 `cancellationConsequence` (HC-9) |
| 2113 | DriverSession Cancellation Reject | — (referencesTo) | 🆕 references-only |
| 2530 | OrderStatusRequest | — (referencesTo) | 🆕 references-only |
| 2531 | OrderStatus | `orderReport` | 🆕 join 6001 branch; realign def (HC-10) |
| 2532 | OrderStatusReject | — (referencesTo) | 🆕 references-only |
| 2540 | RequestForOrderInfo | — (referencesTo) | 🆕 references-only |
| 2541 | OrderInfo | `orderTemplate` | 🆕 join 2800 branch (HC-8) |
| 2800 | OrderTemplate | `orderTemplate` | 🔁 realign def (HC-8) |
| 2801 | OrderTemplateConfirmation | `orderTemplate` | 🆕 join 2800 branch |
| 2810 | ScheduleElementConfirmation | `scheduleElementOrderList` | 🔁 realign def (HC-8) |
| 2900 | AuthorizationRequest | `order` | 🆕 join `order` branch |
| 2901 | AuthorizationAccept | `authorizationAccept` | 🔁 move off `resource` branch to new `authorizationAccept` (HC-3) |
| 2902 | AuthorizationReject | — (referencesTo) | 🆕 references-only |
| 3000 | Request For Dispatch Approval | `resourceDispatch` | 🆕 join `resource` branch (HC-11) |
| 3001 | Dispatch Rejected | `resourceDispatch` | 🆕 join `resource` branch |
| 3002 | Dispatch Approval | — (referencesTo) | 🆕 references-only |
| 3003 | Dispatch Confirmation | `resourceDispatch` | ✅ (uses `resource` property) |
| 3004 | Dispatch Approval Interrupted | `resourceDispatch` | 🆕 join `resource` branch |
| 3013 | Dispatch Reservation | `resourceDispatch` | 🆕 join `resource` branch |
| 4000 | Request For Traffic Information | — (referencesTo) | ✅ (keeps `resource`, HC-13) |
| 4001 | Requested Traffic Information | `order` | ✅ |
| 4002 | Release Vehicle | — (referencesTo) | 🆕 references-only |
| 4010 | Pickup Confirmation | `pickupConfirmation` | ✅ (as `event`) |
| 4011 | Vehicle Event Accepted | — (referencesTo) | ✅ (optional `event`) |
| 4012 | Pickup Confirmation Received w/ Complaints | `manualDescriptionMsg` | ✅ (keeps optional `event`, HC-7) |
| 4020 | End Of Order | `order` | ✅ |
| 4021 | Request For End Of Order | — (referencesTo) | 🆕 references-only |
| 4031 | No Contact With Vehicle | — (referencesTo) | ✅ |
| 4040 | Client Event Confirmation | `pickupConfirmation` | 🆕 join 4010 branch (`event`) |
| 4041 | Client Event Confirmation Received (no complaints) | — (referencesTo) | 🆕 join 4011 branch (optional `event`) |
| 4042 | Client Event Confirmation Received w/ Complaints | (analogy w/ 4012) | 🆕 join 4012 branch (optional `event`) (HC-7) |
| 4100 | Request For Action | `actionRequest` | ✅ |
| 4101 | Request For Action Accepted | — (referencesTo) | 🆕 references-only |
| 4102 | Request For Action Rejected | — (referencesTo) | 🆕 references-only |
| 5000 | Message To Vehicle | `manualDescriptionMsg` | ✅ (as `messageTo`) |
| 5001 | Confirmation Message To Vehicle | — (referencesTo) | 🆕 references-only |
| 5002 | Confirmation Message To Vehicle Read | — (referencesTo) | 🆕 references-only |
| 5010 | Message To Client From Vehicle | `manualDescriptionMsg` | ✅ |
| 5011 | Message To Client From Vehicle Confirmation | — (referencesTo) | ✅ |
| 5020 | Request For Location | `locationRequest` | ✅ |
| 5021 | Requested Location | `addressLocation` | ✅ (keeps `geographicLocation`, HC-13) |
| 6001 | Order Report | `orderReport` | 🔁 realign def (HC-10) |
| 6060 | RatingRequest | — (referencesTo) | 🆕 references-only |
| 6061 | RatingResponse | `ratings` | 🆕 join 1061 branch |
| 6062 | RatingRequestReject | — (referencesTo) | 🆕 references-only |
| 6500 | DeliveryNote | `deliveryNote` | 🔁 realign def (HC-14) |
| 6501 | DeliveryNoteAccept | — (referencesTo) | 🆕 references-only |
| 6502 | DeliveryNoteReject | — (referencesTo) | 🆕 references-only |
| 6503 | DeliveryNoteWait | — (referencesTo) | 🆕 references-only |
| 6510 | DeliveryNoteRequest | — (referencesTo) | 🆕 references-only |
| 6511 | DeliveryNoteRequestReject | — (referencesTo) | 🆕 references-only |
| 6800 | RequestedOrderInformation | `orderTemplate` | 🆕 join 2800 branch |
| 6810 | RequestForOrderInformation | — (referencesTo) | 🆕 references-only |
| 7000 | Keep Alive | — (referencesTo) | ✅ |
| 7001 | Keep Alive Confirmation | — (referencesTo) | ✅ |
| 7002 | Temporary Stop | — (referencesTo) | 🆕 references-only |
| 7010 | Shutdown Service | — (referencesTo) | 🆕 references-only |
| 7011 | Shutdown Service Complete | — (referencesTo) | 🆕 references-only |
| 7015 | Shut Down Failure | — (referencesTo) | 🆕 references-only |
| 7020 | Restart Service | — (referencesTo) | 🆕 references-only |
| 7021 | Re Start | — (referencesTo) | 🆕 references-only |
| 7030 | Syntax Error | `manualDescriptionMsg` | ✅ |
| 7031 | Not Operational | `manualDescriptionMsg` | ✅ |
| 7099 | Confirmation Of Received Message | — (referencesTo) | 🆕 references-only |
| 7100 | Link Mapping Request | `order` | ✅ |
| 7101 | Link Mapping Response | `order` | ✅ |
| 8000 | Accounting Basic Provider | `accounting` | 🔁 realign def (HC-15) |
| 8010 | Accounting Reconsider Provider | `accounting` | 🆕 join 8000 branch |
| 8101 | Accounting Basic Client | `accounting` | 🆕 join 8000 branch |
| 8102 | Accounting Direct Client | `accounting` | 🆕 join 8000 branch |
| 8111 | Accounting Reconsider Client | `accounting` | 🆕 join 8000 branch |
| 8181 | Accounting Revaluate Client | `accounting` | 🆕 join 8000 branch |
| 8199 | Accounting Payment Specification | `accounting` | 🆕 join 8000 branch |

## 4. Hard choices

### HC-1 — Block 100x/101x: `resourceInformation`, not `resourceReservation`
The XSD maps msgs 1000–1002 and 1010–1012 to the `resourceInformation` element
(`resourceType`). The XSD `resourceReservation` complexType exists but is **never used**
in the `msg` choice. The current JSON schema invented a `resourceReservation` payload for
1000. Since the XSD is master and no 1000 example exists yet, 1000 is **realigned** to
`resourceInformation` (a `$ref` to the shared `resource` def) together with the five new
messages. The unused `resourceReservation` def is removed. Chosen over keeping
`resourceReservation` because the XSD explicitly documents `resourceInformation` for this
block and a single shared `resource` shape keeps request/response symmetric.

### HC-2 — 2040 Order Linked: `orderLink`, not `driverSession`
The XSD assigns 2040 the `orderLink` element (`idOrder*` + `subOrderLink*`, see "How to
use SUTI" 4.1.1.5). The current JSON schema grouped 2040 with 2100/2101 under
`driverSession`. 2040 is moved to a new `orderLink` def (`ids[]` + `subOrderLinks[]`
following the flattening convention). No 2040 example exists, so nothing breaks. Chosen
because the XSD is master and the driverSession mapping contradicts the documented
semantics (linking combined orders, not dispatching a session).

### HC-3 — 2901 AuthorizationAccept: `authorizationAccept`, not `resource`
The XSD gives 2901 a dedicated `authorizationAccept` element (`idAuthorization`,
`process` (nodeprocess), `restrictions`, `contents`). The current JSON schema grouped
2901 with 3003/4000 under `resource`. 2901 gets its own branch with a new
`authorizationAccept` def. This requires the new defs `restrictionsType` and `price`
(which 1601 also needs). Chosen because `resource` cannot express monetary/geographical
restrictions, which are the point of the message ("How to use SUTI" 4.3 flagstops).

### HC-4 — 2011 carries `cancellationConsequence`
The XSD lists `cancellationConsequence` for 2011, 2012, 2021, 2022. The current JSON
schema treats 2011 as references-only. 2011 is moved into the `cancellationConsequence`
branch (payload stays optional — acceptance without cost needs no body, matching the
existing 2011 example). Chosen over the status quo because the XSD is explicit.

### HC-5 — Realign `infoRequest`/`infoResponse` (1500/1501, 1600/1601)
The current defs (`requestType`/`idRequest`, `responseType`/`nodes[]`) do not exist in
the XSD. The XSD `infoRequest` is a **repeatable** group of
(`requestItem` choice: `requestContent`/`requestVehicle`/`requestPrice`/`requestCustomer`/
`requestOrg`, plus optional `requestCalendar`, `requestProduct`); `infoResponse` is
`responseList` (node[]), `responsePrice` (price[]), `responseOrg` (organization[]).
JSON shape: `infoRequest.requests[]` (flattening the repetition), `infoResponse`
with `nodes[]`, `prices[]`, `organizations[]`. Chosen because adding 1501/1601 (price
request/response) is impossible with the current ad-hoc defs, and the XSD is master.

### HC-6 — Realign `resourceAllocation` (1920)
The current def (`idAllocation`, `resource`, `orders[]`) does not match the XSD inline
definition: `resourceOrderid`, `resourceCapacity` (resourceType), `resourceStarttime`,
`resourceEndtime` (timesType), `resourceAddress` (addressType). JSON: `resourceOrderId`,
`resourceCapacity`, `resourceStartTime[]`, `resourceEndTime[]`, `resourceAddress`.
No example exists, so realignment is free. 1921/1922 are references-only.

### HC-7 — Complaint messages 4012/4042 keep `event`
The XSD maps 4012 to `manualDescriptionMsg` and does not list 4042 in the choice at all.
The current JSON schema already models 4012 with the optional `event` payload (three
shipped examples use it). Changing 4012 would break released examples for marginal
fidelity gain: in JSON the `event` payload already carries the disputed event, and free
text can travel in `msg` references/manual descriptions. 4042 follows 4012 by analogy;
4041 follows 4011. Documented as a conscious deviation.

### HC-8 — Realign `orderTemplate`/`scheduleElementOrderList` (2800/2801/2541/6800, 2810)
The current defs (`schedules[]` with `{idScheduleElement, order}`) do not match the XSD:
`idOrderTemplate` (with `orderTemplateName`), `orderTemplateCalendar` (required),
`orderTemplateAgreement`, and `scheduleElements` whose items carry
`scheduleElementWeekday`/`scheduleElementDate`/`scheduleElementReferencesTo`/
`scheduleElementRoute` plus attributes `scheduleElementSequenceNbr`,
`scheduleElementFunction` (Insert/Delete/Update), `scheduleElementResponse`.
JSON drops the redundant `scheduleElement` prefix (convention 2): `weekday`, `date`,
`referencesTo`, `route`, `sequenceNo`, `function`, `response`.
`scheduleElementOrderList` (2810) becomes `scheduleElementOrders[]` with `referencesTo`,
`date`, `orderListClosed`. No examples exist for these messages, so realignment is free.

### HC-9 — 2111/2112 use `cancellationConsequence` by documented analogy
The XSD does not give the 21xx cancellation flow a payload, but SUTI_Messages.pdf states:
"From msg 2101 and the rest of 21xx messages are identical with the corresponding 20xx
messages." Therefore 2111/2112 mirror 2011/2012 (`cancellationConsequence`, optional),
while 2103–2107, 2110, 2113 mirror their references-only 20xx counterparts. Chosen over
references-only because the PDF explicitly defines the 21xx block as analogous.

### HC-10 — Realign `orderReport` (6001 + new 2531)
XSD `orderReport`: `eventReport` (event[]), `summaryReport+`, `economyReport*`,
`orderStatus`, `resourceReport`. The JSON def already flattens `eventReport` → `events[]`
(convention 3); `orderStatus` and `resourceReport` ($ref `resource`) are added.
`summaryReport` is realigned to the XSD attributes: `vehicle`, `durationStart`,
`distanceStart`, `orderEnded`, `subOrders[]` (was an invented
`nodeSeqNo`/`contentSeqNo`/`status`/`times` shape). `economyReport` is realigned to
`payments[]` (formOfPayment, required in XSD), `subOrders[]`, `nodeSeqNo` (was an
invented `amount`/`distance`/`duration` shape). No 6001/2531 examples exist.

### HC-11 — Dispatch block shares the `resource` property
The XSD types 1020, 3000, 3001, 3003, 3004, 3013 all as `resourceDispatch`
(resourceType). The JSON schema already renamed this payload to `resource` for 3003 and
kept `resourceDispatch` for 1020 (with a released example each). Rather than renaming
either released spelling, the new dispatch messages 3000/3001/3004/3013 join the existing
3003 `resource` branch. Chosen over unifying names because both released spellings stay
valid; the duplication is cosmetic.

### HC-12 — 1120/1121/1122 are references-only
These codes are in the XSD enumeration but absent from SUTI_Messages.pdf and from the
`msg` choice. Following the XSD rule ("If a message is not explicitly mentioned in XSD it
only uses referencesTo"), they are added as references-only so that the enum is complete
and validators reject nothing the master allows.

### HC-13 — Existing deviations kept for backward compatibility
These released mappings deviate from the XSD but have shipped examples; they are kept
as-is and documented here: 1023 `resourceDispatch` (XSD: references-only), 1022 gets the
XSD-documented `messageTo` *added* (optionally), 2030 `orderForward` payload (XSD:
references-only via `idOrderForward`), 4000 `resource` (XSD: references-only), 5021
`geographicLocation` (XSD: `addressLocation` — the JSON choice is the more common
implementation), 4010-family `event` instead of `pickupConfirmation`.

### HC-14 — Realign `deliveryNote` (6500)
XSD: `idReceipt` (required), `agreementDeliveryNote`, `eventReportDeliveryNote`,
`summaryReportDeliveryNote` (required), `economyReportDeliveryNote*`, attribute
`deliveryNoteType` (debit/credit). JSON: `idReceipt`, `agreement`, `events[]`,
`summaryReport` (required), `economyReports[]`, `deliveryNoteType` enum. The invented
`idDeliveryNote`/`order`/`resource` shape is dropped. No 6500 example exists. 6501–6511
are references-only.

### HC-15 — Realign `accounting` (8000 family)
The current def has a placeholder `tours[]` ({idTour, orders[]}). The XSD `tour` is rich:
`referencesToTour`, `statusTour` (`idActivity`, `statusTourError[]`,
`manualDescriptionStatus[]`), `suborderTour[]`, `calculationsTour`
(`calculationFare[]`), `summaryReportTour`, `economyReportTour[]`, `resourceTour`,
`eventTour[]`. New defs: `tour` (realigned), `statusTour`, `errorType`, `suborderTour`,
`calculationFare` (with `fixedPriceAmount` XOR `taximeterAmount` via `oneOf`),
`tourEvent`. JSON names drop the `...Tour` suffix inside `tour` (convention 2).
The existing `organization`/`orgPayment` defs already match `organizationType` and are
reused. 8182 is excluded (not in the XSD enumeration).

### HC-16 — `msgName` and `clientContactReference` added to `msg`
The XSD `msg` has an optional `msgName` attribute and a `ClientContactReference` element.
Both are added as optional `msgName` / `clientContactReference` properties on the `msg`
def — cheap parity with the master, no impact on existing examples.

## 5. New and changed `$defs`

**New:** `price`, `taxiMeter`, `priceCalculation`, `restrictionsType`,
`authorizationAccept`, `orderLink`, `tour` (replaces placeholder), `statusTour`,
`errorType`, `suborderTour`, `calculationFare`, `tourEvent`.

**Realigned:** `infoRequest`, `infoResponse`, `resourceAllocation`, `orderTemplate`,
`scheduleElement`, `scheduleElementOrderList`, `orderReport`, `summaryReport`,
`economyReport`, `deliveryNote`, `accounting`.

**Removed:** `resourceReservation` (HC-1).

**Branch changes:**
- `resourceInformation` (resource): 1000, 1001, 1002, 1010, 1011, 1012 — payload required
  for 1010/1011/1012 responses; optional for 1000–1002 requests (a request may narrow
  scope purely via `referencesTo`).
- `messageTo` added (optional): 1022, 1025.
- References-only: 1024, 1060, 1062, 1120–1122, 1921, 1922, 2003, 2005–2007, 2013, 2023,
  2031, 2032, 2050, 2061, 2103–2107, 2110, 2113, 2530, 2532, 2540, 2902, 3002, 4002,
  4021, 4101, 4102, 5001, 5002, 6060, 6062, 6501–6503, 6510, 6511, 6810, 7002, 7010,
  7011, 7015, 7020, 7021, 7099.
- `bulkLocationRequest`: +1101, +1102. `bulkLocationList`: +1110.
- `ratings`: +6061.
- `cancellationConsequence`: +2011, +2021, +2022, +2111, +2112.
- `order` (required): +2900.
- `orderLink` (required): 2040.
- `authorizationAccept` (required): 2901.
- `resource`: +3000, +3001, +3004, +3013.
- `event` required: +4040; `event` optional: +4041, +4042.
- `orderReport` (required): +2531.
- `orderTemplate` (required): +2801, +2541, +6800.
- `accounting` (required): +8010, +8101, +8102, +8111, +8181, +8199.
- `msgTypeEnum`: extended to all 136 XSD codes (8182 excluded, HC-15).

## 6. Examples plan

Location: `examples/JSON/2026/`, naming `<msgType>_<camelCaseName>.json`, each with a
`$schema` pointer to the schema, following the style of the existing files.

**Hand-written examples** (one per payload-carrying message):
1000, 1001, 1002, 1010, 1011, 1012, 1025, 1101, 1102, 1110, 1501, 1601, 1921, 1922,
2040, 2111, 2112, 2531, 2801, 2900, 2901, 3000, 3001, 3004, 3013, 4040, 4041, 4042,
6061, 6501, 6800, 8010 (plus updated 1500/1600-style coverage via 1501/1601 examples).

**Generated references-only examples** (small, template-based): 1024, 1060, 1062, 1120,
1121, 1122, 2003, 2005, 2006, 2007, 2013, 2021, 2022, 2023, 2031, 2032, 2050, 2061,
2103, 2104, 2105, 2106, 2107, 2110, 2113, 2530, 2532, 2540, 2902, 3002, 4002, 4021,
4101, 4102, 5001, 5002, 6060, 6062, 6502, 6503, 6510, 6511, 6810, 7002, 7010, 7011,
7015, 7020, 7021, 7099.

(2021/2022 are listed with the generated set — they carry an optional
`cancellationConsequence` but their minimal form is references-only.)

**Example updates:** `2011_orderCancellationAccepted.json` gains an optional
`cancellationConsequence` variant if needed (minimal form still validates).

## 7. Execution checklist

1. ✅ Analysis (this document)
2. ✅ `$defs`: add new + realign existing (section 5)
3. ✅ `msgTypeEnum`: extended to all 136 XSD codes
4. ✅ Branches: added/reworked per section 5, then corrected per the 2026-08-13
   decisions (payloads made optional; XSD deviations removed)
5. ✅ Hand-written examples (payload messages)
6. ✅ Generated references-only examples
7. ✅ Validated every example in `examples/JSON/2026/` against the updated schema
   (122/122 non-legacy examples pass; the legacy example passes its own schema)
