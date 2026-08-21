# SUTI XML Examples  
Directory: `examples/XML/`

## Quick Start

1. **Validate a file via command line:**
   ```bash
   cd examples/XML
   xmllint --noout --schema ../../schemas/SUTI_Message.xsd 1020.xml
   ```

2. **Validate all files:**
   ```bash
   cd examples/XML
   for file in *.xml; do xmllint --noout --schema ../../schemas/SUTI_Message.xsd "$file"; done
   ```

3. **In an IDE:**  
   Open any XML file – validation occurs automatically via the relative schema reference.

## Golden fixtures (XML ↔ JSON)

The files `1501_PriceRequest.xml`, `1601_PriceResponse.xml`, `2531_OrderStatus.xml`, `2901_AuthorizationAccept.xml`, `6500_DeliveryNote.xml` and `8000_AccountingBasicProvider.xml` are XML twins of the JSON examples with the same message type in `examples/JSON/2026/`. They validate against the XSD and carry the same values as the JSON files; see [docs/SUTI_JSON_Mapping.md](../../docs/SUTI_JSON_Mapping.md) §4.

## Purpose  
This directory contains XML examples for various SUTI messages.  
The examples can be validated directly against the official schema file located in the repository’s `schemas/` directory.

All XML files are configured with:

- XML declaration using UTF-8 encoding (supports Swedish characters å, ä, ö)
- Schema reference using `xsi:noNamespaceSchemaLocation` (the schema does not use a target namespace)
- Relative path to the schema file for easy validation

## Directory Structure  
```
/schemas
    SUTI_Message.xsd
/examples
    /XML
        1020.xml
        1021.xml
        1022.xml
        ...
```

## Schema Reference in the Examples  
All XML examples reference the schema using a **relative path** with `noNamespaceSchemaLocation`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<SUTI
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="../../schemas/SUTI_Message.xsd">
```

**Important notes:**

- **Encoding:** UTF-8 is used to ensure correct handling of Swedish characters (å, ä, ö) and other international characters.
- **No namespace:** The schema does not define a `targetNamespace`, so XML files use `xsi:noNamespaceSchemaLocation` instead of `xsi:schemaLocation`.
- **Element structure:** All elements are in the default (no) namespace, so no namespace prefixes are needed on elements.

### Why a relative path?
- Works immediately after cloning the repository  
- Requires no network access  
- All common IDEs (VS Code, IntelliJ, Eclipse, oXygen, etc.) automatically locate the schema  
- Simplifies local development, testing, and CI

---

## How to Validate the Examples

### Command Line (CLI)

**Validate a single file:**
```bash
cd examples/XML
xmllint --noout --schema ../../schemas/SUTI_Message.xsd 1020.xml
```

**Validate all files:**
```bash
cd examples/XML
for file in *.xml; do 
  echo "Validating $file..."
  xmllint --noout --schema ../../schemas/SUTI_Message.xsd "$file"
done
```

**Expected output when validation succeeds:**
- No error messages  
- Command exits quietly (exit code 0)

**Example error:**
```
1020.xml:39: element SUTI: Schemas validity error : Element 'SUTI': ...
1020.xml fails to validate
```

### In an IDE  
Open a file in:

- **VS Code** (with XML or XML Tools extensions)
- **IntelliJ / WebStorm / Rider**
- **Eclipse**
- **oXygen XML Editor**

The IDE will validate the file automatically using the relative schema path and highlight any issues.

---

## Important Notes on Validation

- `xsi:noNamespaceSchemaLocation` acts as a **hint** to tools and development environments  
- Production systems should **not** validate against GitHub or suti.se  
- In your own system: store the schema in a local directory (e.g., `/schemas`)  
- For robust operation, use an XML Catalog or equivalent resolver

**Note:** Since the schema does not use a target namespace, XML files use `xsi:noNamespaceSchemaLocation` rather than `xsi:schemaLocation`.

Example XML Catalog entry (if using namespace in the future):

```xml
<uri name="http://www.suti.se/schema"
     uri="file:///path/to/local/schemas/SUTI_Message.xsd"/>
```

---

## Version Management  
The schema `SUTI_Message.xsd` represents the current version of the standard on the main branch.  
When a new version is released:

- The schema file is updated  
- XML examples are updated  
- Previous versions are tagged via GitHub releases

---

## Support & Troubleshooting

### If an example fails validation:

1. **Check the path:**  
   Verify that `../../schemas/SUTI_Message.xsd` exists relative to the XML file.
   ```bash
   ls -la ../../schemas/SUTI_Message.xsd
   ```

2. **Check schema reference:**  
   Verify that `xsi:noNamespaceSchemaLocation` is used (not `xsi:schemaLocation`), since the schema does not define a target namespace.

3. **Network problems:**  
   Confirm that your IDE/validator is not attempting to fetch the schema from the internet.

4. **Encoding:**  
   Make sure the file is saved using UTF-8.

### Common issues

- **“Schema not found”**:  
  Run the command from the correct directory (`examples/XML/`).

- **"Schema not found" or "No matching global declaration"**:  
  Ensure that `xsi:noNamespaceSchemaLocation` is used (the schema does not use a target namespace).

- **“Invalid character”**:  
  File is not saved as UTF-8.

---
