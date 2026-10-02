# Flujo de trabajo (workflow)

Cómo se trabaja una tarea en cualquier proyecto del harness.

## Roles

- **Líder**: lee la tarea, planifica, delega, decide cuándo está lista. Vive uno por worktree.
- **Implementador**: escribe el código y los tests.
- **Revisor**: corre los chequeos, controla convenciones y spec, aprueba o rechaza por escrito.
- **Explorador** (opcional): investiga sin modificar nada.

Los prompts de cada rol están en `agents/`. Primero líder + implementador + revisor general; especialistas (Fase 6) solo cuando el área lo justifique.

## Paso a paso

1. **Leer**: `AGENTS.md` del proyecto, `progress/` del worktree, y la spec si la tarea la tiene.
2. **Entorno**: correr `init.sh`. Si falla, no se empieza: se arregla el entorno primero.
3. **Spec (solo no trivial)**: sin spec aprobada no se implementa (ver `docs/specs.md`). La tarea en `progress/` apunta a su spec.
4. **Implementar**: una tarea a la vez, con tests que prueben comportamiento real.
5. **Verificar**: correr `check` (skill `verify-check`). Si está en rojo, la tarea no está terminada.
6. **Revisar**: el revisor aprueba o rechaza por escrito en `progress/` (ver `agents/reviewer.md`).
7. **Cerrar**: actualizar `progress/` y la spec si el comportamiento cambió en el mismo cambio.

## Definición de terminado

- [ ] Criterios de aceptación cumplidos (los de la tarea o los de la spec).
- [ ] `check` en verde.
- [ ] Tests nuevos que prueban comportamiento real.
- [ ] Revisor aprobó por escrito en `progress/`.
- [ ] `progress/` actualizado con el resumen del cambio.
- [ ] Spec actualizada si algo cambió (mismo PR/cambio).

## Delegación (líder)

Pregunta guía: **¿esto infla mi contexto sin necesidad?** Si sí → delegar. Si no → inline.

| Acción | Inline (líder) | Delegar |
|---|---|---|
| Leer 1–3 archivos para decidir o verificar | Sí | No |
| Explorar 4+ archivos para entender | No | Sí, al explorador |
| Escribir un archivo atómico y mecánico | Sí | No |
| Escribir varios archivos o lógica nueva | No | Sí, al implementador |
| Correr `check` o tests | No | Sí (implementador o revisor) |
| Definir alcance y dar por terminado | Sí | Nunca |

Antipatrones: leer 4+ archivos "para entender" y después editar inline; implementar una feature multi-archivo sin pasar por el implementador; correr los tests vos en vez de exigir `check` en verde al rol que corresponde.

## Dependencias (qué lee y qué escribe cada paso)

El líder pasa **referencias** (rutas), no contenido completo.

| Paso | Lee | Escribe |
|---|---|---|
| Explorar | nada | respuesta al líder (hallazgo, archivos, no verificado) |
| Spec | exploración (opcional) | `specs/<feature>.md` (Estado: borrador) |
| Planificar | spec aprobada (requerida si no trivial) | `progress/current.md` (alcance, pasos, criterios) |
| Implementar | plan + spec + `progress/` | código + tests + `progress/` (qué cambió, cómo verificar) |
| Revisar | spec + plan + diff | veredicto escrito en `progress/` |
| Cerrar | todo lo anterior | `progress/` + spec actualizada + snapshot en `history/` |

Paso con dependencia requerida ausente (ej. implementar sin spec aprobada) → bloqueado: no se delega hasta resolver.

## Carga de revisión

Antes de aprobar un plan, el líder estima tamaño: si son **más de ~400 líneas o más de una unidad de entrega**, el plan se divide en slices y cada slice recorre implementar → verificar → revisar por separado. Nunca se le pide al revisor un veredicto sobre un cambio gigante de una sola vez.
