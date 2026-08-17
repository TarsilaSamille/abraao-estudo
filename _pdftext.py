import sys, subprocess, os

pdf = "exodus-overview/pdf-sessoes/sessao-16.pdf"
out = "/tmp/sessao16.txt"

# try pdftotext first
try:
    subprocess.run(["pdftotext", "-layout", pdf, out], check=True)
    print("pdftotext OK")
except Exception as e:
    print("pdftotext failed:", e)
    try:
        import fitz
        doc = fitz.open(pdf)
        with open(out, "w") as f:
            for p in doc:
                f.write(p.get_text())
        print("pymupdf OK")
    except Exception as e2:
        print("pymupdf failed:", e2)
        try:
            from pypdf import PdfReader
            r = PdfReader(pdf)
            with open(out, "w") as f:
                for pg in r.pages:
                    f.write(pg.extract_text() or "")
            print("pypdf OK")
        except Exception as e3:
            print("pypdf failed:", e3)

with open(out) as f:
    print(f.read())
