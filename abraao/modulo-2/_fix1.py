import re, io, sys
P = 'sessao-4.html'
s = io.open(P, encoding='utf-8').read()
miss = []

def rep(old, new, n=1):
    global s
    pat = re.compile(r'\s+'.join(map(re.escape, old.split())))
    found = len(pat.findall(s))
    if found < n:
        miss.append((old[:70], found)); return
    s = pat.sub(lambda m: new, s, count=n)

STYLE = '''    <style>
        html[lang="en"] .lang-pt { display: none !important; }
        html[lang="pt"] .lang-en, html[lang="pt-BR"] .lang-en { display: none !important; }
        .heb { font-family: 'SBL Hebrew', 'Times New Roman', serif; direction: rtl; unicode-bidi: embed; }
        .k { display: inline; padding: 2px 7px; border-radius: 6px; font-weight: 700; line-height: 1.4;
             box-decoration-break: clone; -webkit-box-decoration-break: clone; }
        .k-lpurp  { background: #e6e6f9; color: #6d4cba; }
        .k-lblue  { background: #cfe0f7; color: #2b5fb0; }
        .k-lteal  { background: #cdeef0; color: #0c7c99; }
        .k-lred   { background: #f9e3de; color: #972a4e; }
        .k-tan    { background: #f5e1bd; color: #823221; }
        .k-lgreen { background: #d9ead3; color: #38761d; }
        .k-lorange{ background: #fce5cd; color: #b45f06; }
        .k-gray   { background: #e2e6eb; color: #475069; }
        .tx-blue  { color: #3b5299; font-weight: 700; }
        .tx-tan   { color: #8a6d3b; font-weight: 700; }
        .t-box { border: 2px solid #d1d5db; border-radius: 12px; padding: 1rem; background: #fff; margin-bottom: 1rem; }
        .t-box.black { border-color: #111827; }
        @media print { .print\\:hidden { display: none !important; }
            * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; } }
    </style>
</head>'''
s = s.replace('</head>', STYLE, 1)

# ---- CORES: chips semanticos ----
s, n_tan = re.subn(r'class="[^"]*bg-orange-200[^"]*text-yellow-900[^"]*"', 'class="k k-tan"', s)
s, n_tan2 = re.subn(r'class="[^"]*text-yellow-900[^"]*bg-orange-200[^"]*"', 'class="k k-tan"', s)
s, n_lblue = re.subn(r'class="[^"]*bg-blue-100[^"]*text-blue-900[^"]*"', 'class="k k-lblue"', s)
s, n_lgreen = re.subn(r'class="[^"]*bg-green-200[^"]*text-green-900[^"]*"', 'class="k k-lgreen"', s)
s, n_lorange = re.subn(r'class="[^"]*bg-orange-100[^"]*text-orange-900[^"]*"', 'class="k k-lorange"', s)
s, n_txblue = re.subn(r'class="\s*font-semibold text-blue-900\s*"', 'class="tx-blue"', s)
s, n_txtan = re.subn(r'class="\s*font-semibold text-orange-700\s*"', 'class="tx-tan"', s)

# ---- BORDA: Grossman -> barra preta grossa ----
rep('<blockquote class="border-l-4 border-gray-700 p-6 my-8 text-slate-600 bg-gray-50">',
    '<blockquote class="border-l-8 border-black p-6 my-8 text-slate-600 bg-slate-50">')
# ---- BORDA: 12:1-2 / 12:4 / 12:7 -> cinza claro ----
s, n_gray = re.subn(r'border-l-4 border-green-400 bg-green-50', 'border-l-4 border-slate-400 bg-slate-50', s)

# ---- CONTEUDO: 11:1-9 -> 11:27-12:9 em "Um Novo Noe" ----
rep('data-reference="Gênesis+11:1-9">11:1-9</a> em um paralelo',
    'data-reference="Gênesis+11:27-12:9">11:27-12:9</a> em um paralelo')

io.open(P, 'w', encoding='utf-8').write(s)
print('tan', n_tan + n_tan2, 'lblue', n_lblue, 'lgreen', n_lgreen, 'lorange', n_lorange,
      'txblue', n_txblue, 'txtan', n_txtan, 'graybq', n_gray)
print('MISS:', miss)
