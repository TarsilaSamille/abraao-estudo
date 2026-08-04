#!/usr/bin/env python3
"""Build a module session HTML in the canonical sessao-16 style.

Usage: python3 build_session.py <NN> <title_pt> <title_en> <content_file> [prev_nn] [out_dir] [shell_html]
- Reads canonical shell from <shell_html> (default modulo-4/sessao-16.html).
- prev_nn=0 -> back link href="index.html" (module-first session).
- Inserts <content_file> (raw bilingual PT/EN body) between container open and page-footer.
"""
import sys, re, os

BASE = os.path.dirname(os.path.abspath(__file__))
S16 = os.path.join(BASE, 'modulo-4', 'sessao-16.html')

def main():
    nn = sys.argv[1]
    title_pt = sys.argv[2]
    title_en = sys.argv[3]
    content_file = sys.argv[4]
    prev_nn = sys.argv[5] if len(sys.argv) > 5 else str(int(nn) - 1)
    out_dir = sys.argv[6] if len(sys.argv) > 6 else os.path.join(BASE, 'modulo-4')
    shell = sys.argv[7] if len(sys.argv) > 7 else S16

    c16 = open(shell, encoding='utf-8').read()
    content = open(content_file, encoding='utf-8').read().strip()

    marker_open = '<div class="max-w-4xl mx-auto px-6 md:px-10 py-14">'
    head = c16[:c16.index(marker_open) + len(marker_open)]
    head = re.sub(r'<title>[^<]*</title>', f'<title>{title_pt}</title>', head)
    script_block_raw = c16[c16.rindex('<script>'):]

    # Back-link always returns to the module's own index.html (same dir).
    back_href = 'index.html'
    head = re.sub(r'href="[^"]*index\.html"', 'href="index.html"', head)
    head = re.sub(r'href="session\d+\.html"', 'href="index.html"', head)
    if prev_nn == '0':
        head = re.sub(r'Sessão 14', 'Sessões', head)
        head = re.sub(r'Session 14', 'Sessions', head)
        back_label_pt, back_label_en = 'Sessões', 'Sessions'
    else:
        head = re.sub(r'Sessão 14', f'Sessão {prev_nn}', head)
        head = re.sub(r'Session 14', f'Session {prev_nn}', head)
        back_label_pt, back_label_en = f'Sessão {prev_nn}', f'Session {prev_nn}'

    script_block = script_block_raw.replace("'s16-lang'", f"'s{nn}-lang'")

    footer = (
        f'  <div class="page-footer">\n'
        f'    <span>Class Notes: Abraham</span>\n'
        f'    <span><span class="lang-pt">Sessão {nn} · {title_pt}</span>'
        f'<span class="lang-en">Session {nn} · {title_en}</span></span>\n'
        f'  </div>\n'
        f'</div>\n'
    )

    full = head + '\n' + content + '\n\n' + footer + script_block
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f'sessao-{nn}.html')
    open(out, 'w', encoding='utf-8').write(full)
    print(f'wrote {out} ({len(full)} bytes)')

if __name__ == '__main__':
    main()
