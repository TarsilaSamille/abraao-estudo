#!/usr/bin/env python3
# Translate English sub-headings left untranslated inside the PT session files.
# Maps exact English heading line -> PT. "Reflection Question" intentionally kept EN (site convention).
import os, glob

# EN heading (exact line) -> PT
HEAD = {
  "New Testament Views of Heaven and Earth": "Visões do Novo Testamento sobre Céus e Terra",
  "Heaven and Earth United in Jesus": "Céus e Terra Unidos em Jesus",
  "Reflection on Our Own Cosmology Versus Biblical Cosmology": "Reflexão Sobre Nossa Própria Cosmologia Versus a Cosmologia Bíblica",
  "The Limitations of Human Language About God": "As Limitações da Linguagem Humana Sobre Deus",
  "Reading the Bible as an Ancient Text": "Ler a Bíblia como um Texto Antigo",
  "Approaching Scripture with Humility": "Aproximar-se das Escrituras com Humildade",
  "The Creation of Light": "A Criação da Luz",
  "Day One Establishes the Pattern": "O Dia Um Estabelece o Padrão",
  "Comparing Cosmologies": "Comparando Cosmologias",
  "The Egyptian View": "A Visão Egípcia",
  "The Enuma Elish": "O Enuma Elish",
  "The Key Difference": "A Diferença Principal",
  "Function Over Material Origin": "Função Acima da Origem Material",
  "Creation as Naming and Ordering": "Criação como Nomear e Ordenar",
  "Creation as Sustaining Work": "Criação como Obra de Sustentação",
  "From Chaos to Completion": "Do Caos à Conclusão",
  "Paying Attention to Repetition": "Prestar Atenção à Repetição",
  "The Story of the Seven Days": "A História dos Sete Dias",
  "Rulers Above and Below": "Governantes de Cima e de Baixo",
  "The Waters Above": "As Águas de Cima",
  "Water as Both Life and Death": "A Água como Vida e Morte",
  "The Tannin in the Bible": "O Tannin na Bíblia",
  "The Dry Land": "A Terra Seca",
  "The Land as a Disc": "A Terra como um Disco",
  "Dry Land as Salvation": "A Terra Seca como Salvação",
  "This session has no other notes": "Esta sessão não tem outras anotações",
  "The Biblical Earth and Its Foundations in a Modern Worldview": "A Terra Bíblica e Seus Alicerces numa Cosmovisão Moderna",
  "Rivers as a Symbol of Life": "Rios como Símbolo de Vida",
  "Two Realities in Tension": "Duas Realidades em Tensão",
  "Heaven Coming to Earth": "O Céu Descendo à Terra",
  "Heaven and Earth Meeting in the Temple": "Céus e Terra se Encontrando no Templo",
  "From Eden to Jesus": "Do Éden a Jesus",
  "Reflections on Heaven and Earth": "Reflexões sobre Céus e Terra",
  "Heaven Coming to Earth in Jesus": "O Céu Descendo à Terra em Jesus",
  "The Host of Heaven": "A Hoste dos Céus",
  "Heavenly Beings as Rulers": "Seres Celestiais como Governantes",
  "The Divine Council": "O Concílio Divino",
  "Ruling as Partners with God": "Governar como Parceiros de Deus",
  "Priestly and Royal Functions": "Funções Sacerdotais e Reais",
  "No Idols Because We Are the Image": "Sem Ídolos Porque Nós Somos a Imagem",
  "The Image of God in the Storyline of the Hebrew Bible": "A Imagem de Deus na Trama da Bíblia Hebraica",
  "The Coming Seed and Jesus": "A Semente Vindoura e Jesus",
  "Two Words for Rest": "Duas Palavras para Descanso",
  "The Unending Seventh Day": "O Sétimo Dia Sem Fim",
  "Jesus and the Jubilee": "Jesus e o Jubileu",
  "The Image of God = God's Idol Statue in His Cosmic Temple": "A Imagem de Deus = a Estátua-Ídolo de Deus em Seu Templo Cósmico",
  "A Modern View of the Cosmos": "Uma Visão Moderna do Cosmos",
  "A Modern View of the Words \"Heaven\" and \"Earth\"": "Uma Visão Moderna das Palavras “Céu” e “Terra”",
  "The Biblical View of \"Heavens\" and \"Earth\"": "A Visão Bíblica de “Céus” e “Terra”",
  "A Helpful Grid": "Uma Grade Útil",
  "Scripture, Communication, Language, and Culture": "Escritura, Comunicação, Linguagem e Cultura",
  "A Glimmer of Hope": "Um Vislumbre de Esperança",
  "A Literary Device": "Um Recurso Literário",
  "A Correspondence Between Days": "Uma Correspondência Entre os Dias",
  "Created, Not Defeated": "Criado, Não Derrotado",
  "The Many Meanings of \"Heaven\" in the Bible": "Os Muitos Sentidos de “Céu” na Bíblia",
  "A Long Tradition of Translation": "Uma Longa Tradição de Tradução",
  "Image, Unity, and Diversity": "Imagem, Unidade e Diversidade",
  "The Meaning of \"Seven\"": "O Significado de “Sete”",
}

# EN session title (first line) -> PT title
TITLE = {
  "Session 1: Our Place in the Universe": "Sessão 1: Nosso Lugar no Universo",
  "Session 2: The Words “Heavens” and “Earth” in the": "Sessão 2: As Palavras “Céus” e “Terra” na Bíblia Hebraica",
  "Session 3: Heaven and Earth Come Together in Jesus": "Sessão 3: Céus e Terra se Unem em Jesus",
  "Session 4: Reflections on the New Testament’s View": "Sessão 4: Reflexões sobre a Visão do Novo Testamento",
  "Session 5: Scripture, Communication, Language, and": "Sessão 5: Escritura, Comunicação, Linguagem e Cultura",
  "Session 6: Genesis 1 Is an Ancient Israelite": "Sessão 6: Gênesis 1 é uma Cosmologia Israelita Antiga",
  "Session 7: The Purpose of Light on Day One": "Sessão 7: O Propósito da Luz no Dia Um",
  "Session 8: Ancient Egyptian Cosmology": "Sessão 8: Cosmologia Egípcia Antiga",
  "Session 9: Ancient Babylonian Cosmology": "Sessão 9: Cosmologia Babilônica Antiga",
  "Session 10: The Beginning and Nothingness": "Sessão 10: O Princípio e o Nada",
  "Session 11: Genesis 1 Imagery in Jeremiah 4": "Sessão 11: Imagética de Gênesis 1 em Jeremias 4",
  "Session 12: Genesis 1 Imagery in Psalm 104": "Sessão 12: Imagética de Gênesis 1 no Salmo 104",
  "Session 13: The Structure and Message of Genesis 1": "Sessão 13: A Estrutura e a Mensagem de Gênesis 1",
  "Session 14: Repeated Words in Genesis 1": "Sessão 14: Palavras Repetidas em Gênesis 1",
  "Session 15: Relationships Between Days": "Sessão 15: Relações Entre os Dias",
  "Session 16: The Waters Above and Below": "Sessão 16: As Águas de Cima e de Baixo",
  "Session 17: The Dragon in the Waters": "Sessão 17: O Dragão nas Águas",
  "Session 18: The Dry Land": "Sessão 18: A Terra Seca",
  "Session 19: Reflections on Where All Creation Is": "Sessão 19: Reflexões sobre Para Onde Toda a Criação Caminha",
  "Session 20: Rivers of Life": "Sessão 20: Rios de Vida",
  "Session 21: Jesus and Living Water": "Sessão 21: Jesus e a Água Viva",
  "Session 22: Ancient Cosmology in Psalm 36": "Sessão 22: Cosmologia Antiga no Salmo 36",
  "Session 23: The Heavens": "Sessão 23: Os Céus",
  "Session 24: Heaven and Earth United in the Temple": "Sessão 24: Céus e Terra Unidos no Templo",
  "Session 25: Reflections on Heaven Coming to Earth": "Sessão 25: Reflexões sobre o Céu Descendo à Terra",
  "Session 26: The Rulers Above": "Sessão 26: Os Governantes de Cima",
  "Session 27: The Rulers Below": "Sessão 27: Os Governantes de Baixo",
  "Session 28: Humans as the Image, or Idol, of God": "Sessão 28: Humanos como a Imagem, ou Ídolo, de Deus",
  "Session 29: The Image of God in the Storyline of the": "Sessão 29: A Imagem de Deus na Trama da Bíblia Hebraica",
  "Session 30: God Rests on the Seventh Day": "Sessão 30: Deus Descansa no Sétimo Dia",
  "Session 31: The Sabbath With No End": "Sessão 31: O Sábado Sem Fim",
}

def patch(path):
    with open(path) as f:
        lines = f.read().split('\n')
    changed = 0
    for i, line in enumerate(lines):
        if line in HEAD:
            lines[i] = HEAD[line]
            changed += 1
        elif line in TITLE:
            lines[i] = TITLE[line]
            changed += 1
    with open(path, 'w') as f:
        f.write('\n'.join(lines))
    return changed

total = 0
for f in sorted(glob.glob('/tmp/he_session_*_pt.txt')):
    # only patch heaven-and-earth files (he_session_N_pt.txt, not other prefixes)
    import re
    if re.search(r'/he_session_\d+_pt\.txt$', f):
        total += patch(f)
print(f"Patched {total} heading lines across heaven-and-earth PT files")
