#!/usr/bin/env python3
"""Ad-hoc content-coverage audit (NOT a suite): for each session PDF, extract
verse-ref markers (Gen X:Y, Psalm, etc.) and section headings, then check how
many appear in the corresponding module HTML. Reports coverage % per session."""
import re, os, glob

ROOT = "/Users/macbook/GitHub/biblia-estudo/abraao"
PDF = os.path.join(ROOT, "pdf-sessoes")
TXT = "/tmp/pdftxt"

# map session number -> module html path
def html_for(n):
    for m in ["modulo-1", "modulo-2", "modulo-3", "modulo-4"]:
        p = os.path.join(ROOT, m, f"sessao-{n}.html")
        if os.path.exists(p):
            return p
    return None

# find the module dir that actually holds a given session (for prev/back logic)
def module_of(n):
    for m in ["modulo-1", "modulo-2", "modulo-3", "modulo-4"]:
        if os.path.exists(os.path.join(ROOT, m, f"sessao-{n}.html")):
            return m
    return None

def refs(txt):
    # Genesis/Gen chapter:verse style, plus "Psalm", "John", etc.
    return set(re.findall(r'(?:Genesis|Gen)\.?\s*\d{1,2}:\d{1,3}', txt))

print(f"{'s':>3} {'mod':8} {'refs':>5} {'hit':>5} {'cov%':>5}  note")
for n in range(1, 31):
    pdf = os.path.join(PDF, f"sessao-{n}.pdf")
    txtp = os.path.join(TXT, f"s{n}.txt")
    hp = html_for(n)
    if not os.path.exists(pdf):
        print(f"{n:>3} {'-':8} {'-':>5} {'-':>5} {'-':>5}  no PDF")
        continue
    txt = open(txtp, encoding="utf-8", errors="ignore").read()
    r = refs(txt)
    if not r:
        print(f"{n:>3} {str(module_of(n)):8} {0:>5} {0:>5} {0:>5}  no verse refs in PDF")
        continue
    if not hp:
        print(f"{n:>3} {'NONE':8} {len(r):>5} {0:>5} {0:>5}  NO HTML FILE")
        continue
    html = open(hp, encoding="utf-8", errors="ignore").read()
    hit = sum(1 for x in r if x.replace(" ", "") in html.replace(" ", ""))
    cov = round(100 * hit / len(r))
    note = "" if cov >= 80 else "  <-- LOW"
    print(f"{n:>3} {str(module_of(n)):8} {len(r):>5} {hit:>5} {cov:>4}%{note}")
