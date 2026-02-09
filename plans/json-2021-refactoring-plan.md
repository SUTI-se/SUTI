# JSON Schema 2021→2026 Refaktoreringsplan

**Datum:** 2026-02-09
**Version:** 1.3 (uppdaterad med XSD-JSON mappningsdokumentation)
**Status:** ✅ Implementation och validering genomförd

---

## 1. Beslutade vägval

| Beslut | Val | Motivering |
|--------|-----|------------|
| JSON Schema-version | **draft-2020-12** | Modern standard, bättre verktyg |
| Enumerationer | **Text-only** | Renare JSON, lättläst |
| XSD-bastyper | **Ta bort helt** | Onödig komplexitet |
| Omfattning | **Alla meddelandetyper** | Komplett ersättning |

---

## 2. Översikt av förändringar

### 2.1 Strukturella förändringar

```
2021-version                          2026-version
─────────────────────────────────────────────────────────────
{                                     {
  "SUTI_2000_order": {       →          "msg": {
    "msg": { ... },                       "msgType": "2000",
    "order": { ... }                      ...
  }                                     },
}                                       "order": { ... }
                                      }
```

**Förändring:** Wrapper-element (`SUTI_XXXX_*`) tas bort. Meddelandetypen identifieras via `msg.msgType`.

### 2.2 Valideringsmodell

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://suti.se/schema/SUTI_Message.schema.json",
  "type": "object",
  "properties": { "msg": { "$ref": "#/$defs/msg" } },
  "required": ["msg"],

  "allOf": [
    {
      "if": { "properties": { "msg": { "properties": { "msgType": { "const": "2000" } } } } },
      "then": { "properties": { "order": { "$ref": "#/$defs/order" } }, "required": ["msg", "order"] }
    },
    { /* ... fler if/then för varje meddelandetyp */ }
  ]
}
```

**Förändring:** `allOf` med `if/then`-villkor baserat på `msg.msgType` ersätter hårdkodad `SUTI_validateObject`. Denna struktur ger bättre felmeddelanden än `oneOf`.

---

## 3. Detaljerad ändringsspecifikation

### 3.1 Schema-metadata

| Element | 2021 | 2026 | Åtgärd |
|---------|------|------|--------|
| `$schema` | `http://json-schema.org/schema#` | `https://json-schema.org/draft/2020-12/schema` | ✅ Uppdaterad |
| `$id` | *(saknas)* | `https://suti.se/schema/SUTI_Message.schema.json` | ✅ Tillagd |
| `title` | *(saknas)* | `SUTI Message Schema` | ✅ Tillagd |
| `description` | *(saknas)* | Beskrivande text | ✅ Tillagd |
| Entry point | `$ref` → `SUTI_validateObject` | Root-objekt med `allOf` | ✅ Ändrad |
| `definitions` | Används | Ersatt med `$defs` | ✅ Migrerad |

### 3.2 XSD-bastyper (ta bort)

| 2021-typ | Ersätts med | Kommentar |
|----------|-------------|-----------|
| `xs:string` | `"type": "string"` | Direkt JSON-typ |
| `xs:integer` | `"type": "integer"` | Direkt JSON-typ |
| `xs:int` | `"type": "integer"` | Ta bort min/max constraints |
| `xs:positiveInteger` | `"type": "integer", "minimum": 1` | Inline constraint |
| `xs:nonNegativeInteger` | `"type": "integer", "minimum": 0` | Inline constraint |
| `xs:decimal` / `xs:float` | `"type": "number"` | Fixa xs:float-bug |
| `xs:boolean` | `"type": "boolean"` | Direkt JSON-typ |
| `xs:date` | `"type": "string", "format": "date"` | Lägg till format |
| `xs:dateTime` | `"type": "string", "format": "date-time"` | Lägg till format |
| `xs:anyType` | *(ta bort)* | XML-specifik, ej relevant |
| `xs:anySimpleType` | *(ta bort)* | XML-specifik, ej relevant |

### 3.3 Stavfel att korrigera

| 2021 (fel) | 2026 (rätt) | Typ |
|------------|-------------|-----|
| `idVerson` | `idVersion` | msg-header |
| `preeOrder` | `preOrder` | process |
| `exhangeRate` | `exchangeRate` | economy |
| `resourceAlloc ation` | `resourceAllocation` | msgResourceAllocation |
| `nodeprocess` | `nodeProcess` | node |
| `msgSeqno` | `msgSeqNo` | bulkLocationList |
| `sendinformationDisptch` | `sendinformationDispatch` | nodeProcess |

### 3.4 Enumerationer (text-only)

#### nodeType
```json
// 2021: ["1801", "action", "1802", "navigation", "1803", "pickup", "1804", "destination"]
// 2026:
"nodeType": {
  "type": "string",
  "enum": ["action", "navigation", "pickup", "destination"]
}
```

#### eventType
```json
// 2021: ["1716", "acceptOrder", "1714", "start", ...]
// 2026:
"eventType": {
  "type": "string",
  "enum": [
    "acceptOrder", "start", "stop", "pickup", "destination",
    "navigation", "action", "passengerInVehicle", "passengerDropped",
    "noShow", "parcelInVehicle", "parcelDropped", "actionDone",
    "navigationDone", "cancelAtDoor", "vehicleAtNode", "infoToContent",
    "dispatchConfirmationSent", "delayConfirmationSent", "arrivalConfirmationSent"
  ]
}
```

**Notera:** camelCase tillämpas konsekvent (t.ex. `passengerinvehicle` → `passengerInVehicle`)

#### paymentType
```json
// 2021: ["1301", "cash", "1302", "card", ...]
// 2026:
"paymentType": {
  "type": "string",
  "enum": [
    "cash", "card", "account", "ticket", "voucher",
    "prepaidsocialfee", "app", "invoice"
  ]
}
```

#### orderStatus
```json
// 2021: ["none", "started", "completed", ...]
// 2026: (oförändrad - redan text-only)
"status": {
  "type": "string",
  "enum": ["none", "started", "completed", "noshow", "confirmed",
           "dispatching", "dispatched", "cancelled"]
}
```

### 3.5 Format-validering (nya)

| Fält | Lägg till |
|------|-----------|
| `msgTimeStamp` | `"format": "date-time"` |
| `infoTimeStamp` | `"format": "date-time"` |
| `time` (i timeList) | `"format": "date-time"` |
| `url` (i address) | `"format": "uri"` |

### 3.6 Required-fält (komplettera)

| Typ | Saknas i 2021 | Lägg till |
|-----|---------------|-----------|
| `msg` | `msgType` | `required: ["orgSender", "orgReceiver", "idMsg", "msgType"]` |
| `order` | *(inget required)* | `required: ["idOrder"]` |
| `node` | OK | - |
| `event` | OK | - |

### 3.7 Meddelandestruktur (förenklad)

Varje meddelandetyp definieras som ett `if/then`-villkor i `allOf`:

```json
{
  "if": {
    "properties": { "msg": { "properties": { "msgType": { "const": "2000" } } } },
    "required": ["msg"]
  },
  "then": {
    "properties": {
      "msg": true,
      "order": { "$ref": "#/$defs/order" }
    },
    "required": ["msg", "order"],
    "unevaluatedProperties": false
  }
}
```

**Notera:** `"msg": true` i `then` tillåter msg-propertyn utan att omdefiniera den.

---

## 4. Meddelandetyper

### 4.1 Komplett lista

| MsgType | Namn | Body-typ | Status |
|---------|------|----------|--------|
| 1000 | resourceRequest | resourceReservation | Ny struktur |
| 1061 | ratingResponse | ratings | Ny struktur |
| 1100 | bulkLocationRequest | bulkLocationRequest | **Ny + Legacy** |
| 1111 | bulkLocationResponse | bulkLocationList | **Ny + Legacy** |
| 1112 | bulkLocationResponse | bulkLocationList | **Ny + Legacy** |
| 1500 | nodeListRequest | infoRequest | Ny struktur |
| 1600 | nodeListResponse | infoResponse | Ny struktur |
| 1920 | resourceAllocation | resourceAllocation | Ny struktur |
| 2000 | order | order | Ny struktur |
| 2001 | orderConfirmation | *(endast msg)* | Ny struktur |
| 2002 | orderReject | orderReject | Ny struktur |
| 2012 | cancellationAcceptWithConsequence | cancellationConsequence | Ny struktur |
| 2020 | nodeCancellation | nodeCancellation | Ny struktur |
| 2030 | orderForward | orderForward | Ny struktur |
| 2040 | orderLink | driverSession | Ny struktur |
| 2060 | providerOrderUpdate | providerOrderUpdate | Ny struktur |
| 2100 | driverSession | driverSession | Ny struktur |
| 2101 | driverSessionAccept | driverSession | Ny struktur |
| 2102 | driverSessionReject | driverSessionReject | Ny struktur |
| 2800 | orderTemplate | orderTemplate | Ny struktur |
| 2810 | ScheduleElementConfirmation | scheduleElementOrderList | Ny struktur |
| 2901 | authorizationAccept | resource | Ny struktur |
| 3003 | dispatchConfirmation | resource | Ny struktur |
| 4000 | trafficInformationRequest | resource | Ny struktur |
| 4001 | trafficInformationResponse | order | Ny struktur |
| 4010 | eventVehicle | event | Ny struktur |
| 4100 | actionRequest | actionRequest | Ny struktur |
| 5000 | messageToVehicle | messageTo | Ny struktur |
| 5020 | locationRequest | locationRequest | Ny struktur |
| 5021 | locationResponse | geographicLocation | Ny struktur |
| 6001 | orderReport | orderReport | Ny struktur |
| 6500 | deliveryNote | deliveryNote | Ny struktur |
| 7000 | keepAlive | *(endast msg)* | Ny struktur |
| 7001 | keepAliveConfirmation | *(endast msg)* | Ny struktur |
| 8000 | accounting | accounting | Ny struktur |

### 4.2 Meddelanden med endast header

Dessa meddelanden kräver endast `msg`-header utan body:
- 2001 (orderConfirmation)
- 7000 (keepAlive)
- 7001 (keepAliveConfirmation)

---

## 5. bulkLocation: Dubbelt stöd

### 5.1 Bakgrund

Meddelandetyperna 1100, 1111 och 1112 är i produktion med 2021-formatet (wrapper-element). För att möjliggöra smidig migrering stöds dessa meddelanden i **båda formaten**:

| Format | Schema | Beskrivning |
|--------|--------|-------------|
| **Nytt format** | `SUTI_Message.schema.json` | Förenklad struktur utan wrapper |
| **Legacy format** | `SUTI_BulkLocation_legacy.schema.json` | Wrapper-element, bakåtkompatibelt |

### 5.2 Formatjämförelse

**Nytt format (rekommenderat):**
```json
{
  "msg": { "msgType": "1111", "orgSender": {...}, "orgReceiver": {...}, "idMsg": {...} },
  "bulkLocationList": { "locationList": [...] }
}
```

**Legacy format (deprecated):**
```json
{
  "SUTI_1111_bulkLocationResponse": {
    "msg": { "msgType": "1111", ... },
    "bulkLocationList": { "locationList": [...] }
  }
}
```

### 5.3 Befintliga implementationer

Befintliga implementationer som använder legacy-formatet behöver **inte ändra något omedelbart**. Legacy-schemat validerar produktionsmeddelanden utan modifiering.

### 5.4 Legacy-schema: `SUTI_BulkLocation_legacy.schema.json`

Legacy-schemat är implementerat och innehåller:
- Stöd för wrapper-element (`SUTI_1100_*`, `SUTI_1111_*`, `SUTI_1112_*`)
- Minimal uppsättning typdefinitioner (endast bulkLocation-relaterade)
- Modern JSON Schema (draft-2020-12) för bättre valideringsstöd
- Deprecation-varning i description

**Fil:** `schemas/SUTI_BulkLocation_legacy.schema.json` (~180 rader)

### 5.5 Migreringsplan för bulkLocation

| Fas | Period | Åtgärd |
|-----|--------|--------|
| **1. Parallell** | Q2 2026 | Båda format stöds, legacy deprecated |
| **2. Varning** | Q1 2027 | Aktiv varning vid legacy-användning |
| **3. Avveckling** | Q3 2027 | Legacy-schema arkiveras |

**Migreringsåtgärd:**

```diff
// FÖR 1111:
- { "SUTI_1111_bulkLocationResponse": { "msg": {...}, "bulkLocationList": {...} } }
+ { "msg": {"msgType": "1111", ...}, "bulkLocationList": {...} }
```

---

## 6. Fil-leverabler (✅ Genererade)

| Fil | Plats | Status |
|-----|-------|--------|
| `SUTI_Message.schema.json` | `schemas/` | ✅ Klar |
| `SUTI_BulkLocation_legacy.schema.json` | `schemas/` | ✅ Klar |
| `json-schema-2026-changelog.md` | `plans/` | ✅ Klar |

---

## 7. Implementationsordning (✅ Genomförd)

1. ✅ **Skapa $defs för bastyper** (id, org, address, etc.)
2. ✅ **Skapa $defs för meddelandekroppar** (order, event, etc.)
3. ✅ **Skapa msg-definition** med korrigerad struktur
4. ✅ **Skapa allOf/if/then-struktur** för alla meddelandetyper
5. ✅ **Skapa legacy-schema** för bulkLocation
6. ✅ **Validera** mot befintliga exempelfiler
7. ✅ **Dokumentera** alla ändringar

---

## 8. Risker och mitigering

| Risk | Mitigering |
|------|------------|
| Brytande förändring för produktion | Legacy-schema för bulkLocation |
| Enum-värden matchar inte | Dokumentera mappning numerisk→text |
| Verktyg stöder ej draft-2020-12 | Testa med vanliga validerare |
| Stavfel påverkar kompatibilitet | Tydlig migreringsguide |

---

## 9. Genomförandestatus

- [x] Vägval godkända (draft-2020-12, text-only, ta bort xs:*, alla meddelanden)
- [x] Plan skapad och granskad
- [x] `SUTI_Message.schema.json` implementerad (~1100 rader)
- [x] `SUTI_BulkLocation_legacy.schema.json` implementerad (~180 rader)
- [x] Ändringslogg dokumenterad (`json-schema-2026-changelog.md`)
- [x] Validering mot exempelfiler (11 exempel i `examples/JSON/draft_2026/`)
- [ ] TK-granskning

---

## 10. Genererade filer

| Fil | Plats | Storlek | Beskrivning |
|-----|-------|---------|-------------|
| `SUTI_Message.schema.json` | `schemas/` | ~1100 rader | Nytt huvudschema |
| `SUTI_BulkLocation_legacy.schema.json` | `schemas/` | ~180 rader | Legacy-stöd |
| `json-schema-2026-changelog.md` | `plans/` | ~500 rader | Komplett ändringslogg |
| `xsd-json-mapping.yaml` | `plans/` | ~450 rader | XSD↔JSON mappningstabell |

---

## 11. Validerade exempel (✅ Komplett)

Alla 2021-exempel har konverterats till 2026-format och validerats mot det nya schemat.

| Fil | MsgType | Body | Status |
|-----|---------|------|--------|
| `1111_bulkLocationResponse.json` | 1111 | bulkLocationList | ✅ Valid |
| `2000_order.json` | 2000 | order | ✅ Valid |
| `2001_orderConfirmation.json` | 2001 | *(endast msg)* | ✅ Valid |
| `2002_orderReject.json` | 2002 | orderReject | ✅ Valid |
| `3003_dispatchConfirmation.json` | 3003 | resource | ✅ Valid |
| `4010_eventVehicle.json` | 4010 | event | ✅ Valid |
| `5000_messageToVehicle.json` | 5000 | messageTo | ✅ Valid |
| `5020_locationRequest.json` | 5020 | locationRequest | ✅ Valid |
| `5021_locationResponse.json` | 5021 | geographicLocation | ✅ Valid |
| `7000_keepAlive.json` | 7000 | *(endast msg)* | ✅ Valid |
| `7001_keepAliveConfirmation.json` | 7001 | *(endast msg)* | ✅ Valid |

**Plats:** `examples/JSON/draft_2026/`

### 11.1 Konverteringsändringar

Vid konvertering från 2021 till 2026-format gjordes följande anpassningar:

1. **Wrapper-element borttagna** - `SUTI_XXXX_*` ersatt med flat struktur
2. **camelCase normaliserad** - t.ex. `nodeSeqno` → `nodeSeqNo`
3. **timeType-värden uppdaterade** - t.ex. `scheduledTime` → `ordered`, `promisedTime` → `confirmed`
4. **Strukturer förenklade** - t.ex. `manualText` som objekt → sträng

---

## 12. XSD-JSON Mappningsdokumentation

En komplett mappningstabell har skapats i `plans/xsd-json-mapping.yaml` som dokumenterar:

### 12.1 Strukturella mappningar

Dokumenterar transformationen mellan **tre** format:

| Format | Struktur |
|--------|----------|
| **XSD/XML** | `<SUTI><orgSender/><orgReceiver/><msg msgType="2000"><order/></msg></SUTI>` |
| **JSON 2021** | `{"SUTI_2000_order": {"msg": {...}, "order": {...}}}` |
| **JSON 2026** | `{"msg": {...}, "order": {...}}` |

**Viktiga skillnader:**
- XSD: body är **barn** till `<msg>`, orgSender/Receiver på envelope-nivå
- JSON 2021: wrapper `SUTI_XXXX_*`, msg och body som **syskon**
- JSON 2026: ingen wrapper, msg och body som **syskon** på rotnivå

### 12.2 Övriga mappningar i filen

- **Array-namn** - XSD `nodeList` → JSON `nodes` etc.
- **Enumerationer** - numeriska koder → textvärden
- **Anomalikorrigeringar** - `pickupConfirmation` → `event`, stavningsfel etc.
- **Typmappningar** - `xs:string` → `{"type": "string"}` etc.
- **Meddelandetyper** - msgType → body-property mappningar

---

**Nästa steg:** Förbereda för TK-granskning.
