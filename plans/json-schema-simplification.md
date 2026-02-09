# JSON Schema Förenkling - Revisionsbeskrivning

**Datum:** 2026-02-09
**Status:** Förslag för TK-beslut

---

## Sammanfattning

Vi föreslår en förenkling av JSON Schema-strukturen som tar bort redundanta wrapper-element. Befintliga implementationer (1111 bulkLocation) stöds via parallella scheman under en övergångsperiod.

---

## Bakgrund

### Problem med nuvarande design (2021)

Det nuvarande JSON Schema från 2021 använder wrapper-element som duplicerar information:

```json
{
  "SUTI_2000_order": {           ← Wrapper anger meddelandetyp
    "msg": {
      "msgType": "2000",         ← Samma information igen
      ...
    },
    "order": { ... }
  }
}
```

**Konsekvenser:**

| Problem | Beskrivning |
|---------|-------------|
| **Redundans** | Meddelandetypen anges två gånger |
| **Komplext schema** | Varje meddelandetyp kräver egen wrapper-definition |
| **Svår validering** | Schema måste konfigureras per meddelandetyp |
| **Icke-idiomatiskt** | Avviker från JSON-konventioner |

### Beslutskriterier

1. **1111 bulkLocation är i produktion** - måste stödjas under övergång
2. **Nya meddelanden bör vara enkla** - inget behov av bakåtkompatibilitet
3. **Ett schema för alla meddelanden** - enklare underhåll och validering

---

## Reviderad design

### Nytt format (förenklat)

```json
{
  "msg": {
    "msgType": "2000",
    "orgSender": { ... },
    "orgReceiver": { ... },
    "msgTimeStamp": "2026-02-09T10:30:00Z"
  },
  "order": { ... }
}
```

### Fördelar

| Aspekt | Gammalt format | Nytt format |
|--------|----------------|-------------|
| Wrapper-element | `SUTI_XXXX_name` krävs | Inget |
| Meddelandetyp | Anges 2 gånger | Anges 1 gång i `msg.msgType` |
| Schema-storlek | ~3600 rader | ~2000 rader (uppskattning) |
| Validering | Konfigureras per typ | Ett schema för alla |
| Parsing | Inspektera rot-nyckel | Läs `msg.msgType` |

### Schema-struktur

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://suti.se/schema/SUTI_Message.schema.json",

  "type": "object",
  "properties": {
    "msg": { "$ref": "#/$defs/msg" }
  },
  "required": ["msg"],

  "oneOf": [
    {
      "if": { "properties": { "msg": { "properties": { "msgType": { "const": "2000" }}}}},
      "then": {
        "properties": { "order": { "$ref": "#/$defs/order" }},
        "required": ["msg", "order"]
      }
    },
    {
      "if": { "properties": { "msg": { "properties": { "msgType": { "const": "4010" }}}}},
      "then": {
        "properties": { "event": { "$ref": "#/$defs/event" }},
        "required": ["msg", "event"]
      }
    }
    // ... övriga meddelandetyper
  ],

  "$defs": {
    "msg": { /* gemensam header */ },
    "order": { /* order-struktur */ },
    "event": { /* event-struktur */ }
  }
}
```

---

## Migreringsplan

### Översikt

```
         2021-schema                    Nytt schema
    ┌─────────────────────┐        ┌─────────────────────┐
    │  SUTI_Message_JSON  │        │  SUTI_Message       │
    │  _draft_20210915    │        │  .schema.json       │
    │                     │        │                     │
    │  • 1111 (produktion)│   →    │  • Alla nya msg     │
    │  • Legacy-format    │        │  • Förenklat format │
    └─────────────────────┘        └─────────────────────┘
           ↓                              ↓
      Deprecated                    Rekommenderad
       2027-06-30                    från 2026-Q2
```

### Fas 1: Förberedelse (Q1 2026)

**Mål:** Skapa nytt schema utan att påverka produktion

| Aktivitet | Ansvarig | Leverabel |
|-----------|----------|-----------|
| Skapa nytt förenklat schema | TK | `SUTI_Message.schema.json` |
| Dokumentera formatskillnader | TK | Migreringsguide |
| Uppdatera exempelfiler | TK | Nya exempel i båda format |
| Informera implementatörer | Sekretariat | Nyhetsbrev/mail |

**Leverabler:**
- [ ] `schemas/json/SUTI_Message.schema.json` (nytt)
- [ ] `schemas/json/SUTI_Message_legacy.schema.json` (omdöpt 2021-schema)
- [ ] `docs/json-migration-guide.md`
- [ ] Exempelfiler i `examples/JSON/` för båda format

### Fas 2: Parallell drift (Q2 2026 - Q2 2027)

**Mål:** Stödja båda formaten, uppmuntra migrering

| Format | Schema | Status |
|--------|--------|--------|
| Legacy (wrapper) | `SUTI_Message_legacy.schema.json` | Stöds, deprecated |
| Nytt (förenklat) | `SUTI_Message.schema.json` | Rekommenderad |

**För nya implementationer:**
- Använd endast nytt format
- Validera mot `SUTI_Message.schema.json`

**För befintliga implementationer (1111):**
- Fortsätt använda legacy-format
- Planera migrering före 2027-06-30
- Kontakta TK vid frågor

**Migreringsåtgärd för 1111:**

```diff
- {
-   "SUTI_1111_bulkLocationResponse": {
-     "msg": { "msgType": "1111", ... },
-     "bulkLocationList": { ... }
-   }
- }
+ {
+   "msg": { "msgType": "1111", ... },
+   "bulkLocationList": { ... }
+ }
```

Ändringen är minimal: ta bort wrapper-elementet.

### Fas 3: Avveckling av legacy (Q3 2027)

**Mål:** Ett schema, ett format

| Datum | Åtgärd |
|-------|--------|
| 2027-01-01 | Påminnelse till kvarvarande legacy-användare |
| 2027-04-01 | Sista varning |
| 2027-06-30 | Legacy-schema markeras som arkiverat |
| 2027-07-01 | Endast nytt format stöds officiellt |

**Efter avveckling:**
- `SUTI_Message_legacy.schema.json` flyttas till `schemas/archive/`
- Dokumentation uppdateras
- Legacy-exempel behålls för referens

---

## Påverkan på implementatörer

### Inga åtgärder krävs för:
- Nya implementationer (använd nytt format direkt)
- XSD-baserade implementationer (ingen påverkan)

### Åtgärder krävs för:
- Befintliga 1111-implementationer (ta bort wrapper före 2027-06-30)
- System som validerar mot 2021-schemat (byt schema-referens)

### Uppskattad arbetsinsats för migrering:

| Komponent | Insats | Beskrivning |
|-----------|--------|-------------|
| Avsändare | ~1 timme | Ta bort wrapper vid serialisering |
| Mottagare | ~1 timme | Justera parsing (om wrapper förväntas) |
| Validering | ~15 min | Ändra schema-URL |
| Test | ~2 timmar | Verifiera med nya exempelfiler |

---

## Risker och mitigering

| Risk | Sannolikhet | Konsekvens | Mitigering |
|------|-------------|------------|------------|
| Implementatörer missar deadline | Medel | Valideringsfel | Aktiv kommunikation, påminnelser |
| Oklarheter i nytt format | Låg | Felaktig implementation | Tydliga exempel, support |
| Legacy-system utan underhåll | Låg | Kan ej migrera | Förläng stöd vid behov |

---

## Beslutspunkter för TK

1. **Godkänns förenklad design?**
   - Ja / Nej / Behöver justering

2. **Godkänns migreringsplan och tidplan?**
   - Ja / Nej / Föreslå alternativ tidplan

3. **Vem ansvarar för kommunikation till implementatörer?**
   - TK / Sekretariat / Annan

---

## Relaterade dokument

- [json-schema-strategy-2026.md](json-schema-strategy-2026.md) - Övergripande strategi
- [xsd-anomalies-for-json.md](xsd-anomalies-for-json.md) - Anomalier att korrigera
- [json-legacy-analysis.md](json-legacy-analysis.md) - Analys av 2021-arbetet
- [profile-based-standard-analysis.md](profile-based-standard-analysis.md) - Profilbaserad struktur

---

**Författare:** Claude Code / TK-arbetsgrupp
**Granskning:** Väntar på TK-möte
