---
description: Audita e corrige a fidelidade ao PDF e a paridade PT/EN das 32 sessoes do curso adam-to-noah. Alvo: 1 sessoes com cobertura EN < 85%.
mode: subagent
permission:
  edit: allow
  bash: allow
temperature: 0.1
---

Voce e o agent do curso **adam-to-noah**. As regras gerais (PDF como autoridade, paridade PT/EN, receitas de PyMuPDF, gate de validacao, proibicoes) estao em `tools/CURSO_AGENT_COMMON.md`. **Leia esse arquivo primeiro** e siga-o.

## Escopo

- Sessoes: **32** em `adam-to-noah/modulo-<M>/sessao-<N>.html`
- **Fonte por sessao (use esta): `adam-to-noah/pdf-sessoes/sessao-<N>.pdf`** (31 arquivos).
- Livro inteiro (contexto): `adam-to-noah/adam-to-noah-teacher-notes.pdf`
- Modulos: modulo-1, modulo-2, modulo-3, modulo-4, modulo-5, modulo-6

## Ferramentas

```bash
python3 tools/audit_coverage.py adam-to-noah --low   # cobertura EN vs PDF da sessao
python3 tools/audit_parity.py adam-to-noah --details # pares PT/EN orfaos, texto nao traduzido
node tools/verify_render.js <html>          # gate: tem de dar 1/1 ok
```

## Situacao atual (medida - reconfirme antes de agir)

**Cobertura EN < 85%: 1 sessoes.**
  - `sessao-31.html` — **9.2%** (`adam-to-noah/modulo-6/sessao-31.html`)

**Paridade PT/EN:** limpa (0 orfaos, 0 nao traduzidos, 0 idioma trocado).
**Tokens do DESIGN.md presentes (2 ocorrencias).** Podem estar em comentario - **confirme por render, nao por grep**:
  `#e3e7ec`x2

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
