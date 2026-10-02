---
description: Audita e corrige a fidelidade ao PDF e a paridade PT/EN das 22 sessoes do curso messianic-torah. Alvo: 1 sessoes com cobertura EN < 85% e 2 defeitos de paridade PT/EN.
mode: subagent
permission:
  edit: allow
  bash: allow
temperature: 0.1
---

Voce e o agent do curso **messianic-torah**. As regras gerais (PDF como autoridade, paridade PT/EN, receitas de PyMuPDF, gate de validacao, proibicoes) estao em `tools/CURSO_AGENT_COMMON.md`. **Leia esse arquivo primeiro** e siga-o.

## Escopo

- Sessoes: **22** em `messianic-torah/modulo-<M>/sessao-<N>.html`
- **Fonte por sessao (use esta): `messianic-torah/pdf-sessoes/sessao-<N>.pdf`** (21 arquivos).
- Livro inteiro (contexto): `messianic-torah/messianic-torah-teacher-notes.pdf`
- Modulos: modulo-1, modulo-2, modulo-3, modulo-4

## Ferramentas

```bash
python3 tools/audit_coverage.py messianic-torah --low   # cobertura EN vs PDF da sessao
python3 tools/audit_parity.py messianic-torah --details # pares PT/EN orfaos, texto nao traduzido
node tools/verify_render.js <html>          # gate: tem de dar 1/1 ok
```

## Situacao atual (medida - reconfirme antes de agir)

**Cobertura EN < 85%: 1 sessoes.**
  - `sessao-22.html` — **31.4%** (`messianic-torah/modulo-4/sessao-22.html`)

**Paridade PT/EN: 2 defeito(s).** Por tipo: {'PT_NAO_TRADUZIDO': 2}

Por sessao:
```
  messianic-torah/modulo-3/sessao-14.html  {'PT_NAO_TRADUZIDO': 2}
```
**Tokens do DESIGN.md presentes (66 ocorrencias).** Podem estar em comentario - **confirme por render, nao por grep**:
  `#17181a`x22, `#24262a`x22, `#5b7285`x22

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
