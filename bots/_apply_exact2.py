#!/usr/bin/env python3
P="abraao/modulo-1/sessao-2.html"
h=open(P,encoding='utf-8').read()
R,G,B,K="#af5267","#487860","#4877ae","#9d9ea7"
for a,b in [
 ("border-red-500",f"border-[{R}]"),("bg-red-500",f"bg-[{R}]"),
 ("border-emerald-600",f"border-[{G}]"),("bg-emerald-600",f"bg-[{G}]"),
 ("border-blue-600",f"border-[{B}]"),("bg-blue-600",f"bg-[{B}]"),
 ("border-indigo-600",f"border-[{B}]"),("bg-indigo-600",f"bg-[{B}]"),
 ("border-slate-500",f"border-[{K}]"),("bg-slate-500",f"bg-[{K}]"),
 ("border-slate-800",f"border-[{K}]"),("bg-slate-800",f"bg-[{K}]"),
 ("text-red-600",f"text-[{R}]"),("text-red-700",f"text-[{R}]"),
 ("text-emerald-600",f"text-[{G}]"),("text-emerald-700",f"text-[{G}]"),
 ("text-blue-600",f"text-[{B}]"),("text-blue-700",f"text-[{B}]"),
 ("text-indigo-600",f"text-[{B}]"),
 ("border-slate-400",f"border-[{K}]"),
 ("border-[#787878]",f"border-[{K}]"),
]:
    h=h.replace(a,b)
h=h.replace("#475569",K).replace("#5b7285",K).replace("#787878",K)
open(P,"w",encoding="utf-8").write(h)
print("done red",R,"green",G,"blue",B,"grey",K)
