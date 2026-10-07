# Joseph — Sessão 5: plano e diretrizes

Alvo: `joseph/modulo-2/sessao-5.html`. Fonte de autoridade: `joseph/pdf-sessoes/sessao-5.pdf` (8 páginas).
Referência de qualidade: sessões 1, 2, 3 e 4 do joseph (já auditadas e commitadas).

## 1. Onde paramos

- Sessões 1–4 do joseph: auditadas, commitadas (último commit: `eca62156`, sessão 4).
- Sessão 5: começou. O working tree tinha uma troca de cor `#1b1b1b` -> `#1a1a1a` no bloco `.m37-sub`.
- A primeira passada do agent `curso-joseph` na sessão 5:
  - Reverteu a troca de cor. `#1b1b1b` é a cor real do PDF; `#1a1a1a` é o token `ink` do DESIGN.md e não existe neste PDF.
  - Reconstruiu o diagrama "Genesis 37: Macro Design" (painéis A, B, A', págs. 1–2). Este diagrama está bom.
  - Completou traduções PT e corrigiu bugs (barra invertida no `<h1>`, `Yosep` -> `Yoseph`).
  - Deixou de fora a figura literária das págs. 3–5.
- Feedback do dono: "não tá bom, olhe o 1 2 3 e 4 como exemplo".

## 2. Diagnóstico (comparação PDF x HTML x sessões 1–4)

O `audit_coverage` dá 100% porque o texto está todo no HTML. O erro é de estrutura, não de texto.

### Defeito 1 — a figura "Paragraph 1: A Favored Son and a Hated Brother" não existe (PDF págs. 3, 4, 5)

No PDF é um diagrama de caixas aninhadas:
- moldura externa clara `#e3e7ee`;
- caixas com borda preta `#17181a` e caixas com borda clara;
- pílulas no topo: "Brothers' Hatred", "Yoseph's 1st Dream", "Yoseph's 2nd Dream", "Brothers' Jealousy";
- rótulos literários na margem esquerda: `A`, `B`, `A'`, `B'`, `A''`;
- realces coloridos (fundos rosa, cinza, laranja `#fae4c4`; texto roxo, verde, vermelho; pílulas cinza-escuro com texto branco);
- legenda "Genesis 37:2-14. Translation and Literary Design by Tim Mackie...".

No HTML está achatado:
- versos partidos em `<p class="body">` e `<ul class="bullets">`, com fragmentos de linha como bullets ("com os filhos", "de Bilhá ,", ...);
- `A`, `B`, `A'`, `B'`, `A''` viraram `<li>` de lista, e um `A''` ficou colado no fim de um parágrafo;
- os títulos das pílulas estão como texto solto no fim do último parágrafo.

### Defeito 2 — blocos de escritura sem `.scripture`

Afeta Gn 29:16-18, 29:30-31, 25:28, 17:5-6, 17:15-16 e 35:10-11.
- No PDF: barra vertical à esquerda, rótulo em negrito, tipo de tradução em azul-acinzentado, nota `*Key Words Adapted by Teacher` abaixo do bloco.
- No HTML: `<h2 class="section">` mais um `<p class="body">` que engole o rótulo do bloco seguinte e a nota.
- Padrão correto: sessão 1 (`<div class="scripture">`, `.scripture-label`, `.scripture-type`, `.scripture-text`, `<sup class="vs">`, `.kw`, `<p class="rotulo">`).

### Defeito 3 — tabela Dia 4 / Dia 6 (PDF pág. 7)

- PDF: 2 linhas, sem cabeçalho. Coluna esquerda é o rótulo (Day 4 / Day 6 + referência); a direita é o texto do versículo.
- HTML: tem `<thead>` "Dia 4 | Dia 6" e uma única linha de corpo.
- Dois `<ul class="bullets">` acima da tabela ("Dia 4: / as luzes celestiais / ...") duplicam a coluna esquerda da tabela. Não existem no PDF.

### Observação sobre o padrão de diagramas

- Sessões 2 e 4 usam o padrão largo: `.diagram-scroll > .diagram-viewport > .diagram-canvas` (1600px, auto-fit, 100vw).
- Sessões 1 e 3 usam pilha em fluxo (`.dg-panel`, `.mg-panel`).
- O Macro Design da sessão 5 (`.m37-*`) segue o padrão em fluxo, coerente com 1 e 3. Mantido.

## 3. Passos de execução

1. Backup: `cp joseph/modulo-2/sessao-5.html /tmp/joseph-s5.round2.bak.html` (já feito).
2. Rodar `python3 tools/diagram_reuse.py joseph 5` para ver se a figura já existe pronta em outro curso. Portar em vez de reconstruir.
3. Medir no PDF as págs. 3–5 (`get_drawings`, `span["color"]`, mapa de fontes Type3 para negrito). Confirmar todo fill e borda por pixel com `get_pixmap(Matrix(6,6))`.
4. Reconstruir a figura "Paragraph 1" com caixas aninhadas, pílulas em fluxo, rótulos de margem e realces. Prefixo de classes local: `.lit37*`. Todo texto em `lang-pt` + `lang-en`.
5. Converter os 6 blocos de escritura para `.scripture`.
6. Refazer a tabela Dia 4/Dia 6 com a estrutura real e remover os 2 `<ul>` duplicados.
7. Remover do `<style>` local as regras mortas, só depois de confirmar que continuam sem uso no body.
8. Registrar as medidas do PDF em comentário no CSS.

## 4. Regras

- O PDF é a autoridade. Não usar tokens do DESIGN.md que não estejam no PDF.
- Não apagar bloco sem mover o conteúdo para o lugar certo. Já houve arquivos quebrados por `</div>` órfão.
- Não editar sessões 1–4 nem CSS compartilhado.
- Não usar `git add` e não commitar até o dono aprovar.
- Bilinguismo obrigatório: nada de texto EN dentro de `lang-pt` e vice-versa.

## 5. Gates

```bash
node tools/verify_render.js joseph/modulo-2/sessao-5.html   # 1/1 ok
python3 tools/audit_parity.py joseph --details              # 0 órfãos, 0 PT==EN, 0 idioma errado
python3 tools/audit_coverage.py joseph                      # 0 abaixo de 85%
node _shot.js joseph/modulo-2/sessao-5.html /tmp/s5/new.png full
```

`verify_render` só checa estrutura. Comparar o screenshot com o raster do PDF (págs. 3, 4, 5 e 7), em PT e em EN.

## 6. Estado atual

- A delegação ao agent `curso-joseph` para executar os passos 2–8 foi cancelada antes de rodar.
- Nenhuma alteração nova foi feita no HTML. O working tree está igual ao fim da primeira passada.
- Próximo passo: reiniciar a execução, por mim ou pelo agent, depois que o dono validar este plano.
