import fitz
import os

base = os.getcwd()
pdf_path = os.path.join(base, "pdf-sessoes", "sessao-23.pdf")
# Session 22 is in modulo-3 based on index.html MODULES array (15-22)
output_dir = os.path.join(base, "modulo-3")
img_dir = os.path.join(output_dir, "img", "sessao-22")
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

# Extract text per page
doc = fitz.open(pdf_path)
pages_text = [page.get_text() for page in doc]
doc.close()

# Load template from modulo-1/sessao-2.html
template_path = os.path.join(base, "modulo-1", "sessao-2.html")
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

# Split the template using known strings
div_open_str = '<div class="max-w-4xl mx-auto px-5 py-12 md:py-16">'
div_open_idx = template.find(div_open_str)
if div_open_idx == -1:
    print("Could not find div open")
    exit(1)
div_open_end = div_open_idx + len(div_open_str)

div_close_str = '</div>'
div_close_idx = template.find(div_close_str, div_open_end)
if div_close_idx == -1:
    print("Could not find div close")
    exit(1)
div_close_end = div_close_idx + len(div_close_str)

script_open_str = '<script>'
script_open_idx = template.find(script_open_str, div_close_end)
if script_open_idx == -1:
    print("Could not find script open")
    exit(1)
script_open_end = script_open_idx + len(script_open_str)

before_div = template[:div_open_idx]
between_div_and_script = template[div_close_end:script_open_idx]
after_script = template[script_open_end:]

# Extract the title from the PDF first page
first_page_text = pages_text[0].strip()
lines = [line.strip() for line in first_page_text.split('\\n') if line.strip()]
title_line = None
for line in lines:
    if line.lower().startswith('session 22:') or line.lower().startswith('sessão 22:'):
        title_line = line
        break
if title_line is None:
    # Fallback: use the first non-empty line that is not the header and not the page number
    for line in lines:
        if not line.startswith('Class Notes:') and not (' of ' in line and line.replace(' ', '').isdigit() is False):
            title_line = line
            break
if title_line is None:
    title_line = "Session 22: Covenant Ratified"  # from actual PDF

# Get the base title (after the colon)
if ':' in title_line:
    base_title = title_line.split(':', 1)[1].strip()
else:
    base_title = title_line

# Build Portuguese and English titles
pt_title = f"Sessão 22: {base_title}"
en_title = f"Session 22: {base_title}"

# Update the head title in before_div
title_open = before_div.find('<title>')
title_close = before_div.find('</title>', title_open)
if title_open != -1 and title_close != -1:
    before_div = before_div[:title_open+7] + pt_title + before_div[title_close:]
else:
    pass

# Update the localStorage key in after_script
after_script = after_script.replace("exodus-s2-lang", "exodus-s22-lang")

# Build new_inner
new_inner = ''
new_inner += '    <h1 class="title reveal"><span class="lang-pt">' + pt_title + '</span><span class="lang-en">' + en_title + '</span></h1>\\n'
new_inner += '    <hr class="rule">\\n'

# Add each page's content
for i, text in enumerate(pages_text):
    # Escape HTML in text
    text_escaped = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # Replace newlines with <br> for simplicity
    text_escaped = text_escaped.replace('\\n', '<br>')
    new_inner += '    <div class="page reveal">' + text_escaped + '</div>\\n'
    # Check if there is an image for this page
    img_path = f"img/sessao-22/p{i+1}-vector.png"
    if os.path.exists(os.path.join(output_dir, img_path)):
        new_inner += '    <div class="table-img reveal"><img src="' + img_path + '" alt="Page ' + str(i+1) + ' diagram"><p class="caption"><span class="lang-pt">�������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������Êxodo X:Y. Tradução e Design Literário por Tim Mackie para BibleProject Classroom: José (2021).</span><span class="lang-en">Exodus X:Y. Translation and Literary Design by Tim Mackie for BibleProject Classroom: Joseph (2021).</span></p></div>\\n'

# Reassemble the template
new_template = before_div + div_open_str + new_inner + div_close_str + between_div_and_script + script_open_str + after_script

# Write the output
output_path = os.path.join(output_dir, "sessao-22.html")
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(new_template)

print(f"Created {output_path}")