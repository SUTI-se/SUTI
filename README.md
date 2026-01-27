# SUTI
Documentation, examples and tools for the SUTI (Standardized Utilization of Transport Information) standard for exchange of Demand Responsive Transport information.

## Introduction
A good starting point for getting to know the SUTI standard can be found at [SUTI Introduction (PDF)](/docs/SUTI_introduction.pdf).

## Official releases
All official releases of the standard are found as [Tags](https://github.com/SUTI-se/SUTI/tags).

The main branch contains all reviewed changes to date, and should only be used for reference but not as basis for a maintained implementation. Ongoing projects are maintained in separate branches.

## Repository Structure

```
SUTI/
├── data/           # Enumeration data (YAML source, CSV exports)
├── docs/           # PDF documentation
├── examples/       # XML message examples
├── schemas/        # XSD schemas
└── tools/          # CSV generation scripts
```

## Data Files

The `data/` directory contains SUTI enumeration values and attributes:

| File | Description |
|------|-------------|
| `SUTI_Enumerations.yaml` | Canonical source for all enumeration values with i18n translations (en, da, fi, no, sv) |

CSV files can be generated from the YAML source using the tools in `tools/`.

### YAML Structure

The YAML file uses XPath expressions as keys to identify where each enumeration is used in the XSD schema:

```yaml
enumerations:
  "order/idOrderState/@id":
    pending:
      id: 20001
      description: Order is pending confirmation
      translations:
        en: pending
        sv: väntande
        da: afventende
        fi: odottaa
        no: venter
```

## Tools

The `tools/` directory contains scripts for generating CSV files from the canonical YAML source:

| Script | Output |
|--------|--------|
| `generate_enumeration_values_csv.py` | `data/generated_SUTI_Enumeration_Values.csv` |
| `generate_attribute_list_csv.py` | `data/generated_SUTI_Attribute_List.csv` |

See [tools/README.md](tools/README.md) for detailed usage instructions.
