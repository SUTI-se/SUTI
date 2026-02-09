# SUTI JSON Schema 2021 - Kommenterad analys

**Fil:** `schemas/SUTI_Message_JSON_draft_20210915.json`
**Datum:** 2026-02-09
**Syfte:** Genomgång av schemats struktur med kommentarer och förbättringsförslag

---

## Innehållsförteckning

1. [Övergripande struktur](#1-övergripande-struktur)
2. [XSD-bastyper](#2-xsd-bastyper)
3. [Meddelandedefinitioner](#3-meddelandedefinitioner)
4. [Gemensam msg-header](#4-gemensam-msg-header)
5. [Meddelande-wrappers (msg*)](#5-meddelande-wrappers)
6. [Kärntyper](#6-kärntyper)
7. [Enumerationer](#7-enumerationer)
8. [Sammanfattning av problem](#8-sammanfattning-av-problem)

---

## 1. Övergripande struktur

```json
{
  "$schema": "http://json-schema.org/schema#",     // [1]
  "$ref": "#/definitions/SUTI_validateObject",     // [2]
  "definitions": {                                  // [3]
    "SUTI_validateObject": { ... },                // [4]
    "xs:*": { ... },                               // [5]
    "SUTI_XXXX_*": { ... },                        // [6]
    "msg*": { ... },                               // [7]
    // ... övriga typer
  }
}
```

### Kommentarer

| Rad | Element | Kommentar | Problem/Förbättring |
|-----|---------|-----------|---------------------|
| [1] | `$schema` | Refererar till generisk JSON Schema | **Problem:** Bör ange specifik draft (t.ex. `draft-07` eller `2020-12`) |
| [2] | `$ref` | Pekar på entry point | **Problem:** Hårdkodad till en meddelandetyp |
| [3] | `definitions` | Alla typer samlade | **Förbättring:** Använd `$defs` (modern standard) |
| [4] | `SUTI_validateObject` | Wrapper för validering | **Problem:** Måste ändras för varje meddelandetyp |
| [5] | `xs:*` | XSD-bastyper | **Förbättring:** Onödigt - använd JSON-typer direkt |
| [6] | `SUTI_XXXX_*` | Meddelandetyper | **Problem:** Redundanta wrapper-definitioner |
| [7] | `msg*` | Meddelande-strukturer | OK - men duplicering |

### SUTI_validateObject (rad 5-16)

```json
"SUTI_validateObject": {
  "type": "object",
  "properties": {
    "SUTI_4100_actionRequest": {           // [A]
      "$ref": "#/definitions/SUTI_4100_actionRequest"
    }
  },
  "required": ["SUTI_4100_actionRequest"], // [B]
  "additionalProperties": false             // [C]
}
```

| Punkt | Kommentar | Problem |
|-------|-----------|---------|
| [A] | Hårdkodad till 4100 | **Kritiskt:** Schemat validerar endast EN meddelandetyp |
| [B] | Kräver exakt denna property | Måste ändras för varje meddelande |
| [C] | Tillåter inga andra properties | Bra för strikt validering |

**Förbättring:** Använd `oneOf` för att stödja alla meddelandetyper (se [json-schema-simplification.md](json-schema-simplification.md))

---

## 2. XSD-bastyper

```json
"xs:anySimpleType": { "type": "number" },           // [1]
"xs:anyType": {                                      // [2]
  "type": "object",
  "properties": { "$": { "type": ["string", "number", "boolean"] } },
  "patternProperties": {
    "^@\\w+$": { "type": ["string", "number", "boolean"] },  // [3]
    "^\\w+$": { }                                            // [4]
  }
},
"xs:boolean": { "type": "boolean" },
"xs:date": { "type": "string" },                     // [5]
"xs:dateTime": { "type": "string" },                 // [6]
"xs:decimal": { "type": "number" },
"xs:float": { "type": "string" },                    // [7]
"xs:int": { "type": "integer", "minimum": -2147483648, "maximum": 2147483647 },
"xs:integer": { "type": "integer" },
"xs:nonNegativeInteger": { "type": "integer", "minimum": 0 },
"xs:positiveInteger": { "type": "integer", "minimum": 1 },
"xs:string": { "type": "string" }
```

### Kommentarer

| Rad | Typ | Problem | Förbättring |
|-----|-----|---------|-------------|
| [1] | `xs:anySimpleType` | Definierad som `number` | Bör vara union av alla enkla typer |
| [2] | `xs:anyType` | Komplex XML-konstruktion | **Ta bort** - ej JSON-idiomatisk |
| [3] | `^@\\w+$` | Matchar XML-attribut (`@name`) | **Ta bort** - XML-specifikt |
| [4] | `^\\w+$` | Tom definition | **Bug:** Tillåter allt |
| [5] | `xs:date` | Bara `string` | **Förbättring:** Lägg till `format: "date"` |
| [6] | `xs:dateTime` | Bara `string` | **Förbättring:** Lägg till `format: "date-time"` |
| [7] | `xs:float` | Definierad som `string` | **Bug:** Bör vara `number` |

**Rekommendation:** Ta bort alla `xs:*`-typer och använd JSON Schema-typer direkt med format-validering.

---

## 3. Meddelandedefinitioner

### Mönster 1: Direkt referens

```json
"SUTI_2000_order": { "$ref": "#/definitions/msgOrder" },
"SUTI_2001_orderConfirmation": { "$ref": "#/definitions/msgBasic" },
"SUTI_4010_eventVehicle": { "$ref": "#/definitions/msgEvent" }
```

**Kommentar:** Rent och enkelt - pekar på gemensam struktur.

### Mönster 2: Inline-definition

```json
"SUTI_1100_bulkLocationRequest": {
  "type": "object",
  "properties": {
    "msg": { "$ref": "#/definitions/msg" },
    "bulkLocationRequest": { "$ref": "#/definitions/bulkLocationRequest" }
  },
  "required": ["msg", "bulkLocationRequest"],
  "additionalProperties": false
}
```

**Problem:** Duplicerar strukturen som redan finns i `msgBulkLocationRequest`.

### Mönster 3: Inkonsekvent struktur

```json
"SUTI_1111_bulkLocationResponse": { "$ref": "#/definitions/msgBulkLocationList" },
"SUTI_1112_bulkLocationResponse": { "$ref": "#/definitions/msgBulkLocationList" }  // [!]
```

**Problem:** 1111 och 1112 är olika meddelanden men pekar på samma definition.

### Fullständig meddelandelista

| Meddelande | Definition | Kategori | Problem |
|------------|------------|----------|---------|
| `SUTI_1000_resourceRequest` | inline | Resource | Saknar `required` |
| `SUTI_1061_ratingResponse` | inline | Resource | Saknar `required` |
| `SUTI_1100_bulkLocationRequest` | inline | Resource | OK |
| `SUTI_1111_bulkLocationResponse` | `$ref` | Resource | OK |
| `SUTI_1112_bulkLocationResponse` | `$ref` | Resource | Samma som 1111 |
| `SUTI_1500_nodeListRequest` | inline | Resource | Saknar `required` |
| `SUTI_1600_nodeListResponse` | inline | Resource | Saknar `required` |
| `SUTI_1920_resourceAllocation` | `$ref` | Resource | OK |
| `SUTI_2000_order` | `$ref` | Order | OK |
| `SUTI_2001_orderConfirmation` | `$ref` | Order | OK |
| `SUTI_2002_orderReject` | `$ref` | Order | OK |
| `SUTI_2012_cancellationAcceptWithConsequence` | `$ref` | Order | Saknar `msg` wrapper |
| `SUTI_2020_nodeCancellation` | `$ref` | Order | OK |
| `SUTI_2030_orderForward` | inline | Order | OK |
| `SUTI_2040_orderLink` | `$ref` | Order | Samma som 2100 |
| `SUTI_2060_providerOrderUpdate` | inline | Order | Saknar `required` |
| `SUTI_2100_driverSession` | `$ref` | Session | OK |
| `SUTI_2101_driverSessionAccept` | `$ref` | Session | Samma def som 2100 |
| `SUTI_2102_driverSessionReject` | `$ref` | Session | OK |
| `SUTI_2800_orderTemplate` | inline | Repetitive | OK |
| `SUTI_2810_ScheduleElementConfirmation` | inline | Repetitive | OK |
| `SUTI_2901_authorizationAccept` | `$ref` | Flagstop | OK |
| `SUTI_3003_dispatchConfirmation` | `$ref` | Dispatch | OK |
| `SUTI_4000_trafficInformationRequest` | `$ref` | Traffic | OK |
| `SUTI_4001_trafficInformationResponse` | `$ref` | Traffic | Använder `msgOrder` |
| `SUTI_4010_eventVehicle` | `$ref` | Traffic | OK |
| `SUTI_4100_actionRequest` | `$ref` | Traffic | OK |
| `SUTI_5000_messageToVehicle` | `$ref` | Comm | OK |
| `SUTI_5020_locationRequest` | `$ref` | Comm | OK |
| `SUTI_5021_locationResponse` | `$ref` | Comm | OK |
| `SUTI_6001_orderReport` | `$ref` | Report | OK |
| `SUTI_6500_deliveryNote` | `$ref` | Report | OK |
| `SUTI_7000_keepAlive` | `$ref` | Technical | OK |
| `SUTI_7001_keepAliveConfirmation` | `$ref` | Technical | OK |
| `SUTI_8000_accounting` | inline | Accounting | OK |

---

## 4. Gemensam msg-header

```json
"msg": {
  "type": "object",
  "properties": {
    "orgSender": { "$ref": "#/definitions/org" },          // [1]
    "orgReceiver": { "$ref": "#/definitions/org" },        // [2]
    "infoTimeStamp": { "$ref": "#/definitions/xs:dateTime" },  // [3]
    "msgTimeStamp": { "$ref": "#/definitions/xs:dateTime" },   // [4]
    "msgType": {                                            // [5]
      "type": "string",
      "enum": ["1000", "1001", ... "8199"]                 // 134 värden
    },
    "idMsg": { "$ref": "#/definitions/idMsg" },            // [6]
    "referencesTo": { "$ref": "#/definitions/referencesTo" }, // [7]
    "idVerson": { "$ref": "#/definitions/id" }             // [8] STAVFEL!
  },
  "required": ["orgSender", "orgReceiver", "idMsg"],       // [9]
  "additionalProperties": false
}
```

### Kommentarer

| Rad | Fält | Kommentar | Problem/Förbättring |
|-----|------|-----------|---------------------|
| [1] | `orgSender` | Avsändarorganisation | OK |
| [2] | `orgReceiver` | Mottagarorganisation | OK |
| [3] | `infoTimeStamp` | Informationstidsstämpel | **Förbättring:** Lägg till `format: "date-time"` |
| [4] | `msgTimeStamp` | Meddelandetidsstämpel | **Förbättring:** Lägg till `format: "date-time"` |
| [5] | `msgType` | Meddelandetyp som enum | **Problem:** Hårdkodat, svårt att underhålla |
| [6] | `idMsg` | Meddelande-ID | OK |
| [7] | `referencesTo` | Referenser till andra meddelanden | OK |
| [8] | `idVerson` | STAVFEL! | **Bug:** Ska vara `idVersion` |
| [9] | `required` | Saknar `msgType` | **Problem:** `msgType` bör vara obligatoriskt |

**Förbättringsförslag för msgType:**
```json
"msgType": {
  "type": "string",
  "pattern": "^[1-8][0-9]{3}$",
  "description": "4-siffrig meddelandetypskod"
}
```

---

## 5. Meddelande-wrappers

### msgBasic - Enklaste formen

```json
"msgBasic": {
  "type": "object",
  "properties": {
    "msg": { "$ref": "#/definitions/msg" }
  },
  "required": ["msg"],
  "additionalProperties": false
}
```

**Användning:** 2001 (orderConfirmation), 7000/7001 (keepAlive)

### msgOrder - Order med kropp

```json
"msgOrder": {
  "type": "object",
  "properties": {
    "msg": { "$ref": "#/definitions/msg" },
    "order": { "$ref": "#/definitions/order" }
  },
  "required": ["msg", "order"],
  "additionalProperties": false
}
```

**Användning:** 2000 (order), 4001 (trafficInformationResponse)

### msgEvent - Händelser

```json
"msgEvent": {
  "type": "object",
  "properties": {
    "msg": { "$ref": "#/definitions/msg" },
    "event": { "$ref": "#/definitions/event" }
  },
  "required": ["msg", "event"],
  "additionalProperties": false
}
```

**Användning:** 4010 (eventVehicle) - notera att detta är `pickupConfirmation` i XSD!

### msgResourceAllocation - Med stavfel

```json
"msgResourceAllocation": {
  "type": "object",
  "properties": {
    "msg": { "$ref": "#/definitions/msg" },
    "resourceAlloc ation": {                    // [!] STAVFEL - mellanslag
      "$ref": "#/definitions/resourceAllocation"
    }
  },
  "required": ["msg", "resourceAlloc ation"],  // [!] STAVFEL i required
  "additionalProperties": false
}
```

**Kritiskt problem:** Mellanslag i property-namn gör att detta inte fungerar korrekt!

---

## 6. Kärntyper

### order

```json
"order": {
  "type": "object",
  "properties": {
    "agreement": { "$ref": "#/definitions/agreement" },
    "economyOrder": { "$ref": "#/definitions/economy" },
    "idOrder": { "$ref": "#/definitions/IdOrder" },        // [1]
    "orderStatus": { "$ref": "#/definitions/orderStatus" },
    "orgProvider": { "$ref": "#/definitions/org" },
    "process": { "$ref": "#/definitions/process" },
    "resourceOrder": { "$ref": "#/definitions/resource" },
    "route": { "$ref": "#/definitions/route" }
  },
  "additionalProperties": false                             // [2]
}
```

| Punkt | Problem |
|-------|---------|
| [1] | `IdOrder` med stor I - inkonsekvent namngivning |
| [2] | Saknar `required` - allt är valfritt |

### node

```json
"node": {
  "type": "object",
  "properties": {
    "nodeSeqno": { "$ref": "#/definitions/xs:positiveInteger" },
    "nodeType": {
      "type": "string",
      "enum": [
        "1801", "action",       // [1] Dubbla värden
        "1802", "navigation",
        "1803", "pickup",
        "1804", "destination"
      ]
    },
    "subnodeType": {
      "type": "string",
      "enum": [
        "1901", "break",        // [1] Dubbla värden
        "1902", "driverassist",
        // ...
      ]
    },
    "addressNode": { "$ref": "#/definitions/address" },
    "contentList": { "$ref": "#/definitions/contentList" },
    "nodeprocess": { "$ref": "#/definitions/nodeProcess" },  // [2] Liten 'p'
    "timeListNode": { "$ref": "#/definitions/timeList" }
  },
  "required": ["nodeSeqno", "nodeType"],
  "additionalProperties": false
}
```

| Punkt | Problem |
|-------|---------|
| [1] | Enum innehåller både numeriska koder OCH textvärden |
| [2] | `nodeprocess` - inkonsekvent casing (bör vara `nodeProcess`) |

### event

```json
"event": {
  "type": "object",
  "properties": {
    "eventType": {
      "type": "string",
      "enum": [
        "1716", "acceptOrder",
        "1714", "start",
        "1715", "stop",
        "pickup", "destination", "navigation", "action",  // [1] Utan kod
        "1701", "passengerinvehicle",
        "1702", "passengerdropped",
        "1703", "noshow",
        // ...
      ]
    },
    "eventNode": { "$ref": "#/definitions/node" }
  },
  "required": ["eventType"],
  "additionalProperties": false
}
```

| Punkt | Problem |
|-------|---------|
| [1] | Vissa värden saknar numerisk kod - inkonsekvent |

### process

```json
"process": {
  "type": "object",
  "properties": {
    "allowForward": { "$ref": "#/definitions/xs:boolean" },
    "allowRouting": { "$ref": "#/definitions/xs:boolean" },
    "automaticStatus": { "$ref": "#/definitions/xs:boolean" },
    "deliveryNote": { "$ref": "#/definitions/xs:boolean" },      // [1]
    "dispatch": { "$ref": "#/definitions/xs:boolean" },
    "dispatchResponsible": {
      "type": "string",
      "enum": ["client", "provider"]                              // [2]
    },
    "manualDispatch": { "$ref": "#/definitions/xs:boolean" },
    "orderAlteration": { "$ref": "#/definitions/xs:boolean" },
    "pickupconfirmation": {                                       // [3]
      "type": "string",
      "enum": ["notrequested", "standard", "extended"]
    },
    "preeOrder": { "type": "string" },                            // [4]
    "preorderedVehicle": { "$ref": "#/definitions/xs:boolean" },
    "report": { "$ref": "#/definitions/xs:boolean" },
    "statusDistance": { "$ref": "#/definitions/xs:nonNegativeInteger" },
    "trafficControl": { "$ref": "#/definitions/xs:boolean" },
    "multiDispatch": { "type": "boolean" }                        // [5]
  },
  "required": ["allowRouting", "dispatchResponsible"],
  "additionalProperties": false
}
```

| Punkt | Problem |
|-------|---------|
| [1] | `deliveryNote` - boolean, men kan behöva mer info |
| [2] | `dispatchResponsible` - bra, text-enum |
| [3] | `pickupconfirmation` - liten 'c', inkonsekvent |
| [4] | `preeOrder` - stavfel (bör vara `preOrder`) |
| [5] | `multiDispatch` - använder `boolean` direkt, inte `xs:boolean` |

---

## 7. Enumerationer

### Problem: Dubbla värden (numeriska + text)

Genomgående i schemat finns enum-värden med både numerisk kod och textrepresentation:

```json
"nodeType": {
  "enum": ["1801", "action", "1802", "navigation", "1803", "pickup", "1804", "destination"]
}
```

**Problem:**
- Otydligt vilken som ska användas
- Valideraren accepterar båda
- Svårt att upprätthålla konsistens

**Förbättring:** Välj EN representation. Rekommendation: text-only för JSON.

### Problem: Inkonsekvent casing

| Typ | Exempel | Problem |
|-----|---------|---------|
| `paymentType` | `"prepaidsocialfee"` | Ingen separator, svårläst |
| `eventType` | `"passengerinvehicle"` | Ingen separator |
| `dispatchResponsible` | `"client"`, `"provider"` | OK - enkla ord |

**Förbättring:** Använd konsekvent format, t.ex. `camelCase` eller `kebab-case`.

---

## 8. Sammanfattning av problem

### Kritiska fel

| Problem | Plats | Åtgärd |
|---------|-------|--------|
| Mellanslag i property-namn | `resourceAlloc ation` | Fixa stavning |
| Stavfel | `idVerson`, `preeOrder`, `exhangeRate` | Korrigera |
| `xs:float` som string | XSD-bastyper | Ändra till `number` |
| Hårdkodad validateObject | Rad 5-16 | Implementera `oneOf` |

### Strukturella problem

| Problem | Beskrivning | Förbättring |
|---------|-------------|-------------|
| Wrapper-redundans | Meddelandetyp anges två gånger | Ta bort wrapper-element |
| Inkonsekvent definition | Vissa inline, vissa `$ref` | Standardisera |
| Saknade `required` | Många typer saknar obligatoriska fält | Lägg till |
| XSD-bastyper | Onödigt lager | Ta bort, använd JSON-typer |

### Designproblem

| Problem | Beskrivning | Förbättring |
|---------|-------------|-------------|
| Dubbla enum-värden | Numerisk + text | Välj text-only |
| Inkonsekvent casing | `nodeprocess` vs `nodeProcess` | Standardisera camelCase |
| Gamla `definitions` | Inte modern JSON Schema | Migrera till `$defs` |
| Saknad format-validering | Datum är bara `string` | Lägg till `format` |

### Förbättringsmöjligheter

| Förbättring | Beskrivning | Prioritet |
|-------------|-------------|-----------|
| Modern $schema | Uppgradera till draft 2020-12 | Hög |
| Ta bort xs:* | Använd native JSON-typer | Hög |
| Förenklad struktur | Ta bort wrapper-element | Hög |
| Text-only enums | Ta bort numeriska koder | Medium |
| Format-validering | date-time, uri, email | Medium |
| Beskrivningar | Lägg till `description` | Låg |

---

## Relaterade dokument

- [json-schema-simplification.md](json-schema-simplification.md) - Förenklingsförslag
- [xsd-anomalies-for-json.md](xsd-anomalies-for-json.md) - XSD-anomalier
- [json-schema-strategy-2026.md](json-schema-strategy-2026.md) - Övergripande strategi

---

**Författare:** Claude Code
**Granskning:** Väntar på TK
