# Guia de Fidelidade: Tabelas e Desenhos Literários (HTML idêntico ao PDF)

Este guia dita **exatamente** como cada tabela e cada desenho literário (quiasmo,
estrutura macro de 3 colunas, caixas de comparação) deve ser renderizado em
`modulo-N/sessao-N.html` para ser **idêntico ao PDF teacher-notes original**.
É a fonte de verdade para converter as `<img>` de tabela em HTML semântico e para
reconstruir os desenhos literários que hoje vivem como imagem.

> **Princípio do usuário (decisivo):** "as tabelas têm que estar idênticas com o
> highlight etc, tudo idêntico, bordas arredondadas, as cores etc." → Fidelidade
> visual, não só textual. Onde o PDF desenha uma tabela/diagrama, o HTML deve
> desenhá-lo com as mesmas bordas, cantos, cores de highlight e legenda.

---

## 0. Como usar este guia

1. Para cada `sessao-N.html`, liste as `<img>` de tabela: `grep -o 'p[0-9]*-vector.png' …`.
2. Confirme se é **tabela real** (grade linha×coluna) ou **desenho literário**
   (caixas/setas/quiasmo) ou **prosa com highlight** (deixar como `<img>`).
3. Converta aplicando a especificação da seção 1 (tabelas) ou 2 (literários).
4. Renderize com Chrome headless e compare ao PNG do PDF (seção 4).
5. Marque em `TABELAS-EM-IMAGEM.md` o que foi convertido e o que NÃO é tabela.

**Regra crítica — `table-img` MENTE.** O wrapper `<div class="table-img">` envolve
~400 imagens repo-wide; a MAIORIA é diagrama/prosa, não tabela. SÓ converta se for
grade real de linhas×colunas. Fluxogramas, timelines de caixas e esquemas
literários NÃO são `<table>` — use a seção 2 (HTML semântico/`.cx`/`.macro`).

---

## 1. Especificação universal — TABELAS (`<table class="md">`)

Aplicável a todos os cursos que usam o padrão "outros cursos" (jacob, adam-to-noah,
noah-to-abraham, messianic-torah, exodus-overview, ezekiel, joseph, etc.).
Módulo 4 do abraao usa `.doc-table` — ver seção 1b.

### 1a. CSS obrigatório (inserir ANTES de `  .table-img {` no `<style>`, 1× por arquivo)

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

`border-collapse: separate` é **OBRIGATÓRIO** — com `collapse` o `border-radius`
é ignorado e os cantos ficam quadrados (rejeitado pelo usuário).

### 1b. Módulo 4 do abraao usa `.doc-table` (NÃO `table.md`)

O CSS canônico de `abraao/modulo-4/sessao-16.html`:

```css
  .doc-table { width: 100%; border-collapse: separate; border-spacing: 0; border: 3px solid #d9dee6; border-radius: 14px; overflow: hidden; background: #fff; }
  .doc-table th { background: #e2e6eb; text-align: left; padding: 1rem 1.3rem; font-weight: 800; font-size: 1.02rem; color: #17181a; }
  .doc-table td { padding: 1.1rem 1.3rem; border-top: 1px solid #e5e7eb; vertical-align: top; line-height: 1.78; font-size: .97rem; color: #24262a; }
  .doc-table td + td { border-left: 1px solid #e5e7eb; }
  .doc-table tbody tr:hover td { background: #f8fafc; }
  .doc-table tfoot td { border-top: 1px solid #d1d5db; background: #fbfcfd; color: #5b6472; font-size: .92rem; }
```
Tabelas de módulo 4 (abraao) devem usar `class="doc-table reveal"`; os chips de
highlight são `.k` (ex: `.k-blue #3b82c4`, `.k-green #2e7d4e`, `.k-rose #c04a63`,
`.k-rust`, `.k-teal`, `.k-purple`, `.k-brown`, `.k-gray`) — pastel-bg NÃO, estes são
chips coloridos sólidos com texto branco.

### 1c. Regras de conteúdo (idêntico ao PDF)

- **Toda célula é bilíngue:** `<span class="lang-pt">…</span><span class="lang-en">…</span>`
  em `<th>` e `<td>`. EN = texto literal do PDF; PT = tradução fiel.
- **Cantos arredondados + borda `#d7dde5` + header `#e3e7ec`** sempre (exceto doc-table).
- **Tabelas largas** (≥4 colunas / muitas colunas): envolver em
  `<div class="overflow-x-auto"><table class="md reveal" style="min-width:900px;">`.
- **`colspan`** deve == número de `<th>`. Conferir sempre (sessao-4 "Like Father"
  saiu com `colspan="4"` numa tabela de 3 colunas → borda vazia).
- **Referências bíblicas:** PDF renderiza em **negrito** e devem abrir o verse-modal.
  jacob usa `.verse-link`; abraao/mod3 usam `.ref`. Formato canônico:
  ```html
  <strong><span class="verse-link" data-reference="Gênesis+25:23">Gn 25:23</span></strong>
  ```
  PT: `data-reference="Gênesis+25:23"`; EN: `data-reference="Genesis+25:23"`.
  **Armadilha:** label dividido (`data-reference="Gênesis+16,">Gn 16,</span> 21`) quebra
  o modal (404). Reescrever como um só: `data-reference="Gênesis+16,21">Gn 16, 21`.

### 1d. Paleta de highlights (AMOSTRADA DOS PIXELS REAIS DO PDF — usar exatamente)

| Classe | bg (hex) | texto (hex) | uso no PDF |
|---|---|---|---|
| `.hl-tan` | `#fae3c3` | `#90362e` | terra / land / "ama/loves" |
| `.hl-sky` | `#d9ecfd` | `#404ba6` | abençoar / bless / "no campo" |
| `.hl-grn` | `#d3f1cc` | `#2a6145` | semente / seed / descendência |
| `.hl-rose` | `#f9e3de` | `#97294e` | lamento / "por que" / pergunta |
| `.hl-brick` | `#b4533a` | `#ffffff` | hierarquia / serviço / "maior/menor" |

Chrome: header `#e3e7ec`, texto `#1b1b1b`, legenda `#4e5669`/`#6b7280`.
Tabelas moncromáticas (sem nenhuma dessas cores nos pixels) → **não** aplicar
nenhum `.hl-*`. Decida "tem highlight?" por **histograma de pixels**, nunca por
vision_analyze (a visão inventa e nega highlights).
- hebraico transliterado em `<span class="heb">…</span>` (RTL, copiar exato do PDF).

### 1e. Legenda = `<tfoot>`, NÃO `<p class="caption">` irmão

O PDF desenha "Created by Tim Mackie for BibleProject Classroom: …" **dentro** da
borda inferior da tabela.
```html
<tfoot><tr><td colspan="{N_TH}"><span class="lang-pt">…Tim Mackie…</span><span class="lang-en">…Tim Mackie…</span></td></tr></tfoot>
```
Substituir o bloco inteiro `<div class="table-img reveal"><img …><p class="caption">…</p></div>`
pela `<table class="md">` (não só a `<img>`).

---

## 2. Especificação universal — DESENHOS LITERÁRIOS (HTML semântico)

Estes NÃO são `<table>`. São diagramas de caixas/setas/quiasmo que o PDF desenha
como imagem. Reconstruir com `.cx` (quiasmo) / `.macro` (estrutura de 3 colunas) /
`.doc-table` + `.k` chips (caixas de comparação). CSS canônico de
`abraao/modulo-4/sessao-16.html` (copiar para o curso alvo se ausente).

### 2a. Quiasmo / simetria em escada (`.cx`)

Caixa por letra (A…G e A'…G'), com `margin-left/right %` formando a escada. Cores
por letra **devem bater com o PDF** (cada letra tem uma cor). Sequência canônica
(abraao sessao-16, Gênesis 18-19):

| Letra | cor `.cx-*` | border | bg | tag |
|---|---|---|---|---|
| A | `cx-slate` | `#6b7280` | `#e9ebee` | `#6b7280` |
| B | `cx-rust` | `#c0562f` | `#f7e6dd` | `#c0562f` |
| C | `cx-rose` | `#c04a63` | `#f7e0e5` | `#c04a63` |
| D | `cx-blue` | `#5468d4` | `#e4e8f9` | `#5468d4` |
| E | `cx-green` | `#2e7d4e` | `#dfeee2` | `#2e7d4e` |
| F | `cx-purple` | `#8b5cf6` | `#efe2f8` | `#8b5cf6` |
| G | `cx-tan` | `#8a6d3b` | `#ece7dc` | `#8a6d3b` |
| (espelho) | repete E→A | igual | igual | igual |

Margens da escada (ABERTO → ápice → FECHADO), exatamente como o PDF:
```
A  margin-left:0;  margin-right:0;
B  margin-left:3%; margin-right:3%;
C  margin-left:6%; margin-right:6%;
D  margin-left:9%; margin-right:5%;
E  margin-left:13%;margin-right:4%;
F  margin-left:17%;margin-right:3%;
G  margin-left:21%;margin-right:3%;
F' margin-left:17%;margin-right:3%;
E' margin-left:13%;margin-right:4%;
D' margin-left:9%; margin-right:5%;
C' margin-left:6%; margin-right:6%;
B' margin-left:3%; margin-right:3%;
```
Estrutura de cada caixa:
```html
<div class="cx cx-slate reveal" style="margin-left:0; margin-right:0;">
  <span class="cx-tag">Genesis 18:1-15</span>
  <h4>A - <span class="lang-pt">…</span><span class="lang-en">…</span></h4>
  <ul class="bullets"><li>… versos com <span class="ref">Gn 18:1</span> …</li></ul>
</div>
```
CSS base: `.cx { border:3px solid; border-radius:12px; padding:1.35rem 1.5rem 1.2rem; margin:1.15rem 0; }`
`.cx-tag { display:inline-block; font-weight:700; color:#fff; padding:1px 13px; border-radius:6px; margin-bottom:.7rem; }`

### 2b. Estrutura macro de 3 colunas (`.macro`)

Grade `grid-template-columns: 1fr 1fr 1fr; gap:1rem`. Cada `.mcol` tem `.mtag`
(cabeçalho colorido), `.mcol-title`, e `.mboxes` (caixas de versos empilhadas).
```html
<div class="macro reveal">
  <div class="mcol"><span class="mtag mtag-green">Genesis 18:1-15</span>
    <p class="mcol-title"><span class="lang-pt">…</span><span class="lang-en">…</span></p>
    <div class="mboxes"><div class="mbox"><span class="mhdr">18:1-2</span></div>…</div>
  </div>
  <div class="mcol dark">… coluna escura (.mtag-dark #3d4453) …</div>
</div>
<p class="caption reveal"><span class="lang-pt"><em>Gênesis 18:1-19:38</em>. Design Literário por Tim Mackie…</span><span class="lang-en">…</span></p>
```
`mtag-green` `#2e7d4e`, `mtag-dark` `#3d4453`; `.mbox` borda `#b9c2cf`, `.mhdr` bg `#7d8697`.
Em telas ≤860px vira 1 coluna (media query no CSS).

### 2c. Caixas de comparação / duas colunas (não-quiasmo)

Quando o PDF mostra duas colunas lado-a-lado comparando passagens (ex: "Avram's
Deception in Gen 12" vs "The Snake's Deception in Gen 3"; ou Esaú/Nimrode,
Adão/Edom), usar `<table class="md">` de 2 colunas OU duas `.mcol` dentro de um
`.macro` de 2 colunas — seguir o que o PDF desenha (grade = table; caixas =
mcol). Aplicar highlights `.hl-*` idênticos ao PDF.

### 2d. Prosa com highlight (NÃO é tabela nem diagrama)

Páginas do PDF que são parágrafos com palavras destacadas em cor → deixar como
`<img>` (ex: jacob sessao-5 p3/p4, exodus-overview páginas de notas). Converter
só se for grade real.

---

## 3. Loop de verificação (renderizar e comparar ao PDF)

Após converter, **o usuário julga pelos pixels**, não por asserts estruturais.

1. Estrutura: `assert s.count('<table')==s.count('</table>')`, `colspan==len(th)`,
   `lang-pt==lang-en`, `table.md {` / `.doc-table` presente, todo `<img>` restante
   resolve no disco.
2. Render: `cd` no curso, `python3 -m http.server 8137` (background),
   `browser_navigate http://localhost:8137/<curso>/modulo-N/sessao-N.html`.
   (O `browser` bloqueia `file://`; use o servidor.) Ou Chrome headless:
   ```bash
   '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' --headless --disable-gpu \
     --screenshot=/tmp/prev.png --window-size=1200,2400 file:///tmp/prev.html
   ```
3. Comparar screenshot ao PNG do PDF (`img/sessao-N/pX-vector.png`): bordas
   arredondadas ✓, header cinza ✓, cada highlight na cor certa ✓, legenda dentro
   da tabela ✓. "Falta highlight?" → **diff de histograma de pixels** entre PNG
   fonte e screenshot renderizado, não re-perguntar à visão.
4. **Um arquivo por vez.** O usuário pediu "um por um" — converter, mostrar
   veredito, perguntar antes do próximo. Não empilhar tudo num mega-edit silencioso.

---

## 4. Mapa de cobertura por curso (estado atual, derivado dos arquivos)

**Já convertido (tem `<table class="md">` / `.doc-table` / `.cx` / `.macro`):**
- **abraao**: 21 sessões (1,6,8,9,11,12,14,15,16,18–24,26–30) — referência canônica.
- **jacob**: 13 sessões (4,5,6,7,8,9,10,11,12,13,14,15,18) — referência de tabela.
- **noah-to-abraham**: 5 (1,3,5,7,8) · **messianic-torah**: 2 (2,15) ·
  **adam-to-noah**: 2 (5,6) · **heaven-and-earth**: 1 (13) · **intro-hebrew-bible**: 1 (3).

**Pendente de auditoria (ainda tem `<img>` vetorial — verificar cada uma: tabela?
literário? prosa?)** — NÃO converter cegamente:
- **exodus-overview**: 25 sessões (5,7–30) — na maioria prosa/diagrama de notas,
  confirmado falso-positivo em várias (p14 = Horeb/Sinai prosa).
- **joseph**: 16 (4,5,6,7,10,11,14,17,19,20,21,22,23,25,26,28).
- **ezekiel**: 9 (1,2,3,4,6,9,26,27,28) — p2/p3 são diagramas de cânone (NÃO tabela).
- **jacob**: 26 (as demais de 1,2,4,5,6,7,8,9,10,11,12,13,14,15,17,18–28 não convertidas).
- **adam-to-noah**: 14 (12,14,15,18–29).
- **messianic-torah**: 7 (1,2,3,5,6,7,9) — p5/p7 são tabelas reais (Prov/Mt).
- **art-of-biblical-words**: 3 (2,3,4) · **others**: 3 (6,8,14).

> Obs: o scan de desvios (`scan_design_deviations.py`, `DESVIOS-DESIGN.md`) lista
> 62 "candidatos a tabela" por detector de colunas — mas o detector é ruidoso
> (páginas inteiras de notas passam). Sempre confirmar com visão + histograma.

---

## 5. Exemplos canônicos para copiar

- **Tabela bilíngue 5-col com verse-links + highlights**: `jacob/modulo-1/sessao-4.html`
  (bloco "God Blesses the Chosen One" — `table.md` + `.hl-tan`/`.hl-sky`/`.hl-grn`/
  `.hl-brick`, legenda em `<tfoot>`).
- **Quiasmo em escada + macro 3-col**: `abraao/modulo-4/sessao-16.html`
  (Gênesis 18-19 — `.cx` + `.macro`, cores por letra, margens da seção 2a).
- **Caixas de comparação 2-col**: `jacob/modulo-1/sessao-4.html` (bloco
  "Avram's Deception … / The Snake's Deception …", `<table class="md">` 2 colunas).

Sempre copiar o CSS + estrutura do arquivo canônico do MESMO curso/módulo; não
misturar sistemas (módulo 4 abraao = `.doc-table`/`.k`; outros = `table.md`/`.hl-*`).

