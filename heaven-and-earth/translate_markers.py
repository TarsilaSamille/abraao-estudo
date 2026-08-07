#!/usr/bin/env python3
"""Extract __TR__:...__/TR__ markers from all sessao HTML files and help translate them."""

import re
import os
import json
from collections import OrderedDict

BASE = "/Users/macbook/GitHub/biblia-estudo/heaven-and-earth"

def find_all_markers(base):
    """Find all __TR__ markers across all sessao files."""
    markers = {}  # english_text -> list of (filepath, full_marker)
    for root, dirs, files in os.walk(base):
        for f in sorted(files):
            if not f.startswith("sessao-") or not f.endswith(".html"):
                continue
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as fh:
                content = fh.read()
            
            # Find all __TR__:...__/TR__ markers
            pattern = r'__TR__:(.*?)__/TR__'
            matches = list(re.finditer(pattern, content))
            if matches:
                for m in matches:
                    eng_text = m.group(1)
                    full_marker = m.group(0)
                    markers.setdefault(eng_text, []).append((filepath, full_marker))
    
    return markers

markers = find_all_markers(BASE)
print(f"Total unique English texts to translate: {len(markers)}")
total_occurrences = sum(len(v) for v in markers.values())
print(f"Total marker occurrences: {total_occurrences}")
print()

# Print all unique texts with their count
for i, (eng, files) in enumerate(sorted(markers.items()), 1):
    count = len(files)
    # Show first 120 chars
    eng_short = eng[:120] + "..." if len(eng) > 120 else eng
    print(f"{i:3d}. [{count:2d}x] {eng_short}")