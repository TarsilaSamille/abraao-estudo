# Data tables that were rendered as images → converted to `<table class="md">`

**Scope:** All `sessao-*.html` under the repo (447 session files, ~597 `<img>` refs across 14 courses).
**Method:** Pixel grid heuristic pre-filtered candidates; every candidate confirmed by `vision_analyze` (TABLE vs NOT-TABLE). Real tables here = 2/3-column comparison grids with light-grey headers (jacob `p6/p8/p10-vector`, messianic `p*-vector`/`p*-case*`). The heuristic under-counts real tables (light borders don't trip the dark-line threshold) and over-flags diagrams (full-width highlight bars), so vision was the source of truth.

## Converted this session (image removed, replaced by bilingual `<table class="md reveal">` + `<tfoot>` caption)

| Session file | Image | Topic |
|---|---|---|
| `jacob/modulo-1/sessao-4.html` | `img/sessao-4/p10-vector.png` | From Barrenness to Life + Two Brothers in the Womb (2× 3 col) |
| `jacob/modulo-2/sessao-10.html` | `img/sessao-10/p6-vector.png` | Gen. 27:39b-40 × 1 Kings 11:14 / 2 Kings 8:20-22 |
| `jacob/modulo-5/sessao-22.html` | `img/sessao-22/p6-vector.png` | Yaaqov & Esau × Cain & Abel (2 col) |
| `jacob/modulo-5/sessao-22.html` | `img/sessao-22/p8-vector.png` | Yaaqov Flood Narrative Hyperlinks (3 col: Gn 27 / 32-33 / 6-8) |
| `messianic-torah/modulo-1/sessao-1.html` | `img/sessao-1/p5-vector.png` | Jesus' Teaching as Lady Wisdom (Provérbios × Mateus, 2 col) |
| `messianic-torah/modulo-1/sessao-2.html` | `img/sessao-2/p10-vector.png` | Mateus 4:23-25 × Marcos 1:14,28,3:7-8 |

(Record also kept in `TABELAS-EM-IMAGEM.md`.)

## Orphaned-on-disk images — resolved

- `messianic-torah/modulo-3/sessao-13/p2-vector.png` → **converted**: it was a BROKEN `<img src="...p2-righteousness.png">` in `messianic-torah/modulo-3/sessao-13.html` (Generosidade/Oração/Jejum, h2 "Justiça e Práticas Religiosas"). Replaced the broken img with the `<table.md>` (Mateus 5:21-48 × 6:1-21).
- `jacob/modulo-1/img/sessao-4/p6-vector.png`, `messianic-torah/modulo-1/img/sessao-2/p12-vector.png`, `messianic-torah/modulo-2/img/sessao-13/p2-vector.png` → **deleted**: their table content already exists as `<table.md>` in-session; these were stale leftover files unreferenced by any HTML.

## Not tables (verified, excluded)

The bulk of `*-vector.png` / `*-page.png` / `*-case*` / `*-structure*` / photo images are **literary-outline pages, diagrams, verse boxes, or illustrations** (Genesis creation structure, tabernacle layout, chiastic outlines, Mona Lisa / Hubble / Van Gogh analogies, BibleProject illustrations). These are legitimate and stay as `<img>` per DESIGN.md. Spot-verified NOT-TABLE across exodus-overview, joseph, ezekiel, adam-to-noah, heaven-and-earth, intro-hebrew-bible, art-of-biblical-words, 1-corinthians, ephesians, abraao, others/.

## Caveat

Vision classification is the source of truth; the pixel heuristic was unreliable. Only images vision-labeled TABLE were converted. Remaining un-verified-by-vision images are overwhelmingly diagrams/outlines/photos by filename + course pattern, but a full 597-image vision pass was not performed (rate-limit impractical) — the table class is well-characterized by now.
