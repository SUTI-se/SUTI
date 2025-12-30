# SUTI - Standardized Utilization of Transport Information

> Technical communication protocol for Demand Responsive Transport (DRT) information exchange

[![SUTI Version](https://img.shields.io/badge/SUTI-2026-blue)](https://github.com/SUTI-se/SUTI/tags)
[![License](https://img.shields.io/badge/license-SUTI%20Standard-green)](LICENSE)

SUTI is a standard for communication between Client planning/booking systems and Provider vehicle dispatch systems in Demand Responsive Transport. Used by hundreds of DRT services handling **30+ million orders yearly** in the Nordic region.

---

## 📚 Documentation

### Quick Start
- **[Introduction](docs/introduction/README.md)** - What is SUTI? Core concepts and actors
- **[Getting Started](docs/getting-started/README.md)** - Set up your first SUTI implementation
- **[Message Reference](docs/messages/README.md)** - Complete message specifications

### Implementation Guides
- **[Use Cases & Flows](docs/use-cases/README.md)** - Real-world implementation scenarios
- **[Message Flows](docs/message-flows/README.md)** - Visual message sequence diagrams
- **[Schema Documentation](docs/schemas/README.md)** - XML/JSON validation and reference

### Resources
- **[XML Examples](examples/README.md)** - 35+ validated message examples
- **[PDF Documentation](docs/)** - Original specification documents

---

## 🚀 Quick Example

```xml
<SUTI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="schemas/SUTI_Message.xsd">
  <orgSender name="ClientName">
    <idOrg src="SUTI:idLink" id="clientsw_clientname_0024" unique="true"/>
  </orgSender>
  <orgReceiver name="ProviderName">
    <idOrg src="SUTI:idLink" id="providersw_providername_0009" unique="true"/>
  </orgReceiver>
  <msg msgType="2000" msgName="Order">
    <!-- Order details -->
  </msg>
</SUTI>
```

**Validate:**
```bash
xmllint --noout --schema schemas/SUTI_Message.xsd examples/XML/2000.xml
```

---

## 📋 Message Blocks

| Block | Description | Messages |
|-------|-------------|----------|
| **[10](docs/messages/block-10-resource.md)** | Dynamic Resource Utilization | 1000-1922 |
| **[20](docs/messages/block-20-order.md)** | Order Management | 2000-2902 |
| **[30](docs/messages/block-30-dispatch.md)** | Dispatch | 3000-3013 |
| **[40](docs/messages/block-40-traffic.md)** | Traffic Control | 4000-4102 |
| **[50](docs/messages/block-50-communication.md)** | Communication | 5000-5021 |
| **[60](docs/messages/block-60-report.md)** | Reports | 6001-6810 |
| **[70](docs/messages/block-70-technical.md)** | Technical Control | 7000-7101 |
| **[80](docs/messages/block-80-accounting.md)** | Accounting | 8000-8199 |

---

## 🔧 Getting Started

### Prerequisites
- XML/JSON parser
- HTTP client (for communication)
- SUTI member organization credentials (for official implementations)

### Installation
1. Clone this repository
2. Review [Introduction](docs/introduction/README.md)
3. Explore [examples](examples/README.md)
4. Follow [Getting Started Guide](docs/getting-started/README.md)

### Validation
All XML examples can be validated against the XSD schema:

```bash
# Validate a single file
xmllint --noout --schema schemas/SUTI_Message.xsd examples/XML/2000.xml

# Validate all examples
for file in examples/XML/*.xml; do
  xmllint --noout --schema schemas/SUTI_Message.xsd "$file" && echo "✓ $file"
done
```

---

## 🏢 Actors in SUTI

```
Traveller → Client (Planning/Booking) → SUTI Link → Provider (Dispatch) → Driver/Vehicle
```

- **Traveller**: Person/entity needing transport
- **Client**: Public Transport Authority, booking aggregator
- **Provider**: Taxi company, transport operator
- **Driver**: Person performing the transport

---

## 📦 Repository Structure

```
SUTI/
├── docs/                    # Markdown documentation
│   ├── introduction/        # Core concepts
│   ├── getting-started/     # Implementation guide
│   ├── messages/            # Message reference
│   ├── message-flows/       # Flow diagrams
│   ├── use-cases/           # Scenarios
│   └── schemas/             # Schema documentation
├── examples/
│   └── XML/                 # Validated examples
├── schemas/
│   └── SUTI_Message.xsd     # XML Schema Definition
└── data/                    # Source documents
```

---

## 🔖 Official Releases

All official releases are published as [GitHub Tags](https://github.com/SUTI-se/SUTI/tags).

**Current Version:** SUTI 2026

**Note:** The `main` branch contains reviewed changes and should be used for reference only. For production implementations, use tagged releases. Ongoing development happens in feature branches.

---

## 📖 Additional Resources

### Original PDF Documentation
- [SUTI Introduction](docs/SUTI_Introduction.pdf) - Quick overview
- [SUTI Messages](docs/SUTI_Messages.pdf) - Message specifications (54 pages)
- [Message Flow](docs/SUTI_Message_Flow.pdf) - Flow diagrams
- [How to use SUTI](docs/How%20to%20use%20SUTI.pdf) - Complete guide (170 pages)

### Markdown Documentation
- [Documentation Hub](docs/README.md) - Navigate all documentation
- [Examples Catalog](examples/README.md) - Browse XML examples by type

---

## 🤝 Contributing

SUTI is maintained by the SUTI Technical Committee. To become an official SUTI implementation:

1. Your organization must be a SUTI member
2. Software names must be approved by the Technical Committee
3. Follow the [Link Mapping process](docs/getting-started/establishing-link.md)

---

## 📞 Support

- **Technical Committee**: Contact via SUTI organization
- **Documentation Issues**: Open an issue in this repository
- **Implementation Questions**: See [Getting Started Guide](docs/getting-started/README.md)

---

## 📄 License

SUTI Standard - See SUTI organization for terms and membership

---

**Made with ❤️ by the SUTI Community**
