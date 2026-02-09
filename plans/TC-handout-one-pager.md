# SUTI Schema Modernization - One Page Summary

## The Opportunity

Analysis of "How to use SUTI" (170 pages) reveals that **Self Declarations already function as implicit profiles**. We recommend formalizing this into explicit XSD profiles to enable cleaner JSON Schema generation.

---

## Proposed: Five Profile Levels

| Profile | Target | What's Included |
|---------|--------|-----------------|
| **SUTI-Basic** | Simple taxi apps | Orders (2000/2001), Technical (7xxx) |
| **SUTI-Standard** | Standard DRT | + Dispatch (3xxx), Traffic Control (4xxx), Reports |
| **SUTI-Advanced** | Full Client control | + Node-by-node, Delivery Notes (6500-6511) |
| **SUTI-Session** | Dynamic routing | + DriverSession (2100-2199), Order combinations |
| **SUTI-Full** | Complete standard | + Repetitive Orders, Flagstops, Accounting |

**~80% of implementations can use SUTI-Basic or SUTI-Standard**

---

## Why This Helps JSON Generation

| Current State | Proposed State |
|---------------|----------------|
| Single 3,131-line XSD | Modular XSD files by flow |
| All-or-nothing | Profile-based subsets |
| Hard to map to JSON | Clean JSON Schema per module |
| No conformance levels | Clear profile conformance |

---

## Recommended Roadmap

| Phase | Timeline | Deliverables |
|-------|----------|--------------|
| **v1.x Improvements** | Q1-Q2 2026 | Fix issues, extract types, deprecation warnings |
| **v2.0 Planning** | Q3-Q4 2026 | Profile specs, JSON Schema pilot (Core types) |
| **v2.0 Release** | Q1-Q2 2027 | Modular XSD, Profile files, JSON Schema Basic/Standard |
| **v2.x Evolution** | Q3+ 2027 | Full JSON coverage, OpenAPI specs |

---

## Key Benefits

- **New implementers:** Start small with SUTI-Basic
- **RFPs:** Reference specific profile conformance
- **JSON transition:** Generate schema per module, not monolithic
- **Backward compatible:** SUTI-Complete.xsd maintains v1.x compatibility

---

## Questions for TC

1. Does formalizing implicit profiles into explicit XSD profiles make sense?
2. Which flows should get JSON Schema first? (Recommendation: bulkLocation + Basic orders)
3. Is the proposed timeline realistic?

---

*Full analysis: `.claude/plans/xsd-analysis-executive-summary.md`*
*Presentation: `.claude/plans/TC-presentation-json-generation.md`*
