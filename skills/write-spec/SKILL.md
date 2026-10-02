---
name: write-spec
description: Ayuda a redactar la spec de una feature siguiendo la plantilla del harness. Úsala cuando el líder determine que la tarea necesita spec.
---

# write-spec

Ayudás a escribir la spec de una feature no trivial. Plantilla: `specs/spec-template.md`. Reglas de cuándo y quién aprueba: `docs/specs.md`.

## Cómo

1. Si falta información, **preguntá antes de inventar** (comportamiento esperado, casos borde, qué queda fuera).
2. Completá todas las secciones de la plantilla. Criterios de aceptación verificables: cada uno dice **cómo se comprueba** (test, comando, e2e).
3. Validá contra este checklist y mostrá el resultado:
   - [ ] Problema y contexto claros para alguien que no conoce la feature.
   - [ ] Cada criterio de aceptación tiene su forma de verificación.
   - [ ] Casos borde listados (no solo el camino feliz).
   - [ ] Fuera de alcance explícito (qué NO incluye).
   - [ ] Decisiones técnicas con su motivo.
4. Guardá como `specs/<feature>.md` con `Estado: borrador`.

La spec la **aprueba el usuario** (pasa a `Estado: aprobada`). Sin spec aprobada no se implementa.
