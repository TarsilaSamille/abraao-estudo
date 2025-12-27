"""
Script para analisar a estrutura do PDF e identificar diferenças com o HTML
"""
import os
import json
from pathlib import Path

# Ler o texto extraído
with open('/Users/tarsilasamille/Documents/GitHub/abraao-estudo/abraao/extracted_text.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Dividir por páginas
pages = content.split('================================================================================\nPAGE ')

print(f"Total de páginas encontradas: {len(pages) - 1}")

# Analisar a estrutura
structure = {
    "total_pages": len(pages) - 1,
    "modules": [],
    "sessions": []
}

current_module = None
current_session = None

for i, page in enumerate(pages[1:], 1):  # Skip the first empty split
    lines = page.split('\n')
    page_num = i
    
    # Procurar por módulos
    for line in lines:
        if 'Module' in line and ':' in line:
            module_info = {
                "page": page_num,
                "title": line.strip(),
                "sessions": []
            }
            structure["modules"].append(module_info)
            current_module = module_info
            
        # Procurar por sessões
        if 'Session' in line and ':' in line and 'SESSIONS' not in line:
            session_info = {
                "page": page_num,
                "title": line.strip()
            }
            structure["sessions"].append(session_info)
            if current_module:
                current_module["sessions"].append(session_info)

# Salvar análise
with open('/Users/tarsilasamille/Documents/GitHub/abraao-estudo/others/pdf_structure_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(structure, f, indent=2, ensure_ascii=False)

print("\n=== ESTRUTURA DO PDF ===\n")
print(f"Total de páginas: {structure['total_pages']}")
print(f"Total de módulos: {len(structure['modules'])}")
print(f"Total de sessões: {len(structure['sessions'])}")

print("\n=== MÓDULOS E SUAS SESSÕES ===\n")
for module in structure["modules"]:
    print(f"\n{module['title']} (Página {module['page']})")
    if module['sessions']:
        for session in module['sessions']:
            print(f"  - {session['title']} (Página {session['page']})")

# Calcular distribuição de páginas por sessão
print("\n=== DISTRIBUIÇÃO DE PÁGINAS POR SESSÃO ===\n")
for i, session in enumerate(structure["sessions"]):
    if i < len(structure["sessions"]) - 1:
        pages_in_session = structure["sessions"][i+1]["page"] - session["page"]
    else:
        pages_in_session = structure["total_pages"] - session["page"] + 1
    
    print(f"{session['title']}: {pages_in_session} páginas (Páginas {session['page']}-{session['page'] + pages_in_session - 1})")

print("\n=== ANÁLISE CONCLUÍDA ===")
print("Arquivo salvo em: others/pdf_structure_analysis.json")
