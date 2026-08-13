# Desvios do DESIGN.md (padrão abraao)

Gerado por `scan_design_deviations.py`. 441 arquivos `sessao-*.html` escaneados.

## A. Conteúdo como imagem (DEVE ser HTML semântico)

- Arquivos com `<img>`: **104** de 441
- Imagens quebradas (src não existe): **0**
- Páginas completas como imagem (provavelmente redundantes): **0**
- SVGs (diagrama vetorial, OK): **2**
- Vetoriais PNG (diagrama ou tabela): **24**
- Outros PNG: **170**
- **Candidatos a tabela real** (detector de colunas >=3): **40**

### A.1 Candidatos a tabela (imagem deveria ser `<table class="md">`)

| Arquivo | src | existe | wrapper |
|---|---|---|---|
| 1-corinthians/modulo-6/sessao-15.html | img/sessao-15/illu-004-000.jpg | sim |  |
| 1-corinthians/modulo-7/sessao-18.html | img/sessao-18/illu-002-000.jpg | sim |  |
| adam-to-noah/modulo-1/sessao-1.html | img/sessao-1/mona-lisa.png | sim | figure reveal |
| adam-to-noah/modulo-1/sessao-2.html | img/sessao-2/p3_387.png | sim | figure reveal |
| adam-to-noah/modulo-1/sessao-4.html | img/sessao-4/p2_309.png | sim | figure reveal |
| adam-to-noah/modulo-2/sessao-10.html | img/sessao-10/p5-origami.png | sim | figure reveal |
| adam-to-noah/modulo-6/sessao-30.html | img/sessao-30/hubble.png | sim | figure reveal |
| adam-to-noah/modulo-6/sessao-30.html | img/sessao-30/van-gogh.png | sim | figure reveal |
| ephesians/modulo-1/sessao-1.html | img/sessao-1/illu-001-000.jpg | sim |  |
| ephesians/modulo-10/sessao-31.html | img/sessao-31/illu-003-000.jpg | sim |  |
| ephesians/modulo-2/sessao-7.html | img/sessao-7/illu-003-000.jpg | sim |  |
| ephesians/modulo-3/sessao-9.html | img/sessao-9/illu-002-000.jpg | sim |  |
| ephesians/modulo-4/sessao-12.html | img/sessao-12/illu-003-001.jpg | sim |  |
| ephesians/modulo-5/sessao-15.html | img/sessao-15/illu-004-000.jpg | sim |  |
| ephesians/modulo-6/sessao-18.html | img/sessao-18/illu-002-000.jpg | sim |  |
| ephesians/modulo-8/sessao-23.html | img/sessao-23/illu-005-000.jpg | sim |  |
| ephesians/modulo-9/sessao-24.html | img/sessao-24/illu-001-000.jpg | sim |  |
| ephesians/modulo-9/sessao-24.html | img/sessao-24/illu-001-001.jpg | sim |  |
| ezekiel/modulo-4/sessao-16.html | ../modulo-3/img/sessao-16/p12-ill.jpeg | sim | figure reveal |
| heaven-and-earth/modulo-1/sessao-1.html | img/sessao-1/p0_x5.png | sim | figure reveal |
| heaven-and-earth/modulo-1/sessao-1.html | img/sessao-1/p1_x224.png | sim | figure reveal |
| heaven-and-earth/modulo-1/sessao-1.html | img/sessao-1/p1_x225.png | sim | figure reveal |
| heaven-and-earth/modulo-1/sessao-1.html | img/sessao-1/p1_x226.png | sim | figure reveal |
| heaven-and-earth/modulo-1/sessao-5.html | img/sessao-5/p1_x296.png | sim | figure reveal |
| heaven-and-earth/modulo-2/sessao-12.html | img/sessao-12/p1_x355.png | sim | figure reveal |
| heaven-and-earth/modulo-2/sessao-6.html | img/sessao-6/p0_x5.png | sim | figure reveal |
| heaven-and-earth/modulo-4/sessao-22.html | img/sessao-22/p2_x319.png | sim | figure reveal |
| heaven-and-earth/modulo-5/sessao-26.html | img/sessao-26/p3_x380.png | sim | figure reveal |
| heaven-and-earth/modulo-6/sessao-28.html | img/sessao-28/p2_x374.png | sim | figure reveal |
| heaven-and-earth/modulo-6/sessao-28.html | img/sessao-28/p3_x377.png | sim | figure reveal |
| heaven-and-earth/modulo-6/sessao-28.html | img/sessao-28/p3_x378.png | sim | figure reveal |
| intro-hebrew-bible/modulo-2/sessao-9.html | img/sessao-9/p1_269.png | sim | figure reveal |
| intro-hebrew-bible/modulo-3/sessao-11.html | img/sessao-11/p0_5.jpeg | sim | figure reveal |
| intro-hebrew-bible/modulo-3/sessao-12.html | img/sessao-12/p0_5.jpeg | sim | figure reveal |
| intro-hebrew-bible/modulo-3/sessao-12.html | img/sessao-12/p1_233.jpeg | sim | figure reveal |
| intro-hebrew-bible/modulo-3/sessao-13.html | img/sessao-13/p3_335.jpeg | sim | figure reveal |
| intro-hebrew-bible/modulo-4/sessao-18.html | img/sessao-18/p1_231.jpeg | sim | figure reveal |
| intro-hebrew-bible/modulo-4/sessao-18.html | img/sessao-18/p2_290.jpeg | sim | figure reveal |
| intro-hebrew-bible/modulo-5/sessao-22.html | img/sessao-22/p1_295.jpeg | sim | figure reveal |
| intro-hebrew-bible/modulo-5/sessao-23.html | img/sessao-23/p2_351.jpeg | sim | figure reveal |

### A.2 Imagens quebradas (src ausente no disco)

| Arquivo | src |
|---|---|

### A.3 Páginas completas como imagem (redundantes? verificar texto no HTML)

| Arquivo | src | existe | wrapper |
|---|---|---|---|

## B. Componentes obrigatórios ausentes (DESIGN.md)

Arquivos com componente faltando: **0**

| Arquivo | faltando |
|---|---|

## C. Resumo

- Arquivos 100% sem `<img>` (compatíveis com padrão abraao): **337**
- Arquivos com algum `<img>`: **104**

> Nota: SVG/diagramas vetoriais são legítimos no design. Tabelas em imagem e
> páginas completas como imagem são os desvios reais a corrigir.
> `is_table` usa detector determinístico (>=3 separadores verticais >=40% altura).