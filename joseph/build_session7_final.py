import fitz
import os
import re
import json
import html

base = os.getcwd()
N = 7
pdf_path = f"{base}/pdf-sessoes/sessao-{N+1}.pdf"  # sessao-8.pdf

# Read the Joseph course index.html to determine modulo (MODULES array for Joseph course)
index_path = f"{base}/index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

# Find the MODULES array in the Joseph course index
# Look for: const MODULES = [...];
pattern = r'const MODULES = (\\\\[.*?\\\\]);'
match = re.search(pattern, index_content, re.DOTALL)
if match:
    modules_json = match.group(1)
    # Replace single quotes with double quotes for JSON parsing
    modules_json = modules_json.replace("'", '"')
    try:
        MODULES = json.loads(modules_json)
    except json.JSONDecodeError:
        print("Failed to parse JSON, using fallback")
        # Fallback: hardcoded modules from the Joseph course
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
    print("Could not find MODULES array, using fallback")
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

# Render images if not already done (pages with >=8 drawings)
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

# Get title: we want the line that contains "Session 7: Down Into the Pit"
# From the text we saw, it's the third line (index 2) of the first page.
# Let's extract lines from the first page and find the one that starts with "Session"
first_page_lines = pages_text[0].split('\n')
title_line = ""
for line in first_page_lines:
    if line.strip().startswith("Session"):
        title_line = line.strip()
        break
if not title_line:
    # fallback: take the first non-empty line
    for line in first_page_lines:
        if line.strip():
            title_line = line.strip()
            break
if not title_line:
    title_line = f"Session {N}: Unknown Title"

# The title_line is like "Session 7: Down Into the Pit"
# We need PT and EN versions.
# We'll assume the English title is the title_line, and we need to translate the part after "Session 7: " to Portuguese.
# We'll use a simple translation for the phrase we know: "Down Into the Pit" -> "Descendo para o Poço"
if title_line.startswith("Session"):
    # Remove "Session {N}: " prefix
    prefix = f"Session {N}: "
    if title_line.startswith(prefix):
        title_part = title_line[len(prefix):]
    else:
        # maybe the format is slightly different
        # split by colon
        parts = title_line.split(':', 1)
        if len(parts) == 2:
            title_part = parts[1].strip()
        else:
            title_part = title_line
else:
    title_part = title_line

# Translate title_part to Portuguese using a small dictionary
translation_map = {
    "Down Into the Pit": "Descendo para o Poço",
    # Add more as needed
}
title_part_pt = translation_map.get(title_part, title_part)  # fallback to same (not ideal but okay for now)
title_pt = f"Sessão {N}: {title_part_pt}"
title_en = f"Session {N}: {title_part}"

print(f"PT title: {title_pt}")
print(f"EN title: {title_en}")

# Load template
template_path = f"{base}/modulo-1/sessao-2.html"
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

# Replace title in the HTML title tag
# We'll find the <title> and </title> tags and replace the content.
title_open = '<title>'
title_close = '</title>'
title_start = template.find(title_open)
if title_start == -1:
    print("Could not find title tag")
    exit(1)
title_end = template.find(title_close, title_start)
if title_end == -1:
    print("Could not find closing title tag")
    exit(1)
template = template[:title_start+len(title_open)] + title_pt + template[title_end:]

# Replace the h1.title content
# We'll find the <h1 class="title reveal"> and </h1> tags and replace the content.
h1_open = '<h1 class="title reveal">'
h1_close = '</h1>'
h1_start = template.find(h1_open)
if h1_start == -1:
    # try with single quotes
    h1_open = '<h1 class=\'title reveal\'>'
    h1_start = template.find(h1_open)
if h1_start == -1:
    print("Could not find h1 tag")
    exit(1)
h1_end = template.find(h1_close, h1_start)
if h1_end == -1:
    print("Could not find closing h1 tag")
    exit(1)
# The content to replace is between h1_start+len(h1_open) and h1_end
new_h1_content = f'<span class="lang-pt">{title_pt}</span><span class="lang-en">{title_en}</span>'
template = template[:h1_start+len(h1_open)] + new_h1_content + template[h1_end:]

# Update localStorage key
template = template.replace("localStorage.setItem('joseph-s2-lang',l)", "localStorage.setItem('joseph-s7-lang',l)")
template = template.replace("localStorage.getItem('joseph-s2-lang')", "localStorage.getItem('joseph-s7-lang')")

# Now we want to split the template at the hr tag and then at the closing div after the hr.
# Find the hr tag
hr_tag = '<hr class="rule">'
hr_index = template.find(hr_tag)
if hr_index == -1:
    print("Could not find hr tag")
    exit(1)

# Find the closing div after the hr
div_close_tag = '</div>'
div_close_index = template.find(div_close_tag, hr_index)
if div_close_index == -1:
    print("Could not find closing div after hr")
    exit(1)

# Now we have:
#   part1: from start to and including the hr
#   part2: from after the hr to the closing div (exclusive) -> this is the content to replace
#   part3: from the closing div to the end
part1 = template[:hr_index + len(hr_tag)]
part2 = template[hr_index + len(hr_tag):div_close_index]  # we will ignore this
part3 = template[div_close_index:]  # includes the closing div and everything after

# Now we build our content.
our_content = ""

# First, we add the extracted text as paragraphs.
full_text = '\n'.join(pages_text)
lines = full_text.split('\n')
for line in lines:
    line = line.strip()
    if not line:
        continue
    # Escape HTML special characters
    escaped_line = html.escape(line)
    our_content += f'<p class=\"body reveal\"><span class=\"lang-pt\">{escaped_line}</span><span class=\"lang-en\">{escaped_line}</span></p>\n'

# Then we add the images (pages with >=8 drawings)
doc = fitz.open(pdf_path)
for i, page in enumerate(doc):
    if len(page.get_drawings()) >= 8:
        img_path = f"img/sessao-{N}/p{i+1}-vector.png"
        our_content += f'<div class=\"table-img reveal\"><img src=\"{img_path}\" alt=\"Diagram page {i+1}\"><p class=\"caption\"><span class=\"lang-pt\">Diagram from page {i+1}</span><span class=\"lang-en\">Diagram from page {i+1}</span></p></div>\n'
doc.close()

# Now combine: part1 + our_content + part3
new_template = part1 + our_content + part3

# Write the output
output_path = f"{output_dir}/sessao-{N}.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(new_template)
print(f"Generated {output_path}")