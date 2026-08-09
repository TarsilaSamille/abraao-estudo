import fitz
import os
import re

base = os.getcwd()
pdf_path = f"{base}/pdf-sessoes/sessao-6.pdf"  # N+1 = 6
output_dir = f"{base}/modulo-2"
img_dir = f"{output_dir}/img/sessao-5"
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
title_lines = first_page_text.split('\n')
title_pt = title_lines[0].strip() if title_lines else "Sessão 5: Título em Português"
# We'll also try to get an English title? Not in PDF, we'll use a placeholder.
# For now, we'll use the same for both, but note the task says: update title to "Sessão 5: [title from PDF]" and "Session 5: [English title]"
# We don't have English title in PDF, so we'll set English title as a translation placeholder.
# However, looking at sessao-2.html, they have both PT and EN in the h1.
# We'll set the PT title from PDF and EN title as a placeholder (maybe we can translate later?).
# For now, we'll use the PT title and set EN title as the same but in English? Not possible.
# Let's assume the PDF title is in Portuguese and we need to provide an English version.
# Since we don't have translation, we'll use the same string for both, but note the task expects two different.
# We'll check the pattern in existing sessions: they have both PT and EN in the h1.
# We'll set:
#   title_pt = "Sessão 5: [extracted title]"
#   title_en = "Session 5: [extracted title in English?]"
# We don't have the English title, so we'll leave it as the same for now and note that it should be updated manually.
# Alternatively, we can look at the pattern in the index.html for modules to guess the English title for session 5.
# But the task says: update title to "Sessão 5: [title from PDF]" and "Session 5: [English title]"
# We'll extract the title from PDF and then use that for PT, and for EN we'll use a placeholder.
# Let's extract the title and then we'll format:
#   PT: "Sessão 5: " + extracted_title
#   EN: "Session 5: " + extracted_title (but this is not English, just same words)
# We'll do that and then maybe the user can adjust.

# However, looking at the build_s4.py, they hardcoded the title.
# Let's instead follow the pattern in the existing session files (like sessao-2.html) which have:
#   <h1 class="title reveal"><span class="lang-pt">Sessão 2: A Melodia Temática da Bíblia Hebraica</span><span class="lang-en">Session 2: The Thematic Melody of the Hebrew Bible</span></h1>
# We don't have the English title for session 5, so we'll set the English span to the same as PT for now, but note that it should be changed.

# We'll extract the title from the PDF and then use it for both, but we'll note in the output that the English title needs to be updated.

# Let's extract the title from the first page, first non-empty line.
title_extracted = ""
for line in title_lines:
    if line.strip():
        title_extracted = line.strip()
        break

if not title_extracted:
    title_extracted = "Título não encontrado"

title_pt = f"Sessão 5: {title_extracted}"
title_en = f"Session 5: {title_extracted}"  # Placeholder

# Load template
template_path = f"{base}/modulo-1/sessao-2.html"
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

# Replace title in the HTML title tag
template = re.sub(r'<title>.*?</title>', f'<title>{title_pt}</title>', template)

# Replace the h1.title content
# We want to replace the inner content of the h1.title with our PT and EN spans.
# We'll use a regex to find the h1.title and replace its inner HTML.
# We'll keep the class and everything else.
# We'll replace from '<h1 class="title reveal">' to the closing '</h1>'
# We'll capture the entire h1 tag and replace its content.
# We'll use a regex that matches the entire h1 tag and replace the inner content.
# We'll do: re.sub(r'(<h1 class="title reveal">).*?(</h1>)', r'\1<span class="lang-pt">...PT...</span><span class="lang-en">...EN...</span>\2', template, flags=re.DOTALL)
# But note: the existing h1 has two spans. We'll replace the entire content.

# Let's do:
pattern = r'(<h1 class="title reveal">)(.*?)(</h1>)'
replacement = r'\1<span class="lang-pt">' + title_pt + r'</span><span class="lang-en">' + title_en + r'</span>\3'
template = re.sub(pattern, replacement, template, flags=re.DOTALL)

# We also need to update the localStorage key in the JavaScript.
# In the template, there is a script that sets the language for that session.
# We need to change the key from 'joseph-s2-lang' to 'joseph-s5-lang'
# We'll find the script tag and replace the key.

# We'll do two replacements in the script:
#   1. localStorage.setItem('joseph-s2-lang',l) -> localStorage.setItem('joseph-s5-lang',l)
#   2. localStorage.getItem('joseph-s2-lang') -> localStorage.getItem('joseph-s5-lang')

# We'll do a simple string replace for these.

template = template.replace("localStorage.setItem('joseph-s2-lang',l)", "localStorage.setItem('joseph-s5-lang',l)")
template = template.replace("localStorage.getItem('joseph-s2-lang')", "localStorage.getItem('joseph-s5-lang')")

# Now we need to replace the content of the div (from the opening div with class "max-w-4xl mx-auto px-5 py-12 md:py-16" to the closing div before the script)
# We'll use a similar approach as in build_s4.py.

# We'll split the template into three parts: before the div, the div (with its opening and closing), and after the div (which includes the script).
# Actually, we want to keep the div tags and replace the inner content.

# Let's find the div and its closing tag that is immediately followed by the script.
# We'll use a regex to capture:
#   (everything before the div) (the opening div) (the inner content) (the closing div and the script that follows) (everything after)
# But note: the closing div is followed by a script tag. We want to keep the closing div and the script.

# We'll do:
#   pattern = r'(.*?)(<div class="max-w-4xl mx-auto px-5 py-12 md:py-16">)(.*?)(</div>\s*<script>)(.*)'
#   Then we replace the inner content (group 3) with our new content.

# However, note that the template might have multiple divs. We assume the first one with that class is the one we want.

# Let's try:
pattern = r'(.*?)(<div class="max-w-4xl mx-auto px-5 py-12 md:py-16">)(.*?)(</div>\s*<script>)(.*)'
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
    rule_split = inner_old.split('<hr class="rule">', 1)
    if len(rule_split) == 2:
        before_rule = rule_split[0]  # includes the title and maybe some whitespace
        after_rule = rule_split[1]   # everything after the rule
        # We will keep before_rule and the rule, and then replace after_rule with our page content.
        new_inner = before_rule + '<hr class="rule">'
    else:
        # If we can't find the rule, we just keep the entire inner_old and then append our page content? 
        # But we don't want to duplicate. Let's just use the inner_old and then append.
        new_inner = inner_old
    
    # Now we generate the page content.
    for i, text in enumerate(pages_text):
        # Escape HTML in text
        text_escaped = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        # Replace newlines with <br> for simplicity
        text_escaped = text_escaped.replace('\n', '<br>')
        new_inner += f'<div class="page reveal">{text_escaped}</div>'
        # Check if there is an image for this page
        img_path = f"img/sessao-5/p{i+1}-vector.png"
        if os.path.exists(f"{output_dir}/{img_path}"):
            new_inner += f'<div class="table-img reveal"><img src="{img_path}" alt="Page {i+1} diagram"><p class="caption"><span class="lang-pt">Gênesis X:Y. Tradução e Design Literário por Tim Mackie para BibleProject Classroom: José (2021).</span><span class="lang-en">Genesis X:Y. Translation and Literary Design by Tim Mackie for BibleProject Classroom: Joseph (2021).</span></p></div>'
    
    # Now reconstruct the template
    new_template = before + div_open + new_inner + div_close_script + after
    
    # Write the new template to the output file
    output_path = f"{output_dir}/sessao-5.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_template)
    print(f"Created {output_path}")
else:
    print("Could not find the div pattern in the template")