import re

# Read the current sessao-4.html (with updated title and h1)
with open('modulo-1/sessao-4.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Read the extracted text
with open('sessao-4-extracted2.txt', 'r', encoding='utf-8') as f:
    extracted = f.read()

# Split the extracted text into paragraphs (separated by one or more blank lines)
paragraphs = [p.strip() for p in extracted.split('\n\n') if p.strip()]

# Convert each paragraph to an HTML paragraph with language spans
html_paragraphs = []
for p in paragraphs:
    # Escape HTML special characters
    p_escaped = p.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#x27;')
    # Replace newlines within a paragraph with <br> (if any)
    p_escaped = p_escaped.replace('\n', '<br>')
    html_paragraphs.append(f'    <p class="body reveal"><span class="lang-pt">{p_escaped}</span><span class="lang-en">{p_escaped}</span></p>')

# Join the paragraphs with newlines
new_content = '\n'.join(html_paragraphs)

# Replace the content inside the div with class "max-w-4xl mx-auto px-5 py-12 md:py-16"
# Pattern: opening div, then any content (non-greedy) until the closing div followed by script
pattern = r'(<div class="max-w-4xl mx-auto px-5 py-12 md:py-16">)(.*?)(</div>\s*<script>)'
new_html = re.sub(pattern, r'\1\n' + new_content + '\n\3', html, flags=re.DOTALL)

# Write back
with open('modulo-1/sessao-4.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print('Content replaced.')
