# SUTI JSON Schema: Legacy Work Analysis & Alignment with New Profile Proposal

**Date:** 2026-01-30 (Updated)
**Purpose:** Analyze the 2021 JSON work in context of the new profile-based XSD refactoring proposal
**Legacy Work Location:** `.claude/context/old_json/`

---

## Key Constraints (2026)

Before analyzing the legacy work, the following constraints must be acknowledged:

1. **XSD backward compatibility** - The XSD(s) must remain backward compatible, at least in the first iteration
2. **JSON Schema derived from XSD** - JSON Schema shall be generated from the XSD, not independently designed
3. **XSD as single source of truth** - The XSD defines the standard; JSON is a serialization format

These constraints **differ from the 2021 approach**, which explicitly abandoned XSD-derivation.

---

## Executive Summary

The 2021 JSON work provides **valuable insights** but followed a different philosophy:

| Aspect | 2021 Approach | 2026 Requirement |
|--------|---------------|------------------|
| Source of truth | JSON Schema (independent) | XSD (authoritative) |
| JSON Schema creation | Hand-crafted, JSON-first | Generated from XSD |
| Naming conventions | JSON-idiomatic (plurals, arrays) | Must match XSD element names |
| Structure | Simplified for JSON | Must reflect XSD structure |

**Key finding:** The 2021 examples are useful as **validation targets** and **usability references**, but cannot be the basis for JSON Schema generation. The JSON Schema must be derived from XSD to ensure consistency.

**What can be preserved:**
- The examples serve as test cases for XSD-to-JSON conversion
- Usability improvements can inform XSD refactoring (where backward compatible)
- The message coverage provides a validation baseline

---

## Legacy Work Inventory

### Files Found (2019-2021)

| File | Message Type | Flow | Status |
|------|-------------|------|--------|
| `2000_order.json` | Order | Basic | Complete |
| `2001_orderConfirmation.json` | Order Confirmation | Basic | Complete |
| `2002_orderReject.json` | Order Reject | Basic | Syntax errors |
| `3003_dispatchConfirmation.json` | Dispatch Confirmation | Standard | Complete |
| `4010_eventVehicle.json` | Event/Pickup Confirmation | Standard | Complete |
| `5000_messageToVehicle.json` | Message to Vehicle | Communication | Complete |
| `5020_locationRequest.json` | Location Request | Communication | Complete |
| `5021_locationResponse.json` | Location Response | Communication | Complete |
| `7000_keepAlive.json` | Keep Alive | Technical | Complete |
| `7001_keepAliveConfirmation.json` | Keep Alive Confirmation | Technical | Complete |
| `1111_bulkLocationResponse.json` | Bulk Location Response | Resource | Complete |

**Note:** A `validerade20210317/` subfolder contains validated versions from March 2021.

---

## Design Decisions from 2021 (agenda.txt)

The `agenda.txt` file documents key decisions made by the working group:

### 1. JSON Schema Per Message

> "vi har lämnat iden att utgå ifrån xml schemat, skall vara ett JSON schemat"
> "Tanken är att vi skall ha ett JSON schema per specificerat telegram"

**Translation:** Abandoned the idea of deriving from XSD; instead create a native JSON Schema per message type.

**Alignment with Profile Proposal:** ✅ **Perfect alignment**
- Profile-based approach also proposes per-flow/per-message schemas
- JSON Schema per message enables selective implementation

### 2. Common Schema for Shared Elements

> "Om där finns delar som är gemensamt med telegrammen så skall vi kolla på att ha dessa i ett separat gemensamt schema"

**Translation:** Shared parts should be in a separate common schema.

**Alignment with Profile Proposal:** ✅ **Perfect alignment**
- `SUTI-Core.xsd` → `suti-core.schema.json`
- Common types referenced via `$ref`

### 3. Structure: Header + Message Body

> "Tanken är att vi har en sutiheader, msgheader och sedan respektive meddelande"

**Translation:** Structure is SUTI header + msg header + message-specific content.

**Observed in Examples:**
```json
{
  "SUTI_2000_order": {
    "msg": { /* header */ },
    "order": { /* message body */ }
  }
}
```

**Alignment with Profile Proposal:** ✅ **Consistent**
- Profile approach maintains this separation
- Root element named `SUTI_{msgType}_{msgName}`

### 4. Array Naming Conventions

> "Array av referencesTo, attributeContent skulle heta attributesContent"
> "attributesVehicle, attributesContent skall vara array av idAttribute"
> "Om finns t.ex många idVehicle ... skall vi göra en array med plural idVehicleArray"

**Translation:** Use plural names for arrays; rename singular to plural.

**Observed in Examples:**
| XSD Name | JSON Name |
|----------|-----------|
| `referencesTo` (implied singular) | `referencesTo` (array) |
| `attributeContent` | `attributesContent` |
| `idVehicle` (multiple) | `idVehicleArray` |
| `formOfPayment` | `payments` |
| `contactInfoDriver` | `contactInfosDriver` |
| `seats` (with positions) | `positions` (array) |

**Alignment with Profile Proposal:** ⚠️ **Carry forward**
- These conventions should be documented and maintained
- JSON-idiomatic naming improves usability

---

## Structural Analysis of Legacy Examples

### Common Message Header Pattern

All messages share this structure:

```json
{
  "msg": {
    "msgType": "XXXX",
    "msgTimeStamp": "ISO-8601",
    "orgSender": {
      "name": "string",
      "idOrg": { "src": "string", "id": "string", "unique": boolean }
    },
    "orgReceiver": {
      "name": "string",
      "idOrg": { "src": "string", "id": "string", "unique": boolean }
    },
    "idMsg": { "src": "string", "id": "string", "unique": boolean },
    "referencesTo": [ /* array of id objects */ ]
  }
}
```

**Recommendation:** Extract this as `suti-msg-header.schema.json`

### ID Type Pattern

Consistent across all examples:

```json
{
  "src": "namespace:type",
  "id": "value",
  "unique": true|false
}
```

**Recommendation:** Define as `$defs/idType` in core schema

### Geographic Location Pattern

```json
{
  "typeOfCoordinate": "WGS-84",
  "lat": 55.000000,
  "lon": 13.000000,
  "precision": 6
}
```

**Note:** Uses `lon` instead of XSD's `long` (reserved word in many languages).

---

## Coverage Analysis: Legacy vs Profile Proposal

### Messages Covered by 2021 Work

| Profile | Message | 2021 Status | Completeness |
|---------|---------|-------------|--------------|
| **Basic** | 2000 Order | ✅ Done | Full example |
| **Basic** | 2001 OrderConfirmation | ✅ Done | Full example |
| **Basic** | 2002 OrderReject | ⚠️ Syntax errors | Needs fix |
| **Basic** | 7000 KeepAlive | ✅ Done | Full example |
| **Basic** | 7001 KeepAliveConfirmation | ✅ Done | Full example |
| **Standard** | 3003 DispatchConfirmation | ✅ Done | Full example |
| **Standard** | 4010 EventVehicle | ✅ Done | Full example |
| **Standard** | 5000 MessageToVehicle | ✅ Done | Full example |
| **Standard** | 5020 LocationRequest | ✅ Done | Full example |
| **Standard** | 5021 LocationResponse | ✅ Done | Full example |
| **Full** | 1111 BulkLocationResponse | ✅ Done | Full example |

### Messages NOT Covered (Gaps)

| Profile | Message | Priority |
|---------|---------|----------|
| **Standard** | 3000 DispatchRequest | High |
| **Standard** | 6001 OrderReport | High |
| **Advanced** | 6500-6511 DeliveryNote | Medium |
| **Session** | 2100-2105 DriverSession | Medium |
| **Full** | 8xxx Accounting | Low |
| **Full** | 2800-2810 RepetitiveOrders | Low |

---

## Recommendations

### 1. Use Legacy Examples as Validation Targets

The 2021 examples **cannot be the source** for JSON Schema, but they can serve as:

- **Test cases:** Verify that XSD-generated JSON Schema can validate similar structures
- **Usability benchmarks:** Compare generated JSON against hand-crafted JSON
- **Gap analysis:** Identify where XSD-to-JSON conversion produces awkward results

**Action:** Fix syntax errors and use as test suite for JSON Schema generator.

### 2. JSON-Idiomatic Naming in Hybrid Approach

Since the recommended strategy is a **hybrid approach** (see [json-schema-strategy-2026.md](json-schema-strategy-2026.md)), the 2021 naming conventions CAN be adopted:

- JSON element names can differ from XSD
- Explicit mapping documentation bridges the gap
- Best of both worlds: XSD as authority, JSON as developer-friendly

### 3. Evaluate XSD-to-JSON Generation Tools

Since JSON Schema should be informed by XSD, evaluate:

- **xsd2json** - Direct XSD to JSON Schema conversion
- **JAXB + jsonschema-generator** - Via Java classes
- **Custom XSLT** - Transform XSD to JSON Schema
- **Manual mapping with automation** - Hybrid approach

**Action:** Prototype JSON Schema generation from current SUTI XSD.

---

## Conclusion

The 2021 JSON work provides **useful reference material** and **demonstrates JSON-idiomatic patterns** that should be adopted in the hybrid approach.

### What the 2021 Work IS Useful For:

1. **Validation test cases** - The 11 examples can validate that JSON Schema produces reasonable results
2. **Usability benchmark** - Compare generated JSON against hand-crafted JSON to identify awkward patterns
3. **Coverage baseline** - Shows which messages were prioritized (Basic, Standard profiles)
4. **Historical context** - Documents decisions made and why (agenda.txt)
5. **JSON naming patterns** - Demonstrates idiomatic JSON that should be adopted

### Reconciliation Path:

```
2021 Approach              2026 Hybrid Approach
─────────────────────────────────────────────────────
JSON Schema (hand-crafted)  →  JSON Schema (designed with mapping)
JSON-idiomatic naming       →  JSON-idiomatic naming (KEPT!)
Independent design          →  XSD is authoritative (with mapping)
Examples as templates       →  Examples as test cases + usability guide
```

**Recommendation:** The hybrid approach allows preserving the JSON-idiomatic design from 2021 while maintaining XSD as the authoritative source through explicit mapping documentation.

---

## Related Documents:

- [json-schema-strategy-2026.md](json-schema-strategy-2026.md) - Strategy document
- [xsd-anomalies-for-json.md](xsd-anomalies-for-json.md) - Anomalies to fix
- [profile-based-standard-analysis.md](profile-based-standard-analysis.md) - Profile proposal
- [TC-presentation-json-generation-sv.md](TC-presentation-json-generation-sv.md) - TC presentation

---

**Prepared for:** SUTI Technical Committee
**Date:** 2026-01-30 (updated 2026-02-09)
