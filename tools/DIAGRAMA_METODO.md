# Método para reconstruir um diagrama de PDF em HTML/CSS

Leia isto **antes** de mexer em qualquer sessão. Cada item abaixo é uma armadilha
em que já caímos neste trabalho.

## 0. O PDF é a autoridade

O HTML é reconstrução, não adaptação. Não invente conteúdo, não "melhore", não
use tokens do `DESIGN.md` se não estão no PDF.

## 1. ANTES de construir: procure implementação existente

A mesma ilustração do BibleProject reaparece em cursos diferentes. **Já levei
um dia para reconstruir do zero um diagrama que já existia pronto** em
`abraao/modulo-1/sessao-3.html`.

```bash
python3 tools/diagram_reuse.py <curso> <sessao>
```

Se aparecer um match forte (>= 6/8 sondas), **porte** a implementação em vez de
reconstruir. O padrão do projeto para diagramas largos é:

- `.diagram-scroll > .diagram-viewport > .diagram-canvas` — canvas fixo de
  1600px, `#sessao-N > .diagram-scroll` em `100vw` (sangria), auto-fit por
  `transform: scale()` no desktop via JS `fitDiagrams()`, empilhamento vertical no
  mobile via media query. Referência: `abraao/modulo-1/sessao-3.html`.
- Componentes: `.diag-cluster-blue`, `.diag-cluster-slate`, `.diag-badge-blue`,
  `.diag-badge-slate`, `.diag-badge-inner`, `.diag-badge-mini`, `.diag-box`,
  `.diag-subbox`, `.diag-bullets`, `.flow-box-blue`, `.flow-box-slate`,
  `.flow-card-inner`. Bordas de **3px**, raios 9/6/5px, pílulas **em fluxo**
  (`display: inline-block`), nunca `position: absolute` com offsets medidos.

## 2. `fill` do PyMuPDF MENTE — sempre confirme por pixel

Já mentiu 3 vezes (sessões 1, 2 e 3 do `joseph`). Reportou `#be4966` num painel
que é branco. **Todo preenchimento e toda cor de borda precisa ser confirmada
amostrando o pixel**:

```python
import fitz
d = fitz.open(pdf)
pm = d[pagina].get_pixmap(matrix=fitz.Matrix(6, 6))
print(tuple(pm.pixel(int(x*6), int(y*6))))   # => (R, G, B)
```

## 3. Flags de textoType3 NÃO reportam negrito

`span['flags']` e `span['font']` dizem "R" para texto que é claramente negrito.
O jeito é mapear os **IDs das fontes** — no `joseph`:

| fonte Type3 | uso |
|---|---|
| `11`  | texto normal do corpo |
| `67`  | pontuação |
| `110` | **NEGRITO** (pílulas, nomes, descrições, destaques coloridos) |
| `163` | **NEGRITO** (dígitos dentro de pílulas, esp\S5fcuras) |
| `345`/`350` | **NEGRITO** (ex.: `firstborn`) |
| `312`/`315` | referência **sublinhada** |

Correlacione sempre com um render do PDF para não confiar na tabela às cegas.

## 4. Unidades

- `1pt = 1.3333px` a 96dpi. Traço `1.5pt = 2px`.
- **As medidas do PDF são centro-do-traço.** A caixa CSS é o `border-box`, ou
  seja **1.5pt MAIOR** que a medida do PDF. Ex.: PDF 60pt -> CSS 61.5pt = 82px.
- Recuo/vão de `2.8pt = 3.7px`.

## 5. Geometria interna

Sempre meça a partir do PDF, para cada elemento:

```
topo do elemento - 6.8pt (da borda)   -> posicao da pílula
15pt = 20px                            -> altura da pílula
entrelinha 15.8pt = 21px               -> line-height do texto
vão entre caixas 7.5pt = 10px
```

Depois **confirme no navegador** e compare com o PDF. Não confie no cálculo.
Exemplo de medição no navegador (playwright):

```js
const PT = 1 / 1.3333;
// rect.left - box.left, etc.  Compare com os numeros do PDF.
```

## 6. Sublinhados e realces invisíveis às flags

Sublinhado = retângulo fino (`height` <= 1.0pt) nos drawings, **não** é texto.
Realce = texto com cor diferente. Negrito = fonte 110/163.

## 7. Bilinguismo obrigatório

Todo texto precisa de `<span class="lang-pt">` e `<span class="lang-en">`.
Texto neutro (referências como `1:1-5:32`) pode ficar fora dos spans.
Textos **de outra sessão/curso não entram**: só o que está no PDF desta sessão.
Verificar com `python3 tools/audit_parity.py <curso>`.

## 8. Imagens

Confira se o arquivo **existe**: `ls <curso>/img/<sessao>/`. Se o PDF tiver a
imagem, extraia:

```python
im = pg.get_images(full=True)[0]
pix = fitz.Pixmap(d, im[0])
pix.save(destino)
```

Reduza para ~2x do tamanho em que ela aparece no PDF (economiza muito KB).

## 9. Validação obrigatória

```bash
node tools/verify_render.js <curso>/modulo-X/sessao-N.html   # precisa ser 1/1 ok
python3 tools/audit_parity.py <curso>                       # 0 orfaos, 0 PT==EN
python3 tools/audit_coverage.py <curso>                     # 0 abaixo de 85%
```

E **olhe o resultado**: fa;a um screenshot e compare com o PDF. `verify_render` só checa
estrutura, não aparência.

Checagem de que nada do PDF ficou de fora (pega conteúdo faltando):

```python
# compare cada frase do PDF contra o texto visivel do HTML
```

## 10. Onde registrar a medição

Comente no CSS, com os números do PDF. O próximo vai agradecer:

```css
/* Medido no PDF (1pt = 1.3333px): moldura 1.5pt, raio 5.3pt, vao 7.5pt. */
```

## 11. Commitar

Um commit por sessão, mensagem explicando o que estava errado e o que foi medido.