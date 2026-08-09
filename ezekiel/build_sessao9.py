import fitz
import os
import html

# Configuration
N = 9
pdf_path = f'pdf-sessoes/sessao-{N+1}.pdf'  # sessao-10.pdf
template_path = 'modulo-1/sessao-2.html'
output_path = 'modulo-2/sessao-9.html'
image_output_dir = 'modulo-2/img/sessao-9'

# Ensure output directories exist
os.makedirs(image_output_dir, exist_ok=True)

# Extract text and render diagrams from PDF
doc = fitz.open(pdf_path)
pages_text = []
images_info = []  # list of (page_num, image_path)

for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    pages_text.append(text)
    
    # Check for drawings
    drawings = page.get_drawings()
    if len(drawings) >= 8:
        # Render the page as a PNG at 2x scale
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        img_filename = f'p{page_num+1}-vector.png'
        img_path = os.path.join(image_output_dir, img_filename)
        if not os.path.exists(img_path):
            pix.save(img_path)
            print(f'Rendered {img_path}')
        images_info.append((page_num, img_path))

doc.close()

# Determine titles from PDF first line
first_line = pages_text[0].strip() if pages_text else ""
# Extract English title: assume format "Session 9: ..."
import re
match = re.match(r'Session\s+\d+:\s+(.+)', first_line, re.IGNORECASE)
if match:
    title_en = f'Session 9: {match.group(1).strip()}'
    # Create Portuguese title by translating known parts
    pt_translation = match.group(1).strip()
    pt_translation = re.sub(r'Corrupted Temple Vision', 'Visão do Templo Corrompido', pt_translation, flags=re.IGNORECASE)
    title_pt = f'Sessão 9: {pt_translation}'
else:
    # Fallback
    title_en = 'Session 9: Corrupted Temple Vision'
    title_pt = 'Sessão 9: Visão do Templo Corrompido'

# Read the template
with open(template_path, 'r') as f:
    template = f.read()

# Update the title tag
title_tag_pt = 'Sessão 9: Visão do Templo Corrompido'
title_tag_en = 'Session 9: Corrupted Temple Vision'
new_title = f'<span class="lang-pt">{title_tag_pt}</span><span class="lang-en">{title_tag_en}</span>'
# Find the title tag
title_start = template.find('<title>')
if title_start == -1:
    raise Exception("Title tag not found")
title_end = template.find('</title>', title_start)
if title_end == -1:
    raise Exception("Closing title tag not found")
# Replace the content between the title tags
template = template[:title_start+7] + new_title + template[title_end:]

# Update the localStorage key in the template (assuming it's currently set to ezekiel-s2-lang)
template = template.replace('ezekiel-s2-lang', 'ezekiel-s9-lang')

# Build the inner content for the main div
opening_tag = '<div class="max-w-4xl mx-auto px-5 py-12 md:py-16">'
start = template.find(opening_tag)
if start == -1:
    raise Exception("Opening tag of main div not found")
# Find the matching closing tag
pos = start + len(opening_tag)
counter = 1
while counter > 0 and pos < len(template):
    next_open = template.find('<div', pos)
    next_close = template.find('</div>', pos)
    if next_close == -1:
        break
    if next_open != -1 and next_open < next_close:
        counter += 1
        pos = next_open + 4
    else:
        counter -= 1
        pos = next_close + 6
end = pos

# Build new inner content
new_h1 = f'<h1 class="title reveal"><span class="lang-pt">{title_pt}</span><span class="lang-en">{title_en}</span></h1>'
new_hr = '<hr class="rule">'

generated_content = []
for page_num, text in enumerate(pages_text):
    # Escape HTML and replace newlines with <br>
    escaped = html.escape(text)
    escaped = escaped.replace('\n', '<br>')
    # Use same text for both languages (as in build_session.py)
    content_parts = [f'<span class="lang-pt">{escaped}</span>', f'<span class="lang-en">{escaped}</span>']
    lang_wrapped = ''.join(content_parts)
    generated_content.append(f'<div class="page reveal">{lang_wrapped}</div>')
    
    # If this page has an image, add the image div
    if any(ip[0] == page_num for ip in images_info):
        img_path = [ip[1] for ip in images_info if ip[0] == page_num][0]
        # Relative path from HTML to image: from modulo-2/sessao-9.html to img/sessao-9/p{page_num+1}-vector.png
        img_src = f'img/sessao-9/p{page_num+1}-vector.png'
        caption_pt = f'Diagrama da página {page_num+1}. Ilustração criada por Tim Mackie para BibleProject Classroom: Ezequiel (2021).'
        caption_en = f'Diagram from page {page_num+1}. Illustration by Tim Mackie for BibleProject Classroom: Ezekiel (2021).'
        generated_content.append(f'''\n        <div class="table-img reveal">\n          <img src="{img_src}" alt="Diagrama da página {page_num+1}">\n          <p class="caption">\n            <span class="lang-pt">{caption_pt}</span>\n            <span class="lang-en">{caption_en}</span>\n          </p>\n        </div>\n        ''')

# Join the generated content
generated_content_str = '\n'.join(generated_content)
new_inner_content = f'{new_h1}\n{new_hr}\n{generated_content_str}'

# Replace the inner content of the main div
new_template = template[:start+len(opening_tag)] + new_inner_content + template[end:]

# Write the output
with open(output_path, 'w') as f:
    f.write(new_template)

print(f'Session {N} written to {output_path}')
