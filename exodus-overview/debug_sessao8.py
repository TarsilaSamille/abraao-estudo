import os, re, fitz, json
base = os.getcwd()
N = 8
pdf_path = f'pdf-sessoes/sessao-{N+1}.pdf'
print('PDF path:', pdf_path)
# Determine modulo from index.html SESSIONS array (root)
index_path = f'../index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()
print('index content first 500 chars:', index_content[:500])
# Find MODULES array
pattern = r'const MODULES = (\\[.*?\\]);'
match = re.search(pattern, index_content, re.DOTALL)
if match:
    modules_json = match.group(1).replace("'", '"')
    print('modules_json:', modules_json)
    MODULES = json.loads(modules_json)
else:
    print('no MODULES match')
    MODULES = [
        {'pos': 1, 'first': 1, 'last': 6, 'title_en': 'Moses Delivered and Commissioned', 'title_pt': 'Moisés Libertado e Comissionado'},
        {'pos': 2, 'first': 7, 'last': 14, 'title_en': 'Exodus from Egypt', 'title_pt': '���Êxodo do Egito'},
        {'pos': 3, 'first': 15, 'last': 22, 'title_en': 'A Covenant at Mount Sinai', 'title_pt': 'Uma Aliança no Monte Sinai'},
        {'pos': 4, 'first': 23, 'last': 28, 'title_en': 'Presence in the Tabernacle', 'title_pt': 'Presença no Tabernáculo'},
        {'pos': 5, 'first': 29, 'last': 30, 'title_en': 'Reflecting on Exodus', 'title_pt': 'Refletindo sobre ��� � � Êxodo'}
    ]
target_module = None
for m in MODULES:
    if m['first'] <= N <= m['last']:
        target_module = m
        break
print('target_module:', target_module)
if target_module is None:
    print('Error: Session {} not found in any module'.format(N))
    exit(1)
output_dir = f'modulo-{target_module["pos"]}'
img_dir = f'{output_dir}/img/sessao-{N}'
os.makedirs(img_dir, exist_ok=True)
# Get titles from module's index.html
module_index_path = f'{output_dir}/index.html'
with open(module_index_path, 'r', encoding='utf-8') as f:
    module_index_content = f.read()
print('module_index content first 500 chars:', module_index_content[:500])
session_pattern = r'const SESSIONS = (\\[.*?\\]);'
session_match = re.search(session_pattern, module_index_content, re.DOTALL)
if session_match:
    sessions_json = session_match.group(1).replace("'", '"')
    print('sessions_json:', sessions_json)
    SESSIONS = json.loads(sessions_json)
else:
    print('no SESSIONS match in module index')
    SESSIONS = []
print('SESSIONS list:')
for s in SESSIONS:
    print(s)
session_info = None
for s in SESSIONS:
    if s['n'] == N:
        session_info = s
        break
print('session_info:', session_info)
if session_info is None:
    print(f'Error: Session {N} not found in module {target_module["pos"]} SESSIONS')
    # Let's see what n values are present
    ns = [s['n'] for s in SESSIONS]
    print('Available n:', ns)
    exit(1)
title_pt = session_info['title_pt']
title_en = session_info['title_en']
print(f'PT title: {title_pt}')
print(f'EN title: {title_en}')
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
print('Number of pages:', len(pages_text))
# Load template
template_path = f'modulo-1/sessao-2.html'
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()
print('Template loaded, length:', len(template))
# Replace title in HTML title tag
template = re.sub(r'<title>.*?</title>', f'<title>{title_pt}</title>', template, flags=re.DOTALL)
# Replace the h1.title content
pattern = r'(<h1 class="title reveal">)(.*?)(</h1>)'
replacement = r'\\1<span class="lang-pt">' + title_pt + r'</span><span class="lang-en">' + title_en + r'</span>\\3'
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
        page_content += f'<div class="table-img reveal"><img src="{img_path}" alt="Page {i+1} diagram"><p class="caption"><span class="lang-pt">���Êxodo X:Y. Tradução e Design Literário por Tim Mackie para BibleProject Classroom: José (2021).</span><span class="lang-en">Exodus X:Y. Translation and Literary Design by Tim Mackie for BibleProject Classroom: Joseph (2021).</span></p></div>'
# New inner content: content_before_hr + page_content
new_inner = content_before_hr + page_content
# Reconstruct the template
new_template = template[:pos_after_open] + new_inner + template[pos_close_start:]
# Write the new template to the output file
output_path = f'{output_dir}/sessao-{N}.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(new_template)
print(f'Created {output_path}')
