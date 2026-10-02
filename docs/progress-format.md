# Formato de progress/

`progress/` es la memoria **de la tarea de este worktree**. Cada worktree tiene su propia copia: dos agentes en paralelo no se ven hasta el merge. El estado global (qué está hecho y qué falta) vive en issues de GitHub o Linear.

## progress/current.md

Refleja siempre lo último. Esqueleto:

```md
# Tarea: <título corto>

- Estado: en-curso | bloqueado | listo-para-revisar | terminado
- Spec: specs/<feature>.md (Estado: aprobada) | N/A — trivial: <motivo en 1 línea>
- Issue: #n | N/A — <motivo en 1 línea>
- Criterios de aceptación:
  - [ ] <criterio verificable>
- Plan:
  1. <paso>
- Decisiones:
  - <decisión + motivo corto>
- Bloqueos:
  - <qué falta y de quién depende>
- Último resumen: <qué se hizo, qué falta, cómo verificarlo>
```

## progress/history/

Un archivo por hito cerrado: `history/YYYY-MM-DD-<tema>.md`. Es un snapshot de `current.md` al cerrar el hito (se copia, no se mueve). Sirve para abrir sesiones nuevas sin perder información y para auditar decisiones.

## Reglas

- Todo lo importante va al archivo, no queda en el contexto del agente.
- La tarea apunta a su spec (o justifica por qué es trivial; el revisor lo valida).
- La tarea apunta a su issue de GitHub (`Issue: #n`) o justifica `N/A`. Un hallazgo fuera de alcance se abre con la skill `crear-issue`, no queda solo como frase.
- El veredicto del revisor (aprobado/rechazado con motivos) queda en `current.md`.

## Continuidad (merge, no overwrite)

`current.md` lo tocan varios roles en momentos distintos. Quien actualiza **fusiona** con lo existente: lee el archivo primero, suma su parte y conserva decisiones, bloqueos y el veredicto del revisor. Nunca se reescribe desde cero. Si dos agentes trabajan en paralelo (dos worktrees), cada uno tiene su propia copia y se reconcilian en el merge de git, igual que el código.

## Snapshot en engram (por hito)

Al cerrar un hito, además de copiar a `history/`, guardar `mem_save(topic_key: "progress/<tema>", capture_prompt: false)` con el resumen. Sirve para recuperar el estado tras una compactación sin leer todo el historial.
