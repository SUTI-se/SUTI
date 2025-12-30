# SUTI XML Examples

> Validated XML message examples for SUTI implementation reference

This directory contains **35+ working XML examples** that demonstrate proper SUTI message structure and validate against the official XSD schema.

---

## 📂 Quick Access

| Message Block | Examples | Jump To |
|---------------|----------|---------|
| **Block 10** - Resource | 1020-1023 | [View](#block-10-dynamic-resource-utilization) |
| **Block 20** - Order | 2000-2902 | [View](#block-20-order-management) |
| **Block 30** - Dispatch | 3003 | [View](#block-30-dispatch) |
| **Block 40** - Traffic | 4010-4102 | [View](#block-40-traffic-control) |
| **Block 50** - Communication | 5010-5011 | [View](#block-50-communication) |
| **Block 60** - Reports | 6001-6810 | [View](#block-60-reports) |
| **Block 70** - Technical | 7010 | [View](#block-70-technical-control) |
| **Block 80** - Accounting | 8010-8011 | [View](#block-80-accounting) |

---

## ✅ Validation

### Validate Single File

```bash
xmllint --noout --schema schemas/SUTI_Message.xsd examples/XML/2000.xml
```

**Expected output:**
```
examples/XML/2000.xml validates
```

### Validate All Examples

```bash
for file in examples/XML/*.xml; do
  echo "Validating: $(basename "$file")"
  xmllint --noout --schema schemas/SUTI_Message.xsd "$file" && echo "✓ Valid"
done
```

### Using Python

```python
from lxml import etree

# Load schema
schema = etree.XMLSchema(file='schemas/SUTI_Message.xsd')

# Validate message
doc = etree.parse('examples/XML/2000.xml')
is_valid = schema.validate(doc)

if is_valid:
    print("✓ Message is valid")
else:
    print("✗ Validation errors:")
    for error in schema.error_log:
        print(f"  - {error}")
```

---

## 📋 Examples Catalog

### Block 10: Dynamic Resource Utilization

Resource login/logout and availability management.

| File | Message Type | Description |
|------|--------------|-------------|
| [`1020.xml`](XML/1020.xml) | MSG 1020 | Resource Login |
| [`1021.xml`](XML/1021.xml) | MSG 1021 | Resource Login Confirmation |
| [`1022.xml`](XML/1022.xml) | MSG 1022 | Resource Login Reject |
| [`1023.xml`](XML/1023.xml) | MSG 1023 | Resource Logoff |

**Reference**: [Block 10 Documentation](../docs/messages/block-10-resource.md)

---

### Block 20: Order Management

Order lifecycle from creation to completion.

| File | Message Type | Description |
|------|--------------|-------------|
| [`2000.xml`](XML/2000.xml) | MSG 2000 | Order (Basic) |
| [`2000_OrderAlter.xml`](XML/2000_OrderAlter.xml) | MSG 2000 | Order with Alteration |
| [`2001.xml`](XML/2001.xml) | MSG 2001 | Order Confirmation |
| [`2010.xml`](XML/2010.xml) | MSG 2010 | Order Cancellation Request |
| [`2011.xml`](XML/2011.xml) | MSG 2011 | Order Cancellation Accepted |

**Reference**: [Block 20 Documentation](../docs/messages/block-20-order.md)

**Key Example**: [`2000.xml`](XML/2000.xml) - Shows complete order structure

---

### Block 30: Dispatch

Dispatch operations and driver assignment.

| File | Message Type | Description |
|------|--------------|-------------|
| [`3003.xml`](XML/3003.xml) | MSG 3003 | Dispatch Information |

**Reference**: [Block 30 Documentation](../docs/messages/block-30-dispatch.md)

---

### Block 40: Traffic Control

Real-time traffic events during transport.

| File | Message Type | Description |
|------|--------------|-------------|
| [`4010_Bom.xml`](XML/4010_Bom.xml) | MSG 4010 | Event Confirmation - Beginning of Mission |
| [`4010_Drop.xml`](XML/4010_Drop.xml) | MSG 4010 | Event Confirmation - Drop-off |
| [`4010_Pickup.xml`](XML/4010_Pickup.xml) | MSG 4010 | Event Confirmation - Pickup |
| [`4011_Drop.xml`](XML/4011_Drop.xml) | MSG 4011 | Event - Drop-off |
| [`4011_Drop with infomessage.xml`](XML/4011_Drop%20with%20infomessage.xml) | MSG 4011 | Event - Drop-off with Info Message |
| [`4011_Pickup.xml`](XML/4011_Pickup.xml) | MSG 4011 | Event - Pickup |
| [`4011_Pickup with infomessage.xml`](XML/4011_Pickup%20with%20infomessage.xml) | MSG 4011 | Event - Pickup with Info Message |
| [`4011_NoShow.xml`](XML/4011_NoShow.xml) | MSG 4011 | Event - No Show |
| [`4011_NoShow with infomessage.xml`](XML/4011_NoShow%20with%20infomessage.xml) | MSG 4011 | Event - No Show with Info |
| [`4012_BomRejected.xml`](XML/4012_BomRejected.xml) | MSG 4012 | Event Reject - BOM Rejected |

**Reference**: [Block 40 Documentation](../docs/messages/block-40-traffic.md)

**Note**: Files with spaces in names require URL encoding when linking: `%20`

---

### Block 50: Communication

Communication messages between systems.

| File | Message Type | Description |
|------|--------------|-------------|
| [`5010.xml`](XML/5010.xml) | MSG 5010 | Information Request |
| [`5011.xml`](XML/5011.xml) | MSG 5011 | Information Response |

**Reference**: [Block 50 Documentation](../docs/messages/block-50-communication.md)

---

### Block 60: Reports

Reporting and statistics.

| File | Message Type | Description |
|------|--------------|-------------|
| [`6001.xml`](XML/6001.xml) | MSG 6001 | Trip Report |
| [`6810.xml`](XML/6810.xml) | MSG 6810 | Statistics Report |

**Reference**: [Block 60 Documentation](../docs/messages/block-60-report.md)

---

### Block 70: Technical Control

Technical monitoring and control.

| File | Message Type | Description |
|------|--------------|-------------|
| [`7010.xml`](XML/7010.xml) | MSG 7010 | System Status |

**Reference**: [Block 70 Documentation](../docs/messages/block-70-technical.md)

---

### Block 80: Accounting

Billing and accounting messages.

| File | Message Type | Description |
|------|--------------|-------------|
| [`8010.xml`](XML/8010.xml) | MSG 8010 | Invoice |
| [`8011.xml`](XML/8011.xml) | MSG 8011 | Invoice Confirmation |

**Reference**: [Block 80 Documentation](../docs/messages/block-80-accounting.md)

---

## 🔍 Example Message Structure

All SUTI messages follow this basic structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<SUTI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="../../schemas/SUTI_Message.xsd">

  <!-- Sender identification -->
  <orgSender name="OrganizationName">
    <idOrg src="SUTI:idLink"
           id="softwarename_orgname_0024"
           unique="true"/>
  </orgSender>

  <!-- Receiver identification -->
  <orgReceiver name="ReceiverName">
    <idOrg src="SUTI:idLink"
           id="softwarename_receiver_0009"
           unique="true"/>
  </orgReceiver>

  <!-- Message content -->
  <msg msgType="XXXX" msgName="MessageName">
    <idMsg src="softwarename_orgname_0024:idMsg"
           id="unique_message_id"
           unique="true"/>

    <!-- Message-specific elements -->

  </msg>
</SUTI>
```

### Key Elements

- **`<SUTI>`**: Root element with schema reference
- **`<orgSender>`**: Identifies who sent the message
- **`<orgReceiver>`**: Identifies recipient
- **`<msg>`**: Contains message type and content
- **`<idMsg>`**: Unique message identifier
- **`msgType`**: 4-digit message number (e.g., 2000)
- **`msgName`**: Human-readable message name (e.g., "Order")

---

## 💡 Usage Tips

### 1. Start with Simple Examples

Begin with basic messages:
1. [`1020.xml`](XML/1020.xml) - Resource Login (simple)
2. [`2000.xml`](XML/2000.xml) - Basic Order
3. [`2001.xml`](XML/2001.xml) - Order Confirmation

### 2. Use Examples as Templates

Copy an example and modify:
- Update `orgSender` and `orgReceiver` names/IDs
- Change `idMsg` to unique value
- Modify message-specific content
- Validate before sending

### 3. Understand ID Formats

ID formats are defined during Link Mapping:

```xml
<idOrg src="SUTI:idLink"
       id="softwarename_organizationname_sequencenumber"
       unique="true"/>
```

**Parts**:
- `softwarename`: Approved by SUTI Technical Committee
- `organizationname`: Your organization name
- `sequencenumber`: 4-digit sequence (0001-9999)

### 4. Validate Early, Validate Often

Always validate messages before sending:

```bash
# Quick validation
xmllint --noout --schema schemas/SUTI_Message.xsd your_message.xml

# Detailed validation with error messages
xmllint --schema schemas/SUTI_Message.xsd your_message.xml
```

---

## 📚 Additional Resources

- **[Message Reference](../docs/messages/README.md)** - Complete message specifications
- **[XSD Schema](../schemas/SUTI_Message.xsd)** - XML Schema Definition
- **[Validation Guide](../docs/schemas/validation-guide.md)** - Detailed validation instructions
- **[Getting Started](../docs/getting-started/README.md)** - Implementation guide

---

## 🤝 Contributing Examples

Have a useful SUTI message example?

1. Ensure it validates against the XSD schema
2. Remove any sensitive/production data
3. Use generic organization names (e.g., "ClientName", "ProviderName")
4. Add descriptive filename (e.g., `2000_ComplexOrder.xml`)
5. Submit a pull request

---

## ⚠️ Important Notes

### Encoding
- Always use **UTF-8 encoding**
- Required for Swedish characters (å, ä, ö)
- Specified in XML declaration: `<?xml version="1.0" encoding="UTF-8"?>`

### Schema Location
- Examples use relative path: `../../schemas/SUTI_Message.xsd`
- Adjust path based on your file location
- Or use absolute path in production

### Unique IDs
- All `idMsg` values must be unique
- Never reuse message IDs
- Typically use timestamp + sequence number

### Testing
- **Never use production IDs in test messages**
- Set up separate test environments
- Use clearly marked test organization names

---

[← Back to Main README](../README.md) | [View Documentation →](../docs/README.md)
