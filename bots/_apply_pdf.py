#!/usr/bin/env python3
# Cores EXATAS do sessao-2.pdf (pdftocairo 150dpi, pagina do design).
# red #b44860 | green #307860 | blue #3078b4 | grey #9c9ca8
P="abraao/modulo-1/sessao-2.html"
h=open(P,encoding='utf-8').read()
R,G,B,K="#b44860","#307860","#3078b4","#9c9ca8"
OLD=["#a85a43","#3c6049","#34588b","#787878","#ae5266","#4c7c60","#4876ae","#9c9ca4","#af5267","#487860","#4877ae","#9d9ea7"]
for old in OLD:
    for pre in ("border-[","bg-[","text-["):
        h=h.replace(pre+old+"]",pre+({"#a85a43":R,"#3c6049":G,"#34588b":B,"#787878":K,"#ae5266":R,"#4c7c60":G,"#4876ae":B,"#9c9ca4":K,"#af5267":R,"#487860":G,"#4877ae":B,"#9d9ea7":K}[old])+"]")
TW=[("border-red-500",f"border-[{R}]"),("bg-red-500",f"bg-[{R}]"),
 ("border-emerald-600",f"border-[{G}]"),("bg-emerald-600",f"bg-[{G}]"),
 ("border-blue-600",f"border-[{B}]"),("bg-blue-600",f"bg-[{B}]"),
 ("border-indigo-600",f"border-[{B}]"),("bg-indigo-600",f"bg-[{B}]"),
 ("border-slate-500",f"border-[{K}]"),("bg-slate-500",f"bg-[{K}]"),
 ("border-slate-800",f"border-[{K}]"),("bg-slate-800",f"bg-[{K}]"),
 ("border-slate-400",f"border-[{K}]"),
 ("text-red-600",f"text-[{R}]"),("text-red-700",f"text-[{R}]"),
 ("text-emerald-600",f"text-[{G}]"),("text-emerald-700",f"text-[{G}]"),
 ("text-blue-600",f"text-[{B}]"),("text-blue-700",f"text-[{B}]"),
 ("text-indigo-600",f"text-[{B}]")]
for a,b in TW: h=h.replace(a,b)
h=h.replace("#475569",K).replace("#5b7285",K)
h=h.replace("border: 1.5px solid #787878","border: 1.5px solid "+K).replace("background: #787878","background: "+K)
open(P,"w",encoding="utf-8").write(h)
print("PDF-exact: red",R,"green",G,"blue",B,"grey",K)
