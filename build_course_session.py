#!/usr/bin/env python3
"""Assembler genérico para cursos no padrão Tailwind+bp_lang (ephesians, 1-corinthians).
Clona o shell canonico (modulo-1/sessao-1.html) e troca titulo/h1/corpo por sessao.

Uso: python3 build_course_session.py <shell.html> <out_dir> <sessoes.json>
JSON: {"sessions":[{"n","title_pt","title_en","body_html"},...]}
Mapeamento PDF->HTML: HTML session N <- pdf-sessoes/sessao-(N+1).pdf (off-by-one, igual jonah).
"""
import json, re, sys, os

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def build(shell_path, out_dir, sessions):
    shell = open(shell_path).read()
    # HEAD = do inicio ate a abertura da tag <main ...> (inclui nav/style verbatim)
    mi = shell.index("<main")
    main_open = shell[mi:shell.index(">", mi)+1]
    shell_head = shell[:mi] + main_open + "\n"
    for s in sessions:
        n = s["n"]; tp = s["title_pt"]; te = s["title_en"]; body = s["body"]
        head = re.sub(r'<title[^>]*>.*?</title>',
                      f'<title data-i18n="title">{esc(f"Sessão {n}: {tp}")}</title>',
                      shell_head, count=1)
        h1 = (f'    <h1 class="text-4xl font-bold text-slate-900 md:text-5xl" data-i18n="h1">'
              f'<span class="lang-pt">{esc(f"Sessão {n}: {tp}")}</span>'
              f'<span class="lang-en">{esc(f"Session {n}: {te}")}</span></h1>\n')
        section = f'    <hr class="my-8 border-t-2 border-slate-200" />\n    <section class="space-y-6" data-i18n="body">\n{body}\n    </section>\n  </main>\n'
        script = (
            '  <script src="../js/verse-modal.js"></script>\n'
            '  <script>\n'
            '    const I18N = {"pt": {"title": "' + esc(f"Sessão {n}: {tp}") + '", "h1": "' + esc(f"Sessão {n}: {tp}") + '", "back": "Voltar"}, '
            '"en": {"title": "' + esc(f"Session {n}: {te}") + '", "h1": "' + esc(f"Session {n}: {te}") + '", "back": "Back"}};\n'
            '    function setLang(lang){\n'
            "      localStorage.setItem('bp_lang',lang);\n"
            "      document.documentElement.lang = lang==='pt'?'pt-BR':'en';\n"
            "      const t=I18N[lang];\n"
            "      document.querySelectorAll('[data-i18n]').forEach(el=>{const k=el.getAttribute('data-i18n'); if(t[k]!==undefined) el.innerHTML=t[k];});\n"
            "      document.title=t.title;\n"
            "      const on='bg-sky-600 text-white', off='bg-white text-slate-600 hover:bg-slate-100';\n"
            "      document.getElementById('lang-pt').className='px-4 py-1.5 text-sm font-semibold transition-colors '+(lang==='pt'?on:off);\n"
            "      document.getElementById('lang-en').className='px-4 py-1.5 text-sm font-semibold transition-colors '+(lang==='en'?on:off);\n"
            "    }\n"
            "    setLang(localStorage.getItem('bp_lang')||'pt');\n"
            '  </script>\n'
            '</body>\n</html>\n'
        )
        out = head + h1 + section + script
        path = os.path.join(out_dir, f"sessao-{n}.html")
        open(path, "w").write(out)
        print("wrote", path)

if __name__ == "__main__":
    shell, out_dir, jsonf = sys.argv[1], sys.argv[2], sys.argv[3]
    data = json.load(open(jsonf))
    build(shell, out_dir, data["sessions"])
