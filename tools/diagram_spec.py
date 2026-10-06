#!/usr/bin/env python3
"""Extrai a especificacao de um diagrama do PDF, para reconstruir em HTML/CSS.

Os diagramas do BibleProject tem sempre a mesma anatomia: um ou mais paineis
externos com moldura, cada um com uma pílula de etiqueta, e dentro deles
sub-paineis (a / b / a' / "Genesis 37a" ...) com as suas proprias caixas e
baloes.

Este script le o vetor do PDF e imprime a arvore, ja com:
  - cores de preenchimento e de traco, e opacidade
  - o texto de cada pílula (a pílula e o retangulo colorido; o texto é branco)
  - as linhas de conteudo, com a cor de cada trecho

REGRA IMPORTANTE: o atributo `fill` do PyMuPDF mente em path so-tracejado.
Um painel aparece com fill #3e4054 quando na verdade so tem o traco e o
interior e branco. Use `--pixel` para confirmar por raster antes de escrever
o CSS.

Uso:
    python3 tools/diagram_spec.py <curso> <N>            # todas as paginas
    python3 tools/diagram_spec.py <curso> <N> --page 1   # so uma pagina
    python3 tools/diagram_spec.py <curso> <N> --pixel    # confirma fills por pixel
"""
import argparse
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOID_HINT = 12.0


def hexof(r):
    return "#%02x%02x%02x" % tuple(int(round(c * 255)) for c in r)


def load(course, n):
    import fitz
    p = os.path.join(REPO, course, 'pdf-sessoes', f'sessao-{n}.pdf')
    if not os.path.exists(p):
        sys.exit(f"PDF nao encontrado: {p}")
    return fitz.open(p)


def boxes(page):
    """Retangulos grandes: molduras de painel, sub-painel, pilula e barra."""
    out = []
    for d in page.get_drawings():
        r = d['rect']
        if r.width < 40 or r.height < VOID_HINT:
            continue
        if r.width > 545 and r.height > 700:      # fundo da pagina
            continue
        out.append(d)
    return out


def texts(page, y0=None, y1=None):
    out = []
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for s in l.get('spans', []):
                t = s['text'].strip()
                if not t:
                    continue
                bb = s['bbox']
                if y0 is not None and (bb[1] < y0 - 2 or bb[3] > y1 + 2):
                    continue
                out.append((bb, '#%06x' % (s['color'] & 0xFFFFFF), round(s['size'], 1), t))
    out.sort(key=lambda x: (round(x[0][1], 1), x[0][0]))
    return out


def pixel_confirm(doc, page_no, pts):
    page = doc[page_no]
    pix = page.get_pixmap(dpi=170)
    s = 170 / 72.0
    print(f"  -- pixel pagina {page_no+1} --")
    for label, (x, y) in pts:
        q = pix.pixel(int(round(x * s)), int(round(y * s)))
        print(f"     {label:34s} ({x:.0f},{y:.0f}) = #{q[0]:02x}{q[1]:02x}{q[2]:02x}")


def group_lines(spans, tol=3.0):
    """Junta spans da mesma linha visual.

    Os spans de uma etiqueta sao fatias separadas ("Act", "1—", "Genesis",
    "37:2-41:57") e cada uma tem um bbox com o topo 0.1-0.5pt diferente.
    Ordenar so por y embaralha a etiqueta; agrupar por faixa de y devolve a
    ordem de leitura.
    """
    lines = []
    for bb, c, sz, t in sorted(spans, key=lambda x: (x[0][1], x[0][0])):
        placed = False
        for ln in lines:
            if abs(ln['y'] - bb[1]) <= tol:
                ln['items'].append((bb[0], t, c))
                ln['y'] = (ln['y'] + bb[1]) / 2
                placed = True
                break
        if not placed:
            lines.append({'y': bb[1], 'items': [(bb[0], t, c)]})
    for ln in lines:
        ln['items'].sort(key=lambda x: x[0])
        ln['text'] = ' '.join(t for _, t, _ in ln['items'])
        ln['color'] = ln['items'][0][2]
    return sorted(lines, key=lambda l: l['y'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('course')
    ap.add_argument('n', type=int)
    ap.add_argument('--page', type=int)
    ap.add_argument('--pixel', action='store_true')
    a = ap.parse_args()

    doc = load(a.course, a.n)
    pages = range(doc.page_count) if not a.page else [a.page - 1]
    confirm = []

    for pi in pages:
        page = doc[pi]
        bs = boxes(page)
        if not bs:
            continue
        print(f"\n{'=' * 74}\n{a.course}/sessao-{a.n}  PAGINA {pi+1}/{doc.page_count}\n{'=' * 74}")
        for d in bs:
            r = d['rect']
            f = hexof(d['fill']) if d.get('fill') else '-'
            s = hexof(d['color']) if d.get('color') else '-'
            kind = 'PAINEL/SUB' if r.width > 300 else 'PILULA/BARRA'
            print(f"\n  [{kind}] ({r.x0:.1f},{r.y0:.1f})-({r.x1:.1f},{r.y1:.1f}) "
                  f"w={r.width:.0f} h={r.height:.0f}")
            print(f"      fill={f} a {d.get('fill_opacity')} | stroke={s} lw={d.get('width')}")
            # texto branco sobre a caixa => e a pilula
            if r.height <= 30:
                sp = [(bb, c, sz, t) for bb, c, sz, t
                      in texts(page, r.y0 - 3, r.y0 + r.height + 3) if c == '#ffffff']
                if sp:
                    print(f"      etiqueta: {group_lines(sp)[0]['text']}")
            # amostra para confirmar por pixel
            if r.width > 100 and r.height > 20:
                confirm.append((f"({r.x0:.0f},{r.y0:.0f}) {f}",
                                ((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)))

        print("\n  --- conteudo (por linha) ---")
        for ln in group_lines(texts(page)):
            print(f"    y={ln['y']:6.1f} {ln['color']} | {ln['text'][:92]}")

    if a.page is not None or a.pixel:
        pass
    if confirm:
        print("\n" + "=" * 74)
        print("CONFIRME OS FILLS POR PIXEL (o `fill` acima mente em path so-tracejado):")
        pixel_confirm(doc, pages[0] if not a.page else a.page - 1, confirm[:10])
    doc.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())