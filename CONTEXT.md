# CONTEXT.md — visão geral do projeto

## O que é
Portal de estudos bíblicos bilíngues (PT/EN) no estilo The Bible Project
(anotações de aula do Dr. Tim Mackie). Conteúdo é gerado a partir de PDFs de
"teacher notes" e reconstruído como páginas HTML estáticas.

## Arquitetura
- **Site estático**, zero build de runtime. Tailwind via CDN
  (`@tailwindcss/browser@4` ou `cdn.tailwindcss.com`) + `<style>` por sessão.
- **Raiz**: `index.html` = grid de cursos (array `COURSES` em JS, `data-i18n`).
- **Curso** = pasta topo (`abraao/`, `ephesians/`, `1-corinthians/`,
  `jacob/`, `jonah/`, `joseph/`, `ezekiel/`, `messianic-torah/`,
  `noah-to-abraham/`, `adam-to-noah/`, `heaven-and-earth/`, `intro-hebrew-bible/`,
  `art-of-biblical-words/`, `rise-of-the-messiah/`, `exodus-overview/`,
  `atos-dos-apostolos/`).
- **Sessão** = `curso/modulo-N/sessao-N.html`. Módulos 1–3 e 4 (16+) por curso.
- **JS compartilhado** por curso: `curso/js/verse-modal.js` (modal de
  versículos/scripture, toggle PT/EN, progresso de leitura).

## Tokens de design
`DESIGN.md` define paleta + tipografia (frontmatter YAML). Cores primárias:
`primary #0284c7`, `ink #1a1a1a`, `body #24262a`. Tipografia: Inter (UI) +
Newsreader (serif) + SBL Hebrew (hebraico). Não invente cores — use os tokens.

## Ferramentas de apoio (Python)
- `build_course_session.py` — gera/Rebuild de sessão a partir de PDF.
- `build_exo_sessao8.py`, `exodus-overview/build_sessao7.py` — builders específicos.
- `check_session_coverage.py` — validação de completude (ver `SESSAO_CHECKLIST.md`).
- `scan_design_deviations.py` + `DESVIOS-DESIGN.md` / `desvios-design.json` —
  varredura de desvios de design entre sessões.
- `render_tables.py` — render de tabelas (algumas em imagem, ver
  `TABELAS-EM-IMAGEM.md`, `IMAGE-TABLES-INVENTORY.md`).

## Estrutura de conteúdo por sessão
1. Header: `Voltar`/`Imprimir`, toggle PT/EN, `#reading-progress`, `verse-modal.js`.
2. Blocos bilíngues: todo conteúdo em `lang-pt` + `lang-en`.
3. Imagens vetoriais do PDF (diagramas BibleProject).
4. Citações no formato `Autor (AAAA). Título. Editora.`

## Deploy
GitHub Pages, `.github/workflows/static.yml`: push em `main` faz upload do
repo inteiro e publica. Sem pipeline de testes automatizada além do script de
coverage (manual).
