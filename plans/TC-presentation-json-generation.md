# SUTI Schema Modernization
## Technical Committee Presentation

**Topic:** XSD Refactoring & JSON Schema Strategy
**Date:** 2026-01-30
**Presenter:** [Your Name]

---

# AGENDA

1. Current State Analysis
2. Key Finding: Implicit Profiles
3. Proposed Profile-Based Structure
4. JSON Schema Path Forward
5. Recommended Roadmap
6. Discussion

---

# 1. CURRENT STATE

## Schema at a Glance

```
+------------------+------------------+
|     METRIC       |      VALUE       |
+------------------+------------------+
| Schema Size      | 3,131 lines      |
| Complex Types    | 86               |
| Message Types    | 136              |
| Flows Identified | 12 categories    |
| Documentation    | 89.5% coverage   |
+------------------+------------------+
```

## The Challenge

- **Single monolithic XSD** - difficult to navigate
- **All-or-nothing** implementation required
- **No clear conformance levels** for RFPs
- **JSON transition** needs clean structure

---

# 2. KEY FINDING: IMPLICIT PROFILES EXIST

## From "How to use SUTI" Documentation:

> "SUTI provides the possibility for several different ways
> of configuring a connection between Client and Provider.
> A simple taxi-app requires much less functionality than
> a complicated dynamic combination of trips."

## Self Declarations = Implicit Profiles

```
  CLIENT SELF DECLARATION
  +-----------------------------------------+
  |  "We support these flows:"              |
  |  [x] Basic Order (2000, 2001)           |
  |  [x] Dispatch (3xxx)                    |
  |  [x] Traffic Control (4xxx)             |
  |  [ ] DriverSession (21xx)      <-- NO   |
  |  [ ] Accounting (8xxx)         <-- NO   |
  +-----------------------------------------+
        ^
        |
        This IS a profile!
```

**80% of implementations use only a subset of features**

---

# 3. PROPOSED: EXPLICIT PROFILES

## Five Conformance Levels

```
  SUTI-Full ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    + Repetitive Orders, Flagstops, Accounting     ┃
                                                   ┃
  SUTI-Session ━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓       ┃
    + DriverSession (21xx), Order combos   ┃       ┃
                                           ┃       ┃
  SUTI-Advanced ━━━━━━━━━━━━━━━━━━━┓       ┃       ┃
    + Node-by-node, Delivery Notes ┃       ┃       ┃
                                   ┃       ┃       ┃
  SUTI-Standard ━━━━━━━━━━━┓       ┃       ┃       ┃
    + Dispatch, Traffic    ┃       ┃       ┃       ┃
                           ┃       ┃       ┃       ┃
  SUTI-Basic ━━━━┓         ┃       ┃       ┃       ┃
    Orders only  ┃         ┃       ┃       ┃       ┃
                 ┃         ┃       ┃       ┃       ┃
  ━━━━━━━━━━━━━━━┻━━━━━━━━━┻━━━━━━━┻━━━━━━━┻━━━━━━━┛
       ~30%         ~50%      ~15%     ~4%     ~1%
     of impls     of impls
```

---

## Profile Details

| Profile | Use Case | Key Messages |
|---------|----------|--------------|
| **Basic** | Simple taxi apps | 2000, 2001, 7xxx |
| **Standard** | Standard DRT | + 3xxx, 4010, 6001 |
| **Advanced** | Full Client control | + 6500-6511, node-by-node |
| **Session** | Dynamic routing | + 2100-2105, 2040 |
| **Full** | Complete standard | + 2800, 2900, 8xxx |

---

## Proposed File Structure

```
SUTI-Schema/
│
├── core/
│   ├── SUTI-Core.xsd           # Shared types
│   ├── SUTI-Enumerations.xsd   # All enums
│   └── SUTI-CommonTypes.xsd    # Reusable types
│
├── flows/
│   ├── SUTI-Order.xsd          # 2000-2099
│   ├── SUTI-Session.xsd        # 2100-2199
│   ├── SUTI-Dispatch.xsd       # 3000-3099
│   ├── SUTI-TrafficControl.xsd # 4000-4099
│   ├── SUTI-DeliveryNote.xsd   # 6500-6599
│   ├── SUTI-Technical.xsd      # 7000-7199
│   ├── SUTI-Accounting.xsd     # 8000-8199
│   └── ...
│
├── profiles/
│   ├── SUTI-Basic.xsd          # Core + Order
│   ├── SUTI-Standard.xsd       # + Dispatch + Traffic
│   ├── SUTI-Advanced.xsd       # + Delivery
│   ├── SUTI-Session.xsd        # + Session types
│   └── SUTI-Full.xsd           # Everything
│
└── SUTI-Complete.xsd           # v1.x compatibility
```

---

# 4. JSON SCHEMA PATH FORWARD

## Key Constraints

```
  ┌─────────────────────────────────────────────────────┐
  │  1. XSD must remain BACKWARD COMPATIBLE             │
  │  2. JSON Schema shall be GENERATED FROM XSD         │
  │  3. XSD is the SINGLE SOURCE OF TRUTH               │
  └─────────────────────────────────────────────────────┘
```

**Implication:** JSON element names will match XSD names (not JSON-idiomatic)

---

## 2021 JSON Work: Historical Context

In 2021, a different approach was taken:

> "vi har lämnat iden att utgå ifrån xml schemat"
> (We abandoned the idea of deriving from the XML schema)

**2021 created hand-crafted JSON with:**
- JSON-idiomatic naming (plurals, array suffixes)
- Simplified structures
- 11 example messages

**2026 approach differs:**
- JSON Schema generated FROM XSD
- Names match XSD exactly
- 2021 examples useful as TEST CASES, not templates

---

## Why Profiles Help JSON Generation

```
  CURRENT (Monolithic)          PROPOSED (Modular)

  ┌─────────────────┐           ┌─────────────────┐
  │                 │           │   SUTI-Core     │
  │   SINGLE XSD    │    →      ├─────────────────┤
  │   3,131 lines   │           │   SUTI-Order    │
  │                 │           ├─────────────────┤
  │   Hard to       │           │   SUTI-...      │
  │   generate      │           └─────────────────┘
  │   clean JSON    │                    ↓
  └─────────────────┘           ┌─────────────────┐
                                │  JSON Schema    │
                                │  (generated)    │
                                └─────────────────┘
```

## Benefits of Modular XSD for JSON Generation

1. **Named types in XSD** → Reusable `$defs` in JSON Schema
2. **Smaller XSD modules** → Cleaner generated schemas
3. **Profile-based XSD** → Profile-based JSON Schema
4. **v1.x backward compatible** → Safe evolution path

---

## JSON Generation Strategy (XSD-First)

```
  Phase 1: Tooling & Pilot
  ────────────────────────
  Current XSD → XSD-to-JSON tool → Generated JSON Schema
                                          ↓
                              Validate against 2021 examples


  Phase 2: XSD Improvements (v1.x, backward compatible)
  ─────────────────────────────────────────────────────
  Extract inline types → Named types → Better $defs


  Phase 3: Generate Per Profile
  ─────────────────────────────
  SUTI-Core.xsd    →  suti-core.schema.json
  SUTI-Order.xsd   →  suti-order.schema.json
  SUTI-Basic.xsd   →  suti-basic.schema.json (bundle)
```

---

## Enumeration Strategy for JSON

```xml
<!-- CURRENT (XSD) - Dual representation -->
<xs:enumeration value="3101"/>
<xs:enumeration value="client"/>
```

```json
// PROPOSED (JSON Schema) - Text only
{
  "dispatchResponsible": {
    "type": "string",
    "enum": ["client", "provider", "both"]
  }
}
```

**Migration:** Keep numeric codes in external mapping table

---

# 5. RECOMMENDED ROADMAP

```
  2026                          2027
  ─────────────────────────────────────────────────

  Q1-Q2: v1.x IMPROVEMENTS (Non-Breaking)
  ├── Fix critical issues (minOccurs, typos)
  ├── Extract inline types
  ├── Complete documentation
  └── Add deprecation warnings

  Q3-Q4: v2.0 PLANNING
  ├── Define profile conformance tests
  ├── Design modular structure
  ├── Community feedback
  └── Start JSON Schema pilot (Core types)

  2027 Q1-Q2: v2.0 RELEASE
  ├── Modular XSD structure
  ├── Profile XSD files
  ├── JSON Schema for Basic/Standard
  └── Migration tools

  2027 Q3+: v2.x EVOLUTION
  ├── Complete JSON Schema coverage
  ├── OpenAPI/AsyncAPI specs
  └── Tooling and validation
```

---

# 6. DISCUSSION POINTS

## Questions for TC

1. **Profile approach:** Does formalizing implicit profiles make sense?

2. **Profile names:** Basic/Standard/Advanced/Session/Full - are these clear?

3. **JSON priority:** Which flows should get JSON Schema first?
   - Recommendation: Start with bulkLocation (already JSON) + Basic orders

4. **Enumeration strategy:** Text-only in JSON, keep numeric mapping external?

5. **Timeline:** Is the proposed roadmap realistic?

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Fragmentation between profiles | Clear upgrade path, profile compatibility matrix |
| Import complexity in XSD | Provide bundled single-file option (SUTI-Complete.xsd) |
| JSON/XSD drift | Single source of truth, generate JSON from XSD |
| Legacy system support | 12-month parallel support period |

---

## Benefits Summary

| Stakeholder | Benefit |
|-------------|---------|
| **New Implementers** | Start with SUTI-Basic, clear learning path |
| **Existing Links** | No breaking changes until v2.0, migration tools |
| **RFP Writers** | Reference specific profiles, clear conformance |
| **TC** | Easier maintenance, parallel development |
| **Tool Vendors** | Smaller schemas, better tooling support |

---

# APPENDIX: Flow Inventory

## All Documented Flows

| Block | Flow | Messages | Profile |
|-------|------|----------|---------|
| 1xxx | Resource Exchange | 1000-1112 | Full |
| 2xxx | Order (Basic) | 2000-2099 | Basic+ |
| 2xxx | DriverSession | 2100-2199 | Session |
| 2xxx | Repetitive Orders | 2800-2810 | Full |
| 2xxx | Authorization | 2900-2902 | Full |
| 3xxx | Dispatch | 3000-3099 | Standard+ |
| 4xxx | Traffic Control | 4000-4099 | Standard+ |
| 5xxx | Communication | 5000-5099 | Standard+ |
| 6xxx | Reports | 6000-6499 | Standard+ |
| 6xxx | Delivery Notes | 6500-6599 | Advanced+ |
| 7xxx | Technical | 7000-7199 | Basic+ |
| 8xxx | Accounting | 8000-8199 | Full |

---

# APPENDIX: Profile Dependency Matrix

```
                    Core  Order  Session  Dispatch  Traffic  Report  Delivery  Tech  Accounting  Resource
SUTI-Basic           ✓     ✓                                                    ✓
SUTI-Standard        ✓     ✓               ✓         ✓        ✓                 ✓
SUTI-Advanced        ✓     ✓               ✓         ✓        ✓        ✓        ✓
SUTI-Session         ✓     ✓       ✓       ✓         ✓        ✓                 ✓
SUTI-Full            ✓     ✓       ✓       ✓         ✓        ✓        ✓        ✓      ✓           ✓
```

---

# APPENDIX: Related Documents

Available in repository `.claude/plans/`:

- `xsd-analysis-executive-summary.md` - Full analysis
- `profile-based-standard-analysis.md` - Profile details
- `how-to-use-suti.md` - Extracted PDF documentation

---

# Thank You

## Next Steps

1. TC feedback on profile approach
2. Prioritize JSON Schema starting point
3. Draft profile conformance criteria
4. Plan community consultation

**Questions?**
