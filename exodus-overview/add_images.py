import re

# Read the current sessao-4.html
with open('modulo-1/sessao-4.html', 'r', encoding='utf-8') as f:
    html = f.read()

# We want to insert the image tags right after the opening div and before the first paragraph.
# Pattern: the opening div, then we want to insert the images, then the rest.
# We'll use a regex to match the opening div and then capture the rest until the closing div? 
# Actually, we can just insert after the opening div.

# Let's split the HTML into two parts: the opening div and the rest.
# We'll use a regex to find the opening div and then insert the images right after it.

pattern = r'(<div class="max-w-4xl mx-auto px-5 py-12 md:py-16">)'
# We'll replace the opening div with itself plus the images and a newline.
replacement = r'\1\n    <img src="modulo-1/img/sessao-4/diagram-page1.svg" alt="Diagram">\n    <img src="modulo-1/img/sessao-4/diagram-page2.svg" alt="Diagram">'

new_html = re.sub(pattern, replacement, html, count=1)

# Write back
with open('modulo-1/sessao-4.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print('Images added.')
