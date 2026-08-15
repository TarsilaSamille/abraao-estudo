#!/usr/bin/env python3
"""gen_body.py — rebuild the BODY of ONE joseph sessao-N.html from its
_reconstruct/sessao-N.txt, preserving head/nav/footer/scripts.

Mirrors EN->PT (interim mode, shared_state: glossario_padrao.status=interim).
Edits exactly ONE file per invocation:  python3 gen_body.py <N>
"""
import sys, os, re, glob, html

REPO = "/Users/macbook/GitHub/biblia-estudo"
J = os.path.join(REPO, "joseph")


def find_html(n):
    hits = glob.glob(os.path.join(J, "modulo-*", f"sessao-{n}.html"))
    return hits[0] if hits else None


def clean_line(s):
    s = s.strip()
    if re.match(r"^Session \d+:", s):
        return ""
    if re.match(r"^Class Notes:", s):
        return ""
    if re.match(r"^\d+ of \d+$", s):
        return ""
    if s in ("\f", ""):
        return ""
    return s


# Headings (own paragraph OR leading a paragraph)
H2_RE = re.compile(r"(Act \d+ — .+|Act \d+|Yaaqov.?s Sons in the Biblical Imagination|The Yaaqov Story|The Mosaic Portrait)")
H3_RE = re.compile(
    r"(Key Takeaways|Principais Lições|Later Recollections|The Point|O Ponto|"
    r"Reflection Question|Pergunta de Reflexão|Key Words Adapted by Teacher|"
    r"Genesis \S[\w\-]*|Gênesis \S[\w\-]*|\d+[a-z]?-\d+[a-z]?|"
    r"45b-46a|46b-47|48-50|Vertical.*|.*Imagination)"
)
SCRIPTURE_RE = re.compile(r"NASB\*?$|NRSV\*?$|ESV\*?$")
VERSE_LINE_RE = re.compile(r"^\d+\s*$")
REF_RE = re.compile(r"^(Números|Numbers|1 |2 |3 |4 |Ezequiel|Ezekiel|Zacarias|Zechariah|Atos|Acts|1 Crônicas|1 Chronicles|Gênesis|Genesis|Êxodo|Exodus)\b.*:\s")
BULLET_DASH_RE = re.compile(r"^[a-z]\s*[\'\-]\s+")


def span_pair(text):
    e = html.escape(text, quote=True)
    return f'<span class="lang-pt">{e}</span><span class="lang-en">{e}</span>'


def split_paragraph(para_text):
    """Given a paragraph (possibly with an inlined heading), return
    (heading_html_or_None, rest_text)."""
    m2 = H2_RE.match(para_text)
    m3 = H3_RE.match(para_text)
    if m2:
        return f'<h2 class="section reveal">{span_pair(m2.group(1))}</h2>', para_text[m2.end():].strip()
    if m3:
        return f'<h3 class="sub reveal">{span_pair(m3.group(1))}</h3>', para_text[m3.end():].strip()
    return None, para_text


def parse_blocks(paras):
    out = []
    i = 0
    n = len(paras)
    while i < n:
        text = " ".join(paras[i]).strip()
        if not text:
            i += 1
            continue
        # Scripture block header (line ends with translation label)
        if SCRIPTURE_RE.search(text):
            sctext = []
            j = i
            while j < n:
                joined = " ".join(paras[j]).strip()
                if not joined:
                    j += 1
                    continue
                if H2_RE.match(joined) or H3_RE.match(joined) or joined.startswith("Key Takeaways"):
                    break
                sctext.append(joined)
                j += 1
                if j < n and paras[j] and VERSE_LINE_RE.match(paras[j][0]):
                    sctext.append(" ".join(paras[j]))
                    j += 1
            body = " ".join(sctext).strip()
            label = "NASB" if "NASB" in body else "Scripture"
            out.append(
                f'<div class="scripture reveal"><div><span class="scripture-label">Ref</span>'
                f'<span class="scripture-type">{label}</span></div>'
                f'<p class="scripture-text">{span_pair(body)}</p></div>'
            )
            i = j
            continue
        # Heading?
        h_html, rest = split_paragraph(text)
        if h_html:
            out.append(h_html)
            if rest:
                # the heading line also carried a sentence -> paragraph
                out.append(f'<p class="body reveal">{span_pair(rest)}</p>')
            i += 1
            # absorb following short lines as a bullet list under this heading
            j = i
            items = []
            while j < n and paras[j] and len(paras[j]) <= 2:
                joined = " ".join(paras[j]).strip()
                if not joined or H2_RE.match(joined) or H3_RE.match(joined) or SCRIPTURE_RE.search(joined):
                    break
                items.append(f'<li class="reveal">{span_pair(joined)}</li>')
                j += 1
            if items:
                out.append('<ul class="bullets">' + "".join(items) + "</ul>")
            i = j
            continue
        # bullet dash lines (a - , b - , a' -)
        if BULLET_DASH_RE.match(text):
            items = []
            j = i
            while j < n and paras[j]:
                joined = " ".join(paras[j]).strip()
                if not joined or not BULLET_DASH_RE.match(joined):
                    break
                bl = re.sub(r"^[a-z]\s*[\'\-]\s+", "", joined).strip()
                if bl:
                    items.append(f'<li class="reveal">{span_pair(bl)}</li>')
                j += 1
            if items:
                out.append('<ul class="bullets">' + "".join(items) + "</ul>")
                i = j
                continue
        # reference list item (single line, has "Book XX: ...")
        if REF_RE.match(text) and len(paras[i]) == 1:
            out.append(f'<ul class="bullets"><li class="reveal">{span_pair(text)}</li></ul>')
            i += 1
            continue
        # default paragraph
        out.append(f'<p class="body reveal">{span_pair(text)}</p>')
        i += 1
    return out


def build_body(n):
    txt_path = os.path.join(J, "_reconstruct", f"sessao-{n}.txt")
    raw = open(txt_path, encoding="utf-8").read()
    raw = raw.replace("\f", "\n")
    raw_lines = [clean_line(l) for l in raw.split("\n")]
    paras = []
    cur = []
    for ln in raw_lines:
        if ln == "":
            if cur:
                paras.append(cur)
                cur = []
        else:
            cur.append(ln)
    if cur:
        paras.append(cur)
    blocks = parse_blocks(paras)
    return "\n".join(blocks)


def main():
    n = int(sys.argv[1])
    path = find_html(n)
    if not path:
        print(f"no html for sessao-{n}")
        return 1
    body = build_body(n)
    t = open(path, encoding="utf-8").read()
    REG = re.compile(r'(<div class="max-w-4xl[^"]*"[^>]*>\s*)(.*?)(\s*<footer class="page-footer">)', re.S)
    new_t, cnt = REG.subn(lambda m: m.group(1) + "\n" + body + "\n" + m.group(3), t, count=1)
    if cnt != 1:
        print(f"REPLACE FAILED sessao-{n} (cnt={cnt})")
        return 1
    open(path, "w", encoding="utf-8").write(new_t)
    pt = new_t.count("lang-pt")
    en = new_t.count("lang-en")
    print(f"sessao-{n}: body={len(body)}B | lang-pt={pt} lang-en={en} balanced={pt==en}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
