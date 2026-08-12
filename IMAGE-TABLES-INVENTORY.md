# Sessions with DATA TABLES rendered as images (DESIGN.md deviation)

**Generated:** 2026-08-11
**Scope:** All `sessao-*.html` under the repo (447 session files, 597 `<img>` references across 14 courses).
**Method:** Pixel grid heuristic pre-filtered candidates; each candidate confirmed by vision (TABLE vs NOT-TABLE).
**Rule (DESIGN.md):** Tables must be semantic HTML `<table>` + bilingual `lang-pt`/`lang-en` spans, not images.

## Verified data tables still rendered as `<img>` (convert to `<table>`)

| Session file | Image (table rendered as picture) | Topic |
|---|---|---|
| `jacob/modulo-1/sessao-4.html` | `img/sessao-4/p10-vector.png` | Like Father Avraham / Like Son Yaaqov comparison (3 col) |
| `jacob/modulo-2/sessao-10.html` | `img/sessao-10/p6-vector.png` | Jacob narrative comparison table |
| `jacob/modulo-5/sessao-22.html` | `img/sessao-22/p6-vector.png` | Jacob/Esau comparison table |
| `messianic-torah/modulo-1/sessao-2.html` | `img/sessao-2/p10-vector.png` | Matthew 4:23-25 × Mark compositional strategy (2 col) |

## Data tables present on disk but NOT currently referenced by their session HTML

These were likely already converted to `<table>`, or the image is orphaned. Confirm before re-converting:

| Session file | Image | Note |
|---|---|---|
| `jacob/modulo-1/sessao-4.html` | `img/sessao-4/p6-vector.png` | on disk, not in current `<img>` set |
| `messianic-torah/modulo-1/sessao-2.html` | `img/sessao-2/p12-vector.png` | Matthew 4:23-25 × Mark parallel (2 col) — on disk, not referenced |
| `messianic-torah/modulo-3/sessao-15.html` | `img/sessao-15/p3-compare.png` | Matthew 6:19-34 × 7:1-11 — on disk, not referenced |

## Already converted (per `TABELAS-EM-IMAGEM.md`) — now `<table>` not `<img>`

- `noah-to-abraham/modulo-1/sessao-8.html` / `sessao-7.html` — Genesis × Gilgamesh tables
- `jacob/modulo-1/sessao-4.html` — `p1-vector` / `p6-vector` (Like Father…) — verify; some still show `<img>`
- `jacob/modulo-4/sessao-18.html` — Yaaqov's Speech (Genesis 31) — vision: NOT a grid table (prose comparison)
- `messianic-torah/modulo-1/sessao-2.html` — `p12-vector`, `p10-vector` (see above, partially still `<img>`)
- `messianic-torah/modulo-2/sessao-15.html` — `p3-compare.png` (see above, not referenced)

## Notes / non-tables checked (so they're excluded)

The bulk of `*-vector.png` / `*-page.png` images are **literary-outline pages, diagrams, or illustrations** (e.g. Genesis 1 creation structure, tabernacle layout, chiastic outlines, photos like Mona Lisa / Hubble / Van Gogh used as analogies). These are legitimate illustrations, NOT tables, and should stay as images per DESIGN.md.

**Caveat:** Vision classification is the source of truth here; the pixel-grid heuristic was unreliable (real tables have light borders that don't trip a dark-line threshold, while diagrams with full-width highlight bars do). Only the images vision-labeled TABLE are listed above.
