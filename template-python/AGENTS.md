# AGENTS.md (proyecto: harness-template-python)

Plantilla Python compatible con el harness. Si usás esta plantilla como base, adaptá este archivo al proyecto real.

## Stack

Python 3.11+, pytest (`tests/`), ruff (lint+format), mypy estricto. Entorno local en `.venv` (nunca en `/tmp`, nunca `--break-system-packages`).

## Comandos

- `make install` — crea `.venv` e instala dependencias dev (o `uv venv && uv pip install -e ".[dev]"`).
- `make check` — **validación oficial**: lint + typecheck + tests. Sale ≠ 0 si algo falla.
- `make test` — solo tests. `make lint`, `make typecheck` — por separado.

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

- Variables de entorno: copiar `.env.example` a `.env` (nunca se commitea; en Orca lo restaura el hook de worktree).
