# Specs (solo tareas grandes)

Una spec por feature no trivial, versionada en git junto al código en `specs/`. Plantilla: `specs/spec-template.md`. Skill de ayuda: `write-spec`.

## Cuándo hace falta spec

- **Sin spec**: bug obvio de 1 archivo, cambio de texto/estilo, refactor sin cambio de comportamiento.
- **Con spec**: nueva feature, nuevo endpoint, migración de DB, cambio de comportamiento visible, auth/pagos/datos sensibles.
- Casos límite los decide el líder; si el revisor discrepa, se escribe la spec (ante la duda, spec).

## Flujo

1. Líder (+ skill `write-spec`) redacta → `Estado: borrador`.
2. **El usuario aprueba** → `Estado: aprobada`.
3. Implementador codifica + tests contra los criterios de aceptación.
4. Revisor verifica spec + `check` en verde.

## Reglas duras

- Ninguna tarea no trivial se implementa sin spec aprobada (lo exige el revisor, ver `agents/reviewer.md`).
- La tarea en `progress/` apunta a su spec.
- Si la feature cambia después, **la spec se actualiza en el mismo PR/cambio** (lo exige el revisor).

## Engram (índice y recovery)

El archivo en `specs/` es la fuente de verdad (la historia vive en git). Engram guarda un snapshot para encontrar y recuperar specs entre sesiones y tras compactaciones:

- Al aprobar: `mem_save(title: "specs/<feature>", topic_key: "specs/<feature>", type: "architecture", capture_prompt: false, content: <contenido completo>)`.
- Mismo `topic_key` → upsert (pisa la versión anterior): por eso la historia vive en git, no en engram.
- Al retomar: `mem_search("specs/<feature>")` → `mem_get_observation(id)` para el contenido completo (los previews del search vienen truncados).
