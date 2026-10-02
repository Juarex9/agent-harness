# Spec: saludo (lib)

- **Estado**: aprobada
- **Fecha**: 2026-09-27
- **Autor**: harness (spec de ejemplo de la plantilla)

## Contexto y problema

La plantilla necesita una función mínima que demuestre el contrato del harness en Python: comportamiento testeable de punta a punta con pytest.

## Comportamiento esperado

`greet(name)` devuelve `"Hola, <nombre>"`. Con `None`, vacío o solo espacios devuelve `"Hola, mundo"`. El nombre se recorta.

## Criterios de aceptación

- [ ] `greet("Ana") == "Hola, Ana"` (cómo se comprueba: `tests/test_greet.py`).
- [ ] `greet(None)`, `greet("")` y `greet("   ")` devuelven `"Hola, mundo"` (cómo se comprueba: unitarios).
- [ ] `greet("  Ana  ") == "Hola, Ana"` (cómo se comprueba: unitario).
- [ ] `ruff check`, `ruff format --check` y `mypy --strict` pasan (cómo se comprueba: `make check`).

## Casos borde

- `None`, vacío y solo espacios: equivalen a ausente → "mundo".
- Nombres con unicode o muy largos: pasan tal cual, sin truncar.

## Fuera de alcance

- API web, base de datos, otros idiomas.
- Empaquetado para PyPI.

## Decisiones técnicas

- Función pura en `src/`: testeable sin infraestructura.
- `mypy --strict` desde el día uno: el código es chico y el costo es cero.
- `ruff` cubre lint y formato en una sola herramienta.
