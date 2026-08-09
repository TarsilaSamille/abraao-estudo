import fitz
import os
import re
import json
import html

base = os.getcwd()
N = 7
pdf_path = f"{base}/pdf-sessoes/sessao-{N+1}.pdf"  # sessao-8.pdf

# Read joseph/index.html to determine modulo (MODULES array for Joseph course)
index_path = f"{base}/index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

# For now, we'll use the fallback modules since the MODULES array in index.html is for the main page, not the Joseph course.
# We need to look at joseph/index.html for the MODULES array.
joseph_index_path = f"{base}/joseph/index.html"
with open(joseph_index_path, 'r', encoding='utf-8') as f:
    joseph_index_content = f.read()

# Find the MODULES array in the Joseph course index
# Look for: const MODULES = [...];
pattern = r'const MODULES = (\\\\[.*?\\\\]);'
match = re.search(pattern, joseph_index_content, re.DOTALL)
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

# Now split the template by the hr tag.
# We want to keep everything up to and including the hr, then insert our content, then the rest (which starts with the closing div and script).
# We split at the first occurrence of '<hr class="rule">'
parts = template.split('<hr class="rule">', 1)
if len(parts) != 2:
    print("Could not find hr tag")
    exit(1)
part1 = parts[0] + '<hr class="rule">'  # everything before and including the hr
part2 = parts[1]  # everything after the hr

print("Length of part2:", len(part2))
print("First 200 chars of part2:", repr(part2[:200]))

# Now we need to split part2 into the content to replace and the closing div and script.
# We look for the first occurrence of '</div>' followed by optional whitespace and then '<script>'
# We'll use a regex on part2.
match = re.search(r'(.*?)(</div>\\s*<script>.*)', part2, re.DOTALL)
if not match:
    print("Could not split part2 at closing div and script")
    # Let's try to find the closing div and script separately
    # Find the first '</div>'
    div_close_pos = part2.find('</div>')
    if div_close_pos == -1:
        print("No closing div found in part2")
    else:
        print(f"Found closing div at {div_close_pos}")
        # Look for '<script>' after the div
        script_pos = part2.find('<script>', div_close_pos)
        if script_pos == -1:
            print("No script tag found after the closing div")
        else:
            print(f"Found script tag at {script_pos}")
            # If we have both, we can split
            content_to_replace = part2[:div_close_pos]
            closing_and_script = part2[div_close_pos:]
            print("Using manual split")
    exit(1)
content_to_replace = match.group(1)  # we will ignore this and put our own
closing_and_script = match.group(2)  # the closing div, script, and rest

print("Length of content_to_replace:", len(content_to_replace))
print("First 100 chars of content_to_replace:", repr(content_to_replace[:100]))
print("Length of closing_and_script:", len(closing_and_script))
print("First 100 chars of closing_and_script:", repr(closing_and_script[:100]))

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

# Now combine: part1 + our_content + closing_and_script
new_template = part1 + our_content + closing_and_script

# Write the output
output_path = f"{output_dir}/sessao-{N}.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(new_template)
print(f"Generated {output_path}")