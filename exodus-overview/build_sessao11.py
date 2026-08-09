import fitz
import os
import re

# Use the current working directory (which is /Users/macbook/GitHub/biblia-estudo/exodus-overview)
BASE_DIR = os.getcwd()
PDF_PATH = os.path.join(BASE_DIR, 'pdf-sessoes', 'sessao-12.pdf')
TEMPLATE_PATH = os.path.join(BASE_DIR, 'modulo-1', 'sessao-2.html')
OUTPUT_DIR = os.path.join(BASE_DIR, 'modulo-2')
IMG_DIR = os.path.join(OUTPUT_DIR, 'img', 'sessao-11')
os.makedirs(IMG_DIR, exist_ok=True)

# Extract text and render images
doc = fitz.open(PDF_PATH)
pages_text = []
for i, page in enumerate(doc):
    pages_text.append(page.get_text())
    if len(page.get_drawings()) >= 8:
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        img_path = os.path.join(IMG_DIR, f'p{i+1}-vector.png')
        if not os.path.exists(img_path):
            pix.save(img_path)
            print(f'Rendered {img_path}')
doc.close()

# Load template
with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    template = f.read()

# Split the template
pattern = r'(.*?)(<div class=\"max-w-4xl mx-auto px-5 py-12 md:py-16\">)(.*?)(</div>\\s*<script>)(.*)'
match = re.search(pattern, template, re.DOTALL)
if not match:
    print('Could not find the div pattern in the template')
    exit(1)

before_div = match.group(1)
div_open = match.group(2)
inner_content = match.group(3)
div_close_script = match.group(4)
after_script = match.group(5)

# Get title from PDF first page
first_page_text = pages_text[0]
title_pt = None
title_en = None
for line in first_page_text.split('\n'):
    line = line.strip()
    if line.startswith('Session 11:'):
        title_en = line[len('Session 11:'):].strip()
    elif line.startswith('Sessão 11:'):
        title_pt = line[len('Sessão 11:'):].strip()

# Fallback to known titles if not found in PDF
if not title_en:
    title_en = 'Sea Crossing'
if not title_pt:
    title_pt = 'Travessia do Mar'

# Update the head title in before_div
new_title = f'Sessão 11: {title_pt}'
before_div = re.sub(r'<title>.*?</title>', f'<title>{new_title}</title>', before_div)

# Update the localStorage key in after_script
after_script = after_script.replace('exodus-s2-lang', 'exodus-s11-lang')

# Build new_inner
new_inner = ''
# Add the updated h1 and rule
new_inner += '    <h1 class=\"title reveal\"><span class=\"lang-pt\">Sessão 11: ' + title_pt + '</span><span class=\"lang-en\">Session 11: ' + title_en + '</span></h1>\\n'
new_inner += '    <hr class=\"rule\">\\n'

# Add each page's content
for i, text in enumerate(pages_text):
    # Escape HTML in text
    text_escaped = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # Replace newlines with <br> for simplicity
    text_escaped = text_escaped.replace('\\n', '<br>')
    new_inner += '    <div class=\"page reveal\">' + text_escaped + '</div>\\n'
    # Check if there is an image for this page
    img_path = f'img/sessao-11/p{i+1}-vector.png'
    if os.path.exists(os.path.join(OUTPUT_DIR, img_path)):
        new_inner += '    <div class=\"table-img reveal\"><img src=\"' + img_path + '\" alt=\"Page ' + str(i+1) + ' diagram\"><p class=\"caption\"><span class=\"lang-pt\">Gênesis X:Y. Tradução e Design Literário por Tim Mackie para BibleProject Classroom: José (2021).</span><span class=\"lang-en\">Genesis X:Y. Translation and Literary Design by Tim Mackie for BibleProject Classroom: Joseph (2021).</span></p></div>\\n'

# Reassemble the template
new_template = before_div + div_open + new_inner + div_close_script + after_script

# Write the output
output_path = os.path.join(OUTPUT_DIR, 'sessao-11.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(new_template)

print(f'Created {output_path}')