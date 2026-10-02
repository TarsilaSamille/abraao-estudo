# Regras comuns — agents de curso (biblia-estudo)

Você é um agente de curso deste repositório. Este arquivo tem as regras que valem
para **todos** os cursos. Seu prompt tem os dados específicos do seu curso.
Leia isto antes de editar qualquer coisa.

## REGRA CENTRAL: O PDF É A AUTORIDADE

Isto é o que mais importa e é onde o trabalho anterior errou o rumo.

- **Cor, tamanho de caixa e diagramas: copie o PDF.** Não os tokens do DESIGN.md.
- O DESIGN.md vale para **estrutura e tipografia** (escala de fonte, `max-w-4xl`,
  hierarquia de títulos, `.scripture`, `.doc-table`) — **não** para escolher cor.
- Motivo concreto: os PDFs pintam com cores próprias (`#1b1b1b` no corpo,
  `#4f5669` no secundário, `#e4e8ed` em grade/pílula, `#6b7384`, `#3e4054`,
  `#816f4d`, `#0000ee`…). O HTML herdava tokens do DESIGN.md (`#24262a`,
  `#17181a`, `#5b7285`, `#e2e6eb`, `#e3e7ec`, `#a9b1be`) que **não existem em
  nenhum PDF**. Essa é a "diferença de cores" que o dono do repositório viu.
- Onde o PDF tem uma cor e o HTML tem outra, volte para a do PDF.

## Os dois defeitos que você vai corrigir

### 1. Fidelidade ao PDF (conteúdo e cor)
- **Cor:** meça no PDF, nunca no DESIGN.md.
- **Conteúdo:** o PDF é a fonte do texto. Se falta no HTML, está faltando.
- **Citações:** referência, tradução (NASB / Tradução do Instrutor / NIV), ordem
  e se a citação existe no PDF.

### 2. Paridade PT/EN
Todo conteúdo bilíngue é `lang-pt` seguido de `lang-en`, na mesma ordem:

```html
<span class="lang-pt">…</span><span class="lang-en">…</span>
```

- Um span sem par é **conteúdo faltando em um dos idiomas** — corrige traduzindo.
- `en` a mais que `pt` = traduções órfãs. `pt` a mais que `en` = sem tradução.
- Não invente texto que não está no PDF: se o par falta, traduza o que existe
  no outro idioma, ou omita o excedente se ele não tiver origem no PDF.
- O chrome da UI (`Voltar`, `Imprimir`, `PT`, `EN`) **não** é conteúdo.

## Ferramentas

```bash
cd /Users/macbook/GitHub/biblia-estudo

# 1. cobertura verbatim EN contra o PDF DA SESSAO (exige pdftotext)
python3 tools/audit_coverage.py            # todos os cursos
python3 tools/audit_coverage.py <curso>    # um curso
python3 tools/audit_coverage.py --low      # so o que esta abaixo de 85%
# Nao use bots/audit_verbatim.py: ele adivinha o intervalo de paginas de cada
# sessao varrendo o livro inteiro e subestima a cobertura (no abraao, 65,5%
# em vez de 87,7% na sessao 5).

# 2. cores do PDF vs cores pintadas no HTML, + render dos dois lados
python3 tools/compare_session.py <N> --render    # curso abraao
#    compare_session.py é específico do abraao. Para outros cursos use o
#    passo 3, que é genérico.

# 3. paleta + geometria do PDF (funciona em qualquer curso) — ver recipes abaixo
```

### Receita: paleta e geometria de um PDF (qualquer curso)
`tools/compare_session.py` só está hard-coded para `abraao`. Para os outros
cursos, extraia direto com PyMuPDF (`import fitz`, instalado):

```python
import fitz
def hexof(r): return "#%02x%02x%02x" % tuple(int(round(c*255)) for c in r)
doc = fitz.open("<curso>/<curso>-teacher-notes.pdf")
for d in doc[N].get_drawings():
    r = d["rect"]
    print(hexof(d["fill"]) if d.get("fill") else "-",
          hexof(d["color"]) if d.get("color") else "-",
          "fo=", d.get("fill_opacity"), "so=", d.get("stroke_opacity"),
          "lw=", d.get("width"), "rect=", r)
# texto: span["color"] e span["size"] por get_text("dict")
```

**Cuidado:** o atributo `fill` do PyMuPDF engana em paths só-tracejados (ele
reporta `fill=#1b1b1b` para o que é na verdade um contorno). **Confirme sempre
por pixel** no raster:

```python
pix = doc[N].get_pixmap(dpi=170); s = 170/72.0
q = pix.pixel(int(x*s), int(y*s))   # => "#rrggbb"
```

### Receita: ver o PDF e o HTML lado a lado (obrigatório)
A lista de cores não mostra forma nem layout. **Olhe as imagens.**

```bash
python3 -c "
import fitz; d=fitz.open('<pdf>'); d[N].get_pixmap(dpi=170, clip=fitz.Rect(x0,y0,x1,y1)).save('/tmp/pdf.png')"
pdftoppm -png -r 100 <pdf> /tmp/pdf-pag      # todas as páginas
node tools/verify_render.js <html>            # screenshot + validação
```

Compare **diagrama por diagrama**: nº de painéis, cor de cada painel, textos das
caixas, ordem, tamanho relativo, formato dos bullets, itálico em legenda.

## Validação (gate obrigatório)

Toda sessão tocada precisa passar:

```bash
node tools/verify_render.js <curso>/modulo-<M>/sessao-<N>.html
```

Tem de sair `1/1 ok`. Se quebrar, reverta a mudança causadora.
Sem scroll horizontal, sem erro JS, sem caixa com texto cortado.

## Proibições

### NÃO QUEBRE A ESTRUTURA DO HTML — isso já aconteceu

Na rodada anterior, agents quebraram **36 arquivos** de três formas:

1. **`<div>` não fechado.** O `<div class="nav-btn-fixed">` do cabeçalho ficou
   sem `</div>`. Como ele é `position:fixed`, engole o `<main>` inteiro e a
   página renderiza com a altura da viewport (1000px) — praticamente vazia.
2. **`</span>` órfão.** Ao remover um bloco sobrou `</span>` sem abertura
   (típico de `</span></span></li>`).
3. **`</figure>`, `<div class="overflow-x-auto">` e `</span>` faltando** onde
   o agente mexeu em legenda ou tabela.

O pior: **o `verify_render.js` antigo dava "ok" em todas**, porque o DOM corrige
tag não fechada silenciosamente. O gate agora checa — mas você tem que rodar:

```bash
node tools/verify_render.js <html>        # tem de dar 1/1 ok
```

E conferir o balanceamento antes de seguir:

```bash
python3 - <<'PY' <html>
import re,sys
h=open(sys.argv[1],encoding='utf-8').read()
for t in ['html','head','body','main','div','section','figure','figcaption',
          'span','table','blockquote','footer','svg']:
    o,c=len(re.findall(r'<%s\b'%t,h)),len(re.findall(r'</%s>'%t,h))
    if o!=c: print(f'DESBALANCEADO <{t}>: {o} abre / {c} fecha')
PY
```

Regra prática: **não apague bloco nenhum.** Prefira corrigir o texto dentro, ou
remover o par `lang-pt`/`lang-en` inteiro junto com o elemento que o contém.

### outras proibições

- **NÃO** edite nenhum `.css` nem o `DESIGN.md`. Só o HTML da sessão.
  Se precisar sobrescrever a base, use o `<style>` local **dentro** do HTML.
- **NÃO** edite `index.html`, `bots/`, `tools/` nem outro curso.
- **NÃO** faça churn cosmético. Se já estiver fiel, pare e diga "já está fiel".
  Ordem de prioridade: (a) traduções faltando → (b) cores → (c) citações →
  (d) diagramas → (e) conteúdo ausente. Tipografia é do DESIGN.md: não mexa.
- **NÃO** use `git add`. A rodada anterior stageou 120 arquivos, o que mistura
  seu trabalho com o do dono no índice. Deixe tudo no working tree.
- **NÃO** comite. Deixe as mudanças no working tree para o dono revisar.
- **NÃO** apague PDF, imagem ou base64. `_pdf_extra_backup/` guarda PDFs que
  não existem em mais nenhum lugar do repositório.

## Relatório final (obrigatório)

Para cada sessão tocada:
1. Já estava fiel? sim/não
2. Diferenças de cor (PDF → HTML, com hex nos dois lados)
3. Citações corrigidas
4. Diagramas/estruturas corrigidos
5. `verify_render`: ok/falha

No fim, um resumo: sessões tocadas, o que **não** foi mudado e por quê.