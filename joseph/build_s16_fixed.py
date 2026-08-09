#!/usr/bin/env python3
import fitz
import os
import re
from pathlib import Path

# Paths
base_dir = Path('/Users/macbook/GitHub/biblia-estudo/joseph')
pdf_path = base_dir / 'pdf-sessoes' / 'sessao-17.pdf'
template_path = base_dir / 'modulo-1' / 'sessao-2.html'
output_dir = None  # to be determined
output_path = None

# 1. Open PDF and get title
doc = fitz.open(pdf_path)
first_page = doc[0]
text = first_page.get_text()
# Extract title: first line that starts with "Session 16:"
lines = text.split('\n')
title_line = None
for line in lines:
    if line.strip().startswith('Session 16:'):
        title_line = line.strip()
        break
if not title_line:
    # fallback
    title_line = 'Session 16: Judah\'s Offering'
english_title = title_line  # e.g., "Session 16: Judah’s Offering"
# Portuguese translation: we'll translate Judah’s Offering to "Oferta de Judá"
portuguese_title = 'Sessão 16: Oferta de Judá'
# If you want to keep the exact PDF title but in Portuguese? We'll use translation.

# 2. Determine modulo directory from index.html
index_path = base_dir / 'index.html'
index_content = index_path.read_text()
# Find MODULES array
import json
# Extract the array using regex
match = re.search(r'const MODULES = (\\[.*?\\]);', index_content, re.DOTALL)
if match:
    modules_str = match.group(1)
    modules = json.loads(modules_str)
else:
    # fallback: we know session 16 is in module 4
    modules = [
        {"pos": 1, "first": 1, "last": 4},
        {"pos": 2, "first": 5, "last": 9},
        {"pos": 3, "first": 10, "last": 12},
        {"pos": 4, "first": 13, "last": 17},
        {"pos": 5, "first": 18, "last": 20},
        {"pos": 6, "first": 21, "last": 25},
        {"pos": 7, "first": 26, "last": 29}
    ]

target_module = None
for m in modules:
    if m['first'] <= 16 <= m['last']:
        target_module = m
        break
if not target_module:
    raise ValueError('Session 16 not found in any module')
mod_pos = target_module['pos']
output_dir = base_dir / f'modulo-{mod_pos}'
output_path = output_dir / f'sessao-16.html'

# 3. Ensure image directory exists
img_dir = output_dir / 'img' / 'sessao-16'
img_dir.mkdir(parents=True, exist_ok=True)

# 4. Render diagrams for pages with >=8 drawings at 2x scale
zoom = 2  # 2x scale
mat = fitz.Matrix(zoom, zoom)
for page_num in range(len(doc)):
    page = doc[page_num]
    drawings = page.get_drawings()
    if len(drawings) >= 8:
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img_filename = f'p{page_num+1}-vector.png'
        img_path = img_dir / img_filename
        pix.save(str(img_path))
        print(f'Saved {img_path}')
    else:
        print(f'Skipping page {page_num+1} with {len(drawings)} drawings')

# 5. Read template
template = template_path.read_text()

# 6. Update title tag
template = re.sub(r'<title>.*?</title>', f'<title>{portuguese_title}</title>', template, flags=re.DOTALL)

# 7. Update h1 tag: replace the entire h1 block
new_h1 = f'<h1 class="title reveal"><span class="lang-pt">{portuguese_title}</span><span class="lang-en">{english_title}</span></h1>'
template = re.sub(r'<h1 class="title reveal">.*?</h1>', new_h1, template, flags=re.DOTALL)

# 8. Update localStorage key in JavaScript
# Change 'joseph-s2-lang' to 'joseph-s16-lang' in two places:
# a) localStorage.setItem('joseph-s2-lang',l)
template = re.sub(r"localStorage\.setItem\('joseph-s2-lang',l\)", "localStorage.setItem('joseph-s16-lang',l)", template)
# b) setLang(localStorage.getItem('joseph-s2-lang')||'pt');
template = re.sub(r"setLang\(localStorage\.getItem\('joseph-s2-lang'\)\|\|'pt'\)", "setLang(localStorage.getItem('joseph-s16-lang')||'pt')", template)

# 9. Write output
output_path.write_text(template)
print(f'Generated {output_path}')