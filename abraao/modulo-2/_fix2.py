# -*- coding: utf-8 -*-
import re, io
P = 'sessao-4.html'
s = io.open(P, encoding='utf-8').read()
miss = []

def rep(old, new, n=1):
    global s
    pat = re.compile(r'\s+'.join(map(re.escape, old.split())))
    if len(pat.findall(s)) < n:
        miss.append(old[:70]); return
    s = pat.sub(lambda m: new, s, count=n)

# ---- p.25: paragrafo final ausente ----
P25 = '''<p>
    <span class="lang-pt">Note como a jornada de “toda a terra” em Gênesis 6:1-11:26 aprofunda o retrato temático da natureza humana expresso em Gênesis 6:5 e 8:21: “os humanos são maus desde a sua juventude”. Eles tomam o potencial e a unidade dados por Deus e os usam para fins egoístas e (que se tornarão) imperiais: a deificação e a exaltação do seu próprio nome.</span>
    <span class="lang-en">Notice how the sojourn of “all the land” in Genesis 6:1-11:26 furthers the thematic portrait of human nature expressed in Genesis 6:5 and 8:21, “humans are bad from their youth.” They take their God-given potential and unity and use it for selfish and (what will become) imperial ends: the deification and exaltation of their name.</span>
</p>
<p>'''
rep('<p>Em contraste, a jornada de Terá começa com a trágica morte', P25 + 'Em contraste, a jornada de Terá começa com a trágica morte')

# ---- Secao: Foco Narrativo da Biblia Hebraica (antes da Questao para Reflexao) ----
SEC = '''<h2 class="text-3xl font-bold text-slate-900 mb-6 mt-12">
    <span class="lang-pt">Foco Narrativo da Bíblia Hebraica</span>
    <span class="lang-en">Narrative Focus of the Hebrew Bible</span>
</h2>
<div class="rounded-xl border border-slate-300 p-6">
    <div class="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-slate-500 mb-4">
        <span>GEN 1&mdash;11</span><span>GEN 12 &mdash;&mdash;&mdash; OT</span><span>NT</span>
    </div>
    <div class="flex items-stretch gap-3">
        <div class="flex-1 border-t-4 border-slate-800 pt-2 text-center text-sm font-bold text-slate-800">
            <span class="lang-pt">DEUS &amp; HUMANIDADE</span><span class="lang-en">GOD &amp; HUMANITY</span>
        </div>
        <div class="flex-[2] space-y-3">
            <div class="border-t-4 border-dashed border-slate-500 pt-2 text-center text-sm font-bold text-slate-700">
                <span class="lang-pt">DEUS &amp; NAÇÕES</span><span class="lang-en">GOD &amp; NATIONS</span>
            </div>
            <div class="border-t-4 border-slate-800 pt-2 text-center text-sm font-bold text-slate-800">
                <div>AVRAHAM</div>
                <div><span class="lang-pt">DEUS &amp; ISRAEL</span><span class="lang-en">GOD &amp; ISRAEL</span></div>
            </div>
        </div>
        <div class="flex items-center text-lg font-extrabold text-slate-900">
            <span class="mr-1">&gt;</span><span class="lang-pt">JESUS</span><span class="lang-en">JESUS</span>
        </div>
    </div>
</div>
<p class="mt-2 text-xs italic text-slate-500">
    <span class="lang-pt">Foco Narrativo da Bíblia Hebraica. Ilustração criada por Tim Mackie para BibleProject Classroom: Abraham (2021).</span>
    <span class="lang-en">Narrative Focus of the Hebrew Bible. Illustration created by Tim Mackie for BibleProject Classroom: Abraham (2021).</span>
</p>

<h2 class="text-2xl font-bold text-slate-800 my-10">'''
rep('<h2 class="text-2xl font-bold text-slate-800 my-10">Questão para Reflexão</h2>',
    SEC + '<span class="lang-pt">Questão para Reflexão</span><span class="lang-en">Reflection Question</span></h2>')

io.open(P, 'w', encoding='utf-8').write(s)
print('MISS:', miss)
