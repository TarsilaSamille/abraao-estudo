import fitz
import os
import re
import json

base = os.getcwd()
print("base:", base)
N = 21
pdf_path = f"{base}/pdf-sessoes/sessao-{N+1}.pdf"  # sessao-22.pdf
print("pdf_path:", pdf_path)
print("pdf exists:", os.path.exists(pdf_path))

# Read index.html to determine modulo
index_path = f"{base}/index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()
print("index_content length:", len(index_content))

# Find the MODULES array
pattern = r'const MODULES = (\\[.*?\\]);'
match = re.search(pattern, index_content, re.DOTALL)
if match:
    modules_json = match.group(1)
    modules_json = modules_json.replace("'", '"')
    try:
        MODULES = json.loads(modules_json)
        print("MODULES loaded:", MODULES)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)
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

print("target_module:", target_module)
if target_module is None:
    print(f"Error: Session {N} not found in any module")
    exit(1)

output_dir = f"{base}/modulo-{target_module['pos']}"
img_dir = f"{output_dir}/img/sessao-{N}"
print("output_dir:", output_dir)
print("img_dir:", img_dir)
os.makedirs(img_dir, exist_ok=True)

# Now, get the titles from the module's index.html
module_index_path = f"{output_dir}/index.html"
print("module_index_path:", module_index_path)
with open(module_index_path, 'r', encoding='utf-8') as f:
    module_index_content = f.read()
print("module_index_content length:", len(module_index_content))
print("First 200 chars:", module_index_content[:200])

# Find the SESSIONS array in the module's index.html
session_pattern = r'const SESSIONS = (\\[.*?\\]);'
session_match = re.search(session_pattern, module_index_content, re.DOTALL)
if session_match:
    sessions_json = session_match.group(1)
    sessions_json = sessions_json.replace("'", '"')
    print("sessions_json:", sessions_json)
    try:
        SESSIONS = json.loads(sessions_json)
        print("SESSIONS loaded:", SESSIONS)
    except json.JSONDecodeError as e:
        print("Failed to parse SESSIONS JSON:", e)
        SESSIONS = []
else:
    SESSIONS = []
    print("No SESSIONS match")

# Find the session with n=N
session_info = None
for s in SESSIONS:
    if s["n"] == N:
        session_info = s
        break

print("session_info:", session_info)
if session_info is None:
    print(f"Error: Session {N} not found in module {target_module['pos']} SESSIONS")
    exit(1)

title_pt = session_info["title_pt"]
title_en = session_info["title_en"]
print(f"PT title: {title_pt}")
print(f"EN title: {title_en}")
