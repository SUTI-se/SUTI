#!/usr/bin/env python3
"""
Convert SUTI_Messages.txt to modular Markdown files organized by message blocks.

This script parses the extracted PDF text and creates:
- docs/messages/README.md (overview)
- docs/messages/block-XX-name.md (one per block)

Each block file contains all messages in that block with proper formatting,
links to XML examples, and validation snippets.
"""

import re
from pathlib import Path
from typing import List, Dict, Optional

# Map block numbers to descriptive names
BLOCK_NAMES = {
    10: "resource",
    20: "order",
    30: "dispatch",
    40: "traffic",
    50: "communication",
    60: "report",
    70: "technical",
    80: "accounting",
    90: "versions"
}

BLOCK_TITLES = {
    10: "Dynamic Resource Utilization",
    20: "Order Management",
    30: "Dispatch",
    40: "Traffic Control",
    50: "Communication",
    60: "Reports",
    70: "Technical Control",
    80: "Accounting",
    90: "Alterations (Version History)"
}

def parse_messages_file(txt_path: Path) -> Dict[int, Dict]:
    """Parse SUTI_Messages.txt and extract block and message information."""

    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = {}
    current_block = None
    current_block_desc = ""

    # Find block headers: "1     BLOCK 10: DYNAMIC RESOURCE UTILIZATION"
    block_pattern = r'^\d+\s+BLOCK (\d+):\s+(.+)$'

    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Check for block header
        block_match = re.match(block_pattern, line)
        if block_match:
            block_num = int(block_match.group(1))
            block_title = block_match.group(2).strip()

            # Get block description (next few non-empty lines)
            desc_lines = []
            j = i + 1
            while j < len(lines) and j < i + 10:
                desc_line = lines[j].strip()
                if desc_line and not desc_line.startswith('Page') and not re.match(r'^\d+\.\d+', desc_line):
                    desc_lines.append(desc_line)
                elif desc_line.startswith('1.1') or desc_line.startswith('2.1'):  # First message
                    break
                j += 1

            current_block = block_num
            current_block_desc = ' '.join(desc_lines)

            blocks[block_num] = {
                'title': block_title,
                'description': current_block_desc,
                'messages': []
            }

        i += 1

    return blocks

def find_xml_examples(msg_number: str) -> List[str]:
    """Find XML example files for a given message number."""
    examples_dir = Path('/Users/martin/Documents/GitHub/SUTI-worktree/examples/XML')

    if not examples_dir.exists():
        return []

    # Look for files matching the message number
    examples = []
    for xml_file in examples_dir.glob('*.xml'):
        if xml_file.stem.startswith(msg_number):
            examples.append(xml_file.name)

    return sorted(examples)

def generate_block_markdown(block_num: int, block_data: Dict) -> str:
    """Generate Markdown content for a message block."""

    block_name = BLOCK_NAMES.get(block_num, f"block-{block_num}")
    title = block_data['title']
    description = block_data['description']

    md = f"""# Block {block_num}: {title}

> {description}

---

## Overview

**Block {block_num}** contains messages for {title.lower()}.

**Message Range**: {block_num}000-{block_num}999

---

## Messages in this Block

"""

    # TODO: Add actual messages here
    # For now, placeholder
    md += """
*Message conversion in progress. This block will be populated with detailed message specifications.*

**Available in this block**:
- Message specifications from SUTI_Messages.pdf
- XML examples (where available)
- Validation instructions

---

## XML Examples

Check the [Examples Catalog](../../examples/README.md) for validated XML examples in this block.

---

## Validation

All messages in this block can be validated using:

```bash
xmllint --noout --schema schemas/SUTI_Message.xsd examples/XML/XXXX.xml
```

---

## Additional Resources

- **[SUTI Messages PDF](../SUTI_Messages.pdf)** - Original specification
- **[Message Flows](../message-flows/block-{block_num:02d}-flows.md)** - Visual flow diagrams
- **[Use Cases](../use-cases/README.md)** - Real-world scenarios

---

[← Back to Messages](README.md) | [Documentation Hub →](../README.md)
"""

    return md

def main():
    """Main conversion function."""

    # Paths
    worktree = Path('/Users/martin/Documents/GitHub/SUTI-worktree')
    txt_file = worktree / 'docs/SUTI_Messages.txt'
    messages_dir = worktree / 'docs/messages'

    # Create messages directory
    messages_dir.mkdir(parents=True, exist_ok=True)

    print("Parsing SUTI_Messages.txt...")
    blocks = parse_messages_file(txt_file)

    print(f"Found {len(blocks)} blocks")

    # Generate block files
    for block_num in sorted(blocks.keys()):
        block_data = blocks[block_num]
        block_name = BLOCK_NAMES.get(block_num, f"block-{block_num}")

        output_file = messages_dir / f"block-{block_num:02d}-{block_name}.md"

        print(f"Generating {output_file.name}...")
        md_content = generate_block_markdown(block_num, block_data)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)

    print("\n✅ Block files created!")
    print(f"📁 Output directory: {messages_dir}")
    print("\nNext: Create docs/messages/README.md overview file")

if __name__ == '__main__':
    main()
