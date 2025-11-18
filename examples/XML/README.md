# SUTI XML Examples  
Katalog: `examples/XML/`

## Quick Start

1. **Validera en fil via kommandorad:**
   ```bash
   cd examples/XML
   xmllint --noout --schema ../schemas/SUTI_Message.xsd 1020.xml
   ```

2. **Validera alla filer:**
   ```bash
   cd examples/XML
   for file in *.xml; do xmllint --noout --schema ../schemas/SUTI_Message.xsd "$file"; done
   ```

3. **I en IDE:** Öppna valfri XML-fil - validering sker automatiskt via den relativa schemareferensen.

## Syfte  
Denna katalog innehåller XML-exempel för olika SUTI-meddelanden. Exemplen kan valideras direkt mot den officiella schemafilen som ligger i repots katalog `schemas/`.

Alla XML-filer är konfigurerade med:
- XML-deklaration med UTF-8 encoding (stödjer svenska tecken som å, ä, ö)
- Namespace-deklarationer för SUTI-schemat
- Relativ sökväg till schemafilen för enkel validering

## Mappstruktur  
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

## Schema-referens i exemplen  
Samtliga XML-exempel refererar till schemat via en **relativ sökväg**:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<SUTI
    xmlns="http://www.suti.se/schema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.suti.se/schema ../../schemas/SUTI_Message.xsd">
```

**Viktigt om encoding:** UTF-8 används för att stödja svenska tecken (å, ä, ö) och andra internationella tecken korrekt.

### Varför en relativ sökväg?
- Fungerar direkt efter att du klonat repot  
- Ingen nätverksåtkomst krävs  
- Alla vanliga IDE:er (VS Code, IntelliJ, Eclipse, oXygen m.fl.) hittar schemat automatiskt  
- Underlättar lokal utveckling, testning och CI

---

## Hur du validerar exemplen

### Via kommandorad (CLI)

**Validera en fil:**
```bash
cd examples/XML
xmllint --noout --schema ../../schemas/SUTI_Message.xsd 1020.xml
```

**Validera alla filer:**
```bash
cd examples/XML
for file in *.xml; do 
  echo "Validerar $file..."
  xmllint --noout --schema ../../schemas/SUTI_Message.xsd "$file"
done
```

**Förväntat resultat vid lyckad validering:**
- Inga felmeddelanden visas
- Kommandot returnerar utan output (exit code 0)

**Exempel på felmeddelande:**
```
1020.xml:39: element SUTI: Schemas validity error : Element 'SUTI': ...
1020.xml fails to validate
```

### I en IDE
Öppna en XML-fil i t.ex.:

- **VS Code** (med XML- eller XML Tools-plugin)
- **IntelliJ / WebStorm / Rider**
- **Eclipse**
- **oXygen XML Editor**

IDE:n kommer automatiskt validera filen via den relativa sökvägen och visa eventuella fel direkt i editorn.

---

## Viktigt om validering

- `xsi:schemaLocation` fungerar som **hint** för verktyg i utvecklingsmiljö  
- Produktionssystem bör **inte** validera mot GitHub eller suti.se  
- I egna projekt: lägg schemat i en lokal katalog (t.ex. `/schemas`)  
- För robust drift rekommenderas XML Catalog eller likvärdig resolver

Exempel på XML Catalog-post:

```xml
<uri name="http://www.suti.se/schema"
     uri="file:///path/to/local/schemas/SUTI_Message.xsd"/>
```

---

## Versionshantering  
Schemat `SUTI_Message.xsd` representerar aktuell version av standarden i main-branchen.  
Vid nya versioner:

- Uppdateras schemafilen  
- Uppdateras XML-exemplen  
- Märks tidigare versioner upp via GitHub releases/tags

---

## Support & felsökning

### Om något exempel inte validerar

1. **Kontrollera sökväg:** Säkerställ att `../../schemas/SUTI_Message.xsd` finns relativt till XML-filen
   ```bash
   ls -la ../../schemas/SUTI_Message.xsd
   ```

2. **Kontrollera namespace:** Verifiera att `xmlns="http://www.suti.se/schema"` matchar `targetNamespace` i XSD

3. **Nätverksåtkomst:** Säkerställ att IDE:n eller valideringsverktyget inte försöker hämta schemat via nätet

4. **Encoding:** Kontrollera att filen är sparad med UTF-8 encoding

### Vanliga problem

- **"Schema not found"**: Kontrollera att du kör kommandot från rätt katalog (`examples/XML/`)
- **"Namespace mismatch"**: Verifiera att namespace-deklarationen i XML-filen matchar schemat
- **"Invalid character"**: Säkerställ att filen är sparad med UTF-8 encoding

---

