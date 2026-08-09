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
# Look for: const MODULES = [...];
pattern = r'const MODULES = (\\[.*?\\]);'
match = re.search(pattern, index_content, re.DOTALL)
if match:
    modules_json = match.group(1)
    # Replace single quotes with double quotes for JSON parsing
    modules_json = modules_json.replace("'", '"')
    try:
        MODULES = json.loads(modules_json)
    except json.JSONDecodeError:
        # Fallback: manually parse if needed
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

# Get title from first line of first page
first_page_text = pages_text[0].strip()
# Assume title is the first line, but we'll take until first newline or a reasonable length
title_lines = first_page_text.split('\\n')
title_extracted = ""
for line in title_lines:
    if line.strip():
        title_extracted = line.strip()
        break
if not title_extracted:
    title_extracted = "Título não encontrado"

# The extracted title is expected to be in English (from the PDF we saw)
title_en = f"Session {N}: {title_extracted}"
# Translate to Portuguese (simple translation for now)
# We'll translate "Down Into the Pit" to "Descendo para o Poço"
# But we need to extract just the title part after "Session 7: "
# Actually title_extracted is like "Session 7: Down Into the Pit"
# We want the part after the colon.
if ': ' in title_extracted:
    title_part = title_extracted.split(': ', 1)[1]
else:
    title_part = title_extracted
# Translate title_part to Portuguese using a simple dictionary or heuristic
# For now, we'll use a mapping for known phrases or just a placeholder.
# We'll do a simple translation: "Down Into the Pit" -> "Descendo para o Poço"
# We'll also handle other common words? Not needed.
translation_map = {
    "Down Into the Pit": "Descendo para o Poço",
    # Add more if needed
}
title_part_pt = translation_map.get(title_part, title_part)  # fallback to same
title_pt = f"Sessão {N}: {title_part_pt}"

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

# Now we need to replace the content of the div (from the opening div with class "max-w-4xl mx-auto px-5 py-12 md:py-16" to the closing div before the script)
# We'll use a similar approach as in build_s4.py.
# We'll split the template into three parts: before the div, the div (with its opening and closing), and after the div (which includes the script).
# Actually, we want to keep the div tags and replace the inner content.

# Let's find the div and its closing tag that is immediately followed by the script.
# We'll use a regex to capture:
#   (everything before the div) (the opening div) (the inner content) (the closing div and the script that follows) (everything after)
# But note: the closing div is followed by a script tag. We want to keep the closing div and the script.

# We'll do:
pattern = r'(.*?)(<div class="max-w-4xl mx-auto px-5 py-12 md:py-16\">)(.*?)(</div>\\s*<script>)(.*)'
match = re.search(pattern, template, re.DOTALL)
if match:
    before = match.group(1)
    div_open = match.group(2)
    inner_old = match.group(3)
    div_close_script = match.group(4)
    after = match.group(5)
    
    # We will generate the new inner content.
    # We want to keep the title and rule? Actually, in the template, the title and rule are inside this div.
    # We have already updated the title in the template (in the h1) which is inside this div.
    # So the inner_old already contains our updated title and the rule.
    # We will keep the title and rule and then add the page content after the rule.
    # We'll split the inner_old by the rule (hr) and keep everything before and including the rule, then replace the rest with our page content.
    
    # Split by the rule
    rule_split = inner_old.split('<hr class=\"rule\">', 1)
    if len(rule_split) == 2:
        before_rule = rule_split[0]  # includes the title and maybe some whitespace
        after_rule = rule_split[1]   # everything after the rule
        # We will keep before_rule and the rule, and then replace after_rule with our page content.
        new_inner = before_rule + '<hr class=\"rule\">'
    else:
        # If we can't find the rule, we just keep the entire inner_old and then append our page content? 
        # But we don't want to duplicate. Let's just use the inner_old and then append.
        new_inner = inner_old
    
    # Now we generate the page content.
    for i, text in enumerate(pages_text):
        # Escape HTML in text
        text_escaped = text.replace('&', '&amp;').replace('<', '&lt').replace('>', '&gt;')
        # Replace newlines with <br> for simplicity
        text_escaped = text_escaped.replace('\\n', '<br>')
        new_inner += f'<div class="page reveal">{text_escaped}</div>'
        # Check if there is an image for this page
        img_path = f"img/sessao-{N}/p{i+1}-vector.png"
        if os.path.exists(f"{output_dir}/{img_path}"):
            new_inner += f'<div class="table-img reveal"><img src="{img_path}" alt="Page {i+1} diagram"><p class="caption"><span class="lang-pt">Gênesis X:Y. Tradução e Design Literário por Tim Mackie para BibleProject Classroom: José (2021).</span><span class="lang-en">Genesis X:Y. Translation and Literary Design by Tim Mackie for BibleProject Classroom: Joseph (2021).</span></p></div>'
    
    # Now reconstruct the template
    new_template = before + div_open + new_inner + div_close_script + after
    
    # Write the new template to the output file
    output_path = f"{output_dir}/sessao-{N}.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_template)
    print(f"Created {output_path}")
else:
    print("Could not find the div pattern in the template")
