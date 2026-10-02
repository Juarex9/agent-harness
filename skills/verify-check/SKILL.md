---
name: verify-check
description: Corre el chequeo del proyecto y decide si la tarea puede darse por terminada. Úsalo siempre antes de cerrar una tarea.
---

# verify-check

Ninguna tarea está terminada porque lo digas vos, sino cuando los chequeos pasan.

## Pasos

1. Detectá el chequeo del proyecto: `npm run check` (Node/Next) o `make check` (Python).
2. Correlo completo, sin salteos ni filtros.
3. Si está en **verde**: la tarea puede pasar a revisión.
4. Si está en **rojo**: la tarea NO está terminada. Arreglá lo que falla, volvé a correrlo completo y recién ahí avisá.

Reportá siempre el comando corrido y su resultado (qué pasó: tests, lint, typecheck).
