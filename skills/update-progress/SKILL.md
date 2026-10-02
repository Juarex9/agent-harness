---
name: update-progress
description: Mantiene la memoria de la tarea en progress/. Úsalo al planificar, al avanzar y al cerrar cada tarea.
---

# update-progress

`progress/` es la memoria de la tarea de este worktree. Formato completo en `docs/progress-format.md` (repo del harness).

## Pasos

1. Al **empezar**: escribí `progress/current.md` (tarea, spec o N/A trivial con motivo, criterios, plan).
2. Al **avanzar**: actualizá estado, decisiones y bloqueos. Lo importante va al archivo, no queda en tu contexto.
3. Al **cerrar un hito**: copiá un snapshot a `progress/history/YYYY-MM-DD-<tema>.md` y dejá `current.md` reflejando lo último.
4. Al **terminar**: resumen del cambio + cómo verificarlo + veredicto del revisor.

Cada worktree tiene su propia copia: no ves lo de otros agentes hasta el merge. El estado global vive en issues (GitHub/Linear).
