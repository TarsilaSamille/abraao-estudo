# Chapter data for Atos dos Apostolos — chapters 1-14.
# Content is a faithful PT rendering of BibleProject's "Guide to the Book of Acts"
# (bibleproject.com/guides/book-of-acts) + overview videos. Not a literal
# teacher-notes PDF (none exists for Acts), so this course is NOT in the root catalog.
# Schema per chapter:
#   t = title_pt
#   k = list of 3 Key-Takeaway bullets (PT)
#   p = prose HTML (PT) — may include verse-link spans
#   d = design key (see gen_atos_sessions.py) or None
#   r = Questao para Refle xo (PT)

CHAPTERS_A = {
    "1": {
        "t": "A Comissão e a Ascensão",
        "k": [
            "Atos é o segundo volume da obra unificada que conhecemos como Lucas-Atos; o primeiro volume foi o Evangelho de Lucas.",
            "Jesus promete o Espírito e envia os discípulos como testemunhas de Jerusalém, Judeia e Samaria até os confins da terra (Atos 1:8).",
            "O título tradicional \"Atos dos Apóstolos\" é impreciso — o personagem que unifica o livro do início ao fim é Jesus, agindo pessoalmente ou pelo Espírito.",
        ],
        "p": """
        <p>O livro começa recontando como o Jesus ressurreto passou cerca de 40 dias com seus discípulos ensinando-os \"a respeito do Reino de Deus\" (<span class="verse-link" data-reference="Atos+1:3">Atos 1:3</span>), ligando-se de volta à história do Evangelho de Lucas. Ali, Jesus afirmara que estava restauraindo o Reino de Deus sobre o mundo, começando por Israel. Ele chamou Israel a viver sob o seu reinado seguiindo-o, e foi entronizado como o Rei messiânico quando entregou sua vida, conquistando a morte por meio de seu amor.</p>
        <p>Na linha de abertura, Lucas diz: \"Produzi o meu primeiro volume (isto é, o Evangelho) a respeito de tudo o que Jesus começou a fazer e a ensinar\" (<span class="verse-link" data-reference="Atos+1:1">Atos 1:1</span>). Esse versículo é uma pista do que o livro de Atos tratará: no volume um, Jesus começou \"a fazer e a ensinar\"; no volume dois, ele naturalmente continua o que começou. É por isso que o livro poderia ser mais precisamente chamado <em>Atos de Jesus e do Espírito</em>.</p>
        <p>Jesus promete que o Espírito logo virá e os imergirá com sua presença pessoal, cumprindo uma das principais esperanças dos profetas do Antigo Testamento — de que, no Reino messiânico, a presença de Deus, o seu Espírito, passaria a habitar entre o seu povo, transformando seus corações (<span class="verse-link" data-reference="Isaías+32:15">Isaías 32:15</span>; <span class="verse-link" data-reference="Ezequiel+36:26-27">Ezequiel 36:26-27</span>; <span class="verse-link" data-reference="Joel+2:28-32">Joel 2:28-32</span>). Quando isso acontecer, diz Jesus, o Espírito capacitará seus discípulos \"a ser minhas testemunhas em Jerusalém, Judeia e Samaria, e até os confins da terra\" (<span class="verse-link" data-reference="Atos+1:8">Atos 1:8</span>).</p>
        <p>Então Jesus é levado para cima, para fora da vista deles, em uma nuvem. Essa é uma imagem de <span class="verse-link" data-reference="Daniel+7">Daniel 7</span> mostrando que Jesus está agora sendo entronizado como o Filho do Homem, vindicado depois de seu sofrimento. Ele agora participa do governo de Deus sobre o mundo, o qual trará plenamente aqui na terra quando retornar.</p>
        <p>Os temas principais e o <strong>design</strong> de todo o livro fluem diretamente desse capítulo de abertura. Atos é sobre Jesus liderando seu povo, pelo Espírito, para sair pelo mundo e convidar todas as nações a viver sob o seu reinado. A história começa com a mensagem se espalhando em Jerusalém (caps. 2-7), passando para as regiões vizinhas da Judeia e Samaria, cheias de não-judeus (caps. 8-12), e dali para as nações e os confins da terra (caps. 13-28).</p>
        """,
        "d": "geo_thesis",
        "r": "Jesus disse que seus seguidores seriam suas testemunhas \"até os confins da terra\". O que significa, de modo concreto, viver como testemunha do Reino de Jesus hoje, no lugar onde você vive?",
    },
    "2": {
        "t": "O Espírito e a Pentecoste",
        "k": [
            "O Espírito desce em Pentecoste como vento e fogo sobre os discípulos, cumprindo a promessa dos profetas de que a presença de Deus habitaria o seu povo.",
            "O vento e o fogo em Atos 2 ecoam a presença gloriosa e ardente de Deus enchendo o tabernáculo e o templo (Êxodo 40; 2 Crônicas 7).",
            "Lucas destaca a composição multi-tribo e internacional de Israel que primeiro respondeu — a reunificação das nações prometida pelos profetas.",
        ],
        "p": """
        <p>O foco permanece em Jerusalém nos capítulos 2-7, enquanto os seguidores de Jesus aguardam na cidade até a festa de Pentecoste, quando peregrinos judeus chegam de todo o mundo antigo. Subitamente, o Espírito Santo vem sobre os discípulos como um grande vento, e algo como chamas aparece sobre a cabeça de cada pessoa. Juntos, eles começam a anunciar e contar as \"proezas de Deus\" (<span class="verse-link" data-reference="Atos+2:11">Atos 2:11</span>), falando em todas as línguas que antes não conheciam. E, notavelmente, todas as pessoas ali reunidas entendem perfeitamente suas palavras.</p>
        <p>Para ver o que Lucas está enfatizando, é crucial perceber as raízes do Antigo Testamento nessas imagens. Primeiro, o vento e o fogo são uma alusão direta às histórias sobre a presença gloriosa e ardente de Deus enchendo o tabernáculo e o templo (<span class="verse-link" data-reference="Êxodo+40:38">Êxodo 40:38</span>; <span class="verse-link" data-reference="2+C rônicas+7:1-3">2 Crônicas 7:1-3</span>). Essas imagens também recordam as promessas proféticas de que Deus viria habitar, por meio do seu Espírito, no novo templo do Reino messiânico (<span class="verse-link" data-reference="Ezequiel+43">Ezequiel 43</span>; <span class="verse-link" data-reference="Ageu+2">Ageu 2</span>). Aqui em Atos, a presença ardente de Deus vem habitar não um edifício, mas o seu povo. Lucas está dizendo que o novo templo de que falaram os profetas é, na verdade, a nova família da aliança de Jesus.</p>
        <p>Isso se conecta a um segundo ponto. Os profetas prometeram que, quando Deus viesse habitar no seu novo templo, ele reuniria as tribos de Israel sob o Rei messiânico — e então as boas-novas do reinado de Deus seriam anunciadas a todas as nações (<span class="verse-link" data-reference="Isaías+11">Isaías 11</span>; <span class="verse-link" data-reference="Ezequiel+37">Ezequiel 37</span>). Lucas descreve em detalhe a composição internacional e multi-tribo dos israelitas que primeiro responderam à mensagem de Pedro em Pentecoste. Os apóstolos começam a chamar os israelitas a reconhecerem Jesus como o seu Messias, e milhares o fazem, formando novas comunidades de generosidade, adoração e celebração.</p>
        """,
        "d": "pentecost",
        "r": "O Espírito de Deus desceu não sobre um edifício, mas sobre pessoas. Onde você vê hoje a \"presença ardente\" de Deus se manifestando na comunidade de Jesus?",
    },
    "3": {
        "t": "Pedro, João e o Homem Coxo",
        "k": [
            "Lucas conta um \"conto de dois templos\": a comunidade de Jesus (o novo templo) em contraste com o templo de Jerusalém.",
            "Pedro cura um coxo à porta do templo e é preso pelos líderes; em cada caso, ele declara que Jesus é o verdadeiro Rei de Israel.",
            "No centro da simetria está a generosidade da comunidade — cumprindo o propósito original que a lei destinava ao templo.",
        ],
        "p": """
        <p>Nem todos estão celebrando. Lucas também mostra como a nova família de Jesus enfrentou rapidamente a hostilidade dos líderes de Jerusalém. Com um design belamente simétrico nos capítulos 3-5, Lucas conta um conto de dois templos. O novo templo de Deus — a comunidade dos seguidores de Jesus — reúne-se \"todos os dias no pátio do templo e de casa em casa\" (<span class="verse-link" data-reference="Atos+2:46">Atos 2:46</span>; <span class="verse-link" data-reference="Atos+5:42">Atos 5:42</span>).</p>
        <p>Dentro dessas narrativas espelhadas há duas histórias de Pedro e outros apóstolos curando pessoas nos pátios do templo, apenas para serem presos pelos líderes do templo (<span class="verse-link" data-reference="Atos+3-4">Atos 3-4</span> e <span class="verse-link" data-reference="Atos+5">Atos 5</span>). Cada prisão é seguida por um discurso de Pedro, afirmando que Jesus é o verdadeiro Rei de Israel. No centro dessa simetria estão histórias sobre os seguidores de Jesus que doam propriedades e bens a um fundo comum para ajudar os pobres (<span class="verse-link" data-reference="Atos+4:32-5:11">Atos 4:32-5:11</span>).</p>
        <p>Essa generosidade é maravilhosa, mas parece aleatória vinda de Lucas. Leitores judeus, porém, entenderiam: segundo a lei da Torá (<span class="verse-link" data-reference="Deuteronômio+14-15">Deuteronômio 14-15</span>), essa prática deveria acontecer através do templo de Jerusalém e de seus líderes. O ponto de Lucas é claro: o novo templo da comunidade de Jesus está cumprindo o propósito que Deus sempre teve para o templo de Jerusalém — ser o lugar onde o Céu e a Terra se encontram e onde as pessoas encontram a presença generosa e curadora de Deus.</p>
        """,
        "d": "two_temples",
        "r": "A comunidade de Jesus é chamada de \"novo templo\". O que muda na sua compreensão de igreja quando ela é vista como o lugar da presença de Deus no mundo?",
    },
    "4": {
        "t": "O Arresto e a Oração da Comunidade",
        "k": [
            "Pedro e João são presos por ensinar sobre Jesus, mas libertados após afirmar que só há salvação no seu nome.",
            "A comunidade responde à ameaça com oração coletiva, e o lugar onde estão treme com a presença do Espírito.",
            "A generosidade partilhada (tudo em comum) continua sendo a marca visível do novo templo.",
        ],
        "p": """
        <p>Pedro e João são levados perante os líderes religiosos de Jerusalém. Interrogados sobre \"com que poder\" agiram, Pedro declara publicamente que o homem coxo foi curado \"pelo nome de Jesus Cristo, o Nazareno\" e que \"não há salvação em nenhum outro\" (<span class="verse-link" data-reference="Atos+4:12">Atos 4:12</span>). Os líderes, vendo a ousadia dos apóstolos e não tendo como negar o milagre, os ameaçam e os soltam.</p>
        <p>Ao voltar, a comunidade eleva uma oração coletiva a Deus, citando as Escrituras e pedindo coragem para continuar a falar a sua palavra. Lucas registra que, ao terminarem, \"o lugar em que estavam reunidos tremeu, e todos ficaram cheios do Espírito Santo\" (<span class="verse-link" data-reference="Atos+4:31">Atos 4:31</span>). A resposta de Deus não é livrá-los do conflito, mas enchê-los de sua presença no meio dele.</p>
        <p>É nesse contexto que Lucas insere a descrição da generosidade partilhada: \"Todos os que creram eram uma só alma e um só coração; ninguém considerava propriedade particular o que possuía\" (<span class="verse-link" data-reference="Atos+4:32">Atos 4:32</span>). José, a quem os apóstolos chamaram de Barnabé, vende um campo e deposita o valor aos pés deles — o primeiro de muitos exemplos desse novo padrão de vida.</p>
        """,
        "d": None,
        "r": "A comunidade orou pedindo coragem, não livramento. Quando você ora diante de ameaças, o que costuma pedir — e o que Jesus estaria pedindo?",
    },
    "5": {
        "t": "Ananias, Safira e o Crescimento",
        "k": [
            "Ananias e Safira mentem sobre sua doação e morrem — um aviso sombrio sobre tratar a comunidade com leviandade.",
            "Apesar do conflito interno, sinais e prodígios continuam, e o número de discípulos cresce rapidamente.",
            "Os apóstolos são presos novamente, libertados por um anjo, e continuam ensinando no templo.",
        ],
        "p": """
        <p>Lucas relata o caso de Ananias e Safira, que conspiram para fingir ter doado a totalidade do preço de um campo, retendo uma parte para si, e mentem ao Espírito Santo. Ambos caem mortos aos pés de Pedro (<span class="verse-link" data-reference="Atos+5:1-11">Atos 5:1-11</span>). A história é um aviso solene: a generosidade partilhada do novo templo é sagrada, e brincar com ela tem consequências reais.</p>
        <p>Ao mesmo tempo, Lucas enfatiza que os sinais e prodígios entre o povo continuam, e que \"multidões de homens e mulheres eram acrescentadas ao Senhor\" (<span class="verse-link" data-reference="Atos+5:14">Atos 5:14</span>). Os apóstolos realizam muitos milagres, a ponto de levarem os enfermos às ruas para que ao menos a sombra de Pedro os cobrisse.</p>
        <p>Os líderes do templo prendem novamente os apóstolos, tomados de inveja, mas um anjo do Senhor abre as portas da prisão durante a noite e os manda ensinar no templo. Quando encontrados ali, são levados ao Sinédrio; Gamaliel, um mestre da lei respeitado, aconselha prudência: \"se este plano é de homens, fracassará; se é de Deus, vocês não conseguirão derrotá-los\" (<span class="verse-link" data-reference="Atos+5:38-39">Atos 5:38-39</span>). Apenas açoitados, eles saem alegres por terem sido considerados dignos de sofrer pelo nome de Jesus.</p>
        """,
        "d": None,
        "r": "Ananias e Safira foram julgados por uma mentira dita à comunidade. O que isso revela sobre a seriedade com que Deus leva a vida partilhada da igreja?",
    },
    "6": {
        "t": "Estêvão e os Sete",
        "k": [
            "A igreja nomeia sete homens para servir às mesas, permitindo que os apóstolos se dediquem à oração e ao ensino.",
            "Estêvão, cheio de graça e poder, realiza grandes prodígios e debate-se com oponentes.",
            "A hostilidade dos líderes de Jerusalém começa a se voltar diretamente contra ele.",
        ],
        "p": """
        <p>Como a igreja se multiplica, surge uma queixa: as viúvas de língua grega eram negligenciadas na distribuição diária. Os apóstolos convocam a comunidade e pedem que escolham sete homens \"de boa reputação, cheios do Espírito e de sabedoria\" (<span class="verse-link" data-reference="Atos+6:3">Atos 6:3</span>) para supervisionar esse serviço, a fim de se dedicarem \"à oração e ao ministério da palavra\".</p>
        <p>Entre os sete está Estêvão, descrito como \"cheio de graça e poder, realizando grandes prodígios e sinais entre o povo\" (<span class="verse-link" data-reference="Atos+6:8">Atos 6:8</span>). Ele debate-se com membros de sinagogas de língua grega, e estes, incapazes de resistir à sua sabedoria, subornam homens para acusá-lo de blasfêmia contra Moisés e contra Deus.</p>
        <p>Estêvão é levado perante o Sinédrio. Ali, Lucas prepara o terreno para o clímax do conflito entre os dois templos: a prisão e o discurso que se seguem mostrarão como os líderes de Israel sempre rejeitaram os mensageiros que Deus lhes enviou.</p>
        """,
        "d": None,
        "r": "A solução para a queixa das viúvas foi confiar responsabilidade a outros, não centralizar tudo nos apóstolos. Onde você precisa delegar ou ser delegado na vida da igreja?",
    },
    "7": {
        "t": "O Discurso de Estêvão",
        "k": [
            "Estêvão recapitula a história de Israel mostrando um padrão repetido: os antepassados sempre rejeitaram os escolhidos por Deus.",
            "Ele denuncia os líderes por resistirem ao Espírito Santo e matarem o Justo, o Messias.",
            "Estêvão é apedrejado, tornando-se o primeiro mártir, e sua morte dispara a primeira grande perseguição.",
        ],
        "p": """
        <p>Estêvão pronuncia um longo discurso recapitulando a história de Israel — de Abraão a José, de Moisés ao templo de Salomão — para mostrar um padrão: os antepassados \"sempre resistiram ao Espírito Santo\" (<span class="verse-link" data-reference="Atos+7:51">Atos 7:51</span>) e perseguiram os profetas, e agora, diz ele, traíram e mataram o Justo, o Messias prometido.</p>
        <p>Ele conclui afirmando que o Altíssimo não habita em casas feitas por mãos: \"O Céu é o meu trono, e a terra é o estrado dos meus pés. Que casa vocês me edificarão?\" (<span class="verse-link" data-reference="Atos+7:49">Atos 7:49</span>). Os líderes ficam furiosos, rangem os dentes e o arrastam para fora da cidade, apedrejando-o. Estêvão, vendo o céu aberto, clama: \"Senhor Jesus, recebe o meu espírito\" (<span class="verse-link" data-reference="Atos+7:59">Atos 7:59</span>).</p>
        <p>Assim morre Estêvão, o primeiro mártir, enquanto um jovem chamado Saulo guarda as capas dos apedrejadores. Sua morte desencadeia uma onda de perseguição contra os seguidores de Jesus, expulsando a maioria deles de Jerusalém. A crise, porém, tem um efeito paradoxal: conforme Jesus havia planejado (<span class="verse-link" data-reference="Atos+1:8">Atos 1:8</span>), o povo é agora enviado para Judeia e Samaria.</p>
        """,
        "d": None,
        "r": "Estêvão perdoou seus executores antes de morrer. O que custa, na prática, abençoar aqueles que nos perseguem?",
    },
    "8": {
        "t": "Filipe e a Samaria",
        "k": [
            "A perseguição após a morte de Estêvão espalha os discípulos, e a mensagem chega à Samaria, terra dos inimigos de Israel.",
            "Filipe anuncia o Cristo numa cidade samaritana, e muitos creem e são batizados.",
            "Pedro e João descem e oram para que os samaritanos recebam o Espírito — sinal de que o povo de Deus agora inclui os antes excluídos.",
        ],
        "p": """
        <p>A seção seguinte (caps. 8-12) mostra como a comunidade de Jesus se torna um movimento internacional. A primeira história é sobre a missão de Filipe à Samaria, a terra dos inimigos odiados de Israel. Muitos ali chegam a conhecer e seguir a Jesus (<span class="verse-link" data-reference="Atos+8">Atos 8</span>).</p>
        <p>Filipe desce a uma cidade samaritana e \"anunciava o Cristo\" (<span class="verse-link" data-reference="Atos+8:5">Atos 8:5</span>); há grande alegria, expulsão de espíritos impuros e curas. Quando os apóstolos em Jerusalém ouvem que a Samaria recebeu a palavra de Deus, enviam Pedro e João, que oram para que os samaritanos recebam o Espírito Santo — algo que ainda não havia acontecido. O Espírito desce sobre eles, sinal de que a família de Deus agora atravessa antigas divisões étnicas.</p>
        <p>Mais tarde, um anjo dirige Filipe para o sul, onde ele encontra um oficial etíope lendo Isaías. Filipe explica que as Escrituras falam de Jesus, e o homem cre e é batizado. Assim, a boa-nova começa a romper fronteiras muito além de Israel — preparando o caminho para o que virá nos capítulos seguintes.</p>
        """,
        "d": "three_bridges",
        "r": "O Espírito desceu sobre samaritanos antes mesmo de Pedro e João chegarem. Deus muitas vezes já está agindo onde hesitamos em ir. Onde você subestima a quem Deus pode incluir?",
    },
    "9": {
        "t": "A Conversão de Saulo",
        "k": [
            "Saulo de Tarso, o maior perseguidor da igreja, encontra pessoalmente o Jesus ressurreto no caminho de Damasco.",
            "Cegado e transformado, ele se torna um defensor apaixonado de Jesus, escandalizando seus antigos aliados.",
            "A igreja, a princípio receosa, acaba reconhecendo sua conversão como obra de Deus.",
        ],
        "p": """
        <p>A seguir vem a conversão de Saulo de Tarso, mais conhecido mais tarde como Paulo (<span class="verse-link" data-reference="Atos+9">Atos 9</span>). Ele era o inimigo jurado e até perseguidor dos seguidores de Jesus, até encontrar pessoalmente o Jesus ressurreto como o Rei. Aqui em Atos 9, Lucas relata a cena desse encontro no caminho de Damasco: uma luz do céu, e a voz de Jesus perguntando por que o perseguia.</p>
        <p>Saulo fica cego por três dias. O discípulo Ananias, instruído por uma visão, vai até ele, impõe-lhe as mãos, e as \"escamas\" caem dos seus olhos. Saulo é batizado e, imediatamente, \"pregava nas sinagogas que Jesus é o Filho de Deus\" (<span class="verse-link" data-reference="Atos+9:20">Atos 9:20</span>), deixando todos atônitos por sua reversão.</p>
        <p>Os judeus conspiram para matá-lo; os discípulos o descem numa cesta por uma abertura na muralha de Damasco. Em Jerusalém, os seguidores de Jesus inicialmente temem aproximar-se dele, até que Barnabé os convence de sua genuína conversão. Paulo passa a pregar com ousadia, e os irmãos o levam a Cesaréia e a Tarso para protegê-lo.</p>
        """,
        "d": None,
        "r": "O maior perseguidor tornou-se o maior missionário. Que \"inimigo\" da fé, em sua própria vida, Deus poderia estar chamando para si?",
    },
    "10": {
        "t": "Pedro e Cornélio",
        "k": [
            "Pedro recebe uma visão em que Deus declara puros os animais antes considerados impuros — e, com eles, os não-judeus.",
            "Ele é levado pelo Espírito à casa de Cornélio, um centurião romano, e o Espírito desce sobre todos os presentes.",
            "A inclusão dos gentios no povo de Deus não é decisão humana, mas iniciativa do próprio Espírito.",
        ],
        "p": """
        <p>Vemos a conversão de Pedro (caps. 9-11), que tem uma visão em sonho na qual aprende que Deus não considera os não-judeus ritualmente impuros nem indignos de se unirem à família de Jesus. Pedro é levado pelo Espírito à casa de um soldado romano, Cornélio, cheia de não-judeus, e todos eles respondem às boas-novas sobre Jesus (<span class="verse-link" data-reference="Atos+10">Atos 10</span>).</p>
        <p>Enquanto Pedro ainda fala, \"o Espírito Santo desceu sobre todos os que ouviam a mensagem\" (<span class="verse-link" data-reference="Atos+10:44">Atos 10:44</span>) — exatamente com a mesma potência com que havia descido sobre os discípulos judeus no capítulo 2. Os circuncisos que vieram com Pedro ficam astonitos, pois \"também aos gentios Deus concedeu o arrependimento para a vida\" (<span class="verse-link" data-reference="Atos+11:18">Atos 11:18</span>). Pedro ordena então que sejam batizados em nome de Jesus Cristo.</p>
        <p>Essa história é o ponto de virada do livro: o Evangelho rompe a barreira étnica. O que era prometido a Israel agora se estende às nações. A igreja em Jerusalém, ouvindo o relato, glorifica a Deus — embora o pleno alcance disso ainda gere debates, como veremos no capítulo 15.</p>
        """,
        "d": None,
        "r": "Pedro precisou de uma visão repetida três vezes para soltar preconceitos religiosos. Que barreiras internas Deus precisa quebrar em você para amar quem está \"do outro lado\"?",
    },
    "11": {
        "t": "A Igreja em Antioquia",
        "k": [
            "A dispersão após a perseguição leva a igreja a Antioquia, onde seguidores de Jesus são primeiro chamados de \"cristãos\".",
            "Barnabé e Paulo lideram ali uma comunidade multiétnica que se torna a primeira grande igreja internacional.",
            "É de Antioquia que os primeiros missionários internacionais são enviados.",
        ],
        "p": """
        <p>Lucas conta que Barnabé, um líder judeu da igreja de Jerusalém, foi junto com Paulo ajudar a liderar essa comunidade. Durante o tempo ali, ela se tornou a primeira grande igreja multiétnica da história, bem como o local onde os seguidores de Jesus foram chamados de \"cristãos\" pela primeira vez (<span class="verse-link" data-reference="Atos+11:26">Atos 11:26</span>).</p>
        <p>A igreja em Antioquia nasce quando refugiados da perseguição de Jerusalém levam a mensagem aos gregos da cidade, e \"grande número de pessoas creu e se voltou para o Senhor\" (<span class="verse-link" data-reference="Atos+11:21">Atos 11:21</span>). Barnabé é enviado de Jerusalém para confirmar a obra; vendo a graça de Deus, ele se alegra e encoraja a todos. Então vai a Tarso buscar Saulo, e por um ano inteiro ensinam naquela igreja.</p>
        <p>Dessa igreja, os primeiros missionários internacionais foram enviados, e a comissão de Jesus se tornou realidade. Ela se torna a igreja \"bandeira\" de onde partirão as jornadas de Paulo relatadas nos capítulos seguintes.</p>
        """,
        "d": None,
        "r": "O nome \"cristãos\" nasceu como identificação de uma comunidade onde judeus e gentios se sentavam juntos. Sua igreja hoje reflete essa mesma quebra de barreiras?",
    },
    "12": {
        "t": "Herodes e Pedro",
        "k": [
            "O rei Herodes Agripa persegue a igreja, executando Tiago e prendendo Pedro.",
            "A igreja ora, e um anjo liberta Pedro da prisão na própria noite anterior ao seu julgamento.",
            "Herodes morre, e \"a palavra do Senhor crescia e se multiplicava\" apesar da oposição.",
        ],
        "p": """
        <p>No capítulo 12, o rei Herodes Agripa estende a mão contra alguns da igreja para maltratá-los. Ele manda executar Tiago, irmão de João, à espada, e vendo que isso agradava aos judeus, prende também a Pedro, pretendendo submetê-lo a julgamento público após a festa da Páscoa (<span class="verse-link" data-reference="Atos+12">Atos 12</span>).</p>
        <p>Pedro é mantido por quatro escoltas de soldados, mas \"a igreja fazia sem cessar oração a Deus por ele\" (<span class="verse-link" data-reference="Atos+12:5">Atos 12:5</span>). Na noite anterior ao julgamento, um anjo do Senhor aparece, e as correntes caem. Pedro caminha pela cidade até a casa de Maria, onde a comunidade ora; eles à princípio não acreditam que ele esteja à porta. Herodes, não o encontrando, manda executar os guardas.</p>
        <p>O capítulo conclui com a morte de Herodes, ferido pelo anjo do Senhor por não ter dado glória a Deus, e a nota de que \"a palavra do Senhor crescia e se multiplicava\" (<span class="verse-link" data-reference="Atos+12:24">Atos 12:24</span>). A oposição dos poderes não detém a expansão do Reino.</p>
        """,
        "d": None,
        "r": "A igreja \"orava sem cessar\" enquanto Pedro estava preso — e Deus agiu. Você reage à ameaça orando com persistência ou com ansiedade?",
    },
    "13": {
        "t": "A Primeira Viagem Missionária",
        "k": [
            "O Espírito Santo separa Barnabé e Paulo em Antioquia para a primeira viagem missionária.",
            "Em Chipre e na Ásia Menor, Paulo anuncia Jesus primeiro às sinagogas e depois aos gentios.",
            "A rejeição judaica em alguns lugares leva Paulo a voltar-se explicitamente às nações.",
        ],
        "p": """
        <p>A igreja em Antioquia tornou-se a igreja \"bandeira\" dos primeiros missionários internacionais de Cristo. Barnabé e Paulo estavam servindo ali quando foram movidos pelo Espírito a partir, abrindo a segunda seção principal do livro de Atos (caps. 13-20). Paulo e vários cooperadores viajam pelo império romano para anunciar as boas-novas de que Jesus é o Rei (<span class="verse-link" data-reference="Atos+13-20">Atos 13-20</span>).</p>
        <p>A primeira jornada começa no interior da Ásia Menor (na Turquia moderna) e termina com uma importante reunião dos apóstolos de volta em Jerusalém (cap. 15). Em Chipre, Paulo confronta o falso profeta Bar-Jesus e proclama a Palavra. Em Antioquia da Pisídia, ele discursa na sinagoga mostrando que Jesus é o descendente prometido de Davi, mas diante da rejeição de muitos judeus, declara: \"era necessário anunciar-vos primeiro a palavra de Deus; mas, pois que a rejeitais... eis que nos volvemos para os gentios\" (<span class="verse-link" data-reference="Atos+13:46">Atos 13:46</span>).</p>
        <p>Em cada nova cidade, Paulo primeiro visita a sinagoga judaica para compartilhar como Jesus é o Rei ressurreto que agora forma um novo povo multiétnico de Deus. Muitos judeus reconhecem Jesus como seu Messias; outros, porém, se opõem a Paulo e às vezes o expulsam da cidade como um rebelde perigoso que se opõe à Torá e à tradição judaica.</p>
        """,
        "d": "journey1",
        "r": "Paulo sempre foi primeiro às sinagogas. Qual é o seu \"primeiro lugar\" de testemunho, e você tem evitado começar por ele?",
    },
    "14": {
        "t": "Icônio, Listra e Derbe",
        "k": [
            "Paulo e Barnabé realizam sinais em Icônio, mas a cidade se divide e eles fogem.",
            "Em Listra, Paulo cura um coxo e é tomado por um deus; logo após, é apedrejado e dado por morto.",
            "Eles retornam pelas cidades, consolidando discípulos e designando líderes antes de voltar a Antioquia.",
        ],
        "p": """
        <p>Em Icônio, Paulo e Barnabé entram na sinagoga e falam de modo que \"grande número de judeus e de gregos creu\" (<span class="verse-link" data-reference="Atos+14:1">Atos 14:1</span>). A cidade, porém, se divide entre os que apoiam os apóstolos e os que os resistem. Ameaçados de violência, eles fogem para Listra e Derbe.</p>
        <p>Em Listra, Paulo cura um homem coxo de nascença. A multidão, impressionada, chama Barnabé de Zeus e Paulo de Hermes, querendo sacrificar-lhes. Com dificuldade os apóstolos impedem o culto, declarando-se meros homens. Logo depois, porém, judeus vindos de Antioquia e Icônio convencem a multidão, que apedreja Paulo e o arrasta para fora da cidade, presumindo-o morto (<span class="verse-link" data-reference="Atos+14:19">Atos 14:19</span>).</p>
        <p>Mas os discípulos o cercam, e ele se levanta e entra na cidade. No dia seguinte, parte com Barnabé para Derbe, onde anuncia o Evangelho e faz muitos discípulos. Então retornam por Icônio, Listra e Antioquia da Pisídia, encorajando e consolidando os discípulos, e designando anciãos em cada igreja, antes de voltar a Antioquia da Síria, relatando tudo o que Deus realizara.</p>
        """,
        "d": "journey1",
        "r": "A mesma multidão que quis sacrificar a Paulo o apedrejou dias depois. A popularidade humana é instável — em que você tem ancorado sua identidade?",
    },
}
