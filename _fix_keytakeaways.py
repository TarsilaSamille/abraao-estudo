#!/usr/bin/env python3
"""Post-fix: merge line-wrapped Key Takeaways <li> items in converted exodus files.

The blob converter split a single bullet that wrapped across <br> into several
<li>. A real bullet ends with a sentence terminator; lines without one are a
continuation. Re-merge them. Idempotent.
"""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
TERMINATORS = ('.', '?', '!')
KT_HEAD = re.compile(r'<h2[^>]*>Key Takeaways</h2>')
UL_RE = re.compile(r'(<ul class="bullets reveal">.*?</ul>)', re.S)

def fix_ul(ul):
    lis = re.findall(r'<li>(.*?)</li>', ul, re.S)
    if len(lis) <= 1:
        return ul
    out, buf = [], []
    for t in lis:
        buf.append(t.strip())
        if t.strip().endswith(TERMINATORS):
            out.append(' '.join(buf))
            buf = []
    if buf:
        out.append(' '.join(buf))
    if len(out) == len(lis):  # nothing merged
        return ul
    return '<ul class="bullets reveal">\n' + ''.join(f'      <li>{x}</li>\n' for x in out) + '    </ul>'

def main():
    files = glob.glob(os.path.join(ROOT, 'exodus-overview/**/sessao-*.html'), recursive=True)
    n = 0
    for f in files:
        h = open(f, encoding='utf-8', errors='replace').read()
        if 'Key Takeaways' not in h:
            continue
        def repl(m):
            return fix_ul(m.group(1))
        new = UL_RE.sub(repl, h)
        if new != h:
            open(f, 'w', encoding='utf-8').write(new)
            n += 1
    print(f"fixed Key Takeaways in {n} files")

if __name__ == '__main__':
    main()
