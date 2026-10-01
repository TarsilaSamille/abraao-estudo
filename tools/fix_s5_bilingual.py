#!/usr/bin/env python3
"""
fix_s5_bilingual.py — wrap the English-only blocks of abraao sessao 5.

The session balanced 84 lang-pt / 84 lang-en, but a large amount of text sat
*outside* any lang span: scripture labels, the seven-line blessing
decompositions, the curse list, the NASB verses, both tables and the two
promise quotes. Because those nodes carry no lang class, the shared rules
`html[lang^="pt"] .lang-en {display:none}` never hide them, so in PT mode the
English stayed on screen and the Portuguese never appeared.

Every replacement keeps the existing markup and only inserts the missing pair,
so the highlights (.lit, .stop, .mark) and the bold/bible-references survive.
"""
import re
import sys

F = "abraao/modulo-2/sessao-5.html"
src = open(F, encoding="utf-8").read()
before_pt = len(re.findall(r'class="lang-pt"', src))
n = 0


def sub1(pattern, repl, note, flags=0):
    """Replace every occurrence; count only real changes."""
    global src, n
    new, k = re.subn(pattern, repl, src, flags=flags)
    if k:
        src = new
        n += k
        print(f"  {k:>3}  {note}")
    else:
        print(f"    0  {note}  (NAO ENCONTRADO)")


def pair(pt, en, cls='lang-pt'):
    return (f'<span class="lang-pt">{pt}</span>'
            f'<span class="lang-en">{en}</span>')


print("1. rotulos de traducao")
sub1(r'<span class="font-medium text-\[#4f5669\]">Instructor’s Translation</span>',
     lambda m: pair('Tradução do Instrutor', 'Instructor’s Translation'),
     "Instructor's Translation -> par PT/EN")

print("2. listas de sete linhas (12:2-3, duas ocorrencias)")
L12 = [
    ("and I will make you a great nation", "E farei de você uma grande nação"),
    (None, None),  # placeholder handled by regex below (has <b>bless</b>)
]
sub1(r'<li>and I will make you a great nation</li>',
     '<li>' + pair("E farei de você uma grande nação", "and I will make you a great nation") + '</li>',
     "12:2-3 linha 1")
sub1(r'<li>and I will <b>bless</b> you,</li>',
     '<li>' + pair("e eu o <b>abençoarei</b>,", "and I will <b>bless</b> you,") + '</li>',
     "12:2-3 linha 2")
sub1(r'<li>and I will make your name great;</li>',
     '<li>' + pair("e farei grande o seu nome;", "and I will make your name great;") + '</li>',
     "12:2-3 linha 3")
sub1(r'<li>and so you shall be a <b>blessing</b>;</li>',
     '<li>' + pair("e assim você será uma <b>bênção</b>;", "and so you shall be a <b>blessing</b>;") + '</li>',
     "12:2-3 linha 4")
sub1(r'<li>and I will <b>bless</b> those who <b>bless</b> you,</li>',
     '<li>' + pair("e <b>abençoarei</b> os que o <b>abençoarem</b>,", "and I will <b>bless</b> those who <b>bless</b> you,") + '</li>',
     "12:2-3 linha 5")
sub1(r'<li>and the one who treats you as cursed I will curse;</li>',
     '<li>' + pair("e aquele que o tratar como amaldiçoado eu amaldiçoarei;",
                   "and the one who treats you as cursed I will curse;") + '</li>',
     "12:2-3 linha 6")
sub1(r'<li>and in you all the clan-families of the land will find <b>blessing</b>\.</li>',
     '<li>' + pair("e em você todas as famílias da terra encontrarão <b>bênção</b>.",
                   "and in you all the clan-families of the land will find <b>blessing</b>.") + '</li>',
     "12:2-3 linha 7")

print("3. as cinco maldicoes")
CURSES = [
    ("Gen. 3:14 “cursed! are you” (snake)",
     "Gn. 3:14 “amaldiçoado! é você” (serpente)"),
    ("Gen. 3:17 “cursed! is the ground because of you” (man)",
     "Gn. 3:17 “amaldiçoado! é o solo por sua causa” (homem)"),
    ("Gen. 3:14 “cursed! are you from the ground” (Cain)",
     "Gn. 3:14 “amaldiçoado! é você, do solo” (Caim)"),
    ("Gen. 3:14 “the ground which Yahweh has cursed!”",
     "Gn. 3:14 “o solo que Yahweh amaldiçoou!”"),
    ("Gen. 3:14 “cursed! is Canaan”",
     "Gn. 3:14 “amaldiçoado! é Canaã”"),
]
for en, pt in CURSES:
    sub1(r'<li>' + re.escape(en) + r'</li>',
         lambda m, pt=pt, en=en: '<li>' + pair(pt, en) + '</li>',
         f"maldicao {en[:28]}")

print("4. Genesis 26:3-4")
G26 = [
    ("and I will be with you,", "e eu estarei com você,"),
    ("and I will bless you,", "e eu o abençoarei,"),
    ("for to you and to your descendants I will give all these lands,",
     "pois a você e à sua descendência darei todas estas terras,"),
    ("and I will fulfil the oath which I swore to Avraham your father.",
     "e cumprirei o juramento que fiz ao seu pai Avram."),
    ("I will multiply your descendants as the stars of heaven,",
     "multiplicarei a sua descendência como as estrelas do céu,"),
    ("and will give to your descendants all these lands;",
     "e darei à sua descendência todas estas terras;"),
    ("and by your descendants all the nations of the earth shall bless themselves.",
     "e pela sua descendência todas as nações da terra se abençoarão."),
]
for en, pt in G26:
    sub1(r'<li>' + re.escape(en) + r'</li>',
         lambda m, pt=pt, en=en: '<li>' + pair(pt, en) + '</li>',
         f"26:3-4 {en[:30]}")

print("5. Genesis 27:28-29")
G27 = [
    ("May God give you of the dew of heaven, etc.",
     "Que Deus lhe dê do orvalho do céu, etc."),
    ("Let peoples serve you,", "Que os povos prestem serviço a você,"),
    ("and nations bow down to you.", "e as nações se curvem diante de você."),
    ("Be lord over your brothers,", "Seja senhor sobre seus irmãos,"),
    ("and may your mother’s sons bow down to you.",
     "e os filhos de sua mãe se curvem diante de você."),
    ("Cursed be every one who curses you,",
     "Maldito seja todo aquele que o amaldiçoar,"),
    ("and blessed be every one who blesses you!",
     "e bendito seja todo aquele que o abençoar!"),
]
for en, pt in G27:
    sub1(r'<li>' + re.escape(en) + r'</li>',
         lambda m, pt=pt, en=en: '<li>' + pair(pt, en) + '</li>',
         f"27:28-29 {en[:30]}")

print("6. versiculos NASB")
sub1(r'(<p class="verse-text">)(Terah took Abram his son.*?)</p>',
     lambda m: m.group(1) + pair(
         "Terakh tomou Abrão, seu filho, e Ló, filho de Harã, seu neto, e Sarai, sua nora, "
         "esposa de seu filho Abrão; e saíram juntos de Ur dos Caldeus para entrar na terra "
         "de Canaã; e foram até Harã e ali se estabeleceram.",
         m.group(2)) + '</p>',
     "Genesis 11:31 NASB")
sub1(r'(<p class="verse-text">)(Abram took Sarai his wife.*?)</p>',
     lambda m: m.group(1) + pair(
         "Abrão levou Sarai, sua esposa, e Ló, seu sobrinho, e todos os bens que ajuntaram, e as "
         "pessoas que称作 em Harã, e partiram para a terra de Canaã; assim chegaram à terra de Canaã.",
         m.group(2)) + '</p>',
     "Genesis 12:5 NASB")

print("7. tabelas")
T1 = [
    ("<th>Adam’s Sons in Genesis 4</th>",
     pair("Filhos de Adão em Gênesis 4", "Adam’s Sons in Genesis 4")),
    ("<th>Noah’s “Sons” in Genesis 12</th>",
     pair("“Filhos” de Noé em Gênesis 12", "Noah’s “Sons” in Genesis 12")),
]
for old, new in T1:
    sub1(re.escape(old), lambda m, new=new: "<th>" + new + "</th>", old[:40])

# table cells: wrap the whole <td> body in a lang pair
CELL_PT = [
    ("Abel was a “shepherd of the flock” and made offerings to Yahweh from his flock",
     "Abel era um “pastor do rebanho” e fazia ofertas a Yahweh com seu rebanho"),
    ("Avram (from the line of Shem) leads a migrating shepherd caravan with many flocks",
     "Avram (da linhagem de Sem) conduz uma caravana migratória de pastores com muitos rebanhos"),
    ("Seth, the seed given in the place of Abel, has his first son, named Enosh (= “human”), when “it was begun, calling on the name of Yahweh.”",
     "Sete, a descendência dada no lugar de Abel, tem seu primeiro filho, chamado Enosh (= “humano”), quando “se começou a chamar sobre o nome de Yahweh”."),
    ("Avram builds altars in Canaan and “calls upon the name of Yahweh”",
     "Avram constrói altares em Canaã e “chama sobre o nome de Yahweh”"),
    ("Cain was a farmer (Gen. 4:1-4), who, after his murder of Abel the shepherd, went on to build the first city in the Bible and named it after his first son, Khanok (= “dedicated,” Gen. 4:17)",
     "Caim era um agricultor (Gn. 4:1-4), que, depois de matar Abel, o pastor, passou a construir a primeira cidade da Bíblia e a lhe dar o nome de seu primeiro filho, Qanoc (= “dedicada”, Gn. 4:17)"),
    ("The Canaanites (from the line of Ham), in contrast to Avram, live in the cities",
     "Os Cananeus (da linhagem de Ham), em contraste com Avram, vivem nas cidades"),
]
for en, pt in CELL_PT:
    sub1(r'(<b>Gen\. [^<]*</b>)' + re.escape(en) + r'(</td>)',
         lambda m, pt=pt: "<td>" + pair(m.group(1) + pt, m.group(1) + en) + "</td>",
         f"celula {en[:34]}")

print("   tabela 2 — coluna Joshua e demais paragrafos")
# <span class="stop">Stop #N: X</span>
def stop_repl(m):
    num, place = m.group(1), m.group(2)
    return ('<span class="stop">'
            + pair(f"Parada #{num}: {place}", f"Stop #{num}: {place}")
            + '</span>')
sub1(r'<span class="stop">Stop #(\d+): ([^<]+)</span>', stop_repl,
     "rotulos Stop -> Parada", )

# the <p> bodies of the journey table
JP = [
    ("<b>Gen. 12:6-7</b> And <span class=\"lit lit-shechem\">Avram passed through in the land until the place of Shechem</span>, unto the Terebinth of Vision … And he built an altar there to Yahweh who appeared to him.",
     "<b>Gen. 12:6-7</b> E <span class=\"lit lit-shechem\">Avram passou pela terra até o lugar de Siquém</span>, até o Terebinto da Visão … E construiu ali um altar a Yahweh, que lhe apareceu."),
    ("<b>Gen. 33:18, 20</b> And <span class=\"lit lit-shechem\">Jacob came safely to the city of Shechem</span>, which is in the land of Canaan, when he returned from Paddan-Aram, and he camped in front of the city … And he set up a pillar there, and called it “El, the God of Israel.”",
     "<b>Gen. 33:18, 20</b> E <span class=\"lit lit-shechem\">Jacó chegou em paz à cidade de Siquém</span>, que está na terra de Canaã, ao regressar de Padã-Arã, e acampou diante da cidade … E levantou ali um pilar e o chamou “El, o Deus de Israel”."),
    ("<b>Josh. 8:30</b> Then Joshua built an altar to the Lord, the God of Israel, on Mount Ebal [just outside Shechem, see Deut. 11:29-30].",
     "<b>Jos. 8:30</b> Então Josué construiu um altar ao Senhor, Deus de Israel, no monte Ebal [logo fora de Siquém, veja Deut. 11:29-30]."),
    ("<b>Gen. 12:8</b> And he set out from there to the mountain east of Bethel and pitched his tent, with Bethel on the west and Ai on the east. And he <span class=\"lit lit-bethel\">built there an altar</span> to Yahweh and called on the name of Yahweh.",
     "<b>Gen. 12:8</b> E partiu dali para a montanha a leste de Betel e armou sua tenda, com Betel a oeste e Ai a leste. E <span class=\"lit lit-bethel\">construiu ali um altar</span> a Yahweh e chamou sobre o nome de Yahweh."),
    ("<b>Gen. 35:1</b> God said to Jacob, “Get up, go up to Bethel and stay there and <span class=\"lit lit-bethel\">make there an altar</span> to El who appeared to you when you fled from your brother Esau.”",
     "<b>Gen. 35:1</b> Deus disse a Jacó: “Levanta-te, sobe a Betel e fica ali e <span class=\"lit lit-bethel\">faz ali um altar</span> ao El que te apareceu quando fugiste de teu irmão Esaú.”"),
    ("<b>Gen. 35:6-7</b> Jacob came to Luz (that is, Bethel), which is in the land of Canaan … And <span class=\"lit lit-bethel\">he built an altar</span> there, and called the place El-bethel.",
     "<b>Gen. 35:6-7</b> Jacó veio a Luz (isto é, Betel), que está na terra de Canaã … E <span class=\"lit lit-bethel\">construiu um altar</span> ali, e chamou o lugar de El-betel."),
    ("<b>Josh. 7:2</b> Joshua sent men from Jericho to Ai, which is near Beth-aven, east of Bethel, and said to them, “Go up and spy out the land.” So the men went up and spied out Ai.",
     "<b>Jos. 7:2</b> Josué enviou homens de Jericó para Ai, que está perto de Bet-áven, a leste de Betel, e disse-lhes: “Subi e espiona a terra.” Então os homens subiram e espionaram Ai."),
    ("<b>Josh. 8:9</b> Joshua sent them away, and they went to the place of ambush and remained between Bethel and Ai, on the west side of Ai; but Joshua spent that night among the people.",
     "<b>Jos. 8:9</b> Josué os enviou embora, e eles foram ao lugar da emboscada e permaneceram entre Betel e Ai, no lado oeste de Ai; mas Josué passou aquela noite entre o povo."),
    ("<b>Gen. 12:9</b> And Avram set out, continuing and traveling to the Negev.",
     "<b>Gen. 12:9</b> E Avram partiu, seguindo e viajando para o Negeve."),
    ("<b>Gen. 35:27</b> Jacob came home to his father Isaac in Mamre, near Kiriath Arba (that is, Hebron), where Avraham and Isaac had stayed.",
     "<b>Gen. 35:27</b> Jacó voltou para seu pai Isaque em Mamre, perto de Kiriat Arba (isto é, Hebrom), onde Avram e Isaque tinham permanecido."),
    ("<b>Gen. 46:1</b> Israel set out with all that he had, and came to Beersheba, and offered sacrifices to the God of his father Isaac.",
     "<b>Gen. 46:1</b> Israel partiu com tudo o que tinha, e veio a Beer-Seba, e ofereceu sacrifícios ao Deus de seu pai Isaque."),
    ("<b>Josh. 10:40</b> Joshua struck all the land, the hill country and the Negev and the lowland and the slopes and all their kings.",
     "<b>Jos. 10:40</b> Josué feriu toda a terra, o regionamento montanhoso e o Negeve e a planície e os encostas e todos os seus reis."),
    ("<b>Josh. 11:16</b> Thus Joshua took all that land: the hill country and all the Negev, all that land of Goshen, the lowland, the Arabah, the hill country of Israel and its lowland.",
     "<b>Jos. 11:16</b> Assim Josué tomou toda aquela terra: o regionamento montanhoso e todo o Negeve, toda aquela terra de Gósen, a planície, o Arabá, o regionamento montanhoso de Israel e sua planície."),
]
for en, pt in JP:
    sub1(r'<p>' + re.escape(en) + r'</p>', lambda m, pt=pt: '<p>' + pair(pt, en) + '</p>',
         f"journey {en[:30]}")
sub1(r'<th>Joshua \(After Stop #1: Jericho\)</th>',
     lambda m: "<th>" + pair("Josué (Depois da Parada #1: Jericó)",
                              "Joshua (After Stop #1: Jericho)") + "</th>",
     "th Joshua")

print("8. as duas promessas")
sub1(r'<p>“Go to <span class="lit lit-promise">the land</span> I will show you \.\.\. I will bless you and <span class="lit lit-seed">make you a great nation\.</span>”</p>',
     lambda m: '<p>' + pair(
         "“Vai para <span class=\"lit lit-promise\">a terra</span> que eu te mostrarei ... eu te abençoarei e <span class=\"lit lit-seed\">farei de ti uma grande nação.</span>”",
         m.group(0)[3:-4]) + '</p>', "Promessa #1")
sub1(r'<p>“To <span class="lit lit-seed">your seed</span> I will give <span class="lit lit-promise">this land\.</span>”</p>',
     lambda m: '<p>' + pair(
         "“À <span class=\"lit lit-seed\">tua descendência</span> darei <span class=\"lit lit-promise\">esta terra.</span>”",
         m.group(0)[3:-4]) + '</p>', "Promessa #2")

after_pt = len(re.findall(r'class="lang-pt"', src))
after_en = len(re.findall(r'class="lang-en"', src))
print(f"\nsubstituicoes: {n}")
print(f"lang-pt: {before_pt} -> {after_pt}")
print(f"lang-en: {after_en}")
print("balanceado:", after_pt == after_en)
open(F, "w", encoding="utf-8").write(src)
