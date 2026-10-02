# AGENTS.md (del repo agent-harness)

Instrucciones para cualquier agente que trabaje en este repo.

## Antes de empezar

- Leé `README.md` y los docs de `docs/` que toquen tu cambio.
- Una tarea a la vez, con criterios de aceptación claros.

## Reglas

- Cambios chicos y revisables: una cosa por vez.
- **No inventes rutas ni opciones de configuración.** Toda ruta u opción nueva tiene que tener su fuente en la documentación oficial (agregá el link en el doc o en el mensaje).
- Si una herramienta no soporta lo que se pide, frená y preguntá en vez de improvisar.
- Si cambiás comportamiento (flujo, formato, contrato), actualizá el doc correspondiente en el mismo cambio.
- Nada de secretos en el repo. No commitees, pushees ni deployees sin que te lo pidan.
- Respondé en español y explicá el porqué de cada decisión.

## Definición de terminado

- `install.sh --dry-run` y la instalación real funcionan (probados).
- Docs actualizados si el cambio los afecta.
- Resumen del cambio al terminar.
