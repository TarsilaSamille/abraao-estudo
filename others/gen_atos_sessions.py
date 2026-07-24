#!/usr/bin/env python3
"""Generate 28 bilingual(PT) session pages for the Atos dos Apostolos course.

Source: faithful PT rendering of BibleProject's "Guide to the Book of Acts"
(bibleproject.com/guides/book-of-acts) + overview videos. There is NO
official teacher-notes PDF for Acts, so this course is intentionally NOT in the
root catalog (user instruction 2026-07-24: "como n e fiel ao bible project
n coloque no index").

Conventions mirror the repo's gold sessions (abraao/modulo-1/sessao-1.html):
  <body class="bg-white font-sans text-slate-800">
  Back link -> index.html (one level down, inside modulo-N/)
  <h1> Sessão N: <title>
  <h2> Pontos-Chave  + <ul>
  prose <h2>/<p>, verse-link spans (color:inherit, no underline)
  <h2> Questao para Refle xo in a bordered box
  <script src="../js/verse-modal.js">
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import atos_chapters_a, atos_chapters_b

ROOT = os.path.join(os.path.dirname(__file__), "..", "atos-dos-apostolos")

# module for each chapter (1 -> m1, 2-7 -> m2, 8-12 -> m3, 13-20 -> m4, 21-28 -> m5)
def module_of(ch):
    ch = int(ch)
    if ch == 1: return 1
    if ch <= 7: return 2
    if ch <= 12: return 3
    if ch <= 20: return 4
    return 5

CHAPTERS = {**atos_chapters_a.CHAPTERS_A, **atos_chapters_b.CHAPTERS_B}

# ---------------------------------------------------------------------------
# Literary-design boxes (the "design literario" callouts). Faithful syntheses of
# BibleProject's actual Acts literary observations. White fill + colored border
# (measured house model: white box, 2px border). PT title + EN glosa italic.
# ---------------------------------------------------------------------------

def box_open(caption):
    return (
        '<div class="my-10 p-6 rounded-xl border-2 border-slate-300 bg-slate-50">'
        '<span class="inline-block rounded-full bg-slate-800 text-white text-xs font-semibold px-3 py-1 mb-4">'
        'DESIGN LITERÁRIO · BIBLEPROJECT</span>'
    )

def box_close(caption):
    return (f'<p class="mt-5 text-xs italic text-slate-500">{caption}</p>'
            '</div>')

def design_geo_thesis():
    inner = box_open("")
    inner += '<h3 class="text-xl font-bold text-slate-900 mb-1">A tese geográfica de Atos 1:8</h3>'
    inner += '<p class="text-sm italic text-slate-500 mb-5">The geographical thesis of Acts 1:8</p>'
    inner += '<div class="flex flex-col md:flex-row items-stretch gap-3 text-center">'
    stages = [
        ("Jerusalém", "Atos 2-7", "O Espírito desce; nasce a igreja"),
        ("Judeia &amp; Samaria", "Atos 8-12", "A mensagem cruza fronteiras étnicas"),
        ("Confins da Terra", "Atos 13-28", "Paulo leva o Evangelho a todas as nações"),
    ]
    for i, (name, ref, desc) in enumerate(stages):
        inner += (f'<div class="flex-1 rounded-lg border-2 border-slate-400 p-4 bg-white">'
                  f'<div class="font-bold text-slate-900">{name}</div>'
                  f'<div class="text-xs text-slate-500 mt-1">{ref}</div>'
                  f'<div class="text-sm text-slate-600 mt-2">{desc}</div></div>')
        if i < 2:
            inner += '<div class="flex items-center justify-center text-2xl text-slate-400 font-bold">&rarr;</div>'
    inner += '</div>'
    inner += '<p class="mt-5 text-sm text-slate-700">Jesus prometeu: &ldquo;recebereis poder quando o Espírito Santo descer sobre vós, e sereis minhas testemunhas em Jerusalém, Judeia e Samaria, e até os confins da terra&rdquo; (<span class="verse-link" data-reference="Atos+1:8">Atos 1:8</span>). Todo o design de Atos flui desse versículo.</p>'
    inner += box_close("Baseado no Guia de Atos do Bible Project (bibleproject.com/guides/book-of-acts).")
    return inner

def design_pentecost():
    inner = box_open("")
    inner += '<h3 class="text-xl font-bold text-slate-900 mb-1">Pentecoste: o novo templo é o povo</h3>'
    inner += '<p class="text-sm italic text-slate-500 mb-5">Pentecost: the new temple is God’s people</p>'
    inner += '<div class="grid md:grid-cols-2 gap-4">'
    inner += ('<div class="rounded-lg border-2 border-amber-300 p-4 bg-white">'
              '<div class="font-bold text-slate-900 mb-1">Vento &amp; Fogo</div>'
              '<p class="text-sm text-slate-600">Ecoam a presença gloriosa e ardente de Deus enchendo o tabernáculo e o templo '
              '(<span class="verse-link" data-reference="Êxodo+40:38">Êxodo 40:38</span>; '
              '<span class="verse-link" data-reference="2+C rônicas+7:1-3">2 Crônicas 7:1-3</span>).</p></div>')
    inner += ('<div class="rounded-lg border-2 border-sky-300 p-4 bg-white">'
              '<div class="font-bold text-slate-900 mb-1">Promessa Profética</div>'
              '<p class="text-sm text-slate-600">Cumprem a promessa de que Deus habitaria o novo templo do Reino messiânico '
              '(<span class="verse-link" data-reference="Ezequiel+43">Ezequiel 43</span>; '
              '<span class="verse-link" data-reference="Ageu+2">Ageu 2</span>).</p></div>')
    inner += '</div>'
    inner += '<p class="mt-5 text-sm text-slate-700">Em Atos 2, a presença ardente de Deus vem habitar não um edifício, mas o seu povo. O novo templo de que falaram os profetas é a nova família da aliança de Jesus.</p>'
    inner += box_close("Baseado no Guia de Atos do Bible Project.")
    return inner

def design_two_temples():
    inner = box_open("")
    inner += '<h3 class="text-xl font-bold text-slate-900 mb-1">Um conto de dois templos (Atos 3-5)</h3>'
    inner += '<p class="text-sm italic text-slate-500 mb-5">A tale of two temples — a symmetric chiasm</p>'
    rows = [
        ("A", "A comunidade de Jesus cura um coxo e reúne o povo (Atos 3-4)", "border-slate-400"),
        ("B", "Pedro é preso e discursa: Jesus é o verdadeiro Rei (Atos 3-4)", "border-slate-400"),
        ("A'", "No centro: a generosidade partilhada cumpre o propósito do templo (Atos 4:32-5:11)", "border-amber-400 bg-amber-50"),
        ("B'", "Nova prisão dos apóstolos; libertados por um anjo (Atos 5)", "border-slate-400"),
        ("A''", "A comunidade ensina no templo, cheia do Espírito (Atos 5:42)", "border-slate-400"),
    ]
    inner += '<div class="space-y-2">'
    for letter, text, cls in rows:
        pad = "pl-0" if letter in ("A", "A''") else ("pl-8" if letter == "B" else "pl-16")
        inner += (f'<div class="rounded-lg border-2 {cls} p-3 {pad} bg-white flex gap-3 items-start">'
                  f'<span class="font-bold text-lg text-slate-900 w-8">{letter}</span>'
                  f'<span class="text-sm text-slate-700">{text}</span></div>')
    inner += '</div>'
    inner += box_close("Baseado no Guia de Atos do Bible Project (a simetria dos caps. 3-5).")
    return inner

def design_three_bridges():
    inner = box_open("")
    inner += '<h3 class="text-xl font-bold text-slate-900 mb-1">Três pontes sobre a divisão étnica</h3>'
    inner += '<p class="text-sm italic text-slate-500 mb-5">Three bridges crossing ethnic lines (Acts 8-12)</p>'
    bridges = [
        ("Filipe &rarr; Samaria", "Atos 8", "A mensagem chega à terra dos inimigos de Israel"),
        ("Saulo &rarr; Paulo", "Atos 9", "O perseguidor encontra o Cristo e vira missionário"),
        ("Pedro &rarr; Cornélio", "Atos 10", "O Espírito desce sobre gentios; Deus declara-os puros"),
    ]
    inner += '<div class="grid md:grid-cols-3 gap-3">'
    for title, ref, desc in bridges:
        inner += (f'<div class="rounded-lg border-2 border-emerald-300 p-4 bg-white">'
                  f'<div class="font-bold text-slate-900">{title}</div>'
                  f'<div class="text-xs text-slate-500 mt-1">{ref}</div>'
                  f'<div class="text-sm text-slate-600 mt-2">{desc}</div></div>')
    inner += '</div>'
    inner += '<p class="mt-5 text-sm text-slate-700">Cada ponte mostra o Evangelho rompendo a barreira entre Israel e as nações — exatamente como Jesus previu em <span class="verse-link" data-reference="Atos+1:8">Atos 1:8</span>.</p>'
    inner += box_close("Baseado no Guia de Atos do Bible Project.")
    return inner

def design_council():
    inner = box_open("")
    inner += '<h3 class="text-xl font-bold text-slate-900 mb-1">O Concílio de Jerusalém (Atos 15)</h3>'
    inner += '<p class="text-sm italic text-slate-500 mb-5">The Jerusalem Council — three voices, one verdict</p>'
    inner += '<div class="grid md:grid-cols-3 gap-3 mb-4">'
    voices = [
        ("Pedro", "A experiência: o Espírito caiu sobre os gentios como sobre nós (Atos 15:7-11)"),
        ("Paulo &amp; Barnabé", "A pregação: Deus fazia sinais entre os gentios (Atos 15:12)"),
        ("Tiago", "As Escrituras: a profecia de que os gentios buscariam a Deus (Atos 15:13-18)"),
    ]
    for name, text in voices:
        inner += (f'<div class="rounded-lg border-2 border-slate-400 p-4 bg-white">'
                  f'<div class="font-bold text-slate-900">{name}</div>'
                  f'<p class="text-sm text-slate-600 mt-2">{text}</p></div>')
    inner += '</div>'
    inner += ('<div class="rounded-lg border-2 border-emerald-400 bg-emerald-50 p-4 text-center">'
              '<div class="font-bold text-slate-900">Veredito</div>'
              '<p class="text-sm text-slate-700 mt-1">Os gentios são livres de cargas étnicas; devem apenas afastar-se das práticas pagãs (Atos 15:19-21).</p></div>')
    inner += box_close("Baseado no Guia de Atos do Bible Project.")
    return inner

def design_whole_book():
    inner = box_open("")
    inner += '<h3 class="text-xl font-bold text-slate-900 mb-1">O design de todo o livro de Atos</h3>'
    inner += '<p class="text-sm italic text-slate-500 mb-5">The whole-book design: five movements</p>'
    moves = [
        ("M1", "Atos 1", "Jesus comissiona e ascende"),
        ("M2", "Atos 2-7", "Pentecoste em Jerusalém; nasce a igreja"),
        ("M3", "Atos 8-12", "A comunidade vira movimento internacional"),
        ("M4", "Atos 13-20", "Missão a Israel; tensões com a cultura romana"),
        ("M5", "Atos 21-28", "Paulo preso; a testemunha chega a Roma"),
    ]
    inner += '<div class="flex flex-col md:flex-row items-stretch gap-2 text-center">'
    for i, (m, ref, desc) in enumerate(moves):
        inner += (f'<div class="flex-1 rounded-lg border-2 border-slate-400 p-3 bg-white">'
                  f'<div class="font-bold text-slate-900">{m}</div>'
                  f'<div class="text-xs text-slate-500">{ref}</div>'
                  f'<div class="text-sm text-slate-600 mt-1">{desc}</div></div>')
        if i < 4:
            inner += '<div class="flex items-center justify-center text-xl text-slate-400 font-bold">&rarr;</div>'
    inner += '</div>'
    inner += box_close("Baseado no Guia de Atos do Bible Project — a estrutura macro dos cinco movimentos de Lucas.")
    return inner

def design_philippi():
    inner = box_open("")
    inner += '<h3 class="text-xl font-bold text-slate-900 mb-1">A estrutura de Atos 16</h3>'
    inner += '<p class="text-sm italic text-slate-500 mb-5">The structure of Acts 16 — three boundaries crossed</p>'
    inner += '<div class="grid md:grid-cols-3 gap-3 mb-4">'
    steps = [
        ("Fronteira geográfica", "Atos 16:1-10", "A visão do homem da Macedônia leva o Evangelho da Ásia para a Europa"),
        ("Fronteira social", "Atos 16:11-15", "Lídia, vendedora de púrpura, é a primeira conversão europeia"),
        ("Fronteira espiritual", "Atos 16:16-40", "O carcereiro e sua casa creem após o terremoto abrir as prisões"),
    ]
    for title, ref, desc in steps:
        inner += (f'<div class="rounded-lg border-2 border-indigo-300 p-4 bg-white">'
                  f'<div class="font-bold text-slate-900">{title}</div>'
                  f'<div class="text-xs text-slate-500 mt-1">{ref}</div>'
                  f'<div class="text-sm text-slate-600 mt-2">{desc}</div></div>')
    inner += '</div>'
    inner += ('<div class="rounded-lg border-2 border-slate-300 p-5 bg-slate-50">'
              '<div class="font-bold text-slate-900 mb-3">A cena da prisão em Filipos (quiasmo A-B-A&prime;)</div>'
              '<div class="space-y-2">')
    quiasm = [
        ("A", "Oração e cântico à meia-noite — Paulo e Silas louvam a Deus (16:25)", "pl-0"),
        ("B", "Terremoto abre portas e solta correntes — o carcereiro vai se matar (16:26-27)", "pl-8"),
        ("A'", "Paulo detém o carcereiro; \"não te faças mal algum\" — a mensagem de salvação (16:28-34)", "pl-16"),
    ]
    for letter, text, pad in quiasm:
        inner += (f'<div class="rounded-lg border-2 border-slate-400 p-3 {pad} bg-white flex gap-3 items-start">'
                  f'<span class="font-bold text-lg text-slate-900 w-8">{letter}</span>'
                  f'<span class="text-sm text-slate-700">{text}</span></div>')
    inner += '</div></div>'
    inner += box_close("Baseado no Guia de Atos do Bible Project (a chegada do Evangelho à Europa e a cena da prisão em Filipos).")
    # 2a caixa: leitura acadêmica (corrente de design literário / estudos pós-coloniais)
    inner += box_open("")
    inner += '<h3 class="text-xl font-bold text-slate-900 mb-1">A perícope de Filipos na análise acadêmica</h3>'
    inner += '<p class="text-sm italic text-slate-500 mb-5">Scholarly literary readings — Murai (quiasmo) e Cassidy (leitura anti-imperial)</p>'
    inner += ('<div class="rounded-lg border-2 border-amber-300 p-5 bg-white mb-4">'
              '<div class="font-bold text-slate-900 mb-3">Quiasmo concêntrico de Atos 16:11-40 (Hajime Murai)</div>'
              '<div class="space-y-1 text-sm text-slate-700">')
    murai = [
        ("A", "16:11-15 — Lídia, a vendedora de púrpura, e sua casa (Λυδία)"),
        ("B", "16:16-18 — A jovem escrava com espírito de adivinhação é libertada"),
        ("C", "16:19-24 — Prisão: Paulo e Silas lançados ao cárcere, guardados pelo carcereiro (δεσμοφύλακι)"),
        ("D", "16:25-27 — À meia-noite, oração/cântico e o terremoto que abre as portas"),
        ("C'", "16:28-34 — O carcereiro e sua casa creem e são batizados"),
        ("B'", "16:35-39 — Os magistrados ordenam a soltura; Paulo evoca a cidadania romana"),
        ("A'", "16:40 — Paulo e Silas voltam à casa de Lídia (Λυδίαν)"),
    ]
    for letter, text in murai:
        inner += f'<div class="flex gap-3"><span class="font-bold text-slate-900 w-8">{letter}</span><span>{text}</span></div>'
    inner += ('</div></div>')
    inner += ('<div class="rounded-lg border-2 border-amber-300 p-5 bg-white">'
              '<div class="font-bold text-slate-900 mb-3">Eixo político: cidadania e império (R. J. Cassidy, <span class="italic">Society and Politics in the Acts of the Apostles</span>)</div>'
              '<ul class="list-disc list-inside space-y-2 text-sm text-slate-700">')
    cassidy = [
        "Filipos era colônia romana; Paulo e Silas são cidadãos romanos (16:37), e o uso de <em>rhabdouchoi</em> (bastonadores) reflete a violência das autoridades coloniais.",
        "A exorcismo da jovem escrava (espírito de python) quebra uma fonte de lucro econômico e desafia o sistema que a subjuga — leitura lida também sob a ótica pós-colonial (a escrava vs. Lídia como duas mulheres à margem).",
        "O terremoto e a soltura invertem a lógica do poder romano: quem deveria estar subjugado torna-se agente de salvação para o próprio carcereiro.",
    ]
    for t in cassidy:
        inner += f'<li>{t}</li>'
    inner += '</ul></div>'
    inner += box_close("Fontes: H. Murai, Literary Structure of Acts (bible.literarystructure.info); R. J. Cassidy, Society and Politics in the Acts of the Apostles (1992).")
    return inner

def _acad_box(title_en, amber_blocks):
    """Render a 2nd (amber) academically-grounded design box.
    amber_blocks: list of (heading_pt, list_of_html_li_strings)."""
    inner = box_open("")
    inner += f'<h3 class="text-xl font-bold text-slate-900 mb-1">{title_en[0]}</h3>'
    inner += f'<p class="text-sm italic text-slate-500 mb-5">{title_en[1]}</p>'
    for heading, items in amber_blocks:
        inner += (f'<div class="rounded-lg border-2 border-amber-300 p-5 bg-white mb-4">'
                  f'<div class="font-bold text-slate-900 mb-3">{heading}</div>'
                  f'<ul class="list-disc list-inside space-y-2 text-sm text-slate-700">')
        for it in items:
            inner += f'<li>{it}</li>'
        inner += '</ul></div>'
    return inner

def design_journey1():
    inner = box_open("")
    inner += '<h3 class="text-xl font-bold text-slate-900 mb-1">A Primeira Viagem Missionária como quiasmo</h3>'
    inner += '<p class="text-sm italic text-slate-500 mb-5">The first mission as a literary arc (cf. Conzelmann; Murai)</p>'
    inner += ('<div class="grid md:grid-cols-2 gap-3 mb-4">'
              '<div class="rounded-lg border-2 border-indigo-300 p-4 bg-white"><div class="font-bold text-slate-900">A — Chipre (13:4-12)</div><div class="text-sm text-slate-600 mt-2">Bar-Jesus cego; o poder do Evangelho diante de uma autoridade.</div></div>'
              '<div class="rounded-lg border-2 border-indigo-300 p-4 bg-white"><div class="font-bold text-slate-900">B — Antioquia da Pisídia (13:13-52)</div><div class="text-sm text-slate-600 mt-2">Discurso-programa: a história de Israel coroa em Jesus.</div></div>'
              '<div class="rounded-lg border-2 border-indigo-300 p-4 bg-white"><div class="font-bold text-slate-900">B\' — Icônio (14:1-7)</div><div class="text-sm text-slate-600 mt-2">Judeus e gentios creem; divisão e perseguição.</div></div>'
              '<div class="rounded-lg border-2 border-indigo-300 p-4 bg-white"><div class="font-bold text-slate-900">A\' — Listra & Derbe (14:8-20)</div><div class="text-sm text-slate-600 mt-2">O coxo curado; a multidão quer sacrificar; Paulo apedrejado.</div></div>'
              '</div>')
    inner += box_close("Baseado no Guia de Atos do Bible Project (a primeira viagem missionária).")
    inner += _acad_box(
        ("A viagem na leitura acadêmica", "Scholarly literary readings — Murai (quiasmo) e Tannehill (retorno/êxodo)"),
        [("Quiasmo concêntrico de Atos 13–14 (esboço de H. Murai)", [
            "A — Chipre: Bar-Jesus, o falso profeta, é cegado (13:4-12)",
            "B — Antioquia da Pisídia: discurso de Paulo à sinagoga (13:13-52)",
            "C — Icônio: creem judeus e gregos; perseguição (14:1-7)",
            "D — Listra: o coxo é curado; Paulo tomado por Hermes (14:8-18)",
            "C' — Retorno a Icônio, Antioquia, Pisídia (14:21-23)",
            "B' — Atos 14:24-26 retorna à Antioquia da Síria",
            "A' — Chipre revisitada no caminho de volta (14:26-28)",
        ]),
        ("Eixo teológico: o retorno como novo Êxodo (R. C. Tannehill, <span class=\"italic\">The Narrative Unity of Luke-Acts</span>)", [
            "A viagem repete o padrão de Israel: saída, sinais, rebelião, e volta à comunidade — Paulo como profeta que anuncia o Reino.",
            "O discurso de Antioquia da Pisídia (13:16-41) reconfigura a história de Israel em torno de Jesus como seu clímax prometido.",
        ]),
        ])
    return inner

def design_trial():
    inner = box_open("")
    inner += '<h3 class="text-xl font-bold text-slate-900 mb-1">O padrão repetido dos tribunais</h3>'
    inner += '<p class="text-sm italic text-slate-500 mb-5">The repeated trial pattern (cf. Pervo; Cassidy)</p>'
    inner += ('<div class="rounded-lg border-2 border-slate-300 p-5 bg-slate-50">'
              '<div class="font-bold text-slate-900 mb-3">A estrutura dos julgamentos de Paulo (cadeia A-B-A′)</div>'
              '<div class="space-y-2">'
              '<div class="rounded-lg border-2 border-slate-400 p-3 bg-white flex gap-3 items-start"><span class="font-bold text-lg text-slate-900 w-8">A</span><span class="text-sm text-slate-700">Acusação judaica por agitação (Félix, Festo, Agripa)</span></div>'
              '<div class="rounded-lg border-2 border-slate-400 p-3 pl-8 bg-white flex gap-3 items-start"><span class="font-bold text-lg text-slate-900 w-8">B</span><span class="text-sm text-slate-700">Defesa de Paulo: adora ao Deus dos antepassados e crê na ressurreição (24–26)</span></div>'
              '<div class="rounded-lg border-2 border-slate-400 p-3 bg-white flex gap-3 items-start"><span class="font-bold text-lg text-slate-900 w-8">A′</span><span class="text-sm text-slate-700">Veredito: \"nada fez que mereça morte\" — mas o apelo a César o leva a Roma (26:31)</span></div>'
              '</div></div>')
    inner += box_close("Baseado no Guia de Atos do Bible Project (os julgamentos de Paulo).")
    inner += _acad_box(
        ("Os tribunais na leitura acadêmica", "Scholarly readings — Cassidy (império) e Pervo (retórica)"),
        [("Cidadania romana como recurso narrativo (R. J. Cassidy, <span class=\"italic\">Society and Politics in the Acts of the Apostles</span>)", [
            "Paulo evoca a cidadania (16:37; 22:25-29) não por orgulho, mas para forçar autoridades romanas a agirem com justiça — o império vira instrumento da missão.",
            "Em Festo (25:11) o \"apelo a César\" garante a chegada a Roma, cumprindo Atos 1:8: a testemunha chega aos \"confins da terra\" sob escolta imperial.",
        ]),
        ("A retórica dos discursos de defesa (R. I. Pervo, <span class=\"italic\">Acts: A Commentary</span>)", [
            "Os discursos perante Félix, Festo e Agripa seguem a convenção forense greco-romana: negar o crime, apelar à lei e à boa conduta.",
            "A repetição do padrão (acusação → defesa → veredito de inocência) subverte a autoridade romana: quem é julgado é declarado inocente por seus próprios juízes.",
        ]),
        ])
    return inner

def design_athens():
    inner = box_open("")
    inner += '<h3 class="text-xl font-bold text-slate-900 mb-1">Atenas: o discurso no Areópago</h3>'
    inner += '<p class="text-sm italic text-slate-500 mb-5">The Areopagus address as philosophical dialogue</p>'
    inner += ('<div class="rounded-lg border-2 border-slate-300 p-5 bg-slate-50">'
              '<div class="font-bold text-slate-900 mb-3">Movimento do discurso (A-B-A′)</div>'
              '<div class="space-y-2">'
              '<div class="rounded-lg border-2 border-slate-400 p-3 bg-white flex gap-3 items-start"><span class="font-bold text-lg text-slate-900 w-8">A</span><span class="text-sm text-slate-700">Ponto de contato: o altar \"ao Deus desconhecido\" (17:22-23)</span></div>'
              '<div class="rounded-lg border-2 border-slate-400 p-3 pl-8 bg-white flex gap-3 items-start"><span class="font-bold text-lg text-slate-900 w-8">B</span><span class="text-sm text-slate-700">O Deus criador e Senhor, que não habita em templos feitos por mãos (17:24-29)</span></div>'
              '<div class="rounded-lg border-2 border-slate-400 p-3 bg-white flex gap-3 items-start"><span class="font-bold text-lg text-slate-900 w-8">A′</span><span class="text-sm text-slate-700">O chamado ao arrependimento e o juízo por meio de um homem que Deus ressuscitou (17:30-31)</span></div>'
              '</div></div>')
    inner += box_close("Baseado no Guia de Atos do Bible Project (Paulo em Atenas).")
    inner += _acad_box(
        ("Atenas na leitura acadêmica", "Scholarly readings — Martin (Babel invertida) e Theissen (sabedoria crucificada)"),
        [("A inversão da Torre de Babel (T. W. Martin, <span class=\"italic\">By Philosophy and Empty Deceit</span>)", [
            "O pluralismo religioso de Atenas (altares a todos os deuses) espelha a confusão de línguas em Babel; o discurso de Paulo reúne a humanidade sob um só Deus.",
            "Citar Arato, Epímeno e Cleantes mostra que Paulo encontra \"sementes do Verbo\" na cultura grega, sem abandonar a tese central da ressurreição.",
        ]),
        ("Sabedoria crucificada vs. sabedoria grega (G. Theissen, <span class=\"italic\">A Social History of Early Christianity</span>)", [
            "A ressurreição dos mortos é \"loucura\" para a filosofia grega (1 Cor 1:23); o Areópago mostra o choque entre a sabedoria da cruz e a retórica ateniense.",
            "Alguns zombam, outros pedem ouvir de novo, e alguns creem (Dionísio, Dâmaris) — a recepção mista reflete a tensão cidade/Império.",
        ]),
        ])
    return inner

def design_corinth():
    inner = box_open("")
    inner += '<h3 class="text-xl font-bold text-slate-900 mb-1">Corinto: centro comercial e igreja</h3>'
    inner += '<p class="text-sm italic text-slate-500 mb-5">Corinth — a cosmopolitan hub of the empire</p>'
    inner += ('<div class="grid md:grid-cols-2 gap-3 mb-4">'
              '<div class="rounded-lg border-2 border-indigo-300 p-4 bg-white"><div class="font-bold text-slate-900">Visão de Paulo (18:9-10)</div><div class="text-sm text-slate-600 mt-2">\"Não temas... tenho muito povo nesta cidade\"; proteção divina.</div></div>'
              '<div class="rounded-lg border-2 border-indigo-300 p-4 bg-white"><div class="font-bold text-slate-900">Trabalho e missão (18:1-3)</div><div class="text-sm text-slate-600 mt-2">Paulo, Aquila e Priscila, tecelões de tendas — missão por ofício.</div></div>'
              '</div>')
    inner += box_close("Baseado no Guia de Atos do Bible Project (Paulo em Corinto).")
    inner += _acad_box(
        ("Corinto na leitura acadêmica", "Scholarly readings — Theissen (estrato social) e Meggitt (pobreza)"),
        [("Estratificação social da igreja (G. Theissen, <span class=\"italic\">The Social Setting of Pauline Christianity</span>)", [
            "Aquila e Priscila são artesãs judias expulsas por Cláudio (Suetônio) — a igreja de Corinto une marginalizados e alguns mais abastados.",
            "O trabalho manual de Paulo (tendas) é estratégia missionária e sinal de independência financeira diante da cidade cliente.",
        ]),
        ("Poder colonial e religião (R. J. Cassidy, <span class=\"italic\">Society and Politics</span>)", [
            "Gálio, procônsul da Acaia, recusa julgar a causa (18:12-17) — Roma tolera o conflito interno judaico, mas protege Paulo como cidadão.",
            "Corinto, colônia livre e porto, encarna a mistura de poder imperial e diversidade que a missão de Paulo enfrenta.",
        ]),
        ])
    return inner

def design_ephesus():
    inner = box_open("")
    inner += '<h3 class="text-xl font-bold text-slate-900 mb-1">Éfeso: o confronto com Artemis</h3>'
    inner += '<p class="text-sm italic text-slate-500 mb-5">Ephesus — the clash with the cult of Artemis</p>'
    inner += ('<div class="rounded-lg border-2 border-slate-300 p-5 bg-slate-50">'
              '<div class="font-bold text-slate-900 mb-3">A escalada em Éfeso (A-B-A′)</div>'
              '<div class="space-y-2">'
              '<div class="rounded-lg border-2 border-slate-400 p-3 bg-white flex gap-3 items-start"><span class="font-bold text-lg text-slate-900 w-8">A</span><span class="text-sm text-slate-700">O Evangelho se espalha; livros de magia queimados (19:8-20)</span></div>'
              '<div class="rounded-lg border-2 border-slate-400 p-3 pl-8 bg-white flex gap-3 items-start"><span class="font-bold text-lg text-slate-900 w-8">B</span><span class="text-sm text-slate-700">Tumulto: Demétrio e os prateiros defendem o templo de Artemis (19:23-27)</span></div>'
              '<div class="rounded-lg border-2 border-slate-400 p-3 bg-white flex gap-3 items-start"><span class="font-bold text-lg text-slate-900 w-8">A′</span><span class="text-sm text-slate-700">O escrivão acalma a multidão; Paulo parte para a Macedônia (19:35-41)</span></div>'
              '</div></div>')
    inner += box_close("Baseado no Guia de Atos do Bible Project (Paulo em Éfeso).")
    inner += _acad_box(
        ("Éfeso na leitura acadêmica", "Scholarly readings — Cadwallader (economia do templo) e Cassidy (império)"),
        [("O templo de Artemis como economia política (A. Cadwallader, <span class=\"italic\">The First Christian Sisterhood</span>)", [
            "Demétrio não defende teologia, mas lucro: a Grande Artemis era centro de turismo, banco e comércio de prata em Éfeso.",
            "A queima de livros de magia (19:19) e o tumulto mostram o choque entre a economia do templo e a comunidade de partilha de bens.",
        ]),
        ("Leitura anti-imperial (R. J. Cassidy)", [
            "O escrivão lembra que Paulo e seus companheiros não são sacrílegos nem blasfemos de Artemis — Roma preserva a ordem pública, mas o Evangelho já deslocou o centro de poder.",
            "Éfeso antecipa a tensão entre o culto imperial e o culto a Jesus que marca o resto de Atos.",
        ]),
        ])
    return inner

def design_return():
    inner = box_open("")
    inner += '<h3 class="text-xl font-bold text-slate-900 mb-1">O retorno a Jerusalém</h3>'
    inner += '<p class="text-sm italic text-slate-500 mb-5">The return — the unity of Jewish and Gentile believers</p>'
    inner += ('<div class="rounded-lg border-2 border-slate-300 p-5 bg-slate-50">'
              '<div class="font-bold text-slate-900 mb-3">O arco da viagem de volta (A-B-A′)</div>'
              '<div class="space-y-2">'
              '<div class="rounded-lg border-2 border-slate-400 p-3 bg-white flex gap-3 items-start"><span class="font-bold text-lg text-slate-900 w-8">A</span><span class="text-sm text-slate-700">Despedida em Mileto: Paulo prevê prisões e não verá mais a Ásia (20:17-38)</span></div>'
              '<div class="rounded-lg border-2 border-slate-400 p-3 pl-8 bg-white flex gap-3 items-start"><span class="font-bold text-lg text-slate-900 w-8">B</span><span class="text-sm text-slate-700">A profecia de Ágabo: Paulo será entregue aos gentios em Jerusalém (21:10-14)</span></div>'
              '<div class="rounded-lg border-2 border-slate-400 p-3 bg-white flex gap-3 items-start"><span class="font-bold text-lg text-slate-900 w-8">A′</span><span class="text-sm text-slate-700">A chegada e o arresto no templo — o ciclo de prisões se inicia (21:17-36)</span></div>'
              '</div></div>')
    inner += box_close("Baseado no Guia de Atos do Bible Project (o retorno a Jerusalém).")
    inner += _acad_box(
        ("O retorno na leitura acadêmica", "Scholarly readings — Tannehill (profecia cumprida) e Cassidy (império)"),
        [("A despedida de Mileto como discurso de testamento (R. C. Tannehill, <span class=\"italic\">Narrative Unity</span>)", [
            "O discurso de Mileto (20:18-35) espelha os discursos de despedida de Moisés e Paulo, antecipando o martírio e encarregando os presbíteros.",
            "A insistência em ir a Jerusalém \"amarrado no Espírito\" (20:22) mostra a submissão de Paulo ao plano de Deus acima do perigo.",
        ]),
        ("Prisão e império (R. J. Cassidy)", [
            "O arresto no templo pela multidão judaica e a intervenção da coorte romana (21:27-35) reiniciam a cadeia de tribunais que levará Paulo a Roma.",
            "O retorno selara a unidade entre judeus e gentios: o Evangelho não aboliu Israel, mas o incluiu no mesmo povo de Deus.",
        ]),
        ])
    return inner

DESIGNS = {
    "philippi": design_philippi,
    "journey1": design_journey1,
    "trial": design_trial,
    "athens": design_athens,
    "corinth": design_corinth,
    "ephesus": design_ephesus,
    "return": design_return,
    "geo_thesis": design_geo_thesis,
    "pentecost": design_pentecost,
    "two_temples": design_two_temples,
    "three_bridges": design_three_bridges,
    "council": design_council,
    "whole_book": design_whole_book,
}

SESSION_TPL = r"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Sessão @@N@@: @@TITLE@@</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    .verse-link { color: inherit; cursor: pointer; }
    body { font-family: 'DejaVu Sans','Helvetica Neue',Arial,sans-serif !important; }
    @media print { @page { size: A4; margin: 1.4cm } body{print-color-adjust:exact} .print\:hidden{display:none!important} }
  </style>
</head>
<body class="bg-white font-sans text-slate-800">
  <div class="p-4 print:hidden">
    <a href="index.html" class="text-slate-600 hover:underline">&larr; Voltar para o Índice</a>
  </div>
  <div class="min-h-screen p-8 md:px-16">
    <div id="sessao-@@N@@" class="max-w-4xl mx-auto">
      <h1 class="text-4xl font-bold text-slate-900 mb-8 border-b pb-4">Sessão @@N@@: @@TITLE@@</h1>

      <h2 class="text-2xl font-bold text-slate-800 mb-3">Pontos-Chave</h2>
      <ul class="list-disc list-inside space-y-2 mb-10 text-lg text-slate-700">
@@KEYS@@
      </ul>

@@PROSE@@

@@DESIGN@@

      <h2 class="text-2xl font-bold text-slate-800 mt-12 mb-4">Questão para Reflexão</h2>
      <div class="border-2 border-slate-300 rounded-xl p-6 bg-slate-50">
        <p class="text-lg text-slate-700">@@REFLEX@@</p>
      </div>
    </div>
  </div>
  <script src="../js/verse-modal.js"></script>
</body>
</html>
"""

def render_session(n, ch):
    c = CHAPTERS[ch]
    keys = "\n".join(f'        <li>{k}</li>' for k in c["k"])
    prose = c["p"].strip()
    design = DESIGNS[c["d"]]() if c["d"] else ""
    html = (SESSION_TPL
             .replace("@@N@@", n)
             .replace("@@TITLE@@", c["t"])
             .replace("@@KEYS@@", keys)
             .replace("@@PROSE@@", prose)
             .replace("@@DESIGN@@", design)
             .replace("@@REFLEX@@", c["r"]))
    return html

def main():
    written = 0
    for n in sorted(CHAPTERS.keys(), key=lambda x: int(x)):
        ch = n
        mod = module_of(ch)
        d = os.path.join(ROOT, f"modulo-{mod}")
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, f"sessao-{n}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(render_session(n, ch))
        written += 1
        print("wrote", path)
    print("TOTAL", written)

if __name__ == "__main__":
    main()
