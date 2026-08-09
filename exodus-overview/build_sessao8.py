import fitz
import os
import re

# Configuration
N = 8
pdf_path = os.path.join(os.getcwd(), "pdf-sessoes", f"sessao-{N+1}.pdf")
template_path = os.path.join(os.getcwd(), "modulo-1", "sessao-2.html")
output_dir = os.path.join(os.getcwd(), "modulo-2")
img_dir = os.path.join(output_dir, "img", f"sessao-{N}")
os.makedirs(img_dir, exist_ok=True)
output_path = os.path.join(output_dir, f"sessao-{N}.html")

# Extract text and render images for pages with >=8 drawings
doc = fitz.open(pdf_path)
pages_text = []
for i, page in enumerate(doc):
    pages_text.append(page.get_text())
    if len(page.get_drawings()) >= 8:
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        img_path = os.path.join(img_dir, f"p{i+1}-vector.png")
        if not os.path.exists(img_path):
            pix.save(img_path)
            print(f"Rendered {img_path}")
doc.close()

# Determine title from PDF (first page)
doc = fitz.open(pdf_path)
first_page_text = doc[0].get_text()
doc.close()
# Look for the title line
lines = first_page_text.split('\n')
pt_title = None
en_title = None
for line in lines:
    if line.startswith("Session 8:"):
        en_title = line.strip()
        # Look for Portuguese line nearby (maybe previous line)
        idx = lines.index(line)
        if idx > 0 and "Sessão 8:" in lines[idx-1]:
            pt_title = lines[idx-1].strip()
        elif idx < len(lines)-1 and "Sessão 8:" in lines[idx+1]:
            pt_title = lines[idx+1].strip()
        break
if not pt_title:
    # Fallback: assume pattern from previous sessions
    pt_title = "Sessão 8: Sinais e Maravilhas"
if not en_title:
    en_title = "Session 8: Signs and Wonders"

# Load template
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

# Split template using the verified structure from build_sessao5.py
# Need to escape quotes properly for regex
div_open_match = re.search(r'<div class="max-w-4xl mx-auto px-5 py-12 md:py-16">', template)
if not div_open_match:
    print("Could not find div open")
    # Debug: show what we're looking for
    print("Looking for:", repr('<div class="max-w-4xl mx-auto px-5 py-12 md:py-16">'))
    # Show first few lines that contain div
    for i, line in enumerate(template.split('\n')[:20]):
        if 'div class' in line:
            print(f"Line {i+1}: {line.strip()}")
    exit(1)
div_open_start = div_open_match.start()
div_open_end = div_open_match.end()
div_open = template[div_open_start:div_open_end]

after_div_open = template[div_open_end:]
div_close_match = re.search(r'</div>', after_div_open)
if not div_close_match:
    print("Could not find div close")
    exit(1)
div_close_start = div_open_end + div_close_match.start()
div_close_end = div_open_end + div_close_match.end()
div_close = template[div_close_start:div_close_end]

after_div_close = template[div_close_end:]
script_match = re.search(r'<script>', after_div_close)
if not script_match:
    print("Could not find script open")
    exit(1)
script_start = div_close_end + script_match.start()
script_end = div_close_end + script_match.end()
script_open = template[script_start:script_end]

before_div = template[:div_open_start]
inner_content = template[div_open_end:div_close_start]
between_div_and_script = template[div_close_end:script_start]
after_script = template[script_end:]

# Update the head title in before_div
before_div = re.sub(r'<title>.*?</title>', f'<title>{pt_title}</title>', before_div)

# Update the localStorage key in after_script
after_script = after_script.replace("exodus-s2-lang", f"exodus-s{N}-lang")

# Build new_inner
new_inner = ""
# Add the updated h1 and rule
new_inner += '    <h1 class="title reveal"><span class="lang-pt">' + pt_title + '</span><span class="lang-en">' + en_title + '</span></h1>\\n'
new_inner += '    <hr class="rule">\\n'

# Add each page's content
for i, text in enumerate(pages_text):
    # Escape HTML in text
    text_escaped = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # Replace newlines with <br> for simplicity
    text_escaped = text_escaped.replace('\n', '<br>')
    new_inner += '    <div class="page reveal">' + text_escaped + '</div>\\n'
    # Check if there is an image for this page
    img_path = f"img/sessao-{N}/p{i+1}-vector.png"
    if os.path.exists(os.path.join(output_dir, img_path)):
        new_inner += '    <div class="table-img reveal"><img src="' + img_path + '" alt="Page ' + str(i+1) + ' diagram"><p class="caption"><span class="lang-pt">Êxodo X:Y. Tradução e Design Literário por Tim Mackie para BibleProject Classroom: José (2021).</span><span class="lang-en">Exodus X:Y. Translation and Literary Design by Tim Mackie for BibleProject Classroom: Joseph (2021).</span></p></div>\\n'

# Reassemble the template
new_template = before_div + div_open + new_inner + div_close + between_div_and_script + script_open + after_script

# Write the output
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(new_template)

print(f"Created {output_path}")