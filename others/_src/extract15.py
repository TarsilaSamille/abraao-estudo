import fitz, re, os
pdf="/Users/macbook/Documents/GitHub/abraao-estudo/abraao/abraham-teacher-notes.pdf"
doc=fitz.open(pdf)
out="/Users/macbook/Documents/GitHub/abraao-estudo/others/_src/sessao-15-pdf-pages.txt"
with open(out,"w") as f:
    for i in [102,103,104]:
        f.write(f"\n===== PAGE {i} (PDF {i+1}) =====\n")
        f.write(doc[i].get_text())
print("saved", out)
for i in [102,103,104]:
    t=re.sub(r'\n{3,}','\n\n',doc[i].get_text())
    print("="*70); print(f"PAGE {i}"); print("="*70); print(t)
