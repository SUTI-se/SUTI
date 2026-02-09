# SUTI XSD Type Dependency Analysis

**Generated:** 2026-01-30

---

## Type Dependency Overview

**Total Complex Types:** 86
**Types with Dependencies:** 70
**Isolated Types:** 16

## Key Type Dependencies

### msg

**Line:** 147

**Direct Dependencies (40):**

- `addressType` (line 1798)
- `agreement` (line 137)
- `authorizationAcceptType` (line 2423)
- `bulkLocationList` (line 3047)
- `calculationFareType` (line 2671)
- `calendarType` (line 2588)
- `cancellationConsequence` (line 2167)
- `contactInfosType` (line 2096)
- `date` (line 1792)
- `deliveryNote` (line 2472)
- `driverSession` (line 2898)
- `driverSessionReject` (line 2991)
- `economyReport` (line 2362)
- `errorType` (line 2804)
- `geographicLocation` (line 1881)
- `idType` (line 4)
- `locationRequest` (line 2397)
- `manualDescriptionType` (line 1580)
- `node` (line 1658)
- `nodeCancelationType` (line 2507)
- `nodeCancellationType` (line 2519)
- `order` (line 853)
- `orderLink` (line 2380)
- `orderReject` (line 2137)
- `orderReport` (line 2257)
- `organizationType` (line 2714)
- `pickupConfirmation` (line 2185)
- `price` (line 1131)
- `product` (line 876)
- `providerorderUpdate` (line 2810)
- `ratingType` (line 3082)
- `referencesTo` (line 733)
- `requestContentType` (line 2631)
- `resourceType` (line 1324)
- `route` (line 1650)
- `suborderTourType` (line 2656)
- `summaryReport` (line 2334)
- `time` (line 1742)
- `timesType` (line 1734)
- `weekdaysType` (line 2622)

### order

**Line:** 853

**Direct Dependencies (8):**

- `agreement` (line 137)
- `economyType` (line 1061)
- `idType` (line 4)
- `orderStatus` (line 2937)
- `orgType` (line 120)
- `process` (line 885)
- `resourceType` (line 1324)
- `route` (line 1650)

### driverSession

**Line:** 2898

**Direct Dependencies (6):**

- `changelog` (line 2964)
- `idType` (line 4)
- `orders` (line 2932)
- `process` (line 885)
- `resourceType` (line 1324)
- `sessionNode` (line 3018)

### referencesTo

**Line:** 733

**Direct Dependencies (3):**

- `idMsgRef` (line 30)
- `idType` (line 4)
- `orgType` (line 120)

### route

**Line:** 1650

**Direct Dependencies (1):**

- `node` (line 1658)

### node

**Line:** 1658

**Direct Dependencies (4):**

- `addressType` (line 1798)
- `contents` (line 1961)
- `nodeprocess` (line 999)
- `timesType` (line 1734)

### resourceType

**Line:** 1324

**Direct Dependencies (7):**

- `Validation` (line 3102)
- `driver` (line 1633)
- `geographicLocation` (line 1881)
- `idType` (line 4)
- `manualDescriptionType` (line 1580)
- `timesType` (line 1734)
- `vehicle` (line 1365)

## Dependency Clusters

Types reachable from key domain types (including transitive dependencies):

### msg Cluster

**Total types in cluster:** 82

**Sample types:**

- `Validation` (line 3102)
- `addressType` (line 1798)
- `agreement` (line 137)
- `amountType` (line 2434)
- `associatedReservation` (line 2084)
- `attribute` (line 1567)
- `attributesType` (line 1559)
- `authorizationAcceptType` (line 2423)
- `bulkLocationList` (line 3047)
- `calculationFareType` (line 2671)
- `calendarType` (line 2588)
- `cancellationConsequence` (line 2167)
- `capacity` (line 1432)
- `changelog` (line 2964)
- `connection` (line 2046)
- `contactInfo` (line 2104)
- `contactInfosType` (line 2096)
- `content` (line 1969)
- `contents` (line 1961)
- `date` (line 1792)
- ... and 62 more

### driverSession Cluster

**Total types in cluster:** 52

**Sample types:**

- `Validation` (line 3102)
- `addressType` (line 1798)
- `agreement` (line 137)
- `amountType` (line 2434)
- `associatedReservation` (line 2084)
- `attribute` (line 1567)
- `attributesType` (line 1559)
- `capacity` (line 1432)
- `changelog` (line 2964)
- `connection` (line 2046)
- `contactInfo` (line 2104)
- `contactInfosType` (line 2096)
- `content` (line 1969)
- `contents` (line 1961)
- `driver` (line 1633)
- `driverSession` (line 2898)
- `economyType` (line 1061)
- `environmentalInformation` (line 2835)
- `exchangeRates` (line 1298)
- `exhangeRate` (line 1306)
- ... and 32 more

### order Cluster

**Total types in cluster:** 47

**Sample types:**

- `Validation` (line 3102)
- `addressType` (line 1798)
- `agreement` (line 137)
- `amountType` (line 2434)
- `associatedReservation` (line 2084)
- `attribute` (line 1567)
- `attributesType` (line 1559)
- `capacity` (line 1432)
- `connection` (line 2046)
- `contactInfo` (line 2104)
- `contactInfosType` (line 2096)
- `content` (line 1969)
- `contents` (line 1961)
- `driver` (line 1633)
- `economyType` (line 1061)
- `environmentalInformation` (line 2835)
- `exchangeRates` (line 1298)
- `exhangeRate` (line 1306)
- `formOfPayment` (line 1213)
- `geographicLocation` (line 1881)
- ... and 27 more

### route Cluster

**Total types in cluster:** 42

**Sample types:**

- `Validation` (line 3102)
- `addressType` (line 1798)
- `amountType` (line 2434)
- `associatedReservation` (line 2084)
- `attribute` (line 1567)
- `attributesType` (line 1559)
- `capacity` (line 1432)
- `connection` (line 2046)
- `contactInfo` (line 2104)
- `contactInfosType` (line 2096)
- `content` (line 1969)
- `contents` (line 1961)
- `driver` (line 1633)
- `economyType` (line 1061)
- `environmentalInformation` (line 2835)
- `exchangeRates` (line 1298)
- `exhangeRate` (line 1306)
- `formOfPayment` (line 1213)
- `geographicLocation` (line 1881)
- `idEkInfo` (line 46)
- ... and 22 more

### node Cluster

**Total types in cluster:** 41

**Sample types:**

- `Validation` (line 3102)
- `addressType` (line 1798)
- `amountType` (line 2434)
- `associatedReservation` (line 2084)
- `attribute` (line 1567)
- `attributesType` (line 1559)
- `capacity` (line 1432)
- `connection` (line 2046)
- `contactInfo` (line 2104)
- `contactInfosType` (line 2096)
- `content` (line 1969)
- `contents` (line 1961)
- `driver` (line 1633)
- `economyType` (line 1061)
- `environmentalInformation` (line 2835)
- `exchangeRates` (line 1298)
- `exhangeRate` (line 1306)
- `formOfPayment` (line 1213)
- `geographicLocation` (line 1881)
- `idEkInfo` (line 46)
- ... and 21 more

### content Cluster

**Total types in cluster:** 38

**Sample types:**

- `Validation` (line 3102)
- `addressType` (line 1798)
- `amountType` (line 2434)
- `associatedReservation` (line 2084)
- `attribute` (line 1567)
- `attributesType` (line 1559)
- `capacity` (line 1432)
- `connection` (line 2046)
- `contactInfo` (line 2104)
- `contactInfosType` (line 2096)
- `content` (line 1969)
- `driver` (line 1633)
- `economyType` (line 1061)
- `environmentalInformation` (line 2835)
- `exchangeRates` (line 1298)
- `exhangeRate` (line 1306)
- `formOfPayment` (line 1213)
- `geographicLocation` (line 1881)
- `idEkInfo` (line 46)
- `idType` (line 4)
- ... and 18 more

### resourceType Cluster

**Total types in cluster:** 20

**All types:**

- `Validation` (line 3102)
- `attribute` (line 1567)
- `attributesType` (line 1559)
- `capacity` (line 1432)
- `contactInfo` (line 2104)
- `contactInfosType` (line 2096)
- `driver` (line 1633)
- `environmentalInformation` (line 2835)
- `geographicLocation` (line 1881)
- `idType` (line 4)
- `manualDescriptionType` (line 1580)
- `position` (line 1511)
- `ratingIdType` (line 3095)
- `ratingType` (line 3082)
- `resourceType` (line 1324)
- `seats` (line 1484)
- `time` (line 1742)
- `timesType` (line 1734)
- `vehicle` (line 1365)
- `vehicleDistance` (line 2555)

### economyType Cluster

**Total types in cluster:** 15

**All types:**

- `amountType` (line 2434)
- `economyType` (line 1061)
- `exchangeRates` (line 1298)
- `exhangeRate` (line 1306)
- `formOfPayment` (line 1213)
- `idEkInfo` (line 46)
- `idType` (line 4)
- `manualDescriptionType` (line 1580)
- `payment` (line 1229)
- `price` (line 1131)
- `priceCalculation` (line 1091)
- `taxiMeter` (line 1072)
- `time` (line 1742)
- `timesType` (line 1734)
- `vatAmountSpecificationType` (line 2496)

### referencesTo Cluster

**Total types in cluster:** 4

**All types:**

- `idMsgRef` (line 30)
- `idType` (line 4)
- `orgType` (line 120)
- `referencesTo` (line 733)

## Shared Type Analysis

### Types Used by 3+ Key Types (46)

These are truly shared infrastructure types:

- `idType` (line 4)
  - Used by: content, driverSession, economyType, msg, node, order, referencesTo, resourceType, route
- `manualDescriptionType` (line 1580)
  - Used by: content, driverSession, economyType, msg, node, order, resourceType, route
- `time` (line 1742)
  - Used by: content, driverSession, economyType, msg, node, order, resourceType, route
- `timesType` (line 1734)
  - Used by: content, driverSession, economyType, msg, node, order, resourceType, route
- `orgType` (line 120)
  - Used by: content, driverSession, msg, node, order, referencesTo, route
- `vatAmountSpecificationType` (line 2496)
  - Used by: content, driverSession, economyType, msg, node, order, route
- `geographicLocation` (line 1881)
  - Used by: content, driverSession, msg, node, order, resourceType, route
- `payment` (line 1229)
  - Used by: content, driverSession, economyType, msg, node, order, route
- `capacity` (line 1432)
  - Used by: content, driverSession, msg, node, order, resourceType, route
- `Validation` (line 3102)
  - Used by: content, driverSession, msg, node, order, resourceType, route
- `exhangeRate` (line 1306)
  - Used by: content, driverSession, economyType, msg, node, order, route
- `position` (line 1511)
  - Used by: content, driverSession, msg, node, order, resourceType, route
- `idEkInfo` (line 46)
  - Used by: content, driverSession, economyType, msg, node, order, route
- `vehicleDistance` (line 2555)
  - Used by: content, driverSession, msg, node, order, resourceType, route
- `ratingType` (line 3082)
  - Used by: content, driverSession, msg, node, order, resourceType, route
- `vehicle` (line 1365)
  - Used by: content, driverSession, msg, node, order, resourceType, route
- `contactInfosType` (line 2096)
  - Used by: content, driverSession, msg, node, order, resourceType, route
- `formOfPayment` (line 1213)
  - Used by: content, driverSession, economyType, msg, node, order, route
- `taxiMeter` (line 1072)
  - Used by: content, driverSession, economyType, msg, node, order, route
- `environmentalInformation` (line 2835)
  - Used by: content, driverSession, msg, node, order, resourceType, route
- `amountType` (line 2434)
  - Used by: content, driverSession, economyType, msg, node, order, route
- `price` (line 1131)
  - Used by: content, driverSession, economyType, msg, node, order, route
- `ratingIdType` (line 3095)
  - Used by: content, driverSession, msg, node, order, resourceType, route
- `attributesType` (line 1559)
  - Used by: content, driverSession, msg, node, order, resourceType, route
- `attribute` (line 1567)
  - Used by: content, driverSession, msg, node, order, resourceType, route
- `contactInfo` (line 2104)
  - Used by: content, driverSession, msg, node, order, resourceType, route
- `driver` (line 1633)
  - Used by: content, driverSession, msg, node, order, resourceType, route
- `exchangeRates` (line 1298)
  - Used by: content, driverSession, economyType, msg, node, order, route
- `priceCalculation` (line 1091)
  - Used by: content, driverSession, economyType, msg, node, order, route
- `seats` (line 1484)
  - Used by: content, driverSession, msg, node, order, resourceType, route
- `subOrderType` (line 2242)
  - Used by: content, driverSession, msg, node, order, route
- `addressType` (line 1798)
  - Used by: content, driverSession, msg, node, order, route
- `product` (line 876)
  - Used by: content, driverSession, msg, node, order, route
- `economyType` (line 1061)
  - Used by: content, driverSession, msg, node, order, route
- `connection` (line 2046)
  - Used by: content, driverSession, msg, node, order, route
- `resourceType` (line 1324)
  - Used by: content, driverSession, msg, node, order, route
- `associatedReservation` (line 2084)
  - Used by: content, driverSession, msg, node, order, route
- `contents` (line 1961)
  - Used by: driverSession, msg, node, order, route
- `content` (line 1969)
  - Used by: driverSession, msg, node, order, route
- `nodeprocess` (line 999)
  - Used by: driverSession, msg, node, order, route
- `node` (line 1658)
  - Used by: driverSession, msg, order, route
- `route` (line 1650)
  - Used by: driverSession, msg, order
- `process` (line 885)
  - Used by: driverSession, msg, order
- `orderStatus` (line 2937)
  - Used by: driverSession, msg, order
- `agreement` (line 137)
  - Used by: driverSession, msg, order
- `multiDispatch` (line 1056)
  - Used by: driverSession, msg, order

## Order vs Driver Session Flow Separation

### Order-Only Types (0)

Types used only in Order-by-Order flow:


### Driver Session-Only Types (4)

Types used only in Driver Session flow:

- `changelog` (line 2964)
- `log` (line 2972)
- `orders` (line 2932)
- `sessionNode` (line 3018)

### Shared Between Flows (47)

Types used by both Order and Driver Session:

- `Validation` (line 3102)
- `addressType` (line 1798)
- `agreement` (line 137)
- `amountType` (line 2434)
- `associatedReservation` (line 2084)
- `attribute` (line 1567)
- `attributesType` (line 1559)
- `capacity` (line 1432)
- `connection` (line 2046)
- `contactInfo` (line 2104)
- `contactInfosType` (line 2096)
- `content` (line 1969)
- `contents` (line 1961)
- `driver` (line 1633)
- `economyType` (line 1061)
- `environmentalInformation` (line 2835)
- `exchangeRates` (line 1298)
- `exhangeRate` (line 1306)
- `formOfPayment` (line 1213)
- `geographicLocation` (line 1881)
- `idEkInfo` (line 46)
- `idType` (line 4)
- `manualDescriptionType` (line 1580)
- `multiDispatch` (line 1056)
- `node` (line 1658)
- ... and 22 more

## Most Depended Upon Types

Types that many other types depend on (infrastructure types):

- `idType`: used by 36 types (line 4)
- `manualDescriptionType`: used by 9 types (line 1580)
- `timesType`: used by 8 types (line 1734)
- `addressType`: used by 7 types (line 1798)
- `resourceType`: used by 7 types (line 1324)
- `time`: used by 6 types (line 1742)
- `contactInfosType`: used by 6 types (line 2096)
- `attributesType`: used by 6 types (line 1559)
- `geographicLocation`: used by 5 types (line 1881)
- `node`: used by 5 types (line 1658)
- `subOrderType`: used by 5 types (line 2242)
- `summaryReport`: used by 4 types (line 2334)
- `economyReport`: used by 4 types (line 2362)
- `orgType`: used by 4 types (line 120)
- `product`: used by 3 types (line 876)
- `ratingType`: used by 3 types (line 3082)
- `order`: used by 3 types (line 853)
- `price`: used by 3 types (line 1131)
- `agreement`: used by 3 types (line 137)
- `economyType`: used by 3 types (line 1061)

## Leaf Types

**Count:** 16

Types that don't depend on any other types (pure data structures):

- `bulkLocationList` (line 3047)
- `contactInfo` (line 2104)
- `date` (line 1792)
- `environmentalInformation` (line 2835)
- `eventType` (line 2250)
- `gpsType` (line 2772)
- `idEkInfo` (line 46)
- `idMsgRef` (line 30)
- `idType` (line 4)
- `multiDispatch` (line 1056)
- `nodeCancelationType` (line 2507)
- `nodeCancellationType` (line 2519)
- `orderStatus` (line 2937)
- `position` (line 1511)
- `time` (line 1742)
- `weekdaysType` (line 2622)

## Circular Dependency Check

✓ No direct circular dependencies found

---

**Analysis Complete**
