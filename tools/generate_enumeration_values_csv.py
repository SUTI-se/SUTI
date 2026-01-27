#!/usr/bin/env python3
"""
Generate SUTI_Enumeration_Values.csv from SUTI_Enumerations.yaml

Reads the XPath-as-key YAML structure and generates CSV with format:
SUTI ValueNr;Language Nr;Language TextShort;SUTI_Attribute;SUTI_ValueText;SUTI_Object;SUTI_ValueDescription

Usage:
    python3 tools/generate_enumeration_values_csv.py

Author: Claude Code
Date: 2026-01-19
"""

import sys
import re
from pathlib import Path
from collections import OrderedDict


def extract_attribute_and_object_from_xpath(xpath):
    """
    Extract attribute name and object from XPath.

    For SUTI_Attribute: preserves @ prefix to distinguish attributes from elements.
    For SUTI_Object: returns the parent path (without the attribute).

    Examples:
        "content/@contentType" → ("@contentType", "content")
        "vehicle/capacity/seats/position/@direction" → ("@direction", "vehicle/capacity/seats/position")
        "payment/@paymentType" → ("@paymentType", "payment")
        "actionRequest/idAction" → ("idAction", "actionRequest")

    Returns:
        tuple: (attribute_name_with_prefix, object_path)
    """
    # Match attribute paths (ending with @attributeName)
    attr_match = re.match(r'(.+)/(@.+)$', xpath)
    if attr_match:
        object_path = attr_match.group(1)
        attribute_name = attr_match.group(2)  # Includes @ prefix
        return attribute_name, object_path

    # For element paths (no @), use the last segment as attribute
    parts = xpath.split('/')
    if len(parts) >= 2:
        attribute_name = parts[-1]
        object_path = '/'.join(parts[:-1])
        return attribute_name, object_path

    # Fallback
    return xpath, xpath


def read_yaml_enumerations(file_path):
    """
    Read XPath-as-key YAML structure manually.

    Returns:
        list: [{id, value_text, attribute, object, description, i18n}]
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
            attribute, obj = extract_attribute_and_object_from_xpath(current_xpath)

            current_entry = {
                'id': None,
                'value_text': current_value_name,
                'attribute': attribute,
                'object': obj,
                'description': '',
                'translations': {}
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
                current_entry['description'] = desc

            elif stripped in ('i18n:', 'translations:'):
                pass  # Start of i18n section

            elif ':' in stripped and current_entry:
                # Language translation
                parts = stripped.split(':', 1)
                lang = parts[0].strip().strip('"\'')
                text = parts[1].strip() if len(parts) > 1 else ''

                if lang in ['en', 'da', 'fi', 'no', 'sv'] and text:
                    current_entry['translations'][lang] = text

    # Save last entry
    if current_entry and 'id' in current_entry:
        entries.append(current_entry)

    return entries


def generate_csv(entries, output_file):
    """
    Generate CSV file from entries.

    Format: SUTI ValueNr;Language Nr;Language TextShort;SUTI_Attribute;SUTI_ValueText;SUTI_Object;SUTI_ValueDescription
    """
    # Language mapping
    lang_mapping = {
        'en': (1, 'ENG'),
        'da': (2, 'DAN'),
        'fi': (3, 'FIN'),
        'no': (4, 'NOR'),
        'sv': (5, 'SWE')
    }

    # Sort by ID
    entries_sorted = sorted(entries, key=lambda x: x['id'])

    # Generate rows
    rows = []
    header = 'SUTI ValueNr;Language Nr;Language TextShort;SUTI_Attribute;SUTI_ValueText;SUTI_Object;SUTI_ValueDescription'
    rows.append(header)

    for entry in entries_sorted:
        entry_id = entry['id']
        value_text = entry['value_text']
        attribute = entry['attribute']
        obj = entry['object']
        description = entry['description']
        translations = entry['translations']

        # For entries where value_text equals description AND the xpath points to
        # idError/@id or idAction/@id, the original CSV has empty SUTI_ValueText
        # since these are ID-only entries (identified solely by their numeric ID)
        display_value_text = value_text
        xpath_indicates_id_only = obj.endswith('idError') or obj.endswith('idAction')
        if value_text == description and xpath_indicates_id_only:
            display_value_text = ''

        # Generate 5 rows (one per language)
        for lang in ['en', 'da', 'fi', 'no', 'sv']:
            lang_nr, lang_text = lang_mapping[lang]

            # First row (English) has full columns with description
            if lang == 'en':
                # English row uses description field for SUTI_ValueDescription
                row = f"{entry_id};{lang_nr};{lang_text};{attribute};{display_value_text};{obj};{description}"
                rows.append(row)
            else:
                # Other languages: only add row if translation exists and is not '–'
                translation = translations.get(lang)
                if translation and translation != '–':  # Skip row if no translation or is '–'
                    row = f"{entry_id};{lang_nr};{lang_text};;{display_value_text};;{translation}"
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
    output_file = base_dir / "data" / "generated_SUTI_Enumeration_Values.csv"

    if not yaml_file.exists():
        print(f"❌ Error: File not found: {yaml_file}")
        sys.exit(1)

    print("=" * 80)
    print("Generate SUTI_Enumeration_Values.csv")
    print("=" * 80)
    print()

    print(f"Reading: {yaml_file}")
    entries = read_yaml_enumerations(yaml_file)
    print(f"✅ Found {len(entries)} entries")
    print()

    print(f"Generating: {output_file}")
    count = generate_csv(entries, output_file)
    print(f"✅ Generated {count * 5} rows ({count} IDs × 5 languages)")
    print()

    print("=" * 80)
    print("✅ Done!")
    print()
    print(f"Output: {output_file}")
    print(f"Compare with: diff {base_dir / 'data' / 'SUTI_Enumeration_Values.csv'} {output_file}")


if __name__ == "__main__":
    main()
