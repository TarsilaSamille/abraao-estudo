# -*- coding: utf-8 -*-
import io
P = 'sessao-4.html'
s = io.open(P, encoding='utf-8').read()

def swap(start_marker, new):
    global s
    i = s.index(start_marker)
    a = s.rindex('<table', 0, i)
    b = s.index('</table>', i) + len('</table>')
    s = s[:a] + new + s[b:]

L = lambda r, t: '<a href="#" class="verse-link hover:underline" data-reference="%s">%s</a>' % (r, t)
def B(pt, en):
    return '<span class="lang-pt">%s</span><span class="lang-en">%s</span>' % (pt, en)
NAME_PT = '<span class="k k-lblue">nome</span>'
NAME_EN = '<span class="k k-lblue">name</span>'
def OUT(pt, en):
    return '<span class="k k-lpurp">%s</span>' % pt, '<span class="k k-lpurp">%s</span>' % en

# ---------- TABELA 1: Noe x Avram ----------
t1 = '''<table class="w-full text-left text-slate-700">
    <thead class="bg-slate-100 text-slate-800">
        <tr>
            <th class="p-4 w-1/2">''' + B('Saída de Noé da Arca e Bênção Familiar', "Noah’s Exit From the Ark and Family Blessing") + '''</th>
            <th class="p-4 w-1/2">''' + B('Saída de Avram da Babilônia e Bênção Familiar', "Avram’s Exit From Babylon and Family Blessing") + '''</th>
        </tr>
    </thead>
    <tbody class="divide-y divide-slate-200">
        <tr class="align-top">
            <td class="p-4">''' + B('Dez gerações de Adão a Noé; 3 filhos', 'Ten generations from Adam to Noah; 3 sons') + '''</td>
            <td class="p-4">''' + B('Dez gerações de Noé a Avram (de 3 filhos)', 'Ten generations from Noah to Avram (of 3 sons)') + '''</td>
        </tr>
        <tr class="align-top">
            <td class="p-4"><b>''' + L('Gênesis+6:1-4', 'Gn. 6:1-4') + '''</b>
                ''' + B('A história do dilúvio começa com violência e derramamento de sangue perpetrados por guerreiros e “homens do ' + NAME_PT + '”.',
                        'The flood story begins with violence and bloodshed perpetrated by warriors and “men of the ' + NAME_EN + '.”') + '''</td>
            <td class="p-4"><b>''' + L('Gênesis+10:8-12', 'Gn. 10:8-12') + '''</b>
                ''' + B('Babilônia é fundada por um guerreiro violento, um homem do ' + NAME_PT + '.',
                        'Babylon is founded by a violent warrior, a man of the ' + NAME_EN + '.') + '''<br>
                <b>''' + L('Gênesis+11:1-9', 'Gn. 11:1-9') + '''</b>
                ''' + B('Babilônia é construída por pessoas que buscam fazer um ' + NAME_PT + ' para si mesmas.',
                        'Babylon is built by people who seek to make a ' + NAME_EN + ' for themselves.') + '''</td>
        </tr>
        <tr class="align-top">
            <td class="p-4">''' + B('Noé e aqueles com ele são abrigados na arca durante o dilúvio.',
                                    'Noah and those with him are sheltered in the ark during the flood.') + '''</td>
            <td class="p-4">''' + B('Terá e aqueles com ele se refugiam em Harã após a dispersão da Babilônia.',
                                    'Terakh and those with him take refuge in Haran after the scattering of Babylon.') + '''</td>
        </tr>
        <tr class="align-top">
            <td class="p-4">''' + B('Noé “sai” da arca com sua família (<span class="heb">יצא</span> repetido 4x em Gn. ' + L('Gênesis+8:16-19', '8:16-19') + '): “e <span class="k k-lpurp">Noé saiu da</span> arca, e seus filhos, sua esposa e as esposas de seus filhos”.',
                                    'Noah “goes out” from the ark with his family (<span class="heb">יצא</span> repeated 4x in Gen. ' + L('Gênesis+8:16-19', '8:16-19') + '): “and <span class="k k-lpurp">Noah went out from</span> the ark, and his sons and his wife and his sons’ wives.”') + '''</td>
            <td class="p-4"><b>''' + L('Gênesis+11:31', 'Gn. 11:31') + '''</b>
                ''' + B('Terá “saiu” da Babilônia com sua família: “e Terá tomou Avram seu filho... <span class="k k-lpurp">e eles saíram com eles de</span> Ur dos Caldeus”.',
                        'Terakh “went out” from Babylon with his family: “and Terakh took Avram his son ... <span class="k k-lpurp">and they went out with them from</span> Ur of the Chaldeans.”') + '''<br>
                <b>''' + L('Gênesis+12:5', 'Gn. 12:5') + '''</b>
                ''' + B('Avram “saiu” de Harã com sua família: “e Avram tomou sua esposa e o filho de seu irmão... <span class="k k-lpurp">e eles saíram para ir para a terra de Canaã</span>”.',
                        'Avram “went out” from Haran with his family: “and Avram took his wife and the son of his brother ... <span class="k k-lpurp">and they went out to go to the land of Canaan</span>.”') + '''</td>
        </tr>
        <tr class="align-top">
            <td class="p-4">''' + B('Deus promete que Noé e sua esposa serão “frutíferos e se multiplicarão”.',
                                    'God promises that Noah and his wife will be “fruitful and multiply.”') + '''<br>
                <b>''' + L('Gênesis+9:1', 'Gn. 9:1') + '''</b>
                ''' + B('“E Deus abençoou Noé e seus filhos e disse: ‘Sede fecundos, multiplicai-vos e enchei a terra’”.',
                        '“And God blessed them and said, ‘Be fruitful and multiply and fill the land.’”') + '''</td>
            <td class="p-4">''' + B('Deus promete fazer Avram e sua esposa “frutíferos e se multiplicarem”.',
                                    'God promises to make Avram and his wife “fruitful and multiply.”') + '''<br>
                <b>''' + L('Gênesis+12:1-2', 'Gn. 12:1-2') + '''</b>
                ''' + B('“E Yahweh disse a Avram: ‘... Farei de ti uma grande nação e te abençoarei...’”.',
                        '“And Yahweh said to Avram, ‘... I will make you a great nation and I will bless you ...’”') + '''</td>
        </tr>
    </tbody>
</table>'''
swap('Saída de Noé da Arca', t1)

# ---------- TABELA 2: Duas Jornadas ----------
def row(ptl, enl, ptr, enr, cls='align-top text-sm'):
    return ('<tr class="%s"><td class="p-4">%s</td><td class="p-4">%s</td></tr>'
            % (cls, B(ptl, enl), B(ptr, enr)))

t2 = '''<table class="w-full text-left text-slate-700">
    <thead class="bg-slate-100 text-slate-800">
        <tr>
            <th class="p-4 w-1/2">''' + L('Gênesis+11:1-9', B('Gênesis 11:1-9 <br>Uma Jornada para o Desastre', 'Genesis 11:1-9 <br>A Sojourn Into Disaster')) + '''</th>
            <th class="p-4 w-1/2">''' + L('Gênesis+11:27-12:9', B('Gênesis 11:27-12:9 <br>Uma Jornada para a Bênção', 'Genesis 11:27-12:9 <br>A Sojourn Into Blessing')) + '''</th>
        </tr>
    </thead>
    <tbody class="divide-y divide-slate-200">
''' + row(
  'Começa com “toda a terra... viajando (<span class="heb">נסע</span>) do leste (<span class="heb">מקדם</span>)” ' + L('Gênesis+11:1-2', '[11:1-2]') + '<br>Conclui com “toda a terra” sendo “espalhada” (<span class="heb">נפוץ / הפיץ</span>) ' + L('Gênesis+11:9', '[11:9]'),
  'Begins with “all the land ... journeying (<span class="heb">נסע</span>) from the east (<span class="heb">מקדם</span>)” ' + L('Gênesis+11:1-2', '[11:1-2]') + '<br>Concludes with “all the land” being “scattered” (<span class="heb">נפוץ / הפיץ</span>) ' + L('Gênesis+11:9', '[11:9]'),
  'Começa com uma família saindo (<span class="heb">ויצאו</span>) do lugar da dispersão, Ur dos Caldeus ' + L('Gênesis+11:31', '[11:31]') + '<br>Conclui com Avram “viajando” (<span class="heb">נסע</span>) para Canaã em lugares “do leste” (<span class="heb">מקדם</span>) ' + L('Gênesis+12:8-9', '[12:8-9]'),
  'Begins with one family leaving (<span class="heb">ויצאו</span>) the place of scattering, Ur of the Chaldeans ' + L('Gênesis+11:31', '[11:31]') + '<br>Concludes with Avram “journeying” (<span class="heb">נסע</span>) into Canaan in places “from the east” (<span class="heb">מקדם</span>) ' + L('Gênesis+12:8-9', '[12:8-9]')
) + row(
  'Eles encontram uma “planície em Sinar” e “ali se estabeleceram” (<span class="heb">וישבו שם</span>) ' + L('Gênesis+11:2', '[11:2]'),
  'They find a “plain in Shinar” and “they settled there” (<span class="heb">וישבו שם</span>) ' + L('Gênesis+11:2', '[11:2]'),
  'Eles chegam a Harã e “ali se estabeleceram” (<span class="heb">וישבו שם</span>) ' + L('Gênesis+11:31', '[11:31]'),
  'They come to Haran and “they settled there” (<span class="heb">וישבו שם</span>) ' + L('Gênesis+11:31', '[11:31]')
) + row(
  '“Vamos construir (<span class="heb">בנה</span>) para nós uma cidade e uma torre” ' + L('Gênesis+11:4', '[11:4]') + '<br>“... a cidade e a torre que os filhos de Adão construíram (<span class="heb">בנה</span>) para si mesmos” ' + L('Gênesis+11:5', '[11:5]'),
  '“Let us build (<span class="heb">בנה</span>) for ourselves a city and tower” ' + L('Gênesis+11:4', '[11:4]') + '<br>“... the city and tower which the sons of ’adam built (<span class="heb">בנה</span>) for themselves” ' + L('Gênesis+11:5', '[11:5]'),
  '“e Yahweh disse” (<span class="heb">ויאמר יהוה</span>) ' + L('Gênesis+12:1', '[12:1]') + ' seguido por uma reversão de circunstâncias — da esterilidade ao nascimento',
  '“and Yahweh said” (<span class="heb">ויאמר יהוה</span>) ' + L('Gênesis+12:1', '[12:1]') + ' followed by a reversal of circumstances — from barrenness to birth'
) + row(
  '“Façamos para nós um nome (<span class="heb">שם</span>)” ' + L('Gênesis+11:4', '[11:4]'),
  '“Let us make a name (<span class="heb">שם</span>) for ourselves” ' + L('Gênesis+11:4', '[11:4]'),
  '“Eu farei grande o seu nome (<span class="heb">שם</span>)” ' + L('Gênesis+12:2', '[12:2]'),
  '“I will make great your name (<span class="heb">שם</span>)” ' + L('Gênesis+12:2', '[12:2]')
) + row(
  '“e Yahweh disse” (<span class="heb">ויאמר יהוה</span>) ' + L('Gênesis+11:6', '[11:6]') + ' seguido por uma reversão de circunstâncias — da construção à dispersão',
  '“and Yahweh said” (<span class="heb">ויאמר יהוה</span>) ' + L('Gênesis+11:6', '[11:6]') + ' followed by a reversal of circumstances — from building to scattering',
  '“e [Avram] construiu (<span class="heb">בנה</span>) ali um altar a Yahweh” ' + L('Gênesis+12:7', '[12:7]') + '<br>“e [Avram] construiu (<span class="heb">בנה</span>) ali um altar a Yahweh e invocou o nome (<span class="heb">שם</span>) de Yahweh.” ' + L('Gênesis+12:8', '[12:8]'),
  '“and [Avram] built (<span class="heb">בנה</span>) there an altar to Yahweh” ' + L('Gênesis+12:7', '[12:7]') + '<br>“and [Avram] built (<span class="heb">בנה</span>) there an altar to Yahweh and he called upon the name (<span class="heb">שם</span>) of Yahweh.” ' + L('Gênesis+12:8', '[12:8]')
) + row(
  'Uma jornada para o oeste que termina com o estabelecimento de humanos que usam seu potencial para seu próprio nome, de modo que Yahweh se torna o antagonista e reverte suas circunstâncias.',
  'A westward sojourn that ends with settlement by humans who use their potential for their own name, so that Yahweh becomes the antagonist and reverses their circumstances.',
  'Uma jornada para o oeste que termina com o estabelecimento de humanos que não têm potencial para fazer um nome para si mesmos, de modo que Yahweh se torna o protagonista e reverte suas circunstâncias.',
  'A westward sojourn that ends with settlement by humans who have no potential to make a name for themselves, so that Yahweh becomes the protagonist and reverses their circumstances.',
  'align-top text-sm bg-slate-50'
) + '''
    </tbody>
</table>'''
swap('Uma Jornada para o\n                                            Desastre', t2)

io.open(P, 'w', encoding='utf-8').write(s)
print('ok')
