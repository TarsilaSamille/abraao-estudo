---
description: Audita e corrige a fidelidade ao PDF e a paridade PT/EN das 28 sessoes do curso atos-dos-apostolos. Alvo: 27 defeitos de paridade PT/EN.
mode: subagent
permission:
  edit: allow
  bash: allow
temperature: 0.1
---

Voce e o agent do curso **atos-dos-apostolos**. As regras gerais (PDF como autoridade, paridade PT/EN, receitas de PyMuPDF, gate de validacao, proibicoes) estao em `tools/CURSO_AGENT_COMMON.md`. **Leia esse arquivo primeiro** e siga-o.

## Escopo

- Sessoes: **28** em `atos-dos-apostolos/modulo-<M>/sessao-<N>.html`
- **Sem `*teacher-notes.pdf` e sem `pdf-sessoes/`:** nao ha PDF de origem, entao a fidelidade ao PDF NAO pode ser verificada. Corrija so paridade PT/EN e tokens de cor, e declare isso no relatorio.
- Modulos: modulo-1, modulo-2, modulo-3, modulo-4, modulo-5

## Ferramentas

```bash
python3 tools/audit_coverage.py atos-dos-apostolos --low   # cobertura EN vs PDF da sessao
python3 tools/audit_parity.py atos-dos-apostolos --details # pares PT/EN orfaos, texto nao traduzido
node tools/verify_render.js <html>          # gate: tem de dar 1/1 ok
```

## Situacao atual (medida - reconfirme antes de agir)

**Cobertura EN:** nenhuma sessao abaixo de 85%.

**Paridade PT/EN: 27 defeito(s).** Por tipo: {'SEM_IDIOMA': 27}

Por sessao:
```
  atos-dos-apostolos/modulo-1/sessao-1.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-2/sessao-2.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-2/sessao-3.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-2/sessao-4.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-2/sessao-5.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-2/sessao-6.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-2/sessao-7.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-3/sessao-10.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-3/sessao-11.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-3/sessao-12.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-3/sessao-8.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-3/sessao-9.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-4/sessao-13.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-4/sessao-14.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-4/sessao-15.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-4/sessao-16.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-4/sessao-17.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-4/sessao-18.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-4/sessao-19.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-4/sessao-20.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-5/sessao-21.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-5/sessao-22.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-5/sessao-23.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-5/sessao-24.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-5/sessao-25.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-5/sessao-26.html  {'SEM_IDIOMA': 1}
  atos-dos-apostolos/modulo-5/sessao-28.html  {'SEM_IDIOMA': 1}
```
**Tokens do DESIGN.md presentes (56 ocorrencias).** Podem estar em comentario - **confirme por render, nao por grep**:
  `#17181a`x28, `#24262a`x28

## Nao e defeito (deixe como esta)

- Referencias biblicas (`Gênesis 11:27` vs `Genesis 11:27`).
- Marcadores do design literario (`a`, `b`, `a'`, `17`) e numeros de verso.
- Siglas de traducao (NASB, NIV, ESV, NRSV).
- Citacoes bibliograficas no formato do repo `Autor (AAAA). Titulo. Editora.` - sao **iguais de proposito** nos dois idiomas.
- Creditos de imagem (`Created by Tim Mackie for BibleProject Classroom...`).
- Transliteracoes de nomes proprios e termos hebraicos/gregos/aramaicos.

## Blindagem (obrigatorio)

- **Nao apague bloco nenhum.** 36 arquivos ja quebraram por `</div>`, `</span>` e `</figure>` orfaos quando um agent removeu um bloco.
- Rode `node tools/verify_render.js <html>` em **cada** sessao tocada: tem de dar `1/1 ok`. O gate detecta tag desbalanceada e conteudo colapsado.
- **Nao use `git add`** e nao comite. Deixe tudo no working tree.
- Backup antes: `cp <html> /tmp/<curso>-s<N>.bak.html`.

## Relatorio final

Por sessao tocada: (1) ja estava fiel? sim/nao, (2) diferencas de cor com hex dos dois lados, (3) traducoes feitas, (4) diagramas/estruturas corrigidos, (5) `verify_render` ok/falha. Depois um resumo do que **nao** mudou e por que.
