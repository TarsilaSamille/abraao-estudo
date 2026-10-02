#!/usr/bin/env python3
"""Cobertura verbatim EN do HTML contra o PDF DA SESSÃO.

Por que este arquivo substitui o medidor por intervalo de páginas:
o auditor antigo adivinhava o intervalo de cada sessão varrendo o livro
inteiro em busca de "Session N:" + "Key Takeaways". Esse método erra:
no abraao ele atribuiu as páginas [30,41] à sessão 5, quando o PDF real
da sessão (`pdf-sessoes/sessao-5.pdf`) cobre outras páginas. O resultado
era uma cobertura subestimada (65,5% em vez de 87,7%) e palavras de outras
sessoes aparecendo como "faltando".

Aqui a fonte é sempre o recorte por sessao, `pdf-sessoes/sessao-N.pdf`, que
e o PDF da sessao. So quando ele nao existe caimos no livro inteiro — e nesse
caso marcamos `range=BOOK` para nao confiar no numero.

Uso:
    python3 bots/audit_coverage.py            # todos os cursos
    python3 bots/audit_coverage.py abraao     # um curso
    python3 bots/audit_coverage.py --low      # so as sessões abaixo do limite
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THRESHOLD = 85.0

# Chrome da UI e cabecalho/rodape do PDF: nao contam como conteudo.
BOILER = re.compile(r'Class Notes.*?\d+\s*of\s*\d+|^\s*\d+\s*$', re.M)
UI_WORDS = {
    'voltar', 'imprimir', 'back', 'print', 'portugues', 'português',
    'english', 'ingles', 'inglês',
}


def words(text):
    return set(w.lower() for w in re.findall(r"[A-Za-zÀ-ÿ]{4,}", text))


def pdftotext(path, first=None, last=None):
    cmd = ['pdftotext', '-layout']
    if first:
        cmd += ['-f', str(first), '-l', str(last)]
    cmd += [path, '-']
    return subprocess.run(cmd, capture_output=True, text=True).stdout


ANY_SPAN = re.compile(r'<span\b[^>]*>|</span>', re.I)
OPEN_EN = re.compile(r'<span class="lang-en"[^>]*>', re.I)


def balanced_en_text(body):
    """Texto dos spans lang-en, com aninhamento resolvido.

    O regex Ingenuo `<span class="lang-en">(.*?)</span>` para no PRIMEIRO
    `</span>`, e quase todo texto bilíngue tem span aninhado
    (`<span class="lang-en">…<span class="ref">…</span>…</span>`). O texto
    ficava truncado e as palavras depois do primeiro `</span>` contavam como
    "faltando" — foi o que produziu 8 sessões de abraao marcadas como 75-84%
    quando na verdade tinham 97-100% (medido por agents de forma independente).
    Aqui varremos ate a profundidade zero, como em audit_parity.py.
    """
    out = []
    for m in OPEN_EN.finditer(body):
        depth, pos = 1, m.end()
        while depth > 0:
            n = ANY_SPAN.search(body, pos)
            if not n:
                break
            depth += -1 if n.group(0).startswith('</') else 1
            pos = n.end()
        raw = body[m.end():pos - len('</span>')] if depth == 0 else body[m.end():]
        out.append(re.sub(r'<[^>]+>', ' ', raw))
    return ' '.join(out)


def html_en_words(path):
    """Palavras do conteudo EN: spans lang-en, ou o corpo se forem poucos."""
    html = open(path, encoding='utf-8').read()
    body = re.sub(r'<style\b[\s\S]*?</style>|<script\b[\s\S]*?</script>', '', html, flags=re.I)
    # corta o chrome do cabecalho
    m = re.search(r'<main\b', body)
    if m:
        body = body[m.start():]
    en = balanced_en_text(body)
    if len(words(en)) < 150:          # pagina sem spans: usa o HTML todo
        en = re.sub(r'<[^>]+>', ' ', body)
    return words(en)


def find_html(course, n):
    for mod in sorted(glob.glob(os.path.join(REPO, course, 'modulo-*'))):
        cand = os.path.join(mod, f'sessao-{n}.html')
        if os.path.exists(cand):
            return cand
    hits = sorted(glob.glob(os.path.join(REPO, course, '**', f'sessao-{n}.html'), recursive=True))
    return hits[0] if hits else None


def book_ranges(pdf):
    """Fallback: intervalos por 'Session N:' no livro inteiro. Menos confiavel."""
    pages = pdftotext(pdf).split('\f')
    starts = {}
    for i, p in enumerate(pages, 1):
        if i <= 4:
            continue
        m = re.search(r'Session\s+(\d+)\s*:', p)
        if m:
            starts.setdefault(int(m.group(1)), i)
    nums = sorted(starts)
    out = {}
    for idx, n in enumerate(nums):
        end = starts[nums[idx + 1]] - 1 if idx + 1 < len(nums) else len(pages)
        out[n] = (starts[n], end)
    return out


def session_slice(pdf):
    """Paginas [ini, fim) da sessão N dentro do PDF, se ele contiver varias.

    Alguns `pdf-sessoes/sessao-N.pdf` sao recortes Large demais e incluem o
    comeco da sessão N+1 (adam-to-noah/sessao-31 tem as sessoes 31 e 32;
    intro-hebrew-bible/sessao-28 tem 28 e 29). Medir contra o arquivo inteiro
    contava como "faltando" o texto da sessão seguinte e dava cobertura
    artificialmente baixa (9,2% em vez de ~100%). Aqui cortamos na pagina em
    que a proxima sessao comeca.
    """
    try:
        import fitz
    except ImportError:
        return None
    doc = fitz.open(pdf)
    starts = []
    for i, page in enumerate(doc, 1):
        t = page.get_text()
        if re.search(r'Session\s+\d+\s*:', t) and 'Key Takeaways' in t:
            m = re.search(r'Session\s+(\d+)\s*:', t)
            starts.append((i, int(m.group(1))))
    doc.close()
    if len(starts) < 2:
        return None
    for idx, (pg, num) in enumerate(starts):
        end = starts[idx + 1][0] - 1 if idx + 1 < len(starts) else 10**6
        if num == n_of(pdf) and end < 10**6:
            return (pg, end)
    return None


def n_of(pdf):
    m = re.search(r'sessao-(\d+)\.pdf$', pdf)
    return int(m.group(1)) if m else -1


def audit_course(course):
    htmls = sorted(glob.glob(os.path.join(REPO, course, 'modulo-*', 'sessao-*.html')))
    if not htmls:
        return None
    nums = sorted({int(re.search(r'sessao-(\d+)\.html', h).group(1)) for h in htmls})
    book = sorted(glob.glob(os.path.join(REPO, course, '*teacher-notes.pdf')))
    ranges = book_ranges(book[0]) if book else {}

    res = {}
    for n in nums:
        html = find_html(course, n)
        got = html_en_words(html)
        per_session = os.path.join(REPO, course, 'pdf-sessoes', f'sessao-{n}.pdf')
        if os.path.exists(per_session):
            sl = session_slice(per_session)
            if sl:
                txt, src, rng = pdftotext(per_session, sl[0], sl[1]), 'pdf-sessoes', list(sl)
            else:
                txt, src, rng = pdftotext(per_session), 'pdf-sessoes', None
        elif n in ranges:
            s, e = ranges[n]
            txt, src, rng = pdftotext(book[0], s, e), 'teacher-notes', [s, e]
        else:
            res[n] = {'cov': None, 'status': 'NO_PDF', 'file': os.path.relpath(html, REPO)}
            continue
        exp = words(BOILER.sub(' ', txt))
        cov = round(100 * len(exp & got) / max(1, len(exp)), 1)
        status = 'OK' if cov >= THRESHOLD else 'LOW'
        if rng:
            status += '(BOOK)'          # numero derivado do livro: nao confiar
        res[n] = {
            'cov': cov,
            'status': status,
            'src': src,
            'range': rng,
            'file': os.path.relpath(html, REPO),
            'missing': sorted(exp - got)[:60],
        }
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('course', nargs='?')
    ap.add_argument('--low', action='store_true', help='so as sessoes abaixo do limite')
    ap.add_argument('--json', default=os.path.join(REPO, 'bots/state/coverage.json'))
    a = ap.parse_args()

    courses = [a.course] if a.course else sorted(
        d for d in os.listdir(REPO)
        if os.path.isdir(os.path.join(REPO, d))
        and glob.glob(os.path.join(REPO, d, 'modulo-*', 'sessao-*.html'))
    )

    all_res = {}
    low_total = 0
    for course in courses:
        res = audit_course(course)
        if not res:
            continue
        all_res[course] = res
        low = [k for k, v in res.items() if str(v['status']).startswith('LOW')]
        low_total += len(low)
        print(f"\n=== {course}  ({len(res)} sessoes, {len(low)} abaixo de {THRESHOLD:.0f}%) ===")
        for n in sorted(res, key=int):
            v = res[n]
            if v['cov'] is None:
                print(f"  S{n:>2}  [SEM PDF]  {v['file']}")
                continue
            if a.low and not str(v['status']).startswith('LOW'):
                continue
            print(f"  S{n:>2}  {v['cov']:5.1f}%  {v['status']:9s} {v['src']:13s} {v['file']}")

    # Nao sobrescreva o arquivo completo quando o comando foi com escopo:
    # rodar `audit_coverage.py abraao` apagava o resultado dos outros 15 cursos
    # e deixava briefs/orquestracao com dados de um curso so.
    out = a.json if not a.course else a.json.replace('.json', f'.{a.course}.json')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(all_res, fh, indent=1, ensure_ascii=False)

    total = sum(len(v) for v in all_res.values())
    print(f"\n{'=' * 60}\nCursos: {len(all_res)}  Sessoes: {total}  Abaixo de {THRESHOLD:.0f}%: {low_total}")
    print(f"Escrito {os.path.relpath(out, REPO)}")
    if a.course:
        print(f"(escopo: o completo continua em {os.path.relpath(a.json, REPO)})")
    return 0


if __name__ == '__main__':
    sys.exit(main())