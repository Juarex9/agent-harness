# Veredictos de especialistas — /saludo (Fase 6, prueba en example/)

Fecha: 2026-09-27. Ambos corrieron en paralelo, en contexto limpio, sin modificar archivos.

## Seguridad: APROBADO

- Entradas/XSS: `page.tsx` pasa `name` (o primer elemento si es array) a `greet()`; sin concatenación en queries/comandos/SQL; React escapa por defecto y el e2e lo demuestra con texto exacto + `h1 b` count 0.
- Secretos: `.gitignore` cubre `.env`; sin keys en código, logs ni errores.
- Dependencias: `npm audit --omit=dev` revisado (alcance: sin cambios de deps en la feature).
- Sin issues aparte.

## Testing: APROBADO

Mapeo spec → test 1:1 (`specs/saludo.md`):
- Sin `name` → e2e `saludo.spec.ts:3`; `?name=Ana` → `:9`; HTML literal → `:15`.
- `greet("  Ana  ")`, `undefined`, vacío → unitarios en `tests/greet.test.ts`.
- Comportamiento real (fallarían con código roto), bordes cubiertos, e2e compilan (`--list`: 4 tests), nada roto ni salteado (8/8 en verde, corrido por el especialista).
- Sin issues aparte.

## Reglas aplicadas (docs/matrix.md)

Activación justificada: la tarea refleja input de URL en HTML (seguridad) y tiene criterios dependientes de tests (testing). Ningún rechazo → sin desempate. Veredictos por escrito acá, el líder no depende de su contexto.
