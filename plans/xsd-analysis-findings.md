# SUTI XSD Schema Analysis

**Generated:** 2026-01-30

**Schema File:** `/Users/martin/Documents/GitHub/SUTI/schemas/SUTI_Message.xsd`

**Lines of Code:** 3131

---

## Executive Summary

- **Complex Types:** 86
- **Simple Types:** 0
- **Top-level Elements:** 1
- **Groups:** 0
- **Message Types:** 136
- **Message Content Elements:** 28

## 1. Current Structure Analysis

### 1.1 Schema Organization

**Single File Schema:** All SUTI message definitions are contained in one XSD file:
- `SUTI_Message.xsd` (3131 lines)
- No imports or includes
- Self-contained schema definition

**Namespace:**
- Default XML Schema namespace: `http://www.w3.org/2001/XMLSchema`
- `elementFormDefault="qualified"`
- `attributeFormDefault="unqualified"`

### 1.2 Root Element Structure

**Root Element:** `<SUTI>`

```xml
<SUTI>
  <orgSender>      <!-- Sending organization -->
  <orgReceiver>    <!-- Receiving organization -->
  <contactReference> <!-- Optional contact info -->
  <msg>            <!-- One or more messages (maxOccurs=unbounded) -->
    <!-- Message content via choice construct -->
  </msg>
  <idVersion>      <!-- Optional version info -->
</SUTI>
```

### 1.3 Complex Types Inventory

Total: 86 complex types

#### By Category:

**Order By Order** (16 types):
- `cancellationConsequence` (line 2167)
- `content` (line 1969)
- `contents` (line 1961)
- `multiDispatch` (line 1056)
- `node` (line 1658)
- `nodeCancelationType` (line 2507)
- `nodeCancellationType` (line 2519)
- `nodeprocess` (line 999)
- `order` (line 853)
- `orderLink` (line 2380)
- ... and 6 more

**Driver Session** (6 types):
- `changelog` (line 2964)
- `driverSession` (line 2898)
- `driverSessionReject` (line 2991)
- `orderStatus` (line 2937)
- `orders` (line 2932)
- `sessionNode` (line 3018)

**Shared** (25 types):
- `Validation` (line 3102)
- `amountType` (line 2434)
- `authorizationAcceptType` (line 2423)
- `connection` (line 2046)
- `environmentalInformation` (line 2835)
- `event` (line 2279)
- `eventReport` (line 2269)
- `eventType` (line 2250)
- `exchangeRates` (line 1298)
- `exhangeRate` (line 1306)
- ... and 15 more

**Infrastructure** (16 types):
- `addressType` (line 1798)
- `agreement` (line 137)
- `attribute` (line 1567)
- `attributesType` (line 1559)
- `contactInfo` (line 2104)
- `contactInfosType` (line 2096)
- `date` (line 1792)
- `errorType` (line 2804)
- `geographicLocation` (line 1881)
- `orgPaymentType` (line 2743)
- ... and 6 more

**Accounting** (12 types):
- `associatedReservation` (line 2084)
- `calculationFareType` (line 2671)
- `deliveryNote` (line 2472)
- `economyReport` (line 2362)
- `economyType` (line 1061)
- `formOfPayment` (line 1213)
- `payment` (line 1229)
- `price` (line 1131)
- `priceCalculation` (line 1091)
- `resourceReservation` (line 2531)
- ... and 2 more

**Resource** (7 types):
- `capacity` (line 1432)
- `driver` (line 1633)
- `position` (line 1511)
- `resourceType` (line 1324)
- `vehicle` (line 1365)
- `vehicleDistance` (line 2555)
- `vehicleLocation` (line 3028)

**Repetitive** (2 types):
- `calendarType` (line 2588)
- `weekdaysType` (line 2622)

**Information** (2 types):
- `bulkLocationList` (line 3047)
- `locationRequest` (line 2397)

### 1.4 Message Types

**Total Message Types:** 136

#### Message Ranges:

**1000-1999: Resource & Information** (31 messages)
- 1000, 1001, 1002, 1010, 1011, 1012, 1020, 1021, 1022, 1023, 1024, 1025, 1060, 1061, 1062, ... (+16 more)

**2000-2099: Order Management** (22 messages)
- 2000, 2001, 2002, 2003, 2005, 2006, 2007, 2010, 2011, 2012, 2013, 2020, 2021, 2022, 2023, ... (+7 more)

**2100-2199: Driver Session** (12 messages)
- 2100, 2101, 2102, 2103, 2104, 2105, 2106, 2107, 2110, 2111, 2112, 2113

**2500-2599: Reports** (5 messages)
- 2530, 2531, 2532, 2540, 2541

**2800-2899: Templates** (3 messages)
- 2800, 2801, 2810

**2900-2999: Authorization** (3 messages)
- 2900, 2901, 2902

**3000-3099: Dispatch** (6 messages)
- 3000, 3001, 3002, 3003, 3004, 3013

**4000-4199: Traffic Control** (15 messages)
- 4000, 4001, 4002, 4010, 4011, 4012, 4020, 4021, 4031, 4040, 4041, 4042, 4100, 4101, 4102

**5000-5099: Address/Location** (7 messages)
- 5000, 5001, 5002, 5010, 5011, 5020, 5021

**6000-6999: Reports & Delivery** (12 messages)
- 6001, 6060, 6061, 6062, 6500, 6501, 6502, 6503, 6510, 6511, 6800, 6810

**7000-7099: Provider Orders** (11 messages)
- 7000, 7001, 7002, 7010, 7011, 7015, 7020, 7021, 7030, 7031, 7099

**8000-8999: Accounting** (7 messages)
- 8000, 8010, 8101, 8102, 8111, 8181, 8199

## 2. Message Flow Identification

### 2.1 Message Content Elements (Choice Construct)

The `msg` complex type uses a choice construct to define different message contents.
**Total choices:** 28

#### Order-by-Order Flow Elements:

**Count:** 11

- `<order>` (type: `order`)
  - Messages: msgs: 2000,  2900, 4001, 4020, 7100, 7101
- `<orderReject>` (type: `None`)
  - Messages: msgs: 2002
- `<cancellationConsequence>` (type: `cancellationConsequence`)
  - Messages: msgs: 2011, 2012, 2021, 2022
- `<pickupConfirmation>` (type: `None`)
  - Messages: msgs: 4010, 4040 pickupConfirmation
- `<orderLink>` (type: `orderLink`)
  - Messages: msg: 2040
- `<orderReport>` (type: `orderReport`)
  - Messages: msg 6001, 2531
- `<nodeCancelation>` (type: `None`)
  - Messages: Msg 2020 Node Cancelation. This shall not be used due to  error in spelling. TU request members to change to nodeCancellation as soon as possible.
- `<nodeCancellation>` (type: `nodeCancellationType`)
  - Messages: Msg 2020 Node Cancellation
- `<orderTemplate>` (type: `None`)
  - Messages: Msg 2800, 2801, 2541, 6800
- `<scheduleElementOrderList>` (type: `None`)
  - Messages: Msg 2810
- ... and 1 more

#### Driver Session Flow Elements:

**Count:** 2

- `<driverSession>` (type: `driverSession`)
  - Messages: msgs: 2100, 2101
- `<driverSessionReject>` (type: `driverSessionReject`)
  - Messages: msgs: 2102

#### Other/Shared Elements:

**Count:** 15

- `<resourceDispatch>` (type: `resourceType`)
  - Messages: msgs: 1020, 3000, 3001, 3003, 3004, 3013
- `<addressLocation>` (type: `addressType`)
  - Messages: msgs: 4003, 5021
- `<manualDescriptionMsg>` (type: `None`)
  - Messages: msgs: 1022, 1025, 4012,  5000, 5010, 7030, 7031
- `<locationRequest>` (type: `locationRequest`)
  - Messages: msg 5020, if sequential addressLocations are required
- `<authorizationAccept>` (type: `authorizationAcceptType`)
  - Messages: msg 2901
- `<deliveryNote>` (type: `deliveryNote`)
  - Messages: Msg 6500
- `<resourceAllocation>` (type: `None`)
  - Messages: Msg 1920
- `<infoRequest>` (type: `None`)
  - Messages: Msg 15XX
- `<infoResponse>` (type: `None`)
  - Messages: Msg 16XX
- `<accounting>` (type: `None`)
  - Messages: Msg 8XXX
- `<bulkLocationRequest>` (type: `None`)
  - Messages: Msg 110xx

See “How to use SUTI” 4.6.3 bulkLocation request and response
- `<bulkLocation>` (type: `bulkLocationList`)
  - Messages: Msg111x

See “How to use SUTI” 4.6.3 bulkLocation request and response
- `<resourceInformation>` (type: `resourceType`)
  - Messages: Msg 100x, 101x

See “How to use SUTI” 4.6 Exchanging resource information
- `<ratings>` (type: `ratingType`)
  - Messages: Msg 1061, 6061

See “How to use SUTI” 4.6 Exchanging resource information
- `<actionRequest>` (type: `None`)
  - Messages: Msg 4100

### 2.2 Type Dependencies by Flow

#### Infrastructure/Shared Types

**Count:** 16

These types are used across all message flows:

- `addressType`
- `agreement`
- `attribute`
- `attributesType`
- `contactInfo`
- `contactInfosType`
- `date`
- `errorType`
- `geographicLocation`
- `orgPaymentType`
- `orgType`
- `organizationType`
- `providerorderUpdate`
- `referencesTo`
- `time`
- `timesType`

#### Order-by-Order Specific Types

**Count:** 16

- `cancellationConsequence`
- `content`
- `contents`
- `multiDispatch`
- `node`
- `nodeCancelationType`
- `nodeCancellationType`
- `nodeprocess`
- `order`
- `orderLink`
- `orderReject`
- `orderReport`
- `pickupConfirmation`
- `requestContentType`
- `route`
- `subOrderType`

#### Driver Session Specific Types

**Count:** 6

- `changelog`
- `driverSession`
- `driverSessionReject`
- `orderStatus`
- `orders`
- `sessionNode`

#### Accounting Types

**Count:** 12

- `associatedReservation`
- `calculationFareType`
- `deliveryNote`
- `economyReport`
- `economyType`
- `formOfPayment`
- `payment`
- `price`
- `priceCalculation`
- `resourceReservation`
- `suborderTourType`
- `vatAmountSpecificationType`

#### Resource Management Types

**Count:** 7

- `capacity`
- `driver`
- `position`
- `resourceType`
- `vehicle`
- `vehicleDistance`
- `vehicleLocation`

#### Repetitive Orders Types

**Count:** 2

- `calendarType`
- `weekdaysType`

## 3. Complexity Analysis

### 3.1 Deeply Nested Types

✓ No excessively nested types found

### 3.2 Large Complex Types

Types with many child elements (>20):

- `msg`: 80 elements (line 147)
- `referencesTo`: 21 elements (line 733)

### 3.3 Highly Optional Types

✓ No types with excessive optionals found

### 3.4 Documentation Coverage

**Coverage:** 77/86 types (89.5%)

Types with sparse/missing documentation (37):

- `Validation`
- `addressType`
- `amountType`
- `attribute`
- `calculationFareType`
- `calendarType`
- `contactInfo`
- `content`
- `contents`
- `date`
- `driver`
- `economyType`
- `errorType`
- `event`
- `exhangeRate`
- `idMsgRef`
- `log`
- `manualDescriptionType`
- `orderReject`
- `orderStatus`
- ... and 17 more

### 3.5 Extension Mechanisms

**Extension Points:** 17

Types using xs:extension:

- Extends `msg` in `unknown`
- Extends `referencesTo` in `unknown`
- Extends `orderReject` in `unknown`
- Extends `manualDescriptionType` in `unknown`
- Extends `pickupConfirmation` in `unknown`
- Extends `nodeCancelationType` in `unknown`
- Extends `idType` in `unknown`
- Extends `referencesTo` in `unknown`
- Extends `payment` in `unknown`
- Extends `vatAmountSpecificationType` in `unknown`
- Extends `addressType` in `unknown`
- Extends `nodeprocess` in `unknown`
- Extends `idType` in `unknown`
- Extends `idType` in `unknown`
- Extends `attributesType` in `unknown`
- ... and 2 more

### 3.6 Enumeration Analysis

**Total Enumerations:** 0


## 4. Technical Details

### 4.1 Namespaces

- **XML Schema:** `http://www.w3.org/2001/XMLSchema`
- **No custom namespaces** defined
- **No imports or includes**

### 4.2 Versioning Approach

- Optional `<idVersion>` element at root level
- Note in schema: *'TU would like to know if anyone uses this part'*
- **Versioning mechanism unclear/underused**

### 4.3 Special Constructs

- **Choice constructs:** 3 types
- **Sequence constructs:** 71 types
- **Extensions:** 9 types
- **xs:any elements:** (requires manual inspection)
- **Substitution groups:** None found

### 4.4 Cardinality Patterns

- **Optional elements (minOccurs=0):** 217
- **Unbounded elements (maxOccurs=unbounded):** 61

## 5. Refactoring Opportunities

### 5.1 Schema Modularity

**Current:** Single 3131-line file

**Potential Split:**

1. **Core Infrastructure** (~500 lines)
   - `idType`, `orgType`, `agreement`, `referencesTo`
   - `addressType`, `geographicLocation`, `timesType`, `date`
   - `contactInfosType`, `attributesType`, `errorType`

2. **Order-by-Order Flow** (~1200 lines)
   - `order`, `route`, `node`, `contents`, `content`
   - `orderReject`, `cancellationConsequence`, `pickupConfirmation`
   - `nodeprocess`, `connection`, `orderLink`

3. **Driver Session Flow** (~300 lines)
   - `driverSession`, `driverSessionReject`, `orders`, `orderStatus`
   - `changelog`, `log`, `sessionNode`

4. **Resource Management** (~400 lines)
   - `resourceType`, `vehicle`, `driver`, `capacity`
   - `position`, `vehicleLocation`, `bulkLocationList`

5. **Accounting & Economy** (~500 lines)
   - `economyType`, `price`, `priceCalculation`, `payment`
   - `economyReport`, `summaryReport`, `deliveryNote`
   - `calculationFareType`, `vatAmountSpecificationType`

6. **Repetitive Orders** (~200 lines)
   - `calendarType`, `weekdaysType`, template structures

### 5.2 Simplification Opportunities

#### Over-engineered Patterns:

1. **Excessive Optional Elements**
2. **Deep Nesting**
3. **Inline Complex Types**
   - Many anonymous complex types defined inline
   - Consider: Extract to named types for reuse

4. **Enumeration Inconsistency**
   - Mix of numeric codes ('3101', '3102') and text values ('client', 'provider')
   - Consider: Standardize on one approach

### 5.3 Documentation Improvements

- 37 types need better documentation
- Many references to external document 'How to use SUTI'
- Consider: Inline more context, examples in annotations

### 5.4 Versioning Strategy

**Current Issues:**
- Optional `idVersion` element rarely used
- No namespace versioning
- No version attributes on schema

**Recommendations:**
- Add version attribute to schema element
- Consider namespace versioning for major changes
- Define clear versioning policy

### 5.5 Backward Compatibility Considerations

**Breaking Changes to Avoid:**
- Removing optional elements
- Making optional elements required
- Changing element types
- Removing enumeration values

**Safe Changes:**
- Adding new optional elements
- Adding new enumeration values
- Expanding documentation
- Making required elements optional (with care)

## 6. Summary Statistics

| Metric | Count |
|--------|-------|
| Total Lines | 3131 |
| Complex Types | 86 |
| Simple Types | 0 |
| Top-level Elements | 1 |
| Groups | 0 |
| Message Types | 136 |
| Message Content Choices | 28 |
| Optional Elements | 217 |
| Unbounded Elements | 61 |
| Enumerations | 0 |
| Extension Points | 17 |
| Documentation Coverage | 89.5% |

---

**Analysis Complete**

This comprehensive analysis provides the foundation for informed refactoring decisions.
