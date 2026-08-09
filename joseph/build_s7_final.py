import fitz
import os
import re
import json

base = os.getcwd()
N = 7
pdf_path = f"{base}/pdf-sessoes/sessao-{N+1}.pdf"  # sessao-8.pdf

# Read index.html to determine modulo
index_path = f"{base}/index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

# Find the MODULES array
pattern = r'const MODULES = (\\[.*?\\]);'
match = re.search(pattern, index_content, re.DOTALL)
if match:
    modules_json = match.group(1)
    modules_json = modules_json.replace("'", '"')
    try:
        MODULES = json.loads(modules_json)
    except json.JSONDecodeError:
        print("Failed to parse JSON, using fallback")
        MODULES = [
            {"pos": 1, "first": 1, "last": 4, "title_en": "Introduction to the Joseph Story", "title_pt": "Introdução à História de José"},
            {"pos": 2, "first": 5, "last": 9, "title_en": "Joseph’s Dreams and Hostile Brothers", "title_pt": "Os Sonhos de José e os Irmãos Hostis"},
            {"pos": 3, "first": 10, "last": 12, "title_en": "Rise and Fall and Rise Again", "title_pt": "Ascensão, Queda e Nova Ascensão"},
            {"pos": 4, "first": 13, "last": 17, "title_en": "Joseph Tests His Brothers", "title_pt": "José Testa Seus Irmãos"},
            {"pos": 5, "first": 18, "last": 20, "title_en": "Joseph Rescues Egypt and His Family", "title_pt": "José Resgata o Egito e Sua Família"},
            {"pos": 6, "first": 21, "last": 25, "title_en": "Jacob’s Song of Blessing", "title_pt": "O Cântico de Bênção de Jacó"},
            {"pos": 7, "first": 26, "last": 29, "title_en": "Going Up to Canaan", "title_pt": "Subindo para Canaã"}
        ]
else:
    MODULES = [
        {"pos": 1, "first": 1, "last": 4, "title_en": "Introduction to the Joseph Story", "title_pt": "Introdução à História de José"},
        {"pos": 2, "first": 5, "last": 9, "title_en": "Joseph’s Dreams and Hostile Brothers", "title_pt": "Os Sonhos de José e os Irmãos Hostis"},
        {"pos": 3, "first": 10, "last": 12, "title_en": "Rise and Fall and Rise Again", "title_pt": "Ascensão, Queda e Nova Ascensão"},
        {"pos": 4, "first": 13, "last": 17, "title_en": "Joseph Tests His Brothers", "title_pt": "José Testa Seus Irmãos"},
        {"pos": 5, "first": 18, "last": 20, "title_en": "Joseph Rescues Egypt and His Family", "title_pt": "José Resgata o Egito e Sua Família"},
        {"pos": 6, "first": 21, "last": 25, "title_en": "Jacob’s Song of Blessing", "title_pt": "O Cântico de Bênção de Jacó"},
        {"pos": 7, "first": 26, "last": 29, "title_en": "Going Up to Canaan", "title_pt": "Subindo para Canaã"}
    ]

# Find the module that contains session N
target_module = None
for m in MODULES:
    if m["first"] <= N <= m["last"]:
        target_module = m
        break

if target_module is None:
    print(f"Error: Session {N} not found in any module")
    exit(1)

output_dir = f"{base}/modulo-{target_module['pos']}"
img_dir = f"{output_dir}/img/sessao-{N}"
os.makedirs(img_dir, exist_ok=True)

# Render images if not already done
doc = fitz.open(pdf_path)
for i, page in enumerate(doc):
    if len(page.get_drawings()) >= 8:
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        img_path = f"{img_dir}/p{i+1}-vector.png"
        if not os.path.exists(img_path):
            pix.save(img_path)
            print(f"Rendered {img_path}")
doc.close()

# Extract text
doc = fitz.open(pdf_path)
pages_text = [page.get_text() for page in doc]
doc.close()

# Get title: find the line that starts with "Session"
first_page_lines = pages_text[0].split('\\n')
title_line = ""
for line in first_page_lines:
    if line.strip().startswith("Session"):
        title_line = line.strip()
        break
if not title_line:
    for line in first_page_lines:
        if line.strip():
            title_line = line.strip()
            break
if not title_line:
    title_line = "Session 7: Unknown Title"

# Extract the part after "Session 7: "
if title_line.startswith("Session"):
    # Remove "Session {N}: " prefix
    prefix = f"Session {N}: "
    if title_line.startswith(prefix):
        title_part = title_line[len(prefix):]
    else:
        parts = title_line.split(':', 1)
        if len(parts) == 2:
            title_part = parts[1].strip()
        else:
            title_part = title_line
else:
    title_part = title_line

# Translate title_part to Portuguese (we know this one)
translation_map = {
    "Down Into the Pit": "Descendo para o Poço",
}
title_part_pt = translation_map.get(title_part, title_part)  # fallback
title_pt = f"Sessão {N}: {title_part_pt}"
title_en = f"Session {N}: {title_part}"

print(f"PT title: {title_pt}")
print(f"EN title: {title_en}")

# Load template
template_path = f"{base}/modulo-1/sessao-2.html"
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

# Replace title in the HTML title tag
template = re.sub(r'<title>.*?</title>', f'<title>{title_pt}</title>', template, flags=re.DOTALL)

# Replace the h1.title content
pattern = r'(<h1 class="title reveal\">)(.*?)(</h1>)'
replacement = r'\\1<span class="lang-pt">' + title_pt + r'</span><span class="lang-en">' + title_en + r'</span>\\3'
template = re.sub(pattern, replacement, template, flags=re.DOTALL)

# Update localStorage key
template = template.replace("localStorage.setItem('joseph-s2-lang',l)", "localStorage.setItem('joseph-s7-lang',l)")
template = template.replace("localStorage.getItem('joseph-s2-lang')", "localStorage.getItem('joseph-s7-lang')")

# Now process the div content
# Find the opening div
div_open_pattern = r'(<div class="max-w-4xl mx-auto px-5 py-12 md:py-16\">)'
match = re.search(div_open_pattern, template)
if not match:
    print("Could not find opening div")
    exit(1)
div_open = match.group(1)
pos_after_open = match.end()

# Find the closing div that is followed by a script tag
# We'll search from pos_after_open for the pattern: </div>\s*<script>
# We want to find the first such occurrence after the opening div.
remaining = template[pos_after_open:]
close_pattern = r'(</div>\s*<script>)'
match_close = re.search(close_pattern, remaining)
if not match_close:
    print("Could not find closing div followed by script")
    exit(1)
div_close_script = match_close.group(1)
pos_close_start = pos_after_open + match_close.start()
pos_after_close = pos_after_open + match_close.end()

# Now we have:
# template[:pos_after_open] = everything up to and including the opening div
# template[pos_after_open:pos_close_start] = the inner content of the div
# template[pos_close_start:pos_after_close] = the closing div and the opening script tag
# template[pos_after_close:] = the rest (the script content and after)

inner_content = template[pos_after_open:pos_close_start]

# We want to keep the h1 and the hr, and replace everything after the hr.
# Split inner_content at the first occurrence of '<hr class="rule">'
hr_pattern = r'(<hr class=\"rule\">)'
match_hr = re.search(hr_pattern, inner_content)
if not match_hr:
    print("Could not find hr tag in inner content")
    exit(1)
hr_tag = match_hr.group(1)
pos_hr_end = match_hr.end()

# Keep everything up to and including the hr
content_before_hr = inner_content[:pos_hr_end]  # includes the hr

# Generate the page content
page_content = ""
for i, text in enumerate(pages_text):
    # Escape HTML in text
    text_escaped = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # Replace newlines with <br> for simplicity
    text_escaped = text_escaped.replace('\\n', '<br>')
    page_content += f'<div class="page reveal">{text_escaped}</div>'
    # Check if there is an image for this page
    img_path = f"img/sessao-{N}/p{i+1}-vector.png"
    if os.path.exists(f"{output_dir}/{img_path}"):
        page_content += f'<div class="table-img reveal"><img src="{img_path}" alt="Page {i+1} diagram"><p class="caption"><span class="lang-pt">Gênesis X:Y. Tradução e Design Literário por Tim Mackie para BibleProject Classroom: José (2021).</span><span class="lang-en">Genesis X:Y. Translation and Literary Design by Tim Mackie for BibleProject Classroom: Joseph (2021).</span></p></div>'

# New inner content: content_before_hr + page_content
new_inner = content_before_hr + page_content

# Reconstruct the template
new_template = template[:pos_after_open] + new_inner + template[pos_close_start:]

# Write the new template to the output file
output_path = f"{output_dir}/sessao-{N}.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(new_template)
print(f"Created {output_path}")
