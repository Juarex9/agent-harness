# Plantilla MERN del harness

Copiá esta carpeta como base de un proyecto nuevo y adaptá `AGENTS.md` a la realidad del proyecto.

## Primera vez (desde la raíz)

```bash
npm ci                   # instala root + server + client (workspaces)
npx playwright install   # navegadores para el e2e
./init.sh                # verifica que el entorno esté sano
npm run check            # lint + tests + build + e2e
```

```bash
npm run dev --workspace=server   # API http://localhost:3001
npm run dev --workspace=client   # web http://localhost:5173
```

## Qué incluye

| Parte | Para qué |
|---|---|
| `AGENTS.md` | Reglas del proyecto para los agentes |
| `init.sh` | Chequeo de entorno (no trabajar si falla) |
| `npm run check` | Validación oficial |
| `server/` | Express: `GET /api/saludo`, `GET /api/health`, tests con supertest |
| `client/` | Vite + React: home + helper `saludoUrl()` con unitarios |
| `e2e/` | End-to-end con Playwright (home del client) |
| `specs/` | Una spec por feature no trivial (`example.md` de muestra) |
| `progress/` | Memoria de la tarea del worktree |
| `.github/workflows/ci.yml` | CI: corre `check` en cada PR |

Nota: la plantilla es stateless (sin Mongo). El cableado a MongoDB se agrega por proyecto.
