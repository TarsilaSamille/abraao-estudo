# Briefing: comparar UMA sessão do abraao com o PDF e corrigir

## Par
- HTML: `abraao/modulo-<M>/sessao-<N>.html`
- PDF:  `abraao/pdf-sessoes/sessao-<N>.pdf`
(`abraao/pdf-images/` são PNGs do livro inteiro de 230 páginas — **não** é a fonte por sessão.
Use `pdf-sessoes/`.)

## REGRA CENTRAL: O PDF É A AUTORIDADE
Isto é o que mais importa e é onde trabalho anterior errou o rumo.

- **Cor, tamanho de caixa, e diagramas: copie o PDF.** Não os tokens do DESIGN.md.
- O DESIGN.md vale para **estrutura e tipografia** (escala de fonte, `max-w-4xl`,
  hierarquia de títulos, `.scripture`, `.doc-table`) — **não** para escolher cor.
- Motivo concreto: o PDF usa cores próprias (`#1b1b1b`, `#3a8060`, `#3e4054`,
  `#be4967`, `#7e62bc`, `#816f4d`, `#b5543a`, `#2b6146`, `#5d4897`, `#404ca6`,
  `#645537`, `#4f5669`). O HTML usa os tokens do DESIGN.md (`#24262a`, `#2e7d4e`,
  `#c04a63`, `#8b5cf6`...). **Essa é a "diferença de cores" que o usuário viu.**
  Onde o PDF tem uma cor e o HTML tem outra, volte para a do PDF.

## Passos
1. `cd /Users/macbook/GitHub/biblia-estudo`
2. Backup: `cp <html> /tmp/s<N>.bak.html`
3. Extraia as cores dos dois lados:
   `python3 tools/compare_session.py <N>`
   Lista as cores que o PDF pinta e o HTML não usa, e vice-versa.
4. **Olhe as imagens** (obrigatório — a lista de cores não mostra forma nem layout):
   `python3 tools/compare_session.py <N> --render` → PNGs em `/tmp/cmp-s<N>/`
   Use a ferramenta Read em cada PNG do PDF e no screenshot do HTML.
   Compare **diagrama por diagrama**: nº de painéis, cor de cada painel, textos das
   caixas, ordem, tamanho relativo, formato dos bullets, itálico em legenda.
5. Corrija o que divergir, nesta ordem de prioridade:
   a) **Cores** de diagramas/tabelas/citações/texto que divergem do PDF
   b) **Citações**: referência, tradução (NASB / Tradução do Instrutor / NIV), ordem,
      e se a citação existe no PDF
   c) **Diagramas**: painéis faltando, caixas, rótulos, cores
   d) **Conteúdo presente no PDF e ausente no HTML**
6. Valide: `node tools/verify_render.js <html>` → precisa sair `1/1 ok`.
   Se quebrar, reverta a mudança causadora.

## Regras
- **NÃO** edite nenhum `.css` nem o `DESIGN.md`. Só este HTML.
- Corra local no `<style>` do próprio HTML quando precisar sobrescrever a base.
- **NÃO** altere traduções PT/EN. Só cores, tamanhos, e o que estiver
  genuinamente faltando/errado frente ao PDF.
- **NÃO** quebre o toggle PT/EN, `#reading-progress`, `verse-modal.js`.
- Se houver `diagram-viewport`/`diagram-canvas`, não quebre o `fitDiagrams()`.
- Se um par de cores ficar ilegível, escolha o do PDF que mantém contraste e
  **reporte** a escolha.

## Se já estiver fiel
Pare. Não faça churn cosmetics. Diga "já está fiel" e liste o que você conferiu
(cores, citações, diagramas) para deixar claro que a comparação foi feita.

## Relatório
1. Já estava fiel? sim/não
2. Diferenças de cor (PDF → HTML, com hex)
3. Citações corrigidas
4. Diagramas/estruturas corrigidos
5. `verify_render`: ok/falha
6. O que você não mudou e por quê