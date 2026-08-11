---
name: Estudos Bíblicos — The Bible Project
description: Bilingual (PT/EN) biblical-study course portal and reading pages, built on Tailwind plus a shared editorial stylesheet.
colors:
  primary: "#0284c7"
  primary-link: "#2563eb"
  ink: "#1a1a1a"
  body: "#24262a"
  heading-ink: "#17181a"
  muted: "#5b6472"
  muted2: "#5b7285"
  caption: "#5b6472"
  border: "#d7dde5"
  border-soft: "#d7d7df"
  border-quote: "#aeb6bf"
  surface: "#f1f5f9"
  bg: "#ffffff"
  scripture-rule: "#dfe4ea"
  scripture-hover: "#9aa7b8"
  quote-text: "#3a3f47"
  nav-text: "#475569"
  sup: "#333333"
  rust: "#c0392b"
  emerald: "#059669"
  amber: "#d97706"
  amber-badge: "#f59e0b"
  amber-badge-bg: "#fffbeb"
  cx-slate: "#6b7280"
  cx-rust: "#c0562f"
  cx-rose: "#c04a63"
  cx-blue: "#5468d4"
  cx-green: "#2e7d4e"
  cx-purple: "#8b5cf6"
  cx-tan: "#8a6d3b"
  cx-slate-tint: "#e9ebee"
  cx-rust-tint: "#f7e6dd"
  cx-rose-tint: "#f7e0e5"
  cx-blue-tint: "#e4e8f9"
  cx-green-tint: "#dfeee2"
  cx-purple-tint: "#efe2f8"
  cx-tan-tint: "#ece7dc"
  k-blue: "#3b82c4"
  k-green: "#2e6b4e"
  k-rose: "#c04a63"
  k-teal: "#0d7d8c"
  k-purple: "#7c5ad0"
  t-teal: "#0d8aa0"
  surface-abraham: "#f6f8fa"
  border-abraham: "#e3e7ee"
  border-abraham2: "#e5e7eb"
  border-abraham3: "#d9dee6"
  header-tint: "#e2e6eb"
  ink-abraham: "#17181a"
  ink-soft: "#1f2937"
  macro-dark: "#3d4453"
  mbox-hdr: "#7d8697"
  tfoot: "#d1d5db"
  surface-div: "#e6eaf0"
  kblue-soft-bg: "#cddcf5"
  kblue-soft-fg: "#2b5fb0"
  frame-light: "#b9c2cf"
  rust-accent: "#bf5a2b"
  paper-faint: "#fbfcfd"
  shadow-card: "rgba(30,41,59,.4)"
  shadow-hairline: "rgba(0,0,0,.06)"
typography:
  display:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "2.6rem"
    fontWeight: 800
    lineHeight: 1.08
    letterSpacing: "-0.025em"
  section:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "1.9rem"
    fontWeight: 800
    lineHeight: 1.2
    letterSpacing: "-0.015em"
  sub:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "1.3rem"
    fontWeight: 800
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "1.05rem"
    fontWeight: 400
    lineHeight: 1.78
  serif:
    fontFamily: "Newsreader, Georgia, serif"
    fontSize: "1.05rem"
    fontWeight: 400
    lineHeight: 1.85
  hebrew:
    fontFamily: "SBL Hebrew, 'Times New Roman', serif"
    fontSize: "1.05em"
  label:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 600
    letterSpacing: "0.06em"
  fine:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "0.78rem"
    fontWeight: 700
    letterSpacing: "0.06em"
  caption:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "0.92rem"
    fontStyle: "italic"
  meta:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "0.95rem"
    fontWeight: 700
  small:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "0.97rem"
    fontWeight: 400
  detail:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "0.99rem"
    fontWeight: 400
  micro:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "0.72rem"
    fontWeight: 700
  callout-title:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 800
rounded:
  pill: "999px"
  card: "12px"
  lg: "20px"
  xs: "5px"
  sm: "6px"
  r9: "9px"
  r10: "10px"
  r14: "14px"
  r16: "16px"
spacing:
  container-session: "56rem"
  container-portal: "80rem"
  gutter: "1.5rem"
components:
  button-pill:
    backgroundColor: "transparent"
    textColor: "#475569"
    rounded: "{rounded.pill}"
    padding: "0.375rem 1rem"
  course-card:
    backgroundColor: "{colors.bg}"
    textColor: "#0f172a"
    rounded: "16px"
    padding: "1.5rem"
  scripture:
    backgroundColor: "transparent"
    textColor: "{colors.body}"
    padding: "0.25rem 0 0.25rem 1.25rem"
  nav-lang:
    backgroundColor: "{colors.bg}"
    textColor: "#475569"
    rounded: "{rounded.pill}"
    padding: "0.375rem 0.875rem"
---

# Design System: Estudos Bíblicos — The Bible Project

## Overview

**Creative North Star: "The Annotated Lecture Hall"** — the reading experience of a well-set seminary reader: calm white pages, a confident near-black ink, and a single disciplined blue that marks every cross-reference, alongside a color-coded system that turns dense biblical structure (chiasms, genealogies, macro outlines) into legible diagrams. The product is a bilingual (Portuguese/English) library of course "class notes" from The Bible Project, so the visual job is comprehension-first: long-form reading that stays quiet, Hebrew set correctly right-to-left, and scripture quotations clearly walled off from commentary.

Two surfaces share one identity. The **portal** (`index.html`) is a Tailwind-v3 CDN grid of course cards — the browse/discover face. The **session pages** (`<course>/modulo-N/sessao-N.html`) are Tailwind-v4 (`@tailwindcss/browser`) reading pages carrying a shared editorial stylesheet (`style.css`-equivalent inline `<style>`). Both surface a PT/EN language toggle stored in `localStorage` and gated by `html[lang]`.

Every session page reuses the **same class vocabulary** (`h1.title`, `h2.section`, `h3.sub`, `p.body`, `.rule`, `.scripture`, `.bullets`, `.reveal`, `.page-footer`, reading-progress bar), so the courses are recolor variants of one template, not separate designs. Two documented expressions of that template exist: the **Reader template** (canonical, ~350 pages across Jonah, Joseph, Jacob, Exodus, Ezekiel, Adam-to-Noah, Messianic-Torah, Art-of-Biblical-Words, Intro-Hebrew, Heaven-and-Earth, Noah-to-Abraham, and Abraham modules 1–6) and the **Abraham cx-callout system** (the richest diagram vocabulary, used in the Abraham module). A few courses add a deliberate *course accent* (see Variants).

**Key Characteristics:**
- Calm white reading canvas; structure via 2–4px borders and tints, not by heavy shadows.
- One blue accent (`#0284c7` sky / `#2563eb` for inline scripture refs) used sparingly: links, active language, hover borders.
- A signature **color-coded callout system** (`cx-*`) that assigns each theme a hue + tinted fill so recurring diagrams stay recognizable (Abraham module).
- Bilingual by construction: every string ships as `.lang-pt` / `.lang-en` pairs toggled together.
- Hebrew set in SBL Hebrew, forced RTL; poems and pull-quotes set in Newsreader serif for a contemplative beat.

## Colors

A near-monochrome ink-and-paper base, an editorial blue accent, and a fixed categorical palette for the callout/diagram system. The cx callout hues (below) are the only place multiple saturated colors appear, and they are always paired with a matching tint so they read as a system, not as decoration.

### Primary
- **Bible-Project Sky** (`#0284c7`, Tailwind `sky-600`): the brand accent on the portal — active language pill, course-card hover border (`sky-500`), and the "Start here" emerald / "Under construction" amber badges' sibling. Used sparingly; its rarity is the point.
- **Reference Blue** (`#2563eb`, `blue-600`): the hover color of inline scripture/verse links (`.ref:hover`) and the verse-modal title text. Treat as the same accent family as Sky; the two are near-indistinguishable at a glance.

### Neutral (Reader template — canonical)
- **Ink** (`#1a1a1a`): body text and bullet markers (`body { color:#1a1a1a }`, `ul.bullets>li:before`). Near-black, not pure black.
- **Body** (`#24262a`): paragraph (`.body`) and scripture text.
- **Heading Ink** (`#17181a`): scripture labels only.
- **Muted** (`#5b6472` / `#5b7285`): captions, footnotes, secondary labels, scripture translation tags.
- **Borders:** `#d7dde5` (`.rule`, `.table-img`), `#aeb6bf` (`.quote` rule), `#d7d7df` (nav pill), `#dfe4ea` (`.scripture` rule) — the dominant depth cues.
- **Surface** (`#f1f5f9`): nav hover fill.
- **Quote Text** (`#3a3f47`): `.quote` / `.poem` body.
- **Nav Text** (`#475569`): floating control labels.
- **Paper** (`#ffffff`): page and card backgrounds.

### Neutral (Abraham cx-callout module)
The Abraham module's inline `<style>` uses `#17181a` ink, `#24262a` body, `#5b6472` muted, `#d7dde5`/`#e3e7ee` borders, and `#f6f8fa` inset surface — the same neutrals as the Reader template with marginally different hexes (e.g. `#17181a` vs `#1a1a1a`, `#e3e7ee` vs `#d7dde5`). Treat as the same neutral family; the drift is intra-template, not a defect.

### Categorical — cx callout system
`cx-slate` `#6b7280`, `cx-rust` `#c0562f`, `cx-rose` `#c04a63`, `cx-blue` `#5468d4`, `cx-green` `#2e7d4e`, `cx-purple` `#8b5cf6`, `cx-tan` `#8a6d3b`, each with its `#e9ebee`/`#f7e6dd`/`#f7e0e5`/`#e4e8f9`/`#dfeee2`/`#efe2f8`/`#ece7dc` tint. Plus annotation chips `k-blue` `#3b82c4`, `k-green` `#2e6b4e`, `k-rose` `#c04a63`, `k-teal` `#0d7d8c`, `k-purple` `#7c5ad0`, `t-teal` `#0d8aa0`. Always border + matching tint.

### Variants (course-specific accents — intentional, not defects)
- **Amber scripture accent** (Ephesians, 1 Corinthians): `blockquote` left-rule `#f59e0b` (`amber-badge`) on a `#fffbeb` (`amber-badge-bg`) tint. A deliberate course accent, distinct from the blue primary.
- **Abraham module 2–6 extended palette**: a richer per-module categorical set (teals `#0c7c99`/`#0d7685`, roses `#972a4e`/`#823221`, blues `#3b5299`/`#1d4ed8`, tans `#8a6d3b`/`#b45f06`, greens `#38761d`/`#2e8b57`, purples `#6d4cba`/`#7c3aed`). Used only inside those modules' custom diagrams; not part of the shared scale.

### Named Rules
**The One-Blue Rule.** A single blue/sky accent carries all interactive emphasis (links, active language, hover borders). Introduce no new *interactive* hue; the cx callout and course accents are categorical/decorative, never used for links or buttons.

**The Tint-Not-Shadow Rule.** Depth is conveyed by borders and tonal fills (`#f1f5f9`, tinted callouts), not by resting drop shadows. The only resting shadow is the 1px hairline `0 1px 3px rgba(0,0,0,.06)` on floating nav controls; larger shadows appear only on hover/overlay.

## Typography

**Display Font:** Inter (with `system-ui, sans-serif` fallback) — every heading, label, UI control, and body paragraph.
**Body Font:** Inter, same stack.
**Serif Font:** Newsreader (with Georgia, serif) — reserved for poems (`.poem`) and pull-quotes (`.quote`); its italic optical size gives commentary a contemplative, "readerly" beat without leaving the system.
**Hebrew Font:** SBL Hebrew (with `Times New Roman`, serif) — `direction: rtl; unicode-bidi: embed` so Hebrew terms render correctly inline.

**Character:** A precise, slightly compressed sans (Inter at 800 weight, negative letter-spacing) for a scholarly-but-modern voice; the serif body provides the only warmth. Newsreader is never a heading face here — it is a readerly accent, not a display choice.

### Hierarchy
- **Display** (800, 2.6rem, line-height 1.08, -0.025em): session `<h1 class="title">` — the lesson title only.
- **Section** (800, 1.9rem, -0.015em): `<h2 class="section">` major topical breaks; 3rem top / 1.25rem bottom margin.
- **Sub** (800, 1.3rem, -0.01em): `<h3 class="sub">` subsection and "Reflection Question" headings.
- **Body** (400, 1.05rem, line-height 1.78, color `#24262a`): default paragraph (`.body`), max readable measure inside `max-w-4xl`.
- **Label / Eyebrow** (600, 0.875rem, uppercase, 0.06em tracking, muted): scripture translation tags, footer, kickers.
- **Serif Quote** (400, 1.05rem, line-height 1.85, Newsreader): `.poem` / `.quote` blocks.
- **Hebrew Inline** (1.05em, SBL Hebrew, RTL): primary font for inline Hebrew terms.

### Named Rules
**The Serif-Is-Readerly Rule.** Newsreader appears only for poems and pull-quotes. Never use it for headings, UI, or body paragraphs; the page stays Inter except where a quotation deserves a different register.

**The RTL Lock Rule.** Any Hebrew string uses `.heb` with `direction: rtl`. Never strip RTL or let Hebrew terms inherit LTR flow — bilingual integrity depends on it.

## Layout

Two distinct spatial models from one token set:
- **Portal:** centered `max-w-7xl` (`80rem`) shell, course grid `gap-8` collapsing `md:grid-cols-2 lg:grid-cols-3`; cards are `rounded-2xl` with a `h-44` (`11rem`) `object-cover` cover image and a `p-6` text block.
- **Session pages:** a single reading column `max-w-4xl` (`56rem`), `px-5 md:px-10 py-12 md:py-16`, left-aligned. Content is long-form: title → `hr.rule` → subsections of heading + body + scripture blocks. Fixed top-left "Back" (`← Voltar`) and top-right "Print / Imprimir + PT|EN" controls float above the column (`print:hidden`).

Responsive behavior is breakpoint-driven by Tailwind utilities plus two bespoke `@media` blocks (in the Abraham module): the macro-outline grid collapses `1fr` under `860px`, and the Isaiah-51 genealogy rows stack under `640px`. Vertical rhythm is generous (`1.5–2.75rem` rule spacing, `3rem` between sections) to keep long reads breathable.

## Elevation & Depth

Predominantly **flat**, conveyed through 2–4px borders and tonal fills rather than shadows. Surfaces at rest cast nothing except the 1px hairline on floating nav controls.

### Shadow Vocabulary
- **Hairline (resting)** (`0 1px 3px rgba(0,0,0,.06)`): on `.nav-btn` / floating controls — the only intentional resting shadow.
- **Hover lift — card** (`0 8px 20px -10px rgba(30,41,59,.4)`): on `.mbox` / `.cx` callouts on hover, paired with `translateY(-2px / -3px)`.
- **Hover lift — portal card** (Tailwind `shadow-xl`): on course-card hover, with `-translate-y-1` and `border-sky-500`.
- **Overlay** (`shadow-xl` + `bg-black/50` scrim): the verse modal panel (`max-w-lg rounded-lg bg-white p-6`).

### Named Rules
**The Flat-By-Default Rule.** Reading-page surfaces are flat at rest. A drop shadow may appear only on hover/focus/overlay state (or the documented 1px nav hairline); never as a static resting style on content surfaces.

## Shapes

Rounded corners are explicit and modest: pills (`999px`) for language toggles and nav controls; `12px` radii for tables/images; `16–20px` for outer frames. Borders are the signature form language — hairline `1px` for tables/rules/nav, confident `3px` for Abraham-module callouts, macro boxes, and outer frames. No skewed or organic geometry; the silhouette is rectangular and calm.

## Components

### Buttons / Pill Controls
- **Shape:** pill (`999px`) with a `1px` slate-300 (`#cbd5e1`) border; `bg-white/90` + `backdrop-blur-xs` on floating controls (Back / Print), plain white on the language toggle (Reader) or `#fff`/`#d7d7df` on `.nav-btn`.
- **Primary (active language):** `bg-sky-600 text-white`. **Off:** `bg-white text-slate-600 hover:bg-slate-100` (portal) or `bg-white text-slate-600 hover:bg-slate-50` (session).
- **Hover/Focus:** color shift + subtle bg change; `transition-colors`.

### Course Card (portal)
- **Shape:** `rounded-2xl` (16px), `border-2` slate-200, white bg, `overflow-hidden`.
- **Cover:** `h-44 w-full object-cover`.
- **Body:** title `text-2xl font-bold text-slate-900` → `group-hover:text-sky-600`; reference label `text-sm font-semibold uppercase tracking-wider text-slate-500`; description `text-sm text-slate-600`.
- **Hover:** border-sky-500, `shadow-xl`, `-translate-y-1`.
- **Status badge:** pill, top-right — emerald-100 bg / emerald-700 text ("Start here") or amber-100 bg / amber-700 text ("Under construction").

### Scripture Block
- **Style:** `border-left: 4px solid #dfe4ea`, padding `0.25rem 0 0.25rem 1.25rem`, `transition: border-color .2s`.
- **Label:** `font-weight 800` ink (`#17181a`); **type tag:** muted 700 (`NVI` / `NASB`).
- **Text:** `1.05rem`, line-height `1.8`, color `#24262a`. Optional inset box (`#f6f8fa` in Abraham module).
- **Hover:** border-left shifts to `#9aa7b8`.

### Quote / Poem
- **Style:** `border-left: 4px solid #aeb6bf`, padding `.4rem 0 .4rem 1.25rem`; text `#3a3f47`, italic, Newsreader when `.poem`.
- **Variant:** Ephesians/1 Corinthians use `#f59e0b` amber rule on `blockquote` over `#fffbeb` tint.

### Signature Component — Color-Coded Callout (`cx-*`, Abraham module)
The defining pattern: a `3px` colored border + matching tinted fill, a white-on-color tag pill, and a hover lift. Reused so recurring structures (chiasms, themes) stay visually consistent.
- **cx-slate** `#6b7280` / `#e9ebee` · **cx-rust** `#c0562f` / `#f7e6dd` · **cx-rose** `#c04a63` / `#f7e0e5` · **cx-blue** `#5468d4` / `#e4e8f9` · **cx-green** `#2e7d4e` / `#dfeee2` · **cx-purple** `#8b5cf6` / `#efe2f8` · **cx-tan** `#8a6d3b` / `#ece7dc`.
- Hover: `box-shadow 0 12px 26px -16px rgba(23,24,26,.45)` + `translateY(-2px)`.

### Verse Modal
Injected by the shared `js/verse-modal.js`. Fixed `inset-0 z-50` `bg-black/50` scrim; panel `w-full max-w-lg rounded-lg bg-white p-6 shadow-xl`; title `text-xl font-bold text-slate-900`; body `max-h-[60vh] overflow-y-auto text-slate-700`. Fetches from `bible-api.com` on `.ref` / `.verse-link` click.

### Reading Progress Bar
Fixed top, `height: 3px`, full width, `bg #1a1a1a` (Reader) / `#17181a` (Abraham), `transform: scaleX(0→1)` driven by scroll. `aria-hidden`; hidden in print.

### Tables (`.doc-table` / `.table-img`)
`border-collapse: separate`, `3px` border `#d9dee6`, `rounded-14`, `overflow: hidden`; or a 1px `#d7dde5` border with `rounded-12` for image tables. Header `th` `bg #e2e6eb`, `font-weight 800`, ink; rows hover `#f8fafc` / `#f1f5f9`.

### Navigation
Floating controls + the PT/EN split toggle (documented under Buttons). Mobile: controls stay fixed top-left/right; grid collapses to one column.

## Do's and Don'ts

### Do:
- **Do** keep Inter for all UI, headings, and body; reserve Newsreader for `.poem` / `.quote` only.
- **Do** set Hebrew in `.heb` with RTL — never let Hebrew terms flow LTR.
- **Do** convey depth with borders and `#f1f5f9`/`#f6f8fa` tints; the only resting shadow is the 1px nav hairline.
- **Do** reuse the `cx-*` hue set consistently for callouts; pair each border with its tinted fill.
- **Do** keep session reading width at `max-w-4xl` and preserve the PT/EN toggle + reading-progress bar.

### Don't:
- **Don't** introduce a new *interactive* accent color — links, active language, and hover borders stay in the blue/sky family.
- **Don't** apply resting drop shadows to reading-page content surfaces (cards, callouts, tables).
- **Don't** drop or restyle the bilingual `.lang-pt` / `.lang-en` toggle; it is the product's core control.
- **Don't** use Newsreader or SBL Hebrew as a display/UI face.
- **Don't** break `print` rules (`@media print` hides progress bar/controls) — print fidelity is a requirement.
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
