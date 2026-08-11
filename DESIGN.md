# DESIGN.md — Estrutura das Sessões de Curso

Este repositório contém cursos bíblicos (BibleProject Classroom). Cada curso tem
um PDF de `teacher-notes` e sessões HTML bilíngues (PT/EN) no padrão **abraao**
(curso de referência considerado "terminado igual ao PDF").

## Estrutura de pastas

```
<curso>/
  <curso>-teacher-notes.pdf     # fonte canônica do conteúdo
  index.html                    # índice dos módulos (header + toggle PT/EN)
  modulo-N/
    sessao-N.html               # NÃO em subpasta (write_file direto)
    img/sessao-N/pK-vector.png # imagens vetoriais por página do PDF (quando houver)
  js/verse-modal.js             # modal de versículo (compartilhado)
```

Mapeamento PDF→sessão é feito pelo marcador `Session N:` no teacher-notes.

## Padrão abraao (golden)

Template reutilizado em `abraao/modulo-1/sessao-1.html`:

- **HEAD/CSS**: fontes Inter + Newsreader, `.heb` (hebraico), `.ref`, `.scripture`,
  `.cx` (quiasmo), `.doc-table`, `.v-outer`, `.title`, `.section`, `.sub`,
  `.body`, `.reveal`, barra `#reading-progress`.
- **NAV**: botão `Voltar` → `index.html`, `Imprimir` (`window.print()`),
  toggle `PT`/`EN` (`setLang`, `localStorage` `sN-lang`).
- **CORPO**: `<div class="max-w-4xl mx-auto ...">` → `<h1 class="title reveal">`
  → `<hr>` → blocos `h2.section`/`h3.sub`/`p.body`/`.scripture`/`.heb`/`.ref`/`.cx`,
  cada um com `<span class="lang-pt">` + `<span class="lang-en">`.
- **TAIL**: script `setLang()`, `#reading-progress` (scroll), `IntersectionObserver`
  reveal, `verse-modal.js`. **Zero `<img>`** nas sessões abraao (texto curado).

## Checklist de sessão completa (`SESSAO_CHECKLIST.md`)

Uma sessão está completa quando satisfaz:

1. **Header/estrutura** — `<title>` correto, `Voltar`, `Imprimir`, toggle PT/EN,
   `#reading-progress`, `verse-modal.js`, `page-footer`.
2. **Texto bilíngue** — `lang-en` + `lang-pt` por bloco; EN reproduz o PDF, PT traduzido.
3. **Todo o texto do PDF** — cada frase do teacher-notes da sessão aparece no HTML
   (PT ou EN); sem lixo de cabeçalho (`Class Notes:`, `N of M`, `Session N:`).
4. **Todas as imagens do PDF da sessão** — `<img>` contagem == imagens nas páginas
   do PDF (`img/sessao-N/pK-vector.png`).
5. **Citações** — formato `Autor (AAAA). Título. Editora.` (Wright, Pennington, etc).

## Verificação

`check_session_coverage.py` auto-mapeia PDF→sessão e valida os 5 critérios
(header, en_pt, text, images, citations), reportando por sessão o que falta.

Teto do check: valida presença de EN do PDF, não fidelidade da tradução PT
(sem motor de tradução); contagem de imagens usa `pdfimages -list` (poppler).

## Convenções

- NUNCA editar CSS de sessão abraao existente — só spans `lang-pt`/`lang-en`.
- PT/EN: onde não há tradução humana, o EN fonte fica em ambos os spans
  (interim; abraao real tem PT curado).
- Gerar imagens: `pdftoppm -f P -l P prefix` cria `prefix-P.png`; renomear para
  `pK-vector.png` (pdftoppm acrescenta o número da página).
