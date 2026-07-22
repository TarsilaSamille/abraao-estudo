import fitz, re, os
pdf="/Users/macbook/Documents/GitHub/abraao-estudo/abraao/abraham-teacher-notes.pdf"
doc=fitz.open(pdf)
out="/Users/macbook/Documents/GitHub/abraao-estudo/others/_src/sessao-15-FULL.txt"
with open(out,"w") as f:
    for i in range(100, 115):  # idx 100..114 => pdf 101..115
        f.write(f"\n===== IDX {i}  (PDF page {i+1}) =====\n")
        f.write(doc[i].get_text())
print("saved", out)
# print a condensed view of headings per page
for i in range(100,115):
    t=doc[i].get_text()
    head=" | ".join([l.strip() for l in t.splitlines() if l.strip()][:4])
    print(f"idx{i} pdf{i+1}: {head[:100]}")
