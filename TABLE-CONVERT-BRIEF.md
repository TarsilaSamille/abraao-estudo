# Brief: Converter tabelas-imagem em tabelas HTML fiéis (curso: __COURSE__)

Repositório: /Users/macbook/GitHub/biblia-estudo
Curso alvo: __COURSE__  (ex: noah-to-abraham, exodus-overview, joseph, ezekiel, messianic-torah, adam-to-noah, heaven-and-earth)

## Objetivo
Em cada arquivo `sessao-N.html` do curso, toda imagem `<img ... pX-vector.png>` que seja uma **tabela real** (grade de linhas/colunas, não diagrama/fluxograma) deve ser substituída por `<table class="md">` HTML idêntica ao PDF/original, com:
- texto bilíngue PT/EN via `<span class="lang-pt">...</span><span class="lang-en">...</span>`
- highlights de cores idênticos ao original
- hebraico transliterado em `<span class="heb">...</span>`
- referências bíblicas como link clicável: `<strong><span class="verse-link" data-reference="Gênesis+25:23">Gn 25:23</span></strong>` (PT) e `Genesis+25:23` (EN)
- legenda do Tim Mackie em `<tfoot>` itálico

## REGRA CRÍTICA (skill biblia-estudo-sessoes-html)
`table-img` MENTE. Muitas "tabelas" são diagramas/fluxogramas (boxes empilhadas, setas). SÓ converta se for grade real de linhas×colunas com células alinhadas. Fluxogramas, timelines com caixas, e esquemas literários NÃO são tabela — deixe a imagem como está. Quando em dúvida, pergunte ou pule.

## Padrão CSS (inserir ANTES de `  .table-img {` no `<style>`, uma vez por arquivo)
```css
  table.md { width: 100%; border-collapse: separate; border-spacing: 0; border: 1px solid #d7dde5; border-radius: 12px; overflow: hidden; background: #fff; margin: 1.5rem 0; font-size: .92rem; }
  table.md th { background: #e3e7ec; text-align: left; padding: .8rem 1rem; font-weight: 700; color: #1b1b1b; }
  table.md td { padding: .85rem 1rem; border-top: 1px solid #e5e7eb; vertical-align: top; line-height: 1.65; color: #1b1b1b; }
  table.md td + td, table.md th + th { border-left: 1px solid #e5e7eb; }
  table.md tbody tr:hover td { background: #f8fafc; }
  table.md tfoot td { border-top: 1px solid #d7dde5; background: #fbfcfd; color: #6b7280; font-size: .86rem; font-style: italic; padding: .7rem 1rem; }
  .hlx { padding: .05rem .35rem; border-radius: .3rem; font-weight: 600; }
  .hl-tan  { background: #fae3c3; color: #90362e; }
  .hl-sky  { background: #d9ecfd; color: #404ba6; }
  .hl-grn  { background: #d3f1cc; color: #2a6145; }
  .hl-rose { background: #f9e3de; color: #97294e; }
  .hl-brick{ background: #b4533a; color: #fff; }
```
Classes de highlight: `.hl-tan` (bege/terra), `.hl-sky` (azul/bênção), `.hl-grn` (verde/descendência), `.hl-rose` (rosa), `.hl-brick` (tijolo/marrom — usar para "serviço", "maior", "menor", destaques fortes). Use `.hl-tan` para "terra/land", `.hl-sky` para "abençoar/bless", `.hl-grn` para "semente/seed", `.hl-rose` para lamento/pergunta "por que", `.hl-brick` para hierarquia/servidão.

## Fluxo por sessão
1. `grep -o 'p[0-9]*-vector.png' __COURSE__/modulo-*/sessao-N.html` → lista de imagens.
2. Para cada imagem: recorte com PIL (`Image.open(...).crop((90,200,1740,2250))`) e use `vision_analyze` para classificar TABELA ou NAO.
3. Se TABELA: transcreva célula a célula (vision_analyze) marcando highlights por cor; use `/tmp/hl.py` (script PIL) para confirmar cores por pixel se necessário.
4. Substitua o bloco `<div class="table-img reveal"> <img ...> <p class="caption">...</p> </div>` pela `<table class="md">`.
5. Insira o CSS se ausente.
6. Verifique com Chrome headless screenshot se possível (opcional).

## Ferramentas disponíveis
- `/tmp/hl.py` — detecta retângulos de cores num PNG: `python3 /tmp/hl.py <img> '#b4533a' '#fae3c3' ...`
- `vision_analyze` para transcrever/validar.
- Chrome headless: `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless --disable-gpu --screenshot=/tmp/x.png --window-size=1300,2000 file:///tmp/x.html`

## Curso já tem js/verse-modal.js (data-reference funciona). Não mexer em CSS de layout, só inserir o bloco table.md.

## Reportar ao final: lista de sessões processadas, quantas tabelas convertidas por sessão, e quais imagens deixadas como imagem (e porquê).
