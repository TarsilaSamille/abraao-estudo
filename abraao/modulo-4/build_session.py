#!/usr/bin/env python3
"""Build a modulo-4 session HTML in the canonical sessao-16 style.

Usage: python3 build_session.py <NN> <title_pt> <title_en> <content_file> [prev_nn]
- Reads canonical shell from modulo-4/sessao-16.html (head/style + nav + open container + script).
- Replaces back-link href/label, lang key sNN-lang, page-footer title.
- Inserts content from <content_file> (raw HTML body, already bilingual PT/EN) between container open and page-footer.
"""
import sys, re, os

BASE = os.path.dirname(os.path.abspath(__file__))
S16 = os.path.join(BASE, 'sessao-16.html')

def main():
    nn = sys.argv[1]
    title_pt = sys.argv[2]
    title_en = sys.argv[3]
    content_file = sys.argv[4]
    prev_nn = sys.argv[5] if len(sys.argv) > 5 else str(int(nn) - 1)

    c16 = open(S16, encoding='utf-8').read()
    content = open(content_file, encoding='utf-8').read().strip()

    # Shell parts
    marker_open = '<div class="max-w-4xl mx-auto px-6 md:px-10 py-14">'
    marker_footer = '<div class="page-footer">'
    head = c16[:c16.index(marker_open) + len(marker_open)]
    # footer block (from sessao-16) — we rebuild our own footer instead
    script_block_raw = c16[c16.rindex('<script>'):]

    # Back link: session16 uses href="index.html" label "Sessão 14"/"Session 14" — but canonical back is session14.html.
    # For our sessions: href="session{prev}.html", label "Sessão {prev}"/"Session {prev}".
    head = re.sub(r'href="index.html"', f'href="session{prev_nn}.html"', head)
    head = re.sub(r'Sessão 14', f'Sessão {prev_nn}', head)
    head = re.sub(r'Session 14', f'Session {prev_nn}', head)

    # Lang key
    script_block = script_block_raw.replace("'s16-lang'", f"'s{nn}-lang'")

    # Footer
    footer = (
        f'  <div class="page-footer">\n'
        f'    <span>Class Notes: Abraham</span>\n'
        f'    <span><span class="lang-pt">Sessão {nn} · {title_pt}</span>'
        f'<span class="lang-en">Session {nn} · {title_en}</span></span>\n'
        f'  </div>\n'
        f'</div>\n'
    )

    full = head + '\n' + content + '\n\n' + footer + script_block
    out = os.path.join(BASE, f'sessao-{nn}.html')
    open(out, 'w', encoding='utf-8').write(full)
    print(f'wrote {out} ({len(full)} bytes)')

if __name__ == '__main__':
    main()
