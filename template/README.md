# Plantilla Next.js del harness

Copiá esta carpeta como base de un proyecto nuevo y adaptá `AGENTS.md` a la realidad del proyecto.

## Primera vez

```bash
npm ci
npx playwright install   # navegadores para el e2e
./init.sh                # verifica que el entorno esté sano
npm run check            # lint + typecheck + unitarios + e2e
npm run dev              # http://localhost:3000
```

## Qué incluye

| Archivo | Para qué |
|---|---|
| `AGENTS.md` | Reglas del proyecto para los agentes |
| `init.sh` | Chequeo de entorno (no trabajar si falla) |
| `npm run check` | Validación oficial: todo en verde o no está terminado |
| `tests/` | Unitarios con Vitest (ejemplo: `lib/format.ts`) |
| `e2e/` | End-to-end con Playwright (ejemplo: home) |
| `specs/` | Una spec por feature no trivial (`example.md` de muestra) |
| `progress/` | Memoria de la tarea del worktree |
| `.github/workflows/ci.yml` | CI: corre `check` en cada PR |
