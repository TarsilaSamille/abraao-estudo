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

# Get title: we want the line that contains "Session 7: Down Into the Pit"
# From the text we saw, it's the third line (index 2) of the first page.
# Let's extract lines from the first page and find the one that starts with "Session"
first_page_lines = pages_text[0].split('\\n')
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
    title_line = "Session 7: Unknown Title"

# The title_line is like "Session 7: Down Into the Pit"
# We need PT and EN versions.
# For PT, we want "Sessão 7: Down Into the Pit" translated? Actually looking at existing sessions, the PT title is a translation of the English title.
# For example, sessao-2.html: PT: "Sessão 2: A Melodia Temática da Bíblia Hebraica", EN: "Session 2: The Thematic Melody of the Hebrew Bible"
# So we need to translate the English title to Portuguese.
# We don't have an automatic translator, but we can guess that the PDF is in English (since we saw "Class Notes: Joseph").
# So the title_line is English. We'll set EN title to that, and we need to provide a PT translation.
# We'll do a simple translation for the phrase we know: "Down Into the Pit" -> "Descendo para o Poço"
# We'll also keep the "Session 7:" -> "Sessão 7:"
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
# We'll add known translations from previous sessions? Not available.
# We'll use a heuristic: if we don't know, we'll keep the English and note that it should be updated.
# For now, we'll use a mapping for the phrase we saw.
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
pattern = r'(<h1 class="title reveal\">)(.*?)(</h1>)'
replacement = r'\\1<span class="lang-pt">' + title_pt + r'</span><span class="lang-en">' + title_en + r'</span>\\3'
template = re.sub(pattern, replacement, template, flags=re.DOTALL)

# Update localStorage key
template = template.replace("localStorage.setItem('joseph-s2-lang',l)", "localStorage.setItem('joseph-s7-lang',l)")
template = template.replace("localStorage.getItem('joseph-s2-lang')", "localStorage.getItem('joseph-s7-lang')")

# Now we need to replace the content of the div (from the opening div with class "max-w-4xl mx-auto px-5 py-12 md:py-16" to the closing div before the script)
# Let's examine the template to see the exact structure.
# We'll write a more robust pattern: we want to replace everything between the opening div and the closing div that is just before the script tag.
# We'll assume the structure is exactly as in sessao-2.html.

# Let's split the template into three parts: before the div, the div block, and after the div block (which includes the script).
# We'll use regex to capture the div block and replace its inner content.

# We'll find the opening div and the closing div that is followed by a script tag.
# We'll use a regex that captures:
#   (.*?) before the div
#   (<div class="max-w-4xl mx-auto px-5 py-12 md:py-16">) the opening div
#   (.*?) the inner content (non-greedy)
#   (</div>\\s*<script>) the closing div and the script opening tag
#   (.*) the rest
# This is what we did before, but it failed. Let's check why.

# Let's print the template to see what we are matching against? But we can't in this environment.
# Instead, let's write a simpler approach: we know the inner content we want to replace starts after the <hr class="rule"> and ends before the script.
# We'll keep everything from the start of the template up to and including the <hr class="rule">, then insert our page content, then add the closing div and script.

# Let's find the position of the <hr class="rule">.
hr_pattern = r'(<hr class=\"rule\">)'
match = re.search(hr_pattern, template)
if match:
    # We have the hr tag. We want to keep everything up to and including this hr tag.
    # But note: the hr tag is inside the div, after the h1.
    # Actually, we want to keep the h1 and the hr, and replace everything after the hr.
    # Let's split the template into two parts: before the hr (including the hr) and after the hr.
    # We'll keep the before part, then insert our page content, then we need to add the closing div and script? 
    # Wait, the after part already includes the closing div and script? Let's see.
    # In the template, after the hr, there is the content (like <h3 class=\"takeaways-h reveal\"> ...), and eventually the closing div and then the script.
    # So if we keep everything up to and including the hr, and then append our page content, and then append the rest of the template after the hr? 
    # That would duplicate the hr? Actually we want to replace the content after the hr with our page content, but we want to keep the closing div and script that are after the original content.
    # So we need to know where the original content ends and the closing div begins.
    # This is getting messy.

    # Let's instead use the same approach as before but debug by printing the groups.
    # We'll write a small test to see if our pattern matches.
    # We'll do it in the script but we can't see output easily. Let's instead write a temporary file and examine? 
    # Given time, let's try a different tactic: we can replace the entire inner content of the div by setting the innerHTML via JavaScript? 
    # But we are generating a static HTML file.

    # Let's look at the template again by reading it in the terminal? We can do that now.
    pass
else:
    print("Could not find hr tag")
    exit(1)

# Actually, let's step back and look at the template by reading a few lines.
# We'll do that in the terminal now.
