#!/usr/bin/env python3
"""
pdf_palette.py — remap the Abraao sessions onto the teacher-notes PDF palette.

The sessions were normalised onto DESIGN.md tokens, which moved the pages away
from the PDFs they are supposed to reproduce. The PDF is the authority. This
holds the palette extracted from all 30 teacher-notes PDFs and the role mapping
that takes each token back to it.

The palette was extracted with PyMuPDF over abraao/pdf-sessoes/*.pdf:
  #1b1b1b 30206 · #4f5669 3258 · #e4e8ed 2090 · #2c2c2c 442 · #6b7384 390
  #404ca6 284 · #91362e 258 · #645537 235 · #972a4e 213 · #be4967 211
  #3a8060 210 · #5d4897 189 · #2b6146 187 · #816f4d 176 · #d9ecfd 173
  #7e62bc 171 · #b5543a 164 · #00626f 161 · #fae4c4 144 · #713c92 135
  #d3f2cd 130 · #e6e6fa 120 · #efe8db 119 · #245791 113 · #5869cd 107
  #181d36 106 · #097d8d 104 · #f9e3de 99 · #3678b4 98 · #3e4054 93
  #f7e1f5 82 · #ccf1fa 75 · #b9eff7 74 · #9855af 58 · #c1c9d0 30

Usage:
    python3 tools/pdf_palette.py --check abraao/modulo-2/sessao-5.html
    python3 tools/pdf_palette.py --apply abraao/modulo-2/sessao-5.html
    python3 tools/pdf_palette.py --apply abraao          # whole course
"""
import argparse
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- neutrals: the PDF is almost monochrome -------------------------------
INK = "#1b1b1b"        # 30206 spans. every body/heading/bullet colour
CAPTION = "#4f5669"    # 3258. captions, labels, scripture type, quote text
HAIRLINE = "#e4e8ed"   # 2090. borders and table chrome
FOOTER = "#2c2c2c"     # 442. page footer only
RULE = "#c1c9d0"       # 30. the rule under the session title
GRAY = "#6b7384"       # 390. neutral panel / gray badge

# --- categorical hues: PDF has a deeper, richer set than the DESIGN tokens ---
HUE = {
    # green
    "#2e7d4e": "#3a8060", "#dfeee2": "#d3f2cd", "#2e6b4e": "#2b6146",
    # gray / slate
    "#6b7280": GRAY, "#e9ebee": HAIRLINE,
    # dark macro panel
    "#3d4453": "#3e4054", "#45495d": "#3e4054", "#7d8697": GRAY,
    # blue / indigo
    "#5468d4": "#404ca6", "#4a5ecb": "#5869cd", "#e4e8f9": "#d9ecfd",
    "#dce9f6": "#ccf1fa", "#cddcf5": "#d9ecfd", "#2b5fb0": "#245791",
    "#3678b4": "#3678b4",
    # rose / red
    "#c04a63": "#be4967", "#f7e0e5": "#f9e3de", "#c0562f": "#b5543a",
    "#f7e6dd": "#fae4c4", "#bf5a2b": "#b5543a", "#823221": "#91362e",
    "#972a4e": "#972a4e",
    # tan / brown
    "#8a6d3b": "#816f4d", "#ece7dc": "#efe8db", "#b45f06": "#645537",
    # purple
    "#8b5cf6": "#7e62bc", "#efe2f8": "#e6e6fa", "#7c5ad0": "#5d4897",
    "#6d4cba": "#713c92", "#7c3aed": "#9855af", "#f7e1f5": "#f7e1f5",
    # teal
    "#0d7d8c": "#097d8d", "#0d8aa0": "#00626f", "#0c7c99": "#097d8d",
    # tints already in the PDF
    "#f6f8fa": "#efe8db",
    # stragglers found while comparing the sessions
    "#cbd5e1": HAIRLINE, "#e8ebf0": HAIRLINE, "#eef0f4": HAIRLINE,
    "#d9dee7": HAIRLINE, "#e5e9f0": HAIRLINE, "#d9dee6": HAIRLINE,
    "#64748b": GRAY, "#8a93a3": FOOTER, "#475569": CAPTION,
    "#ead9ee": "#e6e6fa",   # purple highlight wash
    "#f3e0c9": "#fae4c4",   # orange highlight wash
    "#f1f5f9": "#e4e8ed",
}

# --- role fixes: a token used in the wrong role goes to the PDF's role colour
ROLE = [
    # every body-text colour collapses onto the single ink
    (r'\bcolor:\s*#(?:24262a|17181a|1a1a1a|334155|475569|202020|242424|252525|1f2937|374151|0f172a|1e293b|111827)\b',
     f'color: {INK}', "ink"),
    # Tailwind slate text utilities
    (r'\btext-\[#(?:24262a|17181a|1a1a1a|334155|475569|0f172a|1e293b)\]',
     f'text-[{INK}]', "ink util"),
    # muted / caption
    (r'\bcolor:\s*#(?:5b6472|5b7285|6b7280|8a93a3|64748b|94a3b8)\b',
     f'color: {CAPTION}', "caption"),
    (r'\btext-\[#(?:5b6472|5b7285|6b7280|64748b|94a3b8)\]',
     f'text-[{CAPTION}]', "caption util"),
    # page footer text is its own, darker ink in the PDF
    (r'(\.page-footer[^{]*\{[^}]*?)color:\s*#[0-9a-f]{3,6}',
     rf'\g<1>color: {FOOTER}', "footer"),
    # the rule under the title
    (r'(\.rule\s*\{[^}]*?)border-top:\s*[^;]*#[0-9a-f]{3,6}',
     rf'\g<1>border-top: 1px solid {RULE}', "title rule"),
    # generic hairlines
    (r'\bborder(?:-top|-bottom|-left|-right)?:\s*(?:1px|2px)\s+solid\s+#(?:d7dde5|d7d7df|d9dee6|d9dee7|e5e7eb|e5e9f0|cbd5e1|e8ebf0|e6eaf0|dfe4ea|e4e7ec|e3e7ee|e2e8f0|e5e5e7)\b',
     'border: 1px solid ' + HAIRLINE, "hairline"),
    # scripture left rule
    (r'(\.scripture\s*\{[^}]*?)border-left:\s*4px\s+solid\s+#[0-9a-f]{3,6}',
     rf'\g<1>border-left: 4px solid {HAIRLINE}', "scripture rule"),
    # quote / academic blockquote rule
    (r'(\.quote[^{]*\{[^}]*?)border-left:\s*4px\s+solid\s+#[0-9a-f]{3,6}',
     rf'\g<1>border-left: 4px solid {CAPTION}', "quote rule"),
]


def convert(text):
    counts = {}
    # 1) plain token -> PDF hue
    def hue(m):
        src = m.group(0).lower()
        dst = HUE.get(src)
        if not dst:
            return m.group(0)
        counts[src] = counts.get(src, 0) + 1
        return dst
    text = re.sub(r'#[0-9a-fA-F]{6}\b', hue, text)
    # 2) role fixes
    for pat, rep, note in ROLE:
        text, n = re.subn(pat, rep, text, flags=re.I)
        if n:
            counts[note] = counts.get(note, 0) + n
    return text, counts


def check(path):
    src = open(path, encoding="utf-8").read()
    new, counts = convert(src)
    return new != src, counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="+")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    files = []
    for t in a.targets:
        p = os.path.join(ROOT, t) if not os.path.isabs(t) else t
        if os.path.isdir(p):
            files += sorted(glob.glob(os.path.join(p, "modulo-*", "sessao-*.html")))
        else:
            files.append(p)

    grand = {}
    changed = 0
    for f in files:
        src = open(f, encoding="utf-8").read()
        new, counts = convert(src)
        if new == src:
            continue
        changed += 1
        for k, v in counts.items():
            grand[k] = grand.get(k, 0) + v
        if a.apply:
            open(f, "w", encoding="utf-8").write(new)

    print(f"sessoes: {len(files)} | a converter: {changed}"
          f"{'' if a.apply else '  (dry run — use --apply)'}")
    if grand and not a.quiet:
        print("\nsubstituicoes:")
        for k, v in sorted(grand.items(), key=lambda x: -x[1]):
            print(f"  {v:>5}  {k}")
    return 0


if __name__ == "__main__":
    sys.exit(main())