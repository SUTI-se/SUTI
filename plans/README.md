# SUTI JSON Schema & XSD Modernization Plans

This directory contains planning documents for the SUTI schema modernization effort, including JSON Schema strategy and XSD refactoring proposals.

## Documents

### Strategy & Analysis

| Document | Description |
|----------|-------------|
| [json-schema-strategy-2026.md](json-schema-strategy-2026.md) | **Main strategy document** - Comprehensive analysis of JSON Schema approaches |
| [json-schema-simplification.md](json-schema-simplification.md) | **Schema simplification proposal** - Removing wrapper elements, migration plan |
| [xsd-anomalies-for-json.md](xsd-anomalies-for-json.md) | Identified anomalies and naming drift that should be corrected in JSON |
| [profile-based-standard-analysis.md](profile-based-standard-analysis.md) | Analysis of profile-based XSD structure |
| [json-legacy-analysis.md](json-legacy-analysis.md) | Analysis of 2021 JSON work and alignment with current strategy |
| [json-schema-2021-annotated-analysis.md](json-schema-2021-annotated-analysis.md) | **Detailed schema review** - Line-by-line analysis with problems and improvements |
| [json-2021-refactoring-plan.md](json-2021-refactoring-plan.md) | **Refactoring plan** - Detailed specification for 2021→2026 migration |
| [json-schema-2026-changelog.md](json-schema-2026-changelog.md) | **Changelog** - Complete list of changes between 2021 and 2026 schemas |

### Presentations & Handouts

| Document | Description |
|----------|-------------|
| [TC-presentation-json-generation-sv.md](TC-presentation-json-generation-sv.md) | Presentation for Technical Committee (Swedish) |
| [TC-handout-one-pager-sv.md](TC-handout-one-pager-sv.md) | One-page summary (Swedish) |

### Reference

| Document | Description |
|----------|-------------|
| [json-idiomatisk-forklaring.md](json-idiomatisk-forklaring.md) | Explanation of "JSON-idiomatic" concept (Swedish) |

## Key Recommendations

1. **Hybrid Strategy**: XSD remains authoritative, JSON Schema designed with JSON-idiomatic naming, explicit mapping documented
2. **Profile-Based Structure**: Five conformance levels (Basic → Standard → Advanced → Session → Full)
3. **Anomaly Corrections**: Fix historical naming issues in JSON (e.g., `pickupConfirmation` → `event`)
4. **Text-Only Enumerations**: JSON uses readable text values, not numeric codes

## Timeline

- **Q1-Q2 2026**: Establish mapping framework, Basic profile JSON Schema
- **Q3-Q4 2026**: Standard profile, tooling
- **2027**: XSD v2.0 alignment, full JSON Schema coverage

## Related Resources

- [schemas/](../schemas/) - XSD and JSON Schema files
  - [SUTI_Message.schema.json](../schemas/SUTI_Message.schema.json) - **New 2026 JSON Schema**
  - [SUTI_BulkLocation_legacy.schema.json](../schemas/SUTI_BulkLocation_legacy.schema.json) - Legacy schema for 1100/1111/1112
- [examples/JSON/](../examples/JSON/) - JSON message examples
- [docs/](../docs/) - SUTI documentation

---

*These documents are working drafts for Technical Committee review.*
