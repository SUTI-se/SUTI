# SUTI JSON Schema Strategi - Uppdaterad Analys februari 2026

**Datum:** 2026-02-09
**Syfte:** Utvärdera strategier för JSON Schema baserat på tidigare analyser och aktuella filer
**Relaterat:**
- [TC-presentation](TC-presentation-json-generation-sv.md)
- [TC-handout](TC-handout-one-pager-sv.md)
- [json-legacy-analysis.md](json-legacy-analysis.md)
- [profile-based-standard-analysis.md](profile-based-standard-analysis.md)
- [json-idiomatisk-forklaring.md](json-idiomatisk-forklaring.md)
- [xsd-anomalies-for-json.md](xsd-anomalies-for-json.md) — **Anomalier och betydelsedrift att åtgärda**

---

## Sammanfattning

Denna analys utvärderar två alternativa strategier för att möjliggöra JSON som kommunikationsformat i SUTI:

| Strategi | Källa | Fördelar | Nackdelar |
|----------|-------|----------|-----------|
| **A: XSD-genererad** | SUTI_Message.xsd → JSON Schema | En sanningskälla, automatisk synk | Mindre [JSON-idiomatisk](json-idiomatisk-forklaring.md), komplex struktur |
| **B: Nytt handgjort** | Utgå från 2021-utkastet | [JSON-idiomatisk](json-idiomatisk-forklaring.md), enklare struktur | Två sanningskällor, manuellt underhåll |

**Rekommendation:** Hybridstrategi - XSD förblir auktoritativ, men JSON Schema designas med JSON-idiomatisk namngivning och mappning dokumenteras explicit.

### Viktigt: Anomalier i XSD

JSON-övergången ger möjlighet att rätta historiska anomalier och betydelsedrift i XSD. Se [xsd-anomalies-for-json.md](xsd-anomalies-for-json.md) för komplett lista, inklusive:

- **pickupConfirmation → event** (historisk namngivning, bör heta `event` i JSON)
- **nodeCancelation** (felstavning som kan uteslutas)
- **location** (dubbelbetydelse som bör separeras)
- **Dubbla enumvärden** (endast text i JSON)

---

## Bakgrund: Tidigare analyser

### TC-presentationen (januari 2026)

Föreslog:
1. **Profilbaserad XSD-struktur** (Basic → Standard → Advanced → Session → Full)
2. **XSD som enda sanningskälla** - JSON Schema genereras från XSD
3. **JSON-namn ska matcha XSD** - inte JSON-idiomatiska

### 2021 JSON-arbete

Beslutade explicit:
> "vi har lämnat iden att utgå ifrån xml schemat, skall vara ett JSON schemat"

Skapade:
- 11 exempelmeddelanden
- JSON-idiomatisk namngivning (plural för arrayer)
- Förenklad struktur för vissa meddelanden

---

## Nuläge: Tillgängliga filer

### Schema-filer (i `schemas/`)

| Fil | Rader | Beskrivning |
|-----|-------|-------------|
| `SUTI_Message.xsd` | 3,131 | Officiell XSD (i produktion) |
| `SUTI_Message_JSON_draft_20210915.json` | 3,647 | Handgjord JSON Schema (2021) |
| `SUTI_Message_JSON_Schema_generated_from_xsd.json` | 2,529 | Genererad från XSD |

### Exempel-filer (i `examples/JSON/draft_2021/`)

- 11 meddelanden (2000, 2001, 2002, 3003, 4010, 5000, 5020, 5021, 7000, 7001, 1111)
- Validerade versioner i `validated/`
- Generaliserade ID:n (uppdaterade 2026-02-09)

---

## Jämförelse: Genererad vs Handgjord JSON Schema

### Struktur-skillnader

| Aspekt | XSD-genererad | Handgjord 2021 |
|--------|---------------|----------------|
| **JSON Schema version** | draft-04 | senaste |
| **Root-struktur** | `definitions` med typer | `SUTI_validateObject` med meddelande-refs |
| **Meddelandenamn** | Ej definierade per meddelande | `SUTI_XXXX_meddelandenamn` |
| **Enumerations** | Blandat numeriskt/text | Endast text |
| **Array-hantering** | `minItems: 0` | Explicit array-definitioner |

### ID-typ jämförelse

**XSD-genererad:**
```json
"idType": {
  "type": "object",
  "required": ["src", "id"],
  "properties": {
    "src": {"type": "string"},
    "id": {"type": "string"},
    "unique": {"type": "boolean", "default": "true"}
  }
}
```

**Handgjord 2021 (i exempel):**
```json
{
  "src": "SUTI:idLink",
  "id": "systemprov_provsite_0001",
  "unique": true
}
```

**Observation:** Strukturen är likvärdig, men den handgjorda har tydligare konventioner för `src`-värden.

### Enumeration-hantering

**XSD-genererad (timeType):**
```json
"timeType": {
  "type": "string",
  "enum": [
    "2101", "scheduledtime",
    "2102", "estimatedtime",
    "2103", "promisedtime",
    ...
  ]
}
```

**Problem:** Blandar numeriska koder och textnamn i samma enum.

**Handgjord 2021:** Endast textvärden används.

---

## Analys av alternativ

### Alternativ A: XSD-genererad JSON Schema (ren form)

**Fördelar:**
- En sanningskälla (XSD)
- Automatisk synkronisering
- Befintlig verktygskedja (xsd2json, etc.)

**Nackdelar:**
- Blandat enum-format (numeriskt + text)
- Ej JSON-idiomatisk namngivning
- Komplex genererad struktur
- Svårt att underhålla läsbar JSON Schema

**Bedömning:** Tekniskt möjlig men producerar suboptimal JSON.

### Alternativ B: Nytt handgjort JSON Schema

**Fördelar:**
- JSON-idiomatisk design
- Renare struktur
- Kan utgå från beprövade 2021-exempel
- Bättre utvecklarupplevelse

**Nackdelar:**
- Två sanningskällor att underhålla
- Risk för drift mellan XSD och JSON Schema
- Dubbelt underhållsarbete

**Bedömning:** Bättre JSON men problematiskt underhåll.

### Alternativ C: Hybridstrategi (rekommenderad)

**Koncept:**
1. **XSD förblir auktoritativ** för datamodellen
2. **JSON Schema designas manuellt** med JSON-idiomatisk stil
3. **Explicit mappningsdokumentation** mellan XSD och JSON
4. **Automatiserade tester** säkerställer konsistens
5. **Profilbaserad struktur** för båda formaten
6. **Anomalier korrigeras** i JSON (se [xsd-anomalies-for-json.md](xsd-anomalies-for-json.md))

**Fördelar:**
- Bästa av båda världar
- Kontrollerad evolution
- Tydlig dokumentation
- Testbar konsistens
- Möjlighet att rätta historiska misstag

**Nackdelar:**
- Kräver initial mappningsinsats
- Automatiserade tester behövs

---

## Rekommenderad strategi: Hybrid med mappning

### Fas 1: Etablera mappningsramverk (Q1 2026)

1. **Dokumentera XSD↔JSON mappning**
   - Element-för-element mappning
   - Namnkonventioner (XSD `formOfPayment` → JSON `payments`)
   - Enumeration-strategi (endast text i JSON)
   - **Anomali-korrektioner** (se [xsd-anomalies-for-json.md](xsd-anomalies-for-json.md))

2. **Skapa mappningstabell**
   ```
   XSD Element          → JSON Property      → Transformation
   formOfPayment        → payments           → array wrapper
   attributeContent     → attributes         → plural + simplify
   idVehicle (multiple) → vehicles           → array wrapper
   pickupConfirmation   → event              → rename (anomaly fix)
   ```

3. **Implementera valideringsverktyg**
   - Säkerställ att JSON-exempel validerar mot båda scheman (struktur)
   - Dokumentera kända skillnader

### Fas 2: Profilbaserad JSON Schema (Q2 2026)

1. **Skapa JSON Schema per profil:**
   - `suti-core.schema.json` - Delade typer (idType, orgType, time)
   - `suti-basic.schema.json` - Basic profil (2000, 2001, 7xxx)
   - `suti-standard.schema.json` - Standard profil (+ 3xxx, 4xxx)

2. **Definiera JSON-konventioner:**
   - Array-namn i plural (`nodes`, `payments`, `vehicles`)
   - Endast textenumerationer
   - Konsekvent datumformat (ISO 8601)
   - Korrigerade namn för anomalier (`event` istället för `pickupConfirmation`)

3. **Skapa komplett exempelbibliotek:**
   - Minst ett exempel per meddelandetyp
   - Validerade mot JSON Schema
   - Dokumenterade edge cases

### Fas 3: Verktyg och validering (Q3 2026)

1. **Konverteringsverktyg:**
   - XML → JSON konverterare
   - JSON → XML konverterare
   - Valideringsverktyg för båda format

2. **CI/CD-integration:**
   - Automatisk validering av exempel
   - Schema-konsistenscheck
   - Dokumentationsgenerering

### Fas 4: XSD v2.0 alignment (2027)

1. **XSD-förbättringar** som underlättar JSON:
   - Standardisera enumerationer till text
   - Extrahera inline-typer till namngivna
   - Profilbaserad XSD-struktur
   - Överväg att korrigera anomalier i XSD v2.0

2. **Synkroniserad release:**
   - XSD v2.0 + JSON Schema v2.0
   - Gemensam versionering
   - Komplett mappningsdokumentation

---

## Konkreta nästa steg

### Omedelbart (denna vecka)

1. **Validera befintliga JSON-exempel**
   - Testa mot handgjord JSON Schema
   - Dokumentera valideringsresultat

2. **Skapa mappningsprototyp**
   - Välj 3-5 centrala typer
   - Dokumentera XSD↔JSON mappning
   - Identifiera transformationer
   - Inkludera anomali-korrektioner

### Kortsiktigt (februari 2026)

3. **Profilbaserad JSON Schema för Basic**
   - `suti-core.schema.json`
   - `suti-basic.schema.json`
   - Exempelvalidering

4. **Verktygsval**
   - Utvärdera JSON Schema verktyg
   - Välj valideringsbibliotek
   - Konfigurera CI/CD

### Medelsiktigt (Q2 2026)

5. **Standard-profil JSON Schema**
6. **Konverteringsverktyg prototyp**
7. **Dokumentation för implementerare**

---

## Frågor till TK

1. **Mappningsstrategi:** Accepteras hybrid-approach där JSON Schema har JSON-idiomatisk namngivning med dokumenterad mappning till XSD?

2. **Enumeration-format:** Ska JSON endast använda textvärden (rekommenderas) eller behålla dubbel representation?

3. **Profilprioritet:** Vilka profiler ska prioriteras för JSON Schema?
   - Rekommendation: Basic → Standard → övriga

4. **Versionshantering:** Ska JSON Schema versioneras separat eller synkroniserat med XSD?
   - Rekommendation: Synkroniserad versionering

5. **Bakåtkompatibilitet:** Ska 2021-exemplen ses som normgivande för JSON-struktur?

6. **Anomali-korrektioner:** Accepteras att JSON använder korrekta namn (t.ex. `event` istället för `pickupConfirmation`) med dokumenterad mappning till XSD?

---

## Bilagor

### A: Fil-struktur förslag

```
schemas/
├── xsd/
│   └── SUTI_Message.xsd           # Produktiv XSD
├── json-schema/
│   ├── suti-core.schema.json      # Delade typer
│   ├── suti-basic.schema.json     # Basic profil
│   ├── suti-standard.schema.json  # Standard profil
│   └── suti-full.schema.json      # Komplett
└── mappings/
    └── xsd-json-mapping.yaml      # Explicit mappning

examples/
├── XML/
│   └── [befintliga]
└── JSON/
    ├── basic/                     # Basic profil exempel
    ├── standard/                  # Standard profil exempel
    └── draft_2021/                # Historiska (referens)
```

### B: Mappningsexempel

```yaml
# xsd-json-mapping.yaml (utkast)
types:
  idType:
    xsd: idType
    json: idType
    notes: "Identisk struktur"

  formOfPayment:
    xsd: formOfPayment
    json: payment
    transform: "singular naming"

  formOfPayments_array:
    xsd: formOfPayment (unbounded)
    json: payments
    transform: "plural array wrapper"

  # Anomali-korrektioner
  pickupConfirmation:
    xsd: pickupConfirmation
    json: event
    transform: "rename - semantic correction"
    notes: "Historical naming, see xsd-anomalies-for-json.md"

enumerations:
  timeType:
    strategy: "text-only"
    xsd_values: ["2101", "scheduledtime", "2102", "estimatedtime"]
    json_values: ["scheduledtime", "estimatedtime"]
    mapping:
      "2101": "scheduledtime"
      "2102": "estimatedtime"
```

### C: Relaterade dokument

| Dokument | Beskrivning |
|----------|-------------|
| [xsd-anomalies-for-json.md](xsd-anomalies-for-json.md) | Identifierade anomalier och åtgärdsförslag |
| [TC-presentation-json-generation-sv.md](TC-presentation-json-generation-sv.md) | Presentation för TK |
| [TC-handout-one-pager-sv.md](TC-handout-one-pager-sv.md) | Sammanfattning på en sida |
| [json-legacy-analysis.md](json-legacy-analysis.md) | Analys av 2021-arbetet |
| [profile-based-standard-analysis.md](profile-based-standard-analysis.md) | Profilbaserad struktur |
| [json-idiomatisk-forklaring.md](json-idiomatisk-forklaring.md) | Vad betyder JSON-idiomatisk? |

---

**Författare:** Claude Code
**Status:** Utkast för TK-granskning
**Nästa steg:** Beslut om strategi på TK-möte
