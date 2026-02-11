# JSON Schema Feature Completeness Plan

**Date:** 2026-02-10
**Version:** 1.1 (Revised after Bengt review)
**Status:** Ready for Execution
**Goal:** Ensure JSON Schema is 100% feature-complete compared to XSD before deployment

### Revision Notes (v1.1)
- Added Phase 0: Discovery & Verification (per Bengt review)
- Corrected body type mappings based on XML example analysis
- Added verification criteria for Phase 1 type checking
- Added regression testing strategy
- Added detailed transformation guide for examples
- Resolved "TBD" for msgType 4031 (header-only)

---

## Executive Summary

| Metric | XSD/XML | JSON Schema | Gap | Action |
|--------|---------|-------------|-----|--------|
| Complex Types | 86 | 65 definitions | ~21 types | Verify all mappings |
| Message Types | 18 in XML examples | 35 in schema | **16 missing** | Add to schema |
| XML Examples | 37 files | 12 JSON files | 25 examples | Create examples |
| Line Count | 3131 | 1408 | N/A | Expected (JSON more compact) |

### Critical Blockers

**16 msgTypes in XML examples are NOT in JSON schema:**
- Resource: 1020, 1021, 1022, 1023
- Order Cancellation: 2010, 2011
- Vehicle Events: 4011, 4012, 4020, 4031
- Messages: 5010, 5011
- Errors/Link: 7030, 7031, 7100, 7101

---

## Phase 0: Discovery & Verification (PREREQUISITE)

> **Added per Bengt review:** Before adding msgTypes, verify all assumed body types exist.

### 0.1 Body Type Verification Results

Based on XML example analysis (2026-02-10):

| msgType | XML Element | Verified Body Type | $def Exists? |
|---------|-------------|-------------------|--------------|
| **1020** | `<resourceDispatch>` | resourceDispatch | ❌ **CREATE** |
| **1021** | *(header only)* | null | ✅ N/A |
| **1022** | *(header only)* | null | ✅ N/A |
| **1023** | `<resourceDispatch>` | resourceDispatch | ❌ **CREATE** |
| **2010** | *(header only)* | null | ✅ N/A |
| **2011** | *(header only)* | null | ✅ N/A |
| **4011** | `<pickupConfirmation>` | event | ✅ Exists |
| **4012** | `<pickupConfirmation>` | event | ✅ Exists |
| **4020** | `<order>` | order | ✅ Exists |
| **4031** | *(header only)* | null | ✅ N/A |
| **5010** | `<manualDescriptionMsg>` | messageTo | ✅ Exists |  <!-- Fixed: schema uses messageTo -->
| **5011** | *(header only)* | null | ✅ N/A |
| **7030** | `<manualDescriptionMsg>` | manualDescription | ✅ Exists |
| **7031** | `<manualDescriptionMsg>` | manualDescription | ✅ Exists |
| **7100** | `<order>` (complex) | order | ✅ Exists |
| **7101** | `<order>` (complex) | order | ✅ Exists |

### 0.2 Missing $defs to Create

**BLOCKER:** Before adding msgTypes 1020 and 1023, create `resourceDispatch` $def:

```json
"resourceDispatch": {
  "type": "object",
  "properties": {
    "vehicle": { "$ref": "#/$defs/vehicleResource" },
    "driver": { "$ref": "#/$defs/driverResource" },
    "manualDescription": { "$ref": "#/$defs/manualDescription" },
    "resourceValidation": { "type": "object" }
  },
  "additionalProperties": false
}
```

### 0.3 Existing $defs Count

Current JSON Schema has **65 $defs** (verified 2026-02-10):
```
accounting, actionRequest, address, agreement, amount, bulkLocationList,
bulkLocationRequest, calendar, cancellationConsequence, capacity, capacityItem,
contactInfo, content, deliveryNote, driverResource, driverSession, driverSessionReject,
driverSpec, economy, economyReport, event, geographicLocation, id, infoRequest,
infoResponse, locationRequest, manualDescription, messageTo, mobilityAid, msg, node,
nodeCancellation, nodeProcess, order, orderForward, orderReject, orderReport,
orderStatus, orderTemplate, org, orgPayment, organization, payment, period, process,
product, providerOrderUpdate, rating, ratingList, referenceToMsg, resource,
resourceAllocation, resourceReservation, resourceSpec, route, scheduleElement,
scheduleElementOrderList, subOrder, summaryReport, time, tour, vehicleLocation,
vehicleResource, vehicleSpec, weekdays
```

### 0.4 Phase 0 Checklist

- [x] Create `resourceDispatch` $def in JSON schema ✅ (2026-02-11)
- [x] Verify `event` $def has `eventType` and `nodeConfirmed` properties for 4011/4012 ✅ (uses existing event $def)
- [ ] Verify `manualDescription` $def has `manualText` and boolean flags
- [ ] Run regression test on all 12 existing examples
- [ ] Document any XSD features not mappable to JSON

---

## Phase 1: XSD Type-by-Type Verification

### 1.1 Methodology

For each XSD `complexType`:
1. Locate corresponding JSON Schema `$def`
2. Compare all attributes/elements
3. Document any missing properties
4. Flag semantic differences

### 1.2 Verification Criteria (per Bengt review)

For each type mapping, verify:

**Structural Equivalence:**
- [ ] All XSD elements mapped to JSON properties
- [ ] All XSD attributes mapped to JSON properties
- [ ] Cardinality preserved (`minOccurs`/`maxOccurs` → `required`/arrays)

**Semantic Equivalence:**
- [ ] Data types compatible (XSD → JSON type)
- [ ] Enumerations match (with documented transformations)
- [ ] Constraints preserved (patterns, min/max values)

**Documentation:**
- [ ] Mapping documented in xsd-json-mapping.yaml
- [ ] Differences explained (e.g., "wrapper removed")
- [ ] Any XSD features not mappable to JSON noted

### 1.3 XSD Complex Types Checklist

#### Core Message Types
| XSD Type | JSON $def | Status | Notes |
|----------|-----------|--------|-------|
| `msg` | `msg` | ⬜ Verify | |
| `idType` | `id` | ⬜ Verify | |
| `idMsgRef` | `referenceToMsg` | ⬜ Verify | |
| `idEkInfo` | *(check if needed)* | ⬜ Verify | |
| `orgType` | `org` | ⬜ Verify | |
| `referencesTo` | *(inline in msg)* | ⬜ Verify | |

#### Order-Related Types
| XSD Type | JSON $def | Status | Notes |
|----------|-----------|--------|-------|
| `order` | `order` | ⬜ Verify | |
| `orderReject` | `orderReject` | ⬜ Verify | |
| `orderStatus` | `orderStatus` | ⬜ Verify | |
| `orderLink` | *(check if needed)* | ⬜ Verify | |
| `orderReport` | `orderReport` | ⬜ Verify | |
| `subOrderType` | `subOrder` | ⬜ Verify | |

#### Route/Node Types
| XSD Type | JSON $def | Status | Notes |
|----------|-----------|--------|-------|
| `route` | `route` | ⬜ Verify | |
| `node` | `node` | ⬜ Verify | |
| `nodeprocess` | `nodeProcess` | ⬜ Verify | |
| `nodeCancelationType` | `nodeCancellation` | ⬜ Verify | Spelling correction |
| `nodeCancellationType` | `nodeCancellation` | ⬜ Verify | |

#### Resource Types
| XSD Type | JSON $def | Status | Notes |
|----------|-----------|--------|-------|
| `resourceType` | `resource` | ⬜ Verify | |
| `vehicle` | `vehicleResource` | ⬜ Verify | |
| `driver` | `driverResource` | ⬜ Verify | |
| `capacity` | `capacity` | ⬜ Verify | |
| `seats` | `capacityItem` | ⬜ Verify | |
| `position` | *(check if needed)* | ⬜ Verify | |
| `resourceReservation` | `resourceReservation` | ⬜ Verify | |

#### Content Types
| XSD Type | JSON $def | Status | Notes |
|----------|-----------|--------|-------|
| `contents` | *(inline in node)* | ⬜ Verify | |
| `content` | `content` | ⬜ Verify | |
| `connection` | *(check if needed)* | ⬜ Verify | |
| `associatedReservation` | *(check if needed)* | ⬜ Verify | |
| `contactInfosType` | *(inline)* | ⬜ Verify | |
| `contactInfo` | `contactInfo` | ⬜ Verify | |

#### Time/Date Types
| XSD Type | JSON $def | Status | Notes |
|----------|-----------|--------|-------|
| `timesType` | *(inline in node)* | ⬜ Verify | |
| `time` | `time` | ⬜ Verify | |
| `date` | *(check if needed)* | ⬜ Verify | |

#### Address/Location Types
| XSD Type | JSON $def | Status | Notes |
|----------|-----------|--------|-------|
| `addressType` | `address` | ⬜ Verify | |
| `geographicLocation` | `geographicLocation` | ⬜ Verify | |
| `gpsType` | *(check if needed)* | ⬜ Verify | |
| `manualDescriptionType` | `manualDescription` | ⬜ Verify | |

#### Economy Types
| XSD Type | JSON $def | Status | Notes |
|----------|-----------|--------|-------|
| `economyType` | `economy` | ⬜ Verify | |
| `taxiMeter` | *(check if needed)* | ⬜ Verify | |
| `priceCalculation` | *(check if needed)* | ⬜ Verify | |
| `price` | *(check if needed)* | ⬜ Verify | |
| `formOfPayment` | `payment` | ⬜ Verify | |
| `payment` | `payment` | ⬜ Verify | |
| `exchangeRates` | *(check if needed)* | ⬜ Verify | |
| `exhangeRate` | *(spelling: exchangeRate)* | ⬜ Verify | |
| `amountType` | `amount` | ⬜ Verify | |
| `economyReport` | `economyReport` | ⬜ Verify | |
| `vatAmountSpecificationType` | *(check if needed)* | ⬜ Verify | |

#### Agreement/Product Types
| XSD Type | JSON $def | Status | Notes |
|----------|-----------|--------|-------|
| `agreement` | `agreement` | ⬜ Verify | |
| `product` | `product` | ⬜ Verify | |

#### Process Types
| XSD Type | JSON $def | Status | Notes |
|----------|-----------|--------|-------|
| `process` | `process` | ⬜ Verify | |
| `multiDispatch` | *(inline boolean)* | ⬜ Verify | |

#### Event Types
| XSD Type | JSON $def | Status | Notes |
|----------|-----------|--------|-------|
| `eventType` | `event` | ⬜ Verify | |
| `event` | `event` | ⬜ Verify | |
| `eventReport` | *(inline in orderReport)* | ⬜ Verify | |
| `summaryReport` | `summaryReport` | ⬜ Verify | |
| `pickupConfirmation` | `event` | ⬜ Verify | Semantic rename |

#### Driver Session Types
| XSD Type | JSON $def | Status | Notes |
|----------|-----------|--------|-------|
| `driverSession` | `driverSession` | ⬜ Verify | |
| `orders` | *(inline array)* | ⬜ Verify | |
| `driverSessionReject` | `driverSessionReject` | ⬜ Verify | |

#### Attribute Types
| XSD Type | JSON $def | Status | Notes |
|----------|-----------|--------|-------|
| `attributesType` | *(inline array)* | ⬜ Verify | |
| `attribute` | `id` | ⬜ Verify | Reuses id type |

#### Location/Request Types
| XSD Type | JSON $def | Status | Notes |
|----------|-----------|--------|-------|
| `locationRequest` | `locationRequest` | ⬜ Verify | |
| `authorizationAcceptType` | *(check if needed)* | ⬜ Verify | |

#### Delivery/Reporting Types
| XSD Type | JSON $def | Status | Notes |
|----------|-----------|--------|-------|
| `deliveryNote` | `deliveryNote` | ⬜ Verify | |
| `restrictionsType` | *(check if needed)* | ⬜ Verify | |

#### Calendar Types
| XSD Type | JSON $def | Status | Notes |
|----------|-----------|--------|-------|
| `calendarType` | `calendar` | ⬜ Verify | |
| `weekdaysType` | `weekdays` | ⬜ Verify | |

#### Organization Types
| XSD Type | JSON $def | Status | Notes |
|----------|-----------|--------|-------|
| `organizationType` | `organization` | ⬜ Verify | |
| `orgPaymentType` | `orgPayment` | ⬜ Verify | |

#### Update/Change Types
| XSD Type | JSON $def | Status | Notes |
|----------|-----------|--------|-------|
| `providerorderUpdate` | `providerOrderUpdate` | ⬜ Verify | |
| `changelog` | *(check if needed)* | ⬜ Verify | |
| `log` | *(check if needed)* | ⬜ Verify | |

#### Miscellaneous Types
| XSD Type | JSON $def | Status | Notes |
|----------|-----------|--------|-------|
| `vehicleDistance` | *(check if needed)* | ⬜ Verify | |
| `requestContentType` | *(check if needed)* | ⬜ Verify | |
| `suborderTourType` | *(check if needed)* | ⬜ Verify | |
| `calculationFareType` | *(check if needed)* | ⬜ Verify | |
| `environmentalInformation` | *(check if needed)* | ⬜ Verify | |
| `errorType` | *(check if needed)* | ⬜ Verify | |
| `cancellationConsequence` | `cancellationConsequence` | ⬜ Verify | |

---

## Phase 2: Message Type Coverage

### 2.1 Message Types in JSON Schema

Current JSON Schema supports these msgTypes (from allOf):

| msgType | Name | Body | Has Example | Status |
|---------|------|------|-------------|--------|
| 1000 | resourceRequest | resourceReservation | ⬜ | ⬜ Verify |
| 1061 | ratingResponse | ratingList | ⬜ | ⬜ Verify |
| 1100 | bulkLocationRequest | bulkLocationRequest | ⬜ | ⬜ Verify |
| 1111 | bulkLocationResponse | bulkLocationList | ✅ | ⬜ Verify |
| 1112 | bulkLocationResponse | bulkLocationList | ⬜ | ⬜ Verify |
| 1500 | infoRequest | infoRequest | ⬜ | ⬜ Verify |
| 1600 | infoResponse | infoResponse | ⬜ | ⬜ Verify |
| 1920 | resourceAllocation | resourceAllocation | ⬜ | ⬜ Verify |
| 2000 | order | order | ✅ | ⬜ Verify |
| 2001 | orderConfirmation | *(header only)* | ✅ | ⬜ Verify |
| 2002 | orderReject | orderReject | ✅ | ⬜ Verify |
| 2012 | cancellationConsequence | cancellationConsequence | ⬜ | ⬜ Verify |
| 2020 | nodeCancellation | nodeCancellation | ⬜ | ⬜ Verify |
| 2030 | orderForward | orderForward | ⬜ | ⬜ Verify |
| 2040 | orderLink | order | ⬜ | ⬜ Verify |
| 2060 | providerOrderUpdate | providerOrderUpdate | ⬜ | ⬜ Verify |
| 2100 | driverSession | driverSession | ⬜ | ⬜ Verify |
| 2101 | driverSessionAccept | driverSession | ⬜ | ⬜ Verify |
| 2102 | driverSessionReject | driverSessionReject | ⬜ | ⬜ Verify |
| 2800 | orderTemplate | orderTemplate | ⬜ | ⬜ Verify |
| 2810 | scheduleElementConfirmation | scheduleElementOrderList | ⬜ | ⬜ Verify |
| 2901 | authorizationAccept | resource | ⬜ | ⬜ Verify |
| 3003 | dispatchConfirmation | resource | ✅ | ⬜ Verify |
| 4000 | trafficInfoRequest | resource | ⬜ | ⬜ Verify |
| 4001 | trafficInfoResponse | event | ⬜ | ⬜ Verify |
| 4010 | eventVehicle | event | ✅ | ⬜ Verify |
| 4100 | actionRequest | actionRequest | ⬜ | ⬜ Verify |
| 5000 | messageToVehicle | messageTo | ✅ | ⬜ Verify |
| 5020 | locationRequest | locationRequest | ✅ | ⬜ Verify |
| 5021 | locationResponse | geographicLocation | ✅ | ⬜ Verify |
| 6001 | orderReport | orderReport | ⬜ | ⬜ Verify |
| 6500 | deliveryNote | deliveryNote | ⬜ | ⬜ Verify |
| 7000 | keepAlive | *(header only)* | ✅ | ⬜ Verify |
| 7001 | keepAliveConfirmation | *(header only)* | ✅ | ⬜ Verify |
| 8000 | accounting | accounting | ⬜ | ⬜ Verify |

### 2.2 Message Types in XML Examples vs JSON Schema

**JSON Schema msgTypes (35 total):**
```
1000, 1061, 1100, 1111, 1112, 1500, 1600, 1920,
2000, 2001, 2002, 2012, 2020, 2030, 2040, 2060, 2100, 2101, 2102, 2800, 2810, 2901,
3003, 4000, 4001, 4010, 4100,
5000, 5020, 5021,
6001, 6500,
7000, 7001,
8000
```

**XML Examples msgTypes (18 unique, 37 files):**
```
1020, 1021, 1022, 1023 (Resource login/logout)
2000, 2001, 2010, 2011 (Order, cancellation)
2100 (Driver session)
3003 (Dispatch confirmation)
4010, 4011, 4012, 4020, 4031 (Vehicle events)
5010, 5011, 5020, 5021 (Messages/location)
7000, 7001, 7030, 7031 (KeepAlive, errors)
7100, 7101 (Link mapping)
```

### 2.3 Gap Analysis: Missing msgTypes (16 total)

| msgType | Name | In XML Example | In JSON Schema | Action Required |
|---------|------|----------------|----------------|-----------------|
| **1020** | ResourceLogin | ✅ 1020.xml | ❌ Missing | Add to schema |
| **1021** | ResourceLogout | ✅ 1021.xml | ❌ Missing | Add to schema |
| **1022** | ResourceLoginConfirm | ✅ 1022.xml | ❌ Missing | Add to schema |
| **1023** | ResourceLoginReject | ✅ 1023.xml | ❌ Missing | Add to schema |
| **2010** | OrderCancellation | ✅ 2010.xml | ❌ Missing | Add to schema |
| **2011** | OrderCancellationConfirm | ✅ 2011.xml | ❌ Missing | Add to schema |
| **4011** | VehicleEventAccepted | ✅ 4011_*.xml (6 files) | ❌ Missing | Add to schema |
| **4012** | VehicleEventRejected | ✅ 4012_*.xml (3 files) | ❌ Missing | Add to schema |
| **4020** | EndOfOrder | ✅ 4020.xml | ❌ Missing | Add to schema |
| **4031** | VehicleEventReject | ✅ 4031.xml | ❌ Missing | Add to schema |
| **5010** | MessageFromVehicle | ✅ 5010.xml | ❌ Missing | Add to schema |
| **5011** | MessageFromVehicleConfirm | ✅ 5011.xml | ❌ Missing | Add to schema |
| **7030** | SyntaxError | ✅ 7030.xml | ❌ Missing | Add to schema |
| **7031** | NotOperational | ✅ 7031.xml | ❌ Missing | Add to schema |
| **7100** | LinkMappingRequest | ✅ 7100.xml | ❌ Missing | Add to schema |
| **7101** | LinkMappingResponse | ✅ 7101.xml | ❌ Missing | Add to schema |

### 2.4 XML Example to JSON Example Matrix

| XML Example | msgType | In Schema | JSON Example | Status |
|-------------|---------|-----------|--------------|--------|
| 1020.xml | 1020 | ❌ | ⬜ Blocked | Need schema first |
| 1021.xml | 1021 | ❌ | ⬜ Blocked | Need schema first |
| 1022.xml | 1022 | ❌ | ⬜ Blocked | Need schema first |
| 1023.xml | 1023 | ❌ | ⬜ Blocked | Need schema first |
| 2000.xml | 2000 | ✅ | ✅ Exists | Done |
| 2000_OrderAlter.xml | 2000 | ✅ | ⬜ Create | Variant example |
| 2000_Trip.xml | 2000 | ✅ | ⬜ Create | Variant example |
| 2000_MultiOrder.xml | 2000 | ✅ | ⬜ Create | Variant example |
| 2001.xml | 2001 | ✅ | ✅ Exists | Done |
| 2010.xml | 2010 | ❌ | ⬜ Blocked | Need schema first |
| 2011.xml | 2011 | ❌ | ⬜ Blocked | Need schema first |
| 2100_DriverSession.xml | 2100 | ✅ | ⬜ Create | High priority |
| 3003.xml | 3003 | ✅ | ✅ Exists | Done |
| 4010_Bom.xml | 4010 | ✅ | ⬜ Create | Variant example |
| 4010_Drop.xml | 4010 | ✅ | ⬜ Create | Variant example |
| 4010_Pickup.xml | 4010 | ✅ | ✅ Exists | Done |
| 4011_Pickup.xml | 4011 | ❌ | ⬜ Blocked | Need schema first |
| 4011_Drop.xml | 4011 | ❌ | ⬜ Blocked | Need schema first |
| 4011_NoShow.xml | 4011 | ❌ | ⬜ Blocked | Need schema first |
| 4011_Pickup with infomessage.xml | 4011 | ❌ | ⬜ Blocked | Need schema first |
| 4011_Drop with infomessage.xml | 4011 | ❌ | ⬜ Blocked | Need schema first |
| 4011_NoShow with infomessage.xml | 4011 | ❌ | ⬜ Blocked | Need schema first |
| 4012_PickUp.xml | 4012 | ❌ | ⬜ Blocked | Need schema first |
| 4012_Drop.xml | 4012 | ❌ | ⬜ Blocked | Need schema first |
| 4012_BomRejected.xml | 4012 | ❌ | ⬜ Blocked | Need schema first |
| 4020.xml | 4020 | ❌ | ⬜ Blocked | Need schema first |
| 4031.xml | 4031 | ❌ | ⬜ Blocked | Need schema first |
| 5010.xml | 5010 | ❌ | ⬜ Blocked | Need schema first |
| 5011.xml | 5011 | ❌ | ⬜ Blocked | Need schema first |
| 5020.xml | 5020 | ✅ | ✅ Exists | Done |
| 5021.xml | 5021 | ✅ | ✅ Exists | Done |
| 7000.xml | 7000 | ✅ | ✅ Exists | Done |
| 7001.xml | 7001 | ✅ | ✅ Exists | Done |
| 7030.xml | 7030 | ❌ | ⬜ Blocked | Need schema first |
| 7031.xml | 7031 | ❌ | ⬜ Blocked | Need schema first |
| 7100.xml | 7100 | ❌ | ⬜ Blocked | Need schema first |
| 7101.xml | 7101 | ❌ | ⬜ Blocked | Need schema first |

### 2.5 Summary Statistics

| Category | Count |
|----------|-------|
| XML example files | 37 |
| Unique msgTypes in XML | 18 |
| msgTypes in JSON schema | 35 |
| **Missing msgTypes (to add)** | **16** |
| JSON examples existing | 12 |
| JSON examples needed (schema ready) | 5 |
| JSON examples blocked (need schema) | 20 |

---

## Phase 3: JSON Example Creation

### 3.1 Examples Ready to Create (Schema Ready - 5 examples)

These can be created immediately as their msgTypes are in the schema:

| Priority | Example File | Source XML | msgType |
|----------|-------------|------------|---------|
| High | `2100_driverSession.json` | 2100_DriverSession.xml | 2100 |
| Medium | `2000_orderAlter.json` | 2000_OrderAlter.xml | 2000 |
| Medium | `2000_trip.json` | 2000_Trip.xml | 2000 |
| Medium | `2000_multiOrder.json` | 2000_MultiOrder.xml | 2000 |
| Medium | `4010_bom.json` | 4010_Bom.xml | 4010 |
| Medium | `4010_drop.json` | 4010_Drop.xml | 4010 |

### 3.2 Examples Blocked (Need Schema Updates First - 20 examples)

These require adding msgTypes to JSON schema first:

| msgType | Example Files | Body Type | $def Status |
|---------|---------------|-----------|-------------|
| 1020 | 1020.xml | resourceDispatch | ❌ CREATE |
| 1021 | 1021.xml | *(header only)* | ✅ N/A |
| 1022 | 1022.xml | *(header only)* | ✅ N/A |
| 1023 | 1023.xml | resourceDispatch | ❌ CREATE |
| 2010 | 2010.xml | *(header only)* | ✅ N/A |
| 2011 | 2011.xml | *(header only)* | ✅ N/A |
| 4011 | 4011_*.xml (6 files) | event (pickupConfirmation) | ✅ EXISTS |
| 4012 | 4012_*.xml (3 files) | event (pickupConfirmation) | ✅ EXISTS |
| 4020 | 4020.xml | order | ✅ EXISTS |
| 4031 | 4031.xml | *(header only)* | ✅ N/A |
| 5010 | 5010.xml | manualDescription | ✅ EXISTS |
| 5011 | 5011.xml | *(header only)* | ✅ N/A |
| 7030 | 7030.xml | manualDescription | ✅ EXISTS |
| 7031 | 7031.xml | manualDescription | ✅ EXISTS |
| 7100 | 7100.xml | order | ✅ EXISTS |
| 7101 | 7101.xml | order | ✅ EXISTS |

**Note:** Only `resourceDispatch` needs to be created. All other body types exist.

### 3.3 Additional Coverage Examples (No XML source, but schema ready)

| Priority | Example File | msgType | Notes |
|----------|-------------|---------|-------|
| Low | `1000_resourceRequest.json` | 1000 | No XML example |
| Low | `1061_ratingResponse.json` | 1061 | No XML example |
| Low | `1100_bulkLocationRequest.json` | 1100 | No XML example |
| Low | `2012_cancellationConsequence.json` | 2012 | No XML example |
| Low | `2020_nodeCancellation.json` | 2020 | No XML example |
| Low | `2030_orderForward.json` | 2030 | No XML example |
| Low | `2060_providerOrderUpdate.json` | 2060 | No XML example |
| Low | `2800_orderTemplate.json` | 2800 | No XML example |
| Low | `4100_actionRequest.json` | 4100 | No XML example |
| Low | `6001_orderReport.json` | 6001 | No XML example |
| Low | `6500_deliveryNote.json` | 6500 | No XML example |
| Low | `8000_accounting.json` | 8000 | No XML example |

### 3.4 Example Transformation Guide (per Bengt review)

**Step-by-step Process:**

1. **Read XML example** and identify:
   - msgType and msgName
   - Body element (if any)
   - All nested structures

2. **Create JSON structure:**
   ```json
   {
     "msg": {
       "msgType": "XXXX",
       "msgName": "...",
       "id": { "src": "...", "id": "..." },
       "sender": { ... },
       "receiver": { ... },
       "referencesTo": { ... }
     },
     "bodyElement": { ... }
   }
   ```

3. **Apply transformations:**
   - Remove `<SUTI>` root wrapper
   - Move `orgSender`/`orgReceiver` into msg as `sender`/`receiver`
   - Apply property name simplifications per xsd-json-mapping.yaml
   - Transform enums to camelCase text
   - Convert `<element>...</element>` arrays to JSON arrays `[...]`
   - Remove `unique="true"` attributes (not in JSON schema)

4. **Property name mappings:**
   | XSD | JSON |
   |-----|------|
   | `idOrg` | `id` |
   | `idMsg` | `id` |
   | `contactInfoDriver` | `contactInfo` |
   | `manualDescriptionMsg` | `manualDescription` |
   | `pickupConfirmation` | `event` |
   | `nodeConfirmed` | `node` (inside event) |

5. **Validate against schema:**
   ```bash
   python3 -c "import json, jsonschema; \
     schema = json.load(open('schemas/SUTI_Message.schema.json')); \
     instance = json.load(open('examples/JSON/draft_2026/XXXX.json')); \
     jsonschema.validate(instance, schema)"
   ```

6. **Document unmappable features:**
   - XSD `xs:choice` - document which option chosen
   - XSD `xs:any` - not representable, omit or document
   - Complex inheritance - flatten into single object

---

## Phase 4: XSD-JSON Mapping Verification

### 4.1 Current Mapping Coverage

The `xsd-json-mapping.yaml` currently documents:
- ✅ Array property mappings (17 items)
- ✅ Property simplifications (21 items)
- ✅ Enumeration mappings (6 enums)
- ✅ Anomaly corrections (8 items)
- ✅ Type mappings (12 items)
- ⬜ Message type mappings (incomplete - only 18 of 35+)

### 4.2 Mapping Gaps to Fill

| Category | Current | Needed | Action |
|----------|---------|--------|--------|
| Message Types | 18 | 35+ | Add missing msgType → body mappings |
| Complex Types | ~30 | 86 | Document all XSD→JSON type mappings |
| Simple Types | 12 | ~20+ | Verify all XSD simple types documented |
| Enumerations | 6 | ~15+ | Add all enum value mappings |

### 4.3 Required Additions to Mapping File

```yaml
# ADD: Missing message types (16 total) - CORRECTED per XML analysis
message_types:
  "1020": { name: "ResourceLogin", body: "resourceDispatch" }  # CREATE $def
  "1021": { name: "ResourceLoginConfirmation", body: null }  # header only
  "1022": { name: "ResourceLoginReject", body: null }  # header only
  "1023": { name: "ResourceLogoff", body: "resourceDispatch" }  # CREATE $def
  "2010": { name: "OrderCancellation", body: null }  # header only
  "2011": { name: "OrderCancellationAccepted", body: null }  # header only
  "4011": { name: "VehicleEventAccepted", body: "event" }  # uses event $def
  "4012": { name: "VehicleEventRejected", body: "event" }  # uses event $def
  "4020": { name: "EndOfOrder", body: "order" }  # uses order $def
  "4031": { name: "NoContactWithVehicle", body: null }  # header only
  "5010": { name: "MessageFromVehicle", body: "messageTo" }  # Fixed: uses messageTo, not manualDescription
  "5011": { name: "MessageFromVehicleConfirm", body: null }  # header only
  "7030": { name: "SyntaxError", body: "manualDescription" }
  "7031": { name: "NotOperational", body: "manualDescription" }
  "7100": { name: "LinkMappingRequest", body: "order" }
  "7101": { name: "LinkMappingResponse", body: "order" }

# ADD: All complex type mappings
complex_types:
  - xsd: "idEkInfo"
    json: "???"
    notes: "..."
  # ... etc for all 86 types

# ADD: All enumeration mappings
enumerations:
  contentType:
    strategy: "text-only"
    values: [...]
  # ... etc for all enums
```

---

## Phase 5: Validation & Testing

### 5.1 Schema Validation Tests

| Test | Description | Status |
|------|-------------|--------|
| All examples validate | Run all JSON examples against schema | ⬜ |
| Unknown msgType rejected | Test invalid msgType is rejected | ⬜ |
| Required fields enforced | Test missing required fields fail | ⬜ |
| additionalProperties enforced | Test extra fields are rejected | ⬜ |
| Enum values validated | Test invalid enum values fail | ⬜ |

### 5.2 Completeness Tests

| Test | Description | Status |
|------|-------------|--------|
| All XSD types mapped | Every complexType has JSON equivalent | ⬜ |
| All msgTypes supported | Every msgType in XSD works in JSON | ⬜ |
| All XML examples converted | JSON example for each XML example | ⬜ |
| All enums documented | Every XSD enum in mapping file | ⬜ |

### 5.3 Automated Validation Script

Create `tools/validate_completeness.py`:
```python
# Validates:
# 1. All JSON examples against schema
# 2. All XSD types have JSON equivalents
# 3. All msgTypes are handled
# 4. All enums are mapped
```

---

## Phase 6: Implementation Order

### Step 0: Discovery & Verification (BLOCKER - per Bengt review)
1. ⬜ **Create `resourceDispatch` $def** (required for 1020, 1023)
2. ⬜ Verify `event` $def supports pickupConfirmation structure
3. ⬜ Verify `manualDescription` $def has all required properties
4. ⬜ **Regression test**: Run all 12 existing JSON examples
5. ⬜ Create backup of schema before modifications

### Step 1: Schema Completeness (CRITICAL PATH)
6. ⬜ Add 16 missing msgTypes to JSON schema:
   - 1020, 1023 (with resourceDispatch body)
   - 1021, 1022 (header only)
   - 2010, 2011 (header only)
   - 4011, 4012 (with event body)
   - 4020 (with order body)
   - 4031 (header only)
   - 5010 (with manualDescription body)
   - 5011 (header only)
   - 7030, 7031 (with manualDescription body)
   - 7100, 7101 (with order body)
7. ⬜ **Regression test**: All 12 existing examples still validate
8. ⬜ Update msgType rejection list with all 51 types

### Step 2: XSD Type Verification
9. ⬜ Read entire XSD systematically (line by line)
10. ⬜ Create XSD type → JSON $def mapping spreadsheet
11. ⬜ Identify any remaining missing JSON definitions
12. ⬜ Document type differences per verification criteria

### Step 3: Example Creation (25 new examples)
13. ⬜ Create 5 ready examples (schema already supports):
   - 2100_driverSession.json
   - 2000_orderAlter.json, 2000_trip.json, 2000_multiOrder.json
   - 4010_bom.json, 4010_drop.json
14. ⬜ Create 20 blocked examples (after Step 1 completes):
   - 1020-1023 examples
   - 2010-2011 examples
   - 4011 examples (6 variants)
   - 4012 examples (3 variants)
   - 4020, 4031, 5010, 5011, 7030, 7031, 7100, 7101 examples
15. ⬜ Validate all 37 examples against schema

### Step 4: Documentation & Tooling
16. ⬜ Complete xsd-json-mapping.yaml with all 16 new msgTypes
17. ⬜ Create automated validation script (`tools/validate_completeness.py`)
18. ⬜ Final verification pass
19. ⬜ Mark ready for deployment

### Rollback Procedure (per Bengt review)

If breaking changes discovered:
1. Restore schema from backup in `.claude/backups/`
2. Document breaking change in issue tracker
3. Consider versioned schema approach (v2026.1 → v2026.2)
4. Get TK decision on migration path

---

## Success Criteria

Before deployment, ALL must be true:

### Phase 0 Prerequisites
- [ ] `resourceDispatch` $def created and tested
- [ ] All 12 existing examples still validate (regression)
- [ ] Schema backup created in `.claude/backups/`

### Phase 1-4 Deliverables
- [ ] Every XSD complexType has corresponding JSON $def or documented exclusion reason
- [ ] All 16 missing msgTypes added to JSON schema (1020-1023, 2010-2011, 4011-4012, 4020, 4031, 5010-5011, 7030-7031, 7100-7101)
- [ ] Every XML example (37 files) has corresponding JSON example
- [ ] xsd-json-mapping.yaml includes all 51 msgTypes (35 existing + 16 new)
- [ ] All JSON examples (37 files) validate against schema
- [ ] Automated validation script passes (`tools/validate_completeness.py`)
- [ ] No unknown msgTypes accepted by schema (strict rejection)
- [ ] All enumerations use text-only values (camelCase)

---

## Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| XSD types without clear JSON mapping | Medium | Document and get TK decision |
| Legacy msgTypes not in current schema | Low | Add to rejection list or support |
| XML features without JSON equivalent | Medium | Document limitations |
| Breaking changes for existing implementations | High | Legacy schema for backward compat |
| **NEW:** Missing $defs block msgType additions | High | Complete Phase 0 before Phase 1 |
| **NEW:** Regression failures after schema changes | High | Run all 12 examples after each change |
| **NEW:** Inconsistent example transformations | Medium | Follow transformation guide strictly |
| **NEW:** Round-trip data loss (XML→JSON→XML) | Medium | Document known limitations |

---

## Appendix A: File Locations

| File | Purpose |
|------|---------|
| `schemas/SUTI_Message.xsd` | Source XSD (3131 lines) |
| `schemas/SUTI_Message.schema.json` | Target JSON Schema (1408 lines) |
| `schemas/SUTI_BulkLocation_legacy.schema.json` | Legacy schema |
| `examples/XML/*.xml` | 37 XML example files |
| `examples/JSON/draft_2026/*.json` | 12 JSON example files |
| `plans/xsd-json-mapping.yaml` | XSD→JSON mapping reference |
| `tools/validate_completeness.py` | Validation script (to create) |

---

## Appendix B: Execution Commands

```bash
# Count XSD types
grep -E "complexType name=" schemas/SUTI_Message.xsd | wc -l

# List JSON definitions
python3 -c "import json; f=open('schemas/SUTI_Message.schema.json'); d=json.load(f); print('\n'.join(sorted(d['$defs'].keys())))"

# Validate all examples
python3 tools/validate_completeness.py

# Find XML examples without JSON
for f in examples/XML/*.xml; do
  base=$(basename "$f" .xml)
  if ! ls examples/JSON/draft_2026/${base}*.json 2>/dev/null; then
    echo "Missing: $base"
  fi
done
```

---

**Owner:** SUTI Development Team
**Created:** 2026-02-10
**Target Completion:** 2026-02-24 (2 weeks)
