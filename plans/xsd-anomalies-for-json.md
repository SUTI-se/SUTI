# XSD-anomalier att åtgärda i JSON-versionen

**Datum:** 2026-02-09
**Syfte:** Identifiera anomalier och betydelsedrift i XSD som bör korrigeras vid JSON Schema-designen
**Källa:** HowToUseSUTI.txt, XSD-analyser, SUTI_Message.xsd

---

## Sammanfattning

| Anomali | Typ | Prioritet | JSON-åtgärd |
|---------|-----|-----------|-------------|
| 1. pickupConfirmation → event | Betydelsedrift | Hög | Byt namn till `event` |
| 2. nodeCancelation (felstavning) | Stavfel | Hög | Endast `nodeCancellation` |
| 3. exhangeRate (felstavning) | Stavfel | Medel | Korrigera till `exchangeRate` |
| 4. location (dubbelbetydelse) | Semantisk konflikt | Hög | Separera till `area` vs `coordinates` |
| 5. Traveller/Passenger/Content | Inkonsekvent terminologi | Medel | Standardisera till `traveller` |
| 6. Dubbla enumvärden | Teknisk skuld | Hög | Endast textvärden |
| 7. formOfPayment (singularis) | Namnkonvention | Medel | JSON: `payments` (plural) |
| 8. idVersion (oanvänd) | Överkonstruktion | Låg | Ersätt med `schemaVersion` |
| 9. eventReport (oklar användning) | Överlapp | Medel | Konsolidera med `event` |
| 10. Boolean-attributöverflöd i process | Komplexitet | Medel | Strukturera som objekt |

---

## 1. pickupConfirmation → event (KRITISK)

### Problem
Dokumenterat i HowToUseSUTI.txt (rad 555-557):
> *"NOTE: For historical reasons and backward compatibility, Events are placed under the PickupConfirmation tag (as it was the first Event type). The attribute EventType clarifies that there are many different Events under PickupConfirmation."*

### Nuvarande situation
- Element heter `pickupConfirmation` men används för **alla event-typer**
- 19 olika eventType-värden (1701-1719):
  - `1701 invehicle` (passengerinvehicle)
  - `1702 exitvehicle` (passengerdropped)
  - `1703 noshow`
  - `1709 vehicleatnode`
  - `1714 start`
  - `1715 stop`
  - `1716 acceptOrder`
  - ... och fler

### JSON-åtgärd
```json
{
  "event": {
    "eventType": "vehicleatnode",
    "nodeNumber": 1,
    "timestamp": "2026-02-09T08:30:00Z",
    "content": { ... }
  }
}
```

**Mappning:**
- XSD: `pickupConfirmation` → JSON: `event`
- Behåll `eventType` som diskriminator
- Dokumentera mappningen explicit

### Bakåtkompatibilitet
- XSD behåller `pickupConfirmation` för bakåtkompatibilitet
- JSON använder det semantiskt korrekta `event`
- Konverteringsverktyg hanterar översättningen

---

## 2. nodeCancelation (felstavning)

### Problem
XSD-schemat innehåller explicit varning (rad 250-252):
> *"Msg 2020 Node Cancelation. This shall not be used due to error in spelling. TU request members to change to nodeCancellation as soon as possible."*

### Nuvarande situation
Båda finns i XSD:
- `nodeCancelation` (felstavat, deprecated)
- `nodeCancellation` (korrekt)

### JSON-åtgärd
- **Endast** `nodeCancellation` i JSON Schema
- Ingen bakåtkompatibilitet för felstavningen behövs

```json
{
  "nodeCancellation": {
    "nodeStart": 1,
    "nodeEnd": 2,
    "reason": "passenger_noshow"
  }
}
```

---

## 3. exhangeRate (felstavning)

### Problem
XSD rad 1306: `<xs:complexType name="exhangeRate">` (saknar 'c')
Elementet heter dock korrekt: `exchangeRate` (rad 1303)

### JSON-åtgärd
- Korrigera till `exchangeRate` i JSON Schema
- Konsekvens i både typ- och elementnamn

```json
{
  "exchangeRates": [
    {
      "fromCurrency": "SEK",
      "toCurrency": "EUR",
      "rate": 0.087
    }
  ]
}
```

---

## 4. location (dubbelbetydelse)

### Problem
Dokumenterat i HowToUseSUTI.txt (rad 585-587):
> *"An Address can contain attributes like street, streetno etc. In this context, the attribute 'location' refers to a geographical area, e.g. a postal area or a taxiarea. This is an exception, as 'location' in all other SUTI contexts refers to geographical coordinates."*

### Nuvarande situation
`location` betyder två olika saker:
1. **I addressType:** Geografiskt område (postnummer, taxiområde)
2. **Överallt annars:** Koordinater (WGS-84)

### JSON-åtgärd
Separera begreppen:

```json
{
  "address": {
    "street": "Kungsgatan",
    "streetNo": "1",
    "area": "Stockholm",           // Tidigare: location (i address)
    "postalCode": "111 43",
    "coordinates": {               // Tidigare: geographicLocation
      "latitude": 59.3293,
      "longitude": 18.0686
    }
  }
}
```

**Mappning:**
- XSD `addressType.location` → JSON `address.area`
- XSD `geographicLocation` → JSON `coordinates`
- Eliminerar semantisk tvetydighet

---

## 5. Traveller/Passenger/Content (inkonsekvent terminologi)

### Problem
HowToUseSUTI.txt (rad 512-514):
> *"The dominating Content types are Traveller (sometimes called Passenger) or Parcel"*

### Nuvarande situation
Tre termer används för samma koncept:
- **Content** - Generisk term (XML-element)
- **Traveller** - Officiell term i dokumentation
- **Passenger** - Alternativ term, används i event-typer (`passengerinvehicle`)

Event-typerna använder `passenger`:
- `1701 invehicle (alt passengerinvehicle)`
- `1702 exitvehicle (alt passengerdropped)`

### JSON-åtgärd
Standardisera på **en term**:

**Rekommendation:** `traveller` (brittisk stavning, matchar NeTEx/Transmodel)

```json
{
  "content": {
    "contentType": "traveller",
    "traveller": {
      "name": "Anna Andersson",
      "id": "12345"
    }
  }
}
```

Event-typer:
```json
{
  "eventType": "travellerInVehicle"  // Istället för passengerinvehicle
}
```

**Alternativ:** Behåll `content` som generisk wrapper men använd konsekvent `traveller` inom den.

---

## 6. Dubbla enumvärden (numeriskt + text)

### Problem
XSD tillåter både numeriska koder och textnamn för samma värde:

```xml
<xs:enumeration value="3101"/>
<xs:enumeration value="client"/>
<xs:enumeration value="3102"/>
<xs:enumeration value="provider"/>
```

### Nuvarande situation
- Skapar validerings-tvetydighet
- Dubbel dokumentation
- Svårt för implementerare

Exempel från XSD:
- `dispatchResponsible`: 3101/client, 3102/provider
- `pickupConfirmation`: 3110/notrequested, 3111/standard, 3112/extended
- `timeType`: 2101/scheduledtime, 2102/estimatedtime, etc.

### JSON-åtgärd
**Endast textvärden** i JSON:

```json
{
  "dispatchResponsible": "client",
  "timeType": "scheduled"
}
```

**Mappningstabell:**
```yaml
enumerations:
  dispatchResponsible:
    "3101": "client"
    "3102": "provider"
  timeType:
    "2101": "scheduled"
    "2102": "estimated"
    "2103": "promised"
    "2104": "actual"
    "2105": "asap"
```

---

## 7. formOfPayment (singularis för kollektion)

### Problem
XSD använder singularis `formOfPayment` för vad som kan vara flera betalningsformer.

### JSON-åtgärd
Följ JSON-konvention med plural för arrayer:

**XSD:**
```xml
<formOfPayment>...</formOfPayment>
<formOfPayment>...</formOfPayment>
```

**JSON:**
```json
{
  "payments": [
    {
      "type": "account",
      "accountId": "12345"
    },
    {
      "type": "socialServiceFee",
      "amount": 50.00
    }
  ]
}
```

**Mappning:**
- XSD `formOfPayment` (element, upprepas) → JSON `payments` (array)

---

## 8. idVersion (oanvänd/oklar)

### Problem
XSD-schemat noterar (rad 111):
> *"TU would like to know if anyone uses this part. Please inform TU in such case."*

### Nuvarande situation
- Optionellt element på rot-nivå
- Ingen tydlig versionsstrategi
- Oklart om någon använder det

### JSON-åtgärd
Ersätt med tydlig versionsstrategi:

```json
{
  "schemaVersion": "2.0.0",
  "message": {
    "msgType": "2000",
    ...
  }
}
```

**Alternativ:** Använd HTTP-header för version istället för i payload.

---

## 9. eventReport (överlappande funktionalitet)

### Problem
XSD innehåller kommentar (rad 2270-2274):
> *"TU is uncertain to the use of eventReport since the use of 4010 pickupConfirmation is more used to give information about an event. Pls inform TU about any usage of eventReport. OBSERVE!! Contact TU before using this!!!"*

### Nuvarande situation
- Två sätt att rapportera events: `pickupConfirmation` och `eventReport`
- `eventReport` verkar oanvänt/oklart
- Skapar förvirring

### JSON-åtgärd
Konsolidera till **en struktur** för events:

```json
{
  "events": [
    {
      "eventType": "vehicleAtNode",
      "timestamp": "2026-02-09T08:30:00Z",
      "nodeNumber": 1,
      "details": { ... }
    }
  ]
}
```

Om `eventReport` behövs för sammanfattning, gör det explicit:

```json
{
  "eventSummary": {
    "totalEvents": 5,
    "completedNodes": 2,
    "events": [ ... ]
  }
}
```

---

## 10. Boolean-attributöverflöd i process

### Problem
`process`-typen har 10 boolean-attribut som skapar 1024 möjliga kombinationer:
- `manualDispatch`
- `dispatch`
- `trafficControl`
- `report`
- `preorderedVehicle`
- `allowRouting`
- `automaticStatus`
- `orderAlteration`
- `deliveryNote`
- `allowForward`

### JSON-åtgärd
Strukturera som grupperade objekt:

```json
{
  "processConfig": {
    "dispatch": {
      "enabled": true,
      "responsible": "client",
      "manual": false
    },
    "control": {
      "trafficControl": true,
      "automaticStatus": false
    },
    "routing": {
      "allowRouting": true,
      "allowForward": false
    },
    "reporting": {
      "report": true,
      "deliveryNote": true
    }
  }
}
```

**Alternativ:** Fördefinierade profiler:

```json
{
  "processProfile": "standardClientControlled"
}
```

---

## Ytterligare observationer

### Stavningsinkonsistenser i dokumentation
- `preeOrder` (borde vara `preOrder`)
- `ReferecesTo` (borde vara `ReferencesTo`) - förekommer i dokumentation
- Inkonsekvens mellan brittisk/amerikansk stavning

### Potentiella JSON-förbättringar utöver anomalifixar

1. **Förenklad tidsstämpelhantering:**
   - Använd ISO 8601 direkt utan separata timeZone-attribut

2. **Plattare struktur för node:**
   - Undvik djup nästling där möjligt

3. **Konsekvent ID-struktur:**
   ```json
   {
     "id": {
       "source": "SUTI:idLink",
       "value": "systemprov_provsite_0001",
       "unique": true
     }
   }
   ```

---

## Implementeringsordning

### Fas 1: Kritiska rättningar (Q1 2026)
1. `pickupConfirmation` → `event`
2. Ta bort `nodeCancelation`
3. Endast text-enum i JSON

### Fas 2: Semantiska förbättringar (Q2 2026)
4. Separera `location` betydelser
5. Standardisera `traveller`/`passenger`
6. Plural för arrayer (`payments`, `events`, etc.)

### Fas 3: Strukturella förbättringar (Q3 2026)
7. Korrigera `exhangeRate` → `exchangeRate`
8. Strukturera `process`-konfiguration
9. Tydlig versionsstrategi
10. Konsolidera `event`/`eventReport`

---

## Nästa steg

1. **TK-diskussion:** Bekräfta att dessa anomalier ska åtgärdas i JSON
2. **Mappningstabell:** Skapa komplett XSD↔JSON mappningsdokument
3. **JSON Schema:** Implementera korrektionerna i JSON Schema-designen
4. **Testfall:** Skapa valideringsexempel som testar korrekt mappning

---

**Status:** Utkast för TK-granskning
**Författare:** Claude Code (nora agent)
