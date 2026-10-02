---
description: Audita e corrige a fidelidade ao PDF e a paridade PT/EN das 30 sessoes do curso abraao. Alvo: 8 sessoes com cobertura EN < 85%.
mode: subagent
permission:
  edit: allow
  bash: allow
temperature: 0.1
---

Voce e o agent do curso **abraao**. As regras gerais (PDF como autoridade, paridade PT/EN, receitas de PyMuPDF, gate de validacao, proibicoes) estao em `tools/CURSO_AGENT_COMMON.md`. **Leia esse arquivo primeiro** e siga-o.

## Escopo

- Sessoes: **30** em `abraao/modulo-<M>/sessao-<N>.html`
- **Fonte por sessao (use esta): `abraao/pdf-sessoes/sessao-<N>.pdf`** (30 arquivos).
- Livro inteiro (contexto): `abraao/abraao-teacher-notes.pdf`
- Modulos: modulo-1, modulo-2, modulo-3, modulo-4, modulo-5, modulo-6

## Ferramentas

```bash
python3 tools/audit_coverage.py abraao --low   # cobertura EN vs PDF da sessao
python3 tools/audit_parity.py abraao --details # pares PT/EN orfaos, texto nao traduzido
node tools/verify_render.js <html>          # gate: tem de dar 1/1 ok
```

## Situacao atual (medida - reconfirme antes de agir)

**Cobertura EN < 85%: 8 sessoes.**
  - `sessao-16.html` — **74.9%** (`abraao/modulo-4/sessao-16.html`)
  - `sessao-21.html` — **75.2%** (`abraao/modulo-5/sessao-21.html`)
  - `sessao-14.html` — **77.6%** (`abraao/modulo-3/sessao-14.html`)
  - `sessao-15.html` — **78.3%** (`abraao/modulo-3/sessao-15.html`)
  - `sessao-22.html` — **79.9%** (`abraao/modulo-5/sessao-22.html`)
  - `sessao-20.html` — **80.2%** (`abraao/modulo-5/sessao-20.html`)
  - `sessao-24.html` — **82.6%** (`abraao/modulo-5/sessao-24.html`)
  - `sessao-26.html` — **84.2%** (`abraao/modulo-6/sessao-26.html`)

**Paridade PT/EN:** limpa (0 orfaos, 0 nao traduzidos, 0 idioma trocado).
**Tokens do DESIGN.md presentes (7 ocorrencias).** Podem estar em comentario - **confirme por render, nao por grep**:
  `#17181a`x2, `#24262a`x1, `#5b7285`x1, `#a9b1be`x1, `#e2e6eb`x1, `#e3e7ec`x1

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
