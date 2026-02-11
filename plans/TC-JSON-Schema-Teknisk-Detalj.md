# TC Teknisk Detalj: JSON Schema för SUTI 2026

**Datum:** 2026-02-11
**Relaterat:** [TC-JSON-Schema-Slutrapport.md](TC-JSON-Schema-Slutrapport.md)

---

## 1. XML vs JSON: Sida-vid-sida-jämförelser

### 1.1 Order (msgType 2000)

Detta är SUTI:s viktigaste meddelande - en transportbeställning med rutt, resenärer och resurskrav.

#### XML-struktur (förkortad)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<SUTI>
  <orgSender name="Client name">
    <idOrg src="SUTI:idLink" id="systemsupplierId_clientOwnerId_uniqueId" unique="true"/>
  </orgSender>
  <orgReceiver name="Provider name">
    <idOrg src="SUTI:idLink" id="systemsupplierId_providerOwnerId_uniqueId" unique="true"/>
  </orgReceiver>
  <msg msgType="2000" msgName="Order">
    <idMsg src="systemsupplierId_clientOwnerId_uniqueId:idMsg" id="2020090915822999" unique="true"/>
    <order>
      <idOrder src="systemsupplierId_clientOwnerId_uniqueId:idOrder" id="482" unique="true"/>
      <process allowRouting="true" trafficControl="true" dispatchResponsible="provider"/>
      <resourceOrder>
        <vehicle>
          <idVehicle src="..." id="77777" unique="true"/>
          <capacity><seats noOfSeats="1"/></capacity>
        </vehicle>
      </resourceOrder>
      <route>
        <node nodeSeqno="1" nodeType="pickup">
          <addressNode addressName=" " street="Kvarnstensgatan" streetNo="8">
            <geographicLocation typeOfCoordinate="WGS-84" lat="56.033811" long="12.711738"/>
          </addressNode>
          <timesNode>
            <time timeType="scheduledtime" time="2020-09-09T16:52:00" dwellTime="720"/>
          </timesNode>
          <contents>
            <content contentType="traveller" name="Nils Testsson">
              <idContent src="..." id="15061" unique="true"/>
            </content>
          </contents>
        </node>
        <!-- ... destination node ... -->
      </route>
    </order>
  </msg>
</SUTI>
```

#### JSON-struktur

```json
{
  "msg": {
    "msgType": "2000",
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
  },
  "order": {
    "idOrder": { "src": "...", "id": "11183742", "unique": true },
    "process": {
      "allowRouting": false,
      "trafficControl": true,
      "dispatchResponsible": "provider"
    },
    "resourceOrder": {
      "vehicle": {
        "ids": [{ "src": "...", "id": "51006P", "unique": true }],
        "capacity": { "seats": { "noOfSeats": 1 } }
      }
    },
    "route": {
      "nodes": [
        {
          "nodeSeqNo": 1,
          "nodeType": "pickup",
          "addressNode": {
            "street": "Baravägen",
            "streetNo": 1,
            "community": "Lund",
            "geographicLocation": {
              "typeOfCoordinate": "WGS-84",
              "lat": 55.718095,
              "lon": 13.190738
            }
          },
          "times": [
            { "timeType": "scheduled", "time": "2015-08-10T08:00:00Z", "dwellTime": 0 }
          ],
          "contents": [
            {
              "contentType": "traveller",
              "name": "John Doe",
              "id": { "src": "...", "id": "5319397", "unique": true }
            }
          ]
        }
      ]
    }
  }
}
```

#### Transformationssammanfattning

| Aspekt | XML | JSON | Förändring |
|--------|-----|------|------------|
| Rot-element | `<SUTI>` wrapper | Ingen wrapper | Borttaget |
| Org-placering | Utanför `<msg>` | Inuti `msg` | Flyttat |
| nodeSeqno | `nodeSeqno` | `nodeSeqNo` | camelCase |
| timesNode | `<timesNode>` wrapper | `times` array | Förenklat |
| timeType | `"scheduledtime"` | `"scheduled"` | Suffix borttaget |
| long → lon | `long="12.711738"` | `"lon": 13.190738` | JSON-konvention |

---

### 1.2 KeepAlive (msgType 7000) - Header-only

Header-meddelanden har ingen body, endast `msg`-struktur.

#### XML

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

#### JSON

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

---

### 1.3 Vehicle Event (msgType 4010)

Fordonshändelser rapporterar pickup, drop, noShow etc.

#### JSON-exempel (pickup)

```json
{
  "msg": {
    "msgType": "4010",
    "msgTimeStamp": "2020-09-09T16:45:00.000Z",
    "orgSender": {
      "name": "Provider name",
      "idOrg": { "src": "SUTI:idLink", "id": "systemsupplierId_providerOwnerId_uniqueId", "unique": true }
    },
    "orgReceiver": {
      "name": "Client name",
      "idOrg": { "src": "SUTI:idLink", "id": "systemsupplierId_clientOwnerId_uniqueId", "unique": true }
    },
    "idMsg": { "src": "systemsupplierId_providerOwnerId_uniqueId:idMsg", "id": "2020090916450123", "unique": true },
    "referencesTo": [
      { "idOrder": { "src": "systemsupplierId_clientOwnerId_uniqueId:idOrder", "id": "482", "unique": true } }
    ]
  },
  "event": {
    "eventType": "passengerInVehicle",
    "node": {
      "nodeSeqNo": 1,
      "times": [
        { "timeType": "actual", "time": "2020-09-09T16:45:00.000Z" }
      ]
    }
  }
}
```

**Notera:** `pickupConfirmation` i XSD heter `event` i JSON (anomalikorrigering).

---

### 1.4 Link Mapping (msgType 7100/7101)

Används för att etablera ID-mappning mellan system.

#### JSON-exempel (7100 Request)

```json
{
  "msg": {
    "msgType": "7100",
    "msgTimeStamp": "2025-09-15T14:50:00.000Z",
    "orgSender": {
      "name": "clientOwnerId",
      "idOrg": { "src": "SUTI:idLink", "id": "systemsupplierId_clientOwnerId_uniqueId", "unique": true }
    },
    "orgReceiver": {
      "name": "providerOwnerId",
      "idOrg": { "src": "SUTI:idLink", "id": "systemsupplierId_providerOwnerId_uniqueId", "unique": true }
    },
    "idMsg": { "src": "systemsupplierId_clientOwnerId_uniqueId:idMsg", "id": "2025091514795234", "unique": true },
    "referencesTo": [
      { "idOrder": { "src": "systemsupplierId_clientOwnerId_uniqueId:idOrder", "id": "LINK-001", "unique": true } },
      { "idNode": { "src": "systemsupplierId_clientOwnerId_uniqueId:idNode", "id": "NODE-001", "unique": true } }
    ]
  },
  "order": {
    "idOrder": { "src": "systemsupplierId_clientOwnerId_uniqueId:idOrder", "id": "LINK-001", "unique": true },
    "agreement": {
      "idAgreement": { "src": "systemsupplierId_clientOwnerId_uniqueId:idAgreement", "id": "AGR-001", "unique": true }
    },
    "resourceOrder": {
      "vehicle": {
        "attributes": [{ "src": "SUTI:idAttribute", "id": "1101", "unique": true }]
      },
      "driver": {
        "attributes": [{ "src": "SUTI:idAttribute", "id": "1201", "unique": true }]
      }
    },
    "route": {
      "nodes": [
        {
          "nodeSeqNo": 1,
          "nodeType": "pickup",
          "contents": [
            {
              "contentType": "traveller",
              "name": "John Doe",
              "id": { "src": "systemsupplierId_clientOwnerId_uniqueId:idContent", "id": "CONTENT-001", "unique": true },
              "attributes": [{ "src": "SUTI:idAttribute", "id": "1301", "unique": true }]
            }
          ]
        }
      ]
    }
  }
}
```

---

## 2. Mappningsdokumentationens struktur

### 2.1 xsd-json-mapping.yaml - Innehåll

Filen dokumenterar alla transformationer mellan XSD och JSON Schema:

```yaml
# Metadata
version: "2026.3"
xsd_source: "SUTI_Message.xsd"
json_schema_target: "SUTI_Message.schema.json"

# Strukturella transformationer
structure:
  root:           # Root-element transformation (SUTI wrapper → direkt)
  definitions:    # XSD definitions → JSON $defs
  organization_header:  # Org-placering
  message_type:   # msgType identifiering

# Array-transformationer (17 st)
arrays:
  - xsd: "nodeList"      → json: "nodes"
  - xsd: "timeListNode"  → json: "times"
  - xsd: "contentList"   → json: "contents"
  # ... etc

# Egenskapsförenklingar (21 st)
property_simplifications:
  content:
    - xsd: "idContent"   → json: "id"
    - xsd: "nameContent" → json: "name"
  vehicle:
    - xsd: "idVehicle"   → json: "id"
  # ... etc

# Enumeration-mappningar (6 typer)
enumerations:
  timeType:
    strategy: "text-only"
    mapping:
      "2101": "scheduled"
      "scheduledtime": "scheduled"
  eventType:
    mapping:
      "1701": "passengerInVehicle"
  # ... etc

# Anomalikorrigeringar (8 st)
anomaly_corrections:
  - xsd_name: "pickupConfirmation" → json_name: "event"
  - xsd_name: "nodeCancelation"    → json_name: null (deprecated)
  - xsd_name: "preeOrder"          → json_name: "preOrder"
  # ... etc

# Meddelandetyper (51 st)
message_types:
  "2000": { name: "order", body: "order" }
  "7000": { name: "keepAlive", body: null }
  # ... alla 51 msgTypes
```

### 2.2 Komplett msgType → Body-mappning

| msgType | Namn | Body-typ | Kategori |
|---------|------|----------|----------|
| **1000** | resourceRequest | resourceReservation | Resurs |
| **1020** | resourceLogin | resourceDispatch | Resurs |
| **1021** | resourceLoginConfirmation | null | Resurs |
| **1022** | resourceLoginReject | null | Resurs |
| **1023** | resourceLogoff | resourceDispatch | Resurs |
| **1061** | ratingResponse | ratingList | Resurs |
| **1100** | bulkLocationRequest | bulkLocationRequest | Resurs |
| **1111** | bulkLocationResponse | bulkLocationList | Resurs |
| **1112** | bulkLocationResponsePart | bulkLocationList | Resurs |
| **1500** | infoRequest | infoRequest | Resurs |
| **1600** | infoResponse | infoResponse | Resurs |
| **1920** | resourceAllocation | resourceAllocation | Resurs |
| **2000** | order | order | Order |
| **2001** | orderConfirmation | null | Order |
| **2002** | orderReject | orderReject | Order |
| **2010** | orderCancellation | null | Order |
| **2011** | orderCancellationAccepted | null | Order |
| **2012** | cancellationConsequence | cancellationConsequence | Order |
| **2020** | nodeCancellation | nodeCancellation | Order |
| **2030** | orderForward | orderForward | Order |
| **2040** | orderLink | driverSession | Order |
| **2060** | providerOrderUpdate | providerOrderUpdate | Order |
| **2100** | driverSession | driverSession | Order |
| **2101** | driverSessionAccept | driverSession | Order |
| **2102** | driverSessionReject | driverSessionReject | Order |
| **2800** | orderTemplate | orderTemplate | Order |
| **2810** | scheduleElementConfirmation | scheduleElementOrderList | Order |
| **2901** | authorizationAccept | resource | Order |
| **3003** | dispatchConfirmation | resource | Dispatch |
| **4000** | trafficInfoRequest | resource | Händelse |
| **4001** | trafficInfoResponse | order | Händelse |
| **4010** | eventVehicle | event | Händelse |
| **4011** | vehicleEventAccepted | event | Händelse |
| **4012** | vehicleEventRejected | event | Händelse |
| **4020** | endOfOrder | order | Händelse |
| **4031** | noContactWithVehicle | null | Händelse |
| **4100** | actionRequest | actionRequest | Händelse |
| **5000** | messageToVehicle | messageTo | Meddelande |
| **5010** | messageFromVehicle | messageTo | Meddelande |
| **5011** | messageFromVehicleConfirm | null | Meddelande |
| **5020** | locationRequest | locationRequest | Meddelande |
| **5021** | locationResponse | geographicLocation | Meddelande |
| **6001** | orderReport | orderReport | Rapport |
| **6500** | deliveryNote | deliveryNote | Rapport |
| **7000** | keepAlive | null | System |
| **7001** | keepAliveConfirmation | null | System |
| **7030** | syntaxError | messageTo | System |
| **7031** | notOperational | messageTo | System |
| **7100** | linkMappingRequest | order | System |
| **7101** | linkMappingResponse | order | System |
| **8000** | accounting | accounting | Ekonomi |

---

## 3. JSON Schema-tekniska detaljer

### 3.1 Villkorlig validering (if/then)

JSON Schema använder villkorliga regler för att matcha msgType med rätt body:

```json
{
  "allOf": [
    {
      "if": {
        "properties": {
          "msg": {
            "properties": { "msgType": { "const": "2000" } }
          }
        }
      },
      "then": {
        "required": ["order"],
        "properties": {
          "order": { "$ref": "#/$defs/order" }
        }
      }
    },
    {
      "if": {
        "properties": {
          "msg": {
            "properties": { "msgType": { "const": "7000" } }
          }
        }
      },
      "then": {
        "unevaluatedProperties": false
      }
    }
  ]
}
```

### 3.2 Centraliserad msgType-enum

Alla giltiga msgTypes definieras på ett ställe:

```json
{
  "$defs": {
    "msgTypeEnum": {
      "type": "string",
      "description": "Valid SUTI message type codes (centralized for reuse)",
      "enum": ["1000", "1020", "1021", "1022", "1023", "1061", "1100", "1111", "1112", "1500", "1600", "1920", "2000", "2001", "2002", "2010", "2011", "2012", "2020", "2030", "2040", "2060", "2100", "2101", "2102", "2800", "2810", "2901", "3003", "4000", "4001", "4010", "4011", "4012", "4020", "4031", "4100", "5000", "5010", "5011", "5020", "5021", "6001", "6500", "7000", "7001", "7030", "7031", "7100", "7101", "8000"]
    }
  }
}
```

### 3.3 Semantiska constraints

#### Koordinatvalidering

```json
{
  "geographicLocation": {
    "properties": {
      "lat": { "type": "number", "minimum": -90, "maximum": 90 },
      "lon": { "type": "number", "minimum": -180, "maximum": 180 }
    }
  }
}
```

#### referenceToMsg - minst ett ID krävs

```json
{
  "referenceToMsg": {
    "anyOf": [
      { "required": ["idMsg"] },
      { "required": ["idOrder"] },
      { "required": ["idNode"] }
    ]
  }
}
```

---

## 4. Valideringsresultat

### 4.1 Alla 36 exempel validerade

```bash
# Validera alla JSON-exempel
for f in examples/JSON/draft_2026/*.json; do
  python3 -c "import json, jsonschema; \
    schema = json.load(open('schemas/SUTI_Message.schema.json')); \
    instance = json.load(open('$f')); \
    jsonschema.validate(instance, schema)" && echo "✓ $f"
done
```

### 4.2 Exempelfiler

| Fil | msgType | Body |
|-----|---------|------|
| 1020_resourceLogin.json | 1020 | resourceDispatch |
| 1021_resourceLoginConfirm.json | 1021 | null |
| 1022_resourceLoginReject.json | 1022 | null |
| 1023_resourceLogoff.json | 1023 | resourceDispatch |
| 2000_order.json | 2000 | order |
| 2000_orderAlter.json | 2000 | order |
| 2000_multiOrder.json | 2000 | order |
| 2000_trip.json | 2000 | order |
| 2001_orderConfirmation.json | 2001 | null |
| 2002_orderReject.json | 2002 | orderReject |
| 2010_orderCancellation.json | 2010 | null |
| 2011_orderCancellationAccepted.json | 2011 | null |
| 2100_driverSession.json | 2100 | driverSession |
| 3003_dispatchConfirmation.json | 3003 | resource |
| 4010_eventVehicle.json | 4010 | event |
| 4010_bom.json | 4010 | event |
| 4010_drop.json | 4010 | event |
| 4011_vehicleEventAccepted.json | 4011 | event |
| 4012_pickup.json | 4012 | event |
| 4012_drop.json | 4012 | event |
| 4012_bomRejected.json | 4012 | event |
| 4020_endOfOrder.json | 4020 | order |
| 4031_noContactWithVehicle.json | 4031 | null |
| 5000_messageToVehicle.json | 5000 | messageTo |
| 5010_messageFromVehicle.json | 5010 | messageTo |
| 5011_messageFromVehicleConfirm.json | 5011 | null |
| 5020_locationRequest.json | 5020 | locationRequest |
| 5021_locationResponse.json | 5021 | geographicLocation |
| 7000_keepAlive.json | 7000 | null |
| 7001_keepAliveConfirmation.json | 7001 | null |
| 7030_syntaxError.json | 7030 | messageTo |
| 7031_notOperational.json | 7031 | messageTo |
| 7100_linkMappingRequest.json | 7100 | order |
| 7101_linkMappingResponse.json | 7101 | order |
| 1111_bulkLocationResponse.json | 1111 | bulkLocationList |
| 1111_bulkLocationResponse.legacy.json | 1111 | (legacy format) |

---

## 5. Implementeringsråd

### 5.1 Konvertering XML → JSON

1. Ta bort `<SUTI>` wrapper
2. Flytta `orgSender`/`orgReceiver` in i `msg`
3. Lägg till `msgTimeStamp` (ISO 8601 med Z)
4. Pluralisera arrays (`timesNode` → `times`, `nodeList` → `nodes`)
5. Byt enum-text (`scheduledtime` → `scheduled`)
6. Byt `long` → `lon` i koordinater
7. Använd `event` istället för `pickupConfirmation`

### 5.2 Konvertering JSON → XML

1. Skapa `<SUTI>` wrapper
2. Flytta `orgSender`/`orgReceiver` ut ur `msg`
3. Ta bort `msgTimeStamp` (valfritt i XML)
4. Singularisera wrappers (`times` → `<timesNode>`)
5. Översätt enum-text till numerisk kod om nödvändigt
6. Byt `lon` → `long`
7. Använd `pickupConfirmation` istället för `event`

---

**Version:** 1.0
**Senast uppdaterad:** 2026-02-11
