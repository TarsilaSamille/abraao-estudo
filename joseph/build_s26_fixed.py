import fitz
import os
import re
import json

base = os.getcwd()
N = 26
pdf_path = f"{base}/pdf-sessoes/sessao-{N+1}.pdf"  # sessao-27.pdf

# 1. Determine module from root index.html
index_path = f"{base}/index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

# Find the MODULES array
pattern = r'const MODULES = (\\[.*?\\]);'
match = re.search(pattern, index_content, re.DOTALL)
if match:
    modules_json = match.group(1)
    # Convert single quotes to double quotes for JSON
    modules_json = modules_json.replace("'", '"')
    try:
        MODULES = json.loads(modules_json)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        # Fallback
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

print(f"Target module: {target_module}")

# 2. Get titles from module's index.html (modulo-{pos}/index.html)
module_index_path = f"{base}/modulo-{target_module['pos']}/index.html"
with open(module_index_path, 'r', encoding='utf-8') as f:
    module_index_content = f.read()

# Find the SESSIONS array in the module's index.html
start_marker = 'const SESSIONS = '
start = module_index_content.find(start_marker)
if start == -1:
    SESSIONS = []
else:
    start += len(start_marker)
    # Find the ending semicolon
    end = module_index_content.find(';', start)
    if end == -1:
        SESSIONS = []
    else:
        sessions_json = module_index_content[start:end].strip()
        try:
            SESSIONS = json.loads(sessions_json)
        except json.JSONDecodeError as e:
            print(f"Failed to parse SESSIONS JSON: {e}")
            print(f"Sessions JSON string: {sessions_json}")
            SESSIONS = []

# Find the session with n=N
session_info = None
for s in SESSIONS:
    if s.get("n") == N:
        session_info = s
        break

if session_info is None:
    print(f"Error: Session {N} not found in module {target_module['pos']} SESSIONS")
    print(f"SESSIONS array: {SESSIONS}")
    exit(1)

title_pt = session_info["title_pt"]
title_en = session_info["title_en"]

print(f"PT title: {title_pt}")
print(f"EN title: {title_en}")

# 3. Extract text from PDF and render images (pages with >=8 drawings) as vector images at 2x scale
img_dir = f"{base}/modulo-{target_module['pos']}/img/sessao-{N}"
os.makedirs(img_dir, exist_ok=True)

doc = fitz.open(pdf_path)
pages_text = []
for i, page in enumerate(doc):
    pages_text.append(page.get_text())
    if len(page.get_drawings()) >= 8:
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        img_path = f"{img_dir}/p{i+1}-vector.png"
        if not os.path.exists(img_path):
            pix.save(img_path)
            print(f"Rendered {img_path}")
doc.close()

# 4. Get title from PDF (first page) for verification (optional)
first_page_text = pages_text[0]
first_page_lines = first_page_text.split('\n')
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
    title_line = f"Session {N}: Unknown Title"

# Extract the part after "Session {N}: "
if title_line.startswith("Session"):
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

print(f"Title from PDF: {title_part}")

# 5. Load template
template_path = f"{base}/modulo-1/sessao-2.html"
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

# 6. Replace title in the HTML title tag
template = re.sub(r'<title>.*?</title>', f'<title>Sessão {N}: {title_pt}</title>', template, flags=re.DOTALL)

# 7. Replace the h1.title content
pattern = r'(<h1 class=\"title reveal\">)(.*?)(</h1>)'
replacement = r'\\1<span class=\"lang-pt\">Sessão ' + str(N) + ': ' + title_pt + r'</span><span class=\"lang-en\">Session ' + str(N) + ': ' + title_en + r'</span>\\3'
template = re.sub(pattern, replacement, template, flags=re.DOTALL)

# 8. Update localStorage key
template = template.replace("localStorage.setItem('joseph-s2-lang',l)", "localStorage.setItem('joseph-s26-lang',l)")
template = template.replace("localStorage.getItem('joseph-s2-lang')", "localStorage.getItem('joseph-s26-lang')")

# 9. Now process the div content
div_open_pattern = r'(<div class=\"max-w-4xl mx-auto px-5 py-12 md:py-16\">)'
match = re.search(div_open_pattern, template)
if not match:
    print("Could not find opening div")
    exit(1)
div_open = match.group(1)
pos_after_open = match.end()

# Find the closing div that is followed by a script tag
remaining = template[pos_after_open:]
close_pattern = r'(</div>\\s*<script>)'
match_close = re.search(close_pattern, remaining)
if not match_close:
    print("Could not find closing div followed by script")
    exit(1)
div_close_script = match_close.group(1)
pos_close_start = pos_after_open + match_close.start()
pos_after_close = pos_after_open + match_close.end()

inner_content = template[pos_after_open:pos_close_start]

# We want to keep the h1 and the hr, and replace everything after the hr.
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
    text_escaped = text_escaped.replace('\n', '<br>')
    page_content += f'<div class="page reveal">{text_escaped}</div>'
    # Check if there is an image for this page
    img_path = f"img/sessao-{N}/p{i+1}-vector.png"
    if os.path.exists(f"{base}/modulo-{target_module['pos']}/{img_path}"):
        page_content += f'<div class="table-img reveal"><img src="{img_path}" alt="Page {i+1} diagram"><p class="caption"><span class="lang-pt">Gênesis X:Y. Tradução e Design Literário por Tim Mackie para BibleProject Classroom: José (2021).</span><span class="lang-en">Genesis X:Y. Translation and Literary Design by Tim Mackie for BibleProject Classroom: Joseph (2021).</span></p></div>'

# New inner content: content_before_hr + page_content
new_inner = content_before_hr + page_content

# Reconstruct the template
new_template = template[:pos_after_open] + new_inner + template[pos_close_start:]

# 10. Write the new template to the output file
output_path = f"{base}/modulo-{target_module['pos']}/sessao-{N}.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(new_template)
print(f"Created {output_path}")