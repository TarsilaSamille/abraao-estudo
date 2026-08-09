import fitz
import os
import re

N = 8
pdf_path = f'pdf-sessoes/sessao-{N+1}.pdf'
output_dir = f'modulo-1/img/sessao-{N}'
os.makedirs(output_dir, exist_ok=True)

doc = fitz.open(pdf_path)
pages_text = []
images_info = []  # list of (page_num, image_path) for pages with >=8 drawings

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
        img_path = os.path.join(output_dir, img_filename)
        if not os.path.exists(img_path):
            pix.save(img_path)
            print(f'Rendered {img_path}')
        images_info.append((page_num, img_path))

doc.close()

# Extract title from first page (first non-empty line, cleaned)
first_page_text = pages_text[0] if pages_text else ''
lines = [line.strip() for line in first_page_text.split('\n') if line.strip()]
subtitle = lines[0] if lines else 'Título não encontrado'
# Clean up subtitle: remove extra spaces, limit length
subtitle = re.sub(r'\s+', ' ', subtitle).strip()
if len(subtitle) > 100:
    subtitle = subtitle[:97] + '...'

title_pt = f'Sessão {N}: {subtitle}'
title_en = f'Session {N}: {subtitle}'

# Generate the HTML content for the main div
content_parts = []
for page_num, text in enumerate(pages_text):
    # Convert newlines to <br> for HTML
    text_html = text.replace('\n', '<br>')
    # Use the same text for both languages
    content_parts.append(f'<div class="page reveal"><span class="lang-pt">{text_html}</span><span class="lang-en">{text_html}</span></div>')

    # If this page has an image, add the image div
    if any(ip[0] == page_num for ip in images_info):
        img_path = [ip[1] for ip in images_info if ip[0] == page_num][0]
        # The image path relative to the HTML file: from modulo-1/sessao-8.html, we go to img/sessao-8/
        img_src = f'img/sessao-{N}/p{page_num+1}-vector.png'
        caption_pt = f'Diagrama da página {page_num+1}. Ilustração criada por Tim Mackie para BibleProject Classroom: Ezequiel (2021).'
        caption_en = f'Diagram from page {page_num+1}. Illustration by Tim Mackie for BibleProject Classroom: Ezekiel (2021).'
        content_parts.append(f'''\n        <div class="table-img reveal">\n          <img src="{img_src}" alt="Diagrama da página {page_num+1}">\n          <p class="caption">\n            <span class="lang-pt">{caption_pt}</span>\n            <span class="lang-en">{caption_en}</span>\n          </p>\n        </div>\n        ''')

generated_content = '\n'.join(content_parts)

# Now read the template
template_path = 'modulo-1/sessao-2.html'
with open(template_path, 'r') as f:
    template = f.read()

# Update the title in the template
new_title = f'<span class="lang-pt">{title_pt}</span><span class="lang-en">{title_en}</span>'

# Find the title tag
title_start = template.find('<title>')
if title_start == -1:
    raise Exception("Title tag not found")
title_end = template.find('</title>', title_start)
if title_end == -1:
    raise Exception("Closing title tag not found")
# Replace the content between the title tags
template = template[:title_start+7] + new_title + template[title_end:]

# Update the localStorage key in the script
template = template.replace('ezekiel-s2-lang', f'ezekiel-s{N}-lang')

# Now we need to replace the content of the main div with our generated_content
# We'll find the main div and replace its innerHTML
opening_tag = '<div class="max-w-4xl mx-auto px-5 py-12 md:py-16">'
start = template.find(opening_tag)
if start == -1:
    raise Exception("Opening tag of main div not found")
# Now find the matching closing tag
pos = start + len(opening_tag)
counter = 1
while counter > 0 and pos < len(template):
    next_open = template.find('<div', pos)
    next_close = template.find('</div>', pos)
    if next_close == -1:
        # No more closing tags, break
        break
    if next_open != -1 and next_open < next_close:
        # Found an opening tag first
        counter += 1
        pos = next_open + 4  # move past '<div'
    else:
        # Found a closing tag first
        counter -= 1
        pos = next_close + 6  # move past '</div>'
end = pos  # this is the position after the matching closing tag

# Now we have the entire main div from start to end
main_div_string = template[start:end]
# We want to replace the innerHTML of this div
# The innerHTML is between the opening tag and the closing tag
inner_html_start = len(opening_tag)
inner_html_end = len(main_div_string) - len('</div>')
# Replace the innerHTML
new_main_div = opening_tag + generated_content + '</div>'
# Now replace the entire main div string with the new one
new_template = template[:start] + new_main_div + template[end:]

# Write the new template to the output file
output_path = f'modulo-1/sessao-{N}.html'
with open(output_path, 'w') as f:
    f.write(new_template)

print(f'Session {N} written to {output_path}')