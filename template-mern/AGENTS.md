# AGENTS.md (proyecto: harness-template-mern)

Plantilla MERN compatible con el harness. Si usás esta plantilla como base, adaptá este archivo al proyecto real.

## Stack

Monorepo con workspaces npm: `server/` (Express) + `client/` (Vite + React). Tests de API con supertest+Vitest, unitarios del client con Vitest, e2e con Playwright.

## Comandos (desde la raíz)

- `npm run dev --workspace=server` — API en http://localhost:3001. `npm run dev --workspace=client` — web en http://localhost:5173.
- `npm run check` — **validación oficial**: lint + tests server + tests client + build client + e2e. Sale ≠ 0 si algo falla.

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

- Primera vez: `npm ci` (instala los 3 workspaces) y `npx playwright install` (navegadores e2e).
- La plantilla es **stateless, sin Mongo**: el endpoint de ejemplo no usa DB. El cableado a MongoDB vive en cada proyecto real (`MONGODB_URI` en `server/.env`, nunca commiteado; en Orca lo restaura el hook de worktree).
- El server devuelve datos tal cual en JSON; escapar al mostrar es trabajo del client (React lo hace por defecto).
