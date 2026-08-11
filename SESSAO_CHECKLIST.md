# Checklist de Sessão Completa (igual ao PDF teacher-notes)

Uma sessão `modulo-N/sessao-N.html` está **completa** quando satisfaz todos os
critérios abaixo. Validação automática em `check_session_coverage.py`.

## Critérios

1. **Header / estrutura abraao**
   - `<title>` correto (nome da sessão, não vazado do template)
   - botão `Voltar` → `index.html` do curso
   - botão `Imprimir` (`window.print()`)
   - toggle `PT` / `EN` funcional (`setLang`, `localStorage` `sN-lang`)
   - `#reading-progress` + `verse-modal.js` carregado
   - `Class Notes: <Curso>` no `page-footer`

2. **Texto bilíngue (EN + PT)**
   - pelo menos um `lang-en` e um `lang-pt` por bloco de conteúdo
   - o EN reproduz o texto do PDF teacher-notes (tradução literal do instrutor
     onde aplicável; abraao mantém o EN fonte + PT traduzido)

3. **Todo o texto do PDF presente**
   - cada frase do PDF teacher-notes da sessão aparece no HTML (PT ou EN)
   - nada de "Class Notes: ... / N of M / Session N:" como lixo de cabeçalho
   - marcadores literários (chiasm, tabelas, "Key Takeaways") preservados

4. **Todas as imagens do PDF da sessão**
   - para cada página da sessão no PDF que contém imagem, o HTML tem um
     `<img>` correspondente (padrão `img/sessao-N/pK-vector.png`)
   - contagem de `<img>` no HTML == contagem de imagens nas páginas do PDF

5. **Citações no estilo certo**
   - referências bibliográficas no formato `Autor (AAAA). Título. Editora.`
     (ex: `Wright, N. T. (2004). Matthew for Everyone. Westminster John Knox Press.`)
   - não quebradas ou sem publisher e no estilo igual ao pdf

## Status esperado

- **abraao módulos 1-2** (S2-S5) e **abraao S6-30**: golden de texto (critérios 1-3 OK).
- Sessões **PT-only** (rise-of-the-messiah, noah-to-abraham): falham em critério 2
  (sem EN do PDF) até serem bilinguizadas.
- Sessões com `<img>` vinda de pdf-image (joseph S15/S16, jonah): falham em 3-4
  (texto/imagens ausentes) até regenerar do PDF vetorial.

## Teto do check

-  valida PT contra EN sem motor de tradução (critério 2 apenas confirma
  presença de ambos os spans, não fidelidade da tradução).
- Contagem de imagens usa `pdfimages -list` (requer poppler).
