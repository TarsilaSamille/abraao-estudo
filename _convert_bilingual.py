#!/usr/bin/env python3
"""Convert bilingual <div class="page reveal"><span lang-pt>..<br>..</span><span lang-en>..<br>..</span></div>
blobs into semantic bilingual HTML (headings/p/ul with per-element lang spans).

Lazy approach: split PT and EN, derive block structure from each independently,
and only emit merged output when the two sides have identical block structure
(same count, same types, same list lengths). On any mismatch, return None and
the caller leaves the blob untouched.
"""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
BLOB_RE = re.compile(r'<div class="page reveal">(.*?)</div>', re.S)
TERMINATORS = ('.', '?', '!')
HEADING_MAX = 120  # ezekiel/joseph use long section-title headings

def _lines(text):
    norm = text.replace('<br>', '\n').replace('<br/>', '\n')
    return [l.strip() for l in norm.split('\n') if l.strip()]

def _drop_header(lines):
    idx = 0
    if lines and lines[0].startswith('Class Notes:'):
        idx = 1
        if idx < len(lines) and re.match(r'^\d+ of \d+$', lines[idx]):
            idx += 1
        if idx < len(lines) and lines[idx].startswith('Session '):
            idx += 1
    return lines[idx:]

def _is_heading_line(s):
    s = s.strip()
    if not s or len(s) > HEADING_MAX or s.endswith(TERMINATORS):
        return False
    return True

def text_to_blocks(text):
    """Return list of (kind, lines) where kind in {'h2','h3','p','ul'}."""
    lines = _lines(text)
    body = _drop_header(lines)
    if not body:
        return []
    # merge broken-across-<br> continuation of a long title into the previous line
    merged = []
    for ln in body:
        if (merged and _is_heading_line(ln) and _is_heading_line(merged[-1])
                and len(merged[-1]) > 40):
            merged[-1] = merged[-1] + ' ' + ln
        else:
            merged.append(ln)
    body = merged

    blocks = []
    cur_para = []
    prev_ended = True

    def is_candidate(line):
        s = line.strip()
        if not _is_heading_line(s):
            return False
        if re.match(r'^\d', s):  # verse number => paragraph, not heading
            return False
        if s.startswith('*'):  # footnote label, not a heading
            return False
        first = s.split()[0].lower().strip('*')
        if first in ('and', 'for', 'but', 'or', 'the', 'that', 'they', 'to', 'of', 'in', 'on', 'with', 'a', 'an'):
            return False
        return True

    i = 0
    while i < len(body):
        line = body[i]
        cand = is_candidate(line)
        if cand and prev_ended:
            # detect run of consecutive candidates (list items)
            j = i
            while j + 1 < len(body) and is_candidate(body[j + 1]):
                j += 1
            n_ahead = j - i
            if n_ahead >= 2:  # 3+ candidates => bullet list
                if cur_para:
                    blocks.append(('p', cur_para)); cur_para = []
                blocks.append(('ul', body[i:j + 1]))
                prev_ended = True
                i = j + 1
                continue
            if n_ahead == 1 and len(body[i]) > 46:
                # long-line break (e.g. "The prophets saw…on" + "the other") — not a 2-item list
                cur_para.append(body[i])
                prev_ended = body[i].endswith(TERMINATORS)
                i += 1
                continue
            # single (or pair) candidate: heading only if next line ends a sentence
            # or is itself a candidate; otherwise it's a paragraph start
            nxt = body[i + 1] if i + 1 < len(body) else ''
            # heading if next line is itself a candidate (another heading/list item),
            # or if this line is short and the next ends a sentence.
            # Long lines followed by a period-terminated sentence are broken paragraphs.
            is_head = is_candidate(nxt) or (len(line) <= 46 and nxt.endswith(TERMINATORS))
            if is_head:
                if cur_para:
                    blocks.append(('p', cur_para)); cur_para = []
                if j > i:  # pair: treat as heading + paragraph fallback
                    blocks.append(('h2', [line]))
                    prev_ended = True
                    i += 1
                    continue
                kind = 'h3' if line.lower().startswith('reflection') else 'h2'
                blocks.append((kind, [line]))
                prev_ended = True
                i += 1
                continue
            # paragraph start (broken line)
        cur_para.append(line)
        prev_ended = line.endswith(TERMINATORS)
        i += 1
    if cur_para:
        blocks.append(('p', cur_para))
    return blocks

def _blocks_match(pb, eb):
    if len(pb) != len(eb):
        return False
    for (pk, pl), (ek, el) in zip(pb, eb):
        if pk != ek:
            return False
        if pk == 'ul' and len(pl) != len(el):
            return False
    return True

def convert_bilingual(inner):
    mpt = re.search(r'<span class="lang-pt">(.*?)</span>', inner, flags=re.S)
    men = re.search(r'<span class="lang-en">(.*?)</span>', inner, flags=re.S)
    if not mpt or not men:
        return None
    pb = text_to_blocks(mpt.group(1))
    eb = text_to_blocks(men.group(1))
    if not _blocks_match(pb, eb):
        return None

    out = []
    for (pk, pl), (ek, el) in zip(pb, eb):
        if pk == 'ul':
            lis = ''.join(
                f'      <li><span class="lang-pt">{p}</span><span class="lang-en">{e}</span></li>\n'
                for p, e in zip(pl, el))
            out.append(f'    <ul class="bullets reveal">\n{lis}    </ul>')
        elif pk in ('h2', 'h3'):
            out.append(f'    <{pk} class="reveal"><span class="lang-pt">{pl[0]}</span><span class="lang-en">{el[0]}</span></{pk}>')
        else:  # p
            out.append(f'    <p class="body reveal"><span class="lang-pt">{" ".join(pl)}</span><span class="lang-en">{" ".join(el)}</span></p>')
    return '\n'.join(out)

def process_file(path):
    data = open(path, encoding='utf-8', errors='replace').read()
    if '<div class="page reveal">' not in data:
        return False
    changed = False

    def repl(m):
        nonlocal changed
        inner = m.group(1)
        if '<span' not in inner:
            return m.group(0)  # not bilingual — leave (handled by other script)
        res = convert_bilingual(inner)
        if res is None:
            return m.group(0)  # mismatch — preserve
        changed = True
        return '\n' + res + '\n'

    new = BLOB_RE.sub(repl, data)
    if changed:
        open(path, 'w', encoding='utf-8').write(new)
    return changed

def main():
    # only courses that still have span+br blobs
    files = glob.glob(os.path.join(ROOT, '**/sessao-*.html'), recursive=True)
    done = skip = 0
    for f in files:
        if 'exodus-overview/' in f:
            continue
        if process_file(f):
            done += 1
        else:
            # count preserved
            h = open(f, encoding='utf-8', errors='replace').read()
            if '<div class="page reveal">' in h and '<span' in h:
                skip += 1
    print(f"converted {done} files, {skip} preserved (mismatch)")

if __name__ == '__main__':
    main()
