#!/usr/bin/env python3
"""
fix_s5_literary.py — make the literary-design blocks of abraao sessao 5 bilingual.

`<span class="label">` and `<div class="literary-line">` held English only, so in
PT mode the structure diagram of 12:1-3 and the Sojourn panels stayed English.
The inner `.lit` spans carry the colour-coding and must survive untouched, so
each line is translated with the same span structure. The a/b/a' markers are
identical in both languages and stay outside the lang pair.
"""
import re

F = "abraao/modulo-2/sessao-5.html"
src = open(F, encoding="utf-8").read()


def pair(pt, en):
    return f'<span class="lang-pt">{pt}</span><span class="lang-en">{en}</span>'


# --- labels: bible references are identical in both languages --------------
LABELS = [
    ("Avram’s Sojourn to Bethel", "Estada de Avram em Betel"),
    ("Avram’s Sojourn to Shechem", "Estada de Avram em Siquém"),
    ("Avram’s Sojourn to the Negev", "Estada de Avram no Negeve"),
    ("Blessing and Children in the Promised Land", "Bênção e Filhos na Terra Prometida"),
    ("Worship + Altar for Yahweh", "Adoração + Altar para Yahweh"),
]

# --- literary lines: (english markup, portuguese markup with same spans) ----
LINES = [
    ("“Get yourself going", "“Vá você mesmo"),
    ('<span class="lit lit-from">from</span> <span class="lit lit-nation">your land</span>,',
     '<span class="lit lit-from">da</span> <span class="lit lit-nation">sua terra</span>,'),
    ('and <span class="lit lit-from">from</span> <span class="lit lit-nation">your family</span>,',
     'e <span class="lit lit-from">da</span> <span class="lit lit-nation">sua família</span>,'),
    ('and <span class="lit lit-from">from</span> <span class="lit lit-house">your father’s house</span>,',
     'e <span class="lit lit-from">da</span> <span class="lit lit-house">casa de seu pai</span>,'),
    ("to the land which I will show you.", "para a terra que eu lhe mostrarei."),
    ('2 <span class="lit lit-great">And I will make you a great nation</span>,',
     '2 <span class="lit lit-great">E farei de você uma grande nação</span>,'),
    ("and I will bless you,", "e eu o abençoarei,"),
    ("and I will make your name great;", "e farei grande o seu nome;"),
    ("and so you shall be a blessing.", "e assim você será uma bênção."),
    ('3 And I will <span class="lit lit-bless">bless</span>',
     '3 E eu <span class="lit lit-bless">abençoarei</span>'),
    ('<span class="lit lit-house">those who</span> <span class="lit lit-bless">bless</span> you,',
     '<span class="lit lit-house">os que</span> <span class="lit lit-bless">abençoarem</span> você,'),
    ('and <span class="lit lit-house">the one who</span> treats you as <span class="lit lit-bless">cursed</span>',
     'e <span class="lit lit-house">aquele que</span> o tratar como <span class="lit lit-bless">amaldiçoado</span>'),
    ('I will <span class="lit lit-bless">curse</span>;',
     '<span class="lit lit-bless">amaldiçoarei</span>;'),
    ('and in you all the <span class="lit lit-nation">families of the land</span>',
     'e em você todas as <span class="lit lit-nation">famílias da terra</span>'),
    ('will find blessing.”', 'encontrarão bênção.”'),
    ('6 <span class="lit lit-move">And Avram passed through (ויעבר)</span> <span class="lit lit-land">in the land</span>',
     '6 <span class="lit lit-move">E Avram passou (ויעבר)</span> <span class="lit lit-land">pela terra</span>'),
    ('<span class="lit lit-call">unto the</span> place of Shechem',
     '<span class="lit lit-call">até</span> o lugar de Siquém'),
    ('<span class="lit lit-call">unto the</span> oak of Moreh,',
     '<span class="lit lit-call">até</span> o carvalho de Moré,'),
    ('and the Canaanite was then <span class="lit lit-land">in the land</span>.',
     'e o Cananeu estava então <span class="lit lit-land">na terra</span>.'),
    ('7 And <span class="lit lit-appear">Yahweh appeared to Avram</span> and he said,',
     '7 E <span class="lit lit-appear">Yahweh apareceu a Avram</span> e disse,'),
    ('“To your seed I will give this land.”',
     '“À sua descendência darei esta terra.”'),
    ('And <span class="lit lit-altar">he built there an altar to Yahweh</span> <span class="lit lit-appear">who appeared to him</span>.',
     'E <span class="lit lit-altar">construiu ali um altar a Yahweh</span> <span class="lit lit-appear">que lhe apareceu</span>.'),
    ('8 <span class="lit lit-move">And he moved on (ויעתק)</span> from there',
     '8 <span class="lit lit-move">E partiu (ויעתק)</span> dali'),
    ('to the hill <span class="lit lit-east">from the east</span> of <span class="lit lit-east">Bethel</span>,',
     'para a colina <span class="lit lit-east">a leste</span> de <span class="lit lit-east">Betel</span>,'),
    ("and he spread out his tent,", "e estendeu sua tenda,"),
    ('<span class="lit lit-east">Bethel</span> on the west and Ai <span class="lit lit-east">from the east</span>;',
     '<span class="lit lit-east">Betel</span> a oeste e Ai <span class="lit lit-east">a leste</span>;'),
    ('and <span class="lit lit-altar">he built there an altar to Yahweh</span>',
     'e <span class="lit lit-altar">construiu ali um altar a Yahweh</span>'),
    ('and <span class="lit lit-call">he called upon the name of Yahweh</span>.',
     'e <span class="lit lit-call">chamou sobre o nome de Yahweh</span>.'),
    ('9 <span class="lit lit-move">And Avram journeyed (ויסע)</span>,',
     '9 <span class="lit lit-move">E Avram viajou (ויסע)</span>,'),
    ('continually <span class="lit lit-move">journeying (נסוע)</span> to the Negev.',
     'seguindo <span class="lit lit-move">em sua jornada (נסוע)</span> para o Negeve.'),
]

n = 0
print("labels")
for en, pt in LABELS:
    src, k = re.subn(
        r'<span class="label">' + re.escape(en) + r'</span>',
        lambda m, pt=pt, en=en: '<span class="label">' + pair(pt, en) + '</span>',
        src)
    n += k
    print(f"  {k}  {en}")

print("literary lines")
for en, pt in LINES:
    # only the content span; the a/b/a' marker stays outside the lang pair
    pat = (r'(<div class="literary-line"><span class="mark">[^<]*</span><span>)'
           + re.escape(en) + r'(</span></div>)')
    src, k = re.subn(
        pat,
        lambda m, pt=pt, en=en: m.group(1) + pair(pt, en) + m.group(2),
        src, flags=re.S)
    n += k
    print(f"  {k}  {re.sub(r'<[^>]+>', '', en)[:52]}")

open(F, "w", encoding="utf-8").write(src)
pt_n = len(re.findall(r'class="lang-pt"', src))
en_n = len(re.findall(r'class="lang-en"', src))
print(f"\nsubstituicoes: {n}")
print(f"lang-pt: {pt_n} | lang-en: {en_n} | balanceado: {pt_n == en_n}")
