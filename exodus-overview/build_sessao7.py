import fitz
import os
import re

base = os.getcwd()
pdf_path = os.path.join(base, "pdf-sessoes", "sessao-8.pdf")
output_dir = os.path.join(base, "modulo-2")  # Session 7 is in modulo-2 based on index.html
img_dir = os.path.join(output_dir, "img", "sessao-7")
os.makedirs(img_dir, exist_ok=True)

# Render images for pages with >=8 drawings
doc = fitz.open(pdf_path)
for i, page in enumerate(doc):
    if len(page.get_drawings()) >= 8:
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        img_path = os.path.join(img_dir, f"p{i+1}-vector.png")
        if not os.path.exists(img_path):
            pix.save(img_path)
            print(f"Rendered {img_path}")
doc.close()

# Extract text
doc = fitz.open(pdf_path)
pages_text = [page.get_text() for page in doc]
doc.close()

# Load template
template_path = os.path.join(base, "modulo-1", "sessao-2.html")
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

# Split the template using the verified structure from build_sessao5.py
# Find div open
div_open_match = re.search(r'<div class="max-w-4xl mx-auto px-5 py-12 md:py-16">', template)
if not div_open_match:
    print("Could not find div open")
    exit(1)
div_open_start = div_open_match.start()
div_open_end = div_open_match.end()
div_open = template[div_open_start:div_open_end]

# Find div close after div open
after_div_open = template[div_open_end:]
div_close_match = re.search(r'</div>', after_div_open)
if not div_close_match:
    print("Could not find div close")
    exit(1)
div_close_start = div_open_end + div_close_match.start()
div_close_end = div_open_end + div_close_match.end()
div_close = template[div_close_start:div_close_end]

# Find script open after div close
after_div_close = template[div_close_end:]
script_match = re.search(r'<script>', after_div_close)
if not script_match:
    print("Could not find script open")
    exit(1)
script_start = div_close_end + script_match.start()
script_end = div_close_end + script_match.end()
script_open = template[script_start:script_end]

# Now we can split:
before_div = template[:div_open_start]
inner_content = template[div_open_end:div_close_start]  # between div open and div close
between_div_and_script = template[div_close_end:script_start]  # between div close and script open
after_script = template[script_end:]  # after script open

# Update the head title in before_div
# We want to extract the session title from the PDF text.
# The PDF first page contains:
#   Line 0: 'Class Notes: Exodus Overview'
#   Line 1: '21 of 80'
#   Line 2: 'Session 7: Let Them Go!'
# We'll look for a line that starts with 'Session 7:' or 'Sessão 7:' (case-insensitive)
first_page_text = pages_text[0].strip()
lines = [line.strip() for line in first_page_text.split('\n') if line.strip()]
title_line = None
for line in lines:
    if line.lower().startswith('session 7:') or line.lower().startswith('sessão 7:'):
        title_line = line
        break
if title_line is None:
    # Fallback: use the first non-empty line that is not the header and not the page number
    # Skip lines that look like 'Class Notes: ...' or contain a number like '21 of 80'
    for line in lines:
        if not line.startswith('Class Notes:') and not (' of ' in line and line.replace(' ', '').isdigit() is False):
            # Simple heuristic: if it's not the header and not the page number, take it.
            title_line = line
            break
if title_line is None:
    title_line = "Sessão 7"  # final fallback

new_title_pt = f"Sessão 7: {title_line}"
new_title_en = f"Session 7: {title_line}"
before_div = re.sub(r'<title>.*?</title>', f'<title>{new_title_pt}</title>', before_div)

# Update the localStorage key in after_script
after_script = after_script.replace("exodus-s2-lang", "exodus-s7-lang")

# Build new_inner
new_inner = ""
# Add the updated h1 and rule
new_inner += '    <h1 class="title reveal"><span class="lang-pt">' + new_title_pt + '</span><span class="lang-en">' + new_title_en + '</span></h1>\n'
new_inner += '    <hr class="rule">\n'

# Add each page's content
for i, text in enumerate(pages_text):
    # Escape HTML in text
    text_escaped = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # Replace newlines with <br> for simplicity
    text_escaped = text_escaped.replace('\n', '<br>')
    new_inner += '    <div class="page reveal">' + text_escaped + '</div>\n'
    # Check if there is an image for this page
    img_path = f"img/sessao-7/p{i+1}-vector.png"
    if os.path.exists(os.path.join(output_dir, img_path)):
        new_inner += '    <div class="table-img reveal"><img src="' + img_path + '" alt="Page ' + str(i+1) + ' diagram"><p class="caption"><span class="lang-pt">Êxodo X:Y. Tradução e Design Literário por Tim Mackie para BibleProject Classroom: José (2021).</span><span class="lang-en">Exodus X:Y. Translation and Literary Design by Tim Mackie for BibleProject Classroom: Joseph (2021).</span></p></div>\n'

# Reassemble the template
new_template = before_div + div_open + new_inner + div_close + between_div_and_script + script_open + after_script

# Write the output
output_path = os.path.join(output_dir, "sessao-7.html")
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(new_template)

print(f"Created {output_path}")