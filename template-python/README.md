# Plantilla Python del harness

Copiá esta carpeta como base de un proyecto nuevo y adaptá `AGENTS.md` a la realidad del proyecto.

## Primera vez

```bash
make install     # crea .venv e instala dev deps (o: uv venv && uv pip install -e ".[dev]")
./init.sh        # verifica que el entorno esté sano
make check       # lint + typecheck + tests
```

## Qué incluye

| Archivo | Para qué |
|---|---|
| `AGENTS.md` | Reglas del proyecto para los agentes |
| `init.sh` | Chequeo de entorno (no trabajar si falla) |
| `Makefile` | `make check` = validación oficial |
| `src/` | Código (`greet.py` de ejemplo) |
| `tests/` | Tests con pytest (ejemplo: `test_greet.py`) |
| `specs/` | Una spec por feature no trivial (`example.md` de muestra) |
| `progress/` | Memoria de la tarea del worktree |
| `.github/workflows/ci.yml` | CI: corre `make check` en cada PR |

Herramientas: ruff (lint+format), mypy en modo estricto, pytest.
