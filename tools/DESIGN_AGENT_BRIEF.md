# Briefing: conformidade DESIGN.md por sessão

Objetivo: o usuário reclamou que **cores e tamanhos** não estão idênticos ao design system.
Causa estrutural já corrigida em `abraao/css/session-base.css`. Sua tarefa: a camada por-sessão.

## Ferramentas (use, não reinvente)
| comando | função |
|---|---|
| `python3 tools/audit_design.py <curso>` | inventário de desvios por categoria |
| `python3 tools/design_fix.py <curso>` | dry-run do mapeamento determinístico |
| `python3 tools/design_fix.py --apply <curso>` | aplica o mapeamento |
| `node tools/verify_render.js <curso>/modulo-*/sessao-*.html` | overflow horizontal, erro JS, diagrama cortado |

Referência já corrigida: `abraao/modulo-2/sessao-4.html` (rode o audit: 0 desvios).

## Procedimento
1. Faça **backup** do diretório do curso antes de editar.
2. Dry-run do `design_fix.py`, leia as substituições propostas.
3. Aplique.
4. Re-audite e resolva manualmente o que sobrar em `color`/`type`/`radius`/`border`/`shadow`.
   **Conservador:** só troque quando o token do DESIGN.md for inequívoco. Na dúvida, deixe e reporte.
5. `verify_render.js` em **todas** as sessões do curso. Se quebrar, reverta a mudança causadora.
6. Valide que texto/traduções não mudaram (diff ignorando `class`/`style` contra o backup).

## Regras duras
- **NÃO** edite nenhum `.css` nem o `DESIGN.md`. Só o HTML do seu curso.
- **NÃO** altere texto, traduções ou spans `lang-pt`/`lang-en`. Só classes/CSS.
- `structure` (`verse-modal.js`, `reading-progress`, `max-w-4xl`, balanço PT/EN) é
  **fora de escopo**: apenas reporte.
- **NÃO** remova `text-sm` (0.875rem **é** o token `label`).
- **NÃO** mude `text-slate-600` (nav) nem `border-slate-300` (pills): documentados no DESIGN.
- **NUNCA** aplique sombra em repouso a card de conteúdo (Flat-By-Default).
  `shadow-sm` só é válido nos pills de nav.
- Variantes documentadas (âmbar `#f59e0b`/`#fffbeb` em ephesians e 1-corinthians;
  paleta estendida do abraao módulo 2–6) são **intencionais**. Não mexa.
- Não quebre `fitDiagrams()` em páginas com `diagram-viewport`/`diagram-canvas`.

## Armadilhas já encontradas (não repita)
1. **`grounded` → `grounded-[5px]`** e **`rounded leaves` → `rounded-[5px] leaves`**.
   Causa: as regras rodavam no documento inteiro. **Agora o `design_fix.py` só reescreve
   dentro de `class="..."`, `style="..."` e `<style>...</style>`** — prosa é intocável.
   Varredura em 442 sessões: 0 corrupção. Ainda assim, confira o texto contra o backup.
2. **Utilitários com prefixo responsivo** (`md:text-5xl`, `lg:text-3xl`) não são cobertos
   pelo audit nem pelo fix. Procure manualmente.
3. **Hex cru dentro de `<style>` ou em `style="..."` inline** não é detectado pelo audit
   (que só lê atributos `class`). Procure manualmente
   (`grep -o '#[0-9a-f]\{6\}'`).
4. **Regra anterior pode anular a seguinte** no desktop: `text-4xl → 2.6rem` mas
   `md:text-5xl` (48px) sobrepõe em ≥768px. Confira sempre o vizinho responsivo.
5. Quando o DESIGN tem duas leituras plausíveis, **não chute** — deixe e reporte.
6. **`.quote`/`.poem` é serif 1.05rem**, não o token `meta` 0.95rem. O DESIGN é explícito:
   "Newsreader... reserved for poems (`.poem`) and pull-quotes (`.quote`)". Já mapeado.
7. **`<img>` usa raio 12px**, não `r9`. O DESIGN diz "12px radii for tables/images".
   Já mapeado por um passe que enxerga a tag.
8. **`line-height` não é auditado** e é o desvio visual mais perceptível que resta.
   Tokens: body 1.78, serif/poem 1.85, bullets 1.75, h1 1.08, h2 1.2, sub 1.25.
   Corrija manualmente onde estiver errado — `h2` sem `line-height` herda o do body e
   fica visivelmente solto.
9. **Paleta categórica não documentada** — NÃO chute, apenas reporte. Alguns cursos têm
   um vocabulário de cor próprio, estruturalmente igual ao sistema `cx-*` (matiz + tint
   pareados) mas com hexes diferentes. `ezekiel` é o caso extremo: **45 hexes distintos**,
   ~15 pares, que não casam nem com a paleta `cx-*` base nem com a variante documentada
   do abraao. Normalizar isso é decisão do dono do design, não do agente. Deixe como está
   e detalhe o padrão no relatório (quais pares matiz/tint, em quantas sessões).
   Aplicado o mesmo aos achados de `#4f5669`/`#91362e`/`#fae4c4`… em `jacob` (`#be4967`),
   `atos-dos-apostolos` (paleta "Google Docs") e `1-corinthians` (`#1b1b1b`).
10. **Bullet corrompido**: se `content: "\x822"` aparecer, o builder emitiu `U+0082` + `"2"`
   em vez de `•`. Isso é bug de render real, vale corrigir.


## Relatório final obrigatório
1. Sessões alteradas + substituições por regra.
2. Achados visuais restantes e por que não mudou.
3. Achados de `structure` (só reporte).
4. Resultado do `verify_render.js` (ok/falhas).
5. Bugs encontrados no `design_fix.py`/`audit_design.py` e o que você sugere.
6. Qualquer texto que tenha sido alterado por engano (se houve).
