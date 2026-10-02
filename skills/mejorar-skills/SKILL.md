---
name: mejorar-skills
description: Junta retros y señales del proyecto en curso y propone ajustes a las skills en un PR draft del harness. No mergea ni afloja controles. Usala con "qué aprendimos" o "ajustá las skills con el uso".
---

# mejorar-skills

Propone, una persona decide. El PR es draft en el repo del harness y no se mergea. Una anécdota no alcanza.

## Reglas

1. Al menos dos casos, o uno grave (bug que llegó a revisión o producción, regla de negocio rota, datos o dinero en riesgo).
2. Nunca quitar ni aflojar: `check` en verde, `check-map` que sale `2`, `--confirmar` de `crear-issue` y de esta skill, spec aprobada, veredicto escrito del revisor, ni el "no mergea". Si un control frena seguido, va en preguntas, no en el diff.
3. Script antes que otra frase en Markdown.
4. Ningún `SKILL.md` pasa de 120 líneas.
5. Un cambio por patrón, con motivo y links.

Si no hay señales nuevas, decilo y terminá.

## 1. Señales

Parado en el proyecto (no en el harness):

```bash
python3 ~/.agents/skills/mejorar-skills/senales.py
```

En este repo, sin `install.sh`: `python3 skills/mejorar-skills/senales.py`. Solo lee. Si `gh` falla o el repo no es de GitHub, frená. No inventes Linear.

## 2. Borrador

```bash
python3 ~/.agents/skills/mejorar-skills/abrir_pr.py \
  --titulo "el ajuste" \
  --patrones "| patrón | casos | ajuste |" \
  --preguntas "(ninguna)" \
  --descartado "(ninguno)"
```

Mostrá el texto y esperá un sí. Sin `--confirmar` no toca git ni `gh`.

## 3. Publicar

Solo después del sí, en el checkout del harness, con el árbol limpio. El script crea `mejorar-skills/AAAA-MM-DD` desde `origin/main` si todavía no hay commits. Commiteá el ajuste en esa rama y repetí el comando con `--confirmar`. Si el árbol está sucio, un `SKILL.md` pasa de 120 líneas o falta un invariante, no hace push. El PR sale con `--draft` contra el harness. No lo mergees.

## 4. Retro al cerrar una revisión

**Skill:** la que se usó.
**Desvío:** dónde no se siguió, o "ninguno".
**Decisión no cubierta:** qué hubo que decidir que la skill no decía.
**Revisión:** qué encontró el revisor que la implementación no vio, o "nada".

```bash
python3 ~/.agents/skills/mejorar-skills/retro.py --cuerpo "<esa retro>"
```

Si el issue `Retros del flujo con agentes` no existe, eso imprime el borrador. Con el sí del usuario, repetí con `--confirmar` (lo crea y lo fija). Si ya existe, el comentario no pide otra confirmación.

Abierto el PR, comentá en ese issue el link y la línea `<!-- mejorar-skills: consolidado -->`.
