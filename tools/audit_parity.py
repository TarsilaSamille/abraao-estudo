#!/usr/bin/env python3
"""Auditoria de paridade PT/EN nas páginas de sessão.

Por que este arquivo existe: medir pares de idioma com um regex
`<span class="lang-(pt|en)"[^>]*>(.*?)</span>` é ERRADO. O `.*?` para no
primeiro `</span>`, e quase todo texto bilíngue tem span aninhado
(`<span class="lang-pt">...<span class="chip">...</span>...</span>`). O
resultado é truncamento, contagem errada e falsos positivos.

Aqui a extração é balanceada: a partir da tag de abertura, conta
`<span`/`</span>` até a profundidade zero.

Detecta quatro defeitos:
  ORFAO   — span de um idioma não seguido imediatamente pelo par do outro
  IGUAL   — lang-en é cópia do lang-pt (tradução não feita)
  IDIOMA  — texto PT com linguagem english, ou texto EN com linguagem portuguesa
  SEMIDIOMA — a página não tem nenhum par de um dos idiomas

Uso:
    python3 tools/audit_parity.py                 # todos os cursos
    python3 tools/audit_parity.py abraao jacob    # so esses cursos
    python3 tools/audit_parity.py --details       # mostra exemplos
"""
import argparse
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Chrome da UI: nao e conteudo bilíngue.
UI_TEXTS = {
    'voltar', 'imprimir', 'back', 'print', 'pt', 'en',
    'português', 'portugues', 'english', 'inglês', 'ingles',
}

# Marcadores tipicos de portugues (para detectar EN nao traduzido)
PT_MARKERS = re.compile(
    r'\b(que|não|você|vocês|com|uma|para|como|onde|quando|muito|'
    r'nós|eles|ela|ele|isto|isso|seu|sua|dos|das|pelo|pela)\b', re.I)
# Marcadores tipicos de ingles (para detectar PT nao traduzido)
EN_MARKERS = re.compile(
    r'\b(the|and|with|from|that|which|were|was|they|their|'
    r'you|your|shall|unto|unto)\b', re.I)

TAG_SPAN = re.compile(r'<span\b[^>]*class="[^"]*\blang-(pt|en)\b[^"]*"[^>]*>', re.I)
ANY_SPAN = re.compile(r'<span\b[^>]*>|</span>', re.I)


def strip_tags(s):
    s = re.sub(r'<br\s*/?>', ' ', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = (s.replace('&ldquo;', '"').replace('&rdquo;', '"')
          .replace('&rsquo;', "'").replace('&lsquo;', "'")
          .replace('&nbsp;', ' ').replace('&amp;', '&')
          .replace('&mdash;', '—').replace('&ndash;', '–'))
    return re.sub(r'\s+', ' ', s).strip()


def extract_spans(html):
    """[(lang, texto, offset)] dos spans lang-pt/lang-en de primeiro nivel.

    Equilibrado: varre ate a profundidade zero, entao spans aninhados nao
    truncam nem sao contados como pares independentes.
    """
    out = []
    for m in TAG_SPAN.finditer(html):
        # profundidade 1 = o proprio span que acabamos de abrir
        depth = 1
        pos = m.end()
        while depth > 0:
            n = ANY_SPAN.search(html, pos)
            if not n:
                break
            depth += -1 if n.group(0).startswith('</') else 1
            pos = n.end()
        raw = html[m.end():pos - len('</span>')] if depth == 0 else html[m.end():]
        out.append((m.group(1).lower(), strip_tags(raw), m.start()))
    return out


def normalise(s):
    """Para comparar PT vs EN: minusculas, sem acento e sem pontuacao."""
    s = s.lower()
    s = ''.join(c for c in unicodedata_nfkd(s) if not _combining(c))
    return re.sub(r'[^a-z0-9 ]', '', s)


def unicodedata_nfkd(s):
    import unicodedata
    return unicodedata.normalize('NFKD', s)


def _combining(c):
    import unicodedata
    return unicodedata.combining(c)


def is_language_neutral(t):
    """Texto que e legitimately igual em PT e EN.

    Sem isso o detector acusa milhares de falsos positivos: referencias
    bíblicas ('Gênesis 11:27' vs 'Genesis 11:27' viram a mesma string depois
    de tirar acento), marcadores do design literário ('a', 'b', "a'", '17'),
    sigla de tradução (NASB, NIV, ESV) e termos hebraicos/gregos.
    """
    if not t:
        return True
    # so numeros / referencia biblica / marcador curto
    if re.fullmatch(r"[\d:;\.\s\-\u2013\u2014]+", t):          # '11:27', '1-3'
        return True
    if len(t) <= 3 and re.fullmatch(r"[a-zA-Z0-9'′\.\s]+", t):  # 'a', "a'", '17'
        return True
    # sigla de traducao / rotulo curto em caixa alta
    if re.fullmatch(r"[A-Z][A-Za-z]{0,7}[*\\]?", t):
        return True
    # tem palavra nao inglesa de verdade? (hebraico/grego fica de fora)
    return not re.search(r'[A-Za-z]{3,}', t)


# Assinatura mais confiavel de referencia bibliografica: ano entre
# parenteses (com 4 digitos, ou um intervalo de anos), precedido de autor com
# virgula ("Pogoloff, Stephen (1992). ...", "García Martínez ... (1997-1998). ...").
# Cobre tambem "(ed.)", que so aparece depois do titulo/nome do editor.
CITATION = re.compile(r'\((1[0-9]{3}|20[0-9]{2})(\s*[-–]\s*(1[0-9]{3}|20[0-9]{2}))?\)')
CITATION_EDITOR = re.compile(r'\((ed\.|eds\.|trad\.|editora)\)', re.I)
CREDIT = re.compile(
    r'(Created by|Illustration|Wikimedia|Openstreetmap|Flickr|Public domain|'
    r'Courtesy of|Cropped from|Photo:|Alamy|Shutterstock)', re.I)
# "Pt: 'Representantes da Visão X: Autor (2010). ...'" ePT correto: o rotulo
# esta traduzido e so a citaacao segue em ingles, por convencao. O mesmo vale
# para listas de nomes proprios (Yehohshaphat, Yoram, Ahaziah...).
NAMELIST = re.compile(r'^[\w\'’.\-]+(\s*,\s*[\w\'’.\-]+){3,}\s*\.?$')


def is_neutral_pair(t):
    """Par PT==EN que é correto por convenção (citação, crédito ou lista de nomes)."""
    return bool(CITATION.search(t) or CITATION_EDITOR.search(t)
                or CREDIT.search(t) or NAMELIST.match(t.strip()))


def long_enough(t, n=60):
    return len(t) >= n


def audit_file(path):
    html = open(path, encoding='utf-8').read()
    # corta o chrome do cabecalho/rodape e o que nao e conteudo
    body = re.sub(r'<style\b[\s\S]*?</style>', '', html, flags=re.I)
    body = re.sub(r'<script\b[\s\S]*?</script>', '', body, flags=re.I)
    m = re.search(r'<main\b', body)
    if m:
        body = body[m.start():]
    else:
        m = re.search(r'<footer\b', body)
        if m:
            body = body[:m.start()]

    spans = [(l, t, o) for l, t, o in extract_spans(body)
             if t and t.lower() not in UI_TEXTS]
    r = {'n_spans': len(spans), 'pt': 0, 'en': 0, 'orfos': 0, 'iguais': 0,
         'idioma_errado': 0, 'neutros': 0, 'problemas': []}

    if not spans:
        r['sem_idioma'] = 'sem nenhum par lang-pt/lang-en'
        return r, spans

    r['pt'] = sum(1 for l, _, _ in spans if l == 'pt')
    r['en'] = sum(1 for l, _, _ in spans if l == 'en')
    if r['pt'] == 0 or r['en'] == 0:
        r['sem_idioma'] = f"so {'pt' if r['pt'] else 'en'} presente"

    for i in range(len(spans) - 1):
        lang, txt, off = spans[i]
        nxt = spans[i + 1]
        if nxt[0] == lang:                      # par nao formado
            r['orfos'] += 1
            r['problemas'].append({
                'tipo': 'ORFAO', 'lang': lang, 'offset': off,
                'texto': txt[:90], 'proximo_lang': nxt[0],
                'proximo': nxt[1][:60],
            })
            continue
        # par formado: checa se os dois idiomas são realmente equivalentes
        a, b = normalise(txt), normalise(nxt[1])
        if a and b:
            # IGUAL: so conta texto de verdade (ver is_language_neutral) e longo
            if a == b and long_enough(txt) and not is_language_neutral(txt):
                # PT==EN so e defeito quando o texto e prosa/citacao
                # biblica. Se e referencia bibliografica ou credito de imagem,
                # a identidade entre os idiomas e a convencao do repo.
                if is_neutral_pair(txt):
                    r['neutros'] = r.get('neutros', 0) + 1
                else:
                    r['iguais'] += 1
                    r['problemas'].append({
                        'tipo': 'PT_NAO_TRADUZIDO' if lang == 'pt' else 'EN_NAO_TRADUZIDO',
                        'lang': lang, 'offset': off,
                        'texto': txt[:90], 'proximo_lang': nxt[0],
                        'proximo': nxt[1][:90],
                    })
            elif long_enough(txt) and not is_neutral_pair(txt):
                # idioma errado: exige texto longo E sinal forte do outro
                # idioma (>5 marcadores) E ausencia do proprio idioma
                if lang == 'pt' and not is_language_neutral(txt):
                    if len(EN_MARKERS.findall(txt)) >= 5 and len(PT_MARKERS.findall(txt)) == 0:
                        r['idioma_errado'] += 1
                        r['problemas'].append({
                            'tipo': 'PT_ESTA_EM_INGLES', 'lang': 'pt',
                            'offset': off, 'texto': txt[:90],
                            'proximo_lang': nxt[0], 'proximo': nxt[1][:60]})
                if lang == 'en' and not is_language_neutral(txt):
                    if len(PT_MARKERS.findall(txt)) >= 5 and len(EN_MARKERS.findall(txt)) == 0:
                        r['idioma_errado'] += 1
                        r['problemas'].append({
                            'tipo': 'EN_ESTA_EM_PORTUGUES', 'lang': 'en',
                            'offset': off, 'texto': txt[:90],
                            'proximo_lang': nxt[0], 'proximo': nxt[1][:60]})
    return r, spans


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('courses', nargs='*')
    ap.add_argument('--details', action='store_true')
    ap.add_argument('--json', default=os.path.join(REPO, 'bots/state/parity.json'))
    a = ap.parse_args()

    courses = a.courses or sorted(
        d for d in os.listdir(REPO)
        if os.path.isdir(os.path.join(REPO, d))
        and glob.glob(os.path.join(REPO, d, 'modulo-*', 'sessao-*.html'))
    )

    out = {}
    grand = Counter()
    print(f"{'CURSO':22}{'sess':>5}{'pt':>7}{'en':>7}{'ORFAO':>7}{'IGUAL':>7}{'IDIOMA':>8}{'SEM':>6}")
    for course in courses:
        files = sorted(glob.glob(os.path.join(REPO, course, 'modulo-*', 'sessao-*.html')),
                       key=lambda p: (len(p), p))
        if not files:
            continue
        cres = {}
        ctot = Counter()
        for f in files:
            r, _ = audit_file(f)
            rel = os.path.relpath(f, REPO)
            cres[rel] = r
            for k in ('pt', 'en', 'orfos', 'iguais', 'idioma_errado', 'neutros'):
                ctot[k] += r.get(k, 0)
            ctot['sess'] += 1
            if r.get('sem_idioma'):
                ctot['sem'] += 1
        out[course] = cres
        grand.update(ctot)
        flag = '' if not (ctot['orfos'] or ctot['iguais'] or ctot['idioma_errado'] or ctot['sem']) else '  <--'
        print(f"{course:22}{ctot['sess']:>5}{ctot['pt']:>7}{ctot['en']:>7}"
              f"{ctot['orfos']:>7}{ctot['iguais']:>7}{ctot['idioma_errado']:>8}{ctot['sem']:>6}{flag}")

        if a.details:
            for rel, r in sorted(cres.items()):
                if not r['problemas'] and not r.get('sem_idioma'):
                    continue
                print(f"\n  {rel}")
                if r.get('sem_idioma'):
                    print(f"      SEM_IDIOMA: {r['sem_idioma']}")
                for p in r['problemas'][:6]:
                    print(f"      {p['tipo']:18s} {p['lang']}: {p['texto']!r}")
                    print(f"      {'':18s} -> {p['proximo_lang']}: {p['proximo']!r}")

    # mesmo cuidado: escopo nao pode sobrescrever o resultado completo
    dest = a.json if not a.courses else a.json.replace('.json', '.' + '-'.join(a.courses) + '.json')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)

    print(f"\n{'=' * 70}")
    print(f"sessoes: {grand['sess']}  pares orfaos: {grand['orfos']}  "
          f"PT==EN: {grand['iguais']}  idioma errado: {grand['idioma_errado']}  "
          f"sem idioma: {grand['sem']}")
    print(f"Escrito {os.path.relpath(dest, REPO)}")
    if a.courses:
        print(f"(escopo: o completo continua em {os.path.relpath(a.json, REPO)})")
    return 0


if __name__ == '__main__':
    sys.exit(main())