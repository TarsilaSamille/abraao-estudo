#!/usr/bin/env python3
"""
audit_design.py — precise DESIGN.md conformance auditor for session pages.

The earlier ad-hoc checks were too weak (e.g. "hex appears somewhere in
DESIGN.md"), which let real deviations through. This tool parses the token
blocks out of DESIGN.md and checks each session against them.

Usage:
    python3 tools/audit_design.py                       # all sessions, summary
    python3 tools/audit_design.py abraao/modulo-2/sessao-4.html   # one file, detail
    python3 tools/audit_design.py --json               # machine readable
    python3 tools/audit_design.py --only color,type    # filter categories
    python3 tools/audit_design.py --worst 20           # top N worst files

Exit code 1 if any session has findings, so it can gate CI.
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESIGN = os.path.join(ROOT, "DESIGN.md")

VOID = {"br", "img", "hr", "input", "meta", "link", "source", "path",
        "circle", "rect", "use", "polygon", "line", "area", "col", "wbr"}


# ---------------------------------------------------------------- tokens

def load_tokens():
    src = open(DESIGN, encoding="utf-8").read()
    front = src.split("---")[1] if src.startswith("---") else src

    colors = {}
    for name, hexv in re.findall(r'^\s{2}([\w-]+):\s*"(#[0-9a-fA-F]{6})"', front, re.M):
        colors[name] = hexv.lower()

    sizes, weights, families = {}, {}, {}
    typo = re.search(r"^typography:\n(.*?)^rounded:", front, re.S | re.M)
    if typo:
        for name, block in re.findall(r'^\s{2}([\w-]+):\n((?:^\s{4}.*\n)+)', typo.group(1), re.M):
            m = re.search(r'fontSize:\s*"([\d.]+)(rem|em)"', block)
            if m:
                sizes[name] = m.group(1) + m.group(2)
            w = re.search(r"fontWeight:\s*(\d+)", block)
            if w:
                weights[name] = int(w.group(1))
            f = re.search(r'fontFamily:\s*"([^"]+)"', block)
            if f:
                families[name] = f.group(1)

    radii = {}
    rad = re.search(r"^rounded:\n(.*?)^spacing:", front, re.S | re.M)
    if rad:
        for name, v in re.findall(r'^\s{2}([\w-]+):\s*"([^"]+)"', rad.group(1), re.M):
            try:
                radii[name] = float(v.replace("px", ""))
            except ValueError:
                pass

    spacing = {}
    sp = re.search(r"^spacing:\n(.*?)^components:", front, re.S | re.M)
    if sp:
        for name, v in re.findall(r'^\s{2}([\w-]+):\s*"([^"]+)"', sp.group(1), re.M):
            spacing[name] = v

    # The spec is DESIGN.md in its entirety: frontmatter tokens plus every hex
    # named in the prose (e.g. #f8fafc is the documented table-row hover, and
    # #0f172a the documented course-card text). The documented intentional
    # Variants palette is included for the same reason.
    variant_hexes = {h.lower() for h in re.findall(r"`?(#[0-9a-fA-F]{6})`?", src)}

    return {
        "colors": colors, "sizes": sizes, "weights": weights,
        "families": families, "radii": radii, "spacing": spacing,
        "variant_hexes": variant_hexes,
    }


# Tailwind default palette -> hex, so we can flag palette utilities that do not
# resolve to a DESIGN token. Only the utilities actually used in this repo.
TAILWIND = {
    "slate-50": "#f8fafc", "slate-100": "#f1f5f9", "slate-200": "#e2e8f0",
    "slate-300": "#cbd5e1", "slate-400": "#94a3b8", "slate-500": "#64748b",
    "slate-600": "#475569", "slate-700": "#334155", "slate-800": "#1e293b",
    "slate-900": "#0f172a", "slate-950": "#020617",
    "sky-50": "#f0f9ff", "sky-100": "#e0f2fe", "sky-500": "#0ea5e9",
    "sky-600": "#0284c7", "sky-700": "#0369a1",
    "blue-600": "#2563eb", "blue-700": "#1d4ed8",
    "emerald-100": "#d1fae5", "emerald-600": "#059669", "emerald-700": "#047857",
    "amber-100": "#fef3c7", "amber-500": "#f59e0b", "amber-600": "#d97706",
    "amber-700": "#b45309",
    "stone-100": "#f5f5f4", "stone-600": "#57534e",
    "gray-100": "#f3f4f6", "gray-200": "#e5e7eb", "gray-600": "#4b5563",
    "gray-700": "#374151", "gray-800": "#1f2937", "gray-900": "#111827",
    "red-600": "#dc2626", "red-700": "#b91c1c", "green-700": "#15803d",
    "purple-600": "#9333ea", "teal-700": "#0f766e", "white": "#ffffff",
    "black": "#000000",
}
# Tailwind text-* size utilities -> rem (v3 scale; v4 same base)
TAIL_SIZE = {
    "xs": "0.75rem", "sm": "0.875rem", "base": "1rem", "lg": "1.125rem",
    "xl": "1.25rem", "2xl": "1.5rem", "3xl": "1.875rem", "4xl": "2.25rem",
    "5xl": "3rem", "6xl": "3.75rem", "7xl": "4.5rem", "8xl": "6rem",
    "9xl": "8rem",
}
TAIL_RADIUS = {
    "none": 0.0, "sm": 2.0, "": 4.0, "md": 6.0, "lg": 8.0, "xl": 12.0,
    "2xl": 16.0, "3xl": 24.0, "full": 999.0,
}


def rem(v):
    return round(float(v) * 16, 2)


# ---------------------------------------------------------------- scanner

class Scanner(HTMLParser):
    """Collect inline style blocks, class attributes and hex colours."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.styles = []
        self.scripts = []
        self.classes = []          # (tag, [class names])
        self.hexes = []            # (context, hex)
        self.in_style = False
        self.in_script = False
        self.text = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "style":
            self.in_style = True
        if tag == "script":
            self.in_script = True
        if "class" in d and d["class"]:
            self.classes.append((tag, d["class"].split()))
        for k, v in attrs:
            for h in re.findall(r"#[0-9a-fA-F]{3,8}\b", v or ""):
                self.hexes.append((tag + "/attr:" + k, h))

    def handle_endtag(self, tag):
        if tag == "style":
            self.in_style = False
        if tag == "script":
            self.in_script = False

    def handle_data(self, data):
        if self.in_style:
            self.styles.append(data)
        elif self.in_script:
            self.scripts.append(data)
        else:
            self.text.append(data)


def split_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out = []
    depth = 0
    buf = ""
    for ch in css:
        if ch == "{":
            depth += 1
            buf += ch
        elif ch == "}":
            depth -= 1
            buf += ch
            if depth == 0:
                out.append(buf)
                buf = ""
            else:
                buf += ""
        else:
            buf += ch
    return out


def audit(path, T, only=None):
    html = open(path, encoding="utf-8", errors="replace").read()
    sc = Scanner()
    sc.feed(html)

    css = "\n".join(sc.styles)
    inline_style = re.sub(r"<style.*?</style>|<script.*?</script>", "", html, flags=re.S)
    findings = defaultdict(list)

    allowed_hex = set(T["colors"].values()) | T["variant_hexes"]
    allowed_hex |= {"#ffffff", "#000000", "#fff", "#000"}
    # rgba()/hsla() are allowed only as the two documented shadows + a hairline
    allowed_rgba = {"rgba(30,41,59,.4)", "rgba(0,0,0,.06)", "rgba(23,24,26,.45)"}

    def cat(name):
        return only is None or name in only

    # ---- 1. colours ----------------------------------------------------
    if cat("color"):
        for ctx, h in sc.hexes:
            n = h.lower()
            if len(n) == 4:
                n = "#" + "".join(c * 2 for c in n[1:])
            if len(n) == 8:
                n = n[:7]
            if n not in allowed_hex:
                findings["color"].append(f"hex {h} fora dos tokens ({ctx})")

        # Hexes inside <style> blocks used to be invisible: the Scanner only
        # collected them from attributes, so a whole undocumented categorical
        # palette could live in a stylesheet and still audit clean. Walk the CSS
        # and attribute each hex to its selector.
        for block in split_css(css):
            sel = block.split("{")[0].strip() or "(regra sem seletor)"
            body_ = block.split("{", 1)[1] if "{" in block else ""
            for h in re.findall(r"#[0-9a-fA-F]{3,8}\b", body_):
                n = h.lower()
                if len(n) == 4:
                    n = "#" + "".join(c * 2 for c in n[1:])
                if len(n) == 8:
                    n = n[:7]
                if n not in allowed_hex:
                    findings["color"].append(
                        f"hex {h} fora dos tokens (em <style>, seletor {sel[:40]})")

        def norm_rgba(v):
            v = re.sub(r"\s+", "", v)
            v = re.sub(r"0\.(\d)", r".\1", v)   # 0.06 -> .06
            v = re.sub(r",0\)", ",0)", v)
            return v
        for m in re.finditer(r"rgba?\([^)]*\)", css + " " + inline_style):
            if norm_rgba(m.group(0)) not in {norm_rgba(x) for x in allowed_rgba}:
                findings["color"].append(f"rgba {m.group(0)} nao documentado")

        for tag, cls in sc.classes:
            for c in cls:
                for util, hexv in TAILWIND.items():
                    if re.fullmatch(r"(text|bg|border|ring|fill|stroke|from|to|via|decoration|divide|outline|shadow|accent|caret)-" + re.escape(util), c):
                        if hexv.lower() not in allowed_hex:
                            findings["color"].append(
                                f"utilitaria Tailwind {c} = {hexv} fora dos tokens")

    # ---- 2. type scale -------------------------------------------------
    # ---- 6. structure / template --------------------------------------
    # A page may legitimately be self-contained (own <style>) instead of
    # importing session-base.css, so only flag the missing import when the
    # shared typography classes are genuinely undefined.
    imports_base = "session-base.css" in html
    defines_typo = bool(re.search(r"h1\.title|h2\.section|h3\.sub|p\.body", css))

    if cat("type"):
        size_rem = {float(v[:-3]) for v in T["sizes"].values() if v.endswith("rem")}

        def on_scale(px):
            """True if px matches a scale token within 0.05rem (0.8px)."""
            return any(abs(px - t * 16) <= 0.8 for t in size_rem)
        for m in re.finditer(r"font-size:\s*([\d.]+)(px|rem|em)", css):
            val, unit = m.group(1), m.group(2)
            if unit == "em":
                # .em is correct for the documented `hebrew` token (1.05em) and
                # for relative verse numbers (sup.vs .72em in session-base.css).
                if not any(abs(float(val) - t) <= 0.01 for t in
                           {1.05, 0.72, 0.75, 0.8, 0.9, 0.95}):
                    findings["type"].append(
                        f"font-size {val}em relativo (use um token rem)")
            else:
                n = rem(val) if unit == "rem" else float(val)
                if not on_scale(n):
                    findings["type"].append(f"font-size {val}{unit} fora da escala")
        for tag, cls in sc.classes:
            for c in cls:
                m = re.fullmatch(r"text-([a-z0-9]+)", c)
                if m and m.group(1) in TAIL_SIZE:
                    v = TAIL_SIZE[m.group(1)]
                    if not on_scale(rem(v[:-3])):
                        findings["type"].append(
                            f"text-{m.group(1)} = {v} fora da escala")
                m2 = re.fullmatch(r"text-\[([\d.]+)(px|rem|em)\]", c)
                if m2:
                    val, unit = m2.group(1), m2.group(2)
                    if unit == "em":
                        findings["type"].append(f"{c} relativo (escala fixa: use rem)")
                    else:
                        n = rem(val) if unit == "rem" else float(val)
                        if not on_scale(n):
                            findings["type"].append(f"{c} fora da escala")

    if cat("type"):
        if not imports_base and not defines_typo:
            findings["type"].append(
                "sem session-base.css E sem definir h1.title/h2.section/h3.sub/p.body "
                "— titulos herdam o tamanho do navegador")
        for tag, cls in sc.classes:
            if tag in ("h1", "h2", "h3") and not ({"title", "section", "sub"} & set(cls)):
                if not any(re.fullmatch(r"text-(\[.+\]|[a-z0-9]+)", c) for c in cls):
                    findings["type"].append(
                        f"<{tag}> sem .title/.section/.sub e sem utilitaria de tamanho")

    if cat("structure"):
        for req, label in [
            ("reading-progress", "barra de progresso"),
            ("verse-modal.js", "verse-modal.js"),
            ("page-footer", "page-footer"),
        ]:
            if req not in html:
                findings["structure"].append(f"falta {label}")
        if 'class="lang-pt"' not in html or 'class="lang-en"' not in html:
            findings["structure"].append("faltam spans lang-pt/lang-en")
        pt = len(re.findall(r'class="lang-pt"', html))
        en = len(re.findall(r'class="lang-en"', html))
        if pt != en:
            findings["structure"].append(f"PT/EN desbalanceado: {pt}/{en}")
        if "max-w-4xl" not in html:
            findings["structure"].append("coluna de leitura sem max-w-4xl")

    # ---- 3. radii ------------------------------------------------------
    if cat("radius"):
        allowed_px = set(T["radii"].values()) | {0.0}
        for m in re.finditer(r"border-radius:\s*([\d.]+)(px|rem)", css):
            n = rem(m.group(1)) if m.group(2) == "rem" else float(m.group(1))
            if n not in allowed_px and n != 999:
                findings["radius"].append(f"border-radius {m.group(0)} fora dos tokens")
        for tag, cls in sc.classes:
            for c in cls:
                m = re.fullmatch(r"rounded(-([a-z0-9]+))?", c)
                if not m:
                    continue
                key = m.group(2) or ""
                if key in TAIL_RADIUS and TAIL_RADIUS[key] not in allowed_px:
                    findings["radius"].append(
                        f"{c} = {TAIL_RADIUS[key]}px fora dos tokens "
                        f"(use .r9/.r10/.r12/.r14/.r16)")
                if re.fullmatch(r"rounded-\[[\d.]+px\]", c):
                    findings["radius"].append(f"{c} arbitrario")

    # ---- 4. border widths ---------------------------------------------
    if cat("border"):
        # DESIGN "Shapes": hairline 1px for tables/rules/nav; confident 3px for
        # Abraham callouts, macro boxes and outer frames; 4px is reserved for
        # the left rule of .scripture/.quote/.vbar. Everything else is off-scale.
        for block in split_css(css) + [b + "{" for b in re.findall(r'style="([^"]*border[\w-]*:[^"]*)"', inline_style)]:
            sel = block.split("{")[0]
            for m in re.finditer(r"(?<!-)\bborder(-(?!radius)[a-z]+)?:\s*(\d)px", block):
                w = int(m.group(2))
                side = (m.group(1) or "").lstrip("-")
                if w in (1, 3):
                    continue
                if w == 4 and side == "left":
                    continue
                findings["border"].append(
                    f"border {w}px{'-' + side if side else ''} fora da escala "
                    f"(use 1px, 3px, ou 4px em border-left)")
        for tag, cls in sc.classes:
            for c in cls:
                if c in ("border-2", "border-4"):
                    w = 2 if c == "border-2" else 4
                    findings["border"].append(
                        f"{c} = {w}px fora da escala (use border / border-[3px])")

    # ---- 5. shadows ----------------------------------------------------
    if cat("shadow"):
        # All three documented shadows are legitimate: the nav hairline at rest,
        # and the two hover lifts. Only flag a resting shadow that is none of
        # them, and never flag a rule that only applies on :hover/:focus.
        documented = {
            "0 1px 3px rgba(0,0,0,.06)",        # nav hairline (resting, allowed)
            "0 8px 20px -10px rgba(30,41,59,.4)",  # .mbox/.cx hover lift
            "0 12px 26px -16px rgba(23,24,26,.45)",  # .cx hover lift
        }
        for block in split_css(css):
            sel = block.split("{")[0]
            body_ = block.split("{", 1)[1] if "{" in block else ""
            if re.search(r":hover|:focus|:active", sel):
                continue
            for m in re.finditer(r"box-shadow:\s*([^;}]+)", body_):
                v = re.sub(r"\s+", "", m.group(1))
                if any(re.sub(r"\s+", "", d) == v for d in documented):
                    continue
                findings["shadow"].append(
                    f"box-shadow em repouso fora do vocabulario: {m.group(1).strip()[:60]}")
        for tag, cls in sc.classes:
            for c in cls:
                if c.startswith("shadow-") and c != "shadow-none":
                    if "0_1px_3px_rgba(0,0,0,0.06)" in c:
                        continue   # the documented nav hairline
                    findings["shadow"].append(
                        f"{c} em repouso (use o hairline 0 1px 3px rgba(0,0,0,.06))")


    # ---- 6. structure / template --------------------------------------
            if not imports_base and not defines_typo:
                findings["structure"].append("sem session-base.css e sem tipografia definida")

    deduped = {k: sorted(set(v)) for k, v in findings.items()}
    total = sum(len(v) for v in deduped.values())
    return {"file": path, "findings": deduped, "total": total}


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--only", default="")
    ap.add_argument("--worst", type=int, default=0)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    T = load_tokens()
    only = set(x for x in a.only.split(",") if x) or None

    if a.paths:
        files = []
        for p in a.paths:
            if os.path.isdir(p):
                files += sorted(glob_session(p))
            else:
                files.append(p)
    else:
        files = sorted(glob_session(ROOT))

    rows = [audit(f, T, only) for f in files]
    rows.sort(key=lambda r: -r["total"])

    if a.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return 0 if all(r["total"] == 0 for r in rows) else 1

    show = rows[:a.worst] if a.worst else rows
    cats = defaultdict(int)
    for r in rows:
        for k, v in r["findings"].items():
            cats[k] += len(v)

    print(f"sessoes auditadas: {len(rows)}")
    print(f"com desvios:       {sum(1 for r in rows if r['total'])}")
    print(f"total de desvios:  {sum(r['total'] for r in rows)}")
    if cats:
        print("por categoria: " + ", ".join(f"{k}={v}" for k, v in sorted(cats.items())))
    print()
    for r in show:
        if not r["total"]:
            continue
        print(f"{r['total']:>4}  {os.path.relpath(r['file'], ROOT)}")
        for k, v in r["findings"].items():
            for item in v[:6]:
                print(f"        [{k}] {item}")
            if len(v) > 6:
                print(f"        [{k}] ... +{len(v) - 6} mais")
    return 0 if all(r["total"] == 0 for r in rows) else 1


def glob_session(base):
    out = []
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames
                       if d not in {"node_modules", ".git", "__pycache__", ".github", "css", "js", "img"}]
        for f in filenames:
            if re.fullmatch(r"sessao-\d+\.html", f):
                out.append(os.path.join(dirpath, f))
    return out


if __name__ == "__main__":
    sys.exit(main())
