# SUTI Schema-modernisering - Sammanfattning på en sida

## Möjligheten

Analys av "How to use SUTI" (170 sidor) visar att **självdeklarationer redan fungerar som implicita profiler**. Vi rekommenderar att formalisera detta till explicita XSD-profiler för att möjliggöra renare JSON Schema-generering.

---

## Förslag: Fem profilnivåer

| Profil | Målgrupp | Innehåll |
|--------|----------|----------|
| **SUTI-Basic** | Enkla taxi-appar | Ordrar (2000/2001), Tekniska (7xxx) |
| **SUTI-Standard** | Standard DRT | + Dispatch (3xxx), Trafikstyrning (4xxx), Rapporter |
| **SUTI-Advanced** | Full klientkontroll | + Nod-för-nod, Följesedlar (6500-6511) |
| **SUTI-Session** | Dynamisk ruttning | + DriverSession (2100-2199), Orderkombinationer |
| **SUTI-Full** | Komplett standard | + Repetitiva ordrar, Flaggstop, Redovisning |

**~80% av implementationerna kan använda SUTI-Basic eller SUTI-Standard**

---

## Varför detta underlättar JSON-generering

| Nuläge | Föreslaget läge |
|--------|-----------------|
| Enda XSD med 3 131 rader | Modulära XSD-filer per flöde |
| Allt-eller-inget | Profilbaserade delmängder |
| Svårt att mappa till JSON | Rent JSON Schema per modul |
| Inga konformitetsnivåer | Tydlig profilkonformitet |

---

## Rekommenderad tidplan

| Fas | Tidplan | Leverabler |
|-----|---------|------------|
| **v1.x Förbättringar** | Q1-Q2 2026 | Fixa problem, extrahera typer, deprecation-varningar |
| **v2.0 Planering** | Q3-Q4 2026 | Profilspecifikationer, JSON Schema-pilot (kärntyper) |
| **v2.0 Release** | Q1-Q2 2027 | Modulär XSD, Profilfiler, JSON Schema Basic/Standard |
| **v2.x Vidareutveckling** | Q3+ 2027 | Full JSON-täckning, OpenAPI-specifikationer |

---

## Huvudsakliga fördelar

- **Nya implementerare:** Börja smått med SUTI-Basic
- **Upphandlingar:** Referera till specifik profilkonformitet
- **JSON-övergång:** Generera schema per modul, inte monolitiskt
- **Bakåtkompatibilitet:** SUTI-Complete.xsd bibehåller v1.x-kompatibilitet

---

## Frågor till TK

1. Är det rimligt att formalisera implicita profiler till explicita XSD-profiler?
2. Vilka flöden bör få JSON Schema först? (Rekommendation: bulkLocation + grundläggande ordrar)
3. Är den föreslagna tidplanen realistisk?

---

*Fullständig analys: `plans/json-schema-strategy-2026.md`*
*Anomalier: `plans/xsd-anomalies-for-json.md`*
*Presentation: `plans/TC-presentation-json-generation-sv.md`*
