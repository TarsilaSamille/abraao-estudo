# Desvios do DESIGN.md (padrão abraao)

Gerado por `scan_design_deviations.py`. 441 arquivos `sessao-*.html` escaneados.

## A. Conteúdo como imagem (DEVE ser HTML semântico)

- Arquivos com `<img>`: **202** de 441
- Imagens quebradas (src não existe): **57**
- Páginas completas como imagem (provavelmente redundantes): **0**
- SVGs (diagrama vetorial, OK): **24**
- Vetoriais PNG (diagrama ou tabela): **207**
- Outros PNG: **216**
- **Candidatos a tabela real** (detector de colunas >=3): **0**

### A.1 Candidatos a tabela (imagem deveria ser `<table class="md">`)

| Arquivo | src | existe | wrapper |
|---|---|---|---|

### A.2 Imagens quebradas (src ausente no disco)

| Arquivo | src |
|---|---|
| exodus-overview/modulo-1/sessao-3.html | modulo-1/img/sessao-3/diagram-page1.svg |
| exodus-overview/modulo-1/sessao-3.html | modulo-1/img/sessao-3/diagram-page2.svg |
| ezekiel/modulo-2/sessao-6.html | img/sessao-6/p1-vector.png |
| ezekiel/modulo-2/sessao-6.html | img/sessao-6/p3-vector.png |
| ezekiel/modulo-2/sessao-6.html | img/sessao-6/p4-vector.png |
| ezekiel/modulo-2/sessao-6.html | img/sessao-6/p6-vector.png |
| ezekiel/modulo-2/sessao-6.html | img/sessao-6/p7-vector.png |
| ezekiel/modulo-2/sessao-6.html | img/sessao-6/p8-vector.png |
| ezekiel/modulo-4/sessao-16.html | img/sessao-16/p12-ill.jpeg |
| ezekiel/modulo-4/sessao-17.html | img/sessao-17/p8-ill.jpeg |
| ezekiel/modulo-4/sessao-18.html | img/sessao-18/p4-ill.jpeg |
| ezekiel/modulo-5/sessao-19.html | img/sessao-19/p7-ill.jpeg |
| ezekiel/modulo-5/sessao-19.html | img/sessao-19/p8-ill.jpeg |
| ezekiel/modulo-5/sessao-20.html | img/sessao-20/p5-ill.jpeg |
| ezekiel/modulo-5/sessao-20.html | img/sessao-20/p6-ill.jpeg |
| ezekiel/modulo-5/sessao-21.html | img/sessao-21/p4-ill.jpeg |
| ezekiel/modulo-5/sessao-22.html | img/sessao-22/p4-ill.jpeg |
| ezekiel/modulo-5/sessao-23.html | img/sessao-23/p7-ill.jpeg |
| ezekiel/modulo-6/sessao-25.html | img/sessao-25/p2-ill.jpeg |
| ezekiel/modulo-6/sessao-25.html | img/sessao-25/p3-ill.jpeg |
| ezekiel/modulo-6/sessao-25.html | img/sessao-25/p4-ill.jpeg |
| ezekiel/modulo-6/sessao-25.html | img/sessao-25/p5-ill.jpeg |
| joseph/modulo-2/sessao-7.html | img/sessao-2/thematic-melody-flow.png |
| joseph/modulo-2/sessao-8.html | img/sessao-2/thematic-melody-flow.png |
| joseph/modulo-2/sessao-9.html | img/sessao-2/thematic-melody-flow.png |
| joseph/modulo-3/sessao-10.html | img/sessao-2/thematic-melody-flow.png |
| joseph/modulo-3/sessao-11.html | img/sessao-2/thematic-melody-flow.png |
| joseph/modulo-3/sessao-12.html | img/sessao-2/thematic-melody-flow.png |
| joseph/modulo-4/sessao-13.html | img/sessao-2/thematic-melody-flow.png |
| joseph/modulo-4/sessao-15.html | img/sessao-2/thematic-melody-flow.png |
| joseph/modulo-4/sessao-16.html | img/sessao-2/thematic-melody-flow.png |
| joseph/modulo-4/sessao-17.html | img/sessao-2/thematic-melody-flow.png |
| joseph/modulo-5/sessao-18.html | img/sessao-2/thematic-melody-flow.png |
| joseph/modulo-5/sessao-19.html | img/sessao-2/thematic-melody-flow.png |
| joseph/modulo-6/sessao-23.html | ../img/sessao-23/p1-vector.png |
| joseph/modulo-6/sessao-23.html | ../img/sessao-23/p2-vector.png |
| joseph/modulo-6/sessao-23.html | ../img/sessao-23/p3-vector.png |
| joseph/modulo-6/sessao-23.html | ../img/sessao-23/p4-vector.png |
| joseph/modulo-6/sessao-23.html | ../img/sessao-23/p5-vector.png |
| joseph/modulo-6/sessao-23.html | img/sessao-2/thematic-melody-flow.png |
| joseph/modulo-6/sessao-24.html | img/sessao-2/thematic-melody-flow.png |
| joseph/modulo-7/sessao-27.html | img/sessao-27/thematic-melody-flow.png |
| messianic-torah/modulo-2/sessao-6.html | img/sessao-6/p1-vector.png |
| messianic-torah/modulo-2/sessao-6.html | img/sessao-6/p2-vector.png |
| messianic-torah/modulo-3/sessao-13.html | img/sessao-13/p1-sermon.png |
| messianic-torah/modulo-3/sessao-13.html | img/sessao-13/p3-poem.png |
| messianic-torah/modulo-3/sessao-13.html | img/sessao-13/p4-case7.png |
| messianic-torah/modulo-3/sessao-13.html | img/sessao-13/p7-case8.png |
| messianic-torah/modulo-3/sessao-13.html | img/sessao-13/p12-fasting.png |
| messianic-torah/modulo-3/sessao-13.html | img/sessao-13/p16-treasure.png |
| messianic-torah/modulo-3/sessao-14.html | img/sessao-14/p3-langs.png |
| messianic-torah/modulo-3/sessao-15.html | img/sessao-15/p1-structure.png |
| messianic-torah/modulo-3/sessao-15.html | img/sessao-15/p3-love.png |
| messianic-torah/modulo-3/sessao-15.html | img/sessao-15/p4-wealth.png |
| messianic-torah/modulo-3/sessao-15.html | img/sessao-15/p14-mammon.png |
| messianic-torah/modulo-3/sessao-16.html | img/sessao-16/p0-worry.png |
| messianic-torah/modulo-3/sessao-16.html | img/sessao-16/p1-worry.png |

### A.3 Páginas completas como imagem (redundantes? verificar texto no HTML)

| Arquivo | src | existe | wrapper |
|---|---|---|---|

## B. Componentes obrigatórios ausentes (DESIGN.md)

Arquivos com componente faltando: **278**

| Arquivo | faltando |
|---|---|
| 1-corinthians/modulo-1/sessao-1.html | reading-progress, page-footer |
| 1-corinthians/modulo-1/sessao-2.html | reading-progress, page-footer |
| 1-corinthians/modulo-2/sessao-3.html | reading-progress, page-footer |
| 1-corinthians/modulo-2/sessao-4.html | reading-progress, page-footer |
| 1-corinthians/modulo-3/sessao-5.html | reading-progress, page-footer |
| 1-corinthians/modulo-3/sessao-6.html | reading-progress, page-footer |
| 1-corinthians/modulo-3/sessao-7.html | reading-progress, page-footer |
| 1-corinthians/modulo-4/sessao-10.html | reading-progress, page-footer |
| 1-corinthians/modulo-4/sessao-8.html | reading-progress, page-footer |
| 1-corinthians/modulo-4/sessao-9.html | reading-progress, page-footer |
| 1-corinthians/modulo-5/sessao-11.html | reading-progress, page-footer |
| 1-corinthians/modulo-5/sessao-12.html | reading-progress, page-footer |
| 1-corinthians/modulo-6/sessao-13.html | reading-progress, page-footer |
| 1-corinthians/modulo-6/sessao-14.html | reading-progress, page-footer |
| 1-corinthians/modulo-6/sessao-15.html | reading-progress, page-footer |
| 1-corinthians/modulo-7/sessao-16.html | reading-progress, page-footer |
| 1-corinthians/modulo-7/sessao-17.html | reading-progress, page-footer |
| 1-corinthians/modulo-7/sessao-18.html | reading-progress, page-footer |
| 1-corinthians/modulo-8/sessao-19.html | reading-progress, page-footer |
| 1-corinthians/modulo-8/sessao-20.html | reading-progress, page-footer |
| 1-corinthians/modulo-8/sessao-21.html | reading-progress, page-footer |
| 1-corinthians/modulo-8/sessao-22.html | reading-progress, page-footer |
| 1-corinthians/modulo-8/sessao-23.html | reading-progress, page-footer |
| art-of-biblical-words/modulo-1/sessao-1.html | page-footer |
| art-of-biblical-words/modulo-1/sessao-2.html | page-footer |
| art-of-biblical-words/modulo-1/sessao-3.html | page-footer |
| art-of-biblical-words/modulo-1/sessao-4.html | page-footer |
| art-of-biblical-words/modulo-1/sessao-5.html | page-footer |
| atos-dos-apostolos/modulo-1/sessao-1.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-2/sessao-2.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-2/sessao-3.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-2/sessao-4.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-2/sessao-5.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-2/sessao-6.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-2/sessao-7.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-3/sessao-10.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-3/sessao-11.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-3/sessao-12.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-3/sessao-8.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-3/sessao-9.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-4/sessao-13.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-4/sessao-14.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-4/sessao-15.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-4/sessao-16.html | reading-progress, page-footer |
| atos-dos-apostolos/modulo-4/sessao-17.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-4/sessao-18.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-4/sessao-19.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-4/sessao-20.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-5/sessao-21.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-5/sessao-22.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-5/sessao-23.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-5/sessao-24.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-5/sessao-25.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-5/sessao-26.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-5/sessao-27.html | reading-progress, page-footer, PT/EN toggle |
| atos-dos-apostolos/modulo-5/sessao-28.html | reading-progress, page-footer, PT/EN toggle |
| ephesians/modulo-1/sessao-1.html | reading-progress, page-footer |
| ephesians/modulo-1/sessao-2.html | reading-progress, page-footer |
| ephesians/modulo-1/sessao-3.html | reading-progress, page-footer |
| ephesians/modulo-1/sessao-4.html | reading-progress, page-footer |
| ephesians/modulo-10/sessao-28.html | reading-progress, page-footer |
| ephesians/modulo-10/sessao-29.html | reading-progress, page-footer |
| ephesians/modulo-10/sessao-30.html | reading-progress, page-footer |
| ephesians/modulo-10/sessao-31.html | reading-progress, page-footer |
| ephesians/modulo-11/sessao-32.html | reading-progress, page-footer |
| ephesians/modulo-11/sessao-33.html | reading-progress, page-footer |
| ephesians/modulo-11/sessao-34.html | reading-progress, page-footer |
| ephesians/modulo-11/sessao-35.html | reading-progress, page-footer |
| ephesians/modulo-2/sessao-5.html | reading-progress, page-footer |
| ephesians/modulo-2/sessao-6.html | reading-progress, page-footer |
| ephesians/modulo-2/sessao-7.html | reading-progress, page-footer |
| ephesians/modulo-3/sessao-8.html | reading-progress, page-footer |
| ephesians/modulo-3/sessao-9.html | reading-progress, page-footer |
| ephesians/modulo-4/sessao-10.html | reading-progress, page-footer |
| ephesians/modulo-4/sessao-11.html | reading-progress, page-footer |
| ephesians/modulo-4/sessao-12.html | reading-progress, page-footer |
| ephesians/modulo-5/sessao-13.html | reading-progress, page-footer |
| ephesians/modulo-5/sessao-14.html | reading-progress, page-footer |
| ephesians/modulo-5/sessao-15.html | reading-progress, page-footer |
| ephesians/modulo-6/sessao-16.html | reading-progress, page-footer |
| ephesians/modulo-6/sessao-17.html | reading-progress, page-footer |
| ephesians/modulo-6/sessao-18.html | reading-progress, page-footer |
| ephesians/modulo-7/sessao-19.html | reading-progress, page-footer |
| ephesians/modulo-7/sessao-20.html | reading-progress, page-footer |
| ephesians/modulo-7/sessao-21.html | reading-progress, page-footer |
| ephesians/modulo-8/sessao-22.html | reading-progress, page-footer |
| ephesians/modulo-8/sessao-23.html | reading-progress, page-footer |
| ephesians/modulo-9/sessao-24.html | reading-progress, page-footer |
| ephesians/modulo-9/sessao-25.html | reading-progress, page-footer |
| ephesians/modulo-9/sessao-26.html | reading-progress, page-footer |
| ephesians/modulo-9/sessao-27.html | reading-progress, page-footer |
| exodus-overview/modulo-1/sessao-1.html | page-footer |
| exodus-overview/modulo-1/sessao-2.html | page-footer |
| exodus-overview/modulo-1/sessao-3.html | page-footer |
| exodus-overview/modulo-1/sessao-4.html | page-footer |
| exodus-overview/modulo-1/sessao-5.html | page-footer |
| exodus-overview/modulo-1/sessao-6.html | page-footer |
| exodus-overview/modulo-2/sessao-10.html | page-footer |
| exodus-overview/modulo-2/sessao-11.html | page-footer |
| exodus-overview/modulo-2/sessao-12.html | page-footer |
| exodus-overview/modulo-2/sessao-13.html | page-footer |
| exodus-overview/modulo-2/sessao-14.html | page-footer |
| exodus-overview/modulo-2/sessao-7.html | page-footer |
| exodus-overview/modulo-2/sessao-8.html | page-footer |
| exodus-overview/modulo-2/sessao-9.html | page-footer |
| exodus-overview/modulo-3/sessao-15.html | page-footer |
| exodus-overview/modulo-3/sessao-16.html | page-footer |
| exodus-overview/modulo-3/sessao-17.html | page-footer |
| exodus-overview/modulo-3/sessao-18.html | page-footer |
| exodus-overview/modulo-3/sessao-19.html | page-footer |
| exodus-overview/modulo-3/sessao-20.html | page-footer |
| exodus-overview/modulo-3/sessao-21.html | page-footer |
| exodus-overview/modulo-3/sessao-22.html | page-footer |
| exodus-overview/modulo-4/sessao-23.html | page-footer |
| exodus-overview/modulo-4/sessao-24.html | page-footer |
| exodus-overview/modulo-4/sessao-25.html | page-footer |
| exodus-overview/modulo-4/sessao-26.html | page-footer |
| exodus-overview/modulo-4/sessao-27.html | page-footer |
| exodus-overview/modulo-4/sessao-28.html | page-footer |
| exodus-overview/modulo-5/sessao-29.html | page-footer |
| exodus-overview/modulo-5/sessao-30.html | page-footer |
| ezekiel/modulo-1/sessao-1.html | page-footer |
| ezekiel/modulo-1/sessao-2.html | page-footer |
| ezekiel/modulo-1/sessao-3.html | page-footer |
| ezekiel/modulo-1/sessao-4.html | page-footer |
| ezekiel/modulo-2/sessao-6.html | page-footer |
| ezekiel/modulo-2/sessao-9.html | page-footer |
| ezekiel/modulo-3/sessao-14.html | verse-modal.js |
| ezekiel/modulo-4/sessao-15.html | verse-modal.js |
| ezekiel/modulo-4/sessao-16.html | verse-modal.js |
| ezekiel/modulo-4/sessao-17.html | verse-modal.js |
| ezekiel/modulo-4/sessao-18.html | verse-modal.js |
| ezekiel/modulo-5/sessao-19.html | verse-modal.js |
| ezekiel/modulo-5/sessao-20.html | verse-modal.js |
| ezekiel/modulo-5/sessao-21.html | verse-modal.js |
| ezekiel/modulo-5/sessao-22.html | verse-modal.js |
| ezekiel/modulo-5/sessao-23.html | verse-modal.js |
| ezekiel/modulo-5/sessao-24.html | verse-modal.js |
| ezekiel/modulo-6/sessao-25.html | verse-modal.js |
| ezekiel/modulo-6/sessao-26.html | page-footer |
| ezekiel/modulo-6/sessao-27.html | page-footer |
| ezekiel/modulo-6/sessao-28.html | page-footer |
| jacob/modulo-1/sessao-1.html | page-footer |
| jacob/modulo-1/sessao-2.html | page-footer |
| jacob/modulo-1/sessao-3.html | page-footer |
| jacob/modulo-1/sessao-4.html | page-footer |
| jacob/modulo-1/sessao-5.html | page-footer |
| jacob/modulo-2/sessao-10.html | page-footer |
| jacob/modulo-2/sessao-11.html | page-footer |
| jacob/modulo-2/sessao-6.html | page-footer |
| jacob/modulo-2/sessao-7.html | page-footer |
| jacob/modulo-2/sessao-8.html | page-footer |
| jacob/modulo-2/sessao-9.html | page-footer |
| jacob/modulo-3/sessao-12.html | page-footer |
| jacob/modulo-3/sessao-13.html | page-footer |
| jacob/modulo-3/sessao-14.html | page-footer |
| jacob/modulo-3/sessao-15.html | page-footer |
| jacob/modulo-3/sessao-16.html | page-footer |
| jacob/modulo-4/sessao-17.html | page-footer |
| jacob/modulo-4/sessao-18.html | page-footer |
| jacob/modulo-4/sessao-19.html | page-footer |
| jacob/modulo-4/sessao-20.html | page-footer |
| jacob/modulo-5/sessao-21.html | page-footer |
| jacob/modulo-5/sessao-22.html | page-footer |
| jacob/modulo-5/sessao-23.html | page-footer |
| jacob/modulo-5/sessao-24.html | page-footer |
| jacob/modulo-5/sessao-25.html | page-footer |
| jacob/modulo-6/sessao-26.html | page-footer |
| jacob/modulo-6/sessao-27.html | page-footer |
| jacob/modulo-6/sessao-28.html | page-footer |
| jacob/modulo-6/sessao-29.html | page-footer |
| jonah/modulo-1/sessao-1.html | page-footer |
| jonah/modulo-1/sessao-2.html | page-footer |
| jonah/modulo-1/sessao-3.html | page-footer |
| jonah/modulo-1/sessao-4.html | page-footer |
| jonah/modulo-1/sessao-5.html | page-footer |
| jonah/modulo-2/sessao-6.html | page-footer |
| jonah/modulo-2/sessao-7.html | page-footer |
| jonah/modulo-2/sessao-8.html | page-footer |
| jonah/modulo-2/sessao-9.html | page-footer |
| jonah/modulo-3/sessao-10.html | page-footer |
| jonah/modulo-3/sessao-11.html | page-footer |
| jonah/modulo-3/sessao-12.html | page-footer |
| jonah/modulo-3/sessao-13.html | page-footer |
| jonah/modulo-3/sessao-14.html | page-footer |
| jonah/modulo-4/sessao-15.html | page-footer |
| jonah/modulo-4/sessao-16.html | page-footer |
| jonah/modulo-4/sessao-17.html | page-footer |
| jonah/modulo-4/sessao-18.html | page-footer |
| jonah/modulo-4/sessao-19.html | page-footer |
| jonah/modulo-4/sessao-20.html | page-footer |
| jonah/modulo-4/sessao-21.html | page-footer |
| jonah/modulo-5/sessao-22.html | page-footer |
| jonah/modulo-5/sessao-23.html | page-footer |
| jonah/modulo-5/sessao-24.html | page-footer |
| jonah/modulo-5/sessao-25.html | page-footer |
| jonah/modulo-5/sessao-26.html | page-footer |
| jonah/modulo-5/sessao-27.html | page-footer |
| jonah/modulo-5/sessao-28.html | page-footer |
| jonah/modulo-6/sessao-29.html | page-footer |
| jonah/modulo-6/sessao-30.html | page-footer |
| jonah/modulo-6/sessao-31.html | page-footer |
| jonah/modulo-6/sessao-32.html | page-footer |
| jonah/modulo-6/sessao-33.html | page-footer |
| jonah/modulo-6/sessao-34.html | page-footer |
| jonah/modulo-6/sessao-35.html | page-footer |
| jonah/modulo-7/sessao-36.html | page-footer |
| jonah/modulo-7/sessao-37.html | page-footer |
| jonah/modulo-7/sessao-38.html | page-footer |
| jonah/modulo-7/sessao-39.html | page-footer |
| jonah/modulo-8/sessao-40.html | page-footer |
| jonah/modulo-8/sessao-41.html | page-footer |
| jonah/modulo-8/sessao-42.html | page-footer |
| jonah/modulo-8/sessao-43.html | page-footer |
| jonah/modulo-8/sessao-44.html | page-footer |
| jonah/modulo-8/sessao-45.html | page-footer |
| joseph/modulo-1/sessao-1.html | page-footer |
| joseph/modulo-1/sessao-2.html | page-footer |
| joseph/modulo-1/sessao-3.html | page-footer |
| joseph/modulo-1/sessao-4.html | page-footer |
| joseph/modulo-2/sessao-5.html | page-footer |
| joseph/modulo-2/sessao-6.html | page-footer |
| joseph/modulo-2/sessao-7.html | page-footer |
| joseph/modulo-2/sessao-8.html | page-footer |
| joseph/modulo-2/sessao-9.html | page-footer |
| joseph/modulo-3/sessao-10.html | page-footer |
| joseph/modulo-3/sessao-11.html | page-footer |
| joseph/modulo-3/sessao-12.html | page-footer |
| joseph/modulo-4/sessao-13.html | page-footer |
| joseph/modulo-4/sessao-14.html | page-footer |
| joseph/modulo-4/sessao-15.html | page-footer |
| joseph/modulo-4/sessao-16.html | page-footer |
| joseph/modulo-4/sessao-17.html | page-footer |
| joseph/modulo-5/sessao-18.html | page-footer |
| joseph/modulo-5/sessao-19.html | page-footer |
| joseph/modulo-5/sessao-20.html | page-footer |
| joseph/modulo-6/sessao-21.html | page-footer |
| joseph/modulo-6/sessao-22.html | page-footer |
| joseph/modulo-6/sessao-23.html | page-footer |
| joseph/modulo-6/sessao-24.html | page-footer |
| joseph/modulo-6/sessao-25.html | page-footer |
| joseph/modulo-7/sessao-26.html | page-footer |
| joseph/modulo-7/sessao-27.html | page-footer |
| joseph/modulo-7/sessao-28.html | page-footer |
| joseph/modulo-7/sessao-29.html | page-footer |
| messianic-torah/modulo-1/sessao-1.html | page-footer |
| messianic-torah/modulo-1/sessao-2.html | page-footer |
| messianic-torah/modulo-1/sessao-3.html | page-footer |
| messianic-torah/modulo-1/sessao-4.html | page-footer |
| messianic-torah/modulo-1/sessao-5.html | page-footer |
| messianic-torah/modulo-2/sessao-10.html | page-footer |
| messianic-torah/modulo-2/sessao-11.html | page-footer |
| messianic-torah/modulo-2/sessao-12.html | page-footer |
| messianic-torah/modulo-2/sessao-6.html | page-footer |
| messianic-torah/modulo-2/sessao-7.html | page-footer |
| messianic-torah/modulo-2/sessao-8.html | page-footer |
| messianic-torah/modulo-2/sessao-9.html | page-footer |
| messianic-torah/modulo-3/sessao-13.html | page-footer |
| messianic-torah/modulo-3/sessao-14.html | page-footer |
| messianic-torah/modulo-3/sessao-15.html | page-footer |
| messianic-torah/modulo-3/sessao-16.html | page-footer |
| messianic-torah/modulo-3/sessao-17.html | page-footer |
| rise-of-the-messiah/modulo-1/sessao-1.html | page-footer |
| rise-of-the-messiah/modulo-1/sessao-2.html | page-footer |
| rise-of-the-messiah/modulo-1/sessao-3.html | page-footer |
| rise-of-the-messiah/modulo-1/sessao-4.html | page-footer |
| rise-of-the-messiah/modulo-2/sessao-10.html | page-footer |
| rise-of-the-messiah/modulo-2/sessao-5.html | page-footer |
| rise-of-the-messiah/modulo-2/sessao-6.html | page-footer |
| rise-of-the-messiah/modulo-2/sessao-7.html | page-footer |
| rise-of-the-messiah/modulo-2/sessao-8.html | page-footer |
| rise-of-the-messiah/modulo-2/sessao-9.html | page-footer |
| rise-of-the-messiah/modulo-3/sessao-11.html | page-footer |
| rise-of-the-messiah/modulo-3/sessao-12.html | page-footer |
| rise-of-the-messiah/modulo-3/sessao-13.html | page-footer |
| rise-of-the-messiah/modulo-3/sessao-14.html | page-footer |
| rise-of-the-messiah/modulo-3/sessao-15.html | page-footer |
| rise-of-the-messiah/modulo-3/sessao-16.html | page-footer |

## C. Resumo

- Arquivos 100% sem `<img>` (compatíveis com padrão abraao): **239**
- Arquivos com algum `<img>`: **202**

> Nota: SVG/diagramas vetoriais são legítimos no design. Tabelas em imagem e
> páginas completas como imagem são os desvios reais a corrigir.
> `is_table` usa detector determinístico (>=3 separadores verticais >=40% altura).