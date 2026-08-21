# JSON Examples

The `2026/` directory contains JSON Schema samples for SUTI messages.

## Purpose

These files are schema samples. They demonstrate the normative JSON representation
of the XSD master schema and are validated against the referenced schema. They are
not complete, end-to-end protocol fixtures: a `referencesTo.idMsg` value may identify
a message outside this repository's example set.

## Representation rules

- `msg` contains the JSON message header.
- Payload properties are siblings of `msg`.
- XSD repeatable elements are JSON arrays. For example,
  `referencesTo.idOrder` is an array because XSD permits multiple equivalent order IDs
  in the same `referencesTo` group.
- The JSON schema applies XSD-required fields and cardinality where JSON can express
  them. It does not add constraints absent from the XSD.
- `bulkLocation` retains its separately adopted JSON representation and is not a
  conversion target for the general message schema work.

## Coverage

Examples are organized by payload family rather than requiring a dedicated file for
every `msgType`. The full XSD-to-JSON message mapping and each message's canonical
payload family are documented in
[JSON Schema Completion Plan](../../docs/JSON_SCHEMA_COMPLETION_PLAN.md).
