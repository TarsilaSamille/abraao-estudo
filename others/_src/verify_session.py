#!/usr/bin/env python3
"""Verificador de cobertura de uma sessão contra o PDF.
Uso: python3 verify_session.py <arquivo.html> <arquivo_full.txt>
Pontua 0-100 baseado em: marcadores-chave, referências bíblicas, seções, designs.
"""
import sys, re

PDF_REF_LABELS = [
    "Genesis 4:10","Genesis 6:13","Genesis 18:20-21","Genesis 15:13-14","Genesis 16:1, 6","Exodus 1:11","Exodus 22:21-23",
    "Genesis 17:1-3","Genesis 17:4-8","Genesis 17:9-14","Genesis 17:15-16","Genesis 17:17-22","Genesis 17:23-27",
    "Genesis 9:8-17","Genesis 9:18-20","Genesis 10:1-32","Genesis 12:1-9","Genesis 12:10-20","Genesis 13",
    "Genesis 16:7-16","Genesis 1:26","Genesis 1:28","Genesis 2:23","Genesis 3:20","Genesis 6:9","Genesis 6:10",
    "Genesis 6:18","Genesis 7:13","Genesis 7:16","Genesis 9:9","Genesis 9:12","Genesis 9:17","Genesis 17:20",
]
# Rótulos de ref que devem aparecer NAS TABELAS (o PDF mostra a ref acima de cada citação)
TABLE_REF_LABELS = ["Gn 1:26","Gn 1:28","Gn 2:23","Gn 3:20","Gn 6:9","Gn 6:10","Gn 6:18","Gn 7:13","Gn 7:16","Gn 9:9","Gn 9:12","Gn 9:17","Gn 17:20","Gn 9:8-17","Gn 9:18-20","Gn 10:1-32","Gn 12:1-9","Gn 12:10-20","Gn 13","Gn 16:7-16"]
MARKERS = [
    "The De-creation and Re-creation of Avram and Sarai",
    "This complex narrative is designed to culminate",
    "Yahweh's Appeal to Israel",
    "Turn to Me and Live",
    "Rainbow","Circumcision",
    "A symbol of God's judgment and mercy that",
    "brought a remnant safely through death",
    "A symbol of God's judgment on Avraham's penis",
    "Avraham and Sarah, Adam and Eve",
    "Mother of All Living",
    "Father of a Multitude",
    "Queen",
    "Kenites","Samaritans","Benjaminite",
    "twelve princes",
    "violence and covenant love",
    "cut off all flesh",
    "hyperlinks",
    "ezer",
]
SECTIONS_EN = ["Key Takeaways","Yahweh Hears","Genesis 15-16 Replays","Covenant #2","Macro Design","Translation and Literary Design","Avraham and Noah","Avraham and Sarah, Adam and Eve","Father and Mother","Reflection Question"]
SECTIONS_PT = ["Pontos-Chave","Yahweh Ouve","Gênesis 15-16 Repete","Aliança #2","Design Macro","Tradução e Design Literário","Avraham e Noé","Avraham e Sara, Adão e Eva","Pai e Mãe","Questão para Reflexão"]

def score(html):
    # split EN / PT
    en = html.split('<div class="lang-en">')[1].split('<div class="lang-pt')[0] if '<div class="lang-en">' in html else html
    pt = html.split('<div class="lang-pt')[1] if '<div class="lang-pt' in html else html
    checks = []
    for label, cond in [
        ("EN speech refs", all(r in en for r in ["Genesis 17:1-3","Genesis 17:4-8","Genesis 17:9-14","Genesis 17:15-16","Genesis 17:17-22","Genesis 17:23-27"])),
        ("EN table ref labels", all(r in en for r in TABLE_REF_LABELS)),
        ("EN markers", sum(m in en for m in MARKERS)),
        ("PT speech refs", all(r in pt for r in ["Gênesis 17:1-3","Gênesis 17:4-8","Gênesis 17:9-14","Gênesis 17:15-16","Gênesis 17:17-22","Gênesis 17:23-27"])),
        ("PT table ref labels", all(r in pt for r in TABLE_REF_LABELS)),
        ("PT markers", sum(m in pt for m in MARKERS)),
        ("EN sections", all(s in en for s in SECTIONS_EN)),
        ("PT sections", all(s in pt for s in SECTIONS_PT)),
        ("width-chiasm", html.count("max-w-[92%]")>=4 and html.count("max-w-[84%]")>=2),
        ("verse-modal", "../js/verse-modal.js" in html),
    ]:
        checks.append((label, cond))
    # report
    miss_markers_en = [m for m in MARKERS if m not in en]
    miss_markers_pt = [m for m in MARKERS if m not in pt]
    miss_refs_en = [r for r in TABLE_REF_LABELS if r not in en]
    miss_refs_pt = [r for r in TABLE_REF_LABELS if r not in pt]
    print("=== VERIFICAÇÃO DE COBERTURA ===")
    print(f"EN markers ausentes ({len(miss_markers_en)}):", miss_markers_en or "NENHUM")
    print(f"PT markers ausentes ({len(miss_markers_pt)}):", miss_markers_pt or "NENHUM")
    print(f"EN table-refs ausentes ({len(miss_refs_en)}):", miss_refs_en or "NENHUM")
    print(f"PT table-refs ausentes ({len(miss_refs_pt)}):", miss_refs_pt or "NENHUM")
    print("Outros checks:", {k: v for k,v in checks if not isinstance(v,int)})
    # score simples
    total = 4 + len(TABLE_REF_LABELS)*2 + len(MARKERS)*2 + len(SECTIONS_EN) + len(SECTIONS_PT) + 3
    got = 4 + (len(TABLE_REF_LABELS)-len(miss_refs_en)) + (len(TABLE_REF_LABELS)-len(miss_refs_pt)) + (len(MARKERS)-len(miss_markers_en)) + (len(MARKERS)-len(miss_markers_pt)) + len(SECTIONS_EN) + len(SECTIONS_PT) + 3
    print(f"SCORE: {got}/{total} = {round(100*got/total)}%")

if __name__=="__main__":
    html = open(sys.argv[1], encoding='utf-8').read()
    score(html)
