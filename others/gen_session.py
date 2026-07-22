#!/usr/bin/env python3
"""Build faithful session pages for a course, matching the Abraao session style.

Workflow (per user instruction):
  1. Generate an ALL-ENGLISH page (sessao-N-en.html) — verified against PDF images.
  2. Generate the TRANSLATED bilingual page (sessao-N.html) with an EN/PT toggle
     button at top and a "PDF" button opening the English teacher-notes PDF
     anchored to the session's first page.

Design fidelity:
  - Colors/borders/spacing copied from abraao/sessao-15.html
  - Key Takeaways rendered as a bulleted list (matches PDF)
  - Image captions in grey italic
  - Verse links preserved
"""
import re, os, json, html, sys

ROOT = "/Users/macbook/Documents/GitHub/abraao-estudo"

STYLE = """        @media print {
            @page { size: A4; margin: 1cm; }
            body { -webkit-print-color-adjust: exact; print-color-adjust: exact; background-color: white !important; }
            .min-h-screen { min-height: auto !important; padding: 0 !important; }
            .p-8, .p-4 { padding: 0 !important; }
            .mb-10, .mb-12, .my-8 { margin-bottom: 1.5rem !important; margin-top: 1.5rem !important; }
            .rounded-2xl, .rounded-xl { border-radius: 8px !important; border-width: 2px !important; }
            .shadow-sm { box-shadow: none !important; }
        }
        .hl-seed   { background-color: #D3F2CD; color: #2B6146; font-weight: 700; padding: 0 5px; border-radius: 4px; }
        .hl-sign   { background-color: #FAE4C4; color: #7a5a1e; font-weight: 700; padding: 0 5px; border-radius: 4px; }
        .hl-mult   { background-color: #E8BEC9; color: #8a2d4a; font-weight: 700; padding: 0 5px; border-radius: 4px; }
        .hl-action { background-color: #E9ECEF; color: #333333; font-weight: 700; padding: 0 5px; border-radius: 4px; }
        .hl-divine { background-color: #5869CD; color: #ffffff; font-weight: 700; padding: 0 5px; border-radius: 4px; }
        .box-hdr-grey { background-color: #6B7384; color: #ffffff; border-radius: 999px; }
        .box-hdr-red   { background-color: #BE4967; color: #ffffff; border-radius: 999px; }
        .badge-col1 { background-color: #DCE6F1; color: #4a5568; font-weight: 700; padding: 2px 10px; border-radius: 999px; display: inline-block; font-size: 13px; margin-bottom: 8px; }
        .badge-col2 { background-color: #6B7384; color: #ffffff; font-weight: 700; padding: 2px 10px; border-radius: 999px; display: inline-block; font-size: 13px; margin-bottom: 8px; }
        .badge-col3 { background-color: #645537; color: #ffffff; font-weight: 700; padding: 2px 10px; border-radius: 999px; display: inline-block; font-size: 13px; margin-bottom: 8px; }
        .badge-col4 { background-color: #DCE6F1; color: #1e40af; font-weight: 700; padding: 2px 10px; border-radius: 999px; display: inline-block; font-size: 13px; margin-bottom: 8px; }
        .heb { font-family: 'Ezra SIL', 'SBL Hebrew', serif; }
        .verse-link { color: #365fa0; text-decoration: underline; cursor: pointer; }
        .replay-grid { display: grid; grid-template-columns: repeat(4, 1fr); grid-auto-rows: 1fr; gap: 0; border: 2px solid #94a3b8; border-radius: 10px; overflow: hidden; }
        .replay-cell { border: 1px solid #94a3b8; padding: 14px 16px; font-size: 14px; line-height: 1.5; display: flex; flex-direction: column; }
        .replay-cell .ttl { font-weight: 700; font-size: 15px; margin-bottom: 8px; }
        .ptable { width: 100%; border-collapse: collapse; font-size: 14px; }
        .ptable th, .ptable td { border: 1px solid #cbd5e1; padding: 9px 12px; vertical-align: top; text-align: left; }
        .ptable th { background-color: #eef1f5; font-weight: 700; }
        .ptable .av { background-color: #faf5ef; }
        .ptable .no { background-color: #eef4f8; }
        .lang-pt { display: none; }
        .lang-toggle-pt .lang-en { display: none; }
        .lang-toggle-pt .lang-pt { display: block; }
"""

# Top bar shared by both EN-only and bilingual pages
def topbar(pdf_url, with_toggle):
    toggle = ""
    if with_toggle:
        toggle = """
            <div class="inline-flex overflow-hidden rounded-full border border-slate-300 bg-white shadow-sm print:hidden">
                <button id="lang-en-btn" onclick="setLang('en')" class="px-4 py-1.5 text-sm font-semibold transition-colors hover:bg-slate-100">EN</button>
                <button id="lang-pt-btn" onclick="setLang('pt')" class="px-4 py-1.5 text-sm font-semibold transition-colors hover:bg-slate-100">PT</button>
            </div>"""
    pdf_btn = f"""
            <a href="{pdf_url}" target="_blank" class="flex items-center gap-2 bg-slate-100 hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-lg transition-colors border border-slate-300 shadow-sm print:hidden">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
                PDF (EN)
            </a>"""
    return f"""    <div class="p-4 flex justify-between items-center print:hidden">
        <a href="../index.html" class="text-sky-600 hover:underline">&larr; Back to Index</a>
        <div class="flex items-center gap-2">{toggle}{pdf_btn}
            <button onclick="window.print()" class="flex items-center gap-2 bg-slate-100 hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-lg transition-colors border border-slate-300 shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
                Print
            </button>
        </div>
    </div>"""

SCRIPT = """    <script>
        function setLang(l){
            const body=document.body;
            if(l==='pt'){ body.classList.add('lang-toggle-pt'); document.getElementById('lang-pt-btn').classList.add('bg-sky-600','text-white'); document.getElementById('lang-en-btn').classList.remove('bg-sky-600','text-white'); }
            else { body.classList.remove('lang-toggle-pt'); document.getElementById('lang-en-btn').classList.add('bg-sky-600','text-white'); document.getElementById('lang-pt-btn').classList.remove('bg-sky-600','text-white'); }
        }
        setLang(localStorage.getItem('bp_lang')||'en');
    </script>"""

def esc(s): return html.escape(s, quote=True)

def parse_blocks(text):
    """Parse a session text into ordered blocks. Returns list of (kind, text).
    kind in: title / takeaways_hdr / refl_hdr / caption / heading / para / bullet."""
    raw = [l.rstrip() for l in text.split("\n")]
    # Drop leading blanks
    while raw and not raw[0].strip():
        raw.pop(0)
    # Pre-merge wrapped continuation lines: a line is a continuation of the previous
    # block if the previous line does NOT end with terminal punctuation and this line
    # is not itself a structural line (heading/caption/Key Takeaways/etc).
    def structural(s):
        if not s.strip():
            return True
        if s == "Key Takeaways" or s == "Reflection Question":
            return True
        if re.match(r'^Session \d+:', s) or s.startswith("Sessão "):
            return True
        if bool(re.search(r'\(\d{4}\)\.|Wikimedia|NASA|Hubble|Stockli|Risinger', s)) or (len(s) < 90 and re.search(r'\b(Photo|Image|A picture|A rendering|A photo|A diagram)\b', s)):
            return True
        # heading heuristic (short, capitalized, no terminal punct)
        if len(s) < 70 and not s.endswith('.') and s[0:1].isupper():
            return True
        return False
    lines = []
    for line in raw:
        if not line.strip():
            continue
        if lines and lines[-1] and lines[-1][-1] not in '.!?":' and not structural(lines[-1]) and not structural(line) and not re.match(r'^[*\-]\s+', line):
            lines[-1] = lines[-1] + " " + line
        else:
            lines.append(line)
    blocks = []
    i = 0
    if i < len(lines):
        blocks.append(("title", lines[i].strip())); i += 1
    cur_mode = None
    cur = []
    def emit():
        nonlocal cur, cur_mode
        if cur_mode and cur:
            txt = "\n".join(cur).strip()
            if cur_mode == "takeaways_body":
                for b in txt.split("\n"):
                    blocks.append(("bullet", b.strip()))
            else:
                blocks.append((cur_mode, txt))
        cur = []
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1; continue
        if s == "Key Takeaways":
            emit(); cur_mode = "takeaways_hdr"; cur=[]; blocks.append(("takeaways_hdr", s)); cur_mode="takeaways_body"; i+=1; continue
        if s == "Reflection Question":
            emit(); cur_mode = "refl_hdr"; cur=[]; blocks.append(("refl_hdr", s)); cur_mode=None; i+=1; continue
        if re.match(r'^Session \d+:', s) or s.startswith("Sessão "):
            emit(); i+=1; continue
        is_caption = bool(re.search(r'\(\d{4}\)\.|Wikimedia|NASA|Hubble|Stockli|Risinger', s)) or (len(s) < 90 and re.search(r'\b(Photo|Image|A picture|A rendering|A photo|A diagram)\b', s))
        if is_caption:
            emit(); blocks.append(("caption", s)); cur_mode=None; i+=1; continue
        if re.match(r'^[*\-]\s+', s):
            if cur_mode != "takeaways_body":
                emit(); cur_mode="takeaways_body"
            cur.append(re.sub(r'^[*\-]\s+', '', s)); i+=1; continue
        if len(s) < 70 and not s.endswith('.') and s[0:1].isupper() and cur_mode not in ("para","heading"):
            emit(); cur_mode="heading"; cur=[s]; i+=1; continue
        if cur_mode in ("para","heading","takeaways_body"):
            cur.append(s); i+=1; continue
        emit(); cur_mode="para"; cur=[s]; i+=1
    emit()
    return blocks

def render_blocks(blocks, is_pt):
    """Render parsed blocks (single language) to HTML body."""
    out = []
    in_list = False
    for kind, txt in blocks:
        if kind == "title":
            continue
        elif kind == "takeaways_hdr":
            if in_list: out.append("</ul>"); in_list=False
            label = "Key Takeaways" if not is_pt else "Principais Lições"
            out.append(f'<h2 class="text-2xl font-bold text-slate-800 mb-3">{label}</h2>')
            in_list = True  # next bullets form the list
        elif kind == "bullet":
            if not in_list:
                out.append('<ul class="list-disc pl-8 mb-6 space-y-2 text-lg text-slate-700 leading-relaxed">'); in_list=True
            out.append(f'<li>{esc(txt)}</li>')
        elif kind == "refl_hdr":
            if in_list: out.append("</ul>"); in_list=False
            label = "Reflection Question" if not is_pt else "Pergunta de Reflexão"
            out.append(f'<h2 class="text-2xl font-bold text-slate-800 mb-3 mt-8">{label}</h2>')
        elif kind == "caption":
            if in_list: out.append("</ul>"); in_list=False
            out.append(f'<p class="text-sm text-slate-500 italic mb-4">{esc(txt)}</p>')
        elif kind == "heading":
            if in_list: out.append("</ul>"); in_list=False
            out.append(f'<h2 class="text-3xl font-bold text-slate-800 mt-10 mb-4 print:mt-0">{esc(txt)}</h2>')
        else:  # para
            if in_list: out.append("</ul>"); in_list=False
            out.append(f'<p class="text-lg text-slate-700 leading-relaxed mb-5">{esc(txt)}</p>')
    if in_list: out.append("</ul>")
    return "\n".join(out)

def build_en_only(en_blocks, sess_num, sess_title, pdf_url, img_html):
    body = render_blocks(en_blocks, is_pt=False)
    return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Session {sess_num}: {esc(sess_title)}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
{STYLE}
    </style>
</head>
<body class="bg-white font-sans text-slate-800">
{topbar(pdf_url, with_toggle=False)}
    <div class="min-h-screen p-8 lg:px-16">
        <div id="sessao-en" class="max-w-4xl mx-auto">
            <h1 class="text-3xl md:text-4xl font-bold text-slate-900 mb-8 border-b pb-4">Session {sess_num}: {esc(sess_title)}</h1>
{body}
{img_html}
        </div>
    </div>
</body>
</html>"""

def build_bilingual(en_blocks, pt_blocks, sess_num, sess_title, pt_title, pdf_url, img_html):
    en_body = render_blocks(en_blocks, is_pt=False)
    pt_body = render_blocks(pt_blocks, is_pt=True)
    return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Session {sess_num}: {esc(sess_title)}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
{STYLE}
    </style>
</head>
<body class="bg-white font-sans text-slate-800">
{topbar(pdf_url, with_toggle=True)}
    <div class="min-h-screen p-8 lg:px-16">
        <div id="sessao-{sess_num}" class="max-w-4xl mx-auto">
            <div class="lang-en">
            <h1 class="text-3xl md:text-4xl font-bold text-slate-900 mb-8 border-b pb-4">Session {sess_num}: {esc(sess_title)}</h1>
{en_body}
            </div>
            <div class="lang-pt">
            <h1 class="text-3xl md:text-4xl font-bold text-slate-900 mb-8 border-b pb-4">Sessão {sess_num}: {esc(pt_title)}</h1>
{pt_body}
            </div>
{img_html}
        </div>
    </div>
{SCRIPT}
</body>
</html>"""

if __name__ == "__main__":
    course = sys.argv[1]
    sess = int(sys.argv[2])
    prefix = {"heaven-and-earth":"he"}.get(course, course.split('-')[0])
    en = open(f"/tmp/{prefix}_session_{sess}.txt").read()
    pt = open(f"/tmp/{prefix}_session_{sess}_pt.txt").read()

    m = re.search(r'Session\s+(\d+):\s*(.+)', en)
    sess_num = m.group(1); sess_title = m.group(2).strip()
    pt_title_line = pt.split('\n', 1)[0].strip()
    pt_title = pt_title_line[len("Sessão %s: " % sess_num):].strip() if pt_title_line.startswith("Sessão") else sess_title

    mods = json.load(open(os.path.join(ROOT, "others", "modules_en.json"), encoding="utf-8"))[course]
    module_pos = 1
    for md in mods:
        if md["first"] <= sess <= md["last"]:
            module_pos = md["pos"]; break

    # PDF anchor: first page of this session in the English teacher-notes PDF
    sp = json.load(open(os.path.join(ROOT, "others", "session_pages.json"), encoding="utf-8"))[course]
    smap = [d for d in sp if d["session"] == sess][0]
    first_page = smap["page_start"] + 1  # fitz 0-idx -> PDF 1-idx
    pdf_url = f"../{course}-teacher-notes.pdf#page={first_page}"

    # Embed the corresponding PDF page images (ground truth) so all design/text is present
    img_html = ""
    imgs = []
    p = smap["page_start"]
    while p < smap["page_end"]:
        rel = f"../pdf-images/page_{p}.png"
        absp = os.path.join(ROOT, course, "pdf-images", f"page_{p}.png")
        if os.path.exists(absp):
            imgs.append(f'            <figure class="mb-8 border rounded-xl overflow-hidden shadow-sm">\n              <img src="{rel}" alt="PDF page {p+1}" class="w-full h-auto" />\n            </figure>')
        p += 1
    if imgs:
        img_html = '            <h2 class="text-2xl font-bold text-slate-800 mt-12 mb-4 border-t pt-6">Original PDF Pages</h2>\n' + "\n".join(imgs)

    en_blocks = parse_blocks(en)
    pt_blocks = parse_blocks(pt)

    d = os.path.join(ROOT, course, f"modulo-{module_pos}")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, f"sessao-{sess}-en.html"), "w").write(build_en_only(en_blocks, sess_num, sess_title, pdf_url, img_html))
    open(os.path.join(d, f"sessao-{sess}.html"), "w").write(build_bilingual(en_blocks, pt_blocks, sess_num, sess_title, pt_title, pdf_url, img_html))
    print(f"WROTE modulo-{module_pos}/sessao-{sess}-en.html + sessao-{sess}.html (PDF page {first_page}, {len(imgs)} page images)")
