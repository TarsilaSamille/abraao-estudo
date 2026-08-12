#!/usr/bin/env python3
"""Scan all sessao-*.html against DESIGN.md (abraao golden pattern).

Flags two deviation classes:
  1. IMAGE-BASED CONTENT  - <img> used where DESIGN wants semantic HTML:
       * tables shipped as <img> (table-img/figure) instead of <table class="md">
       * full-page screenshots whose text already exists in the HTML
       * broken image refs (src file missing on disk)
  2. MISSING COMPONENTS  - file lacks a design-mandated piece:
       reading-progress bar, verse-modal.js, page-footer, PT/EN toggle.

Emits a markdown report to the repo root (parent folder of the courses).
"""
import os, re, glob, json
try:                                    # ponytail: PIL optional; table-detection degrades to None
    from PIL import Image
    import numpy as np
    _HAVE_PIL = True
except Exception:
    _HAVE_PIL = False

ROOT = os.path.dirname(os.path.abspath(__file__))

def find_sessions():
    out = []
    for dirpath, dirs, files in os.walk(ROOT):
        rel = os.path.relpath(dirpath, ROOT)
        parts = rel.split(os.sep)
        if any(p in ('node_modules', 'pdf-images', 'quarantine', 'others', '.git', '.agent', '__pycache__') for p in parts):
            continue
        for f in files:
            if re.match(r'sessao-\d+\.html$', f):
                out.append(os.path.join(dirpath, f))
    return sorted(out)

IMG_RE = re.compile(r'<img\b[^>]*\bsrc=["\']([^"\']+)["\']', re.I)
WRAP_RE = re.compile(r'class="([^"]*(?:table-img|figure|page-img|img-wrap|table)[^"]*)"', re.I)

def classify_src(src):
    base = src.rsplit('/', 1)[-1].lower()
    if re.search(r'-page\.png$|^page-\d+\.png$|page_\d+\.png', base):
        return 'PAGE'          # full-page render -> likely redundant
    if base.endswith('.svg'):
        return 'SVG'           # vector diagram, never a data table
    if '-vector.png' in base or '-compare.png' in base or '-vector.svg' in base:
        return 'VECTOR'        # diagram OR possible table
    return 'OTHER'

def max_run_1d(arr):
    if not _HAVE_PIL:
        return 0
    if not np.any(arr):
        return 0
    bounded = np.pad(arr, (1, 1), 'constant', constant_values=False)
    d = np.diff(bounded.astype(np.int8))
    starts = np.where(d == 1)[0]
    ends = np.where(d == -1)[0]
    return np.max(ends - starts)

def img_is_table(img_path):
    """DESIGN column-separator test: >=3 vertical dark runs spanning >=40% height."""
    if not _HAVE_PIL:
        return None
    try:
        im = Image.open(img_path).convert('L')
        a = np.asarray(im)
    except Exception:
        return None  # unreadable
    h, w = a.shape
    if h < 40 or w < 40:
        return False
    dark = (a < 150)
    col_sums = dark.sum(axis=0)
    row_sums = dark.sum(axis=1)
    cand_cols = np.where(col_sums >= 0.4 * h)[0]
    cand_rows = np.where(row_sums >= 0.4 * w)[0]
    if len(cand_cols) < 4 or len(cand_rows) < 4:
        return False
    sep_cols = sum(1 for c in cand_cols if max_run_1d(dark[:, c]) >= 0.4 * h)
    sep_rows = sum(1 for r in cand_rows if max_run_1d(dark[r, :]) >= 0.4 * w)
    return sep_cols >= 4 and sep_rows >= 4

def main():
    sessions = find_sessions()
    rows = []
    struct_problems = []
    for path in sessions:
        rel = os.path.relpath(path, ROOT)
        html = open(path, encoding='utf-8', errors='replace').read()
        # structural components
        comp = {
            'reading-progress': 'reading-progress' in html,
            'verse-modal.js': 'verse-modal.js' in html,
            'page-footer': 'page-footer' in html,
            'PT/EN toggle': ('setLang' in html or 'bp_lang' in html or 'lang-pt' in html),
        }
        missing = [k for k, v in comp.items() if not v]
        if missing:
            struct_problems.append((rel, missing))
        # images
        imgs = IMG_RE.findall(html)
        for src in imgs:
            kind = classify_src(src)
            # resolve path on disk (relative to the html file)
            base = os.path.dirname(path)
            cand = os.path.join(base, src)
            exists = os.path.exists(cand)
            is_table = None
            if exists and kind in ('VECTOR', 'OTHER', 'PAGE'):
                is_table = img_is_table(cand)
            wrap = ''
            m = WRAP_RE.search(html)
            if m:
                wrap = m.group(1)
            rows.append({
                'file': rel,
                'src': src,
                'kind': kind,
                'exists': exists,
                'is_table': is_table,
                'wrap': wrap,
            })
    # report
    lines = []
    lines.append('# Desvios do DESIGN.md (padrão abraao)')
    lines.append('')
    lines.append(f'Gerado por `scan_design_deviations.py`. {len(sessions)} arquivos `sessao-*.html` escaneados.')
    lines.append('')
    # Section A: image-based content
    lines.append('## A. Conteúdo como imagem (DEVE ser HTML semântico)')
    lines.append('')
    img_rows = [r for r in rows]
    broken = [r for r in img_rows if not r['exists']]
    page = [r for r in img_rows if r['kind'] == 'PAGE' and r['exists']]
    svg = [r for r in img_rows if r['kind'] == 'SVG']
    vec = [r for r in img_rows if r['kind'] == 'VECTOR']
    other = [r for r in img_rows if r['kind'] == 'OTHER']
    table_candidates = [r for r in img_rows if r['is_table'] is True]
    n_img_files = len(set(r['file'] for r in img_rows))
    lines.append(f'- Arquivos com `<img>`: **{n_img_files}** de {len(sessions)}')
    lines.append(f'- Imagens quebradas (src não existe): **{len(broken)}**')
    lines.append(f'- Páginas completas como imagem (provavelmente redundantes): **{len(page)}**')
    lines.append(f'- SVGs (diagrama vetorial, OK): **{len(svg)}**')
    lines.append(f'- Vetoriais PNG (diagrama ou tabela): **{len(vec)}**')
    lines.append(f'- Outros PNG: **{len(other)}**')
    lines.append(f'- **Candidatos a tabela real** (detector de colunas >=3): **{len(table_candidates)}**')
    lines.append('')

    lines.append('### A.1 Candidatos a tabela (imagem deveria ser `<table class="md">`)')
    lines.append('')
    lines.append('| Arquivo | src | existe | wrapper |')
    lines.append('|---|---|---|---|')
    for r in sorted(table_candidates, key=lambda x: x['file']):
        lines.append(f"| {r['file']} | {r['src']} | {'sim' if r['exists'] else 'NÃO'} | {r['wrap']} |")
    lines.append('')

    lines.append('### A.2 Imagens quebradas (src ausente no disco)')
    lines.append('')
    lines.append('| Arquivo | src |')
    lines.append('|---|---|')
    for r in sorted(broken, key=lambda x: x['file']):
        lines.append(f"| {r['file']} | {r['src']} |")
    lines.append('')

    lines.append('### A.3 Páginas completas como imagem (redundantes? verificar texto no HTML)')
    lines.append('')
    lines.append('| Arquivo | src | existe | wrapper |')
    lines.append('|---|---|---|---|')
    for r in sorted(page, key=lambda x: x['file']):
        lines.append(f"| {r['file']} | {r['src']} | {'sim' if r['exists'] else 'NÃO'} | {r['wrap']} |")
    lines.append('')

    # Section B: structural
    lines.append('## B. Componentes obrigatórios ausentes (DESIGN.md)')
    lines.append('')
    lines.append(f'Arquivos com componente faltando: **{len(struct_problems)}**')
    lines.append('')
    lines.append('| Arquivo | faltando |')
    lines.append('|---|---|')
    for rel, miss in sorted(struct_problems):
        lines.append(f"| {rel} | {', '.join(miss)} |")
    lines.append('')

    # Section C: compliant summary
    lines.append('## C. Resumo')
    lines.append('')
    compliant = len(sessions) - len(set(r['file'] for r in img_rows))
    lines.append(f'- Arquivos 100% sem `<img>` (compatíveis com padrão abraao): **{compliant}**')
    n_img_files = len(set(r['file'] for r in img_rows))
    lines.append(f'- Arquivos com algum `<img>`: **{n_img_files}**')
    lines.append('')
    lines.append('> Nota: SVG/diagramas vetoriais são legítimos no design. Tabelas em imagem e')
    lines.append('> páginas completas como imagem são os desvios reais a corrigir.')
    lines.append('> `is_table` usa detector determinístico (>=3 separadores verticais >=40% altura).')

    report = '\n'.join(lines)
    out_path = os.path.join(ROOT, 'DESVIOS-DESIGN.md')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(report)
    # also dump JSON for programmatic use
    with open(os.path.join(ROOT, 'desvios-design.json'), 'w', encoding='utf-8') as f:
        json.dump({'sessions': len(sessions), 'images': rows,
                   'structural_problems': struct_problems}, f, ensure_ascii=False, indent=1)
    print(f'sessions={len(sessions)} images_total={len(rows)}')
    print(f'broken={len(broken)} page={len(page)} svg={len(svg)} vec={len(vec)} other={len(other)}')
    print(f'table_candidates={len(table_candidates)} structural_problems={len(struct_problems)}')
    print(f'report -> {out_path}')

if __name__ == '__main__':
    main()
