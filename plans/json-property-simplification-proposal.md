# JSON 2026 Property Name Simplification Proposal

**Date:** 2026-02-10
**Version:** 1.2
**Status:** ✅ Implemented (2026-02-10)
**Changes in 1.2:** `contacts` → `contactInfo` (keep compound noun item type name)
**Goal:** Maximize clarity and simplicity in JSON property names by removing redundant context

---

## 1. Guiding Principles

| Principle | Description |
|-----------|-------------|
| **No Redundant Context** | If a property is nested within `vehicle`, don't repeat "vehicle" in the name |
| **Plurals for Arrays** | Use plural forms: `ids`, `attributes`, `payments`. Exception: compound nouns like `contactInfo` keep singular form |
| **Consistent Naming** | Same concept = same name across all contexts |
| **camelCase Only** | All property names in camelCase |
| **Preserve Legacy** | Bulk location legacy schema remains unchanged |

---

## 2. Current State Analysis

### 2.1 Identified Redundancy Patterns

| Pattern | Example | Problem |
|---------|---------|---------|
| **List suffix** | `idVehicleList`, `idOrderList` | "List" is redundant with array type |
| **Type-in-name when nested** | `vehicle.attributeListVehicle` | "Vehicle" is already the parent |
| **Context repetition** | `content.contactInfoListContent` | "Content" is already the parent |
| **Verbose compound names** | `economyContent`, `resourceContent` | "Content" suffix unnecessary in nested context |

### 2.2 Examples from Current Draft 2026 Files

**3003_dispatchConfirmation.json** (current):
```json
{
  "resource": {
    "vehicle": {
      "idVehicleList": [...],           // Redundant: "List" + "Vehicle" in vehicle context
      "attributeListVehicle": [...]      // Redundant: "Vehicle" suffix
    },
    "driver": {
      "attributeListDriver": [...],      // Redundant: "Driver" suffix
      "contactInfoListDriver": [...]     // Redundant: "Driver" suffix + verbose
    }
  }
}
```

**2000_order.json** (current):
```json
{
  "contents": [{
    "attributeListContent": [...],       // Redundant: "Content" suffix
    "contactInfoListContent": [...],     // Redundant: "Content" suffix
    "economyContent": {
      "paymentList": [...]               // Redundant: "List" suffix
    },
    "resourceContent": {
      "vehicle": {
        "attributeListVehicle": [...]    // Double redundancy
      }
    },
    "subOrderContent": {
      "idOrderList": [...]               // Redundant: "List" suffix
    }
  }]
}
```

---

## 3. Proposed Simplifications

### 3.1 Complete Before/After Mapping

| Current Name | Proposed Name | Context | Rationale |
|--------------|---------------|---------|-----------|
| `idVehicleList` | `ids` | vehicle | Array of IDs, context is vehicle |
| `idDriverList` | `ids` | driver | Array of IDs, context is driver |
| `idOrderList` | `orderIds` | subOrder | Need to distinguish from other IDs |
| `attributeListVehicle` | `attributes` | vehicle | Context provides scope |
| `attributeListDriver` | `attributes` | driver | Context provides scope |
| `attributeListContent` | `attributes` | content | Context provides scope |
| `contactInfoListContent` | `contactInfo` | content | Keep item type name (compound noun) |
| `contactInfoListDriver` | `contactInfo` | driver | Keep item type name (compound noun) |
| `contactInfoDriver` | `contactInfo` | driver | Keep item type name (compound noun) |
| `driverContacts` | `contactInfo` | driver | Use item type name |
| `economyContent` | `economy` | content | Drop redundant "Content" |
| `resourceContent` | `resource` | content | Drop redundant "Content" |
| `subOrderContent` | `subOrder` | content | Drop redundant "Content" |
| `paymentList` | `payments` | economy | Drop "List", use plural |
| `locationList` | `locations` | bulkLocationList | Already done in 2026 |
| `nodeList` | `nodes` | route | Already done in 2026 |
| `timeListNode` | `times` | node | Already done in 2026 |
| `contentList` | `contents` | node | Already done in 2026 |
| `vehicleStartLocation` | `startLocation` | resource | Context is resource |
| `contactInfoListOrg` | `contactInfo` | organization | Keep item type name |
| `idOrgArray` | `ids` | organization | Already done in 2026 |
| `manualDescriptionAddress` | `manualDescriptions` | address | Already done in 2026 |
| `textTimestamp` | `timestamps` | messageTo | Already done in 2026 |
| `scheduleElementList` | `schedules` | orderTemplate | Already done in 2026 |
| `economyReportList` | `economyReports` | orderReport | Already done in 2026 |
| `eventListReports` | `events` | orderReport | Already done in 2026 |
| `summaryReportList` | `summaryReports` | orderReport | Already done in 2026 |

### 3.2 Structural Changes

**Before (Current Draft 2026):**
```json
{
  "resource": {
    "vehicle": {
      "idVehicleList": [{"src": "...", "id": "..."}],
      "capacity": {...},
      "attributeListVehicle": [{"src": "...", "id": "..."}]
    },
    "driver": {
      "idDriver": {"src": "...", "id": "..."},
      "attributeListDriver": [{"src": "...", "id": "..."}],
      "contactInfoListDriver": [{"contactType": "phone", "contactInfo": "..."}]
    },
    "vehicleStartLocation": {"lat": 55.0, "lon": 13.0}
  }
}
```

**After (Proposed):**
```json
{
  "resource": {
    "vehicle": {
      "ids": [{"src": "...", "id": "..."}],
      "capacity": {...},
      "attributes": [{"src": "...", "id": "..."}]
    },
    "driver": {
      "id": {"src": "...", "id": "..."},
      "attributes": [{"src": "...", "id": "..."}],
      "contactInfo": [{"contactType": "phone", "contactValue": "..."}]
    },
    "startLocation": {"lat": 55.0, "lon": 13.0}
  }
}
```

**Content structure before:**
```json
{
  "contents": [{
    "contentType": "traveller",
    "nameContent": "John Doe",
    "idContent": {"src": "...", "id": "..."},
    "attributeListContent": [...],
    "economyContent": {
      "paymentList": [...]
    },
    "resourceContent": {
      "vehicle": {
        "attributeListVehicle": [...]
      }
    },
    "contactInfoListContent": [...],
    "subOrderContent": {
      "idOrderList": [...]
    }
  }]
}
```

**Content structure after:**
```json
{
  "contents": [{
    "contentType": "traveller",
    "name": "John Doe",
    "id": {"src": "...", "id": "..."},
    "attributes": [...],
    "economy": {
      "payments": [...]
    },
    "resource": {
      "vehicle": {
        "attributes": [...]
      }
    },
    "contactInfo": [...],
    "subOrder": {
      "orderIds": [...]
    }
  }]
}
```

---

## 4. Name Simplification Rules

### 4.1 Array Properties

| Rule | Example |
|------|---------|
| Drop "List" suffix | `paymentList` → `payments` |
| Use plural forms | `id` array → `ids` |
| Context-specific prefix when ambiguous | `idOrderList` → `orderIds` |

### 4.2 Nested Properties

| Rule | Example |
|------|---------|
| Drop parent type suffix | `vehicle.attributeListVehicle` → `vehicle.attributes` |
| Drop redundant "Content" suffix | `economyContent` → `economy` |
| Keep compound noun names | `contactInfoListDriver` → `contactInfo` |

### 4.3 Identifier Properties

| Current | Proposed | When |
|---------|----------|------|
| `idVehicle` | `id` | Single ID in vehicle context |
| `idVehicleList` | `ids` | Multiple IDs in vehicle context |
| `idDriver` | `id` | Single ID in driver context |
| `idContent` | `id` | Single ID in content context |
| `nameContent` | `name` | Name in content context |

---

## 5. Bulk Location Schema - UNCHANGED

The legacy bulk location schema (`SUTI_BulkLocation_legacy.schema.json`) remains completely unchanged:

```json
{
  "bulkLocationList": {
    "isComplete": true,
    "locationListType": 1,
    "msgSeqNo": 1,
    "msgCount": 1,
    "locations": [
      {
        "vehicleIdProvider": "123",
        "time": "2019-12-18T10:39:00.000Z",
        "status": "O",
        "lat": 59.339176,
        "lon": 17.991666
      }
    ]
  }
}
```

**Note:** The legacy schema already uses:
- `locations` (array form, not "locationList")
- Flat structure for `vehicleLocation` (intentionally simple for streaming)
- Single-letter status codes ("O", "F", "B", "N")

The modern 2026 schema (`SUTI_Message.schema.json`) also supports bulkLocation but with the same property names for compatibility.

---

## 6. XSD-JSON Mapping Update Required

The `plans/xsd-json-mapping.yaml` needs to be updated with these additional mappings:

```yaml
arrays:
  # NEW simplified mappings
  - xsd: "idVehicle (unbounded)"
    json: "ids"
    context: "vehicle"

  - xsd: "attributeListVehicle"
    json: "attributes"
    context: "vehicle"

  - xsd: "attributeListDriver"
    json: "attributes"
    context: "driver"

  - xsd: "attributeListContent"
    json: "attributes"
    context: "content"

  - xsd: "contactInfoListContent"
    json: "contacts"
    context: "content"

  - xsd: "contactInfoDriver"
    json: "contacts"
    context: "driver"

  - xsd: "formOfPayment (unbounded)"
    json: "payments"
    context: "economy"

  - xsd: "idOrderList"
    json: "orderIds"
    context: "subOrder"

# NEW structural simplifications
structural_simplifications:
  - xsd: "economyContent"
    json: "economy"
    context: "content"

  - xsd: "resourceContent"
    json: "resource"
    context: "content"

  - xsd: "subOrderContent"
    json: "subOrder"
    context: "content"

  - xsd: "idContent"
    json: "id"
    context: "content"

  - xsd: "nameContent"
    json: "name"
    context: "content"

  - xsd: "vehicleStartLocation"
    json: "startLocation"
    context: "resource"
```

---

## 7. Impact Assessment

### 7.1 Files Requiring Updates

| File | Changes Required |
|------|------------------|
| `schemas/SUTI_Message.schema.json` | Update property names in all $defs |
| `examples/JSON/draft_2026/2000_order.json` | Update property names |
| `examples/JSON/draft_2026/3003_dispatchConfirmation.json` | Update property names |
| `examples/JSON/draft_2026/4010_eventVehicle.json` | Update property names |
| `plans/xsd-json-mapping.yaml` | Add new simplified mappings |

### 7.2 Files NOT Affected

| File | Reason |
|------|--------|
| `schemas/SUTI_BulkLocation_legacy.schema.json` | Legacy schema, intentionally unchanged |
| `examples/JSON/draft_2026/1111_bulkLocationResponse.json` | Uses legacy structure |
| `examples/JSON/draft_2026/7000_keepAlive.json` | Header-only message |
| `examples/JSON/draft_2026/7001_keepAliveConfirmation.json` | Header-only message |
| `examples/JSON/draft_2026/2001_orderConfirmation.json` | Header-only message |

---

## 8. Migration Guide

### 8.1 Search and Replace Patterns

For implementers migrating from XSD/2021 format:

```
XML/2021 Property          →  JSON 2026 Property
--------------------          ------------------
attributeListVehicle      →  attributes (in vehicle)
attributeListDriver       →  attributes (in driver)
attributeListContent      →  attributes (in content)
contactInfoListContent    →  contactInfo (in content)
contactInfoListDriver     →  contactInfo (in driver)
idVehicleList             →  ids (in vehicle)
economyContent            →  economy (in content)
resourceContent           →  resource (in content)
subOrderContent           →  subOrder (in content)
paymentList               →  payments (in economy)
idOrderList               →  orderIds (in subOrder)
idContent                 →  id (in content)
nameContent               →  name (in content)
vehicleStartLocation      →  startLocation (in resource)
```

### 8.2 Transformation Example

**XML → JSON 2026:**

```xml
<content contentType="traveller">
  <idContent src="..." id="123"/>
  <nameContent>John Doe</nameContent>
  <attributeListContent>
    <idType src="SUTI:idAttribute" id="1001"/>
  </attributeListContent>
  <contactInfoListContent>
    <contactInfo contactType="phone">555-1234</contactInfo>
  </contactInfoListContent>
</content>
```

```json
{
  "contentType": "traveller",
  "id": {"src": "...", "id": "123"},
  "name": "John Doe",
  "attributes": [{"src": "SUTI:idAttribute", "id": "1001"}],
  "contactInfo": [{"contactType": "phone", "contactValue": "555-1234"}]
}
```

---

## 9. Design Decisions (Confirmed)

| Decision | Resolution | Rationale |
|----------|------------|-----------|
| `idContent` → `id` | ✅ **Yes** | Context provides meaning |
| `nameContent` → `name` | ✅ **Yes** | Simpler, no ambiguity |
| `ids` vs `vehicleIds` | ✅ **Context-dependent** | Use `ids` inside `vehicle` object; use `vehicleIds` at resource level |
| `economy.payments` structure | Keep `economy` wrapper | Allows future expansion (prices, fees, etc.) |

---

## 10. Implementation Checklist

### Phase 1: Schema Updates ✅
- [x] Update `content` definition with simplified property names
- [x] Update `vehicleResource` definition with simplified property names
- [x] Update `driverResource` definition with simplified property names
- [x] Update `economyContent` → `economy` naming
- [x] Update `resourceContent` → `resource` naming
- [x] Update `subOrderContent` → `subOrder` naming

### Phase 2: Example Updates ✅
- [x] Update 2000_order.json with new property names
- [x] Update 3003_dispatchConfirmation.json with new property names
- [x] Update 4010_eventVehicle.json with new property names
- [x] Validate all examples against updated schema

### Phase 3: Documentation ✅
- [ ] Update xsd-json-mapping.yaml with all simplifications
- [x] Update json-schema-alignment-plan.md
- [x] Add migration guide for implementers (included in alignment plan)

---

## 11. Success Criteria

- [x] All property names follow the simplification rules
- [x] No redundant context in nested property names
- [x] All arrays use plural forms without "List" suffix (except compound nouns like `contactInfo`)
- [x] Bulk location legacy schema completely unchanged
- [x] All examples validate against updated schema (12 files, all pass)
- [ ] XSD-JSON mapping documentation complete
- [x] Migration guide available for implementers

---

**Implementation Complete:** 2026-02-10

All schema and example updates have been applied. Legacy bulk location example added (`1111_bulkLocationResponse.legacy.json`) to demonstrate the wrapper format.

