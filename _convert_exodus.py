#!/usr/bin/env python3
"""Convert exodus-overview <div class="page reveal"> blobs to semantic HTML.

Lazy, deterministic converter. No new deps. Reuses the course's own CSS
classes (.takeaways-h, .bullets, .section, .sub, .body). Keeps text verbatim
(EN) per user decision. Header lines (Class Notes / N of M / Session N:) are
redundant with the existing <h1> and dropped.
"""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
BLOB_RE = re.compile(r'<div class="page reveal">(.*?)</div>', re.S)

TERMINATORS = ('.', '?', '!')
HEADING_MAX = 46  # chars; longer lines are never headings

def is_heading(line, prev_ended_sentence):
    s = line.strip()
    if not s:
        return False
    if len(s) > HEADING_MAX:
        return False
    if s.endswith(TERMINATORS):
        return False
    # a heading only starts a new block right after a paragraph ended
    # (or at block start) — never mid-paragraph (which lacks sentence end)
    if not prev_ended_sentence:
        return False
    return True

def convert_blob(inner):
    # ponytail: real files use either <br> or real newlines — normalize both
    norm = inner.replace('<br>', '\n').replace('<br/>', '\n')
    lines = [l.strip() for l in norm.split('\n')]
    lines = [l for l in lines if l]
    # drop header (first 3 lines): Class Notes / N of M / Session N:
    idx = 0
    if lines and lines[0].startswith('Class Notes:'):
        idx = 1
        if idx < len(lines) and re.match(r'^\d+ of \d+$', lines[idx]):
            idx += 1
        if idx < len(lines) and lines[idx].startswith('Session '):
            idx += 1
    body = lines[idx:]
    if not body:
        return ''

    # group into blocks: heading line, then paragraph lines until next heading
    blocks = []  # (heading_text, [para_lines])  heading may be None for first
    cur_head = None
    cur_para = []
    prev_ended = True  # block start behaves like after a sentence
    for li, line in enumerate(body):
        if is_heading(line, prev_ended):
            # flush previous paragraph
            if cur_para:
                blocks.append((cur_head, cur_para))
                cur_para = []
            cur_head = None  # will be set by this heading line
            # heading line itself
            blocks.append((line, None))  # marker: pure heading
            prev_ended = True
        else:
            cur_para.append(line)
            prev_ended = line.endswith(TERMINATORS)
    if cur_para:
        blocks.append((cur_head, cur_para))

    # render
    html = []
    last_heading = None
    i = 0
    while i < len(blocks):
        head, para = blocks[i]
        if para is None:
            # heading — look ahead for a run of consecutive headings (a list)
            j = i
            while j + 1 < len(blocks) and blocks[j + 1][1] is None:
                j += 1
            if j > i:  # run of >=2 consecutive headings => bullet list
                items = [blocks[k][0] for k in range(i, j + 1)]
                html.append('    <ul class="bullets reveal">')
                for it in items:
                    html.append(f'      <li>{it}</li>')
                html.append('    </ul>')
                last_heading = None
                i = j + 1
                continue
            last_heading = head
            if head.lower().startswith('reflection'):
                html.append(f'    <h3 class="sub reveal">{head}</h3>')
            else:
                html.append(f'    <h2 class="section reveal">{head}</h2>')
            i += 1
            continue
        # paragraph block
        if last_heading == 'Key Takeaways':
            # ponytail: blob bullets are often line-wrapped mid-sentence;
            # group lines until one ends with a sentence terminator
            items = []
            buf = []
            for pl in para:
                buf.append(pl)
                if pl.endswith(TERMINATORS):
                    items.append(' '.join(buf))
                    buf = []
            if buf:
                items.append(' '.join(buf))
            if len(items) == 1:
                html.append(f'    <p class="body reveal">{items[0]}</p>')
            else:
                lis = ''.join(f'      <li>{it}</li>\n' for it in items)
                html.append(f'    <ul class="bullets reveal">\n{lis}    </ul>')
        else:
            text = ' '.join(para)
            html.append(f'    <p class="body reveal">{text}</p>')
        last_heading = None
        i += 1
    return '\n'.join(html)

def convert_file(path):
    data = open(path, encoding='utf-8', errors='replace').read()
    if '<div class="page reveal">' not in data and 'class="table-img' not in data:
        return False
    new = BLOB_RE.sub(lambda m: '\n' + convert_blob(m.group(1)) + '\n', data)
    # exodus table-img are page/diagram renders already covered by the blobs
    new = re.sub(r'<div class="table-img reveal">.*?</div>\s*', '', new, flags=re.S)
    open(path, 'w', encoding='utf-8').write(new)
    return True

def main():
    files = sorted(glob.glob(os.path.join(ROOT, 'exodus-overview/**/sessao-*.html'), recursive=True))
    done = 0
    for f in files:
        rel = os.path.relpath(f, ROOT)
        if 'sessao-12.html' in rel:  # already hand-converted, keep
            continue
        if convert_file(f):
            done += 1
    print(f"converted {done} exodus files")

if __name__ == '__main__':
    main()
