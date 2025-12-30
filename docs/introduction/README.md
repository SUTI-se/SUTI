# Introduction to SUTI

> Standardized Utilization of Transport Information - A technical communication protocol for Demand Responsive Transport

---

## What is SUTI?

**SUTI** (Standardized Utilization of Transport Information) is a technical communication protocol used for exchanging information between:

- **Client's** planning and booking systems
- **Provider's** vehicle dispatch systems

The standard powers Demand Responsive Transport (DRT) services across the Nordic region, processing **30+ million orders annually** for hundreds of DRT implementations.

---

## 📖 In This Section

1. **[What is SUTI?](what-is-suti.md)** - Purpose, scope, and use cases
2. **[Actors & Flows](actors-and-flows.md)** - Who uses SUTI and how
3. **[Message Format](message-format.md)** - XML/JSON structure basics

---

## Quick Overview

### The SUTI Ecosystem

```
┌──────────┐     ┌────────┐    ┌──────┐    ┌──────────┐     ┌────────┐
│Traveller │ ──► │ Client │ ══►│ SUTI │ ══►│ Provider │ ──► │ Driver │
└──────────┘     └────────┘    └──────┘    └──────────┘     └────────┘
   Demand         Booking      Messages     Dispatch        Response
```

### Who's Who

| Actor | Role | Example |
|-------|------|---------|
| **Traveller** | Person needing transport | Student, elderly person, passenger |
| **Client** | Aggregates transport demand | Public Transport Authority |
| **Provider** | Carries out transport | Taxi company, transport operator |
| **Driver** | Performs the transport | Taxi driver, bus driver |

---

## Why SUTI?

### Before SUTI
- 🔴 Proprietary integrations between each Client-Provider pair
- 🔴 High integration costs
- 🔴 Limited interoperability
- 🔴 Difficult to switch providers

### With SUTI
- ✅ Standardized communication protocol
- ✅ Reduced integration complexity
- ✅ Multi-provider competition
- ✅ Easy provider switching
- ✅ Proven at scale (30M+ orders/year)

---

## How SUTI Works

### 1. Communication Methods

SUTI messages (XML or JSON format) are exchanged using common methods:

- **Port-to-port communication** (physical or logical over internet)
- **HTTP with single endpoint** (Client sets up, Provider calls)
- **HTTP with dual endpoints** (Both Client and Provider set up)

Each Client defines their preferred method; most Provider software supports all methods.

### 2. Message Exchange

```xml
<SUTI>
  <orgSender name="...">
  <orgReceiver name="...">
  <msg msgType="2000" msgName="Order">
    <!-- Message content -->
  </msg>
</SUTI>
```

Messages contain either:
- **Requests** (e.g., "Create order")
- **Responses** (e.g., "Order confirmed")

### 3. Order Patterns

SUTI supports multiple transport patterns:

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Simple Order** | Single traveller, pickup → dropoff | Basic taxi ride |
| **Shared Transport** | Multiple travellers, optimized route | Shared ride service |
| **Node-by-Node** | Dynamic routing during transport | Flexible DRT |
| **Flag-Stop** | Driver creates order on signal | Traditional bus flag-stop |
| **Repetitive Order** | Scheduled recurring transport | School transport |

---

## Message Types

SUTI defines **90+ message types** organized into 9 blocks:

| Block | Purpose | Example Messages |
|-------|---------|------------------|
| **10** | Dynamic Resource Utilization | Resource login/logout |
| **20** | Order Management | Order, confirm, reject, cancel |
| **30** | Dispatch | Driver assignment |
| **40** | Traffic Control | Events (pickup, drop-off) |
| **50** | Communication | Driver-Client messages |
| **60** | Reports | Trip reports, statistics |
| **70** | Technical Control | System monitoring |
| **80** | Accounting | Billing, invoices |
| **90** | Alterations | Version history |

[View complete message reference →](../messages/README.md)

---

## Standards & Compliance

### Message Validation

All SUTI messages must conform to:
- **XML Schema** ([`schemas/SUTI_Message.xsd`](../../schemas/SUTI_Message.xsd))
- **JSON Schema** (if using JSON format)

```bash
# Validate XML message
xmllint --noout --schema schemas/SUTI_Message.xsd message.xml
```

### Official Implementation

To be considered an **official SUTI implementation**:

1. ✅ Organization must be a SUTI member
2. ✅ Software names approved by Technical Committee
3. ✅ Complete Link Mapping process
4. ✅ Messages validate against schemas

[Learn about Link Mapping →](../getting-started/establishing-link.md)

---

## Next Steps

Ready to dive deeper?

1. **Learn the Details**: [What is SUTI?](what-is-suti.md)
2. **Understand Actors**: [Actors & Flows](actors-and-flows.md)
3. **See Message Structure**: [Message Format](message-format.md)
4. **Start Building**: [Getting Started Guide](../getting-started/README.md)
5. **Browse Examples**: [XML Examples](../../examples/README.md)

---

## Additional Resources

- **[Original PDF](../SUTI_Introduction.pdf)** - Visual introduction (2 pages)
- **[Message Reference](../messages/README.md)** - Complete message specifications
- **[How to use SUTI](../How%20to%20use%20SUTI.pdf)** - Full implementation guide (PDF, 170 pages)

---

[← Back to Documentation Hub](../README.md) | [Continue to What is SUTI? →](what-is-suti.md)
