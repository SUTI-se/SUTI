# XSD to JSON Schema Gap Matrix

Purpose: Formal tracking matrix for alignment where XSD is master.

Status values:
- exact: equivalent coverage
- renamed: semantic match but naming/path differs
- narrowed: JSON accepts fewer values/shapes than XSD
- missing: no equivalent coverage in JSON

Recommended action values:
- add
- broaden enum
- rename alias
- adjust requiredness

| # | XSD path | JSON path | Status | Recommended action | Progress | Action taken |
|---:|---|---|---|---|---|---|
| 1 | `/xs:schema/xs:complexType[@name='idType']` | `#/$defs/id` | renamed | rename alias | done | kept current setup (no schema change) |
| 2 | `/xs:schema/xs:complexType[@name='orgType']` | `#/$defs/org` | renamed | rename alias | done | kept current setup (no schema change) |
| 3 | `/xs:schema/xs:complexType[@name='referencesTo']` | `#/$defs/referenceToMsg` | narrowed | add | done | extended referenceToMsg with additional XSD references and support defs (idMsgRef, idOrderForwardRef) |
| 4 | `/xs:schema/xs:complexType[@name='referencesTo']/xs:sequence/xs:element[@name='idDriverSession']` | `#/$defs/referenceToMsg/properties/idDriverSession` | exact | add | done | covered via row 3 referenceToMsg extension |
| 5 | `/xs:schema/xs:complexType[@name='referencesTo']/xs:sequence/xs:element[@name='idVehicle']` | `#/$defs/referenceToMsg/properties/idVehicle` | exact | add | done | covered via row 3 referenceToMsg extension |
| 6 | `/xs:schema/xs:complexType[@name='referencesTo']/xs:sequence/xs:element[@name='idDriver']` | `#/$defs/referenceToMsg/properties/idDriver` | exact | add | done | covered via row 3 referenceToMsg extension |
| 7 | `/xs:schema/xs:complexType[@name='referencesTo']/xs:sequence/xs:element[@name='idSuborder']` | `#/$defs/referenceToMsg/properties/idSuborder` | exact | add | done | covered via row 3 referenceToMsg extension |
| 8 | `/xs:schema/xs:complexType[@name='referencesTo']/xs:sequence/xs:element[@name='idPassword']` | `#/$defs/referenceToMsg/properties/idPassword` | exact | add | done | covered via row 3 referenceToMsg extension |
| 9 | `/xs:schema/xs:complexType[@name='referencesTo']/xs:sequence/xs:element[@name='idRejectReason']` | `#/$defs/referenceToMsg/properties/idRejectReason` | exact | add | done | covered via row 3 referenceToMsg extension |
| 10 | `/xs:schema/xs:complexType[@name='referencesTo']/xs:sequence/xs:element[@name='idReceipt']` | `#/$defs/referenceToMsg/properties/idReceipt` | exact | add | done | covered via row 3 referenceToMsg extension |
| 11 | `/xs:schema/xs:complexType[@name='referencesTo']/xs:sequence/xs:element[@name='idAuthorization']` | `#/$defs/referenceToMsg/properties/idAuthorization` | exact | add | done | covered via row 3 referenceToMsg extension |
| 12 | `/xs:schema/xs:complexType[@name='referencesTo']/xs:sequence/xs:element[@name='idOrderTemplate']` | `#/$defs/referenceToMsg/properties/idOrderTemplate` | exact | add | done | covered via row 3 referenceToMsg extension |
| 13 | `/xs:schema/xs:complexType[@name='referencesTo']/xs:sequence/xs:element[@name='idResponse']` | `#/$defs/referenceToMsg/properties/idResponse` | exact | add | done | covered via row 3 referenceToMsg extension |
| 14 | `/xs:schema/xs:complexType[@name='referencesTo']/xs:sequence/xs:element[@name='idOrderForward']` | `#/$defs/referenceToMsg/properties/idOrderForward` | exact | add | done | covered via row 3 referenceToMsg extension (idOrderForwardRef) |
| 15 | `/xs:schema/xs:complexType[@name='referencesTo']/xs:sequence/xs:element[@name='idRunoffGroup']` | `#/$defs/referenceToMsg/properties/idRunoffGroup` | exact | add | done | covered via row 3 referenceToMsg extension |
| 16 | `/xs:schema/xs:complexType[@name='process']/xs:attribute[@name='report' and @use='required']` | `#/$defs/process/properties/report` | narrowed | adjust requiredness | not-started | none yet |
| 17 | `/xs:schema/xs:complexType[@name='process']/xs:attribute[@name='preorderedVehicle' and @use='required']` | `#/$defs/process/properties/preorderedVehicle` | narrowed | adjust requiredness | not-started | none yet |
| 18 | `/xs:schema/xs:complexType[@name='process']/xs:attribute[@name='allowRouting' and @use='required']` | `#/$defs/process/properties/allowRouting` | exact | add | done | kept current setup (no schema change) |
| 19 | `/xs:schema/xs:complexType[@name='process']/xs:attribute[@name='pickupconfirmation']` | `#/$defs/process/properties/pickupConfirmation` | renamed | rename alias | done | kept name pickupConfirmation and broadened enum with numeric codes; used lowercase notrequested for XML->JSON compatibility |
| 20 | `/xs:schema/xs:complexType[@name='process']/xs:attribute[@name='preeOrder']` | `#/$defs/process/properties/preOrder` | renamed | rename alias | done | kept JSON preOrder as canonical; treated XSD preeOrder as spelling mistake |
| 21 | `/xs:schema/xs:complexType[@name='nodeprocess']/xs:attribute[@name='sendinformationDisptch']` | `#/$defs/nodeProcess/properties/sendInformationDispatch` | renamed | rename alias | done | kept corrected JSON names; broadened sendInformation enums with XSD numeric/lowercase aliases for compatibility |
| 22 | `/xs:schema/xs:complexType[@name='geographicLocation']/xs:attribute[@name='zone']` | `#/$defs/geographicLocation/properties/zone` | exact | add | done | added optional geographicLocation.zone for XSD parity |
| 23 | `/xs:schema/xs:complexType[@name='geographicLocation']/xs:attribute[@name='typeOfCoordinate']/xs:simpleType/xs:restriction/xs:enumeration[@value='3301']` | `#/$defs/geographicLocation/properties/typeOfCoordinate` | exact | broaden enum | done | broadened typeOfCoordinate enum to include XSD aliases 3301/WGS84/3302 |
| 24 | `/xs:schema/xs:complexType[@name='geographicLocation']/xs:attribute[@name='typeOfCoordinate']/xs:simpleType/xs:restriction/xs:enumeration[@value='WGS84']` | `#/$defs/geographicLocation/properties/typeOfCoordinate` | exact | broaden enum | done | broadened typeOfCoordinate enum to include XSD aliases 3301/WGS84/3302 |
| 25 | `/xs:schema/xs:complexType[@name='geographicLocation']/xs:attribute[@name='typeOfCoordinate']/xs:simpleType/xs:restriction/xs:enumeration[@value='3302']` | `#/$defs/geographicLocation/properties/typeOfCoordinate` | exact | broaden enum | done | broadened typeOfCoordinate enum to include XSD aliases 3301/WGS84/3302 |
| 26 | `/xs:schema/xs:complexType[@name='geographicLocation']/xs:attribute[@name='long']` | `#/$defs/geographicLocation/properties/lon` | renamed | rename alias | done | kept as is; no schema change |
| 27 | `/xs:schema/xs:complexType[@name='geographicLocation']/xs:attribute[@name='precision' and @use='required']` | `#/$defs/geographicLocation/properties/precision` | exact | adjust requiredness | done | required precision in geographicLocation to align with XSD |
| 28 | `/xs:schema/xs:complexType[@name='geographicLocation']/xs:attribute[@name='speed']` | `#/$defs/geographicLocation/properties/speed` | exact | add | done | added optional geographicLocation.speed |
| 29 | `/xs:schema/xs:complexType[@name='geographicLocation']/xs:attribute[@name='speedSource']` | `#/$defs/geographicLocation/properties/speedSource` | exact | add | done | added optional geographicLocation.speedSource with XSD enum aliases |
| 30 | `/xs:schema/xs:complexType[@name='geographicLocation']/xs:attribute[@name='direction']` | `#/$defs/geographicLocation/properties/direction` | exact | add | done | added optional geographicLocation.direction |
| 31 | `/xs:schema/xs:complexType[@name='geographicLocation']/xs:attribute[@name='height']` | `#/$defs/geographicLocation/properties/height` | exact | add | done | added optional geographicLocation.height |
| 32 | `/xs:schema/xs:complexType[@name='geographicLocation']/xs:attribute[@name='deviationSpeed']` | `#/$defs/geographicLocation/properties/deviationSpeed` | exact | add | done | added optional geographicLocation.deviationSpeed |
| 33 | `/xs:schema/xs:complexType[@name='addressType']/xs:attribute[@name='mapPage']` | `#/$defs/address/properties/mapPage` | exact | add | done | added optional address.mapPage |
| 34 | `/xs:schema/xs:complexType[@name='addressType']/xs:sequence/xs:element[@name='idMap']` | `#/$defs/address/properties/idMap` | exact | add | done | added optional address.idMap as array of id |
| 35 | `/xs:schema/xs:complexType[@name='content']/xs:attribute[@name='contentType']/xs:simpleType/xs:restriction/xs:enumeration[@value='action']` | `#/$defs/content/properties/contentType` | exact | broaden enum | done | added `action` to contentType enum |
| 36 | `/xs:schema/xs:complexType[@name='content']/xs:attribute[@name='contentType']/xs:simpleType/xs:restriction/xs:enumeration[@value='navigation']` | `#/$defs/content/properties/contentType` | exact | broaden enum | done | added `navigation` to contentType enum |
| 37 | `/xs:schema/xs:complexType[@name='content']/xs:attribute[@name='contentType']/xs:simpleType/xs:restriction/xs:enumeration[@value='companion']` | `#/$defs/content/properties/contentType` | exact | broaden enum | done | added `companion` to contentType enum |
| 38 | `/xs:schema/xs:complexType[@name='content']/xs:attribute[@name='contentType']/xs:simpleType/xs:restriction/xs:enumeration[@value='coTraveller']` | `#/$defs/content/properties/contentType` | exact | broaden enum | done | added `coTraveller` to contentType enum |
| 39 | `/xs:schema/xs:complexType[@name='content']/xs:attribute[@name='contentType']/xs:simpleType/xs:restriction/xs:enumeration[@value='child']` | `#/$defs/content/properties/contentType` | exact | broaden enum | done | added `child` to contentType enum |
| 40 | `/xs:schema/xs:complexType[@name='content']/xs:attribute[@name='contentType']/xs:simpleType/xs:restriction/xs:enumeration[@value='animal']` | `#/$defs/content/properties/contentType` | exact | broaden enum | done | added `animal` to contentType enum |
| 41 | `/xs:schema/xs:complexType[@name='content']/xs:attribute[@name='name' and @use='required']` | `#/$defs/content/properties/name` | narrowed | adjust requiredness | not-started | none yet |
| 42 | `/xs:schema/xs:complexType[@name='content']/xs:attribute[@name='maxTravelDuration']` | `#/$defs/content/properties/maxTravelDuration` | exact | add | done | added open any-simple-style field (`string|number|integer|boolean|null`) |
| 43 | `/xs:schema/xs:complexType[@name='content']/xs:attribute[@name='gender']` | `#/$defs/content/properties/gender` | exact | add | done | added optional gender enum (`female|male|child`) |
| 44 | `/xs:schema/xs:complexType[@name='content']/xs:sequence/xs:element[@name='connection']` | `#/$defs/content/properties/connection` | exact | add | done | added content.connection with new `connection` and `associatedReservation` defs (required fields + enums aligned) |
| 45 | `/xs:schema/xs:complexType[@name='content']/xs:sequence/xs:element[@name='productContent']` | `#/$defs/content/properties/product` | exact | add | done | added optional canonical JSON field `product` mapped to `#/$defs/product` |
| 46 | `/xs:schema/xs:complexType[@name='contactInfo']/xs:attribute[@name='contactInfo']` | `#/$defs/contactInfo/properties/contactValue` | renamed | rename alias | not-started | none yet |
| 47 | `/xs:schema/xs:complexType[@name='contactInfo']/xs:attribute[@name='contactType']/xs:simpleType/xs:restriction/xs:enumeration[@value='mail']` | `#/$defs/contactInfo/properties/contactType` | exact | broaden enum | done | replaced contactType enum with XSD-compatible set (`2201/mail/2202/phone/2203/fax/2204/otherInfo/2205/sms/2206/bookingagent/2207/web`) |
| 48 | `/xs:schema/xs:complexType[@name='contactInfo']/xs:attribute[@name='contactType']/xs:simpleType/xs:restriction/xs:enumeration[@value='otherInfo']` | `#/$defs/contactInfo/properties/contactType` | exact | broaden enum | done | covered by broadened contactType enum |
| 49 | `/xs:schema/xs:complexType[@name='contactInfo']/xs:attribute[@name='contactType']/xs:simpleType/xs:restriction/xs:enumeration[@value='bookingagent']` | `#/$defs/contactInfo/properties/contactType` | exact | broaden enum | done | covered by broadened contactType enum |
| 50 | `/xs:schema/xs:complexType[@name='contactInfo']/xs:attribute[@name='contactType']/xs:simpleType/xs:restriction/xs:enumeration[@value='web']` | `#/$defs/contactInfo/properties/contactType` | exact | broaden enum | done | covered by broadened contactType enum |
| 51 | `/xs:schema/xs:complexType[@name='time']/xs:attribute[@name='timeType' and @use='optional']` | `#/$defs/time/required` | exact | adjust requiredness | done | removed `timeType` from required; only `time` remains required |
| 52 | `/xs:schema/xs:complexType[@name='time']/xs:attribute[@name='timeAccuracy']` | `#/$defs/time/properties/timeAccuracy` | exact | add | done | added optional `timeAccuracy` as string |
| 53 | `/xs:schema/xs:complexType[@name='time']/xs:attribute[@name='timeZone']` | `#/$defs/time/properties/timeZone` | exact | add | done | added optional `timeZone` as integer |
| 54 | `/xs:schema/xs:complexType[@name='resourceType']` | `#/$defs/resource` | exact | add | done | expanded resource with missing XSD-mapped fields while keeping canonical JSON naming |
| 55 | `/xs:schema/xs:complexType[@name='resourceType']/xs:sequence/xs:element[@name='manualDescriptionResource']` | `#/$defs/resource/properties/manualDescriptionResource` | exact | add | done | added optional manualDescriptionResource array |
| 56 | `/xs:schema/xs:complexType[@name='resourceType']/xs:sequence/xs:element[@name='idOrg']` | `#/$defs/resource/properties/idOrg` | exact | add | done | added optional idOrg |
| 57 | `/xs:schema/xs:complexType[@name='resourceType']/xs:sequence/xs:element[@name='vehiclestartLocation']` | `#/$defs/resource/properties/startLocation` | renamed | rename alias | done | kept canonical startLocation and intentionally did not add vehiclestartLocation alias |
| 58 | `/xs:schema/xs:complexType[@name='resourceType']/xs:sequence/xs:element[@name='resourceTime']` | `#/$defs/resource/properties/resourceTime` | exact | add | done | added optional resourceTime as array of time |
| 59 | `/xs:schema/xs:complexType[@name='resourceType']/xs:sequence/xs:element[@name='resourceValidation']` | `#/$defs/resource/properties/resourceValidation` | exact | add | done | added optional resourceValidation array with XSD validation fields/enums |
| 60 | `/xs:schema/xs:complexType[@name='resourceType']/xs:attribute[@name='MethodDispatch']` | `#/$defs/resource/properties/MethodDispatch` | exact | add | done | added optional MethodDispatch enum (`normal|change`) |
| 61 | `/xs:schema/xs:complexType[@name='vehicle']/xs:attribute[@name='noOfVehicle']` | `#/$defs/vehicleResource/properties/noOfVehicle` | exact | add | done | added optional noOfVehicle as integer with minimum 1 |
| 62 | `/xs:schema/xs:complexType[@name='vehicle']/xs:attribute[@name='taximeterType']` | `#/$defs/vehicleResource/properties/taximeterType` | exact | add | done | added optional taximeterType as string |
| 63 | `/xs:schema/xs:complexType[@name='vehicle']/xs:attribute[@name='taximeterSoftware']` | `#/$defs/vehicleResource/properties/taximeterSoftware` | exact | add | done | added optional taximeterSoftware as string |
| 64 | `/xs:schema/xs:complexType[@name='vehicle']/xs:attribute[@name='vehicleLink']` | `#/$defs/vehicleResource/properties/vehicleLink` | exact | add | done | added optional vehicleLink as open any-simple-style value |
| 65 | `/xs:schema/xs:complexType[@name='vehicle']/xs:sequence/xs:element[@name='environmentalinfoVehicle']` | `#/$defs/vehicleResource/properties/environmentalinfoVehicle` | exact | add | done | added environmentalinfoVehicle mapped to new environmentalInformation defs |
| 66 | `/xs:schema/xs:complexType[@name='vehicle']/xs:sequence/xs:element[@name='ratingsVehicle']` | `#/$defs/vehicleResource/properties/ratingsVehicle` | exact | add | done | added ratingsVehicle mapped to new ratingType def |
| 67 | `/xs:schema/xs:complexType[@name='vehicle']/xs:sequence/xs:element[@name='descriptionVehicle']` | `#/$defs/vehicleResource/properties/descriptionVehicle` | exact | add | done | added descriptionVehicle mapped to vehicleDescription def |
| 68 | `/xs:schema/xs:complexType[@name='capacity']/xs:sequence/xs:element[@name='luggage']` | `#/$defs/capacity/properties/luggage` | exact | add | done | added luggage array with luggageType/pcs |
| 69 | `/xs:schema/xs:complexType[@name='capacity']/xs:attribute[@name='luggageArea']` | `#/$defs/capacity/properties/luggageArea` | exact | add | done | added luggageArea as number |
| 70 | `/xs:schema/xs:complexType[@name='capacity']/xs:attribute[@name='fullArea']` | `#/$defs/capacity/properties/fullArea` | exact | add | done | added fullArea as number |
| 71 | `/xs:schema/xs:complexType[@name='capacity']/xs:attribute[@name='stretcherArea']` | `#/$defs/capacity/properties/stretcherArea` | exact | add | done | added stretcherArea as number |
| 72 | `/xs:schema/xs:complexType[@name='seats']/xs:attribute[@name='noOfSeatsMax']` | `#/$defs/capacityItem/properties/noOfSeatsMax` | exact | add | done | added noOfSeatsMax as non-negative integer |
| 73 | `/xs:schema/xs:complexType[@name='seats']/xs:sequence/xs:element[@name='position']` | `#/$defs/capacityItem/properties/position` | exact | add | done | added position array on seat-like capacity item |
| 74 | `/xs:schema/xs:complexType[@name='position']` | `#/$defs/position` | exact | add | done | added position def with row/seat/direction/legSpace/access |
| 75 | `/xs:schema/xs:complexType[@name='attributesType']` | `#/$defs/attributesType` | exact | add | done | added attributesType def with attribute array |
| 76 | `/xs:schema/xs:complexType[@name='attribute']` | `#/$defs/attribute` | exact | add | done | added attribute def with required idAttribute |
| 77 | `/xs:schema/xs:complexType[@name='manualDescriptionType']` | `#/$defs/manualDescription` | narrowed | add | not-started | none yet |
| 78 | `/xs:schema/xs:complexType[@name='driver']` | `#/$defs/driverResource` | narrowed | add | not-started | none yet |
| 79 | `/xs:schema/xs:complexType[@name='timesType']` | *(none)* | missing | add | not-started | none yet |
| 80 | `/xs:schema/xs:complexType[@name='date']` | *(none)* | missing | add | not-started | none yet |
| 81 | `/xs:schema/xs:complexType[@name='contents']` | *(none)* | missing | add | not-started | none yet |
| 82 | `/xs:schema/xs:complexType[@name='connection']` | *(none)* | missing | add | not-started | none yet |
| 83 | `/xs:schema/xs:complexType[@name='associatedReservation']` | *(none)* | missing | add | not-started | none yet |
| 84 | `/xs:schema/xs:complexType[@name='contactInfosType']` | *(none)* | missing | add | not-started | none yet |
| 85 | `/xs:schema/xs:complexType[@name='pickupConfirmation']` | *(none)* | missing | add | not-started | none yet |
| 86 | `/xs:schema/xs:complexType[@name='subOrderType']` | `#/$defs/subOrder` | renamed | rename alias | not-started | none yet |
| 87 | `/xs:schema/xs:complexType[@name='eventType']` | *(none)* | missing | add | not-started | none yet |
| 88 | `/xs:schema/xs:complexType[@name='eventReport']` | *(none)* | missing | add | not-started | none yet |
| 89 | `/xs:schema/xs:complexType[@name='orderLink']` | *(none)* | missing | add | not-started | none yet |
| 90 | `/xs:schema/xs:complexType[@name='authorizationAcceptType']` | *(none)* | missing | add | not-started | none yet |
| 91 | `/xs:schema/xs:complexType[@name='amountType']` | `#/$defs/amount` | renamed | rename alias | not-started | none yet |
| 92 | `/xs:schema/xs:complexType[@name='restrictionsType']` | *(none)* | missing | add | not-started | none yet |
| 93 | `/xs:schema/xs:complexType[@name='vatAmountSpecificationType']` | *(none)* | missing | add | not-started | none yet |
| 94 | `/xs:schema/xs:complexType[@name='nodeCancelationType']` | `#/$defs/nodeCancellation` | renamed | rename alias | not-started | none yet |
| 95 | `/xs:schema/xs:complexType[@name='nodeCancellationType']` | `#/$defs/nodeCancellation` | renamed | rename alias | not-started | none yet |
| 96 | `/xs:schema/xs:complexType[@name='vehicleDistance']` | *(none)* | missing | add | not-started | none yet |
| 97 | `/xs:schema/xs:complexType[@name='calendarType']` | `#/$defs/calendar` | renamed | rename alias | not-started | none yet |
| 98 | `/xs:schema/xs:complexType[@name='weekdaysType']` | `#/$defs/weekdays` | renamed | rename alias | not-started | none yet |
| 99 | `/xs:schema/xs:complexType[@name='requestContentType']` | *(none)* | missing | add | not-started | none yet |
| 100 | `/xs:schema/xs:complexType[@name='suborderTourType']` | *(none)* | missing | add | not-started | none yet |
| 101 | `/xs:schema/xs:complexType[@name='calculationFareType']` | *(none)* | missing | add | not-started | none yet |
| 102 | `/xs:schema/xs:complexType[@name='organizationType']` | `#/$defs/organization` | renamed | rename alias | not-started | none yet |
| 103 | `/xs:schema/xs:complexType[@name='orgPaymentType']` | `#/$defs/orgPayment` | renamed | rename alias | not-started | none yet |
| 104 | `/xs:schema/xs:complexType[@name='gpsType']` | *(none)* | missing | add | not-started | none yet |
| 105 | `/xs:schema/xs:complexType[@name='errorType']` | *(none)* | missing | add | not-started | none yet |
| 106 | `/xs:schema/xs:complexType[@name='environmentalInformation']` | *(none)* | missing | add | not-started | none yet |
| 107 | `/xs:schema/xs:complexType[@name='orders']` | *(none)* | missing | add | not-started | none yet |
| 108 | `/xs:schema/xs:complexType[@name='changelog']` | *(none)* | missing | add | not-started | none yet |
| 109 | `/xs:schema/xs:complexType[@name='log']` | *(none)* | missing | add | not-started | none yet |
| 110 | `/xs:schema/xs:complexType[@name='sessionNode']` | *(none)* | missing | add | not-started | none yet |
| 111 | `/xs:schema/xs:complexType[@name='ratingType']` | *(none)* | missing | add | not-started | none yet |
| 112 | `/xs:schema/xs:complexType[@name='ratingIdType']` | *(none)* | missing | add | not-started | none yet |
| 113 | `/xs:schema/xs:complexType[@name='Validation']` | *(none)* | missing | add | not-started | none yet |

## Notes

- This matrix is intentionally conservative: where no direct JSON path is present, status is `missing` even if semantics might be partially flattened elsewhere.
- Rows marked `renamed` still require an explicit aliasing strategy if strict XSD-to-JSON parity is a requirement.
- Rows marked `narrowed` indicate JSON currently rejects some XSD-valid payloads.