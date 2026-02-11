# TC Slutrapport: JSON Schema för SUTI 2026

**Datum:** 2026-02-11
**Status:** Klar för granskning
**Författare:** Claude Code med teknisk expertis

---

## Sammanfattning

Detta dokument presenterar resultatet av arbetet med att skapa ett komplett JSON Schema för SUTI-standarden. Arbetet har genomförts under perioden 30 januari - 11 februari 2026 och resulterat i:

| Leverabel | Antal | Status |
|-----------|-------|--------|
| JSON Schema (SUTI_Message.schema.json) | 1 | ✅ Komplett |
| JSON-exempel (draft_2026/) | 36 | ✅ Validerade |
| Mappningsdokumentation (xsd-json-mapping.yaml) | 1 | ✅ Komplett |
| Meddelandetyper (msgTypes) | 51 | ✅ Alla dokumenterade |

---

## 1. Utvecklingsprocess och tidslinje

### Fas 1: Analys och strategi (30 jan - 9 feb)

| Datum | Aktivitet | Dokument |
|-------|-----------|----------|
| 30 jan | XSD-analys påbörjad | `xsd-analysis-findings.md`, `xsd-additional-findings.md` |
| 30 jan | Beroende-analys | `xsd-dependency-analysis.md` |
| 30 jan | Sammanfattning för TK | `xsd-analysis-executive-summary.md`, `TC-handout-one-pager.md` |
| 30 jan | TC-presentation skapad | `TC-presentation-json-generation.md` |
| 9 feb | Strategi 2026 formulerad | `json-schema-strategy-2026.md` |
| 9 feb | Svenska versioner | `TC-handout-one-pager-sv.md`, `TC-presentation-json-generation-sv.md` |
| 9 feb | Legacy-analys | `json-legacy-analysis.md` |
| 9 feb | Anomalianalys | `xsd-anomalies-for-json.md` |

### Fas 2: Schemautveckling (9-10 feb)

| Datum | Aktivitet | Dokument |
|-------|-----------|----------|
| 9 feb | 2021-schemaanalys | `json-schema-2021-annotated-analysis.md` |
| 9 feb | Refaktoreringsplan | `json-2021-refactoring-plan.md` |
| 10 feb | Förenklingsförslag | `json-property-simplification-proposal.md` |
| 10 feb | Kompletteringsplan | `json-schema-completeness-plan.md` |
| 10 feb | Ändringslogg 2026 | `json-schema-2026-changelog.md` |

### Fas 3: Implementering och validering (10-11 feb)

| Datum | Aktivitet | Resultat |
|-------|-----------|----------|
| 10 feb | Schema uppdaterat | 51 msgTypes, 65+ $defs |
| 10 feb | Mappning dokumenterad | `xsd-json-mapping.yaml` (740 rader) |
| 11 feb | Saknade msgTypes tillagda | 16 nya (1020-1023, 2010-2011, 4011-4012, etc.) |
| 11 feb | JSON-exempel skapade | 36 filer, alla validerade |
| 11 feb | Granskning (Bengt/Platon) | Rekommendationer implementerade |

---

## 2. Hybridstrategi för XSD↔JSON

### Beslutad strategi

**XSD förblir auktoritativ** för datamodellen, men JSON Schema designas med **JSON-idiomatisk namngivning**.

```
XSD (SUTI_Message.xsd)
        ↓
    [Mappning]  ← xsd-json-mapping.yaml dokumenterar transformationer
        ↓
JSON Schema (SUTI_Message.schema.json)
```

### Nyckelprinciper

1. **Strukturell förenkling**: Inga wrapper-element (SUTI_XXXX_*)
2. **Pluralisering av arrayer**: `nodeList` → `nodes`, `formOfPayment` → `payments`
3. **Endast text-enumerationer**: Numeriska koder (2101, 1701) ersatta med text
4. **Anomalikorrektioner**: `pickupConfirmation` → `event`, stavfel rättade
5. **JSON Schema draft-2020-12**: Modern standard med `$defs`, `allOf`, `if/then`

---

## 3. Exempel: XML vs JSON

### KeepAlive (7000) - Enkel header-meddelande

**XML (14 rader):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<SUTI>
  <orgSender name="Client name">
    <idOrg src="SUTI:idLink" id="systemsupplierId_clientOwnerId_uniqueId" unique="true"/>
  </orgSender>
  <orgReceiver name="Provider name">
    <idOrg src="SUTI:idLink" id="systemsupplierId_providerOwnerId_uniqueId" unique="true"/>
  </orgReceiver>
  <msg msgType="7000" msgName="Keep alive">
    <idMsg src="systemsupplierId_clientOwnerId_uniqueId:idMsg" id="2015121414795234" unique="true"/>
  </msg>
</SUTI>
```

**JSON (36 rader):**
```json
{
  "msg": {
    "msgType": "7000",
    "msgTimeStamp": "2019-12-18T10:39:00.000Z",
    "orgSender": {
      "name": "ThisProvider",
      "idOrg": { "src": "SUTI:idLink", "id": "systemprov_provsite_0001", "unique": true }
    },
    "orgReceiver": {
      "name": "ThisClient",
      "idOrg": { "src": "SUTI:idLink", "id": "systemclient_clientsite_0009", "unique": true }
    },
    "idMsg": { "src": "systemprov_provsite_0001:MSGID", "id": "2019121812345678", "unique": true }
  }
}
```

**Skillnader:**
- Ingen `<SUTI>` rot-wrapper
- `msgTimeStamp` tilllagt (ISO 8601 med Z-suffix)
- `orgSender`/`orgReceiver` flyttade in i `msg`-objektet
- Strukturen plattare och mer direkt

---

## 4. Mappningsdokumentation (xsd-json-mapping.yaml)

### Översikt

| Sektion | Innehåll |
|---------|----------|
| `structure` | Root-element och schema-struktur transformation |
| `arrays` | 17 array-egenskaper (XSD → JSON plural) |
| `property_simplifications` | 21 förenklingar (kontext-baserad) |
| `enumerations` | 6 enum-typer med text-mappning |
| `anomaly_corrections` | 8 korrigeringar (semantiska + stavfel) |
| `type_mappings` | 12 XSD→JSON typkonverteringar |
| `message_types` | **Alla 51 msgTypes** med body-typ |

### Exempelutdrag: Meddelandetyper

```yaml
message_types:
  "2000":
    name: "order"
    body: "order"

  "7000":
    name: "keepAlive"
    body: null
    notes: "Header only message"

  "4010":
    name: "eventVehicle"
    body: "event"
```

---

## 5. JSON Schema-statistik

### Struktur

| Komponent | Antal |
|-----------|-------|
| $defs (typdefinitioner) | 66 |
| msgTypes i schema | 51 |
| Villkorliga regler (if/then) | 51 |
| Exempel-filer | 36 |

### Täckning per meddelandekategori

| Kategori | msgTypes | Antal |
|----------|----------|-------|
| Resurs (1xxx) | 1000, 1020-1023, 1061, 1100, 1111-1112, 1500, 1600, 1920 | 12 |
| Order (2xxx) | 2000-2002, 2010-2012, 2020, 2030, 2040, 2060, 2100-2102, 2800, 2810, 2901 | 17 |
| Dispatch (3xxx) | 3003 | 1 |
| Händelser (4xxx) | 4000-4001, 4010-4012, 4020, 4031, 4100 | 8 |
| Meddelanden (5xxx) | 5000, 5010-5011, 5020-5021 | 5 |
| Rapporter (6xxx) | 6001, 6500 | 2 |
| System (7xxx) | 7000-7001, 7030-7031, 7100-7101 | 6 |
| Ekonomi (8xxx) | 8000 | 1 |

---

## 6. Granskningsresultat (Bengt & Platon)

### Implementerade rekommendationer

| Rekommendation | Status |
|---------------|--------|
| Centraliserad msgType-enum | ✅ Implementerad |
| Koordinatgränser (WGS-84) | ✅ lat: -90/+90, lon: -180/+180 |
| referenceToMsg med anyOf-krav | ✅ Minst ett ID krävs |
| additionalProperties: false | ✅ Strikt validering |
| Timestamp-standardisering | ✅ ISO 8601 med Z-suffix |

### Kvalitetsförbättringar

1. **Semantiska constraints**: Koordinatvalidering förhindrar ogiltiga positioner
2. **Typkonsistens**: Alla enumerationer använder endast textvärden
3. **Dokumentation**: Varje msgType har name, body, och notes

---

## 7. Föreslagna nästa steg

### Kortsiktigt (Q1 2026)

1. **TK-godkännande** av JSON Schema och mappningsdokumentation
2. **Pilot-implementation** hos minst två leverantörer
3. **Konverteringsverktyg** för XML↔JSON

### Medelsiktigt (Q2-Q3 2026)

4. **Profilbaserade scheman** (Basic, Standard, Full)
5. **CI/CD-integration** för automatisk validering
6. **Utökade exempel** för alla edge cases

### Långsiktigt (2027)

7. **XSD v2.0** med synkroniserade förbättringar
8. **JSON-first** för nya meddelandetyper

---

## 8. Bilagor

### Relaterade dokument

| Dokument | Beskrivning |
|----------|-------------|
| [TC-JSON-Schema-Teknisk-Detalj.md](TC-JSON-Schema-Teknisk-Detalj.md) | Tekniska detaljer med fler exempel |
| [TC-JSON-Schema-Fullständighetsanalys.md](TC-JSON-Schema-Fullständighetsanalys.md) | Djupanalys baserad på HowToUseSUTI.txt |
| [xsd-json-mapping.yaml](xsd-json-mapping.yaml) | Komplett mappningsdokumentation |
| [json-schema-completeness-plan.md](json-schema-completeness-plan.md) | Arbetsplan med faser |

### Filstruktur

```
SUTI/
├── schemas/
│   └── SUTI_Message.schema.json     # Huvudschema (51 msgTypes)
├── examples/
│   ├── XML/                          # 37 XML-exempel
│   └── JSON/draft_2026/              # 36 JSON-exempel
└── plans/
    ├── xsd-json-mapping.yaml         # Mappningsdokumentation
    └── *.md                          # Analyser och planer
```

---

**Version:** 1.0
**Senast uppdaterad:** 2026-02-11
**Granskat av:** Bengt (kvalitetsgranskare), Platon (extern AI-perspektiv)
