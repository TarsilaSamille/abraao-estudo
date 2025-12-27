"""
Script para comparar o conteúdo do PDF com o HTML gerado
"""
import os
import json
from pathlib import Path
from bs4 import BeautifulSoup

# Carregar análise da estrutura
with open('/Users/tarsilasamille/Documents/GitHub/abraao-estudo/others/pdf_structure_analysis.json', 'r', encoding='utf-8') as f:
    pdf_structure = json.load(f)

# Ler o texto extraído do PDF
with open('/Users/tarsilasamille/Documents/GitHub/abraao-estudo/abraao/extracted_text.txt', 'r', encoding='utf-8') as f:
    pdf_content = f.read()

# Diretório dos HTMLs
html_dir = Path('/Users/tarsilasamille/Documents/GitHub/abraao-estudo/abraao')

# Sessões do PDF (páginas reais do conteúdo)
sessions_info = [
    {"num": 1, "pages": (5, 9), "title": "Session 1: Abraham and Sarah in the Biblical"},
    {"num": 2, "pages": (10, 13), "title": "Session 2: The Abraham Story as a Whole"},
    {"num": 3, "pages": (14, 17), "title": "Session 3: The Literary Design of Genesis 1-11"},
    {"num": 4, "pages": (18, 29), "title": "Session 4: A Tale of Two Journeys"},
    {"num": 5, "pages": (30, 41), "title": "Session 5: God Calls Avram and Promises Blessing"},
    {"num": 6, "pages": (42, 47), "title": "Session 6: Abram the Snake"},
    {"num": 7, "pages": (48, 54), "title": "Session 7: Abram and Lot Separate"},
    {"num": 8, "pages": (55, 59), "title": "Session 8: God's Second Promise to Abram"},
    {"num": 9, "pages": (60, 70), "title": "Session 9: A Flood of Violence"},
    {"num": 10, "pages": (71, 76), "title": "Session 10: Melchizedek the Royal Priest"},
]

print("=== ANÁLISE DE DIFERENÇAS PDF vs HTML ===\n")

differences_report = {
    "sessions_analyzed": [],
    "missing_content": [],
    "structural_differences": []
}

# Analisar algumas sessões
for session in sessions_info[:5]:  # Analisar as primeiras 5 sessões
    session_num = session["num"]
    start_page, end_page = session["pages"]
    
    # Determinar qual arquivo HTML corresponde
    if session_num <= 3:
        html_file = html_dir / f"modulo-1/sessao-{session_num}.html"
    elif session_num <= 10:
        html_file = html_dir / f"modulo-2/sessao-{session_num}.html"
    else:
        continue
    
    if not html_file.exists():
        print(f"❌ Sessão {session_num}: HTML não encontrado em {html_file}")
        continue
    
    print(f"\n{'='*60}")
    print(f"📄 SESSÃO {session_num}: {session['title']}")
    print(f"{'='*60}")
    print(f"📖 PDF: Páginas {start_page}-{end_page} ({end_page - start_page + 1} páginas)")
    
    # Ler HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remover scripts e estilos
    for script in soup(["script", "style"]):
        script.decompose()
    
    html_text = soup.get_text()
    html_words = len(html_text.split())
    
    # Extrair texto do PDF para essas páginas
    pages = pdf_content.split('================================================================================\nPAGE ')
    session_pdf_text = ""
    for page_num in range(start_page, end_page + 1):
        if page_num < len(pages):
            session_pdf_text += pages[page_num]
    
    pdf_words = len(session_pdf_text.split())
    
    print(f"📊 Palavras no PDF: {pdf_words}")
    print(f"📊 Palavras no HTML: {html_words}")
    
    # Calcular diferença
    diff_percentage = abs(pdf_words - html_words) / pdf_words * 100 if pdf_words > 0 else 0
    print(f"📈 Diferença: {diff_percentage:.1f}%")
    
    # Verificar elementos específicos
    print(f"\n🔍 Elementos estruturais no HTML:")
    print(f"   - Títulos (h2): {len(soup.find_all('h2'))}")
    print(f"   - Títulos (h3): {len(soup.find_all('h3'))}")
    print(f"   - Parágrafos: {len(soup.find_all('p'))}")
    print(f"   - Listas: {len(soup.find_all(['ul', 'ol']))}")
    print(f"   - Citações (blockquote): {len(soup.find_all('blockquote'))}")
    print(f"   - Imagens: {len(soup.find_all('img'))}")
    
    # Verificar se há diagramas/ilustrações mencionados no PDF
    if 'illustration' in session_pdf_text.lower() or 'diagram' in session_pdf_text.lower() or 'design by tim mackie' in session_pdf_text.lower():
        print(f"\n⚠️  O PDF contém referências a ilustrações/diagramas")
        has_images = len(soup.find_all('img')) > 0
        print(f"   {'✅' if has_images else '❌'} Imagens encontradas no HTML: {len(soup.find_all('img'))}")
    
    # Verificar referências bíblicas
    pdf_verse_refs = session_pdf_text.count('NIV') + session_pdf_text.count('NASB') + session_pdf_text.count('NAA')
    html_verse_links = len(soup.find_all('a', href='#'))
    
    print(f"\n📖 Referências bíblicas:")
    print(f"   - No PDF: ~{pdf_verse_refs} referências")
    print(f"   - Links no HTML: {html_verse_links}")
    
    session_report = {
        "session": session_num,
        "pdf_words": pdf_words,
        "html_words": html_words,
        "difference_pct": round(diff_percentage, 1),
        "pdf_pages": f"{start_page}-{end_page}",
        "html_file": str(html_file.name)
    }
    differences_report["sessions_analyzed"].append(session_report)

# Salvar relatório
with open('/Users/tarsilasamille/Documents/GitHub/abraao-estudo/others/comparison_report.json', 'w', encoding='utf-8') as f:
    json.dump(differences_report, f, indent=2, ensure_ascii=False)

print(f"\n\n{'='*60}")
print("✅ ANÁLISE CONCLUÍDA")
print("📁 Relatório salvo em: others/comparison_report.json")
print(f"{'='*60}")
