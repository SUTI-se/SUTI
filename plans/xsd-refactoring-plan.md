# SUTI XSD Schema Refactoring Plan

**Date:** 2026-01-30
**Status:** Draft for Review
**Purpose:** Comprehensive plan for XSD modernization and JSON Schema preparation

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current State Analysis](#current-state-analysis)
3. [Industry Comparison](#industry-comparison)
4. [Modularization Strategy](#modularization-strategy)
5. [Simplification Opportunities](#simplification-opportunities)
6. [JSON Schema Considerations](#json-schema-considerations)
7. [Migration Path](#migration-path)
8. [Recommendations](#recommendations)

---

## Executive Summary

### Key Findings

| Aspect | Current State | Recommendation |
|--------|---------------|----------------|
| **Structure** | Single 3,131-line monolithic XSD | Split into 6 modular files |
| **Versioning** | No version attribute | Add namespace versioning |
| **Modularity** | No separation | Functional domain separation |
| **JSON Support** | None | Plan parallel JSON Schema |
| **Documentation** | 89.5% coverage | Complete to 100% |

### Recommended Path

1. **v1.x** - Non-breaking improvements (immediate)
2. **v2.0** - Modular restructuring (6-12 months)
3. **v2.x** - JSON Schema parallel track (12-18 months)

---

## Current State Analysis

### Schema Metrics

| Metric | Value |
|--------|-------|
| Total Lines | 3,131 |
| Complex Types | 86 |
| Message Types | 136 |
| Message Content Elements | 28 |
| Optional Elements | 217 |
| Documentation Coverage | 89.5% |

### Message Flow Breakdown

**Order-by-Order Flow:**
- 16 specific types
- 47 total types in cluster
- Messages: 2000-2099, 4000-4999, 6000-6999

**Driver Session Flow:**
- 6 specific types (only 4 truly unique)
- 52 total types in cluster
- Messages: 2100-2199
- **Key finding:** Only `changelog`, `log`, `orders`, `sessionNode` are exclusive

**Accounting Flow:**
- 12 specific types
- Messages: 8000-8999

**Resource Management:**
- 7 types shared across all flows
- Messages: 1000-1999, 3000-3999

**Shared Infrastructure:**
- 46 types used by 3+ flows
- `idType` used by 36 types (most depended upon)

### Critical Issues Identified

1. **Message choice `minOccurs="0"`** (line 174) - allows empty messages
2. **Deprecated `nodeCancelation`** still present (misspelling)
3. **No versioning strategy** - no schema version attribute
4. **Enumeration inconsistency** - dual numeric/text representation
5. **~50+ inline anonymous types** - reduces reusability

---

## Industry Comparison

### How Similar Standards Handle Modularization

| Standard | Files | Approach | Versioning | JSON Support |
|----------|-------|----------|------------|--------------|
| **NeTEx** | 6 parts | Functional domains | Namespace + branches | No |
| **SIRI** | 6 parts | Service modules | Branch-based | No |
| **GTFS** | 7+ CSV | File per entity | Metadata field | Partial |
| **DATEX II** | Generated | Profile-based | Version number | Emerging |
| **MaaS** | JSON Schema | Domain entities | Evolving | Native |
| **SUTI** | 1 XSD | Monolithic | None | No |

### Key Industry Patterns

**1. Modular File Structure**
Every modern standard uses modular structure:
- NeTEx: 6 functional parts (network, timetables, fares, etc.)
- SIRI: 10+ service modules
- GTFS: 7 required + 15 optional files

**2. Shared Core/Infrastructure**
All modular standards extract common types:
- NeTEx Part 1 framework reused by all parts
- SIRI common services module
- DATEX II core PIM model

**3. Namespace Versioning**
Major versions get new namespace:
```
v1: http://suti.se/schema/v1
v2: http://suti.se/schema/v2
```

**4. Extension Mechanisms**
- GTFS: Reserved ranges (1000-1999 official, 9000-9999 private)
- DATEX II: Abstract base classes
- W3C: `xs:any` wildcards for open extension points

---

## Modularization Strategy

### Question: Should the XSD be divided into several parts?

**Answer: Yes.** Analysis strongly supports modularization.

### Proposed Structure

```
schemas/
├── SUTI-Core.xsd              (~500 lines)
│   Core infrastructure used by ALL implementations
│
├── SUTI-OrderFlow.xsd         (~1,200 lines)
│   Order-by-order booking flow
│
├── SUTI-SessionFlow.xsd       (~300 lines)
│   Driver session management
│
├── SUTI-Resource.xsd          (~400 lines)
│   Resource (vehicle/driver) management
│
├── SUTI-Accounting.xsd        (~500 lines)
│   Billing and accounting
│
└── SUTI-Messages.xsd          (~200 lines)
    Root element and message routing
```

### Module Dependencies

```
SUTI-Messages.xsd
├── imports → SUTI-Core.xsd
├── imports → SUTI-OrderFlow.xsd
├── imports → SUTI-SessionFlow.xsd
├── imports → SUTI-Resource.xsd
└── imports → SUTI-Accounting.xsd

SUTI-OrderFlow.xsd
└── imports → SUTI-Core.xsd

SUTI-SessionFlow.xsd
├── imports → SUTI-Core.xsd
└── imports → SUTI-OrderFlow.xsd (for shared order types)

SUTI-Resource.xsd
└── imports → SUTI-Core.xsd

SUTI-Accounting.xsd
├── imports → SUTI-Core.xsd
└── imports → SUTI-OrderFlow.xsd (for order references)
```

### Module Contents

#### SUTI-Core.xsd (Infrastructure)

**16 Leaf Types (pure data structures):**
- `idType`, `idMsgRef`, `idEkInfo`
- `time`, `date`, `position`
- `bulkLocationList`, `contactInfo`
- `environmentalInformation`, `eventType`
- `gpsType`, `multiDispatch`
- `nodeCancelationType`, `nodeCancellationType`
- `orderStatus`, `weekdaysType`

**Shared Infrastructure Types:**
- `orgType`, `organizationType`, `agreement`
- `addressType`, `geographicLocation`
- `timesType`, `referencesTo`
- `attributesType`, `attribute`
- `contactInfosType`, `manualDescriptionType`
- `errorType`

#### SUTI-OrderFlow.xsd (Order-by-Order)

- `order`, `route`, `node`
- `contents`, `content`, `connection`
- `nodeprocess`, `process`
- `orderReject`, `cancellationConsequence`
- `pickupConfirmation`, `orderLink`
- `orderReport`, `orderTemplate`
- `subOrderType`, `requestContentType`
- `multiDispatch`, `product`

#### SUTI-SessionFlow.xsd (Driver Session)

**Unique types (4):**
- `driverSession`
- `changelog`, `log`
- `orders`
- `sessionNode`

**Plus re-uses from OrderFlow:**
- `order`, `route`, `node` (via import)

#### SUTI-Resource.xsd (Resources)

- `resourceType`
- `vehicle`, `driver`
- `capacity`, `seats`
- `vehicleDistance`, `vehicleLocation`
- `Validation`

#### SUTI-Accounting.xsd (Economy)

- `economyType`, `economyReport`
- `price`, `priceCalculation`
- `payment`, `formOfPayment`
- `deliveryNote`, `summaryReport`
- `calculationFareType`, `vatAmountSpecificationType`
- `amountType`, `exchangeRates`, `exhangeRate`
- `resourceReservation`, `associatedReservation`
- `suborderTourType`, `taxiMeter`

#### SUTI-Messages.xsd (Root)

- `SUTI` root element
- `msg` type with choice construct
- Message routing (`orgSender`, `orgReceiver`)
- 28 message content options

### Pros and Cons

#### Pros of Modularization

| Benefit | Impact |
|---------|--------|
| **Partial implementation** | Implementers only need relevant modules |
| **Easier maintenance** | Changes isolated to specific modules |
| **Clearer understanding** | Separation makes purpose obvious |
| **Parallel development** | Teams can work on different modules |
| **Better tooling** | IDE support improved for smaller files |
| **Aligned with industry** | Matches NeTEx, SIRI, DATEX II approach |

#### Cons of Modularization

| Challenge | Mitigation |
|-----------|------------|
| **Breaking change** | Phase as v2.0 major release |
| **Migration effort** | Provide XSLT transformation tools |
| **Import complexity** | Clear documentation + examples |
| **Testing overhead** | Automated cross-module validation |
| **Learning curve** | Comprehensive migration guide |

### Industry Comparison Summary

| Pattern | NeTEx | SIRI | DATEX II | SUTI Proposed |
|---------|-------|------|----------|---------------|
| Parts | 6 | 6 | Profiles | 6 |
| Approach | Functional | Service | Subset | Functional |
| Core module | Yes | Yes | Yes | Yes |
| Namespace | Versioned | Versioned | Versioned | Versioned |

**Conclusion:** The proposed structure aligns with proven industry patterns.

---

## Simplification Opportunities

### Question: Can the XSD be simplified without losing backward compatibility?

**Answer: Yes, in phases.**

### Phase 1: Non-Breaking Simplifications (v1.x)

#### 1. Fix Critical Validation Issue

**Current (line 174):**
```xml
<xs:choice minOccurs="0" maxOccurs="1">
```

**Fixed:**
```xml
<xs:choice minOccurs="1" maxOccurs="1">
```

**Impact:** Messages must have content (correct behavior)
**Risk:** Low - validates existing valid messages

#### 2. Extract Inline Anonymous Types

**Current pattern:**
```xml
<xs:element name="orderReject">
  <xs:complexType>
    <xs:complexContent>
      <xs:extension base="referencesTo">
        <!-- inline definition -->
      </xs:extension>
    </xs:complexContent>
  </xs:complexType>
</xs:element>
```

**Simplified:**
```xml
<xs:complexType name="orderRejectType">
  <xs:complexContent>
    <xs:extension base="referencesTo">
      <!-- extracted definition -->
    </xs:extension>
  </xs:complexContent>
</xs:complexType>

<xs:element name="orderReject" type="orderRejectType"/>
```

**Impact:** ~50 types can be extracted
**Risk:** None - purely structural, same validation

#### 3. Add Schema Version Attribute

**Current:** No version information

**Added:**
```xml
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           version="1.1.0"
           targetNamespace="http://suti.se/schema/v1"
           xmlns:suti="http://suti.se/schema/v1">
```

**Impact:** Enables versioning strategy
**Risk:** None - additive change

#### 4. Complete Documentation

**Current:** 89.5% coverage (37 types need improvement)

**Target:** 100% with examples

**Types needing documentation:**
- `Validation`, `addressType`, `amountType`
- `attribute`, `calculationFareType`, `calendarType`
- `contactInfo`, `content`, `contents`, `date`
- ... (see detailed findings)

#### 5. Fix Typos

**Current:**
- `exhangeRate` (line 1306) - should be `exchangeRate`
- `nodeCancelation` (line 250) - deprecated, correct is `nodeCancellation`

**Action:** Add deprecation warnings for misspelled elements

### Phase 2: Breaking Simplifications (v2.0)

#### 1. Remove Deprecated Elements

Remove (with 12-month warning):
- `nodeCancelation` (misspelling)
- `idVersion` at root level (rarely used per schema note)

#### 2. Standardize Enumerations

**Current (dual representation):**
```xml
<xs:enumeration value="3101"/>
<xs:enumeration value="client"/>
<xs:enumeration value="3102"/>
<xs:enumeration value="provider"/>
```

**Simplified (text only):**
```xml
<xs:enumeration value="client"/>
<xs:enumeration value="provider"/>
```

**Migration:** External mapping table for numeric equivalents

#### 3. Simplify Boolean Attribute Overuse

**Current:** `process` type has 10 boolean attributes (2^10 = 1024 combinations)

**Simplified:** Consider enum-based status or bitfield approach

#### 4. Flatten Excessive Nesting

Review and flatten:
- `msg` type (80 child elements)
- `referencesTo` (21 child elements)

### Backward Compatibility Matrix

| Change | v1.x Safe? | v2.0? | Notes |
|--------|------------|-------|-------|
| Fix minOccurs | Yes | - | Validates existing valid messages |
| Extract inline types | Yes | - | Same validation, better structure |
| Add version attribute | Yes | - | Purely additive |
| Complete documentation | Yes | - | No schema change |
| Fix typos | Warning | Yes | Deprecate then remove |
| Remove nodeCancelation | No | Yes | Breaking change |
| Standardize enums | No | Yes | Breaking change |
| Simplify booleans | No | Yes | Breaking change |

---

## JSON Schema Considerations

### Question: What must be considered before creating a JSON Schema generator?

### 1. Type Mapping Decisions

| XSD Type | JSON Schema Type | Considerations |
|----------|------------------|----------------|
| `xs:string` | `string` | Direct mapping |
| `xs:integer` | `integer` | Direct mapping |
| `xs:decimal` | `number` | Precision handling |
| `xs:boolean` | `boolean` | Direct mapping |
| `xs:date` | `string` + `format: "date"` | ISO 8601 format |
| `xs:dateTime` | `string` + `format: "date-time"` | ISO 8601 format |
| `xs:choice` | `oneOf` | Requires discriminator |
| `xs:sequence` | `object` + `required` | Order not enforced in JSON |
| `xs:extension` | `allOf` | Composition pattern |
| `xs:any` | `additionalProperties` | Extension mechanism |

### 2. Element Order

**XSD:** Element order enforced via `xs:sequence`
**JSON:** Object property order not guaranteed

**Solution:**
- Don't rely on order in JSON
- Use explicit sequence numbers where order matters
- Document required ordering in application logic

### 3. Attribute vs Element

**XSD:** Supports both attributes and elements
**JSON:** Only properties (no distinction)

**Strategy Options:**

**Option A: Prefix attributes with `@`**
```json
{
  "@msgType": "2000",
  "order": { ... }
}
```

**Option B: Flatten to properties**
```json
{
  "msgType": "2000",
  "order": { ... }
}
```

**Recommendation:** Option B (cleaner, more JSON-native)

### 4. Choice/Union Handling

**XSD `xs:choice`:**
```xml
<xs:choice>
  <xs:element name="order" type="order"/>
  <xs:element name="driverSession" type="driverSession"/>
</xs:choice>
```

**JSON Schema `oneOf` with discriminator:**
```json
{
  "oneOf": [
    { "$ref": "#/definitions/order" },
    { "$ref": "#/definitions/driverSession" }
  ],
  "discriminator": {
    "propertyName": "messageType"
  }
}
```

### 5. Enumeration Format

**Current XSD (dual values):**
```xml
<xs:enumeration value="3101"/>
<xs:enumeration value="client"/>
```

**JSON Schema (text only, recommended):**
```json
{
  "enum": ["client", "provider", "system"]
}
```

**Migration:** Standardize to text before JSON conversion

### 6. Extension Points

**XSD `xs:any`:**
```xml
<xs:any namespace="##other" processContents="lax"/>
```

**JSON Schema:**
```json
{
  "additionalProperties": true
}
```

Or with pattern:
```json
{
  "patternProperties": {
    "^x-": {}
  }
}
```

### 7. Naming Conventions

| XSD Convention | JSON Convention | Transformation |
|----------------|-----------------|----------------|
| `camelCase` | `camelCase` | Keep |
| `msgType` | `msgType` or `messageType` | Expand abbreviations? |
| `orgSender` | `organizationSender` | Expand abbreviations? |

**Recommendation:** Keep existing names for compatibility, document full names

### 8. Required Fields

**XSD:**
- `minOccurs="0"` = optional
- `minOccurs="1"` = required

**JSON Schema:**
```json
{
  "required": ["msgType", "idMsg"],
  "properties": {
    "msgType": { "type": "string" },
    "idMsg": { "$ref": "#/definitions/idType" }
  }
}
```

### 9. Null Handling

**XSD:** Absent elements (no null concept)
**JSON:** `null` values possible

**Strategy:**
```json
{
  "properties": {
    "optionalField": {
      "oneOf": [
        { "type": "string" },
        { "type": "null" }
      ]
    }
  }
}
```

Or disallow null:
```json
{
  "properties": {
    "optionalField": { "type": "string" }
  }
}
```

**Recommendation:** Disallow null, use absent properties for optional

### 10. Generation Tooling Options

| Tool | Approach | Pros | Cons |
|------|----------|------|------|
| **xsd2json** | Automated | Fast, consistent | May need customization |
| **Custom generator** | Tailored | Full control | Development effort |
| **Manual mapping** | Precise | Optimal output | Time-consuming |

**Recommendation:** Hybrid approach
1. Use automated tool for first pass
2. Custom post-processing for SUTI-specific patterns
3. Manual review and optimization

### 11. JSON Schema Modularity

Match XSD modular structure:

```
schemas/json/
├── core/
│   ├── id.schema.json
│   ├── time.schema.json
│   ├── address.schema.json
│   └── index.schema.json
├── order/
│   ├── order.schema.json
│   ├── node.schema.json
│   └── index.schema.json
├── session/
│   ├── driverSession.schema.json
│   └── index.schema.json
├── resource/
│   └── resource.schema.json
├── accounting/
│   └── economy.schema.json
└── suti-message.schema.json  (root)
```

### 12. OpenAPI Integration

**For REST APIs:**
```yaml
openapi: 3.1.0
info:
  title: SUTI API
  version: 2.0.0
paths:
  /orders:
    post:
      requestBody:
        content:
          application/json:
            schema:
              $ref: 'schemas/json/order/order.schema.json'
```

**OpenAPI 3.1.0 benefits:**
- 100% JSON Schema draft 2020-12 compatible
- Native schema validation
- Industry-standard documentation

### Pre-Generation Checklist

Before creating JSON Schema generator:

- [ ] **Standardize enumerations** (text only)
- [ ] **Extract inline types** (named types)
- [ ] **Document attribute vs element** mapping rules
- [ ] **Define null handling** policy
- [ ] **Establish naming conventions**
- [ ] **Choose extension mechanism** (additionalProperties or patternProperties)
- [ ] **Decide discriminator strategy** for choice types
- [ ] **Plan modular structure** matching XSD modules
- [ ] **Select generation tooling**
- [ ] **Define validation test suite**

---

## Migration Path

### Phase 1: v1.x Non-Breaking Improvements (1-3 months)

**Priority 1: Critical Fixes**
- [ ] Fix `minOccurs="0"` on message choice
- [ ] Add schema version attribute
- [ ] Add namespace declaration

**Priority 2: Structural Improvements**
- [ ] Extract inline anonymous types
- [ ] Complete documentation for all 37 under-documented types
- [ ] Add deprecation warnings for `nodeCancelation`
- [ ] Improve internal organization with comment sections

**Deliverables:**
- SUTI_Message.xsd v1.1.0
- Migration notes (minimal changes)
- Updated documentation

### Phase 2: v2.0 Modular Restructuring (6-12 months)

**Step 1: Schema Split**
- [ ] Create SUTI-Core.xsd
- [ ] Create SUTI-OrderFlow.xsd
- [ ] Create SUTI-SessionFlow.xsd
- [ ] Create SUTI-Resource.xsd
- [ ] Create SUTI-Accounting.xsd
- [ ] Create SUTI-Messages.xsd

**Step 2: Breaking Changes**
- [ ] Remove `nodeCancelation`
- [ ] Remove unused `idVersion` at root
- [ ] Standardize enumerations (text only)
- [ ] New namespace: `http://suti.se/schema/v2`

**Step 3: Tooling**
- [ ] XSLT transformation (v1 → v2)
- [ ] Validation scripts
- [ ] Example files for each module

**Deliverables:**
- 6 modular XSD files
- Migration guide
- XSLT transformations
- Validation tools
- Updated examples

### Phase 3: v2.x JSON Schema (12-18 months)

**Step 1: Preparation**
- [ ] Finalize XSD v2.0 structure
- [ ] Define JSON-specific conventions
- [ ] Create generator tooling

**Step 2: Generation**
- [ ] Generate JSON Schema from XSD
- [ ] Post-process for optimizations
- [ ] Validate against sample data

**Step 3: API Integration**
- [ ] OpenAPI 3.1 specification
- [ ] REST API guidelines
- [ ] Bidirectional conversion tools

**Deliverables:**
- JSON Schema files (mirroring XSD modules)
- OpenAPI specification
- XML ↔ JSON conversion tools
- API implementation guide

### Timeline

```
2026 Q1-Q2:  v1.x improvements (current)
2026 Q3-Q4:  v2.0 modular development
2027 Q1:     v2.0 release + migration period
2027 Q2-Q4:  JSON Schema development
2028 Q1:     JSON Schema release
```

### Support Matrix

| Version | Release | Active Support | Security Only |
|---------|---------|----------------|---------------|
| v1.x | Current | Until v2.0+6mo | +12mo |
| v2.0 | 2027 Q1 | Until v2.1 | +24mo |
| JSON | 2028 Q1 | Ongoing | Ongoing |

---

## Recommendations

### Immediate Actions (This Sprint)

1. **Fix critical validation issue**
   - Change `minOccurs="0"` to `minOccurs="1"` on message choice

2. **Add schema version**
   - Add `version="1.1.0"` attribute
   - Add `targetNamespace="http://suti.se/schema/v1"`

3. **Create v1.x release**
   - Non-breaking improvements only
   - Document all changes

### Short-Term (Next 3 Months)

1. **Extract inline types**
   - ~50 anonymous types → named types

2. **Complete documentation**
   - 37 types need improvement
   - Add examples to all complex types

3. **Add deprecation warnings**
   - `nodeCancelation` → use `nodeCancellation`
   - `idVersion` → to be removed in v2.0

### Medium-Term (6-12 Months)

1. **Design modular structure**
   - Finalize 6-module architecture
   - Define import relationships
   - Create dependency documentation

2. **Develop v2.0**
   - Implement modular XSD files
   - Create migration tooling
   - Build validation suite

3. **Community engagement**
   - Announce v2.0 plans
   - Gather implementer feedback
   - Form technical committee

### Long-Term (12-24 Months)

1. **Release v2.0**
   - Modular XSD structure
   - 6-month parallel support with v1.x

2. **Develop JSON Schema**
   - Map XSD v2.0 to JSON Schema
   - Create OpenAPI specification
   - Build conversion tools

3. **API Guidelines**
   - REST API design patterns
   - Authentication standards
   - Rate limiting recommendations

---

## Summary

### Key Decisions Required

1. **Modularization:** Approve 6-module structure
2. **Versioning:** Confirm namespace versioning approach
3. **Enumerations:** Approve text-only standardization
4. **Timeline:** Validate proposed milestones
5. **JSON Schema:** Confirm parallel development track

### Success Criteria

| Metric | Current | Target |
|--------|---------|--------|
| Schema files | 1 | 6 |
| Documentation | 89.5% | 100% |
| Version tracking | None | Semantic versioning |
| JSON support | None | Full JSON Schema |
| Validation tools | None | Automated suite |

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Migration resistance | Medium | High | Long transition period, tooling |
| Breaking changes | High | Medium | v2.0 major release, clear communication |
| Complexity increase | Low | Medium | Good documentation, examples |
| Resource constraints | Medium | Medium | Phased approach, community involvement |

---

## Related Documents

- [xsd-analysis-executive-summary.md](xsd-analysis-executive-summary.md) - Executive summary
- [xsd-analysis-findings.md](xsd-analysis-findings.md) - Detailed technical analysis
- [xsd-dependency-analysis.md](xsd-dependency-analysis.md) - Type dependencies
- [xsd-additional-findings.md](xsd-additional-findings.md) - Supplemental findings

---

**Prepared for:** SUTI Technical Committee
**Author:** Claude Code Analysis
**Date:** 2026-01-30
**Status:** Draft for Review
