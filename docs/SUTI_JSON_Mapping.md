# SUTI JSON Mapping (normative)

Generated from `schemas/SUTI_Message.schema.json` (version 2026.1) on 2026-08-21.

Master: [schemas/SUTI_Message.xsd](../schemas/SUTI_Message.xsd). The JSON Schema is an XSD-derived representation: it never rejects an XSD-valid message, and every JSON-only extension is listed in §2.

This document supersedes the message tables in [JSON_SCHEMA_COMPLETION_PLAN.md](JSON_SCHEMA_COMPLETION_PLAN.md), which is kept as the decision record.

## 1. Message type → payload

`–` means references-only: the message carries `msg` (with `referencesTo`) and no payload. Payload properties are always optional (XSD `msg` choice is `minOccurs="0"`). Footnotes mark JSON extensions (§2).

| msgType | Name | JSON payload property | XSD element | Example(s) |
|---|---|---|---|---|
| 1000 | SingleResourceRequest | `resourceInformation` | `resourceInformation` | `1000_singleResourceRequest.json` |
| 1001 | AgreementResourcesRequest | `resourceInformation` | `resourceInformation` | `1001_agreementResourcesRequest.json` |
| 1002 | AllResourcesRequest | `resourceInformation` | `resourceInformation` | `1002_allResourcesRequest.json` |
| 1010 | SingleResourceResponse | `resourceInformation` | `resourceInformation` | `1010_singleResourceResponse.json` |
| 1011 | AgreementResourceResponse | `resourceInformation` | `resourceInformation` | `1011_agreementResourceResponse.json` |
| 1012 | AllResourceResponse | `resourceInformation` | `resourceInformation` | `1012_allResourceResponse.json` |
| 1020 | Resource Login | `resourceDispatch` | `resourceDispatch` | `1020_resourceLogin.json` |
| 1021 | Resource Login Confirmation | – | – (referencesTo only) | `1021_resourceLoginConfirm.json` |
| 1022 | Resource Login Reject | `messageTo` | `manualDescriptionMsg` | `1022_resourceLoginReject.json` |
| 1023 | Resource Logoff | – | – (referencesTo only) | `1023_resourceLogoff.json` |
| 1024 | Resource Logoff Confirmation | – | – (referencesTo only) | `1024_resourceLogoffConfirmation.json` |
| 1025 | Resource Logoff Reject | `messageTo` | `manualDescriptionMsg` | `1025_resourceLogoffReject.json` |
| 1060 | RatingRequest | – | – (referencesTo only) | `1060_ratingRequest.json` |
| 1061 | RatingResponse | `ratings` | `ratings` | (payload-family example) |
| 1062 | RatingRequestReject | – | – (referencesTo only) | `1062_ratingRequestReject.json` |
| 1100 | SingleBulkLocationRequest | `bulkLocationRequest` | `bulkLocationRequest` | (payload-family example) |
| 1101 | AgreementBulkLocationRequest | `bulkLocationRequest` | `bulkLocationRequest` | `1101_agreementBulkLocationRequest.json` |
| 1102 | AllBulkLocationRequest | `bulkLocationRequest` | `bulkLocationRequest` | `1102_allBulkLocationRequest.json` |
| 1110 | SingleBulkLocationResponse | `bulkLocationList` | `bulkLocation` | `1110_singleBulkLocationResponse.json` |
| 1111 | AgreementBulkLocationResponse | `bulkLocationList` | `bulkLocation` | `1111_bulkLocationResponse.json`, `1111_bulkLocationResponse.legacy.json` |
| 1112 | AllBulkLocationResponse | `bulkLocationList` | `bulkLocation` | (payload-family example) |
| 1120 | (reserved, undocumented) | – | – (referencesTo only) | `1120.json` |
| 1121 | (reserved, undocumented) | – | – (referencesTo only) | `1121.json` |
| 1122 | (reserved, undocumented) | – | – (referencesTo only) | `1122.json` |
| 1500 | NodeListRequest | `infoRequest` | `infoRequest` | (payload-family example) |
| 1501 | PriceRequest | `infoRequest` | `infoRequest` | `1501_priceRequest.json` |
| 1600 | NodeListResponse | `infoResponse` | `infoResponse` | (payload-family example) |
| 1601 | PriceResponse | `infoResponse` | `infoResponse` | `1601_priceResponse.json` |
| 1920 | Resource Allocation | `resourceAllocation` | `resourceAllocation` | `1920_resourceAllocation.json` |
| 1921 | Resource Allocation Accept | – | – (referencesTo only) | `1921_resourceAllocationAccept.json` |
| 1922 | Resource Allocation Reject | – | – (referencesTo only) | `1922_resourceAllocationReject.json` |
| 2000 | Order | `order` | `order` | `2000_multiOrder.json`, `2000_order.json`, `2000_orderAlter.json`, `2000_order_maximized.json`, `2000_trip.json` |
| 2001 | Order Confirmation | – | – (referencesTo only) | `2001_orderConfirmation.json` |
| 2002 | Order Reject | `orderReject` | `orderReject` | `2002_orderReject.json` |
| 2003 | Order Reject Confirmation | – | – (referencesTo only) | `2003_orderRejectConfirmation.json` |
| 2005 | Order Reject Request | – | – (referencesTo only) | `2005_orderRejectRequest.json` |
| 2006 | Order Reject Request Accepted | – | – (referencesTo only) | `2006_orderRejectRequestAccepted.json` |
| 2007 | Order Reject Request Reject | – | – (referencesTo only) | `2007_orderRejectRequestReject.json` |
| 2010 | Order Cancellation Request | – | – (referencesTo only) | `2010_orderCancellation.json` |
| 2011 | Order Cancellation Accepted | `cancellationConsequence` | `cancellationConsequence` | `2011_orderCancellationAccepted.json` |
| 2012 | Order Cancellation Accepted w/ Consequence | `cancellationConsequence` | `cancellationConsequence` | (payload-family example) |
| 2013 | Order Cancellation Reject | – | – (referencesTo only) | `2013_orderCancellationReject.json` |
| 2020 | Node Cancellation Request | `nodeCancellation` | `nodeCancellation` | (payload-family example) |
| 2021 | Node Cancellation Accepted | `cancellationConsequence` | `cancellationConsequence` | `2021_nodeCancellationAccepted.json` |
| 2022 | Node Cancellation Accepted w/ Consequence | `cancellationConsequence` | `cancellationConsequence` | `2022_nodeCancellationAcceptedWithConsequence.json` |
| 2023 | Node Cancellation Reject | – | – (referencesTo only) | `2023_nodeCancellationReject.json` |
| 2030 | Order Forward | – | – (referencesTo only) | (payload-family example) |
| 2031 | Order Forwarded Reject | – | – (referencesTo only) | `2031_orderForwardedReject.json` |
| 2032 | Order Forwarded Received | – | – (referencesTo only) | `2032_orderForwardedReceived.json` |
| 2040 | Order Linked | `orderLink` | `orderLink` | `2040_orderLinked.json` |
| 2050 | Order Freeze | – | – (referencesTo only) | `2050_orderFreeze.json` |
| 2060 | Provider Update Order | `providerOrderUpdate` | `providerOrderupdate` | (payload-family example) |
| 2061 | Confirmation Provider Update Order | – | – (referencesTo only) | `2061_providerOrderUpdateConfirmation.json` |
| 2100 | DriverSession | `driverSession` | `driverSession` | `2100_driverSession.json` |
| 2101 | DriverSession Confirmation | `driverSession` | `driverSession` | (payload-family example) |
| 2102 | DriverSession Reject | `driverSessionReject` | `driverSessionReject` | `2102_driverSessionReject.json` |
| 2103 | DriverSession Reject Confirmation | – | – (referencesTo only) | `2103_driverSessionRejectConfirmation.json` |
| 2104 | DriverSession Synchronization Request | – | – (referencesTo only) | `2104_driverSessionSynchronizationRequest.json` |
| 2105 | DriverSession Reject Request | – | – (referencesTo only) | `2105_driverSessionRejectRequest.json` |
| 2106 | DriverSession Reject Request Accepted | – | – (referencesTo only) | `2106_driverSessionRejectRequestAccepted.json` |
| 2107 | DriverSession Reject Request Reject | – | – (referencesTo only) | `2107_driverSessionRejectRequestReject.json` |
| 2110 | DriverSession Cancellation Request | – | – (referencesTo only) | `2110_driverSessionCancellationRequest.json` |
| 2111 | DriverSession Cancellation Accepted | `cancellationConsequence` ² | – (referencesTo only) | `2111_driverSessionCancellationAccepted.json` |
| 2112 | DriverSession Cancellation Accepted w/ Consequence | `cancellationConsequence` ² | – (referencesTo only) | `2112_driverSessionCancellationAcceptedWithConsequence.json` |
| 2113 | DriverSession Cancellation Reject | – | – (referencesTo only) | `2113_driverSessionCancellationReject.json` |
| 2530 | OrderStatusRequest | – | – (referencesTo only) | `2530_orderStatusRequest.json` |
| 2531 | OrderStatus | `orderReport` | `orderReport` | `2531_orderStatus.json` |
| 2532 | OrderStatusReject | – | – (referencesTo only) | `2532_orderStatusReject.json` |
| 2540 | RequestForOrderInfo | – | – (referencesTo only) | `2540_requestForOrderInfo.json` |
| 2541 | OrderInfo | `orderTemplate` | `orderTemplate` | (payload-family example) |
| 2800 | OrderTemplate | `orderTemplate` | `orderTemplate` | (payload-family example) |
| 2801 | OrderTemplateConfirmation | `orderTemplate` | `orderTemplate` | `2801_orderTemplateConfirmation.json` |
| 2810 | ScheduleElementConfirmation | `scheduleElementOrderList` | `scheduleElementOrderList` | (payload-family example) |
| 2900 | AuthorizationRequest | `order` | `order` | `2900_authorizationRequest.json` |
| 2901 | AuthorizationAccept | `authorizationAccept` | `authorizationAccept` | `2901_authorizationAccept.json` |
| 2902 | AuthorizationReject | – | – (referencesTo only) | `2902_authorizationReject.json` |
| 3000 | Request For Dispatch Approval | `resourceDispatch` | `resourceDispatch` | `3000_requestForDispatchApproval.json` |
| 3001 | Dispatch Rejected | `resourceDispatch` | `resourceDispatch` | `3001_dispatchRejected.json` |
| 3002 | Dispatch Approval | – | – (referencesTo only) | `3002_dispatchApproval.json` |
| 3003 | Dispatch Confirmation | `resourceDispatch` | `resourceDispatch` | `3003_dispatchConfirmation.json` |
| 3004 | Dispatch Approval Interrupted | `resourceDispatch` | `resourceDispatch` | `3004_dispatchApprovalInterrupted.json` |
| 3013 | Dispatch Reservation | `resourceDispatch` | `resourceDispatch` | `3013_dispatchReservation.json` |
| 4000 | Request For Traffic Information | – | – (referencesTo only) | (payload-family example) |
| 4001 | Requested Traffic Information | `order` | `order` | (payload-family example) |
| 4002 | Release Vehicle | – | – (referencesTo only) | `4002_releaseVehicle.json` |
| 4010 | Pickup Confirmation | `pickupConfirmation` | `pickupConfirmation` | `4010_bom.json`, `4010_drop.json`, `4010_eventVehicle.json` |
| 4011 | Vehicle Event Accepted | `event` ¹ | – (referencesTo only) | `4011_vehicleEventAccepted.json` |
| 4012 | Pickup Confirmation Received w/ Complaints | `messageTo` | `manualDescriptionMsg` | `4012_bomRejected.json`, `4012_drop.json`, `4012_pickup.json` |
| 4020 | End Of Order | `order` | `order` | `4020_endOfOrder.json` |
| 4021 | Request For End Of Order | – | – (referencesTo only) | `4021_requestForEndOfOrder.json` |
| 4031 | No Contact With Vehicle | – | – (referencesTo only) | `4031_noContactWithVehicle.json` |
| 4040 | Client Event Confirmation | `pickupConfirmation` | `pickupConfirmation` | `4040_clientEventConfirmation.json` |
| 4041 | Client Event Confirmation Received (no complaints) | – | – (referencesTo only) | `4041_clientEventConfirmationReceived.json` |
| 4042 | Client Event Confirmation Received w/ Complaints | – | – (referencesTo only) | `4042_clientEventConfirmationReceivedWithComplaints.json` |
| 4100 | Request For Action | `actionRequest` | `actionRequest` | (payload-family example) |
| 4101 | Request For Action Accepted | – | – (referencesTo only) | `4101_requestForActionAccepted.json` |
| 4102 | Request For Action Rejected | – | – (referencesTo only) | `4102_requestForActionRejected.json` |
| 5000 | Message To Vehicle | `messageTo` | `manualDescriptionMsg` | `5000_messageToVehicle.json` |
| 5001 | Confirmation Message To Vehicle | – | – (referencesTo only) | `5001_messageToVehicleConfirmation.json` |
| 5002 | Confirmation Message To Vehicle Read | – | – (referencesTo only) | `5002_messageToVehicleRead.json` |
| 5010 | Message To Client From Vehicle | `messageTo` | `manualDescriptionMsg` | `5010_messageFromVehicle.json` |
| 5011 | Message To Client From Vehicle Confirmation | – | – (referencesTo only) | `5011_messageFromVehicleConfirm.json` |
| 5020 | Request For Location | `locationRequest` | `locationRequest` | `5020_locationRequest.json` |
| 5021 | Requested Location | `geographicLocation` ³, `addressLocation` | `addressLocation` | `5021_locationResponse.json` |
| 6001 | Order Report | `orderReport` | `orderReport` | (payload-family example) |
| 6060 | RatingRequest | – | – (referencesTo only) | `6060_ratingRequest.json` |
| 6061 | RatingResponse | `ratings` | `ratings` | `6061_ratingResponse.json` |
| 6062 | RatingRequestReject | – | – (referencesTo only) | `6062_ratingRequestReject.json` |
| 6500 | DeliveryNote | `deliveryNote` | `deliveryNote` | `6500_deliveryNote.json` |
| 6501 | DeliveryNoteAccept | – | – (referencesTo only) | `6501_deliveryNoteAccept.json` |
| 6502 | DeliveryNoteReject | – | – (referencesTo only) | `6502_deliveryNoteReject.json` |
| 6503 | DeliveryNoteWait | – | – (referencesTo only) | `6503_deliveryNoteWait.json` |
| 6510 | DeliveryNoteRequest | – | – (referencesTo only) | `6510_deliveryNoteRequest.json` |
| 6511 | DeliveryNoteRequestReject | – | – (referencesTo only) | `6511_deliveryNoteRequestReject.json` |
| 6800 | RequestedOrderInformation | `orderTemplate` | `orderTemplate` | `6800_requestedOrderInformation.json` |
| 6810 | RequestForOrderInformation | – | – (referencesTo only) | `6810_requestForOrderInformation.json` |
| 7000 | Keep Alive | – | – (referencesTo only) | `7000_keepAlive.json` |
| 7001 | Keep Alive Confirmation | – | – (referencesTo only) | `7001_keepAliveConfirmation.json` |
| 7002 | Temporary Stop | – | – (referencesTo only) | `7002_temporaryStop.json` |
| 7010 | Shutdown Service | – | – (referencesTo only) | `7010_shutdownService.json` |
| 7011 | Shutdown Service Complete | – | – (referencesTo only) | `7011_shutdownServiceComplete.json` |
| 7015 | Shut Down Failure | – | – (referencesTo only) | `7015_shutdownFailure.json` |
| 7020 | Restart Service | – | – (referencesTo only) | `7020_restartService.json` |
| 7021 | Re Start | – | – (referencesTo only) | `7021_reStart.json` |
| 7030 | Syntax Error | `messageTo` | `manualDescriptionMsg` | `7030_syntaxError.json` |
| 7031 | Not Operational | `messageTo` | `manualDescriptionMsg` | `7031_notOperational.json` |
| 7099 | Confirmation Of Received Message | – | – (referencesTo only) | `7099_confirmationOfReceivedMessage.json` |
| 7100 | Link Mapping Request | `order` | `order` | `7100_linkMappingRequest.json` |
| 7101 | Link Mapping Response | `order` | `order` | `7101_linkMappingResponse.json` |
| 8000 | Accounting Basic Provider | `accounting` | `accounting` | `8000_accountingBasicProvider.json` |
| 8010 | Accounting Reconsider Provider | `accounting` | `accounting` | `8010_accountingReconsiderProvider.json` |
| 8101 | Accounting Basic Client | `accounting` | `accounting` | (payload-family example) |
| 8102 | Accounting Direct Client | `accounting` | `accounting` | (payload-family example) |
| 8111 | Accounting Reconsider Client | `accounting` | `accounting` | (payload-family example) |
| 8181 | Accounting Revaluate Client | `accounting` | `accounting` | (payload-family example) |
| 8199 | Accounting Payment Specification | `accounting` | `accounting` | (payload-family example) |

¹ JSON extension: XSD has no payload for 4011; optional `event` kept for the released 4011 examples.  
² JSON extension by documented analogy (SUTI_Messages.pdf: 21xx ≙ 20xx).  
³ JSON extension: accepted alongside the XSD payload `addressLocation`.

## 2. JSON extensions beyond the XSD

These are the only places where the JSON Schema accepts something the XSD does not. All are permissive (JSON is never stricter than the XSD).

| Where | Extension | Status | Rationale |
|---|---|---|---|
| 4011 | optional `event` payload | tolerated, legacy | XSD: references-only. Kept for released 4011 examples (three variants). Candidate for removal when 4011 examples are re-issued. |
| 2111, 2112 | optional `cancellationConsequence` | normative by analogy | SUTI_Messages.pdf: "From msg 2101 and the rest of 21xx messages are identical with the corresponding 20xx messages." |
| 5021 | `geographicLocation` accepted alongside `addressLocation` | tolerated, legacy | XSD payload is `addressLocation`; `geographicLocation` is the common implementation shape. |
| `msg.referencesTo` | array of reference groups | normative JSON form | XSD has one `referencesTo` element; JSON groups equivalent IDs. One XML `referencesTo` ≙ one or more JSON groups. |
| 1120–1122 | references-only branches | reserved | In the XSD enumeration but undocumented; accepted per the XSD rule "if a message is not explicitly mentioned it only uses referencesTo". |

## 3. Naming conventions and renames

General rules (see [examples/JSON/README.md](../examples/JSON/README.md)): XSD attributes and elements become properties; wrapper elements are flattened to arrays; redundant prefixes/suffixes are dropped; numeric enumeration codes are dropped and values are camelCased.

| JSON | XSD | Note |
|---|---|---|
| `resourceDispatch` (1020, 3000, 3001, 3003, 3004, 3013) | `resourceDispatch` (resourceType) | One property name for all dispatch messages; shape is `$defs.resource`. |
| `resourceInformation` (100x, 101x) | `resourceInformation` (resourceType) | Same `$defs.resource` shape. |
| `messageTo` | `manualDescriptionMsg` | |
| `bulkLocationList` | `bulkLocation` | Separately adopted JSON representation; unchanged. |
| `providerOrderUpdate.updateType: "cancelation"` | `providerOrderupdate/@updateType="cancelation"` | XSD spelling retained. |
| `geographicLocation.lon` | `@long` | |
| `price.priceValue` | `price/@price` | Avoids `price.price`. |
| `tour.events[].eventVehicle` | `eventTour/@eventVehicle` | Attribute name retained; values camelCased (`dispatchConfirmationSent`). |
| `locationRequest.{timeFrom, timeTo, interval.seconds, interval.meter}` | `locationRequest/{timeFrom, timeTo, interval/@seconds, interval/@meter}` | Used by 5020 and by `bulkLocationRequest.bulkIntervalRequest` (1100–1102). |
| `contactInfo.contactValue` | `contactInfo/@contactInfo` | |
| `msg.msgTimeStamp` (string) | `msgTimeStamp/time/@time` (timesType) | JSON keeps a single ISO timestamp; XSD wraps it in `timesType`. |
| `event.eventNode` | – | **JSON-only.** XSD `event` carries only `@nodeSeqNo`; `eventNode.nodeType` has no XSD counterpart. Pre-existing (4011 examples); candidate for removal or XSD extension. |
| `orderReport.events[]`, `deliveryNote.events[]` | `eventReport/event`, `eventReportDeliveryNote/event` | Wrapper flattened. |
| `summaryReports[]`, `economyReports[]`, `payments[]` | `summaryReport+`, `economyReport*`, `formOfPayment/payment+` | Wrapper flattened. |
| `idOrder` in `referencesTo` groups | `referencesTo/idOrder*` | Array (XSD `maxOccurs="unbounded"`). |

## 4. Verification

1. Every file in `examples/JSON/2026/` validates against its referenced schema (Draft 2020-12).
2. XML/JSON fixture pairs exist for the high-risk payload families. The XML validates against the XSD and carries the same values as the JSON:

| Family | XML | JSON |
|---|---|---|
| Order status / report | `examples/XML/2531_OrderStatus.xml` | `examples/JSON/2026/2531_orderStatus.json` |
| Delivery note | `examples/XML/6500_DeliveryNote.xml` | `examples/JSON/2026/6500_deliveryNote.json` |
| Accounting | `examples/XML/8000_AccountingBasicProvider.xml` | `examples/JSON/2026/8000_accountingBasicProvider.json` |
| Price request | `examples/XML/1501_PriceRequest.xml` | `examples/JSON/2026/1501_priceRequest.json` |
| Price response | `examples/XML/1601_PriceResponse.xml` | `examples/JSON/2026/1601_priceResponse.json` |
| Authorization accept | `examples/XML/2901_AuthorizationAccept.xml` | `examples/JSON/2026/2901_authorizationAccept.json` |

Pairs are compared value-by-value (name-agnostic): every attribute/text value in the XML must occur in the JSON and vice versa, after normalising booleans, numbers and enumeration case. Result 2026-08-21: all six XML files validate against the XSD; 6500, 1501, 1601 and 2901 are value-identical to their JSON twins; 2531 and 8000 differ only by the JSON-only `event.eventNode.nodeType` values (see §3). Known differences are also listed in each XML file's header comment.

Families still without an XML reference in this repository: 2040 `orderLink`, 2102 `driverSessionReject`, 2800/2810 order templates, 1920 `resourceAllocation`. The Technical Board should supply XML reference messages for these before their JSON shapes are treated as verified.
