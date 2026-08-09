import fitz, os, sys
N = int(sys.argv[1])
M = sys.argv[2] if len(sys.argv) > 2 else None
base = "/Users/macbook/GitHub/biblia-estudo/ephesians"
pdf = f"{base}/pdf-sessoes/sessao-{N+1}.pdf"
doc = fitz.open(pdf)
for i, page in enumerate(doc):
    print(f"===== PAGE {i+1} (drawings={len(page.get_drawings())}) =====")
    print(page.get_text())
if M:
    out = f"{base}/modulo-{M}/img/sessao-{N}"
    os.makedirs(out, exist_ok=True)
    for i, page in enumerate(doc):
        if len(page.get_drawings()) >= 8:
            p = f"{out}/p{i+1}-vector.png"
            page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0)).save(p)
            print("RENDERED", p)
doc.close()
