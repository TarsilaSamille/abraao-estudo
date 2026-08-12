# MEMORY.md — fatos duráveis do projeto

- **Tipo**: site estático bilíngue PT/EN (estilo BibleProject), GitHub Pages.
- **Stack**: HTML + Tailwind CDN + `<style>` por sessão; JS mínimo
  (`verse-modal.js` por curso); Python para build/validação. Sem framework.
- **Cursos** (pastas topo): abraao, ephesians, 1-corinthians, jacob, jonah,
  joseph, ezekiel, messianic-torah, noah-to-abraham, adam-to-noah,
  heaven-and-earth, intro-hebrew-bible, art-of-biblical-words,
  rise-of-the-messiah, exodus-overview, atos-dos-apostolos.
- **Módulo 4 canônico = `sessao-16.html`** (usuário reescreveu o CSS — fonte de
  verdade; não reestilizar).
- **Mapeamento PDF→sessão deslocado +1**: `sessao-1.pdf`=intro; N≥2 ⇒
  `sessao-(N+1).pdf` = Session N. (1 Cor: S12/S23 sem PDF.)
- **Navegação**: Módulos 1–3 → `Voltar`→`index.html` (nav byte-idêntico
  `sessao-15`); Módulo 4 (16+) → `Voltar`→`sessao-(NN-1).html`.
- **Idioma**: `localStorage` `sNN-lang`; `setLang('pt'|'en')`; CSS esconde
  `.lang-en`/`.lang-pt` via `html[lang]`.
- **Regra de ouro**: NUNCA editar CSS inline — só spans `lang-pt`/`lang-en`.
  DRY: editar `js/verse-modal.js` compartilhado, não duplicar inline.
- **Hebraico**: fonte `SBL Hebrew`; PDFs usam Arial Unicode
  (`/System/Library/Fonts/Supplemental/Arial Unicode.ttf`).
- **Imagens**: padrão `img/sessao-N/pK-vector.png` (vetoriais do PDF).
- **Validação**: `python3 check_session_coverage.py [curso]` (requer poppler).
  Critérios em `SESSAO_CHECKLIST.md`. PT-only falha critério 2 (sem EN do PDF).
- **Deploy**: push `main` → `.github/workflows/static.yml` publica Pages.
