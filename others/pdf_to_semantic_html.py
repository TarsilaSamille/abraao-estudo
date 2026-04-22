import fitz
import os
import re

def is_in_rect(bbox, target_rect):
    r = fitz.Rect(bbox)
    center = fitz.Point((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)
    return center in fitz.Rect(target_rect)

def extract_rich_text(line):
    html = ""
    for span in line["spans"]:
        text = span["text"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        flags = span["flags"]
        if flags & 16: text = f"<strong>{text}</strong>"
        if flags & 2: text = f"<em>{text}</em>"
        html += text
    return html

def pdf_to_semantic_html(pdf_path, output_dir):
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    img_dir = os.path.join(output_dir, "image")
    if not os.path.exists(img_dir): os.makedirs(img_dir)

    doc = fitz.open(pdf_path)
    sessions = []
    current_session = {"number": 0, "title": "Introdução", "content": [], "page_num": 1}
    sessions.append(current_session)
    session_map = {0: current_session}

    print(f"Total pages: {len(doc)}")

    for page_num in range(len(doc)):
        if page_num % 20 == 0: print(f"Processing Page {page_num+1}...")
        page = doc[page_num]
        
        tabs = page.find_tables()
        tab_bboxes = [t.bbox for t in tabs]
        tab_contents = [t.extract() for t in tabs]
        
        blocks = page.get_text("dict")["blocks"]
        blocks.sort(key=lambda b: (round(b["bbox"][1]), round(b["bbox"][0])))
        used_tabs = set()

        for b in blocks:
            in_tab = False
            for i, tbox in enumerate(tab_bboxes):
                if is_in_rect(b["bbox"], tbox):
                    if i not in used_tabs:
                        current_session["content"].append(("table", tab_contents[i]))
                        used_tabs.add(i)
                    in_tab = True; break
            if in_tab: continue

            if b["type"] == 0:
                text = ""; rich = ""; ms = 0
                for line in b["lines"]:
                    text += " ".join([s["text"] for s in line["spans"]]) + " "
                    rich += extract_rich_text(line) + " "
                    for s in line["spans"]: ms = max(ms, s["size"])
                
                text = text.strip(); rich = rich.strip()
                if not text or (len(text) < 40 and ("Class Notes" in text or "of 202" in text)): continue

                # Session Detection
                sm = re.search(r"Session\s*(\d+)\s*[:\-]?\s*(.*)", text, re.I)
                if sm and ms > 18 and page_num > 2:
                    sn = int(sm.group(1))
                    st = sm.group(2).strip() or f"Session {sn}"
                    if sn not in session_map:
                        current_session = {"number": sn, "title": st, "content": [], "page_num": page_num + 1}
                        sessions.append(current_session)
                        session_map[sn] = current_session
                    else: current_session = session_map[sn]
                    continue

                # Categorize
                if re.match(r"^([1-3]\s)?[A-Z][a-z]+\s\d+:\d+", text):
                    current_session["content"].append(("verse", rich))
                elif ms > 20 or text.lower() == "key takeaways": 
                    current_session["content"].append(("h2", rich))
                elif ms > 14 and (text.isupper() or len(text) < 60): 
                    current_session["content"].append(("h3", rich))
                elif text.startswith("•") or (len(text) < 300 and b["bbox"][0] > 60):
                    current_session["content"].append(("li", rich.lstrip("• ")))
                else: 
                    current_session["content"].append(("p", rich))
            
            elif b["type"] == 1:
                if b["width"] < 40 or b["height"] < 40: continue
                ifn = f"img_{page_num}_{int(b['bbox'][1])}.{b['ext']}"
                ip = os.path.join(img_dir, ifn)
                if not os.path.exists(ip):
                    with open(ip, "wb") as f: f.write(b["image"])
                current_session["content"].append(("img", ifn))

    print("\nWriting high-fidelity HTML files...")
    
    head_template = """
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
    <link href="https://fonts.googleapis.com" rel="preconnect"/>
    <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet"/>
    <script>
        tailwind.config = {
          theme: {
            extend: {
              fontFamily: { sans: ['Inter', 'sans-serif'] },
              colors: {
                brand: { dark: '#1e1b2e', muted: '#6b7280', border: '#d1d5db', bg: '#f9fafb', badge: '#6b7280' }
              }
            }
          }
        }
    </script>
    <style>
        body { background-color: #f3f4f6; color: #111827; -webkit-font-smoothing: antialiased; }
        .doc-page { width: 100%; max-width: 1000px; margin: 0 auto; background-color: white; position: relative; padding: 60px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); }
        .border-thick { border-width: 2px; }
        .rounded-box { border-radius: 0.5rem; }
        ul.custom-bullets { list-style-type: disc; padding-left: 1.5rem; }
        .badge-bg { background-color: #1e1b2e; color: white; border-radius: 4px; padding: 2px 10px; font-weight: 600; display: inline-block; font-size: 14px; }
    </style>
    """

    for s in sessions:
        sn, title, items, pn = s["number"], s["title"], s["content"], s["page_num"]
        if not items: continue
        
        mod_idx = (sn-1)//6 + 1 if sn > 0 else 0
        mod_dir = f"modulo-{min(mod_idx, 6)}"
        md = os.path.join(output_dir, mod_dir)
        if not os.path.exists(md): os.makedirs(md)
        fn = os.path.join(md, f"sessao-{sn}.html" if sn > 0 else "introducao.html")
        
        html_items = ""
        in_list = False
        
        for t, c in items:
            if t == "li":
                if not in_list: 
                    html_items += '            <ul class="custom-bullets text-base text-gray-800 leading-relaxed space-y-2 mb-6">\n'
                    in_list = True
                html_items += f'                <li>{c}</li>\n'
            else:
                if in_list: 
                    html_items += '            </ul>\n'
                    in_list = False
                
                if t == "h2": 
                    html_items += f'            <h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">{c}</h2>\n'
                elif t == "h3":
                    html_items += f"""            <div class="border-thick border-brand-dark rounded-box p-6 flex flex-col gap-4 mb-8 bg-brand-bg">
                <h3 class="text-xl font-bold text-gray-900">{c}</h3>
            </div>\n"""
                elif t == "p":
                    html_items += f'            <p class="text-base text-gray-800 leading-relaxed mb-6">{c}</p>\n'
                elif t == "verse":
                    html_items += f"""            <div class="border-thick border-brand-border rounded-box p-5 bg-white mb-6 italic text-gray-700">
                {c}
            </div>\n"""
                elif t == "table":
                    html_items += '            <div class="overflow-x-auto my-8 border-thick border-brand-border rounded-box"> <table class="min-w-full divide-y divide-brand-border">'
                    for i, row in enumerate(c):
                        tag = "th" if i == 0 else "td"
                        html_items += f'<tr class="{"bg-gray-50" if i==0 else "bg-white"}">'
                        for cell in row:
                            html_items += f'<{tag} class="px-6 py-4 text-left text-sm border-b">{(cell or "").replace("\n", "<br>")}</{tag}>'
                        html_items += '</tr>'
                    html_items += '</table></div>'
                elif t == "img":
                    html_items += f'            <figure class="my-10 text-center"> <img src="../image/{c}" class="mx-auto rounded-box shadow-md border-thick border-brand-border" /> </figure>\n'

        if in_list: html_items += '            </ul>\n'

        full_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <title>{title}</title>
    {head_template}
</head>
<body class="py-10 px-4">
    <main class="doc-page min-h-screen flex flex-col">
        <header class="border-b border-brand-border pb-6 mb-10 flex justify-between items-end">
            <div>
                <a href="../index.html" class="text-brand-muted text-sm hover:underline mb-2 block">← Voltar ao Índice</a>
                <h1 class="text-4xl font-bold tracking-tight text-gray-900">{title}</h1>
            </div>
            <div class="badge-bg">Session {sn}</div>
        </header>
        
        <div class="flex-grow">
            {html_items}
        </div>

        <footer class="mt-16 pt-8 border-t border-brand-border flex justify-between items-center text-brand-muted text-sm">
            <span>Class Notes: Noah to Abraham</span>
            <span>Page {pn}</span>
        </footer>
    </main>
</body>
</html>"""
        with open(fn, "w", encoding="utf-8") as f: f.write(full_html)
        
    print(f"✅ Generated {len(sessions)} high-fidelity files in {output_dir}")

if __name__ == "__main__":
    pdf_to_semantic_html("others/noah-to-abraham-teacher-notes.pdf", "noah-output")
