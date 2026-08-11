---
name: Estudos Bíblicos — The Bible Project
description: Bilingual (PT/EN) biblical-study course portal and reading pages, built on Tailwind plus a custom editorial stylesheet.
colors:
  primary: "#0284c7"
  primary-link: "#2563eb"
  ink: "#17181a"
  ink-soft: "#1f2937"
  body: "#24262a"
  muted: "#5b6472"
  muted2: "#5b7285"
  caption: "#5b6472"
  border: "#d7dde5"
  border-soft: "#e3e7ee"
  border-soft2: "#e5e7eb"
  header-tint: "#e2e6eb"
  surface: "#f6f8fa"
  surface-div: "#e6eaf0"
  tfoot: "#d1d5db"
  bg: "#ffffff"
  rust: "#c0392b"
  emerald: "#059669"
  amber: "#d97706"
  scripture-rule: "#dfe4ea"
  scripture-hover: "#9aa7b8"
  mbox-hdr: "#7d8697"
  macro-dark: "#3d4453"
  sup: "#333333"
  kblue-soft-bg: "#cddcf5"
  kblue-soft-fg: "#2b5fb0"
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
  callout-title:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 800
  micro:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "0.72rem"
    fontWeight: 700
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

**Creative North Star: "The Annotated Lecture Hall"** — the reading experience of a well-set seminary reader: quiet white pages, a confident near-black ink, and a single disciplined blue that marks every cross-reference, alongside a color-coded system that turns dense biblical structure (chiasms, genealogies, macro outlines) into legible diagrams. The product is a bilingual (Portuguese/English) library of course "class notes" from The Bible Project, so the visual job is comprehension-first: long-form reading that stays calm, with Hebrew terms set correctly right-to-left and scripture quotations clearly walled off from commentary.

Two surfaces share one identity. The **portal** (`index.html`) is a Tailwind-v3 CDN grid of course cards — the browse/discover face. The **session pages** (`<course>/modulo-N/sessao-N.html`) are Tailwind-v4 (`@tailwindcss/browser`) reading pages carrying a bespoke `style.css` with the editorial type scale, the callout vocabulary, the fixed reading-progress bar, scroll-reveal, and a shared verse-modal. Both surface a PT/EN language toggle stored in `localStorage` and gated by `html[lang]`.

**Key Characteristics:**
- Calm, paper-white reading canvas; structure carried by 3px borders and tints, not by heavy shadows.
- One blue accent (`#0284c7` sky / `#2563eb` for inline scripture refs) used sparingly: links, active language, hover borders.
- A signature **color-coded callout system** (`cx-*`) that assigns each theme a hue + tinted fill so recurring diagrams stay recognizable across 12+ courses.
- Bilingual by construction: every string ships as `.lang-pt` / `.lang-en` pairs toggled together.
- Hebrew set in SBL Hebrew, forced RTL; poems and pull-quotes set in Newsreader serif for a contemplative beat.

## Colors

A near-monochrome ink-and-paper base, an editorial blue accent, and a fixed categorical palette for the callout/diagram system. The cx callout hues (below) are the only place multiple saturated colors appear, and they are always paired with a matching tint so they read as a system, not as decoration.

### Primary
- **Bible-Project Sky** (`#0284c7`, Tailwind `sky-600`): the brand accent on the portal — active language pill, course-card hover border (`sky-500`), and the "Start here" emerald / "Under construction" amber badges' sibling. Used sparingly; its rarity is the point.
- **Reference Blue** (`#2563eb`, `blue-600`): the hover color of inline scripture/verse links (`.ref:hover`) and the verse-modal title text. Treat as the same accent family as Sky; the two are near-indistinguishable at a glance.

### Neutral
- **Ink** (`#17181a`): headings (`h1.title`, `h2.section`, `h3.sub`), labels, and the reading-progress bar. Near-black, not pure black.
- **Body** (`#24262a`): paragraph and scripture text.
- **Muted** (`#5b6472` / `#6b7280`): captions, footnotes, secondary labels, scripture translation tags.
- **Border** (`#d7dde5` / `#e3e7ee` / `#d9dee6` / `#e5e7eb`): the 1–3px hairlines that define every surface; the dominant depth cue.
- **Surface** (`#f6f8fa`): inset fills — scripture inner boxes, genealogy column headers, table header tints.
- **Paper** (`#ffffff`): page background and card backgrounds.

### Named Rules
**The One-Blue Rule.** A single blue/sky accent carries all interactive emphasis (links, active language, hover borders). Introduce no new interactive hue; the cx callout palette is categorical, not interactive, and must never be used for links or buttons.

**The Tint-Not-Shadow Rule.** Depth on reading pages is conveyed by borders and tonal fills (`#f6f8fa`, tinted callouts), not by resting drop shadows. Shadows appear only as a hover/overlay response.

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
- **Hebrew Inline** (1.05em, SBL Hebrew, RTL): `.heb` spans inside body copy.

### Named Rules
**The Serif-Is-Readerly Rule.** Newsreader appears only for poems and pull-quotes. Never use it for headings, UI, or body paragraphs; the page stays Inter except where a quotation deserves a different register.

**The RTL Lock Rule.** Any Hebrew string uses `.heb` with `direction: rtl`. Never strip RTL or let Hebrew terms inherit LTR flow — bilingual integrity depends on it.

## Layout

Two distinct spatial models from one token set:
- **Portal:** centered `max-w-7xl` (`80rem`) shell, course grid `gap-8` collapsing `md:grid-cols-2 lg:grid-cols-3`; cards are `rounded-2xl` with a `h-44` (`11rem`) `object-cover` cover image and a `p-6` text block.
- **Session pages:** a single reading column `max-w-4xl` (`56rem`), `px-6 md:px-10 py-14`, left-aligned. Content is long-form: title → `hr.rule` → subsections of heading + body + scripture blocks. Fixed top-left "Back" (`← Voltar`) and top-right "Print / Imprimir + PT|EN" controls float above the column (`print:hidden`).

Responsive behavior is breakpoint-driven by Tailwind utilities plus two bespoke `@media` blocks: the macro-outline grid collapses `1fr` under `860px`, and the Isaiah-51 genealogy rows stack under `640px`. Vertical rhythm is generous (`1.5–2.75rem` rule spacing, `3rem` between sections) to keep long reads breathable.

## Elevation & Depth

Predominantly **flat**, conveyed through 1–3px borders and tonal fills rather than shadows. Surfaces at rest cast nothing; shadow is a *response* — hover lift on cards and callouts, and the modal overlay.

### Shadow Vocabulary
- **Hover lift — card** (`0 8px 20px -10px rgba(30,41,59,.4)`): on `.mbox` / `.cx` callouts on hover, paired with `translateY(-2px / -3px)`.
- **Hover lift — portal card** (Tailwind `shadow-xl`): on course-card hover, with `-translate-y-1` and `border-sky-500`.
- **Overlay** (`shadow-xl` + `bg-black/50` scrim): the verse modal panel (`max-w-lg rounded-lg bg-white p-6`).

### Named Rules
**The Flat-By-Default Rule.** Reading-page surfaces are flat at rest. A drop shadow may appear only on hover/focus/overlay state; never as a static resting style.

## Shapes

Rounded corners are explicit and modest: pills (`999px`) for language toggles and status badges; `12–16px` radii for cards, callouts, and tables; `20px` for the outer verse/illustration frames (`.v-outer`). Borders are the signature form language — hairline `1px` for tables/rules, confident `3px` for callouts, macro boxes, and the outer frames. Clipping is minimal (cover images `object-cover`, table `overflow: hidden` for the rounded corners). No skewed or organic geometry; the silhouette is rectangular and calm.

## Components

### Buttons / Pill Controls
- **Shape:** pill (`999px`) with a `1px` slate-300 (`#cbd5e1`) border; `bg-white/90` + `backdrop-blur-xs` on floating controls (Back / Print), plain white on the language toggle.
- **Primary (active language):** `bg-sky-600 text-white`. **Off:** `bg-white text-slate-600 hover:bg-slate-100`.
- **Hover/Focus:** color shift + subtle bg change; `transition-colors`.

### Course Card (portal)
- **Shape:** `rounded-2xl` (16px), `border-2` slate-200, white bg, `overflow-hidden`.
- **Cover:** `h-44 w-full object-cover`.
- **Body:** title `text-2xl font-bold text-slate-900` → `group-hover:text-sky-600`; reference label `text-sm font-semibold uppercase tracking-wider text-slate-500`; description `text-sm text-slate-600`.
- **Hover:** `-translate-y-1`, `border-sky-500`, `shadow-xl`.
- **Status badge:** pill, top-right — emerald-100 bg / emerald-700 text ("Start here") or amber-100 bg / amber-700 text ("Under construction").

### Scripture Block
- **Style:** `border-left: 4px solid #dfe4ea`, padding `0.25rem 0 0.25rem 1.25rem`, `transition: border-color .2s`.
- **Label:** `font-weight 800` ink; **type tag:** muted 700 (`NVI` / `NASB`).
- **Text:** `1.05rem`, line-height `1.8`, color `#24262a`. Optional `.innerbox` (`#f6f8fa`, `rounded-10`, padding `1rem 1.25rem`) for adaptation notes.
- **Hover:** border-left shifts to `#9aa7b8`.

### Signature Component — Color-Coded Callout (`cx-*`)
The defining pattern: a `3px` colored border + matching tinted fill, a white-on-color tag pill, and a hover lift. Each course reuses the same seven hues so recurring structures (chiasms, themes) stay visually consistent.
- **cx-slate** `#6b7280` / `#e9ebee` · **cx-rust** `#c0562f` / `#f7e6dd` · **cx-rose** `#c04a63` / `#f7e0e5` · **cx-blue** `#5468d4` / `#e4e8f9` · **cx-green** `#2e7d4e` / `#dfeee2` · **cx-purple** `#8b5cf6` / `#efe2f8` · **cx-tan** `#8a6d3b` / `#ece7dc`.
- Hover: `box-shadow 0 12px 26px -16px rgba(23,24,26,.45)` + `translateY(-2px)`.

### Verse Modal
Injected by the shared `js/verse-modal.js`. Fixed `inset-0 z-50` `bg-black/50` scrim; panel `w-full max-w-lg rounded-lg bg-white p-6 shadow-xl`; title `text-xl font-bold text-slate-900`; body `max-h-[60vh] overflow-y-auto text-slate-700`. Fetches from `bible-api.com` on `.ref` / `.verse-link` click.

### Reading Progress Bar
Fixed top, `height: 3px`, full width, `bg #17181a`, `transform: scaleX(0→1)` driven by scroll. `aria-hidden`; hidden in print.

### Tables (`.doc-table`)
`border-collapse: separate`, `3px` border `#d9dee6`, `rounded-14`, `overflow: hidden`. Header `th` `bg #e2e6eb`, `font-weight 800`, ink; rows `td` `1.1rem 1.3rem`, hover `bg #f8fafc`; `tbody tr:hover td` tint.

### Navigation
Floating controls + the PT/EN split toggle (documented under Buttons). Mobile: controls stay fixed top-left/right; grid collapses to one column.

## Do's and Don'ts

### Do:
- **Do** keep Inter for all UI, headings, and body; reserve Newsreader for `.poem` / `.quote` only.
- **Do** set Hebrew in `.heb` with RTL — never let Hebrew terms flow LTR.
- **Do** convey depth with borders and `#f6f8fa` tints; add shadows only on hover/overlay.
- **Do** reuse the `cx-*` hue set consistently for callouts; pair each border with its tinted fill.
- **Do** keep session reading width at `max-w-4xl` and preserve the PT/EN toggle + reading-progress bar.

### Don't:
- **Don't** introduce a new interactive accent color — links, active language, and hover borders stay in the blue/sky family.
- **Don't** apply resting drop shadows to reading-page surfaces (cards, callouts, tables).
- **Don't** drop or restyle the bilingual `.lang-pt` / `.lang-en` toggle; it is the product's core control.
- **Don't** use Newsreader or SBL Hebrew as a display/UI face.
- **Don't** break `print` rules (`@media print` hides progress bar/controls and forces `.reveal` visible) — print fidelity is a requirement.
