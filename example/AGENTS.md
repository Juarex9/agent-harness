# AGENTS.md (proyecto: harness-template-next)

Plantilla Next.js compatible con el harness. Si usás esta plantilla como base, adaptá este archivo al proyecto real.

## Stack

Next.js 15 + React 19 + TypeScript. Tests unitarios con Vitest (`tests/`), e2e con Playwright (`e2e/`).

## Comandos

- `npm run dev` — desarrollo local (http://localhost:3000).
- `npm run check` — **validación oficial**: lint + typecheck + unitarios + e2e. Sale ≠ 0 si algo falla.
- `npm test` — solo unitarios. `npm run test:e2e` — solo e2e (necesita `npx playwright install` la primera vez).

## Reglas del harness

- Antes de empezar: leer `progress/`, correr `./init.sh`, leer la spec si la tarea la tiene.
- Una tarea a la vez, con criterios de aceptación claros.
- Tarea no trivial sin spec aprobada en `specs/`: no se implementa. La tarea en `progress/` apunta a su spec.
- Toda feature o cambio lleva tests de comportamiento real.
- No marcar nada como terminado sin `check` en verde + aprobación escrita del revisor en `progress/`.
- No tocar secretos, `.env`, ni hacer push o deploy sin que lo pidan.
- Rutas sensibles en `docs/mapa-agentes.json`. El revisor corre la skill `check-map` antes de aprobar.
- Si un comportamiento cambia, actualizar su spec en el mismo cambio.

## Particularidades

- Primera vez: `npm ci` y `npx playwright install` (navegadores e2e).
- Variables de entorno: copiar `.env.example` a `.env` (el `.env` real nunca se commitea; en Orca lo restaura el hook de worktree).
