# What is SUTI?

> Understanding the purpose and scope of the SUTI standard

---

## Overview

**SUTI** (Standardized Utilization of Transport Information) is a technical communication protocol designed specifically for **Demand Responsive Transport (DRT)** systems.

### Key Facts

- 📊 **30+ million orders/year** processed across the Nordic region
- 🚕 **Hundreds of DRT services** use SUTI
- 🔗 **Standardized integration** between booking and dispatch systems
- 🌍 **Production-proven** in real-world transport operations

---

## The Problem SUTI Solves

### Demand Responsive Transport Challenges

In DRT, several actors must coordinate:

```
Traveller ──► Client (Booking) ──► Provider (Dispatch) ──► Driver
```

**Without a standard:**
- Every Client-Provider pair needs custom integration
- High development and maintenance costs
- Difficult to add new providers or switch between them
- Limited interoperability

**With SUTI:**
- Single standard integration for all partners
- Reduced costs and faster implementation
- Easy multi-provider management
- Proven, battle-tested protocol

---

## What SUTI Provides

### 1. Technical Communication Protocol

SUTI defines:
- **Message format** (XML or JSON)
- **Message types** (90+ standardized messages)
- **Communication methods** (HTTP, port-to-port)
- **Validation schemas** (XSD for XML, JSON Schema)

### 2. Standardized Message Types

Messages organized into logical blocks:

| Block | Messages | Purpose |
|-------|----------|---------|
| **10** | 1000-1922 | Resource management |
| **20** | 2000-2902 | Order lifecycle |
| **30** | 3000-3013 | Dispatch operations |
| **40** | 4000-4102 | Traffic events |
| **50** | 5000-5021 | Communication |
| **60** | 6001-6810 | Reporting |
| **70** | 7000-7101 | Technical control |
| **80** | 8000-8199 | Accounting |

[View all messages →](../messages/README.md)

### 3. Use Case Coverage

SUTI supports complete DRT workflows:

**Before Transport:**
- Order creation and confirmation
- Resource allocation
- Route planning
- Price calculation

**During Transport:**
- Real-time updates
- Driver communications
- Traffic control events
- Route modifications

**After Transport:**
- Trip reporting
- Billing and accounting
- Performance metrics
- Settlement

---

## How SUTI is Used

### Message Exchange

```xml
<!-- Client sends order -->
<SUTI>
  <orgSender name="ClientName">
    <idOrg src="SUTI:idLink" id="clientsw_client_0024" unique="true"/>
  </orgSender>
  <orgReceiver name="ProviderName">
    <idOrg src="SUTI:idLink" id="providersw_provider_0009" unique="true"/>
  </orgReceiver>
  <msg msgType="2000" msgName="Order">
    <idMsg src="clientsw_client_0024:idMsg" id="12345" unique="true"/>
    <order>
      <!-- Order details -->
    </order>
  </msg>
</SUTI>
```

```xml
<!-- Provider confirms -->
<SUTI>
  <orgSender name="ProviderName">
    <idOrg src="SUTI:idLink" id="providersw_provider_0009" unique="true"/>
  </orgSender>
  <orgReceiver name="ClientName">
    <idOrg src="SUTI:idLink" id="clientsw_client_0024" unique="true"/>
  </orgReceiver>
  <msg msgType="2001" msgName="Order confirmation">
    <idMsg src="providersw_provider_0009:idMsg" id="67890" unique="true"/>
    <referencesTo>
      <idMsg src="clientsw_client_0024:idMsg" id="12345" unique="true"/>
    </referencesTo>
  </msg>
</SUTI>
```

### Communication Methods

**Option 1: Single Endpoint (HTTP)**
- Client sets up endpoint
- Provider POSTs messages to Client endpoint
- Provider polls Client endpoint for new messages

**Option 2: Dual Endpoints (HTTP)**
- Both Client and Provider set up endpoints
- Each POSTs directly to the other's endpoint
- More efficient, real-time communication

**Option 3: Port-to-Port**
- Direct connection (physical or logical)
- Less common in modern implementations

---

## SUTI Governance

### Organization

SUTI is maintained by:
- **SUTI Technical Committee** - Standard development
- **SUTI Members** - Organizations using the standard
- **Software Providers** - Implement SUTI in their systems

### Membership Requirements

To be an **official SUTI implementation**:

1. **Membership**: Organization joins SUTI
2. **Approval**: Software name approved by Technical Committee
3. **Link Mapping**: Complete setup process with partners
4. **Compliance**: Messages validate against schemas

### Self-Declaration

Each SUTI implementation must provide:
- Organization description
- Business model
- Supported flows
- Information element usage
- Communication methods
- Contact information

[Learn about Self-Declaration →](../getting-started/establishing-link.md)

---

## Data Formats

### XML (Primary Format)

```xml
<SUTI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="../../schemas/SUTI_Message.xsd">
  <!-- Message content -->
</SUTI>
```

**Validation:**
```bash
xmllint --noout --schema schemas/SUTI_Message.xsd message.xml
```

### JSON (Alternative Format)

SUTI also supports JSON format for messages. The structure mirrors the XML schema but uses JSON conventions.

---

## Standards Compatibility

SUTI aligns with broader transport standards:

- **NeTEx** (Network Timetable Exchange)
- **Transmodel** (Public transport reference data model)
- **GDPR** compliance built-in

---

## Use Cases

### 1. Public Transport Authority

**Scenario**: City needs flexible transport for areas not served by regular buses

**Solution**:
- Authority (Client) uses SUTI to coordinate multiple taxi companies (Providers)
- Travelers book via Authority app
- Orders distributed to available Providers via SUTI
- Real-time tracking and reporting

### 2. Shared Ride Services

**Scenario**: Optimize multiple passenger rides in single vehicle

**Solution**:
- Client creates Order-by-Order or DriverSession messages
- Provider optimizes route dynamically
- SUTI handles complex multi-node routes
- Real-time updates as route changes

### 3. School Transport

**Scenario**: Daily recurring transport for students

**Solution**:
- Repetitive Orders for scheduled routes
- Resource allocation for specific drivers/vehicles
- Automatic confirmation and tracking
- Exception handling (cancellations, delays)

[See detailed use cases →](../use-cases/README.md)

---

## SUTI Versions

**Current Version**: SUTI 2026

**Version History**:
- SUTI 2026 (current)
- SUTI 2019
- SUTI 2018
- Earlier versions...

[View version changelog →](../messages/block-90-versions.md)

---

## Next Steps

Now that you understand what SUTI is:

1. **[Actors & Flows →](actors-and-flows.md)** - Learn about SUTI participants
2. **[Message Format →](message-format.md)** - Understand message structure
3. **[Getting Started →](../getting-started/README.md)** - Build your first SUTI integration
4. **[Examples →](../../examples/README.md)** - Browse working examples

---

## Additional Resources

- **[SUTI Introduction PDF](../SUTI_Introduction.pdf)** - Visual overview
- **[Message Reference](../messages/README.md)** - All message types
- **[How to use SUTI PDF](../How%20to%20use%20SUTI.pdf)** - Complete guide (170 pages)

---

[← Back to Introduction](README.md) | [Continue to Actors & Flows →](actors-and-flows.md)
