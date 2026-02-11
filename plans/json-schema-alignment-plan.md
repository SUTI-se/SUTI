# JSON Schema Alignment Plan

**Date:** 2026-02-10
**Version:** 1.2
**Status:** ✅ Implemented (2026-02-10)
**Changes v1.2:** `contacts` → `contactInfo` (keep compound noun item type name)
**Goal:** Align JSON Schema with XSD structure for easy XML→JSON migration
**Related:** [json-property-simplification-proposal.md](json-property-simplification-proposal.md) - Property name simplifications

---

## 1. Guiding Principles

| Principle | Decision |
|-----------|----------|
| **Structure** | Mirror XSD nesting (vehicle/driver objects, economyContent, etc.) |
| **Field names** | JSON-idiomatic camelCase with documented mapping |
| **Validation** | Strict (`additionalProperties: false` everywhere) |
| **Completeness** | All XSD fields present in schema (optional where XSD allows) |
| **Enumerations** | Text-only, camelCase |

---

## 2. Issues from JSON_REVIEW.md

### 2.1 High Priority - Schema Gaps

| # | Issue | Current State | Required Change |
|---|-------|---------------|-----------------|
| 1 | **Resource modeling** | Flat: `idVehicle`, `idDriver` | Nested: `vehicle: {}`, `driver: {}` |
| 2 | **Content structure** | Missing fields | Add: `economyContent`, `resourceContent`, `attributeListContent`, `subOrderContent` |
| 3 | **time.dwellTime** | Missing | Add: `dwellTime: integer` |
| 4 | **capacity.seats** | `integer` | Change to: `{ noOfSeats, noOfItems }` |
| 5 | **No additionalProperties** | Allows any extra fields | Add `additionalProperties: false` to all $defs |

### 2.2 Medium Priority - Enumeration & Example Fixes

| # | Issue | File(s) | Fix |
|---|-------|---------|-----|
| 6 | `OrderCancelled` | SUTI_Enumerations.yaml | → `orderCancelled` |
| 7 | `OrderNoShow` | SUTI_Enumerations.yaml | → `orderNoShow` |
| 8 | `OrderCompleted` | SUTI_Enumerations.yaml | → `orderCompleted` |
| 9 | `NoShow` | SUTI_Enumerations.yaml | → `noShow` |
| 10 | `prepaidSocialfee` | SUTI_Enumerations.yaml | → `prepaidSocialFee` |
| 11 | `socialservicefee` | SUTI_Enumerations.yaml | → `socialServiceFee` |
| 12 | `estimatedStarttime` | SUTI_Enumerations.yaml | → `estimatedStartTime` |
| 13 | `estimatedEndtime` | SUTI_Enumerations.yaml | → `estimatedEndTime` |
| 14 | `prepaidsocialfee` | 2000_order.json | → `prepaidSocialFee` |
| 15 | `sendtoVehicle` etc. | 5000_messageToVehicle.json | → `sendToVehicle` |
| 16 | Legacy attribute naming | Multiple | Normalize to camelCase |

### 2.3 Low Priority - Validation Strictness

| # | Issue | Required Change |
|---|-------|-----------------|
| 9 | Unknown msgType passes | Add `else: false` to reject unknown types |
| 10 | Empty locationRequest valid | Add minimum required fields or document intent |

---

## 3. Schema Changes

### 3.1 Add `additionalProperties: false` to All $defs

Apply to every type definition:

```json
"id": {
  "type": "object",
  "properties": { ... },
  "required": ["src", "id"],
  "additionalProperties": false  // ADD THIS
}
```

**Affected definitions:** All ~50 $defs in schema.

### 3.2 Expand `time` Definition

```json
"time": {
  "type": "object",
  "properties": {
    "timeType": {
      "type": "string",
      "enum": ["scheduled", "calculated", "estimated", "actual", "earliest", "latest", "promised"]
    },
    "time": { "type": "string", "format": "date-time" },
    "dwellTime": { "type": "integer", "minimum": 0, "description": "Dwell time in seconds" }
  },
  "required": ["timeType", "time"],
  "additionalProperties": false
}
```

### 3.3 Expand `content` Definition

```json
"content": {
  "type": "object",
  "properties": {
    "contentType": { "type": "string", "enum": ["traveller", "parcel", "goods"] },
    "contentSeqNo": { "type": "integer", "minimum": 1 },
    "id": { "$ref": "#/$defs/id" },
    "name": { "type": "string" },
    "contactInfo": { "type": "array", "items": { "$ref": "#/$defs/contactInfo" } },
    "mobilityAids": { "type": "array", "items": { "$ref": "#/$defs/mobilityAid" } },
    "attributes": { "type": "array", "items": { "$ref": "#/$defs/id" } },
    "economy": { "$ref": "#/$defs/economy" },
    "resource": { "$ref": "#/$defs/resourceSpec" },
    "subOrder": { "$ref": "#/$defs/subOrder" }
  },
  "additionalProperties": false
}
```

> **Note:** Simplified property names per [json-property-simplification-proposal.md](json-property-simplification-proposal.md):
> - `idContent` → `id` (context provides meaning)
> - `nameContent` → `name` (context provides meaning)
> - `economyContent` → `economy` (dropped redundant "Content")
> - `resourceContent` → `resource` (dropped redundant "Content")
> - `subOrderContent` → `subOrder` (dropped redundant "Content")

### 3.4 Add `economy` Definition (for content)

```json
"economy": {
  "type": "object",
  "properties": {
    "payments": {
      "type": "array",
      "items": { "$ref": "#/$defs/payment" }
    }
  },
  "additionalProperties": false
}
```

### 3.5 Add `resourceSpec` Definition (for content)

```json
"resourceSpec": {
  "type": "object",
  "properties": {
    "vehicle": { "$ref": "#/$defs/vehicleSpec" },
    "driver": { "$ref": "#/$defs/driverSpec" }
  },
  "additionalProperties": false
}
```

### 3.6 Add `subOrder` Definition

```json
"subOrder": {
  "type": "object",
  "properties": {
    "orderIds": {
      "type": "array",
      "items": { "$ref": "#/$defs/id" }
    }
  },
  "additionalProperties": false
}
```

> **Note:** `idOrderList` → `orderIds` per simplification proposal (need prefix to distinguish from other IDs)

### 3.7 Restructure `resource` to Match XSD

```json
"resource": {
  "type": "object",
  "description": "Dispatched vehicle/driver resource",
  "properties": {
    "vehicle": { "$ref": "#/$defs/vehicleResource" },
    "driver": { "$ref": "#/$defs/driverResource" },
    "startLocation": { "$ref": "#/$defs/geographicLocation" }
  },
  "additionalProperties": false
}
```

> **Note:** `vehicleStartLocation` → `startLocation` (context is resource)

### 3.8 Add `vehicleResource` Definition

```json
"vehicleResource": {
  "type": "object",
  "properties": {
    "id": { "$ref": "#/$defs/id" },
    "ids": { "type": "array", "items": { "$ref": "#/$defs/id" } },
    "description": { "type": "string" },
    "capacity": { "$ref": "#/$defs/capacity" },
    "attributes": { "type": "array", "items": { "$ref": "#/$defs/id" } },
    "location": { "$ref": "#/$defs/geographicLocation" }
  },
  "additionalProperties": false
}
```

> **Note:** Simplified property names:
> - `idVehicle` → `id` (context is vehicle)
> - `idVehicleList` → `ids` (context is vehicle)
> - `vehicleDescription` → `description` (context is vehicle)
> - `geographicLocation` → `location` (simplified)

### 3.9 Add `driverResource` Definition

```json
"driverResource": {
  "type": "object",
  "properties": {
    "id": { "$ref": "#/$defs/id" },
    "name": { "type": "string" },
    "attributes": { "type": "array", "items": { "$ref": "#/$defs/id" } },
    "contactInfo": { "type": "array", "items": { "$ref": "#/$defs/contactInfo" } }
  },
  "additionalProperties": false
}
```

> **Note:** Simplified property names:
> - `idDriver` → `id` (context is driver)
> - `driverName` → `name` (context is driver)
> - `contactInfoDriver` → `contactInfo` (keep compound noun item type name)

### 3.10 Fix `capacity` Definition

```json
"capacity": {
  "type": "object",
  "properties": {
    "seats": { "$ref": "#/$defs/capacityItem" },
    "wheelchairs": { "$ref": "#/$defs/capacityItem" },
    "stretchers": { "$ref": "#/$defs/capacityItem" },
    "animals": { "$ref": "#/$defs/capacityItem" }
  },
  "additionalProperties": false
},

"capacityItem": {
  "type": "object",
  "properties": {
    "noOfSeats": { "type": "integer", "minimum": 0 },
    "noOfItems": { "type": "integer", "minimum": 0 }
  },
  "additionalProperties": false
}
```

### 3.11 Add Unknown msgType Rejection

```json
{
  "allOf": [
    { "$ref": "#/$defs/baseMessage" },
    { "if": { "properties": { "msg": { "properties": { "msgType": { "const": "2000" } } } } },
      "then": { "properties": { "order": { "$ref": "#/$defs/order" } }, "required": ["order"] }
    },
    // ... other message types ...
    {
      "if": {
        "properties": {
          "msg": {
            "properties": {
              "msgType": {
                "not": { "enum": ["1100", "1111", "2000", "2001", ...] }
              }
            }
          }
        }
      },
      "then": false
    }
  ]
}
```

---

## 4. Example Updates

### 4.1 Fix Casing in 2000_order.json

| Field | Current | Fixed |
|-------|---------|-------|
| `paymentType` | `prepaidsocialfee` | `prepaidSocialFee` |

### 4.2 Fix Casing in 5000_messageToVehicle.json

| Field | Current | Fixed |
|-------|---------|-------|
| `sendtoInvoice` | `sendtoInvoice` | `sendToInvoice` |
| `sendtoOperator` | `sendtoOperator` | `sendToOperator` |
| `sendtoVehicle` | `sendtoVehicle` | `sendToVehicle` |

### 4.3 Validate All Examples After Schema Update

Re-validate all 11 examples after schema changes. Expect some to fail initially due to `additionalProperties: false`.

---

## 5. XSD-JSON Field Mapping (Simplified Names)

| XSD Element | JSON Property | Context | Simplification |
|-------------|---------------|---------|----------------|
| `idContent` | `id` | content | Context provides meaning |
| `nameContent` | `name` | content | Context provides meaning |
| `attributeListContent` | `attributes` | content | Drop redundant suffix |
| `contactInfoListContent` | `contactInfo` | content | Keep item type name |
| `economyContent` | `economy` | content | Drop "Content" |
| `resourceContent` | `resource` | content | Drop "Content" |
| `subOrderContent` | `subOrder` | content | Drop "Content" |
| `idOrderList` | `orderIds` | subOrder | Plural + need prefix |
| `idVehicle` | `id` | vehicle | Context is vehicle |
| `idVehicleList` | `ids` | vehicle | Context is vehicle |
| `vehicleDescription` | `description` | vehicle | Context is vehicle |
| `attributeListVehicle` | `attributes` | vehicle | Drop redundant suffix |
| `idDriver` | `id` | driver | Context is driver |
| `driverName` | `name` | driver | Context is driver |
| `attributeListDriver` | `attributes` | driver | Drop redundant suffix |
| `contactInfoDriver` | `contactInfo` | driver | Keep item type name |
| `vehicleStartLocation` | `startLocation` | resource | Drop "vehicle" |
| `formOfPayment` | `payments` | economy | Plural form |

---

## 6. Implementation Order

### Phase 1: Schema Updates (Priority) ✅
1. [x] Add `dwellTime` to `time`
2. [x] Add `economy`, `resourceSpec`, `subOrder` definitions (simplified names)
3. [x] Add `vehicleResource`, `driverResource`, `capacityItem` definitions
4. [x] Restructure `resource` to use nested vehicle/driver + startLocation
5. [x] Restructure `capacity` to use `capacityItem`
6. [x] Expand `content` with missing fields (using simplified names)
7. [x] Apply property name simplifications per proposal:
    - `idContent` → `id`, `nameContent` → `name` (in content)
    - `economyContent` → `economy`, `resourceContent` → `resource` (in content)
    - `idVehicle` → `id`, `idVehicleList` → `ids` (in vehicle)
    - `idDriver` → `id`, `driverName` → `name` (in driver)
    - `idOrderList` → `orderIds` (in subOrder)
8. [x] Add `additionalProperties: false` to ALL $defs
9. [x] Add unknown msgType rejection

### Phase 2: Enumeration & Example Fixes ✅
10. [x] Fix SUTI_Enumerations.yaml casing (8 keys):
    - `OrderCancelled` → `orderCancelled`
    - `OrderNoShow` → `orderNoShow`
    - `OrderCompleted` → `orderCompleted`
    - `NoShow` → `noShow`
    - `prepaidSocialfee` → `prepaidSocialFee`
    - `socialservicefee` → `socialServiceFee`
    - `estimatedStarttime` → `estimatedStartTime`
    - `estimatedEndtime` → `estimatedEndTime`
11. [x] Fix `paymentType` casing in 2000_order.json
12. [x] Fix `sendTo*` casing in 5000_messageToVehicle.json
13. [x] Update all examples with simplified property names
14. [x] Validate all examples against updated schema
15. [x] Fix any validation failures

### Phase 3: Documentation
16. [ ] Update xsd-json-mapping.yaml with simplified field mappings
17. [x] Update json-schema-2026-changelog.md
18. [ ] Update json-2021-refactoring-plan.md

---

## 7. Migration Guide for Implementers

### 7.1 XML→JSON Transformation Rules

```
XML Element                    JSON Property              Context
-----------                    -------------              -------
<idContent>               →    "id": {...}                content
<nameContent>             →    "name": "..."              content
<attributeListContent>    →    "attributes": [...]        content
<contactInfoListContent>  →    "contactInfo": [...]       content
<economyContent>          →    "economy": {...}           content
<resourceContent>         →    "resource": {...}          content
<subOrderContent>         →    "subOrder": {...}          content
<idOrderList>             →    "orderIds": [...]          subOrder

<idVehicle>               →    "id": {...}                vehicle
<idVehicleList>           →    "ids": [...]               vehicle
<vehicleDescription>      →    "description": "..."       vehicle
<attributeListVehicle>    →    "attributes": [...]        vehicle

<idDriver>                →    "id": {...}                driver
<driverName>              →    "name": "..."              driver
<attributeListDriver>     →    "attributes": [...]        driver
<contactInfoDriver>       →    "contactInfo": [...]       driver

<vehicleStartLocation>    →    "startLocation": {...}     resource
<formOfPayment>           →    "payments": [...]          economy
<capacity><seats>         →    "capacity": { "seats": { "noOfSeats": N } }
```

### 7.2 Casing Transformations

```
XML Value                      JSON Value
---------                      ----------
prepaidsocialfee          →    prepaidSocialFee
sendtoVehicle             →    sendToVehicle
sendtoInvoice             →    sendToInvoice
sendtoOperator            →    sendToOperator
```

### 7.3 Simplification Principle

**When nested inside a typed parent, drop the type from the property name:**

| Instead of | Use | Why |
|------------|-----|-----|
| `vehicle.idVehicle` | `vehicle.id` | Context is vehicle |
| `vehicle.idVehicleList` | `vehicle.ids` | Context is vehicle |
| `driver.driverName` | `driver.name` | Context is driver |
| `content.economyContent` | `content.economy` | Drop redundant "Content" |

---

## 8. Validation Strategy

After implementing all changes:

1. **Strict validation** - All examples must pass with `additionalProperties: false`
2. **No silent failures** - Any unknown field must cause validation error
3. **Unknown msgType rejection** - Messages with unrecognized msgType must fail
4. **Complete coverage** - All XSD fields representable in JSON

---

## 9. Risk Assessment

| Risk | Mitigation |
|------|------------|
| Breaking existing implementations | Legacy schema remains for bulkLocation; document migration path |
| Validation too strict | Review with TK before finalizing |
| Missing XSD fields | Cross-check with complete XSD before release |

---

## 10. Success Criteria

- [x] All 12 draft_2026 examples validate against strict schema (11 + 1 legacy)
- [x] No `additionalProperties` allowed anywhere (all ~50 $defs have `additionalProperties: false`)
- [x] All XSD content/resource/economy fields mapped
- [x] Unknown msgType rejected (via `not` + `then: false` pattern)
- [x] Casing normalized to camelCase throughout
- [x] Property names simplified per proposal (no redundant context)
- [x] Bulk location legacy schema unchanged
- [x] Migration guide complete for XML implementers

---

**Implementation Complete:** 2026-02-10

---

## Appendix: Related Documents

- [json-property-simplification-proposal.md](json-property-simplification-proposal.md) - Detailed property name simplifications
- [xsd-json-mapping.yaml](xsd-json-mapping.yaml) - Complete XSD to JSON mapping
- [JSON_REVIEW.md](../JSON_REVIEW.md) - Original review findings
