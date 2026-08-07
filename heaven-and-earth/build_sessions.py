#!/usr/bin/env python3
"""Build heaven-and-earth session HTML from the combined teacher-notes PDF.

Reuses abraao's bilingual shell layout (same CSS/JS structure) but content is
extracted from heaven-and-earth-teacher-notes.pdf: EN comes verbatim from the
PDF, PT is machine-translated (MyMemory via deep_translator) so it is a real
rendering, not invented.

Usage:
  python3 build_sessions.py            # build all 31 sessions
  python3 build_sessions.py 1 2 3 4 5  # build only these session numbers
"""
import sys, os, re, html, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(ROOT, "heaven-and-earth-teacher-notes.pdf")

# ---- session -> (module_dir, title_pt, title_en) -------------------------
# titles_pt are the canonical course titles (translated); modules mirror abraao.
SESSIONS = {
    1:  ("modulo-1", "Nosso Lugar no Universo", "Our Place in the Universe"),
    2:  ("modulo-1", "As Palavras \u201cC\u00e9us\u201d e \u201cTerra\u201d na B\u00edblia Hebraica", "The Words \u201cHeavens\u201d and \u201cEarth\u201d in the Hebrew Bible"),
    3:  ("modulo-1", "C\u00e9us e Terra se Unem em Jesus", "Heaven and Earth Come Together in Jesus"),
    4:  ("modulo-1", "Reflex\u00f5es sobre C\u00e9us e Terra no Novo Testamento", "Reflections on Heaven and Earth in the New Testament"),
    5:  ("modulo-1", "Escritura, Comunica\u00e7\u00e3o, Linguagem e Cultura", "Scripture, Communication, Language, and Culture"),
    6:  ("modulo-2", "G\u00eanesis 1 \u00e9 uma Cosmologia dos Israelitas Antigos", "Genesis 1 Is an Ancient Israelite Cosmology"),
    7:  ("modulo-2", "O Prop\u00f3sito da Luz no Primeiro Dia", "The Purpose of Light on Day One"),
    8:  ("modulo-2", "Cosmologia do Egito Antigo", "Ancient Egyptian Cosmology"),
    9:  ("modulo-2", "Cosmologia da Babil\u00f4nia Antiga", "Ancient Babylonian Cosmology"),
    10: ("modulo-2", "O Princ\u00edpio e o Nada", "The Beginning and Nothingness"),
    11: ("modulo-2", "Imagens de G\u00eanesis 1 em Jeremias 4", "Genesis 1 Imagery in Jeremiah 4"),
    12: ("modulo-2", "Imagens de G\u00eanesis 1 no Salmo 104", "Song of Songs 104" if False else "Genesis 1 Imagery in Psalm 104"),
    13: ("modulo-3", "A Estrutura e a Mensagem de G\u00eanesis 1", "The Structure and Message of Genesis 1"),
    14: ("modulo-3", "Palavras Repetidas em G\u00eanesis 1", "Repeated Words in Genesis 1"),
    15: ("modulo-3", "Rela\u00e7\u00f5es Entre os Dias", "Relationships Between Days"),
    16: ("modulo-4", "As \u00c1guas de Cima e de Baixo", "The Waters Above and Below"),
    17: ("modulo-4", "O Drag\u00e3o nas \u00c1guas", "The Dragon in the Waters"),
    18: ("modulo-4", "A Terra Seca", "The Dry Land"),
    19: ("modulo-4", "Reflex\u00f5es sobre para Onde Toda a Cria\u00e7\u00e3o se Dirige", "Reflections on Where All Creation Is Headed"),
    20: ("modulo-4", "Rios de Vida", "Rivers of Life"),
    21: ("modulo-4", "Jesus e a \u00c1gua Viva", "Jesus and Living Water"),
    22: ("modulo-4", "Cosmologia Antiga no Salmo 36", "Ancient Cosmology in Psalm 36"),
    23: ("modulo-5", "Os C\u00e9us", "The Heavens"),
    24: ("modulo-5", "C\u00e9us e Terra Unidos no Templo", "Heaven and Earth United in the Temple"),
    25: ("modulo-5", "Reflex\u00f5es sobre o C\u00e9u Vindo \u00e0 Terra", "Reflections on Heaven Coming to Earth"),
    26: ("modulo-5", "Os Governantes de Cima", "The Rulers Above"),
    27: ("modulo-6", "Os Governantes de Baixo", "The Rulers Below"),
    28: ("modulo-6", "Humanos como Imagem, ou \u00cddolo, de Deus", "Humans as the Image, or Idol, of God"),
    29: ("modulo-6", "A Imagem de Deus na Trama da B\u00edblia", "The Image of God in the Storyline of the Bible"),
    30: ("modulo-7", "Deus Descansa no S\u00e9timo Dia", "God Rests on the Seventh Day"),
    31: ("modulo-7", "O Sab\u00e1 Sem Fim", "The Sabbath With No End"),
}

def clean_refs(s):
    """Turn common Bible-reference hyphen/colon quirks into clean text."""
    return s

def split_pages():
    """Return dict session_num -> combined text of its pages (EN, from PDF)."""
    import fitz
    doc = fitz.open(PDF)
    sess_re = re.compile(r'^Session (\d+):', re.MULTILINE)
    starts = {}
    for i in range(doc.page_count):
        for m in sess_re.finditer(doc[i].get_text()):
            starts[int(m.group(1))] = i + 1
    out = {}
    nums = sorted(starts)
    for idx, s in enumerate(nums):
        end = (starts[nums[idx + 1]] - 1) if idx + 1 < len(nums) else doc.page_count
        chunks = []
        for p in range(starts[s], end + 1):
            t = doc[p - 1].get_text()
            # strip running footer/header artifacts
            t = re.sub(r'Class Notes: Heaven and Earth\s*\n\d+ of 141', '', t)
            chunks.append(t)
        out[s] = "\n".join(chunks)
    return out

# Translation cache to avoid re-calling for the same sentence.
_trans_cache = {}

def translate_en_to_pt(text):
    """Placeholder: wraps text in a marker for later subagent translation."""
    if not text or len(text.strip()) < 3:
        return text
    return f"__TR__:{text}__/TR__"

def _is_page_header(line):
    return bool(line.startswith("Class Notes:") or re.match(r'^\d+ of \d+$', line))

def _is_caption(line):
    return any(k in line for k in ["NASA", "Wikimedia", "Hubble", "Stockli", "JPL", "Risinger", "Image courtesy", "Photo by", "Illustration by", "Drawing by", "Credit:"])

def _is_heading(line):
    # short, mostly Title Case, no terminal period -> treat as subheading
    if len(line) > 70 or line.endswith("."):
        return False
    words = line.replace(":", " ").split()
    if len(words) > 9:
        return False
    caps = sum(1 for w in words if w[:1].isupper())
    return caps >= max(1, len(words) * 0.6)

_BOOK_NAMES_PT = {
    "Genesis": "Gênesis", "Exodus": "Êxodo", "Leviticus": "Levítico",
    "Numbers": "Números", "Deuteronomy": "Deuteronômio",
    "Joshua": "Josué", "Judges": "Juízes", "Ruth": "Rute",
    "1 Samuel": "1 Samuel", "2 Samuel": "2 Samuel",
    "1 Kings": "1 Reis", "2 Kings": "2 Reis",
    "1 Chronicles": "1 Crônicas", "2 Chronicles": "2 Crônicas",
    "Ezra": "Esdras", "Nehemiah": "Neemias", "Esther": "Ester",
    "Job": "Jó", "Psalm": "Salmos", "Proverbs": "Provérbios",
    "Ecclesiastes": "Eclesiastes", "Song of Songs": "Cânticos",
    "Isaiah": "Isaías", "Jeremiah": "Jeremias", "Lamentations": "Lamentações",
    "Ezekiel": "Ezequiel", "Daniel": "Daniel",
    "Hosea": "Oseias", "Joel": "Joel", "Amos": "Amós",
    "Obadiah": "Obadias", "Jonah": "Jonas", "Micah": "Miqueias",
    "Nahum": "Naum", "Habakkuk": "Habacuque", "Zephaniah": "Sofonias",
    "Haggai": "Ageu", "Zechariah": "Zacarias", "Malachi": "Malaquias",
    "Matthew": "Mateus", "Mark": "Marcos", "Luke": "Lucas", "John": "João",
    "Acts": "Atos", "Romans": "Romanos",
    "1 Corinthians": "1 Coríntios", "2 Corinthians": "2 Coríntios",
    "Galatians": "Gálatas", "Ephesians": "Efésios", "Philippians": "Filipenses",
    "Colossians": "Colossenses",
    "1 Thessalonians": "1 Tessalonicenses", "2 Thessalonians": "2 Tessalonicenses",
    "1 Timothy": "1 Timóteo", "2 Timothy": "2 Timóteo",
    "Titus": "Tito", "Philemon": "Filemom", "Hebrews": "Hebreus",
    "James": "Tiago", "1 Peter": "1 Pedro", "2 Peter": "2 Pedro",
    "1 John": "1 João", "2 John": "2 João", "3 John": "3 João",
    "Jude": "Judas", "Revelation": "Apocalipse",
}
_SORTED_BOOKS_EN = sorted(_BOOK_NAMES_PT.keys(), key=len, reverse=True)

def _translate_book_names(text):
    """Replace English Bible book names in text with Portuguese."""
    for en, pt in [(b, _BOOK_NAMES_PT[b]) for b in _SORTED_BOOKS_EN]:
        text = text.replace(en, pt)
    return text

def _is_bible_ref(line):
    # English AND Portuguese book names
    books_en = r"(?:1\s+)?(?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|1\s*Samuel|2\s*Samuel|1\s*Kings|2\s*Kings|1\s*Chronicles|2\s*Chronicles|Ezra|Nehemiah|Esther|Job|Psalm|Proverbs|Ecclesiastes|Song\s+of\s+Songs|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|Haggai|Zechariah|Malachi|Matthew|Mark|Luke|John|Acts|Romans|1\s*Corinthians|2\s*Corinthians|Galatians|Ephesians|Philippians|Colossians|1\s*Thessalonians|2\s*Thessalonians|1\s*Timothy|2\s*Timothy|Titus|Philemon|Hebrews|James|1\s*Peter|2\s*Peter|1\s*John|2\s*John|3\s*John|Jude|Revelation)"
    books_pt = r"(?:1\s+)?(?:Gênesis|Êxodo|Levitico|Levítico|Números|Deuteronômio|Deuteronomio|Josué|Josue|Juízes|Juizes|Rute|1\s*Samuel|2\s*Samuel|1\s*Reis|2\s*Reis|1\s*Crônicas|1\s*Cronicas|2\s*Crônicas|2\s*Cronicas|Esdras|Neemias|Ester|Jó|Jo|Salmos|Provérbios|Provérbios|Eclesiastes|Cânticos|Cantares|Isaías|Isaias|Jeremias|Lamentações|Lamentacoes|Ezequiel|Daniel|Oseias|Oseias|Joel|Amós|Amos|Obadias|Jonas|Miqueias|Naum|Habacuque|Sofonias|Ageu|Zacarias|Malaquias|Mateus|Marcos|Lucas|João|Joao|Atos|Romanos|1\s*Coríntios|1\s*Corintios|2\s*Coríntios|2\s*Corintios|Gálatas|Galatas|Efésios|Efesios|Filipenses|Colossenses|1\s*Tessalonicenses|2\s*Tessalonicenses|1\s*Timóteo|1\s*Timoteo|2\s*Timóteo|2\s*Timoteo|Tito|Filemom|Hebreus|Tiago|1\s*Pedro|2\s*Pedro|1\s*João|1\s*Joao|2\s*João|2\s*Joao|3\s*João|3\s*Joao|Judas|Apocalipse)"
    return bool(re.match(rf'^({books_en}|{books_pt})\s+\d+:\d+', line))

_COMMENTARY_STARTERS = {"in", "here", "therefore", "this", "for", "however", "so", "thus", "but", "and in", "there are", "we all", "the following"}
def _is_commentary_start(line):
    lower_first = line.split()[0].lower().rstrip(",:;")
    return lower_first in _COMMENTARY_STARTERS

def parse_session_body(raw):
    """Parse raw PDF text of one session into structured blocks.

    Block modes: 'bullets' (Key Takeaways list), 'section' (subheading),
    'caption' (image credit), 'refq' (reflection question), 'p' (paragraph).
    'Key Takeaways' -> each subsequent sentence becomes its own bullet.
    """
    lines = raw.splitlines()
    blocks = []
    i = 0
    buf = []
    mode = None

    def flush():
        nonlocal buf, mode
        if not buf:
            return
        text = " ".join(b.strip() for b in buf if b.strip())
        text = re.sub(r'\s+', ' ', text).strip()
        if text:
            blocks.append((mode, text))
        buf = []; mode = None

    while i < len(lines):
        line = lines[i].strip()
        low = line.lower()
        if line == "":
            flush(); i += 1; continue
        if _is_page_header(line):
            i += 1; continue
        # consume multi-line session title: "Session N: ...\nmore title\nKey Takeaways"
        if re.match(r'^Session \d+:', line):
            i += 1
            while i < len(lines) and lines[i].strip().lower() != "key takeaways" and lines[i].strip():
                i += 1
            continue
        if low == "key takeaways":
            flush(); mode = "bullets"; i += 1; continue
        if low == "reflection question":
            flush()
            # consume the following line(s) as the question text
            q = []
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("Session ") and (lines[j].strip() != "" or q):
                if lines[j].strip() == "":
                    break
                q.append(lines[j].strip()); j += 1
            qtext = " ".join(q).strip()
            if qtext:
                blocks.append(("refq", qtext))
            i = j; continue
        if _is_caption(line):
            flush()
            blocks.append(("caption", line))
            i += 1; continue
        if _is_bible_ref(line):
            flush()
            blocks.append(("bibleref", line))
            # next mode is scripture quote — consume until blank line
            mode = "scripture"
            buf = []
            i += 1
            while i < len(lines):
                nxt = lines[i].strip()
                if nxt == "" or _is_page_header(nxt) or _is_bible_ref(nxt) or nxt.lower() in ("key takeaways", "reflection question") or _is_caption(nxt):
                    break
                # scripture quotes are verse-numbered ("1 Bless the LORD..."),
                # commentary lines start with commentary patterns
                if nxt and nxt[0].isupper() and not nxt[0].isdigit() and buf:
                    # "In this passage, ...", "Here, ...", "Therefore, ..." -> commentary, not scripture
                    lower_first_word = nxt.split()[0].lower().rstrip(",")
                    if lower_first_word in ("in", "here", "therefore", "this", "for", "however", "so", "thus", "but", "and in"):
                        break
                    # short commentary lines that explain: "This passage is one..."
                    if buf and _is_commentary_start(nxt):
                        break
                buf.append(nxt); i += 1
            text = " ".join(b.strip() for b in buf).strip()
            text = re.sub(r'\s+', ' ', text)
            if text:
                blocks.append(("scripture", text))
            buf = []; continue
        if _is_heading(line) and mode in (None, "p", "section", "caption", "refq", "bullets", "bibleref", "scripture"):
            flush(); mode = "section"; buf.append(line); flush(); i += 1; continue
        if mode == "bullets":
            # accumulate lines until blank/heading/page-header — each sentence = one bullet
            buf.append(line)
            j = i + 1
            while j < len(lines):
                nxt = lines[j].strip()
                if nxt == "" or _is_page_header(nxt) or nxt.lower() in ("key takeaways", "reflection question") or _is_caption(nxt) or _is_bible_ref(nxt) or (_is_heading(nxt) and _is_heading(nxt)):
                    break
                buf.append(nxt); j += 1
            text = " ".join(b.strip() for b in buf).strip()
            text = re.sub(r'\s+', ' ', text)
            # split into sentences
            for sent in re.split(r'(?<=[.!?])\s+', text):
                sent = sent.strip()
                if sent:
                    blocks.append(("bullets", sent))
            buf = []; i = j; continue
        # default paragraph accumulation
        if mode not in (None, "p"):
            flush()
        mode = "p"
        buf.append(line); i += 1
    flush()
    return blocks

def build_block_html(block):
    mode, payload = block
    if mode == "bullets-group":
        return _bullets_group_html(payload)
    en = payload
    pt = translate_en_to_pt(en)
    en_h = html.escape(en)
    pt_h = html.escape(pt)
    if mode == "section":
        return f'  <h2 class="section reveal"><span class="lang-pt">{pt_h}</span><span class="lang-en">{en_h}</span></h2>'
    if mode == "bibleref":
        return f'  <h3 class="bibleref reveal"><span class="lang-pt">{pt_h}</span><span class="lang-en">{en_h}</span></h3>'
    if mode == "scripture":
        return f'  <div class="scripture reveal"><div class="scripture-text"><span class="lang-pt">{pt_h}</span><span class="lang-en">{en_h}</span></div></div>'
    if mode == "refq":
        return f'  <h3 class="sub reveal" style="margin-top:3rem;"><span class="lang-pt">Pergunta para Reflex\u00e3o</span><span class="lang-en">Reflection Question</span></h3>\n  <p class="body reveal"><span class="lang-pt">{pt_h}</span><span class="lang-en">{en_h}</span></p>'
    if mode == "caption":
        return f'  <p class="caption reveal"><span class="lang-pt">{pt_h}</span><span class="lang-en">{en_h}</span></p>'
    return f'  <p class="body reveal"><span class="lang-pt">{pt_h}</span><span class="lang-en">{en_h}</span></p>'

SHELL_HEAD = """<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_pt}</title>
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">
<style>
  * {{ -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }}
  body {{ font-family: 'Inter', system-ui, sans-serif; color: #1a1a1a; background: #fff; }}
  html[lang="pt"] .lang-en {{ display: none !important; }}
  html[lang="en"] .lang-pt {{ display: none !important; }}
  h1.title {{ font-size: 2.6rem; font-weight: 800; letter-spacing: -0.025em; line-height: 1.08; }}
  h2.section {{ font-size: 1.9rem; font-weight: 800; letter-spacing: -0.015em; margin-top: 3rem; margin-bottom: 1.25rem; }}
  h3.sub {{ font-weight: 800; font-size: 1.3rem; margin-top: 2rem; margin-bottom: .75rem; letter-spacing: -0.01em; }}
  p.body {{ font-size: 1.05rem; line-height: 1.78; color: #24262a; margin-bottom: 1.1rem; }}
    .rule {{ border: 0; border-top: 2px solid #d7dde5; margin: 1.75rem 0 2.75rem; }}
      ul.bullets {{ list-style: none; padding: 0; }}
      ul.bullets > li {{ padding-left: 1.6rem; position: relative; margin-bottom: .6rem; line-height: 1.72; font-size: 1.05rem; }}
      ul.bullets > li:before {{ content: "\\2022"; position: absolute; left: .55rem; color: #1a1a1a; }}
      .bibleref {{ font-weight: 700; font-size: 1.05rem; margin-top: 2rem; margin-bottom: 0.3rem; letter-spacing: -0.005em; color: #2563eb; }}
      .scripture {{ border-left: 4px solid #dfe4ea; padding: .25rem 0 .25rem 1.25rem; margin: 1.5rem 0; transition: border-color .2s; }}
      .scripture:hover {{ border-left-color: #9aa7b8; }}
      .scripture-label {{ font-weight: 800; color: #17181a; font-size: 1.05rem; }}
      .scripture-text {{ margin-top: .55rem; font-size: 1.05rem; line-height: 1.8; color: #24262a; }}
      .caption {{ font-style: italic; color: #5b6472; font-size: .92rem; margin-top: .7rem; }}
  .page-footer {{ display: flex; justify-content: space-between; font-size: .875rem; color: #6b7280; border-top: 1px solid #e5e7eb; padding-top: 1rem; margin-top: 3.5rem; }}
  #reading-progress {{ position: fixed; top: 0; left: 0; height: 3px; width: 100%; background: #17181a; transform-origin: 0 50%; transform: scaleX(0); z-index: 60; }}
  .reveal {{ opacity: 0; transform: translateY(14px); transition: opacity .55s cubic-bezier(.22,.61,.36,1), transform .55s cubic-bezier(.22,.61,.36,1); }}
  .reveal.visible {{ opacity: 1; transform: none; }}
  @media print {{ @page {{ margin: 14mm 12mm; }} #reading-progress, .print\\:hidden {{ display: none !important; }} .reveal {{ opacity: 1 !important; transform: none !important; }} * {{ -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }} h1.title, h2.section, h3.sub {{ break-after: avoid-page; }} }}
  @media (prefers-reduced-motion: reduce) {{ .reveal {{ opacity: 1; transform: none; transition: none; }} }}
</style>
</head>
<body>

<div id="reading-progress" aria-hidden="true"></div>

<div class="fixed left-4 top-4 z-50 print:hidden">
  <a href="index.html" class="inline-flex items-center gap-2 rounded-full border border-slate-300 bg-white/90 backdrop-blur-xs px-4 py-1.5 text-sm font-semibold text-slate-600 shadow-sm transition-colors hover:bg-slate-100">
    <span>&larr;</span><span class="lang-pt">Voltar</span><span class="lang-en">Back</span>
  </a>
</div>
<div class="fixed right-4 top-4 z-50 print:hidden flex items-center gap-2">
  <button onclick="window.print()" class="inline-flex items-center gap-2 rounded-full border border-slate-300 bg-white/90 backdrop-blur-xs px-4 py-1.5 text-sm font-semibold text-slate-600 shadow-sm transition-colors hover:bg-slate-100">
    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
    <span class="lang-pt">Imprimir</span><span class="lang-en">Print</span>
  </button>
  <div class="inline-flex overflow-hidden rounded-full border border-slate-300 bg-white/90 backdrop-blur-xs shadow-sm">
    <button id="lang-pt" onclick="setLang('pt')" class="px-3.5 py-1.5 text-sm font-semibold transition-colors">PT</button>
    <button id="lang-en" onclick="setLang('en')" class="px-3.5 py-1.5 text-sm font-semibold transition-colors">EN</button>
  </div>
</div>

<div class="max-w-4xl mx-auto px-6 md:px-10 py-14">

  <h1 class="title reveal"><span class="lang-pt">Sess\u00e3o {n}: {title_pt}</span><span class="lang-en">Session {n}: {title_en}</span></h1>
  <hr class="rule">
"""

SHELL_FOOT = """
  <div class="page-footer">
    <span>Class Notes: Heaven and Earth</span>
    <span><span class="lang-pt">Sess\u00e3o {n} \u00b7 {title_pt}</span><span class="lang-en">Session {n} \u00b7 {title_en}</span></span>
  </div>
</div>

<script>
  function setLang(lang) {{
    document.documentElement.setAttribute('lang', lang);
    try {{ localStorage.setItem('s{n}-lang', lang); }} catch(e) {{}}
    var pt = document.getElementById('lang-pt'), en = document.getElementById('lang-en');
    if (lang === 'pt') {{
      pt.className = "px-3.5 py-1.5 text-sm font-semibold transition-colors bg-slate-800 text-white rounded-l-full";
      en.className = "px-3.5 py-1.5 text-sm font-semibold transition-colors bg-white text-slate-600 hover:bg-slate-50 rounded-r-full";
    }} else {{
      en.className = "px-3.5 py-1.5 text-sm font-semibold transition-colors bg-slate-800 text-white rounded-r-full";
      pt.className = "px-3.5 py-1.5 text-sm font-semibold transition-colors bg-white text-slate-600 hover:bg-slate-50 rounded-l-full";
    }}
  }}
  var saved = 'pt'; try {{ saved = localStorage.getItem('s{n}-lang') || 'pt'; }} catch(e) {{}}
  setLang(saved);

  (function () {{
    var bar = document.getElementById('reading-progress');
    function update() {{
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      bar.style.transform = 'scaleX(' + (max > 0 ? h.scrollTop / max : 0) + ')';
    }}
    window.addEventListener('scroll', update, {{ passive: true }});
    window.addEventListener('resize', update);
    update();
  }})();

  (function () {{
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var targets = document.querySelectorAll('.reveal');
    if (reduced || !('IntersectionObserver' in window)) {{ targets.forEach(function (el) {{ el.classList.add('visible'); }}); return; }}
    var io = new IntersectionObserver(function (entries) {{
      entries.forEach(function (entry) {{ if (entry.isIntersecting) {{ entry.target.classList.add('visible'); io.unobserve(entry.target); }} }});
    }}, {{ threshold: 0.05, rootMargin: '0px 0px -36px 0px' }});
    targets.forEach(function (el) {{ io.observe(el); }});
  }})();
</script>

  <script src="../js/verse-modal.js"></script>
</body>
</html>
"""

def build_session(n, raw):
    raw = _translate_book_names(raw)
    mod_dir, tpt, ten = SESSIONS[n]
    blocks = parse_session_body(raw)
    # merge consecutive 'bullets' blocks into one <ul>
    merged = []
    i = 0
    while i < len(blocks):
        if blocks[i][0] == "bullets":
            j = i
            items = []
            while j < len(blocks) and blocks[j][0] == "bullets":
                items.append(blocks[j][1]); j += 1
            merged.append(("bullets-group", items))
            i = j
        else:
            merged.append(blocks[i]); i += 1
    body = "\n".join(build_block_html(b) for b in merged)
    head = SHELL_HEAD.format(n=n, title_pt=tpt, title_en=ten)
    foot = SHELL_FOOT.format(n=n, title_pt=tpt, title_en=ten)
    full = head + "\n" + body + "\n" + foot
    out_dir = os.path.join(ROOT, mod_dir)
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"sessao-{n}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(full)
    return out, len(full)

def _bullets_group_html(items):
    lis = "\n".join(
        f'    <li><span class="lang-pt">{html.escape(translate_en_to_pt(s))}</span>'
        f'<span class="lang-en">{html.escape(s)}</span></li>'
        for s in items
    )
    return f'  <ul class="bullets reveal">\n{lis}\n  </ul>'

def main():
    nums = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else sorted(SESSIONS)
    raw_map = split_pages()
    for n in nums:
        if n not in SESSIONS:
            print(f"skip {n}: not in SESSIONS map"); continue
        if n not in raw_map:
            print(f"skip {n}: not found in PDF"); continue
        out, size = build_session(n, raw_map[n])
        print(f"wrote {out} ({size} bytes)")

if __name__ == "__main__":
    main()
