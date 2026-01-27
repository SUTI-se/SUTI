# SUTI Tools Directory

Production-ready scripts for generating SUTI CSV files from the canonical YAML source.

---

## Public Tools

These are the **official, production-ready** scripts for working with SUTI enumerations.

### CSV Generation Scripts

#### `generate_enumeration_values_csv.py`
**Purpose**: Generate `SUTI_Enumeration_Values.csv` from YAML

**Usage**:
```bash
python3 tools/generate_enumeration_values_csv.py
```

**Output**:
- File: `data/generated_SUTI_Enumeration_Values.csv`
- Format: Multi-row (5 rows per ID, one per language: en, da, fi, no, sv)
- Rows: ~656 rows (only includes rows with translations, skips `–` values)

**Features**:
- UTF-8 BOM encoding for Excel compatibility
- Semicolon delimiter
- Language mapping: 1=en, 2=da, 3=fi, 4=no, 5=sv
- Skips language rows with missing translations

---

#### `generate_attribute_list_csv.py`
**Purpose**: Generate `SUTI_Attribute_List.csv` from YAML

**Usage**:
```bash
python3 tools/generate_attribute_list_csv.py
```

**Output**:
- File: `data/generated_SUTI_Attribute_List.csv`
- Format: Single-row (1 row per ID with all language columns)
- Rows: 320 rows (all IDs from YAML)

**Features**:
- UTF-8 BOM encoding for Excel compatibility
- Semicolon delimiter
- XPath format conversion (`content/@contentType` → `content/contentType`)
- Context-based attribute prefixing (104 entries):
  - `attributesDriver` prefix (12 entries, IDs 1501-1512)
  - `attributesVehicle` prefix (39 entries, IDs 1601-1639)
  - `attributeVehicle` prefix (8 entries, IDs 1640-1647)
  - `attributeContent` prefix (30 entries, IDs 2301-2330)
  - `adressContent` prefix (15 entries, IDs 2001-2015)

---

## Data Source

Both scripts read from the canonical YAML source:
- **Input**: `data/SUTI_Enumerations.yaml` (XPath-as-key format, v2.0)
- **Structure**: XPath expressions as keys, enumeration values with i18n translations

---

## Usage Workflow

### Generate Both CSV Files
```bash
# Generate Enumeration Values CSV
python3 tools/generate_enumeration_values_csv.py

# Generate Attribute List CSV
python3 tools/generate_attribute_list_csv.py
```

### Verify Generated Files
```bash
# Check generated files
head -20 data/generated_SUTI_Enumeration_Values.csv
head -20 data/generated_SUTI_Attribute_List.csv
```

---

## Requirements

- Python 3.7+
- No external dependencies (uses only Python standard library)

---

## Data Integrity

Both generation scripts ensure:
- ✅ All 320 unique IDs preserved
- ✅ Complete descriptions and translations
- ✅ Proper encoding (UTF-8 BOM)
- ✅ Consistent formatting
- ✅ No data loss

---

**Last Updated**: 2026-01-27
**YAML Format Version**: 2.0 (XPath-as-key)
**Maintained By**: SUTI Development Team
