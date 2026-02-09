# SUTI Schema-modernisering
## Presentation för Tekniska Kommittén

**Ämne:** XSD-refaktorering & JSON Schema-strategi
**Datum:** 2026-01-30
**Presentatör:** [Ditt namn]

---

# AGENDA

1. Nulägesanalys
2. Nyckelinsikt: Implicita profiler
3. Förslag: Profilbaserad struktur
4. Vägen framåt för JSON Schema
5. Rekommenderad tidplan
6. Diskussion

---

# 1. NULÄGE

## Schema i korthet

```
+------------------+------------------+
|     MÄTVÄRDE     |      VÄRDE       |
+------------------+------------------+
| Schemastorlek    | 3 131 rader      |
| Komplexa typer   | 86               |
| Meddelandetyper  | 136              |
| Identifierade    | 12 kategorier    |
| flöden           |                  |
| Dokumentation    | 89,5% täckning   |
+------------------+------------------+
```

## Utmaningen

- **Enda monolitisk XSD** - svår att navigera
- **Allt-eller-inget** vid implementation
- **Inga tydliga konformitetsnivåer** för upphandlingar
- **JSON-övergång** kräver ren struktur

---

# 2. NYCKELINSIKT: IMPLICITA PROFILER FINNS REDAN

## Från dokumentet "How to use SUTI":

> "SUTI ger möjlighet till flera olika sätt att konfigurera
> en koppling mellan Klient och Utförare.
> En enkel taxi-app kräver mycket mindre funktionalitet än
> en komplicerad dynamisk kombination av resor."

## Självdeklarationer = Implicita profiler

```
  KLIENTENS SJÄLVDEKLARATION
  +-----------------------------------------+
  |  "Vi stödjer dessa flöden:"             |
  |  [x] Grundläggande order (2000, 2001)   |
  |  [x] Dispatch (3xxx)                    |
  |  [x] Trafikstyrning (4xxx)              |
  |  [ ] DriverSession (21xx)      <-- NEJ  |
  |  [ ] Redovisning (8xxx)        <-- NEJ  |
  +-----------------------------------------+
        ^
        |
        Detta ÄR en profil!
```

**80% av implementationerna använder endast en delmängd av funktionerna**

---

# 3. FÖRSLAG: EXPLICITA PROFILER

## Fem konformitetsnivåer

```
  SUTI-Full ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    + Repetitiva ordrar, Flaggstop, Redovisning    ┃
                                                   ┃
  SUTI-Session ━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓       ┃
    + DriverSession (21xx), Orderkombos    ┃       ┃
                                           ┃       ┃
  SUTI-Advanced ━━━━━━━━━━━━━━━━━━━┓       ┃       ┃
    + Nod-för-nod, Följesedlar     ┃       ┃       ┃
                                   ┃       ┃       ┃
  SUTI-Standard ━━━━━━━━━━━┓       ┃       ┃       ┃
    + Dispatch, Trafik-    ┃       ┃       ┃       ┃
      styrning             ┃       ┃       ┃       ┃
                           ┃       ┃       ┃       ┃
  SUTI-Basic ━━━━┓         ┃       ┃       ┃       ┃
    Endast ordrar┃         ┃       ┃       ┃       ┃
                 ┃         ┃       ┃       ┃       ┃
  ━━━━━━━━━━━━━━━┻━━━━━━━━━┻━━━━━━━┻━━━━━━━┻━━━━━━━┛
       ~30%         ~50%      ~15%     ~4%     ~1%
     av impl.     av impl.
```

---

## Profildetaljer

| Profil | Användningsfall | Huvudmeddelanden |
|--------|-----------------|------------------|
| **Basic** | Enkla taxi-appar | 2000, 2001, 7xxx |
| **Standard** | Standard DRT | + 3xxx, 4010, 6001 |
| **Advanced** | Full klientkontroll | + 6500-6511, nod-för-nod |
| **Session** | Dynamisk ruttning | + 2100-2105, 2040 |
| **Full** | Komplett standard | + 2800, 2900, 8xxx |

---

## Föreslagen filstruktur

```
SUTI-Schema/
│
├── core/
│   ├── SUTI-Core.xsd           # Delade typer
│   ├── SUTI-Enumerations.xsd   # Alla uppräkningar
│   └── SUTI-CommonTypes.xsd    # Återanvändbara typer
│
├── flows/
│   ├── SUTI-Order.xsd          # 2000-2099
│   ├── SUTI-Session.xsd        # 2100-2199
│   ├── SUTI-Dispatch.xsd       # 3000-3099
│   ├── SUTI-TrafficControl.xsd # 4000-4099
│   ├── SUTI-DeliveryNote.xsd   # 6500-6599
│   ├── SUTI-Technical.xsd      # 7000-7199
│   ├── SUTI-Accounting.xsd     # 8000-8199
│   └── ...
│
├── profiles/
│   ├── SUTI-Basic.xsd          # Core + Order
│   ├── SUTI-Standard.xsd       # + Dispatch + Traffic
│   ├── SUTI-Advanced.xsd       # + Delivery
│   ├── SUTI-Session.xsd        # + Session-typer
│   └── SUTI-Full.xsd           # Allt
│
└── SUTI-Complete.xsd           # v1.x-kompatibilitet
```

---

# 4. VÄGEN FRAMÅT FÖR JSON SCHEMA

## Nyckelkrav

```
  ┌─────────────────────────────────────────────────────┐
  │  1. XSD måste förbli BAKÅTKOMPATIBEL                │
  │  2. JSON Schema ska GENERERAS FRÅN XSD              │
  │  3. XSD är den ENDA SANNINGSKÄLLAN                  │
  └─────────────────────────────────────────────────────┘
```

**Konsekvens:** JSON-elementnamn kommer matcha XSD-namn (inte JSON-idiomatiska)

---

## 2021 JSON-arbete: Historisk kontext

År 2021 valdes en annan approach:

> "vi har lämnat iden att utgå ifrån xml schemat"

**2021 skapade handgjord JSON med:**
- JSON-idiomatiska namn (plural, array-suffix)
- Förenklade strukturer
- 11 exempelmeddelanden

**2026 approach skiljer sig:**
- JSON Schema genereras FRÅN XSD
- Namn matchar XSD exakt
- 2021-exempel användbara som TESTFALL, inte mallar

---

## Varför profiler underlättar JSON-generering

```
  NUVARANDE (Monolitisk)        FÖRESLAGEN (Modulär)

  ┌─────────────────┐           ┌─────────────────┐
  │                 │           │   SUTI-Core     │
  │   ENDA XSD      │    →      ├─────────────────┤
  │   3 131 rader   │           │   SUTI-Order    │
  │                 │           ├─────────────────┤
  │   Svårt att     │           │   SUTI-...      │
  │   generera ren  │           └─────────────────┘
  │   JSON          │                    ↓
  └─────────────────┘           ┌─────────────────┐
                                │  JSON Schema    │
                                │  (genererat)    │
                                └─────────────────┘
```

## Fördelar med modulär XSD för JSON-generering

1. **Namngivna typer i XSD** → Återanvändbara `$defs` i JSON Schema
2. **Mindre XSD-moduler** → Renare genererade scheman
3. **Profilbaserad XSD** → Profilbaserad JSON Schema
4. **v1.x bakåtkompatibel** → Säker utvecklingsväg

---

## Strategi för JSON-generering (XSD-först)

```
  Fas 1: Verktyg & Pilot
  ──────────────────────
  Nuvarande XSD → XSD-till-JSON-verktyg → Genererat JSON Schema
                                                ↓
                                Validera mot 2021-exempel


  Fas 2: XSD-förbättringar (v1.x, bakåtkompatibla)
  ────────────────────────────────────────────────
  Extrahera inline-typer → Namngivna typer → Bättre $defs


  Fas 3: Generera per profil
  ──────────────────────────
  SUTI-Core.xsd    →  suti-core.schema.json
  SUTI-Order.xsd   →  suti-order.schema.json
  SUTI-Basic.xsd   →  suti-basic.schema.json (paket)
```

---

## Uppräkningsstrategi för JSON

```xml
<!-- NUVARANDE (XSD) - Dubbel representation -->
<xs:enumeration value="3101"/>
<xs:enumeration value="client"/>
```

```json
// FÖRESLAGEN (JSON Schema) - Endast text
{
  "dispatchResponsible": {
    "type": "string",
    "enum": ["client", "provider", "both"]
  }
}
```

**Migrering:** Behåll numeriska koder i extern mappningstabell

---

# 5. REKOMMENDERAD TIDPLAN

```
  2026                          2027
  ─────────────────────────────────────────────────

  Q1-Q2: v1.x FÖRBÄTTRINGAR (Icke-brytande)
  ├── Fixa kritiska problem (minOccurs, stavfel)
  ├── Extrahera inline-typer
  ├── Komplettera dokumentation
  └── Lägg till varningar för deprecated

  Q3-Q4: v2.0 PLANERING
  ├── Definiera profilkonformitetstester
  ├── Designa modulär struktur
  ├── Feedback från medlemmar
  └── Starta JSON Schema-pilot (kärntyper)

  2027 Q1-Q2: v2.0 RELEASE
  ├── Modulär XSD-struktur
  ├── Profil-XSD-filer
  ├── JSON Schema för Basic/Standard
  └── Migreringsverktyg

  2027 Q3+: v2.x VIDAREUTVECKLING
  ├── Komplett JSON Schema-täckning
  ├── OpenAPI/AsyncAPI-specifikationer
  └── Verktyg och validering
```

---

# 6. DISKUSSIONSPUNKTER

## Frågor till TK

1. **Profilansats:** Är det rimligt att formalisera implicita profiler?

2. **Profilnamn:** Basic/Standard/Advanced/Session/Full - är dessa tydliga?

3. **JSON-prioritet:** Vilka flöden bör få JSON Schema först?
   - Rekommendation: Börja med bulkLocation (redan JSON) + grundläggande ordrar

4. **Uppräkningsstrategi:** Endast text i JSON, behålla numerisk mappning externt?

5. **Tidplan:** Är den föreslagna tidplanen realistisk?

---

## Risker & Åtgärder

| Risk | Åtgärd |
|------|--------|
| Fragmentering mellan profiler | Tydlig uppgraderingsväg, profilkompatibilitetsmatris |
| Importkomplexitet i XSD | Tillhandahåll samlad enfils-version (SUTI-Complete.xsd) |
| JSON/XSD-drift | En sanningskälla, generera JSON från XSD |
| Stöd för äldre system | 12 månaders parallellt stöd |

---

## Sammanfattning av fördelar

| Intressent | Fördel |
|------------|--------|
| **Nya implementerare** | Börja med SUTI-Basic, tydlig inlärningsväg |
| **Befintliga länkar** | Inga brytande ändringar före v2.0, migreringsverktyg |
| **Upphandlare** | Referera till specifika profiler, tydlig konformitet |
| **TK** | Enklare underhåll, parallell utveckling |
| **Verktygsleverantörer** | Mindre scheman, bättre verktygsstöd |

---

# BILAGA: Flödesinventering

## Alla dokumenterade flöden

| Block | Flöde | Meddelanden | Profil |
|-------|-------|-------------|--------|
| 1xxx | Resursutbyte | 1000-1112 | Full |
| 2xxx | Order (grundläggande) | 2000-2099 | Basic+ |
| 2xxx | DriverSession | 2100-2199 | Session |
| 2xxx | Repetitiva ordrar | 2800-2810 | Full |
| 2xxx | Auktorisation | 2900-2902 | Full |
| 3xxx | Dispatch | 3000-3099 | Standard+ |
| 4xxx | Trafikstyrning | 4000-4099 | Standard+ |
| 5xxx | Kommunikation | 5000-5099 | Standard+ |
| 6xxx | Rapporter | 6000-6499 | Standard+ |
| 6xxx | Följesedlar | 6500-6599 | Advanced+ |
| 7xxx | Tekniska | 7000-7199 | Basic+ |
| 8xxx | Redovisning | 8000-8199 | Full |

---

# BILAGA: Profilberoendematris

```
                    Core  Order  Session  Dispatch  Traffic  Report  Delivery  Tech  Accounting  Resource
SUTI-Basic           ✓     ✓                                                    ✓
SUTI-Standard        ✓     ✓               ✓         ✓        ✓                 ✓
SUTI-Advanced        ✓     ✓               ✓         ✓        ✓        ✓        ✓
SUTI-Session         ✓     ✓       ✓       ✓         ✓        ✓                 ✓
SUTI-Full            ✓     ✓       ✓       ✓         ✓        ✓        ✓        ✓      ✓           ✓
```

---

# BILAGA: Relaterade dokument

Tillgängliga i repositoryt `plans/`:

- `json-schema-strategy-2026.md` - Komplett strategidokument
- `xsd-anomalies-for-json.md` - Anomalier att åtgärda
- `profile-based-standard-analysis.md` - Profildetaljer

---

# Tack!

## Nästa steg

1. TK:s feedback på profilansatsen
2. Prioritera startpunkt för JSON Schema
3. Ta fram profilkonformitetskriterier
4. Planera konsultation med medlemmar

**Frågor?**
