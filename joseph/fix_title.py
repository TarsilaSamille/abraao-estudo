import fitz
import os
import re

base = os.getcwd()
N = 7
pdf_path = f"{base}/pdf-sessoes/sessao-{N+1}.pdf"  # sessao-8.pdf

# Extract text from first page
doc = fitz.open(pdf_path)
first_page_text = doc[0].get_text()
doc.close()

# Split into lines and find the one that starts with "Session"
lines = first_page_text.split('\\n')
title_line = ""
for line in lines:
    if line.strip().startswith("Session"):
        title_line = line.strip()
        break
if not title_line:
    # fallback: take the first non-empty line
    for line in lines:
        if line.strip():
            title_line = line.strip()
            break
if not title_line:
    title_line = f"Session {N}: Unknown Title"

# Now we have title_line like "Session 7: Down Into the Pit"
# Extract the part after the colon (including the space after colon if present)
if ': ' in title_line:
    title_part = title_line.split(': ', 1)[1]  # "Down Into the Pit"
    session_prefix = title_line.split(': ')[0] + ': '  # "Session 7: "
else:
    # If no colon, use the whole line as the part and no prefix
    title_part = title_line
    session_prefix = f"Session {N}: "

# Translate title_part to Portuguese (we know this one)
translation_map = {
    "Down Into the Pit": "Descendo para o Poço",
}
title_part_pt = translation_map.get(title_part, title_part)  # fallback

title_pt = f"Sessão {N}: {title_part_pt}"
title_en = f"Session {N}: {title_part}"

print(f"PT title: {title_pt}")
print(f"EN title: {title_en}")

# Now update the generated HTML file
output_dir = f"{base}/modulo-2"  # from previous run we know it's modulo-2
output_path = f"{output_dir}/sessao-{N}.html"

# Read the file
with open(output_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the title tag
content = re.sub(r'<title>.*?</title>', f'<title>{title_pt}</title>', content, flags=re.DOTALL)

# Replace the h1.title content
pattern = r'(<h1 class="title reveal\">)(.*?)(</h1>)'
replacement = r'\\1<span class="lang-pt">' + title_pt + r'</span><span class="lang-en">' + title_en + r'</span>\\3'
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write back
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Updated {output_path}")
