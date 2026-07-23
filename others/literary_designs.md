# Literary-Design Taxonomy — abraao-estudo (Abraham Classroom)

Auto-categorized from a class-vocabulary scan of all 30 session HTML files
(`abraao/modulo-*/sessao-*.html`). Use this to **facilitate** verification:
each family has a known PDF-source shape and a known check strategy.

## The 4 (+1) families

| # | Family | Sessions | PDF-source shape | Primary fidelity risk |
|---|--------|----------|-----------------|----------------------|
| 1 | **VERSE / INTERLINEAR grid** | S1,S2,S3,S4,S5,S6,S7,S8,S9,S10,S12,S13,S14 (13) | bilingual `grid-cols-[20px_1fr]` rows, `.verse-link` spans | column alignment, verse-link color (must be `color:inherit`, NOT blue/underlined — see memory), EN-glosa italics |
| 2 | **WORD-STUDY highlights** | S16,S17,S18,S19,S20,S21,S22,S23,S24,S25,S26,S27,S28 (13) | `highlight-*` colored chips (gray/pink/blue/orange/purple/green/gold/velhice/brown) | exact palette per memory; the PDF uses specific hex; Brownson/velhice are NOT purple |
| 3 | **MACRO (3-step A/B/A′ chiasm)** | S15 (1) | 3 stacked `.macro-box` (A / B indented / A′), `mbadge-grey` ref pills, `hl-*` lines | border 2px #6B7384, single-line body, bold A/B/A′ letters, B indented |
| 4 | **HL poetic / divine lines** | (subset of above, e.g. S15 has hl-green/hl-divine/hl-mult) | `.hl` colored lines (green/blue/divine/mult) | line color vs exact palette; divine = #5869CD |
| 5 | **OTHER / general** | S11, S29, S30 (3) | mixed / narrative | per-session inspection |

> Note: SPEECH/REF boxes (`sp-*`, `ref-*`) appear inside several families (esp.
> word-study and macro) as sub-components, not standalone sessions.

## How to verify each family (fast + correct)

Two complementary DEV/VERIFY tools (NOT the forbidden `npm run test` suite):

### A) `others/diff_pdf_html.py`  (semantic, deterministic, ~5s) — PREFERRED
Extracts border px/color, letter-bold, and line-wrap from BOTH the PDF
(PyMuPDF) and the rendered HTML (Playwright `getComputedStyle`) and diffs
numerically. Catches real defects on bordered designs (macro, speech, ref).
```
python3 others/diff_pdf_html.py abraao/modulo-3/sessao-15.html 103 --sel ".macro-box"
```
- Works for ANY bordered container (`.macro-box,.sp-*,.ref-*,.hl-*`) because it
  matches PDF boxes ↔ HTML boxes by label text, then compares border/bold/line.
- Limitation: does not measure background **fill** color (highlights) — those
  are verified against the exact palette in MEMORY (measure, don't eyeball).

### B) `others/pixdiff_pdf_html.py`  (Architecture-2 text-masked pixel diff) — EXPERIMENTAL
Rasterizes HTML (text hidden) + PDF (text masked), slides a PDF-height window
to align, and reports structural-change %. **Honest limitation:** the HTML
sessions and the PDF lay out the same content at *non-uniform* scales (compact
HTML vs. tall, widely-spaced PDF page). A uniform stretch aligns extents but
smears edges and produces unreliable % (clean page can read >15%, and a real
defect can read *lower* than clean). **Do not use its PASS/FAIL as proof.**
Keep it only for a rough visual diff PNG (`--out`) to eyeball gross breaks.

## PDF page mapping
Each session's source pages live in `abraao/pdf-images/page_N.png` (0-indexed =
PDF page N). From memory: S15 = PDF pp.101–115 (idx 100–114), macro design on
p104 (= page_103.png). For other sessions, find the matching `page_N.png` by
the page's English heading before running a diff.

## Next-step facilitation
To extend `diff_pdf_html.py` to families 1–2 (grids, highlights) without
per-design hardcoding, add a fill-color extractor: PDF `get_drawings()` exposes
each rectangle's `fill` color; match the HTML element's `backgroundColor` by
label and diff hex. That closes the only gap the semantic tool has today
(background fills). Pixel-diff is NOT the path for this repo.
