# SUTI XSD Schema Analysis - Executive Summary

**Date:** 2026-01-30 (Updated)
**Purpose:** Comprehensive analysis for refactoring decision support
**Schema Version:** Current (no version attribute)
**Schema File:** `/Users/martin/Documents/GitHub/SUTI/schemas/SUTI_Message.xsd`
**New Input:** "How to use SUTI" documentation analysis (170 pages)

---

## Quick Facts

| Metric | Value |
|--------|-------|
| **Schema Size** | 3,131 lines |
| **Complex Types** | 86 |
| **Message Types** | 136 (codes 1000-8999) |
| **Message Content Options** | 28 (via choice construct) |
| **Enumeration Values** | ~502 |
| **Optional Elements** | 217 |
| **Documentation Coverage** | 89.5% of types |
| **Identified Flows** | 12 distinct flow categories |
| **Recommended Profiles** | 5 (Basic, Standard, Advanced, Session, Full) |
| **Profile Feasibility** | HIGH - Self Declarations already function as implicit profiles |

---

## Key Findings Summary

### 1. Structure & Organization

**Current State:**
- **Single monolithic file** - All 86 complex types in one 3131-line XSD
- **No modularization** - No imports, includes, or namespace separations
- **Flat namespace** - No versioning or structural namespacing
- **Mixed patterns** - Inline anonymous types mixed with named types

**Complexity Indicators:**
- `msg` type has 80 child elements (including 28-option choice)
- `referencesTo` type has 21 child elements
- Deep nesting in some structures (up to 6-7 levels)
- 50+ inline anonymous complex types

**Impact:**
- Hard to navigate and understand
- Difficult to maintain
- Challenging for partial implementations
- No clear separation between message flows

### 2. Message Flow Analysis (Updated from "How to use SUTI" Documentation)

**Complete Flow Inventory:**

| Block | Flow Category | Messages | Types | Complexity |
|-------|--------------|----------|-------|------------|
| **1xxx** | Resource Exchange | 1000-1112 | 7 | Low |
| **2xxx** | Order (Basic) | 2000-2099 | 16 | Low-Medium |
| **2xxx** | DriverSession | 2100-2199 | 4 unique + shared | High |
| **2xxx** | Repetitive Orders | 2800-2810 | 5 | Medium |
| **2xxx** | Authorization/Flagstops | 2900-2902 | 3 | Low |
| **3xxx** | Dispatch | 3000-3099 | 6 | Medium |
| **4xxx** | Traffic Control | 4000-4099 | 8 | Medium |
| **5xxx** | Communication | 5000-5099 | 4 | Low |
| **6xxx** | Reports | 6000-6499 | 6 | Medium |
| **6xxx** | Delivery Notes | 6500-6599 | 6 | Medium |
| **7xxx** | Technical | 7000-7199 | 5 | Low |
| **8xxx** | Accounting | 8000-8199 | 12 | High |

**Order Flows (from documentation Chapter 4.1):**
1. Basic Flow, Simple Trip (2000, 2001)
2. Typical Flow, Simple Trip (+ 3003, 4010, 6001)
3. Extensive Flow - Node by Node (+ 3000-3002, full events)
4. Extensive Flow with Traffic Control (+ 4000-4020)
5. Multiple Orders Combined (+ 2040)
6. Order by Order (integrated DriverSession)
7. DriverSession (2100-2105)
8. Order Trading (multi-provider)
9. PreeOrder (2060-2063)
10. Order Forwarding (2050-2051)

**Key Insight:** Flows share 47 core types. True separation requires a common infrastructure module (SUTI-Core). Profile-based approach naturally mirrors existing Self Declaration practice.

### 3. Dependency Analysis

**Most Critical Types (used by many others):**
1. `idType` - Used by 36 types (fundamental ID structure)
2. `manualDescriptionType` - Used by 9 types
3. `timesType` - Used by 8 types
4. `addressType` - Used by 7 types
5. `resourceType` - Used by 7 types

**Shared Infrastructure (used by 3+ key flows):**
- 46 types are truly shared across flows
- These represent core SUTI concepts
- Cannot be separated without duplication

**Leaf Types (16 types):**
- Pure data structures with no dependencies
- Prime candidates for extraction/reuse
- Include: `idType`, `time`, `date`, `position`, `idEkInfo`

**Good News:** ✓ No circular dependencies found

### 4. Complexity & Quality Issues

#### Critical Issues

1. **Message Choice Construct (Line 174)**
   - `minOccurs="0"` on choice - message content is optional!
   - Allows invalid messages with no content
   - Should be `minOccurs="1"` (required)

2. **Deprecated Element Still Present (Line 250)**
   - `<nodeCancelation>` (misspelling)
   - Schema explicitly asks users to migrate
   - Still present for backward compatibility
   - Should be removed in v2.0

3. **No Versioning Strategy**
   - No schema version attribute
   - Optional `idVersion` element not widely used
   - No clear evolution path

#### Structural Issues

1. **Enumeration Inconsistency**
   - Mix of numeric codes ('3101') and text ('client') for same value
   - Creates validation ambiguity
   - Example: `dispatchResponsible` allows both '3101' and 'client'
   - 502 enumeration values across schema

2. **Boolean Attribute Overuse**
   - `process` type has 10 boolean attributes
   - 2^10 = 1024 possible combinations
   - Most combinations invalid/undefined
   - Hard to understand and validate

3. **Large Type Problem**
   - `msg` type: 80 child elements
   - `referencesTo`: 21 child elements
   - Complex to implement and validate
   - Many optional elements increase complexity

4. **Inline Anonymous Types**
   - ~50+ inline complex types
   - Reduces reusability
   - Harder to reference and document
   - Increases perceived complexity

#### Quality Issues

1. **Documentation Gaps**
   - 37 types need better documentation
   - Some types have no documentation (`Validation`, line 3102)
   - Heavy reliance on external "How to use SUTI" document

2. **Naming Inconsistencies**
   - Typo: `exhangeRate` (should be `exchangeRate`)
   - Mix of naming conventions
   - Some abbreviations unclear

3. **Attribute vs Element Confusion**
   - Inconsistent use of attributes vs elements
   - Some complex data in attributes
   - No clear policy

---

## Refactoring Opportunities

### Option A: Profile-Based Modular Structure (Recommended - High Impact)

**Basis:** Analysis of "How to use SUTI" documentation reveals that Self Declarations already function as implicit profiles. Clients select specific flows and message types for their implementations.

**Proposal:** Formalize into explicit XSD profiles with modular file structure

#### Profile Levels:

| Profile | Use Case | Key Flows |
|---------|----------|-----------|
| **SUTI-Basic** | Simple taxi apps | Basic order (2000/2001), Keep alive (7000/7001) |
| **SUTI-Standard** | Standard DRT | + Dispatch (3xxx), Traffic Control (4010), Reports (6001) |
| **SUTI-Advanced** | Full Client control | + Node-by-node, Delivery Notes, Order Trading |
| **SUTI-Session** | Dynamic routing | + DriverSession (21xx), Order combinations (2040) |
| **SUTI-Full** | Complete standard | + Repetitive Orders, Flagstops, Accounting |

#### Proposed File Structure:

```
SUTI-Schema/
├── core/
│   ├── SUTI-Core.xsd              # idType, orgType, timesType, addressType
│   ├── SUTI-Enumerations.xsd      # All enumeration types
│   └── SUTI-CommonTypes.xsd       # Reusable complex types
│
├── flows/
│   ├── SUTI-Order.xsd             # Order types (2000-2099)
│   ├── SUTI-Session.xsd           # DriverSession types (2100-2199)
│   ├── SUTI-Dispatch.xsd          # Dispatch types (3000-3099)
│   ├── SUTI-TrafficControl.xsd    # Traffic control types (4000-4099)
│   ├── SUTI-Report.xsd            # Report types (6000-6499)
│   ├── SUTI-DeliveryNote.xsd      # Delivery note types (6500-6599)
│   ├── SUTI-Technical.xsd         # Technical types (7000-7199)
│   ├── SUTI-Accounting.xsd        # Accounting types (8000-8199)
│   ├── SUTI-Resource.xsd          # Resource types (1000-1199)
│   ├── SUTI-RepetitiveOrders.xsd  # Templates (2800-2810)
│   └── SUTI-Authorization.xsd     # Flagstops (2900-2902)
│
├── profiles/
│   ├── SUTI-Basic.xsd             # Core + basic order
│   ├── SUTI-Standard.xsd          # + dispatch + traffic
│   ├── SUTI-Advanced.xsd          # + delivery + advanced
│   ├── SUTI-Session.xsd           # + session types
│   └── SUTI-Full.xsd              # Complete standard
│
└── SUTI-Complete.xsd              # v1.x backward compatibility
```

**Benefits:**
- Aligns with existing Self Declaration practice
- 80% of implementations can use SUTI-Basic or Standard
- Clear conformance levels for RFPs
- Better tooling support (smaller schemas)
- Backward compatible via SUTI-Full

**Challenges:**
- Multiple files to maintain
- Import dependency management
- Version coordination across profiles

**Recommendation:** Primary strategy for v2.0

---

### Option A-Legacy: Simple Modular Separation (Alternative)

**Proposal:** Split into 6 separate XSD files (original proposal)

1. **`SUTI-Core.xsd`** (~500 lines)
   - `idType`, `orgType`, `timesType`, `addressType`
   - `referencesTo`, `agreement`, `contact` structures
   - All 16 leaf types
   - All shared infrastructure

2. **`SUTI-OrderFlow.xsd`** (~1200 lines)
   - Import SUTI-Core
   - Order-by-order specific types
   - `order`, `route`, `node`, `content`, `pickup`, etc.

3. **`SUTI-SessionFlow.xsd`** (~300 lines)
   - Import SUTI-Core
   - Driver session specific types
   - `driverSession`, `changelog`, `orders`, `sessionNode`

4. **`SUTI-Resource.xsd`** (~400 lines)
   - Import SUTI-Core
   - `resourceType`, `vehicle`, `driver`, `capacity`

5. **`SUTI-Accounting.xsd`** (~500 lines)
   - Import SUTI-Core, potentially OrderFlow
   - `economyType`, `price`, `payment`, `deliveryNote`

6. **`SUTI-Messages.xsd`** (~200 lines)
   - Import all above
   - Root `SUTI` element
   - `msg` type structure
   - Message routing

**Note:** The profile-based approach (Option A) is recommended over this simpler modular approach as it better reflects how SUTI is actually used.

**Recommendation:** Consider as fallback if profile complexity is rejected

### Option B: Internal Restructuring (Medium Impact)

**Proposal:** Keep single file, restructure internally

1. **Extract inline types** to named types
2. **Group types** by domain with comments
3. **Simplify msg choice** construct
4. **Add xs:group** definitions for related elements
5. **Fix critical issues** (minOccurs, deprecations)

**Benefits:**
- Non-breaking for existing implementations
- Immediate improvements
- Lower risk

**Challenges:**
- File still large
- Limited modularity gains
- Doesn't solve fundamental structure issues

**Recommendation:** Do this as v1.x incremental improvement

### Option C: Enumeration Standardization (Quick Win)

**Proposal:** Standardize all enumerations to text values

**Example:**
```xml
<!-- BEFORE (dual representation) -->
<xs:enumeration value="3101"/>
<xs:enumeration value="client"/>
<xs:enumeration value="3102"/>
<xs:enumeration value="provider"/>

<!-- AFTER (single representation) -->
<xs:enumeration value="client"/>
<xs:enumeration value="provider"/>
```

**Benefits:**
- Clearer validation
- Better readability
- Aligns with JSON future
- Simpler implementation

**Migration:**
- Keep numeric codes in external mapping table
- Provide conversion utilities
- Allow both during transition period

**Recommendation:** Plan for v2.0, provide migration period

### Option D: Type Extraction (Quick Win)

**Proposal:** Extract frequently-used inline types to named types

**Priority targets:**
- Anonymous types in `msg` choice elements
- Anonymous types in `orderTemplate`
- Anonymous types in `accounting`
- Any inline type used/referenceable in multiple places

**Benefits:**
- Improved reusability
- Better documentation
- Clearer type hierarchy
- Can be done incrementally

**Recommendation:** Do this in v1.x (non-breaking)

---

## Migration Path Recommendation

### Phase 1: v1.x Incremental Improvements (Non-Breaking)

**Timeline:** 2-3 months

**Changes:**
1. Fix critical validation issues
   - Make msg choice `minOccurs="1"`
   - Add schema version attribute
2. Extract inline types to named types
3. Complete documentation for all types
4. Fix typos and naming issues
5. Add deprecation warnings (not removal)
6. Improve internal organization with comments

**Impact:** Minimal - all backward compatible

### Phase 2: v2.0 Major Refactoring (Breaking Changes)

**Timeline:** 6-12 months (including migration period)

**Changes:**
1. Modular file structure (Option A)
2. Remove deprecated elements (`nodeCancelation`, unused `idVersion`)
3. Standardize enumerations (Option C)
4. Simplify boolean configuration patterns
5. Namespace versioning (`http://suti.se/schema/v2`)
6. Flatten excessive nesting where possible

**Migration Support:**
- Detailed migration guide
- Conversion tools (XSLT transformations)
- Parallel support period (6 months)
- Clear timeline communicated early

### Phase 3: JSON Schema Development (Parallel Track)

**Timeline:** Start with v2.0, complete within 12 months

**Approach:**
- Map XSD v2.0 to JSON Schema
- Use modular XSD structure as blueprint
- Define JSON property naming conventions
- Provide bidirectional conversion tools
- Support both formats in parallel

---

## Critical Decision Points

### 1. Separation vs Consolidation

**Question:** Should Order and Driver Session flows be in separate schemas?

**Finding:** Only 4 truly unique types for Driver Session, 47 shared with Order

**Recommendation:**
- Keep in same schema family but separate files
- Both import common core
- Session flow imports subset of Order flow types
- Allows independent versioning while sharing infrastructure

### 2. Enumeration Strategy

**Question:** Numeric codes, text values, or both?

**Recommendation:**
- **v2.0:** Text values only in schema
- External code mapping table for numeric equivalents
- Migration period allowing both
- Aligns with modern best practices and JSON future

### 3. Versioning Approach

**Question:** How to version schema going forward?

**Recommendation:**
- Semantic versioning (MAJOR.MINOR.PATCH)
- Namespace versioning for major versions
- Schema version attribute required
- Instance version element (replace idVersion)
- Clear compatibility policy documented

### 4. Backward Compatibility

**Question:** How long to support deprecated elements?

**Recommendation:**
- Announce deprecations in v1.x (warnings, not errors)
- Minimum 12-month notice period
- Remove in v2.0 only
- Provide automated migration tools
- Maintain v1.x for 6 months post v2.0 release

---

## Implementation Priorities

### Priority 1: Fix Critical Issues (Immediate)

1. ✅ Make message choice `minOccurs="1"`
2. ✅ Add schema version attribute
3. ✅ Document all undocumented types
4. ✅ Fix typos (`exhangeRate`)

### Priority 2: Structural Improvements (v1.x)

1. ✅ Extract inline anonymous types
2. ✅ Improve internal organization
3. ✅ Add deprecation warnings
4. ✅ Complete documentation

### Priority 3: Major Refactoring (v2.0)

1. ✅ Modular file structure
2. ✅ Remove deprecated elements
3. ✅ Standardize enumerations
4. ✅ Simplify complex types
5. ✅ Namespace versioning

### Priority 4: Future Evolution (v2.x+)

1. ✅ JSON Schema support
2. ✅ OpenAPI integration
3. ✅ GraphQL schema exploration
4. ✅ Further simplification based on v2 feedback

---

## Risk Assessment

### Low Risk Changes
- Documentation improvements ✓
- Internal reorganization ✓
- Adding new optional elements ✓
- Typo fixes in documentation ✓

### Medium Risk Changes
- Extracting inline types (test thoroughly) ⚠️
- Adding deprecation warnings (communication needed) ⚠️
- Schema version attributes (validate existing parsers) ⚠️

### High Risk Changes
- Modular file split (major change, needs migration) ⚠️⚠️
- Enumeration standardization (validation changes) ⚠️⚠️
- Removing deprecated elements (breaking) ⚠️⚠️
- Namespace changes (requires update everywhere) ⚠️⚠️

---

## Success Metrics

### Technical Metrics
- **Reduced complexity:** File size reduction, type count optimization
- **Improved reusability:** Named types vs inline types ratio
- **Better documentation:** 100% coverage with examples
- **Clearer structure:** Modular organization

### Adoption Metrics
- **Migration rate:** % of implementations migrated to v2
- **Issue reduction:** Fewer support questions and issues
- **Implementation time:** Faster time to implement SUTI
- **Error rate:** Fewer validation errors in production

### Community Metrics
- **Feedback quality:** Positive feedback from implementers
- **Contribution rate:** More community contributions
- **Tool support:** Better tooling from vendors
- **Standard adoption:** Wider adoption of SUTI standard

---

## Conclusion

The SUTI XSD schema is a comprehensive, well-documented standard that has evolved organically over time. The analysis reveals:

**Strengths:**
- ✅ Comprehensive coverage of DRT domain
- ✅ High documentation coverage (89.5%)
- ✅ No circular dependencies
- ✅ Good type reusability for core infrastructure
- ✅ Well-established message structure
- ✅ **Implicit profile system via Self Declarations already works**

**Opportunities:**
- 📊 Formalize implicit profiles into explicit XSD profiles
- 📊 Modularization for better maintainability
- 📊 Enumeration standardization for clarity
- 📊 Simplification of complex types
- 📊 Modern versioning strategy
- 📊 Preparation for JSON Schema future

**Recommended Path:**
1. **Short term (v1.x):** Non-breaking improvements and fixes
2. **Medium term (v2.0):** Profile-based modular structure (Option A)
3. **Long term (v2.x+):** JSON Schema support and continued evolution

**Primary Recommendation: Profile-Based Standard**

The analysis of "How to use SUTI" documentation (170 pages) confirms:
- Self Declarations **already define implicit profiles**
- 80% of implementations use a subset of features
- Formalizing into explicit profiles aligns with existing practice
- Five profile levels (Basic → Standard → Advanced → Session → Full) cover all use cases

The refactoring is **justified** based on:
- Improved maintainability
- Easier implementation for new users (start with SUTI-Basic)
- Better alignment with modern standards
- Clear conformance levels for RFPs
- Preparation for JSON transition
- Clearer separation of concerns

However, it should be approached **carefully** with:
- Phased implementation
- Strong backward compatibility support (SUTI-Complete.xsd)
- Clear communication
- Migration tools and documentation
- Community involvement

---

## Additional Flows Identified (from "How to use SUTI" Analysis)

The following flows were identified during documentation analysis and should be considered for separate XSD treatment:

### Previously Unidentified Flows

| Flow | Messages | Current Status | Recommendation |
|------|----------|----------------|----------------|
| **Authorization/Flagstops** | 2900, 2901, 2902 | In main schema | Separate `SUTI-Authorization.xsd` |
| **Repetitive Orders** | 2800, 2801, 2810 | In main schema | Separate `SUTI-RepetitiveOrders.xsd` |
| **Order Forwarding** | 2050, 2051 | In main schema | Include in `SUTI-Order.xsd` |
| **PreeOrder** | 2060-2063 | In main schema | Include in `SUTI-Order.xsd` |
| **Order Combination** | 2040, 2041 | In main schema | Include in `SUTI-Order.xsd` |
| **Geography Information** | 1050, 1051 | In main schema | Include in `SUTI-Resource.xsd` |
| **DeliveryNote** | 6500-6511 | In main schema | Separate `SUTI-DeliveryNote.xsd` |

### Flow Dependency Matrix

```
                        Core  Order  Session  Dispatch  Traffic  Report  Delivery  Tech  Accounting  Resource
SUTI-Basic               ✓     ✓                                                    ✓
SUTI-Standard            ✓     ✓               ✓         ✓        ✓                 ✓
SUTI-Advanced            ✓     ✓               ✓         ✓        ✓        ✓        ✓
SUTI-Session             ✓     ✓       ✓       ✓         ✓        ✓                 ✓
SUTI-Full                ✓     ✓       ✓       ✓         ✓        ✓        ✓        ✓      ✓           ✓
```

---

## Profile-Based Standard Assessment

### Feasibility: HIGH

Based on "How to use SUTI" analysis, a profile-based standard is **already implicitly implemented** through Self Declarations:

> "SUTI provides the possibility for several different ways of configuring a connection between Client and Provider. A simple taxi-app requires much less functionality than a complicated dynamic combination of trips."

### Key Evidence:

1. **Self Declarations define flow subsets** - Clients document which message types they support
2. **RFPs reference specific flows** - Not all implementations use all features
3. **Provider systems adapt** - Providers implement Client-defined subsets
4. **Documentation acknowledges levels** - "Basic flow" vs "Extensive flow" terminology

### Recommendation:

Formalize the implicit profile system into explicit XSD profiles. This aligns with existing practice and makes compliance clearer.

See: `profile-based-standard-analysis.md` for detailed analysis.

---

## Related Documents

- **Detailed Analysis:** `xsd-analysis-findings.md`
- **Additional Findings:** `xsd-additional-findings.md`
- **Dependency Analysis:** `xsd-dependency-analysis.md`
- **Profile Analysis:** `profile-based-standard-analysis.md` (NEW)
- **Extracted PDF:** `how-to-use-suti.md`
- **Analysis Scripts:** `.claude/scripts/analyze_*.py`

---

**Prepared for:** SUTI Technical Committee
**Author:** Claude Code Analysis
**Date:** 2026-01-30
**Status:** Draft for Review
