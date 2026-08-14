#!/usr/bin/env python3
# Aplica as cores EXATAS (color picker na imagem do usuario) em sessao-2.
# red #a85a43 | green #3c6049 | blue #34588b | grey #787878
import sys
P="abraao/modulo-1/sessao-2.html"
h=open(P,encoding='utf-8').read()
R,G,B,K="#a85a43","#3c6049","#34588b","#787878"
repl=[
 # Diagramas (Section 2) - bordas
 ("border-red-500",f"border-[{R}]"),("bg-red-500",f"bg-[{R}]"),
 ("border-emerald-600",f"border-[{G}]"),("bg-emerald-600",f"bg-[{G}]"),
 ("border-blue-600",f"border-[{B}]"),("bg-blue-600",f"bg-[{B}]"),
 ("border-indigo-600",f"border-[{B}]"),("bg-indigo-600",f"bg-[{B}]"),
 ("border-slate-500",f"border-[{K}]"),("bg-slate-500",f"bg-[{K}]"),
 ("border-slate-800",f"border-[{K}]"),("bg-slate-800",f"bg-[{K}]"),
 # textos de cor
 ("text-red-600",f"text-[{R}]"),("text-red-700",f"text-[{R}]"),
 ("text-emerald-600",f"text-[{G}]"),("text-emerald-700",f"text-[{G}]"),
 ("text-blue-600",f"text-[{B}]"),("text-blue-700",f"text-[{B}]"),
 ("text-indigo-600",f"text-[{B}]"),
 # Design 1 (Macro) - slate-400 nas caixas
 ("border-slate-400",f"border-[{K}]"),
]
for a,b in repl:
    h=h.replace(a,b)
# CSS do Design 1
h=h.replace("#475569",K).replace("#5b7285",K)
open(P,"w",encoding="utf-8").write(h)
print("aplicado: red",R,"green",G,"blue",B,"grey",K)
