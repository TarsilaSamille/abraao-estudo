# Desvios do DESIGN.md (padrão abraao)

Gerado por `scan_design_deviations.py`. 442 arquivos `sessao-*.html` escaneados.

## A. Conteúdo como imagem (DEVE ser HTML semântico)

- Arquivos com `<img>`: **133** de 442
- Imagens quebradas (src não existe): **0**
- Páginas completas como imagem (provavelmente redundantes): **15**
- SVGs (diagrama vetorial, OK): **0**
- Vetoriais PNG (diagrama ou tabela): **1**
- Outros PNG: **225**
- **Candidatos a tabela real** (detector de colunas >=3): **53**

### A.1 Candidatos a tabela (imagem deveria ser `<table class="md">`)

| Arquivo | src | existe | wrapper |
|---|---|---|---|
| adam-to-noah/modulo-1/sessao-1.html | img/sessao-1/page-1.jpg | sim |  |
| adam-to-noah/modulo-1/sessao-2.html | img/sessao-2/page-1.jpg | sim |  |
| adam-to-noah/modulo-1/sessao-3.html | img/sessao-3/page-1.jpg | sim |  |
| adam-to-noah/modulo-1/sessao-4.html | img/sessao-4/page-2.jpg | sim |  |
| adam-to-noah/modulo-2/sessao-12.html | img/sessao-12/page-2.jpg | sim |  |
| adam-to-noah/modulo-2/sessao-12.html | img/sessao-12/page-5.jpg | sim |  |
| adam-to-noah/modulo-6/sessao-30.html | img/sessao-30/page-1.jpg | sim |  |
| adam-to-noah/modulo-6/sessao-30.html | img/sessao-30/page-2.jpg | sim |  |
| ephesians/modulo-9/sessao-24.html | img/sessao-24/illu-001-000.jpg | sim |  |
| ephesians/modulo-9/sessao-24.html | img/sessao-24/illu-001-001.jpg | sim |  |
| exodus-overview/modulo-1/sessao-5.html | img/sessao-5/page-1.jpg | sim |  |
| exodus-overview/modulo-2/sessao-7.html | img/sessao-7/page-1.jpg | sim |  |
| exodus-overview/modulo-2/sessao-7.html | img/sessao-7/page-2.jpg | sim |  |
| exodus-overview/modulo-2/sessao-9.html | img/sessao-9/page-1.jpg | sim | table-img reveal |
| exodus-overview/modulo-4/sessao-25.html | img/sessao-25/page-1.jpg | sim |  |
| exodus-overview/modulo-4/sessao-25.html | img/sessao-25/page-2.jpg | sim |  |
| ezekiel/modulo-2/sessao-9.html | img/sessao-9/page-2.jpg | sim |  |
| ezekiel/modulo-4/sessao-16.html | img/sessao-16/page-1.jpg | sim | figure reveal |
| ezekiel/modulo-6/sessao-28.html | img/sessao-28/page-1.jpg | sim |  |
| heaven-and-earth/modulo-1/sessao-1.html | img/sessao-1/page-1.jpg | sim |  |
| heaven-and-earth/modulo-1/sessao-1.html | img/sessao-1/page-2.jpg | sim |  |
| heaven-and-earth/modulo-1/sessao-1.html | img/sessao-1/page-3.jpg | sim |  |
| heaven-and-earth/modulo-1/sessao-1.html | img/sessao-1/page-4.jpg | sim |  |
| heaven-and-earth/modulo-2/sessao-6.html | img/sessao-6/page-1.jpg | sim |  |
| heaven-and-earth/modulo-6/sessao-28.html | img/sessao-28/page-2.jpg | sim |  |
| heaven-and-earth/modulo-6/sessao-28.html | img/sessao-28/page-3.jpg | sim |  |
| heaven-and-earth/modulo-6/sessao-28.html | img/sessao-28/page-4.jpg | sim |  |
| intro-hebrew-bible/modulo-2/sessao-9.html | img/sessao-9/page-1.jpg | sim |  |
| intro-hebrew-bible/modulo-3/sessao-11.html | img/sessao-11/page-1.jpg | sim |  |
| intro-hebrew-bible/modulo-3/sessao-12.html | img/sessao-12/page-1.jpg | sim |  |
| intro-hebrew-bible/modulo-3/sessao-12.html | img/sessao-12/page-2.jpg | sim |  |
| intro-hebrew-bible/modulo-4/sessao-18.html | img/sessao-18/page-1.jpg | sim | figure reveal |
| intro-hebrew-bible/modulo-4/sessao-18.html | img/sessao-18/page-2.jpg | sim | figure reveal |
| intro-hebrew-bible/modulo-5/sessao-22.html | img/sessao-22/page-2.jpg | sim | figure reveal |
| intro-hebrew-bible/modulo-5/sessao-23.html | img/sessao-23/page-2.jpg | sim |  |
| intro-hebrew-bible/modulo-5/sessao-27.html | img/sessao-27/page-1.jpg | sim |  |
| jacob/modulo-3/sessao-12.html | img/sessao-12/page-1.jpg | sim |  |
| jonah/modulo-4/sessao-15.html | img/sessao-15/page-1.jpg | sim |  |
| jonah/modulo-4/sessao-15.html | img/sessao-15/page-2.jpg | sim |  |
| jonah/modulo-6/sessao-29.html | img/sessao-29/page-4.jpg | sim |  |
| joseph/modulo-1/sessao-3.html | img/sessao-3/plants.png | sim | figure reveal my-4 |
| joseph/modulo-2/sessao-8.html | img/sessao-8/page-1.jpg | sim | doc-table-wrap reveal |
| joseph/modulo-6/sessao-25.html | img/sessao-25/illu-001-000.jpg | sim |  |
| messianic-torah/modulo-1/sessao-1.html | img/sessao-1/p2-img0.png | sim | table-img reveal |
| messianic-torah/modulo-3/sessao-13.html | img/sessao-13/page-1.png | sim | table-img reveal |
| messianic-torah/modulo-4/sessao-19.html | img/sessao-19/page-1.png | sim | table-img reveal |
| noah-to-abraham/modulo-1/sessao-2.html | img/sessao-2/page-7-01.png | sim |  |
| noah-to-abraham/modulo-1/sessao-2.html | img/sessao-2/page-8-01.png | sim |  |
| noah-to-abraham/modulo-2/sessao-10.html | img/sessao-10/page-66-01.png | sim |  |
| noah-to-abraham/modulo-4/sessao-17.html | img/sessao-17/page-115-01.png | sim |  |
| noah-to-abraham/modulo-4/sessao-19.html | img/sessao-19/page-132-01.png | sim |  |
| noah-to-abraham/modulo-5/sessao-27.html | img/sessao-27/page-195-01.png | sim |  |
| rise-of-the-messiah/modulo-1/sessao-1.html | ../image/priene-theater.jpg | sim |  |

### A.2 Imagens quebradas (src ausente no disco)

| Arquivo | src |
|---|---|

### A.3 Páginas completas como imagem (redundantes? verificar texto no HTML)

| Arquivo | src | existe | wrapper |
|---|---|---|---|
| 1-corinthians/modulo-1/sessao-1.html | img/sessao-1/page-1.png | sim |  |
| abraao/modulo-2/sessao-5.html | img/sessao-5/page-1.png | sim | journey-table |
| abraao/modulo-2/sessao-5.html | img/sessao-5/page-2.png | sim | journey-table |
| abraao/modulo-2/sessao-7.html | img/sessao-7/page-1.png | sim |  |
| abraao/modulo-5/sessao-23.html | img/sessao-23/page-1.png | sim | doc-table md reveal |
| jacob/modulo-6/sessao-28.html | img/sessao-28/page-1.png | sim |  |
| messianic-torah/modulo-1/sessao-2.html | img/sessao-2/page-1.png | sim | table-img reveal |
| messianic-torah/modulo-1/sessao-2.html | img/sessao-2/page-1.png | sim | table-img reveal |
| messianic-torah/modulo-1/sessao-3.html | img/sessao-3/page-1.png | sim | table-img reveal |
| messianic-torah/modulo-3/sessao-13.html | img/sessao-13/page-1.png | sim | table-img reveal |
| messianic-torah/modulo-4/sessao-19.html | img/sessao-19/page-1.png | sim | table-img reveal |
| messianic-torah/modulo-4/sessao-21.html | img/sessao-21/page-1.png | sim | table-img reveal |
| noah-to-abraham/modulo-3/sessao-15.html | img/sessao-15/page-1.png | sim |  |
| noah-to-abraham/modulo-3/sessao-15.html | img/sessao-15/page-2.png | sim |  |
| noah-to-abraham/modulo-5/sessao-25.html | img/sessao-25/page-000.png | sim |  |

## B. Componentes obrigatórios ausentes (DESIGN.md)

Arquivos com componente faltando: **102**

| Arquivo | faltando |
|---|---|
| 1-corinthians/modulo-8/sessao-23.html | verse-modal.js |
| adam-to-noah/modulo-1/sessao-1.html | verse-modal.js |
| adam-to-noah/modulo-1/sessao-2.html | verse-modal.js |
| adam-to-noah/modulo-1/sessao-3.html | verse-modal.js |
| adam-to-noah/modulo-1/sessao-4.html | verse-modal.js |
| adam-to-noah/modulo-1/sessao-5.html | verse-modal.js |
| adam-to-noah/modulo-2/sessao-12.html | verse-modal.js |
| adam-to-noah/modulo-2/sessao-13.html | verse-modal.js |
| adam-to-noah/modulo-2/sessao-9.html | verse-modal.js |
| adam-to-noah/modulo-4/sessao-19.html | verse-modal.js |
| adam-to-noah/modulo-4/sessao-22.html | verse-modal.js |
| adam-to-noah/modulo-4/sessao-23.html | verse-modal.js |
| adam-to-noah/modulo-4/sessao-24.html | verse-modal.js |
| adam-to-noah/modulo-5/sessao-26.html | verse-modal.js |
| adam-to-noah/modulo-5/sessao-27.html | verse-modal.js |
| adam-to-noah/modulo-6/sessao-30.html | verse-modal.js |
| jonah/modulo-1/sessao-1.html | reading-progress, verse-modal.js |
| jonah/modulo-1/sessao-2.html | reading-progress, verse-modal.js |
| jonah/modulo-1/sessao-3.html | reading-progress, verse-modal.js |
| jonah/modulo-1/sessao-4.html | reading-progress, verse-modal.js |
| jonah/modulo-1/sessao-5.html | reading-progress, verse-modal.js |
| jonah/modulo-2/sessao-6.html | reading-progress, verse-modal.js |
| jonah/modulo-2/sessao-7.html | reading-progress, verse-modal.js |
| jonah/modulo-2/sessao-8.html | reading-progress, verse-modal.js |
| jonah/modulo-2/sessao-9.html | reading-progress, verse-modal.js |
| jonah/modulo-3/sessao-10.html | reading-progress, verse-modal.js |
| jonah/modulo-3/sessao-11.html | reading-progress, verse-modal.js |
| jonah/modulo-3/sessao-12.html | reading-progress, verse-modal.js |
| jonah/modulo-3/sessao-13.html | reading-progress, verse-modal.js |
| jonah/modulo-3/sessao-14.html | reading-progress, verse-modal.js |
| jonah/modulo-4/sessao-15.html | reading-progress, verse-modal.js |
| jonah/modulo-4/sessao-16.html | reading-progress, verse-modal.js |
| jonah/modulo-4/sessao-17.html | reading-progress, verse-modal.js |
| jonah/modulo-4/sessao-18.html | reading-progress, verse-modal.js |
| jonah/modulo-4/sessao-19.html | reading-progress, verse-modal.js |
| jonah/modulo-4/sessao-20.html | reading-progress, verse-modal.js |
| jonah/modulo-4/sessao-21.html | reading-progress, verse-modal.js |
| jonah/modulo-5/sessao-22.html | reading-progress, verse-modal.js |
| jonah/modulo-5/sessao-23.html | reading-progress, verse-modal.js |
| jonah/modulo-5/sessao-24.html | reading-progress, verse-modal.js |
| jonah/modulo-5/sessao-25.html | reading-progress, verse-modal.js |
| jonah/modulo-5/sessao-26.html | reading-progress, verse-modal.js |
| jonah/modulo-5/sessao-27.html | reading-progress, verse-modal.js |
| jonah/modulo-5/sessao-28.html | reading-progress, verse-modal.js |
| jonah/modulo-6/sessao-28.html | reading-progress, verse-modal.js |
| jonah/modulo-6/sessao-29.html | reading-progress, verse-modal.js |
| jonah/modulo-6/sessao-30.html | reading-progress, verse-modal.js |
| jonah/modulo-6/sessao-31.html | reading-progress, verse-modal.js |
| jonah/modulo-6/sessao-32.html | reading-progress, verse-modal.js |
| jonah/modulo-6/sessao-33.html | reading-progress, verse-modal.js |
| jonah/modulo-6/sessao-34.html | reading-progress, verse-modal.js |
| jonah/modulo-6/sessao-35.html | reading-progress, verse-modal.js |
| jonah/modulo-7/sessao-36.html | reading-progress, verse-modal.js |
| jonah/modulo-7/sessao-37.html | reading-progress, verse-modal.js |
| jonah/modulo-7/sessao-38.html | reading-progress, verse-modal.js |
| jonah/modulo-7/sessao-39.html | reading-progress, verse-modal.js |
| jonah/modulo-8/sessao-40.html | reading-progress, verse-modal.js |
| jonah/modulo-8/sessao-41.html | reading-progress, verse-modal.js |
| jonah/modulo-8/sessao-42.html | reading-progress, verse-modal.js |
| jonah/modulo-8/sessao-43.html | reading-progress, verse-modal.js |
| jonah/modulo-8/sessao-44.html | reading-progress, verse-modal.js |
| jonah/modulo-8/sessao-45.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-1/sessao-1.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-1/sessao-2.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-1/sessao-3.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-1/sessao-4.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-1/sessao-5.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-1/sessao-6.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-1/sessao-7.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-1/sessao-8.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-2/sessao-10.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-2/sessao-11.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-2/sessao-12.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-2/sessao-13.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-2/sessao-14.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-2/sessao-9.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-3/sessao-15.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-3/sessao-16.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-4/sessao-17.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-4/sessao-18.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-4/sessao-19.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-4/sessao-20.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-4/sessao-21.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-4/sessao-22.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-5/sessao-23.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-5/sessao-24.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-5/sessao-25.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-5/sessao-26.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-5/sessao-27.html | reading-progress, verse-modal.js |
| noah-to-abraham/modulo-6/sessao-28.html | reading-progress, verse-modal.js |
| rise-of-the-messiah/modulo-1/sessao-2.html | reading-progress, verse-modal.js |
| rise-of-the-messiah/modulo-1/sessao-3.html | reading-progress, verse-modal.js |
| rise-of-the-messiah/modulo-1/sessao-4.html | reading-progress, verse-modal.js |
| rise-of-the-messiah/modulo-2/sessao-10.html | reading-progress, verse-modal.js |
| rise-of-the-messiah/modulo-2/sessao-5.html | reading-progress, verse-modal.js |
| rise-of-the-messiah/modulo-2/sessao-6.html | reading-progress, verse-modal.js |
| rise-of-the-messiah/modulo-2/sessao-7.html | reading-progress, verse-modal.js |
| rise-of-the-messiah/modulo-2/sessao-8.html | reading-progress, verse-modal.js |
| rise-of-the-messiah/modulo-2/sessao-9.html | reading-progress, verse-modal.js |
| rise-of-the-messiah/modulo-3/sessao-11.html | reading-progress, verse-modal.js |
| rise-of-the-messiah/modulo-3/sessao-12.html | reading-progress, verse-modal.js |
| rise-of-the-messiah/modulo-3/sessao-13.html | reading-progress, verse-modal.js |

## C. Resumo

- Arquivos 100% sem `<img>` (compatíveis com padrão abraao): **309**
- Arquivos com algum `<img>`: **133**

> Nota: SVG/diagramas vetoriais são legítimos no design. Tabelas em imagem e
> páginas completas como imagem são os desvios reais a corrigir.
> `is_table` usa detector determinístico (>=3 separadores verticais >=40% altura).