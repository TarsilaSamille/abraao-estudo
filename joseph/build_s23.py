import fitz  # PyMuPDF
import os
import re

# Configuration
SESSION_NUM = 23
PDF_PATH = f"pdf-sessoes/sessao-{SESSION_NUM + 1}.pdf"  # sessao-24.pdf
TEMPLATE_PATH = "modulo-1/sessao-2.html"
# Determine module from session number
MODULE_RANGES = [
    (1, 4, 1),
    (5, 9, 2),
    (10, 12, 3),
    (13, 17, 4),
    (18, 20, 5),
    (21, 25, 6),
    (26, 29, 7)
]
MODULE_POS = None
for start, end, pos in MODULE_RANGES:
    if start <= SESSION_NUM <= end:
        MODULE_POS = pos
        break
if MODULE_POS is None:
    raise ValueError(f"Session {SESSION_NUM} not in any module range")
OUTPUT_DIR = f"modulo-{MODULE_POS}"
IMG_DIR = os.path.join(OUTPUT_DIR, "img", f"sessao-{SESSION_NUM}")
os.makedirs(IMG_DIR, exist_ok=True)

# Load PDF
doc = fitz.open(PDF_PATH)
print(f"PDF has {doc.page_count} pages")

# Extract title from first page (first non-empty line)
first_page = doc.load_page(0)
text_first = first_page.get_text("text")
lines = [line.strip() for line in text_first.split('\n') if line.strip()]
title_pt = lines[0] if lines else f"Sessão {SESSION_NUM}"
# We'll also try to get an English title? Not available in PDF. We'll use a placeholder.
title_en = f"Session {SESSION_NUM}: [English title]"

# Process each page
page_html_snippets = []
for i in range(doc.page_count):
    page = doc.load_page(i)
    text = page.get_text("text")
    drawings = page.get_drawings()
    num_drawings = len(drawings)
    print(f"Page {i+1}: {num_drawings} drawings")
    
    # Clean up text: remove extra whitespace, but keep line breaks for <br>
    # We'll convert newlines to <br> and wrap in a div
    # If there are >=8 drawings, we render the page as a vector image
    if num_drawings >= 8:
        # Render page as vector image at 2x scale
        mat = fitz.Matrix(2.0, 2.0)  # 2x scale
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img_filename = f"p{i+1}-vector.png"
        img_path = os.path.join(IMG_DIR, img_filename)
        pix.save(img_path)
        # HTML snippet for image
        # Note: the path in HTML should be relative to the HTML file.
        # The HTML file will be in OUTPUT_DIR, so we need to go up one level then into img/sessao-23/
        # So: ../img/sessao-23/p1-vector.png
        relative_img_path = f"../img/sessao-{SESSION_NUM}/{img_filename}"
        # Caption (placeholder)
        caption_pt = "Gênesis X:Y. Tradução e Design Literário por Tim Mackie para BibleProject Classroom: José (2021)."
        caption_en = "Genesis X:Y. Translation and Literary Design by Tim Mackie for BibleProject Classroom: Joseph (2021)."
        snippet = f'''<div class="table-img reveal">
  <img src="{relative_img_path}" alt="Page {i+1} diagram">
  <p class="caption"><span class="lang-pt">{caption_pt}</span><span class="lang-en">{caption_en}</span></p>
</div>'''
        page_html_snippets.append(snippet)
    else:
        # Text only: convert newlines to <br> and wrap in a div
        # We'll also escape HTML characters? We'll assume the text is safe.
        # Replace newlines with <br>
        text_br = text.replace('\n', '<br>')
        snippet = f'<div class="page reveal">{text_br}</div>'
        page_html_snippets.append(snippet)

doc.close()

# Read template
with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    template = f.read()

# Replace title in <title> tag
# We want: "Sessão 23: [title from PDF]" (Portuguese) in the title tag.
new_title_pt = f"Sessão {SESSION_NUM}: {title_pt}"
title_pattern = r'<title>.*?</title>'
new_title_tag = f'<title>{new_title_pt}</title>'
template = re.sub(title_pattern, new_title_tag, template)

# Replace the h1 tag content
# We'll keep the two spans for Portuguese and English.
new_h1_content = f'<span class="lang-pt">Sessão {SESSION_NUM}: {title_pt}</span><span class="lang-en">Session {SESSION_NUM}: {title_en}</span>'
h1_pattern = r'(<h1 class="title reveal">)(.*?)(</h1>)'
template = re.sub(h1_pattern, r'\1' + new_h1_content + r'\3', template, flags=re.DOTALL)

# Replace the localStorage key in the JavaScript function and the call
# We need to change 'joseph-s2-lang' to 'joseph-s23-lang' in two places:
# 1. Inside the setLang function: localStorage.setItem('joseph-s2-lang',l)
# 2. At the bottom: setLang(localStorage.getItem('joseph-s2-lang')||'pt');
# We'll do two separate replacements.

# First, replace inside the function
func_pattern = r"(localStorage\.setItem\(')joseph-s\d+-lang(',\s*l\))"
new_func = rf"\1joseph-s{SESSION_NUM}-lang\2"
template = re.sub(func_pattern, new_func, template)

# Second, replace the call at the bottom
call_pattern = r"(setLang\(localStorage\.getItem\(')joseph-s\d+-lang('\)\|\|'pt'\))"
new_call = rf"\1joseph-s{SESSION_NUM}-lang\2"
template = re.sub(call_pattern, new_call, template)

# Replace the content div
content_pattern = r'(<div class="max-w-4xl mx-auto px-5 py-12 md:py-16">)(.*?)(</div>)'
new_content = '\n'.join(page_html_snippets)
template = re.sub(content_pattern, r'\1' + new_content + r'\3', template, flags=re.DOTALL)

# Write the output
output_path = os.path.join(OUTPUT_DIR, f"sessao-{SESSION_NUM}.html")
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(template)

print(f"Session {SESSION_NUM} written to {output_path}")
print(f"Images saved to {IMG_DIR}")
