#!/usr/bin/env python3
"""Checklist de completude de sessao (ver SESSAO_CHECKLIST.md).
Para cada sessao valida: header, EN+PT, texto do PDF, imagens do PDF, citacoes.
Auto-mapeia PDF pagina->sessao via marcador "Session N:".
Uso: python3 check_session_coverage.py [curso]
"""
import os, re, subprocess, sys, glob, json

ROOT = os.path.dirname(os.path.abspath(__file__))


def pdf_text(pdf):
    return subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout


def pdf_images_per_page(pdf):
    """{'pag': n_imagens} via pdfimages -list (requer poppler)."""
    out = subprocess.run(['pdfimages', '-list', pdf], capture_output=True, text=True).stdout
    counts = {}
    for line in out.splitlines()[2:]:  # pula header
        cols = line.split()
        if not cols or not cols[0].isdigit():
            continue
        try:
            pag = int(cols[0])
        except ValueError:
            continue
        counts[pag] = counts.get(pag, 0) + 1
    return counts


def page_to_session(pdf):
    """Mapeia pagina -> numero de sessao. Una unica chamada pdftotext com
    marcadores de pagina (-bbox omitido; usamos 'Session N:' por pagina)."""
    info = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
    mt = re.search(r'Pages:\s*(\d+)', info)
    total = int(mt.group(1)) if mt else 200
    full = {}
    last = None
    for p in range(1, total + 1):
        t = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), pdf, '-'],
                           capture_output=True, text=True).stdout
        m = re.search(r'Session (\d+):', t)
        if m:
            last = int(m.group(1))
        full[p] = last
    return full, total


def norm(t):
    t = t.lower()
    t = re.sub(r'[^a-zà-ú0-9 ]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()


def sentences(text):
    parts = re.split(r'(?<=[\.\:\!\?])\s+|\n', text)
    return [p.strip() for p in parts if len(p.strip()) > 35 and len(p.split()) >= 5]


def split_by_session(text):
    chunks = {}
    marks = [(m.start(), int(m.group(1))) for m in re.finditer(r'Session (\d+):', text)]
    for i, (pos, num) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        chunk = re.sub(r'Class Notes:.*', ' ', text[pos:end])
        chunk = re.sub(r'^\d+ of \d+$', ' ', chunk, flags=re.M)
        chunks.setdefault(num, []).extend(sentences(chunk))
    return chunks


def html_words(html):
    return norm(re.sub(r'&[a-z]+;', ' ', re.sub(r'<[^>]+>', ' ', html)))


def coverage(pdf_sentences, html_norm):
    if not pdf_sentences:
        return 1.0
    present = 0
    for s in pdf_sentences:
        words = set(norm(s).split())
        if not words:
            continue
        if sum(1 for w in words if w in html_norm) / len(words) >= 0.55:
            present += 1
    return present / len(pdf_sentences)


def session_html_path(course, num):
    for d in sorted(glob.glob(os.path.join(ROOT, course, 'modulo-*'))):
        p = os.path.join(d, f'sessao-{num}.html')
        if os.path.exists(p):
            return p
    return None


def check_one(course, num, pdf_sentences, pdf_img_count):
    hp = session_html_path(course, num)
    if not hp:
        return {'exists': False}
    html = open(hp, encoding='utf-8').read()
    hn = html_words(html)
    has_img = '<img' in html
    n_en = len(re.findall(r'class="lang-en">', html))
    n_pt = len(re.findall(r'class="lang-pt">', html))
    ratio = coverage(pdf_sentences, hn)
    # criterios
    crit = {}
    crit['header'] = all(k in html for k in
                         ['class="title', 'Voltar', 'window.print', 'setLang',
                          'reading-progress', 'verse-modal.js', 'page-footer'])
    crit['en_pt'] = n_en > 0 and n_pt > 0
    crit['text'] = ratio >= 0.85
    crit['images'] = (pdf_img_count == 0) or (len(re.findall(r'<img', html)) >= pdf_img_count)
    crit['citations'] = bool(re.search(r'[A-Z][a-z]+ [A-Z]\. ?[A-Z][a-z]+ \(\d{4}\)', html)) or n_en == 0
    crit['ratio'] = round(ratio, 3)
    crit['n_en'] = n_en
    crit['n_pt'] = n_pt
    crit['pdf_imgs'] = pdf_img_count
    crit['html_imgs'] = len(re.findall(r'<img', html))
    return {'exists': True, **crit}


def check_course(course):
    pdf = os.path.join(ROOT, course, f'{course}-teacher-notes.pdf')
    if not os.path.exists(pdf):
        return None
    text = pdf_text(pdf)
    chunks = split_by_session(text)
    pagemap, total = page_to_session(pdf)
    imgcounts = pdf_images_per_page(pdf)
    # imagens por sessao
    sess_imgs = {}
    for p, s in pagemap.items():
        if s:
            sess_imgs[s] = sess_imgs.get(s, 0) + imgcounts.get(p, 0)
    print(f'\n=== {course} ===')
    results = {}
    for num in sorted(chunks):
        c = check_one(course, num, chunks[num], sess_imgs.get(num, 0))
        if not c['exists']:
            results[num] = {'missing_html': True}
            print(f'  S{num:>2}: MISSING HTML')
            continue
        fails = [k for k in ('header', 'en_pt', 'text', 'images', 'citations') if not c[k]]
        tag = 'OK' if not fails else 'FAIL:' + ','.join(fails)
        if c['text'] and not c['en_pt']:
            tag = 'PT'  # traduzido PT-only
        results[num] = c
        extra = f" imgs(html={c['html_imgs']}/pdf={c['pdf_imgs']}) en={c['n_en']} pt={c['n_pt']}"
        print(f'  S{num:>2}: {c["ratio"]:6.1%} [{tag}]{extra}')
    return results


if __name__ == '__main__':
    courses = [sys.argv[1]] if len(sys.argv) > 1 else None
    if not courses:
        courses = [d for d in sorted(os.listdir(ROOT))
                   if os.path.isdir(os.path.join(ROOT, d))
                   and os.path.exists(os.path.join(ROOT, d, f'{d}-teacher-notes.pdf'))]
    bad = 0
    for c in courses:
        r = check_course(c)
        if r:
            for num, d in r.items():
                if d.get('missing_html') or (d.get('exists') and not all(d.get(k, False) for k in ('header', 'en_pt', 'text', 'images'))):
                    bad += 1
    print(f'\n{bad} sessoes com pendencia (header/en_pt/text/imagens)')
