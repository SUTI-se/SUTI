# SUTI Documentation Hub

> Complete reference documentation for the SUTI standard

Welcome to the SUTI documentation. This hub provides access to all specification documents, implementation guides, and resources needed to build SUTI-compliant systems.

---

## 🎯 Start Here

**New to SUTI?** Begin with these resources:

1. **[Introduction](introduction/README.md)** - Understand what SUTI is and core concepts
2. **[Getting Started](getting-started/README.md)** - Set up your first SUTI link
3. **[Examples](../examples/README.md)** - Browse validated XML message examples

---

## 📚 Documentation Sections

### Core Concepts
| Section | Description | Status |
|---------|-------------|--------|
| **[Introduction](introduction/README.md)** | What is SUTI? Actors, flows, and basics | ✅ Ready |
| **[Getting Started](getting-started/README.md)** | Implementation setup guide | 🚧 In Progress |
| **[Message Reference](messages/README.md)** | Complete message specifications | 🚧 In Progress |

### Implementation Guides
| Section | Description | Status |
|---------|-------------|--------|
| **[Use Cases](use-cases/README.md)** | Real-world scenarios and flows | 📋 Planned |
| **[Message Flows](message-flows/README.md)** | Visual sequence diagrams | 📋 Planned |
| **[Schemas](schemas/README.md)** | XSD/JSON schema documentation | 📋 Planned |

### Resources
| Section | Description | Status |
|---------|-------------|--------|
| **[Examples](examples/README.md)** | Example documentation and catalog | 📋 Planned |
| **[PDF Documents](#original-pdf-documentation)** | Original specification PDFs | ✅ Available |

---

## 📖 Documentation Map

### By Role

**I'm a Developer** 👨‍💻
1. [Introduction](introduction/README.md) - Learn SUTI basics
2. [Schemas](schemas/README.md) - Understand message structure
3. [Examples](../examples/README.md) - See working examples
4. [Getting Started](getting-started/README.md) - Build your integration

**I'm a System Architect** 🏗️
1. [Getting Started](getting-started/README.md) - Link establishment
2. [Use Cases](use-cases/README.md) - Understand flows
3. [Message Flows](message-flows/README.md) - Visualize sequences
4. [Message Reference](messages/README.md) - Complete specifications

**I'm a Project Manager** 📊
1. [Introduction](introduction/README.md) - Understand scope
2. [Getting Started](getting-started/README.md) - Implementation requirements
3. [Use Cases](use-cases/README.md) - Real-world scenarios

---

## 🔍 Find Documentation By...

### By Message Block

| Block | Title | Messages | Documentation |
|-------|-------|----------|---------------|
| **10** | Dynamic Resource Utilization | 1000-1922 | [View](messages/block-10-resource.md) |
| **20** | Order Management | 2000-2902 | [View](messages/block-20-order.md) |
| **30** | Dispatch | 3000-3013 | [View](messages/block-30-dispatch.md) |
| **40** | Traffic Control | 4000-4102 | [View](messages/block-40-traffic.md) |
| **50** | Communication | 5000-5021 | [View](messages/block-50-communication.md) |
| **60** | Reports | 6001-6810 | [View](messages/block-60-report.md) |
| **70** | Technical Control | 7000-7101 | [View](messages/block-70-technical.md) |
| **80** | Accounting | 8000-8199 | [View](messages/block-80-accounting.md) |

### By Topic

- **Link Establishment**: [Getting Started → Establishing a SUTI Link](getting-started/establishing-link.md)
- **Message Format**: [Introduction → Message Format](introduction/message-format.md)
- **Order Flows**: [Use Cases → Order Flows](use-cases/order-flows.md)
- **Validation**: [Schemas → Validation Guide](schemas/validation-guide.md)
- **Communication Methods**: [Getting Started → Communication Methods](getting-started/communication-methods.md)
- **GDPR & Security**: [Getting Started → GDPR and Security](getting-started/gdpr-security.md)

---

## 📄 Original PDF Documentation

The source specifications are available as PDFs:

| Document | Pages | Description | Link |
|----------|-------|-------------|------|
| **SUTI Introduction** | 2 | Quick overview and concepts | [PDF](SUTI_Introduction.pdf) |
| **SUTI Messages** | 54 | Message block specifications | [PDF](SUTI_Messages.pdf) |
| **Message Flow** | 12 | Visual flow diagrams | [PDF](SUTI_Message_Flow.pdf) |
| **How to use SUTI** | 170 | Complete implementation guide | [PDF](How%20to%20use%20SUTI.pdf) |

---

## 🚀 Quick Links

### Common Tasks
- **Validate XML**: See [Schemas → Validation Guide](schemas/validation-guide.md)
- **Create an Order**: See [Use Cases → Order Flows](use-cases/order-flows.md)
- **Set up HTTP communication**: See [Getting Started → Communication Methods](getting-started/communication-methods.md)
- **Browse examples**: See [Examples Catalog](../examples/README.md)

### Reference
- **XSD Schema**: [`../schemas/SUTI_Message.xsd`](../schemas/SUTI_Message.xsd)
- **XML Examples**: [`../examples/XML/`](../examples/XML/)
- **Version History**: [Messages → Block 90: Alterations](messages/block-90-versions.md)

---

## 📦 Documentation Structure

```
docs/
├── README.md (this file)       # Documentation hub
│
├── introduction/               # Core concepts
│   ├── README.md              # Overview
│   ├── what-is-suti.md        # SUTI purpose and scope
│   ├── actors-and-flows.md    # DRT actors and order patterns
│   └── message-format.md      # XML/JSON structure basics
│
├── getting-started/           # Implementation guide
│   ├── README.md              # Quick start
│   ├── suti-basics.md         # Terms and concepts
│   ├── establishing-link.md   # Link Mapping process
│   ├── communication-methods.md  # HTTP protocols
│   └── gdpr-security.md       # Security and privacy
│
├── messages/                  # Message specifications
│   ├── README.md              # Messages overview
│   ├── block-10-resource.md   # Dynamic Resource (1000-1922)
│   ├── block-20-order.md      # Orders (2000-2902)
│   ├── block-30-dispatch.md   # Dispatch (3000-3013)
│   ├── block-40-traffic.md    # Traffic Control (4000-4102)
│   ├── block-50-communication.md  # Communication (5000-5021)
│   ├── block-60-report.md     # Reports (6001-6810)
│   ├── block-70-technical.md  # Technical (7000-7101)
│   ├── block-80-accounting.md # Accounting (8000-8199)
│   └── block-90-versions.md   # Version history
│
├── use-cases/                 # Real-world scenarios
│   ├── README.md              # Use cases overview
│   ├── order-flows.md         # Order lifecycle scenarios
│   ├── traffic-control.md     # Traffic management
│   ├── communication.md       # Communication patterns
│   └── reports.md             # Reporting scenarios
│
├── message-flows/             # Visual flow diagrams
│   ├── README.md              # Flows overview
│   ├── block-10-flows.md      # Resource flow diagrams
│   ├── block-20-flows.md      # Order flow diagrams
│   └── ...                    # Other block flows
│
├── schemas/                   # Schema documentation
│   ├── README.md              # Schema overview
│   ├── validation-guide.md    # How to validate
│   └── xsd-reference.md       # XSD documentation
│
└── examples/                  # Examples documentation
    ├── README.md              # Examples overview
    └── message-catalog.md     # Full examples index
```

---

## 🔄 Documentation Status

**Current Version**: SUTI 2026

**Migration Progress**:
- ✅ Phase 1: Foundation (structure, introduction, examples)
- 🚧 Phase 2: Message Reference (in progress)
- 📋 Phase 3: Message Flows (planned)
- 📋 Phase 4: Implementation Guide (planned)

---

## 🤝 Contributing

Found an error or want to improve the documentation?

1. Check existing [issues](https://github.com/SUTI-se/SUTI/issues)
2. Open a new issue with details
3. Or submit a pull request with fixes

---

## 📞 Need Help?

- **General Questions**: See [Getting Started Guide](getting-started/README.md)
- **Technical Support**: Contact SUTI Technical Committee
- **Implementation Help**: Review [Use Cases](use-cases/README.md) and [Examples](../examples/README.md)

---

[Back to Repository](../README.md)
