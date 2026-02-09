# Vad betyder JSON-idiomatisk?

**JSON-idiomatisk** betyder att följa de konventioner och mönster som är naturliga och förväntade i JSON-världen, till skillnad från hur XML typiskt struktureras.

---

## Konkreta exempel

| Aspekt | XML-stil (XSD) | JSON-idiomatisk |
|--------|----------------|-----------------|
| **Array-namn** | `<formOfPayment>` (singular, upprepas) | `"payments": [...]` (plural) |
| **Nesting** | Djupt nästlat med wrapper-element | Plattare struktur |
| **Attribut** | `<node id="123" name="...">` | `{"id": "123", "name": "..."}` |
| **Enums** | Numeriska koder `"3101"` | Läsbara strängar `"client"` |
| **Tomma värden** | Element utelämnas eller `xsi:nil` | `null` eller utelämna |

---

## Från SUTI-exemplen

**XSD-stil:**
```xml
<formOfPayment>
  <payment amount="0" paymentType="prepaidsocialfee"/>
</formOfPayment>
```

**JSON-idiomatisk (2021-exemplen):**
```json
"payments": [
  { "amount": 0, "paymentType": "prepaidsocialfee" }
]
```

---

## Varför det spelar roll

JSON-utvecklare förväntar sig:
- **Pluralform** för arrayer (`users`, inte `user`)
- **camelCase** för properties
- **Läsbara värden** istället för koder
- **Enklare strukturer** utan onödig nesting

Om JSON Schema slaviskt följer XSD-strukturen blir JSON:et "XML i JSON-kläder" - tekniskt korrekt men klumpigt att arbeta med.

---

## Se även

- [JSON Schema Strategy 2026](json-schema-strategy-2026.md)
- [XSD-anomalier för JSON](xsd-anomalies-for-json.md)
