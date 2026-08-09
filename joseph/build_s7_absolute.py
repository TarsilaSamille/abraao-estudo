import fitz
import os
import re

# Use absolute path to avoid any confusion
base = "/Users/macbook/GitHub/biblia-estudo/joseph"
pdf_path = os.path.join(base, "pdf-sessoes", "sessao-8.pdf")
template_path = os.path.join(base, "modulo-1", "sessao-2.html")
output_dir = os.path.join(base, "modulo-2")
img_dir = os.path.join(output_dir, "img", "sessao-7")
os.makedirs(img_dir, exist_ok=True)

print(f"Base: {base}")
print(f"PDF path: {pdf_path}")
print(f"Template path: {template_path}")
print(f"Output dir: {output_dir}")
print(f"Img dir: {img_dir}")

# Render images if not already done (pages with >=8 drawings)
doc = fitz.open(pdf_path)
for i, page in enumerate(doc):
    if len(page.get_drawings()) >= 8:
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        img_path = os.path.join(img_dir, f"p{i+1}-vector.png")
        if not os.path.exists(img_path):
            pix.save(img_path)
            print(f"Rendered {img_path}")
doc.close()

# Extract text from PDF
doc = fitz.open(pdf_path)
pages_text = [page.get_text() for page in doc]
doc.close()

# Get title from first line of first page
first_page_text = pages_text[0].strip()
title_lines = first_page_text.split('\n')
title_extracted = ""
for line in title_lines:
    if line.strip():
        title_extracted = line.strip()
        break
if not title_extracted:
    title_extracted = "Down Into the Pit"  # fallback

# We'll use the extracted title for both PT and EN (as placeholder)
title_pt = f"Sessão 7: {title_extracted}"
title_en = f"Session 7: {title_extracted}"

# Load template
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

# Replace title in the HTML title tag
template = re.sub(r'<title>.*?</title>', f'<title>{title_pt}</title>', template, flags=re.DOTALL)

# Replace the h1.title content
pattern = r'(<h1 class=\"title reveal\">)(.*?)(</h1>)'
replacement = r'\\1<span class=\"lang-pt\">' + title_pt + r'</span><span class=\"lang-en\">' + title_en + r'</span>\\3'
template = re.sub(pattern, replacement, template, flags=re.DOTALL)

# Update localStorage key in JavaScript
template = template.replace("localStorage.setItem('joseph-s2-lang',l)", "localStorage.setItem('joseph-s7-lang',l)")
template = template.replace("localStorage.getItem('joseph-s2-lang')", "localStorage.getItem('joseph-s7-lang')")

# Now we split the template by the hr tag and replace the content between hr and the closing div+script.
hr_tag = '<hr class=\"rule\">'
hr_index = template.find(hr_tag)
if hr_index == -1:
    print("Could not find the hr tag in the template")
else:
    # Part 1: from start to after the hr tag
    part1 = template[:hr_index + len(hr_tag)]
    
    # The rest after the hr tag
    rest = template[hr_index + len(hr_tag):]
    
    # Now we look for the pattern: closing div followed by script tag
    pattern = r'(.*?)(</div>\\s*<script>)(.*)'
    match = re.search(pattern, rest, re.DOTALL)
    if match:
        # The content between the hr and the closing div+script is match.group(1) -> we will replace this.
        # The closing div and script is match.group(2)
        # The rest after is match.group(3)
        part2 = match.group(1)   # we will replace this with our page content
        part3 = match.group(2)   # the closing div and script
        part4 = match.group(3)   # everything after
        
        # Now we generate the page content.
        new_inner = ""
        for i, text in enumerate(pages_text):
            # Escape HTML in text
            text_escaped = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            # Replace newlines with <br> for simplicity
            text_escaped = text_escaped.replace('\\n', '<br>')
            new_inner += f'<div class=\"page reveal\">{text_escaped}</div>'
            # Check if there is an image for this page
            img_path = os.path.join("img", "sessao-7", f"p{i+1}-vector.png")
            img_full_path = os.path.join(output_dir, img_path)
            if os.path.exists(img_full_path):
                new_inner += f'<div class=\"table-img reveal\"><img src=\"{img_path}\" alt=\"Page {i+1} diagram\"><p class=\"caption\"><span class=\"lang-pt\">Gênesis X:Y. Tradução e Design Literário por Tim Mackie para BibleProject Classroom: José (2021).</span><span class=\"lang-en\">Genesis X:Y. Translation and Literary Design by Tim Mackie for BibleProject Classroom: Joseph (2021).</span></p></div>'
        
        # Now reconstruct the template
        new_template = part1 + new_inner + part3 + part4
        
        # Write the new template to the output file
        output_path = os.path.join(output_dir, "sessao-7.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_template)
        print(f"Created {output_path}")
    else:
        print("Could not find the closing div and script pattern in the template")