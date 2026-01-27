#!/usr/bin/env python3
"""
Generate SUTI_Attribute_List.csv from SUTI_Enumerations.yaml

Reads the XPath-as-key YAML structure and generates CSV with format:
AttributeId;Attribute;Usedin;Explanation;Danish;Finnish;Norwegian;Swedish

Usage:
    python3 tools/generate_attribute_list_csv.py

Author: Claude Code
Date: 2026-01-19
"""

import sys
import re
from pathlib import Path


def extract_attribute_from_xpath(xpath):
    """
    Extract attribute name from XPath.

    Examples:
        "content/@contentType" → "contentType"
        "vehicle/capacity/seats/position/@direction" → "direction"
        "payment/@paymentType" → "paymentType"

    Returns:
        str: attribute name
    """
    # Match attribute paths (ending with @attributeName)
    attr_match = re.match(r'.+/@(.+)$', xpath)
    if attr_match:
        return attr_match.group(1)

    # For element paths (no @), use the last segment
    parts = xpath.split('/')
    return parts[-1]


def convert_xpath_to_usedin_format(xpath):
    """
    Convert XPath format to CSV "Usedin" format.

    Preserves @ symbol to distinguish attributes from elements (standard XPath notation).

    Examples:
        "content/@contentType" → "content/@contentType"
        "vehicle/capacity/seats/position/@direction" → "vehicle/capacity/seats/position/@direction"
        "payment/@paymentType" → "payment/@paymentType"

    Returns:
        str: usedin path with @ preserved for attributes
    """
    # Preserve the XPath as-is (including @ for attributes)
    return xpath


def add_attribute_prefix(attribute_name, xpath):
    """
    Add prefix to attribute name based on XPath pattern to match original CSV format.

    Original CSV prefixes attribute names with their context for certain XPaths:
    - attributesDriver/attribute/idAttribute/@id → "attributesDriver {name}"
    - attributesVehicle/attribute/idAttribute/@id → "attributesVehicle {name}"
    - attributeContent/attribute/idAttribute/@id → "attributeContent {name}"
    - attributeAdress/attribute/idAttribute/@id → "adressContent {name}"

    Args:
        attribute_name: The bare attribute name from YAML
        xpath: The XPath this attribute belongs to

    Returns:
        str: Prefixed attribute name matching original CSV format
    """
    # Map XPath patterns to their prefix
    xpath_prefix_map = {
        'attributesDriver/attribute/idAttribute/@id': 'attributesDriver',
        'attributesVehicle/attribute/idAttribute/@id': 'attributesVehicle',
        'attributeContent/attribute/idAttribute/@id': 'attributeContent',
        'attributeAdress/attribute/idAttribute/@id': 'adressContent',  # Note: adressContent not attributeAdress
    }

    # Check if this XPath needs a prefix
    for xpath_pattern, prefix in xpath_prefix_map.items():
        if xpath == xpath_pattern:
            return f"{prefix} {attribute_name}"

    # No prefix needed
    return attribute_name


def read_yaml_enumerations(file_path):
    """
    Read XPath-as-key YAML structure manually.

    Returns:
        list: [{id, attribute, usedin, explanation, danish, finnish, norwegian, swedish}]
    """
    entries = []

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_enumerations = False
    current_xpath = None
    current_value_name = None
    current_entry = {}

    for line in lines:
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())

        if not stripped or stripped.startswith('#'):
            continue

        if stripped == 'enumerations:':
            in_enumerations = True
            continue

        if stripped.startswith('metadata:'):
            break

        if not in_enumerations:
            continue

        # XPath key (indent 2)
        if indent == 2 and stripped.endswith(':'):
            current_xpath = stripped[:-1].strip('"\'')
            continue

        # Value name (indent 4)
        if current_xpath and indent == 4 and stripped.endswith(':'):
            # Save previous entry
            if current_entry and 'id' in current_entry:
                entries.append(current_entry)

            current_value_name = stripped[:-1]
            # Strip quotes from numeric values like '1'
            if current_value_name.startswith("'") and current_value_name.endswith("'"):
                current_value_name = current_value_name[1:-1]
            attribute = extract_attribute_from_xpath(current_xpath)

            current_entry = {
                'id': None,
                'attribute': add_attribute_prefix(current_value_name, convert_xpath_to_usedin_format(current_xpath)),
                'usedin': convert_xpath_to_usedin_format(current_xpath),
                'explanation': '',
                'danish': '',
                'finnish': '',
                'norwegian': '',
                'swedish': ''
            }
            continue

        # Value properties (indent 6+)
        if current_entry and indent >= 6:
            if stripped.startswith('id:'):
                id_match = re.search(r'id:\s*(\d+)', stripped)
                if id_match:
                    current_entry['id'] = int(id_match.group(1))

            elif stripped.startswith('description:'):
                desc = stripped.split(':', 1)[1].strip()
                current_entry['explanation'] = desc

            elif stripped in ('i18n:', 'translations:'):
                pass  # Start of i18n section

            elif ':' in stripped and current_entry:
                # Language translation
                parts = stripped.split(':', 1)
                lang = parts[0].strip().strip('"\'')
                text = parts[1].strip() if len(parts) > 1 else ''

                if lang == 'da' and text:
                    current_entry['danish'] = text
                elif lang == 'fi' and text:
                    current_entry['finnish'] = text
                elif lang == 'no' and text:
                    current_entry['norwegian'] = text
                elif lang == 'sv' and text:
                    current_entry['swedish'] = text

    # Save last entry
    if current_entry and 'id' in current_entry:
        entries.append(current_entry)

    return entries


def generate_csv(entries, output_file):
    """
    Generate CSV file from entries.

    Format: AttributeId;Attribute;Usedin;Explanation;Danish;Finnish;Norwegian;Swedish
    """
    # Sort by ID
    entries_sorted = sorted(entries, key=lambda x: x['id'])

    # Generate rows
    rows = []
    header = 'AttributeId;Attribute;Usedin;Explanation;Danish;Finnish;Norwegian;Swedish'
    rows.append(header)

    for entry in entries_sorted:
        entry_id = entry['id']
        attribute = entry['attribute']
        usedin = entry['usedin']
        explanation = entry['explanation']
        danish = entry['danish'] or '–'
        finnish = entry['finnish'] or '–'
        norwegian = entry['norwegian'] or '–'
        swedish = entry['swedish'] or '–'

        row = f"{entry_id};{attribute};{usedin};{explanation};{danish};{finnish};{norwegian};{swedish}"
        rows.append(row)

    # Write with UTF-8 BOM
    with open(output_file, 'w', encoding='utf-8-sig') as f:
        f.write('\n'.join(rows))
        f.write('\n')  # Trailing newline

    return len(entries_sorted)


def main():
    """Main execution."""
    base_dir = Path(__file__).parent.parent
    yaml_file = base_dir / "data" / "SUTI_Enumerations.yaml"
    output_file = base_dir / "data" / "generated_SUTI_Attribute_List.csv"

    if not yaml_file.exists():
        print(f"❌ Error: File not found: {yaml_file}")
        sys.exit(1)

    print("=" * 80)
    print("Generate SUTI_Attribute_List.csv")
    print("=" * 80)
    print()

    print(f"Reading: {yaml_file}")
    entries = read_yaml_enumerations(yaml_file)
    print(f"✅ Found {len(entries)} entries")
    print()

    print(f"Generating: {output_file}")
    count = generate_csv(entries, output_file)
    print(f"✅ Generated {count} rows")
    print()

    print("=" * 80)
    print("✅ Done!")
    print()
    print(f"Output: {output_file}")
    print(f"Compare with: diff {base_dir / 'data' / 'SUTI_Attribute_List.csv'} {output_file}")


if __name__ == "__main__":
    main()
