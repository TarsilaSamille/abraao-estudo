import os, re, fitz
base = os.getcwd()
N = 9
pdf_path = f'pdf-sessoes/sessao-{N+1}.pdf'  # sessao-10.pdf
print(f'PDF path: {pdf_path}')
# Determine modulo from the SESSIONS array in modulo-2/index.html (since we know session 9 is in modulo 2)
with open('modulo-2/index.html', 'r', encoding='utf-8') as f:
    content = f.read()
match = re.search(r'const SESSIONS = (\[.*?\]);', content, re.DOTALL)
if match:
    sessions_json = match.group(1)
    import json
    SESSIONS = json.loads(sessions_json)
    session_info = None
    for s in SESSIONS:
        if s['n'] == N:
            session_info = s
            break
    if session_info is None:
        print(f'Error: Session {N} not found in SESSIONS')
        exit(1)
    title_pt = session_info['title_pt']
    title_en = session_info['title_en']
    # We know session 9 is in modulo 2 (since SESSIONS array is for modulo 2)
    target_module = {'pos': 2, 'first': 7, 'last': 14, 'title_en': 'Exodus from Egypt', 'title_pt': 'Sinais e Maravilhas'}  # approximate, but we don't need the title from MODULES
else:
    print('Could not find SESSIONS array')
    exit(1)
print(f'PT title: {title_pt}')
print(f'EN title: {title_en}')
output_dir = f'modulo-{2}'  # we know it's modulo 2
img_dir = f'{output_dir}/img/sessao-{N}'
os.makedirs(img_dir, exist_ok=True)
# Extract text from PDF and render images
doc = fitz.open(pdf_path)
pages_text = []
for i, page in enumerate(doc):
    pages_text.append(page.get_text())
    if len(page.get_drawings()) >= 8:
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        img_path = f'{img_dir}/p{i+1}-vector.png'
        if not os.path.exists(img_path):
            pix.save(img_path)
            print(f'Rendered {img_path}')
doc.close()
# Load template
template_path = f'modulo-1/sessao-2.html'
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()
# Replace title in HTML title tag: we want "Sessão 9: [title_pt]"
template = re.sub(r'<title>.*?</title>', f'<title>Sessão 9: {title_pt}</title>', template, flags=re.DOTALL)
# Replace the h1.title content: we want both language spans with the session number
pattern = r'(<h1 class="title reveal">)(.*?)(</h1>)'
replacement = r'\1<span class="lang-pt">Sessão 9: ' + title_pt + r'</span><span class="lang-en">Session 9: ' + title_en + r'</span>\3'
template = re.sub(pattern, replacement, template, flags=re.DOTALL)
# Update localStorage key
template = template.replace("localStorage.setItem('exodus-s2-lang',l)", f"localStorage.setItem('exodus-s{N}-lang',l)")
template = template.replace("localStorage.getItem('exodus-s2-lang')", f"localStorage.getItem('exodus-s{N}-lang')")
# Now process the div content
div_open_pattern = r'(<div class="max-w-4xl mx-auto px-5 py-12 md:py-16">)'
match = re.search(div_open_pattern, template)
if not match:
    print('Could not find opening div')
    exit(1)
div_open = match.group(1)
pos_after_open = match.end()
# Find the closing div that is followed by a script tag
remaining = template[pos_after_open:]
close_pattern = r'(</div>\s*<script>)'
match_close = re.search(close_pattern, remaining)
if not match_close:
    print('Could not find closing div followed by script')
    exit(1)
div_close_script = match_close.group(1)
pos_close_start = pos_after_open + match_close.start()
pos_after_close = pos_after_open + match_close.end()
inner_content = template[pos_after_open:pos_close_start]
# We want to keep the h1 and the hr, and replace everything after the hr.
hr_pattern = r'(<hr class="rule">)'
match_hr = re.search(hr_pattern, inner_content)
if not match_hr:
    print('Could not find hr tag in inner content')
    exit(1)
hr_tag = match_hr.group(1)
pos_hr_end = match_hr.end()
# Keep everything up to and including the hr
content_before_hr = inner_content[:pos_hr_end]  # includes the hr
# Generate the page content
page_content = ''
for i, text in enumerate(pages_text):
    # Escape HTML in text
    text_escaped = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # Replace newlines with <br> for simplicity
    text_escaped = text_escaped.replace('\n', '<br>')
    page_content += f'<div class="page reveal">{text_escaped}</div>'
    # Check if there is an image for this page
    img_path = f'img/sessao-{N}/p{i+1}-vector.png'
    if os.path.exists(f'{output_dir}/{img_path}'):
        page_content += f'<div class="table-img reveal"><img src="{img_path}" alt="Page {i+1} diagram"><p class="caption"><span class="lang-pt">�Êxodo X:Y. Tradução e Design Literário por Tim Mackie para BibleProject Classroom: José (2021).</span><span class="lang-en">Exodus X:Y. Translation and Literary Design by Tim Mackie for BibleProject Classroom: Joseph (2021).</span></p></div>'
# New inner content: content_before_hr + page_content
new_inner = content_before_hr + page_content
# Reconstruct the template
new_template = template[:pos_after_open] + new_inner + template[pos_close_start:]
# Write the new template to the output file
output_path = f'{output_dir}/sessao-{N}.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(new_template)
print(f'Created {output_path}')