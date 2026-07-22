# Plano de Construção — Bible Project Classroom (12 cursos restantes)

Objetivo: replicar o formato do estudo de **Abraão** (`abraao/`) para todos os classrooms do BibleProject.
Meta registrada em: `logseq-study/pages/Metas.md` → Estudos / Carreira.

## Princípios (regras invioláveis do projeto)
1. **TEXTO** = tradução literal do PDF em inglês para PT-BR. Nunca reescrever, parafrasear, resumir ou adicionar comentário.
2. **ESTILO/DESIGN** = fiel ao PDF original. Cabeçalhos = tradução literal do heading em inglês (manter EN como glosa). Nunca inventar seções.
3. **SEMPRE verificar** antes de dizer "pronto" (screenshot via Playwright + comparar com `pdf-images/page_N.png`).
4. **Uma sessão por vez**, sequencial. Sem subagents.
5. `js/verse-modal.js` presente em TODAS as sessões; spans `.verse-link` com `data-reference`.

## Fonte dos PDFs
`https://documents.bibleproject.com/classroom/teacher-notes/{slug}-teacher-notes.pdf`
(também há `instructor-translation` no mesmo padrão, se necessário)

## Estrutura por curso (espelha abraao/)
```
<curso>/
  <curso>-teacher-notes.pdf   ← baixado ✅
  index.html                  ← landing do curso (a construir)
  style.css                   ← copiar/adaptar de abraao/style.css
  js/verse-modal.js           ← copiado ✅
  image/                      ← capa + thumbs de módulo (a gerar)
  pdf-images/page_N.png       ← ground truth, 0-indexed ✅ (renderizado)
  modulo-1..N/
     index.html               ← landing do módulo
     sessao-*.html            ← uma por sessão (tradução literal)
```

## Cursos (status: pasta ✅, PDF ✅, imagens ✅ — falta construir HTML)

### Antigo Testamento
| # | Curso | Ref. | Sessões | Duração | PDF págs | Pasta |
|---|-------|------|---------|---------|----------|-------|
| 1 | Heaven and Earth | Gênesis 1 | 31 | 14h26 | 141 | `heaven-and-earth/` |
| 2 | Adam to Noah | Gênesis 2-5 | 32 | 14h05 | 188 | `adam-to-noah/` |
| 3 | Jacob | Gênesis 25:19-37:1 | 29 | 16h35 | 184 | `jacob/` |
| 4 | Joseph | Gênesis 37:2-50:26 | 29 | 16h41 | 215 | `joseph/` |
| 5 | Exodus Overview (Carmen Imes) | Êxodo 1-40 | 30 | 13h28 | 80 | `exodus-overview/` |
| 6 | Ezekiel | Ezequiel 1-48 | 29 | 16h32 | 249 | `ezekiel/` |
| 7 | Jonah | Jonas 1-4 | 45 | 12h54 | 161 | `jonah/` |

### Novo Testamento
| # | Curso | Ref. | Sessões | Duração | PDF págs | Pasta |
|---|-------|------|---------|---------|----------|-------|
| 8 | The Messianic Torah | Mateus 5-7 | 22 | 15h07 | 245 | `messianic-torah/` |
| 9 | 1 Corinthians (Lucy Peppiatt) | 1 Coríntios 1-16 | 23 | 13h30 | 81 | `1-corinthians/` |
| 10 | Ephesians | Efésios 1-6 | 35 | 11h25 | 134 | `ephesians/` |

### Habilidades de Leitura
| # | Curso | Ref. | Sessões | Duração | PDF págs | Pasta |
|---|-------|------|---------|---------|----------|-------|
| 11 | Introduction to the Hebrew Bible | Reading Skills | 29 | 14h44 | 109 | `intro-hebrew-bible/` |
| 12 | Art of Biblical Words | Reading Skills | 5 | 2h54 | 26 | `art-of-biblical-words/` |

> Também pendente: **Noah to Abraham** (Gênesis 6-11) — pasta `noah-output/` já existe parcialmente, falta finalizar e linkar no index.

## Fluxo de construção por curso (repetir para cada)
1. Extrair texto real por página com PyMuPDF (`fitz`) — nunca adivinhar mapeamento sessão↔página.
2. Identificar módulos e sessões a partir do texto/estrutura do PDF.
3. Construir `index.html` do curso + `modulo-N/index.html`.
4. Construir cada `sessao-*.html`: tradução literal PT + glosa EN nos headings + `.verse-link`.
5. Verificar: `node others/_src/shot.js "file:///.../sessao-X.html" /tmp/out.png` → `vision_analyze` → comparar com `pdf-images/page_N.png`.
6. Só marcar concluído após conferência visual.

## Ordem sugerida
Começar pelos menores para validar o pipeline: **Art of Biblical Words (26p/5 sessões)** → **Exodus Overview (80p)** → **1 Corinthians (81p)** → demais por tamanho.
