import subprocess
import sys
import re
import html

# Read the template
with open('modulo-1/sessao-1.html', 'r') as f:
    html_template = f.read()

# Find the div
opening = '<div class="max-w-4xl mx-auto px-5 py-12 md:py-16">'
closing = '</div>'

start = html_template.find(opening)
if start == -1:
    print("Error: Opening div not found")
    sys.exit(1)

end = html_template.find(closing, start + len(opening))
if end == -1:
    print("Error: Closing div not found")
    sys.exit(1)

# Build new inner content
new_title_pt = "Sessão 2: Os Temas Principais da Torá"
new_title_en = "Session 2: The Main Themes of the Torah"
new_h1 = f'<h1 class="title reveal"><span class="lang-pt">{new_title_pt}</span><span class="lang-en">{new_title_en}</span></h1>'
new_hr = '<hr class="rule">'

# Extract text from PDF by page
try:
    # Use pdftotext with layout to preserve some formatting
    pdf_text = subprocess.check_output(
        ['pdftotext', 'pdf-sessoes/sessao-3.pdf', '-layout', '-'], 
        stderr=subprocess.STDOUT
    ).decode('utf-8')
except subprocess.CalledProcessError as e:
    print(f"Error running pdftotext: {e}")
    sys.exit(1)

# Split by form feed (ASCII 12)
pages = pdf_text.split('\f')

# Remove empty pages
pages = [page.strip() for page in pages if page.strip()]

# For each page, we want to escape HTML and replace newlines with <br>
generated_content = []
for i, page in enumerate(pages, start=1):
    # Escape HTML
    escaped = html.escape(page)
    # Replace newlines with <br>
    escaped = escaped.replace('\n', '<br>')
    generated_content.append(f'<div class="page reveal">{escaped}</div>')

# Join the generated content
generated_content_str = '\n'.join(generated_content)

# Build the new inner content
new_inner_content = f'{new_h1}\n{new_hr}\n{generated_content_str}'

# Replace the inner content of the div
new_html = html_template[:start+len(opening)] + new_inner_content + html_template[end:]

# Now, replace the localStorage key in the JavaScript
new_html = new_html.replace("ezekiel-s1-lang", "ezekiel-s2-lang")

# Write the output
with open('modulo-1/sessao-2.html', 'w') as f:
    f.write(new_html)

print("Session 2 HTML written to modulo-1/sessao-2.html")
