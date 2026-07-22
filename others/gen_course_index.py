#!/usr/bin/env python3
"""Generate bilingual (PT/EN) index.html for each of the 12 courses,
mirroring abraao/index.html layout, using local PDF-derived module data."""
import json, os, html

ROOT = "/Users/macbook/Documents/GitHub/abraao-estudo"

def load(*names):
    d = {}
    for n in names:
        d.update(json.load(open(os.path.join(ROOT, "others", n), encoding="utf-8")))
    return d

META = load("courses_meta_1.json", "courses_meta_2.json", "courses_meta_3.json")
MODS = json.load(open(os.path.join(ROOT, "others", "modules_en.json"), encoding="utf-8"))
PT   = load("module_titles_pt_1.json", "module_titles_pt_2.json")

def esc(s): return html.escape(s or "", quote=True)

TPL = '''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title data-i18n="title">Anotações de Aula: {title_pt}</title>
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
  <div class="min-h-screen">
    <div class="flex min-h-screen flex-col items-center justify-center md:p-12">
      <main class="flex flex-1 flex-col items-center justify-center text-center">
        <div class="flex min-h-screen flex-col p-8 md:p-12">
          <main class="flex flex-1 flex-col items-center justify-center text-center">
            <img src="{cover}" alt="{title_pt}" class="mb-8 h-48 w-48 rounded-2xl object-cover shadow-lg" />
            <p class="mb-2 font-semibold text-slate-500" data-i18n="kicker">Anotações de Aula</p>
            <h1 class="text-6xl font-bold text-slate-900" data-i18n="h1">{title_pt}</h1>
            <h2 class="mt-4 text-2xl text-slate-600" data-i18n="scripture">{scripture_pt}</h2>
            <h3 class="mt-2 text-xl text-slate-500">{teacher}</h3>
            <p class="mt-3 text-base text-slate-400 font-medium">The Bible Project</p>
            <p class="mt-8 max-w-2xl text-lg text-slate-700" data-i18n="desc">{desc_pt}</p>
            <div class="mt-6 p-4 bg-slate-50 rounded-lg border-l-4 border-slate-300">
              <p class="text-xs text-slate-500" data-i18n="source">{source_pt}</p>
            </div>
          </main>
        </div>
        <div id="modgrid" class="grid gap-6 md:grid-cols-2 lg:grid-cols-3 mb-10"></div>
      </main>
    </div>
  </div>
  <script>
    const MODULES = {modules_json};
    const I18N = {i18n_json};
    function render(lang){{
      const g=document.getElementById('modgrid');
      g.innerHTML=MODULES.map(m=>`
        <a href="modulo-${{m.pos}}/index.html"
          class="group block rounded-xl border-2 border-slate-200 bg-white p-8 transition-all hover:-translate-y-1 hover:border-sky-500 hover:shadow-xl">
          <div class="mb-4 flex justify-center">
            <img src="image/img-${{m.pos}}.jpeg" alt="${{lang==='pt'?m.title_pt:m.title_en}}" loading="lazy" class="h-32 w-32 rounded-xl object-cover shadow-md" />
          </div>
          <h3 class="mb-2 text-2xl font-bold text-slate-900 group-hover:text-sky-600">${{I18N[lang].module}} ${{m.pos}}</h3>
          <p class="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-500">${{I18N[lang].sessions}} ${{m.first}}-${{m.last}}</p>
          <p class="text-slate-600">${{lang==='pt'?m.title_pt:m.title_en}}</p>
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

SRC_PT = ('<strong>Fonte:</strong> Material baseado nas anotações de aula do curso "{en}" do The Bible Project, '
          'ministrado por {teacher}. Conteúdo original disponível em '
          '<a href="https://bibleproject.com" class="text-sky-600 hover:underline" target="_blank">bibleproject.com</a>')
SRC_EN = ('<strong>Source:</strong> Material based on the class notes from the "{en}" course by The Bible Project, '
          'taught by {teacher}. Original content available at '
          '<a href="https://bibleproject.com" class="text-sky-600 hover:underline" target="_blank">bibleproject.com</a>')

for slug, meta in META.items():
    mods_en = MODS[slug]
    mods_pt = PT[slug]
    teacher = meta.get("teacher", "Dr. Tim Mackie")
    modules = []
    for i, m in enumerate(mods_en):
        modules.append({
            "pos": m["pos"], "first": m["first"], "last": m["last"],
            "title_en": m["title"],
            "title_pt": mods_pt[i] if i < len(mods_pt) else m["title"],
        })
    i18n = {
        "pt": {
            "title": f'Anotações de Aula: {meta["title_pt"]}',
            "kicker": "Anotações de Aula", "h1": meta["title_pt"],
            "scripture": meta["scripture_pt"], "desc": meta["desc_pt"],
            "source": SRC_PT.format(en=meta["title_en"], teacher=teacher),
            "module": "Módulo", "sessions": "Sessões", "back": "Voltar",
        },
        "en": {
            "title": f'Class Notes: {meta["title_en"]}',
            "kicker": "Class Notes", "h1": meta["title_en"],
            "scripture": meta["scripture"], "desc": meta["desc_en"],
            "source": SRC_EN.format(en=meta["title_en"], teacher=teacher),
            "module": "Module", "sessions": "Sessions", "back": "Back",
        },
    }
    out = TPL.format(
        title_pt=esc(meta["title_pt"]), cover="../"+meta["cover"],
        scripture_pt=esc(meta["scripture_pt"]), teacher=esc(teacher),
        desc_pt=esc(meta["desc_pt"]), source_pt=i18n["pt"]["source"],
        modules_json=json.dumps(modules, ensure_ascii=False),
        i18n_json=json.dumps(i18n, ensure_ascii=False),
    )
    path = os.path.join(ROOT, slug, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"WROTE {slug}/index.html ({len(modules)} modules)")
print("DONE")
