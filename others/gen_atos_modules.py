#!/usr/bin/env python3
"""Generate the 5 module index.html files for the Atos dos Apostolos course.
Safe string templating via @@TOKEN@@ replace (no str.format -> no JS-brace issues).
Convention mirrors ephesians/modulo-2/index.html + abraao/index.html:
bilingual PT/EN toggle (PT default, localStorage bp_lang), Back top-left,
module cover = ../image/img-N.jpeg. NOT in root catalog (no official PDF).
"""
import os, json

ROOT = os.path.join(os.path.dirname(__file__), "..", "atos-dos-apostolos")

MODULES = [
    {"pos": 1, "first": 1, "last": 1,
     "t_pt": "A Comissão de Jesus e a Ascensão",
     "t_en": "Jesus Commissions His Disciples and Ascends",
     "sessions": [(1, "Atos 1: A Comissão e a Ascensão", "Acts 1: The Commission and the Ascension")]},
    {"pos": 2, "first": 2, "last": 7,
     "t_pt": "Pentecoste em Jerusalém e o Nascimento da Igreja",
     "t_en": "Pentecost in Jerusalem and the Birth of the Church",
     "sessions": [
         (2, "Atos 2: O Espírito e a Pentecoste", "Acts 2: The Spirit and Pentecost"),
         (3, "Atos 3: Pedro, João e o Homem Coxo", "Acts 3: Peter, John, and the Lame Man"),
         (4, "Atos 4: O Arresto e a Oração da Comunidade", "Acts 4: The Arrest and the Community's Prayer"),
         (5, "Atos 5: Ananias, Safira e o Crescimento", "Acts 5: Ananias, Sapphira, and the Growth"),
         (6, "Atos 6: Estêvão e os Sete", "Acts 6: Stephen and the Seven"),
         (7, "Atos 7: O Discurso de Estêvão", "Acts 7: Stephen's Speech")]},
    {"pos": 3, "first": 8, "last": 12,
     "t_pt": "A Comunidade de Jesus Torna-se um Movimento Internacional",
     "t_en": "The Jesus Community Becomes an International Movement",
     "sessions": [
         (8, "Atos 8: Filipe e a Samaria", "Acts 8: Philip and Samaria"),
         (9, "Atos 9: A Conversão de Saulo", "Acts 9: The Conversion of Saul"),
         (10, "Atos 10: Pedro e Cornélio", "Acts 10: Peter and Cornelius"),
         (11, "Atos 11: A Igreja em Antioquia", "Acts 11: The Church in Antioch"),
         (12, "Atos 12: Herodes e Pedro", "Acts 12: Herod and Peter")]},
    {"pos": 4, "first": 13, "last": 20,
     "t_pt": "Missão a Israel e Conflitos com a Cultura Romana",
     "t_en": "Mission to Israel and Clashes with Roman Culture",
     "sessions": [
         (13, "Atos 13: A Primeira Viagem Missionária", "Acts 13: The First Missionary Journey"),
         (14, "Atos 14: Icônio, Listra e Derbe", "Acts 14: Iconium, Lystra, and Derbe"),
         (15, "Atos 15: O Concílio de Jerusalém", "Acts 15: The Jerusalem Council"),
         (16, "Atos 16: Filipos e a Europa", "Acts 16: Philippi and Europe"),
         (17, "Atos 17: Tessalônica, Bereia e Atenas", "Acts 17: Thessalonica, Berea, and Athens"),
         (18, "Atos 18: Corinto", "Acts 18: Corinth"),
         (19, "Atos 19: Éfeso", "Acts 19: Ephesus"),
         (20, "Atos 20: O Retorno a Jerusalém", "Acts 20: The Return to Jerusalem")]},
    {"pos": 5, "first": 21, "last": 28,
     "t_pt": "Preso em Jerusalém e Imprisionado em Roma",
     "t_en": "Arrested in Jerusalem and Imprisoned in Rome",
     "sessions": [
         (21, "Atos 21: A Chegada a Jerusalém", "Acts 21: The Arrival in Jerusalem"),
         (22, "Atos 22: A Defesa de Paulo", "Acts 22: Paul's Defense"),
         (23, "Atos 23: Perante o Sinédrio", "Acts 23: Before the Sanhedrin"),
         (24, "Atos 24: Perante Félix", "Acts 24: Before Felix"),
         (25, "Atos 25: Perante Festo", "Acts 25: Before Festus"),
         (26, "Atos 26: Perante Agripa", "Acts 26: Before Agrippa"),
         (27, "Atos 27: A Viagem a Roma", "Acts 27: The Voyage to Rome"),
         (28, "Atos 28: Roma e a Casa Prisão", "Acts 28: Rome and House Arrest")]},
]

TPL = r"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title data-i18n="title">@@TITLE_PT@@</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white font-sans text-slate-800">
  <div class="fixed left-4 top-4 z-50">
    <a href="../index.html"
      class="inline-flex items-center gap-2 rounded-full border border-slate-300 bg-white px-4 py-1.5 text-sm font-semibold text-slate-600 shadow-sm transition-colors hover:bg-slate-100">
      <span>&larr;</span><span data-i18n="back">Voltar</span>
    </a>
  </div>
  <div class="fixed right-4 top-4 z-50">
    <div class="inline-flex overflow-hidden rounded-full border border-slate-300 bg-white shadow-sm">
      <button id="lang-pt" onclick="setLang('pt')" class="px-4 py-1.5 text-sm font-semibold transition-colors">PT</button>
      <button id="lang-en" onclick="setLang('en')" class="px-4 py-1.5 text-sm font-semibold transition-colors">EN</button>
    </div>
  </div>
  <div class="min-h-screen p-8">
    <div class="flex min-h-screen flex-col p-8 md:p-12">
      <main class="flex flex-1 flex-col items-center justify-center text-center">
        <img src="../image/img-@@POS@@.jpeg" alt="@@T_PT@@" class="mb-8 h-48 w-48 rounded-2xl object-cover shadow-lg" />
        <h1 class="text-5xl font-bold text-slate-900" data-i18n="h1">Módulo @@POS@@: @@T_PT@@</h1>
        <h2 class="mt-4 text-lg font-semibold uppercase tracking-wider text-slate-500" data-i18n="sessions">Sessões @@FIRST@@-@@LAST@@</h2>
        <div class="mt-12 w-full max-w-3xl">
          <h2 class="mb-6 text-2xl font-bold text-slate-900" data-i18n="toc">Índice de Sessões</h2>
          <div id="sessgrid" class="grid gap-4 md:grid-cols-2"></div>
        </div>
      </main>
    </div>
  </div>
  <script>
    const SESSIONS = @@SESSIONS@@;
    const I18N = {
      "pt": {"title": "Módulo @@POS@@: @@T_PT@@", "h1": "Módulo @@POS@@: @@T_PT@@", "sessions": "Sessões @@FIRST@@-@@LAST@@", "toc": "Índice de Sessões", "back": "Voltar", "session": "Sessão"},
      "en": {"title": "Module @@POS@@: @@T_EN@@", "h1": "Module @@POS@@: @@T_EN@@", "sessions": "Sessions @@FIRST@@-@@LAST@@", "toc": "Table of Sessions", "back": "Back", "session": "Session"}
    };
    function render(lang){
      document.getElementById('sessgrid').innerHTML = SESSIONS.map(s=>`
        <a href="sessao-${s.n}.html"
          class="group block rounded-lg border-2 border-slate-200 p-6 transition-all hover:border-sky-500 hover:shadow-lg">
          <h3 class="text-xl font-bold text-slate-900 group-hover:text-sky-600">${I18N[lang].session} ${s.n}</h3>
          <p class="mt-2 text-slate-600">${lang==='pt'?s.title_pt:s.title_en}</p>
        </a>`).join('');
    }
    function setLang(lang){
      localStorage.setItem('bp_lang',lang);
      document.documentElement.lang=lang==='pt'?'pt-BR':'en';
      const t=I18N[lang];
      document.querySelectorAll('[data-i18n]').forEach(el=>{const k=el.getAttribute('data-i18n');if(t[k]!==undefined)el.innerHTML=t[k];});
      document.title=t.title;
      const on='bg-sky-600 text-white',off='bg-white text-slate-600 hover:bg-slate-100';
      document.getElementById('lang-pt').className='px-4 py-1.5 text-sm font-semibold transition-colors '+(lang==='pt'?on:off);
      document.getElementById('lang-en').className='px-4 py-1.5 text-sm font-semibold transition-colors '+(lang==='en'?on:off);
      render(lang);
    }
    setLang(localStorage.getItem('bp_lang')||'pt');
  </script>
</body>
</html>
"""

for m in MODULES:
    sess = [{"n": n, "title_pt": pt, "title_en": en} for (n, pt, en) in m["sessions"]]
    html = (TPL
            .replace("@@POS@@", str(m["pos"]))
            .replace("@@FIRST@@", str(m["first"]))
            .replace("@@LAST@@", str(m["last"]))
            .replace("@@T_PT@@", m["t_pt"])
            .replace("@@T_EN@@", m["t_en"])
            .replace("@@TITLE_PT@@", f"Módulo {m['pos']}: {m['t_pt']}")
            .replace("@@SESSIONS@@", json.dumps(sess, ensure_ascii=False)))
    d = os.path.join(ROOT, f"modulo-{m['pos']}")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", os.path.join(d, "index.html"))
print("DONE")
