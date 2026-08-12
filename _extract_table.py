#!/usr/bin/env python3
"""Find which PDF page contains a given table title, and dump its text + a cropped image.
Usage: python3 _extract_table.py <course> <sessao-html> <title-substr>
Prints page index and extracts text from that page (pymupdf)."""
import sys, os, re, glob
import fitz  # pymupdf

course, sessao_html, title = sys.argv[1], sys.argv[2], sys.argv[3]
root = os.path.join(course, 'pdf-sessoes')
# find the pdf for this sessao
pdfs = glob.glob(os.path.join(root, sessao_html.replace('sessao-', 'sessao-') + '.pdf'))
if not pdfs:
    pdfs = glob.glob(os.path.join(root, '*.pdf'))
    # try match by number
    m = re.search(r'sessao-(\d+)', sessao_html)
    num = m.group(1) if m else None
    pdfs = [p for p in pdfs if num and os.path.basename(p).startswith('sessao-'+num)] or pdfs
if not pdfs:
    print("NO PDF FOUND in", root); sys.exit(1)
pdf = pdfs[0]
print("PDF:", pdf)
doc = fitz.open(pdf)
found = []
for i, page in enumerate(doc):
    txt = page.get_text()
    if title.lower() in txt.lower():
        found.append((i, txt))
print(f"matches: {len(found)}")
for i, txt in found:
    print(f"\n===== PAGE {i} =====")
    print(txt[:3000])
