#!/usr/bin/env python3
"""Assemble jonah session HTML from the canonical sessao-1 shell.

jonah's shell (sessao-1.html) is the source of truth: tailwind CDN, the
verse-modal.js tag, the floating nav (back -> ../index.html, lang buttons
calling setLang), the reveal IntersectionObserver, and the lang key
`jonah-sN-lang`. We copy it verbatim and swap only: <title>, the h1, the
container inner body, and the `jonah-s1-lang` key -> jonah-sN-lang.

PDF map (off-by-one, verified): HTML session N <- pdf-sessoes/sessao-(N+1).pdf
for N=1..43. sessao-45.pdf holds sessions 44 AND 45. sessao-1.pdf is cover+TOC.
"""
import json, re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "modulo-1", "sessao-1.html")
MODULE_OF = {n: m for m, rng in {
    1: range(1, 6), 2: range(6, 10), 3: range(10, 15), 4: range(15, 22),
    5: range(22, 29), 6: range(29, 36), 7: range(36, 40), 8: range(40, 46),
}.items() for n in rng}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def takeaways(items):
    lis = "\n".join(
        f'      <li><span class="lang-pt">{esc(p)}</span>'
        f'<span class="lang-en">{esc(e)}</span></li>'
        for p, e in items)
    return (f'    <h3 class="takeaways-h reveal"><span class="lang-pt">'
            f'Principais Lições</span><span class="lang-en">'
            f'Key Takeaways</span></h3>\n    <ul class="bullets reveal">\n'
            f'{lis}\n    </ul>')


def section(h_pt, h_en, blocks):
    """blocks: list of ('p', pt, en) or ('raw', html)."""
    out = [f'    <h2 class="section reveal"><span class="lang-pt">{esc(h_pt)}'
           f'</span><span class="lang-en">{esc(h_en)}</span></h2>']
    for b in blocks:
        if b[0] == 'p':
            out.append(f'    <p class="body reveal"><span class="lang-pt">'
                       f'{esc(b[1])}</span><span class="lang-en">{esc(b[2])}'
                       f'</span></p>')
        elif b[0] == 'sub':
            out.append(f'    <h3 class="sub reveal"><span class="lang-pt">'
                       f'{esc(b[1])}</span><span class="lang-en">{esc(b[2])}'
                       f'</span></h3>')
        elif b[0] == 'raw':
            out.append(b[1])
    return "\n".join(out)


def reflection(pt, en):
    return (f'    <h3 class="sub reveal"><span class="lang-pt">'
            f'Pergunta de Reflexão</span><span class="lang-en">'
            f'Reflection Question</span></h3>\n'
            f'    <p class="body reveal"><span class="lang-pt">{esc(pt)}'
            f'</span><span class="lang-en">{esc(en)}</span></p>')


def build_session(n, title_pt, title_en, body_inner):
    tpl = open(TEMPLATE).read()
    mod = MODULE_OF[n]
    # title
    tpl = re.sub(r'<title>[^<]*</title>',
                 f'<title>Sessão {n}: {esc(title_pt)}</title>', tpl)
    # h1
    tpl = re.sub(r'<h1 class="title reveal">.*?</h1>',
                 f'<h1 class="title reveal"><span class="lang-pt">'
                 f'Sessão {n}: {esc(title_pt)}</span>'
                 f'<span class="lang-en">Session {n}: {esc(title_en)}'
                 f'</span></h1>', tpl, flags=re.S)
    # container inner: between the opening container div and the closing </div> before <script>
    open_m = re.search(r'(<div class="max-w-4xl[^>]*>)', tpl)
    script_m = re.search(r'\n  <script>', tpl)
    head = tpl[:open_m.end()]
    tail = tpl[script_m.start():]
    inner = (f'{open_m.group(1)}\n'
             f'    <h1 class="title reveal"><span class="lang-pt">'
             f'Sessão {n}: {esc(title_pt)}</span>'
             f'<span class="lang-en">Session {n}: {esc(title_en)}</span></h1>\n'
             f'    <hr class="rule">\n{body_inner}\n  ')
    # fix lang key
    tail = tail.replace('jonah-s1-lang', f'jonah-s{n}-lang')
    out = head + inner + tail
    outdir = os.path.join(HERE, f"modulo-{mod}")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"sessao-{n}.html")
    open(path, "w").write(out)
    return path


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    for s in spec["sessions"]:
        p = build_session(s["n"], s["title_pt"], s["title_en"], s["body"])
        print("wrote", p)
