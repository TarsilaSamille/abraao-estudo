#!/usr/bin/env python3
"""Generate bilingual modulo-N/index.html for each of the 12 courses,
mirroring abraao/modulo-3/index.html layout, using local PDF-derived session data."""
import json, os, html

ROOT = "/Users/macbook/Documents/GitHub/abraao-estudo"

# module titles PT/EN
MODPT = json.load(open(os.path.join(ROOT, "others", "module_titles_pt_1.json"), encoding="utf-8"))
MODPT.update(json.load(open(os.path.join(ROOT, "others", "module_titles_pt_2.json"), encoding="utf-8")))
MODEN = json.load(open(os.path.join(ROOT, "others", "modules_en.json"), encoding="utf-8"))
# session title PT (from 5 files) + EN (from session_titles)
SESSPT = {}
for fn in ["sess_pt_1.json","sess_pt_2.json","sess_pt_3.json","sess_pt_4.json","sess_pt_5.json"]:
    SESSPT.update(json.load(open(os.path.join(ROOT, "others", fn), encoding="utf-8")))
SESSTT = json.load(open("/tmp/session_titles.json", encoding="utf-8"))

COURSES = list(MODEN.keys())  # the 12

TPL = '''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title data-i18n="title">Módulo {pos}: {title_pt}</title>
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
        <img src="../image/img-{pos}.jpeg" alt="{title_pt}" class="mb-8 h-48 w-48 rounded-2xl object-cover shadow-lg" />
        <h1 class="text-5xl font-bold text-slate-900" data-i18n="h1">Módulo {pos}: {title_pt}</h1>
        <h2 class="mt-4 text-lg font-semibold uppercase tracking-wider text-slate-500" data-i18n="sessions">Sessões {first}-{last}</h2>
        <div class="mt-12 w-full max-w-3xl">
          <h2 class="mb-6 text-2xl font-bold text-slate-900" data-i18n="toc">Índice de Sessões</h2>
          <div id="sessgrid" class="grid gap-4 md:grid-cols-2"></div>
        </div>
      </main>
    </div>
  </div>
  <script>
    const SESSIONS = {sessions_json};
    const I18N = {i18n_json};
    function render(lang){{
      document.getElementById('sessgrid').innerHTML = SESSIONS.map(s=>`
        <a href="sessao-${{s.n}}.html"
          class="group block rounded-lg border-2 border-slate-200 p-6 transition-all hover:border-sky-500 hover:shadow-lg">
          <h3 class="text-xl font-bold text-slate-900 group-hover:text-sky-600">${{I18N[lang].session}} ${{s.n}}</h3>
          <p class="mt-2 text-slate-600">${{lang==='pt'?s.title_pt:s.title_en}}</p>
        </a>`).join('');
    }}
    function setLang(lang){{
      localStorage.setItem('bp_lang',lang);
      document.documentElement.lang=lang==='pt'?'pt-BR':'en';
      const t=I18N[lang];
      document.querySelectorAll('[data-i18n]').forEach(el=>{{const k=el.getAttribute('data-i18n');if(t[k]!==undefined)el.innerHTML=t[k];}});
      document.title=t.title;
      const on='bg-sky-600 text-white',off='bg-white text-slate-600 hover:bg-slate-100';
      document.getElementById('lang-pt').className='px-4 py-1.5 text-sm font-semibold transition-colors '+(lang==='pt'?on:off);
      document.getElementById('lang-en').className='px-4 py-1.5 text-sm font-semibold transition-colors '+(lang==='en'?on:off);
      render(lang);
    }}
    setLang(localStorage.getItem('bp_lang')||'pt');
  </script>
</body>
</html>
'''

total = 0
for slug in COURSES:
    mods_en = MODEN[slug]
    mods_pt = MODPT[slug]
    sess_en = SESSTT[slug]["sessions"]
    sess_pt = SESSPT[slug]
    for i, m in enumerate(mods_en):
        pos = m["pos"]; first = m["first"]; last = m["last"]
        titles = []
        for s in range(first, last + 1):
            en = sess_en.get(str(s), sess_en.get(s, ""))
            pt = sess_pt.get(str(s), en)  # fallback to EN if no PT
            titles.append({"n": s, "title_pt": pt, "title_en": en})
        # module title
        mpt = mods_pt[i] if i < len(mods_pt) else m["title"]
        men = m["title"]
        i18n = {
            "pt": {"title": f"Módulo {pos}: {mpt}", "h1": f"Módulo {pos}: {mpt}",
                   "sessions": f"Sessões {first}-{last}", "toc": "Índice de Sessões",
                   "back": "Voltar", "session": "Sessão"},
            "en": {"title": f"Module {pos}: {men}", "h1": f"Module {pos}: {men}",
                   "sessions": f"Sessions {first}-{last}", "toc": "Table of Sessions",
                   "back": "Back", "session": "Session"},
        }
        out = TPL.format(
            pos=pos, first=first, last=last,
            title_pt=html.escape(mpt), title_en=html.escape(men),
            sessions_json=json.dumps(titles, ensure_ascii=False),
            i18n_json=json.dumps(i18n, ensure_ascii=False),
        )
        d = os.path.join(ROOT, slug, f"modulo-{pos}")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(out)
        total += 1
        print(f"{slug}/modulo-{pos}/index.html ({last-first+1} sessões)")
print(f"DONE: {total} modulo indexes")
