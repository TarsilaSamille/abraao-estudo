#!/usr/bin/env python3
P="abraao/modulo-1/sessao-2.html"
h=open(P,encoding='utf-8').read()
# mapeia hex velho(mudo) -> exato, e tambem cobre Tailwind/estado limpo
OLD={"#a85a43":"#af5267","#3c6049":"#487860","#34588b":"#4877ae","#787878":"#9d9ea7"}
NEW={"red-500":"#af5267","emerald-600":"#487860","blue-600":"#4877ae","indigo-600":"#4877ae",
     "slate-500":"#9d9ea7","slate-800":"#9d9ea7","slate-400":"#9d9ea7","475569":"#9d9ea7","5b7285":"#9d9ea7"}
for a,b in OLD.items(): h=h.replace("border-["+a+"]","border-["+b+"]").replace("bg-["+a+"]","bg-["+b+"]").replace("text-["+a+"]","text-["+b+"]")
for a,b in NEW.items():
    h=h.replace("border-"+a,"border-["+b+"]").replace("bg-"+a,"bg-["+b+"]").replace("text-"+a,"text-["+b+"]")
open(P,"w",encoding="utf-8").write(h)
print("red #af5267 green #487860 blue #4877ae grey #9d9ea7")
