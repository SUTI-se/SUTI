# JSON Schema 2021→2026 Ändringslogg

**Datum:** 2026-02-09
**Jämförelse:** `SUTI_Message_JSON_draft_20210915.json` → `SUTI_Message.schema.json`

---

## Sammanfattning

| Kategori | Antal ändringar |
|----------|-----------------|
| Strukturella ändringar | 5 |
| Borttagna element | 14 |
| Stavfel korrigerade | 7 |
| Enum-ändringar | 12 |
| Nya features | 8 |
| Typdefinitioner uppdaterade | ~50 |

---

## 1. Schema-metadata

| Element | 2021 | 2026 | Typ |
|---------|------|------|-----|
| `$schema` | `http://json-schema.org/schema#` | `https://json-schema.org/draft/2020-12/schema` | **Uppdatering** |
| `$id` | *(saknas)* | `https://suti.se/schema/SUTI_Message.schema.json` | **Ny** |
| `title` | *(saknas)* | `SUTI Message Schema` | **Ny** |
| `description` | *(saknas)* | Beskrivande text | **Ny** |
| `$ref` entry | `#/definitions/SUTI_validateObject` | `#` (root med `allOf`) | **Strukturändring** |
| `definitions` | Används | Ersatt med `$defs` | **Migrering** |

---

## 2. Borttagna XSD-bastyper

Följande typdefinitioner har tagits bort helt. Deras funktionalitet ersätts av inline JSON Schema-typer.

| 2021-typ | Ersättning i 2026 |
|----------|-------------------|
| `xs:anySimpleType` | *(borttagen)* |
| `xs:anyType` | *(borttagen)* |
| `xs:boolean` | `"type": "boolean"` inline |
| `xs:date` | `"type": "string", "format": "date"` inline |
| `xs:dateTime` | `"type": "string", "format": "date-time"` inline |
| `xs:decimal` | `"type": "number"` inline |
| `xs:float` | `"type": "number"` inline (var felaktigt `string`) |
| `xs:int` | `"type": "integer"` inline |
| `xs:integer` | `"type": "integer"` inline |
| `xs:nonNegativeInteger` | `"type": "integer", "minimum": 0` inline |
| `xs:positiveInteger` | `"type": "integer", "minimum": 1` inline |
| `xs:string` | `"type": "string"` inline |

**Motivering:** JSON Schema har inbyggda typer. XSD-prefix är förvirrande och skapar onödig komplexitet.

---

## 3. Borttagen wrapper-struktur

### 2021: Wrapper-element per meddelande
```json
{
  "SUTI_2000_order": {
    "msg": { "msgType": "2000", ... },
    "order": { ... }
  }
}
```

### 2026: Flat struktur med diskriminator
```json
{
  "msg": { "msgType": "2000", ... },
  "order": { ... }
}
```

**Borttagna definitioner:**
- `SUTI_validateObject`
- `SUTI_1000_resourceRequest`
- `SUTI_1061_ratingResponse`
- `SUTI_1100_bulkLocationRequest`
- `SUTI_1111_bulkLocationResponse`
- `SUTI_1112_bulkLocationResponse`
- `SUTI_1500_nodeListRequest`
- `SUTI_1600_nodeListResponse`
- `SUTI_1920_resourceAllocation`
- `SUTI_2000_order`
- `SUTI_2001_orderConfirmation`
- `SUTI_2002_orderReject`
- `SUTI_2012_cancellationAcceptWithConsequence`
- `SUTI_2020_nodeCancellation`
- `SUTI_2030_orderForward`
- `SUTI_2040_orderLink`
- `SUTI_2060_providerOrderUpdate`
- `SUTI_2100_driverSession`
- `SUTI_2101_driverSessionAccept`
- `SUTI_2102_driverSessionReject`
- `SUTI_2800_orderTemplate`
- `SUTI_2810_ScheduleElementConfirmation`
- `SUTI_2901_authorizationAccept`
- `SUTI_3003_dispatchConfirmation`
- `SUTI_4000_trafficInformationRequest`
- `SUTI_4001_trafficInformationResponse`
- `SUTI_4010_eventVehicle`
- `SUTI_4100_actionRequest`
- `SUTI_5000_messageToVehicle`
- `SUTI_5020_locationRequest`
- `SUTI_5021_locationResponse`
- `SUTI_6001_orderReport`
- `SUTI_6500_deliveryNote`
- `SUTI_7000_keepAlive`
- `SUTI_7001_keepAliveConfirmation`
- `SUTI_8000_accounting`

**Ersättning:** `allOf` med `if/then`-villkor baserat på `msg.msgType`.

---

## 4. Borttagna msg*-wrappers

| 2021 | Status | Kommentar |
|------|--------|-----------|
| `msgBasic` | **Borttagen** | Inline i `allOf` |
| `msgOrder` | **Borttagen** | Inline i `allOf` |
| `msgEvent` | **Borttagen** | Inline i `allOf` |
| `msgResource` | **Borttagen** | Inline i `allOf` |
| `msgBulkLocationList` | **Borttagen** | Inline i `allOf` |
| `msgBulkLocationRequest` | **Borttagen** | Inline i `allOf` |
| `msgAccounting` | **Borttagen** | Inline i `allOf` |
| `msgActionRequest` | **Borttagen** | Inline i `allOf` |
| `msgAuthorizationAccept` | **Borttagen** | Inline i `allOf` |
| `msgCancellationConsequence` | **Borttagen** | Inline i `allOf` |
| `msgDeliveryNote` | **Borttagen** | Inline i `allOf` |
| `msgDriverSession` | **Borttagen** | Inline i `allOf` |
| `msgDriverSessionAccept` | **Borttagen** | Inline i `allOf` |
| `msgDriverSessionReject` | **Borttagen** | Inline i `allOf` |
| `msgGeographicLocation` | **Borttagen** | Inline i `allOf` |
| `msgInfoRequest` | **Borttagen** | Inline i `allOf` |
| `msgInfoResponse` | **Borttagen** | Inline i `allOf` |
| `msgLocationRequest` | **Borttagen** | Inline i `allOf` |
| `msgMessageTo` | **Borttagen** | Inline i `allOf` |
| `msgNodeCancellation` | **Borttagen** | Inline i `allOf` |
| `msgOrderForward` | **Borttagen** | Inline i `allOf` |
| `msgOrderReject` | **Borttagen** | Inline i `allOf` |
| `msgOrderReport` | **Borttagen** | Inline i `allOf` |
| `msgOrderTemplate` | **Borttagen** | Inline i `allOf` |
| `msgProviderOrderUpdate` | **Borttagen** | Inline i `allOf` |
| `msgRatingList` | **Borttagen** | Inline i `allOf` |
| `msgResourceAllocation` | **Borttagen** | Inline i `allOf` |
| `msgResourceResevation` | **Borttagen** | Inline i `allOf` |
| `msgScheduleElementOrderList` | **Borttagen** | Inline i `allOf` |

---

## 5. Stavfel korrigerade

| 2021 (fel) | 2026 (rätt) | Plats |
|------------|-------------|-------|
| `idVerson` | `idVersion` | msg |
| `preeOrder` | `preOrder` | process |
| `exhangeRate` | `exchangeRate` | *(om använd)* |
| `resourceAlloc ation` | `resourceAllocation` | msgResourceAllocation |
| `nodeprocess` | `nodeProcess` | node |
| `msgSeqno` | `msgSeqNo` | bulkLocationList |
| `sendinformationDisptch` | `sendInformationDispatch` | nodeProcess |
| `statusNotinuse` | `statusNotInUse` | bulkLocationRequest |
| `pickupconfirmation` | `pickupConfirmation` | process |

---

## 6. Enum-ändringar (numerisk kod borttagen)

### nodeType

| 2021 | 2026 |
|------|------|
| `["1801", "action", "1802", "navigation", "1803", "pickup", "1804", "destination"]` | `["action", "navigation", "pickup", "destination"]` |

### subnodeType

| 2021 | 2026 |
|------|------|
| `["1901", "break", "1902", "driverassist", ...]` | `["break", "driverAssist", "mobAidPickup", "mobAidDropoff", "ferryDeparture", "ferryArrival", "waitForInstructions", "flagStop", "refuel", "pullIn", "pullOut"]` |

### eventType

| 2021 | 2026 |
|------|------|
| `["1716", "acceptOrder", "1714", "start", ...]` | `["acceptOrder", "start", "stop", "pickup", "destination", "navigation", "action", "passengerInVehicle", "passengerDropped", "noShow", "parcelInVehicle", "parcelDropped", "actionDone", "navigationDone", "cancelAtDoor", "vehicleAtNode", "infoToContent", "dispatchConfirmationSent", "delayConfirmationSent", "arrivalConfirmationSent"]` |

### paymentType

| 2021 | 2026 |
|------|------|
| `["1301", "cash", "1302", "card", ...]` | `["cash", "card", "account", "ticket", "voucher", "prepaidSocialFee", "app", "invoice"]` |

### orderStatus.status

| 2021 | 2026 |
|------|------|
| `["none", "started", "completed", "noshow", ...]` | `["none", "started", "completed", "noShow", "confirmed", "dispatching", "dispatched", "cancelled"]` |

### msgType (i msg)

| 2021 | 2026 |
|------|------|
| Explicit `enum` med 134 värden | `pattern: "^[1-8][0-9]{3}$"` |

**Motivering:** Pattern är enklare att underhålla och validerar alla giltiga meddelandetyper.

---

## 7. Casing-normalisering (camelCase)

| 2021 | 2026 | Typ |
|------|------|-----|
| `passengerinvehicle` | `passengerInVehicle` | eventType |
| `passengerdropped` | `passengerDropped` | eventType |
| `parcelinvehicle` | `parcelInVehicle` | eventType |
| `parceldropped` | `parcelDropped` | eventType |
| `actiondone` | `actionDone` | eventType |
| `navigationdone` | `navigationDone` | eventType |
| `cancelatdoor` | `cancelAtDoor` | eventType |
| `vehicleatnode` | `vehicleAtNode` | eventType |
| `infotocontent` | `infoToContent` | eventType |
| `dispatchconfirmationsent` | `dispatchConfirmationSent` | eventType |
| `delayconfirmationsent` | `delayConfirmationSent` | eventType |
| `arrivalconfirmationsent` | `arrivalConfirmationSent` | eventType |
| `driverassist` | `driverAssist` | subnodeType |
| `mobaidpickup` | `mobAidPickup` | subnodeType |
| `mobaiddropoff` | `mobAidDropoff` | subnodeType |
| `ferrydeparture` | `ferryDeparture` | subnodeType |
| `ferryarrival` | `ferryArrival` | subnodeType |
| `waitforinstructions` | `waitForInstructions` | subnodeType |
| `flagstop` | `flagStop` | subnodeType |
| `notrequested` | `notRequested` | pickupConfirmation |
| `alwayssend` | `alwaysSend` | sendInformation* |
| `neversend` | `neverSend` | sendInformation* |
| `allowsend` | `allowSend` | sendInformation* |
| `prepaidsocialfee` | `prepaidSocialFee` | paymentType |

---

## 8. Nya format-valideringar

| Fält | 2021 | 2026 |
|------|------|------|
| `msgTimeStamp` | `"type": "string"` | `"type": "string", "format": "date-time"` |
| `infoTimeStamp` | `"type": "string"` | `"type": "string", "format": "date-time"` |
| `time` (i time-objekt) | `"type": "string"` | `"type": "string", "format": "date-time"` |
| `url` (i address) | `"type": "string"` | `"type": "string", "format": "uri"` |
| `startDate`, `endDate` | *(om finns)* | `"type": "string", "format": "date"` |

---

## 9. Uppdaterade required-fält

| Typ | 2021 required | 2026 required |
|-----|---------------|---------------|
| `msg` | `["orgSender", "orgReceiver", "idMsg"]` | `["msgType", "orgSender", "orgReceiver", "idMsg"]` |
| `order` | *(inget)* | `["idOrder"]` |
| `id` | *(inget)* | `["src", "id"]` |
| `org` | `["name", "idOrg"]` | `["name", "idOrg"]` *(oförändrad)* |
| `node` | `["nodeSeqno", "nodeType"]` | `["nodeSeqNo", "nodeType"]` |
| `time` | *(inget)* | `["timeType", "time"]` |

---

## 10. Strukturella förändringar i typer

### msg
```diff
  "msg": {
    "properties": {
+     "msgType": { "pattern": "^[1-8][0-9]{3}$" },  // Ändrad från enum
      "msgTimeStamp": { "format": "date-time" },   // Ny format
      "infoTimeStamp": { "format": "date-time" },  // Ny format
-     "idVerson": ...                              // Stavfel korrigerat
+     "idVersion": ...
    },
-   "required": ["orgSender", "orgReceiver", "idMsg"]
+   "required": ["msgType", "orgSender", "orgReceiver", "idMsg"]
  }
```

### node
```diff
  "node": {
    "properties": {
-     "nodeSeqno": ...
+     "nodeSeqNo": ...                    // Casing korrigerad
      "nodeType": {
-       "enum": ["1801", "action", ...]   // Dubbla värden
+       "enum": ["action", "navigation", "pickup", "destination"]
      },
-     "nodeprocess": ...                  // Stavfel
+     "nodeProcess": ...
    }
  }
```

### process
```diff
  "process": {
    "properties": {
-     "pickupconfirmation": {
+     "pickupConfirmation": {             // Casing korrigerad
-       "enum": ["notrequested", ...]
+       "enum": ["notRequested", "standard", "extended"]
      },
-     "preeOrder": ...                    // Stavfel
+     "preOrder": ...
    }
  }
```

### bulkLocationList
```diff
  "bulkLocationList": {
    "properties": {
-     "msgSeqno": ...                     // Stavfel
+     "msgSeqNo": ...
    }
  }
```

---

## 11. Nya typdefinitioner

| Typ | Beskrivning |
|-----|-------------|
| `referenceToMsg` | Separerad från `referencesTo` array |
| `vehicleLocation` | Explicit typ för positionsdata |
| `mobilityAid` | Strukturerad typ för hjälpmedel |
| `tour` | För redovisningsdata |
| `rating` | För betygslista |

---

## 12. Borttagna typer (oanvända eller överflödiga)

| Typ | Anledning |
|-----|-----------|
| `multiDispatch` | Ersatt av boolean i `process` |
| `attribute` | Var alias för `id` |
| `attributeList` | Var alias för `idList` |

---

## 13. Legacy-schema för bulkLocation

Ett separat schema skapas för bakåtkompatibilitet:

**Fil:** `SUTI_BulkLocation_legacy.schema.json`

**Stöder:**
- `SUTI_1100_bulkLocationRequest` (wrapper-format)
- `SUTI_1111_bulkLocationResponse` (wrapper-format)
- `SUTI_1112_bulkLocationResponse` (wrapper-format)

**Deprecation:** 2027-06-30

---

## 14. Migreringsguide

### För 1100/1111/1112 (bulkLocation)

**Steg 1:** Validera mot legacy-schema (omedelbart)
```
SUTI_BulkLocation_legacy.schema.json
```

**Steg 2:** Migrera till nytt format (före 2027-06-30)
```diff
- { "SUTI_1111_bulkLocationResponse": { "msg": {...}, "bulkLocationList": {...} } }
+ { "msg": {"msgType": "1111", ...}, "bulkLocationList": {...} }
```

**Steg 3:** Validera mot nytt schema
```
SUTI_Message.schema.json
```

### För övriga meddelandetyper

Alla andra meddelanden ska använda det nya formatet direkt:

```json
{
  "msg": {
    "msgType": "2000",
    "orgSender": { ... },
    "orgReceiver": { ... },
    "idMsg": { ... }
  },
  "order": { ... }
}
```

---

## 15. Fil-sammanfattning

| Fil | Storlek | Syfte |
|-----|---------|-------|
| `SUTI_Message_JSON_draft_20210915.json` | ~3600 rader | Originalschema (arkiveras) |
| `SUTI_Message.schema.json` | ~1100 rader | Nytt huvudschema |
| `SUTI_BulkLocation_legacy.schema.json` | ~180 rader | Bakåtkompatibelt för 1100/1111/1112 |

**Reduktion:** ~70% mindre schema genom förenklad struktur.

---

**Författare:** Claude Code
**Granskad:** Väntar
**Giltig från:** Q2 2026
