# SKILLS.md — workflows reutilizáveis

Skills do Hermes (em `~/.hermes/skills/`) relevantes para este repo:
- `biblia-estudo-sessoes-html` — construir/checar `sessao-N.html` em qualquer curso.
- `biblia-sessoes-fill` — preencher/reparar sessões 1 Cor bilíngues a partir de PDFs.
- `abraao-session-html` — sessões PT fiéis estilo BibleProject (curso Abraão).
- `bible-study-session-html` — rebuild de sessão BibleProject a partir de PDF.
- `bible-skip` — salmos SBB → PDFs hebraico+português.
- `hebrew-pdf-rendering` — render de hebraico+niqqud em PDF.
- `parallel-corpus-webapp` / `web-development` — app Next.js de corpus paralelo
  (repo irmão `parallel-corpus-`).

## Workflows locais (repo)
**Nova/refill sessão a partir de PDF**
1. Localizar PDF fonte (`curso/pdf-sessoes/sessao-(N+1).pdf`, mapeamento +1).
2. `python3 check_session_coverage.py curso` para baseline.
3. Rodar builder (`build_course_session.py` ou específico).
4. Re-validar com `check_session_coverage.py`.

**Checar desvios de design**
`python3 scan_design_deviations.py` → `DESVIOS-DESIGN.md` / `desvios-design.json`.

**Preview local**
Servir pasta com qualquer static server (ex.: `python3 -m http.server`) e abrir
`index.html`. Não há dev server dedicado.

**Deploy**
Push em `main` → GitHub Actions publica em Pages automaticamente. Sem passos manuais.

## Convenções de edição (ver AGENTS.md)
Só spans `lang-pt`/`lang-en`; não mexer em CSS; `verse-modal.js` compartilhado;
nav byte-idêntico em módulos 1–3.
