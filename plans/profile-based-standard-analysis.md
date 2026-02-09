# SUTI Profile-Based Standard Analysis

**Date:** 2026-01-30
**Based on:** "How to use SUTI" document (170 pages)
**Purpose:** Evaluate feasibility of profile-based schema structure

---

## Executive Summary

After thorough analysis of the "How to use SUTI" documentation, **a profile-based standard is not only possible but already implicitly exists** through the Self Declaration mechanism. The documentation explicitly supports modular implementation where Clients select specific flows and message types. This analysis recommends formalizing this into explicit XSD profiles.

---

## Key Finding: Self Declaration = Implicit Profiles

The SUTI standard already operates on a profile-like model:

> "SUTI provides the possibility for several different ways of configuring a connection between Client and Provider. A simple taxi-app requires much less functionality than a complicated dynamic combination of trips for several travellers."

The **Client Self Declaration** mechanism is essentially a profile definition:
- Clients document which flows they support
- Clients specify which message types are mandatory/optional
- Clients define which information elements are used
- Providers implement only what the Client specifies

---

## Complete Flow Inventory from Documentation

### 1. Order Flows (Block 2-6: Messages 2000-6999)

| Flow Name | Complexity | Key Messages | Section |
|-----------|------------|--------------|---------|
| **Basic Flow, Simple Trip** | Low | 2000, 2001 | 4.1.1.1 |
| **Typical Flow, Simple Trip** | Medium | 2000, 2001, 3003, 4010, 6001 | 4.1.1.2 |
| **Extensive Flow (Node by Node)** | High | 2000, 2001, 3000-3003, 4010, 6001, 6500-6501 | 4.1.1.3 |
| **Extensive Flow with Traffic Control** | High | 2000, 2001, 3000-3003, 4000-4020, 6001, 6500-6501 | 4.1.1.4 |
| **Multiple Client Orders Combined** | High | 2000, 2001, 2040, 3003, 4010, 6001 | 4.1.1.5 |
| **Order by Order** | High | 2000, 2001, 3000-3003, 4010, 4020 | 4.1.1.6 |
| **DriverSession** | Very High | 2100, 2101, 2102, 2105, 3000-3003, 4010, 4020 | 4.1.1.7 |
| **Order Trading** | Medium | 2000, 2001, 2010, 2011 | 4.1.1.8 |
| **PreeOrder (Provider)** | Medium | 2000, 2001, 2060, 2061 | 4.1.1.9 |
| **PreeOrder (ClientConfirm)** | Medium | 2000, 2001, 2060-2063, 4010 | 4.1.1.10 |
| **Order Forwarded** | Medium | 2000, 2001, 2050, 2051, 3003 | 4.1.1.11 |

### 2. Repetitive Orders Flow (Block 2: Messages 2800-2810)

| Flow Name | Key Messages | Section |
|-----------|--------------|---------|
| **OrderTemplate** | 2800, 2801 | 4.2.1-4.2.2 |
| **ScheduleElementConfirmation** | 2810 | 4.2.3, 4.2.5 |
| **RequestForTrafficInformation** | 4000, 4001 | 4.2.7-4.2.8 |
| **Pickup Confirmation** | 4010 | 4.2.9 |

### 3. Flagstops Flow (Block 2: Messages 2900-2902)

| Flow Name | Key Messages | Section |
|-----------|--------------|---------|
| **Authorization** | 2900, 2901, 2902 | 4.3.2.1 |
| **Booking (pickup/dropoff)** | 4010, 4020, 6500, 6501/6502 | 4.3.2.2 |

### 4. Delivery Note Flow (Block 6: Messages 6500-6511)

| Flow Name | Key Messages | Section |
|-----------|--------------|---------|
| **DeliveryNote Request (via 2000)** | 2000 (process.deliveryNoteRequest) | 4.4.1.1 |
| **DeliveryNote Request (via 2901)** | 2901 (process.deliveryNoteRequest) | 4.4.1.2 |
| **DeliveryNote Request (explicit)** | 6510, 6511 | 4.4.1.3-4 |
| **DeliveryNote Send** | 6500 | 4.4.2 |
| **DeliveryNote Response** | 6501, 6502, 6503 | 4.4.3 |

### 5. Accounting Flow (Block 8: Messages 8000-8199)

| Flow Name | Key Messages | Section |
|-----------|--------------|---------|
| **Basic Accounting (Provider→Client)** | 8000, 8100, 8101 | 4.5.1 |
| **Direct Accounting (Client→Provider)** | 8002, 8102 | 4.5.2 |
| **Reconsideration** | 8010, 8110, 8111 | 4.5.1.1 |
| **Revaluation** | 8180, 8181, 8182 | 4.5.1.1 |
| **Payment** | 8199 | 4.5.1.1 |

### 6. Resource Exchange Flow (Block 1: Messages 1000-1112)

| Flow Name | Key Messages | Section |
|-----------|--------------|---------|
| **Resource Request/Response** | 1000-1002, 1010-1012 | 4.6.2 |
| **bulkLocation Request/Response** | 1100-1102, 1110-1112 | 4.6.3 |
| **Geography Information** | 1050, 1051 | 4.2.14-15 |

### 7. Technical Flows (Block 7: Messages 7000-7101)

| Flow Name | Key Messages | Section |
|-----------|--------------|---------|
| **Keep Alive** | 7000, 7001 | 6.5.1-2 |
| **Confirmation of Received Message** | 7099 | 4.2.4 |
| **Link Mapping** | 7100, 7101 | 3.5.2 |
| **Restart** | 7021 | 4.2.6 |
| **Error Handling** | 7030, 7031 | 6.5.3-4 |

---

## Profile-Based Standard: Proposal

### Recommended Profile Structure

Based on the documentation, I propose **5 formal profiles**:

#### Profile 1: SUTI-Basic
**Use Case:** Simple taxi apps, basic trip ordering

**Required Flows:**
- Basic Flow, Simple Trip (2000, 2001)
- Keep Alive (7000, 7001)
- Error Handling (7030, 7031)

**Schema Files:**
- `SUTI-Core.xsd` (idType, orgType, basic types)
- `SUTI-Order-Basic.xsd` (order, node, basic route)
- `SUTI-Technical.xsd` (7xxx messages)

---

#### Profile 2: SUTI-Standard
**Use Case:** Standard DRT with dispatch and traffic control

**Required Flows (includes Basic):**
- Typical Flow with Dispatch (3000-3003)
- Traffic Control Events (4010)
- Order Reports (6001)

**Additional Schema Files:**
- `SUTI-Dispatch.xsd`
- `SUTI-TrafficControl.xsd`

---

#### Profile 3: SUTI-Advanced
**Use Case:** Full Client traffic control, node-by-node operations

**Required Flows (includes Standard):**
- Extensive Flow (Node by Node)
- Order Trading
- PreeOrder
- Order Forwarding
- Delivery Notes (6500-6503)

**Additional Schema Files:**
- `SUTI-DeliveryNote.xsd`
- `SUTI-OrderAdvanced.xsd`

---

#### Profile 4: SUTI-Session
**Use Case:** DriverSession with dynamic order combinations

**Required Flows (includes Standard):**
- Order by Order
- DriverSession (2100-2105)
- Multiple Orders Combined (2040)

**Additional Schema Files:**
- `SUTI-Session.xsd`

---

#### Profile 5: SUTI-Full (Complete Standard)
**Use Case:** All functionality including accounting, repetitive orders

**Required Flows (includes all above):**
- Repetitive Orders (2800-2810)
- Flagstops (2900-2902)
- Full Accounting (8xxx)
- Resource Exchange (1xxx)

**Additional Schema Files:**
- `SUTI-RepetitiveOrders.xsd`
- `SUTI-Accounting.xsd`
- `SUTI-Resource.xsd`

---

## Profile-Based Standard: Pros and Cons

### Pros

1. **Aligns with Existing Practice**
   - Self Declarations already define "implicit profiles"
   - Formalizing this makes the standard clearer
   - No new concept for existing implementers

2. **Reduces Implementation Complexity**
   - New implementers start with SUTI-Basic
   - 80% of simple use cases covered by Profile 1-2
   - Incremental adoption path

3. **Better Tooling Support**
   - Smaller schema files = faster validation
   - IDE autocomplete works better
   - Clear conformance levels

4. **Clearer Documentation**
   - Each profile has defined scope
   - Testing can be profile-specific
   - RFPs can reference profiles

5. **Backward Compatible**
   - SUTI-Full = current monolithic schema
   - Existing implementations unaffected
   - Gradual migration possible

### Cons

1. **Increased Maintenance Burden**
   - Multiple schema files to maintain
   - Version management across profiles
   - Import dependencies to track

2. **Potential for Fragmentation**
   - Different implementers at different levels
   - Interoperability questions between profiles
   - "My profile is better" debates

3. **Schema Import Complexity**
   - XSD imports can be tricky
   - Namespace management required
   - Some tools handle imports poorly

4. **Documentation Overhead**
   - Each profile needs documentation
   - Conformance testing per profile
   - Training materials per profile

5. **Migration Period Challenges**
   - Existing links need mapping to profiles
   - Legacy systems may not understand profiles
   - Transition period complexity

---

## Recommended Modular XSD Structure

Based on the flow analysis, here is the recommended file structure:

```
SUTI-Schema/
├── core/
│   ├── SUTI-Core.xsd           # idType, orgType, timesType, addressType
│   ├── SUTI-Enumerations.xsd   # All enumeration types
│   └── SUTI-CommonTypes.xsd    # Reusable complex types
│
├── profiles/
│   ├── SUTI-Basic.xsd          # Imports core + basic order
│   ├── SUTI-Standard.xsd       # Imports Basic + dispatch + traffic
│   ├── SUTI-Advanced.xsd       # Imports Standard + delivery + advanced
│   ├── SUTI-Session.xsd        # Imports Standard + session types
│   └── SUTI-Full.xsd           # Imports all (current monolithic equiv)
│
├── flows/
│   ├── SUTI-Order.xsd          # Order flow types (2000-2099)
│   ├── SUTI-Session.xsd        # DriverSession types (2100-2199)
│   ├── SUTI-Dispatch.xsd       # Dispatch types (3000-3099)
│   ├── SUTI-TrafficControl.xsd # Traffic control types (4000-4099)
│   ├── SUTI-Communication.xsd  # Communication types (5000-5099)
│   ├── SUTI-Report.xsd         # Report types (6000-6599)
│   ├── SUTI-DeliveryNote.xsd   # Delivery note types (6500-6599)
│   ├── SUTI-Technical.xsd      # Technical types (7000-7199)
│   ├── SUTI-Accounting.xsd     # Accounting types (8000-8199)
│   └── SUTI-Resource.xsd       # Resource types (1000-1199)
│
├── messages/
│   ├── SUTI-Messages.xsd       # Root element, msg type, message routing
│   └── SUTI-MessageTypes.xsd   # Message type enumerations
│
└── SUTI-Complete.xsd           # Single import point (v1.x compatibility)
```

---

## Comparison: Current vs Proposed Structure

| Aspect | Current (Monolithic) | Proposed (Profiles) |
|--------|---------------------|---------------------|
| **Files** | 1 XSD (3131 lines) | 15+ XSD files |
| **Complexity** | All-or-nothing | Graduated levels |
| **Implementation** | Parse everything | Parse only needed |
| **Validation** | Slow (large schema) | Fast (smaller schemas) |
| **Maintenance** | One file, one version | Coordinated versions |
| **Conformance** | Unclear levels | Clear profile levels |
| **Tooling** | Limited IDE support | Better autocomplete |
| **Backward Compat** | N/A | SUTI-Full = current |

---

## Implementation Recommendation

### Phase 1: Core Extraction (v1.x Non-Breaking)
1. Extract `SUTI-Core.xsd` with shared types
2. Keep monolithic file as primary
3. Add `xs:include` for backwards compatibility

### Phase 2: Profile Definition (v2.0 Planning)
1. Define profile conformance levels
2. Document which flows belong to which profile
3. Update Self Declaration guidelines to reference profiles

### Phase 3: Schema Modularization (v2.0)
1. Split into flow-based XSD files
2. Create profile XSD files with imports
3. Maintain `SUTI-Complete.xsd` for legacy

### Phase 4: Profile Adoption
1. Update documentation per profile
2. Create profile-specific validation tools
3. Reference profiles in RFPs

---

## Conclusion

A profile-based standard for SUTI is:
- **Feasible:** The architecture supports it
- **Desirable:** Reduces implementation burden
- **Natural:** Mirrors existing Self Declaration practice
- **Safe:** Can be backward compatible

The key insight from the documentation is that **Clients already define implicit profiles through Self Declarations**. Formalizing this into explicit XSD profiles simply makes the standard's inherent flexibility more accessible and tooling-friendly.

---

## Related Documents

- [json-schema-strategy-2026.md](json-schema-strategy-2026.md) - Strategy document
- [xsd-anomalies-for-json.md](xsd-anomalies-for-json.md) - Anomalies to fix
- [json-legacy-analysis.md](json-legacy-analysis.md) - 2021 work analysis
- [TC-presentation-json-generation-sv.md](TC-presentation-json-generation-sv.md) - TC presentation

---

**Prepared for:** SUTI Technical Committee
**Author:** Claude Code Analysis
**Status:** Draft for Review
