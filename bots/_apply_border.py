#!/usr/bin/env python3
# Aplica cores EXATAS da BORDA do PDF (metodo border-only), separadas por design.
P="abraao/modulo-1/sessao-2.html"
lines=open(P,encoding='utf-8').read().split('\n')
D1="#6c7080"  # macro (usar cinza do V4 pedido antes? usuario nao rejeitou D1; manter #6c7080)
D2={"green":"#3a8060","red":"#be4967","blue":"#3678b4"}
D3={"green":"#3a8060","red":"#be4967","blue":"#3678b4","violet":"#6898c8"}
D4={"green":"#3a8060","red":"#b5543a","blue":"#ccf1fa"}
i_d2=381;i_d3=490;i_d4=len(lines)
for i,l in enumerate(lines,1):
    if "<!-- VISUAL DIAGRAM 3 -->" in l: i_d4=i
OLD={"#307860":"","#b44860":"","#3078b4":"","#9c9ca8":"","#787878":"","#ae5266":"","#4c7c60":"","#4876ae":"#4876ae","#af5267":"","#487860":"","#4877ae":"","#9d9ea7":"","#a85a43":"","#3c6049":"","#34588b":"","#9c9ca4":"","#388060":"","#b84860":"","#3078b0":"","#6898c8":"","#b05038":"","#c8f0f8":"","#a2a2ae":"","#6c7080":"","#7b6fd0":"","#d06a3a":"","#5fb8c8":""}
def sub(line,pal,grey):
    for a,b in [("border-red-500",f"border-[{pal['red']}]"),("bg-red-500",f"bg-[{pal['red']}]"),("text-red-600",f"text-[{pal['red']}]"),("text-red-700",f"text-[{pal['red']}]"),
      ("border-emerald-600",f"border-[{pal['green']}]"),("bg-emerald-600",f"bg-[{pal['green']}]"),("text-emerald-600",f"text-[{pal['green']}]"),("text-emerald-700",f"text-[{pal['green']}]"),
      ("border-blue-600",f"border-[{pal['blue']}]"),("bg-blue-600",f"bg-[{pal['blue']}]"),("text-blue-600",f"text-[{pal['blue']}]"),("text-blue-700",f"text-[{pal['blue']}]"),
      ("border-indigo-600",f"border-[{pal.get('violet',pal['blue'])}]"),("bg-indigo-600",f"bg-[{pal.get('violet',pal['blue'])}]"),("text-indigo-600",f"text-[{pal.get('violet',pal['blue'])}]"),
      ("border-slate-500",f"border-[{grey}]"),("bg-slate-500",f"bg-[{grey}]"),("border-slate-800",f"border-[{grey}]"),("bg-slate-800",f"bg-[{grey}]"),("border-slate-400",f"border-[{grey}]")]:
        line=line.replace(a,b)
    for oh in list(OLD):
        for pre in ("border-[","bg-[","text-["):
            if pre+oh+"]" in line:
                t=grey if oh in("#787878","#9c9ca8","#9c9ca4","#a2a2ae","#6c7080") else pal['red'] if oh in("#b44860","#ae5266","#af527","#a85a43","#b05038","#d06a3a","#be4967","#be5467") else pal['green'] if oh in("#307860","#4c7c60","#487860","#3c6049","#388060","#3a8060") else pal['blue'] if oh in("#3078b4","#4876ae","#4877ae","#34588b","#3078b0","#c8f0f8","#5fb8c8","#ccf1fa","#ccf0f8") else (pal.get('violet',grey) if oh in("#6898c8","#7b6fd0") else grey)
                line=line.replace(pre+oh+"]",pre+t+"]")
    return line
out=[]
for i,l in enumerate(lines,1):
    if i<i_d2: out.append(sub(l,{"red":D1,"green":D1,"blue":D1,"violet":D1},D1))
    elif i<i_d3: out.append(sub(l,D2,D1))
    elif i<i_d4: out.append(sub(l,D3,D1))
    else: out.append(sub(l,D4,D1))
txt="\n".join(out)
txt=txt.replace("#475569",D1).replace("#5b7285",D1).replace("border: 1.5px solid #a2a2ae","border: 1.5px solid "+D1).replace("border: 1.5px solid #9c9ca8","border: 1.5px solid "+D1).replace("border: 1.5px solid #787878","border: 1.5px solid "+D1).replace("background: #a2a2ae","background: "+D1).replace("background: #9c9ca8","background: "+D1).replace("background: #787878","background: "+D1)
open(P,"w",encoding="utf-8").write(txt)
print("BORDER-EXACT applied: D2",D2,"| D3+v",D3["violet"],"| D4",D4)
