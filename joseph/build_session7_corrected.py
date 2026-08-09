import fitz
import os
import re

base = os.getcwd()
N = 7
pdf_path = f"{base}/pdf-sessoes/sessao-{N+1}.pdf"  # sessao-8.pdf

# Read joseph/index.html to determine modulo (MODULES array for Joseph course)
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
template = re.sub(r'<title>.*?</title>', f'<title>{title_pt}</title>', template, flags=re.DOTALL)

# Replace the h1.title content
pattern = r'(<h1 class=\"title reveal\\\">)(.*?)(</h1>)'
replacement = r'\\1<span class=\"lang-pt\">' + title_pt + r'</span><span class=\"lang-en\">' + title_en + r'</span>\\3'
template = re.sub(pattern, replacement, template, flags=re.DOTALL)

# Update localStorage key
template = template.replace("localStorage.setItem('joseph-s2-lang',l)", "localStorage.setItem('joseph-s7-lang',l)")
template = template.replace("localStorage.getItem('joseph-s2-lang')", "localStorage.getItem('joseph-s7-lang')")

# Now we need to replace the content of the div after the hr.
# We'll split the template into three parts: 
#   part1: everything up to and including the hr
#   part2: the content to replace (between hr and closing div)
#   part3: the closing div and everything after (including the script)
pattern = r'(.*?<hr class=\\\"rule\\\">)(.*?)(</div>\\s*<script>.*)'
match = re.search(pattern, template, re.DOTALL)
if match:
    part1 = match.group(1)   # up to and including the hr
    part2 = match.group(2)   # the content to replace (we will ignore this and put our own)
    part3 = match.group(3)   # the closing div, script, and rest
    # Now we need to generate our content (the inner content of the div after the hr)
    # We'll convert the extracted text into HTML blocks.
    # We'll split the text by double newlines to get paragraphs.
    full_text = '\n'.join(pages_text)
    # We'll wrap each non-empty line in a <p> tag? But we want to preserve the structure.
    # For simplicity, we'll split by '\n\n' and wrap each block in a <p> class=\"body reveal\" with lang spans.
    # However, the existing sessions have a more complex structure (h3, ul, etc.). 
    # Since we don't have a specific structure to follow, we'll just output the text as paragraphs.
    # We'll also include the images we rendered.

    # Let's build the inner content:
    inner_content = ""

    # Process the text line by line and build HTML.
    lines = full_text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        # We'll wrap the line in a <p> with class \"body reveal\" and lang spans.
        # We'll duplicate the line for PT and EN? But we don't have a translation.
        # We'll just put the same line in both lang spans? Or we can put the English in the lang-en and a placeholder in lang-pt?
        # Since we don't have a translation, we'll put the same text in both.
        # However, the existing sessions have the text duplicated in lang-pt and lang-en spans.
        # We'll do the same.

        escaped_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\"', '&quot;').replace(\"'\", '&#x27;')
        inner_content += f'<p class=\"body reveal\"><span class=\"lang-pt\">{escaped_line}</span><span class=\"lang-en\">{escaped_line}</span></p>\n'
        i += 1

    # Now, we also need to include the images we rendered.
    # For each image, we can add an <img> tag.
    # We'll add them after the text? Or we can intersperse? We'll just add them at the end for simplicity.
    # We need to re-open the pdf to get the page count? We already have the doc closed, but we can recompute.
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        if len(page.get_drawings()) >= 8:
            img_path = f"img/sessao-{N}/p{i+1}-vector.png"
            inner_content += f'<div class=\"table-img reveal\"><img src=\"{img_path}\" alt=\"Diagram page {i+1}\"><p class=\"caption\"><span class=\"lang-pt\">Diagram from page {i+1}</span><span class=\"lang-en\">Diagram from page {i+1}</span></p></div>\n'
    doc.close()

    # Now, combine the parts:
    new_template = part1 + inner_content + part3

    # Write the output
    output_path = f"{output_dir}/sessao-{N}.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_template)
    print(f"Generated {output_path}")
else:
    print("Could not split template at hr tag")
    exit(1)