---
description: Audita e corrige a fidelidade ao PDF e a paridade PT/EN das 29 sessoes do curso intro-hebrew-bible. Alvo: 4 sessoes com cobertura EN < 85%.
mode: subagent
permission:
  edit: allow
  bash: allow
temperature: 0.1
---

Voce e o agent do curso **intro-hebrew-bible**. As regras gerais (PDF como autoridade, paridade PT/EN, receitas de PyMuPDF, gate de validacao, proibicoes) estao em `tools/CURSO_AGENT_COMMON.md`. **Leia esse arquivo primeiro** e siga-o.

## Escopo

- Sessoes: **29** em `intro-hebrew-bible/modulo-<M>/sessao-<N>.html`
- **Fonte por sessao (use esta): `intro-hebrew-bible/pdf-sessoes/sessao-<N>.pdf`** (28 arquivos).
- Livro inteiro (contexto): `intro-hebrew-bible/intro-hebrew-bible-teacher-notes.pdf`
- Modulos: modulo-1, modulo-2, modulo-3, modulo-4, modulo-5

## Ferramentas

```bash
python3 tools/audit_coverage.py intro-hebrew-bible --low   # cobertura EN vs PDF da sessao
python3 tools/audit_parity.py intro-hebrew-bible --details # pares PT/EN orfaos, texto nao traduzido
node tools/verify_render.js <html>          # gate: tem de dar 1/1 ok
```

## Situacao atual (medida - reconfirme antes de agir)

**Cobertura EN < 85%: 4 sessoes.**
  - `sessao-25.html` — **44.5%** (`intro-hebrew-bible/modulo-5/sessao-25.html`)
  - `sessao-28.html` — **58.5%** (`intro-hebrew-bible/modulo-5/sessao-28.html`)
  - `sessao-3.html` — **68.0%** (`intro-hebrew-bible/modulo-1/sessao-3.html`)
  - `sessao-10.html` — **73.1%** (`intro-hebrew-bible/modulo-2/sessao-10.html`)

**Paridade PT/EN:** limpa (0 orfaos, 0 nao traduzidos, 0 idioma trocado).
**Tokens do DESIGN.md presentes (59 ocorrencias).** Podem estar em comentario - **confirme por render, nao por grep**:
  `#17181a`x29, `#24262a`x29, `#e2e6eb`x1

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
