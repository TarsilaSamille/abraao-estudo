#!/usr/bin/env python3
# Aplica cores EXATAS do PDF, SEPARADAS POR DESIGN (4 designs).
P="abraao/modulo-1/sessao-2.html"
lines=open(P,encoding='utf-8').read().split('\n')
D1_GREY="#a2a2ae"
D2={"green":"#388060","red":"#b84860","blue":"#3078b0"}
D3={"green":"#388060","red":"#b84860","blue":"#3078b0","violet":"#6898c8"}
D4={"green":"#388060","red":"#b05038","blue":"#c8f0f8"}
i_d2=381
i_d3=490
i_d4=None
for i,l in enumerate(lines,1):
    if "<!-- VISUAL DIAGRAM 3 -->" in l: i_d4=i
if i_d4 is None: i_d4=len(lines)-50

# hex velhos que podem estar no baseline
OLD={"#307860":None,"#b44860":None,"#3078b4":None,"#9c9ca8":None,
     "#787878":None,"#ae5266":None,"#4c7c60":None,"#4876ae":None,
     "#af5267":None,"#487860":None,"#4877ae":None,"#9d9ea7":None,
     "#a85a43":None,"#3c6049":None,"#34588b":None,"#9c9ca4":None}

def subst(line, pal, grey):
    repl=[
      ("border-red-500",f"border-[{pal['red']}]"),("bg-red-500",f"bg-[{pal['red']}]"),
      ("text-red-600",f"text-[{pal['red']}]"),("text-red-700",f"text-[{pal['red']}]"),
      ("border-emerald-600",f"border-[{pal['green']}]"),("bg-emerald-600",f"bg-[{pal['green']}]"),
      ("text-emerald-600",f"text-[{pal['green']}]"),("text-emerald-700",f"text-[{pal['green']}]"),
      ("border-blue-600",f"border-[{pal['blue']}]"),("bg-blue-600",f"bg-[{pal['blue']}]"),
      ("text-blue-600",f"text-[{pal['blue']}]"),("text-blue-700",f"text-[{pal['blue']}]"),
      ("border-indigo-600",f"border-[{pal.get('violet',pal['blue'])}]"),("bg-indigo-600",f"bg-[{pal.get('violet',pal['blue'])}]"),
      ("text-indigo-600",f"text-[{pal.get('violet',pal['blue'])}]"),
      ("border-slate-500",f"border-[{grey}]"),("bg-slate-500",f"bg-[{grey}]"),
      ("border-slate-800",f"border-[{grey}]"),("bg-slate-800",f"bg-[{grey}]"),
      ("border-slate-400",f"border-[{grey}]"),
    ]
    for a,b in repl: line=line.replace(a,b)
    # converte hex velhos -> cor do design atual
    for oh in list(OLD):
        for pre in ("border-[","bg-[","text-["):
            if pre+oh+"]" in line:
                line=line.replace(pre+oh+"]", pre+ (grey if oh in("#787878","#9c9ca8","#9c9ca4","#9d9ea7") else pal['red'] if oh in("#b44860","#ae5266","#af5267","#a85a43","#b05038") else pal['green'] if oh in("#307860","#4c7c60","#487860","#3c6049") else pal['blue'] if oh in("#3078b4","#4876ae","#4877ae","#34588b") else grey) +"]")
    return line

out=[]
for i,l in enumerate(lines,1):
    if i<i_d2: out.append(subst(l, {"red":D1_GREY,"green":D1_GREY,"blue":D1_GREY,"violet":D1_GREY}, D1_GREY))
    elif i<i_d3: out.append(subst(l, D2, D1_GREY))
    elif i<i_d4: out.append(subst(l, D3, D1_GREY))
    else: out.append(subst(l, D4, D1_GREY))
txt="\n".join(out)
txt=txt.replace("#475569",D1_GREY).replace("#5b7285",D1_GREY)
txt=txt.replace("border: 1.5px solid #a2a2ae","border: 1.5px solid "+D1_GREY).replace("border: 1.5px solid #787878","border: 1.5px solid "+D1_GREY)
txt=txt.replace("background: #a2a2ae","background: "+D1_GREY).replace("background: #787878","background: "+D1_GREY)
open(P,"w",encoding="utf-8").write(txt)
print("done")
