# Spec: home de la plantilla

- **Estado**: aprobada
- **Fecha**: 2026-09-27
- **Autor**: harness (spec de ejemplo de la plantilla)

## Contexto y problema

La plantilla necesita una home mínima que demuestre el contrato del harness: algo visible que los tests unitarios y e2e puedan verificar de punta a punta.

## Comportamiento esperado

Al abrir `/`, se ve un título "Plantilla Harness", una descripción de qué valida `npm run check` y un precio de ejemplo formateado en pesos argentinos.

## Criterios de aceptación

- [ ] El título "Plantilla Harness" es visible (cómo se comprueba: e2e `e2e/home.spec.ts`).
- [ ] El precio de ejemplo contiene "$" (cómo se comprueba: e2e `e2e/home.spec.ts`).
- [ ] `formatCurrency(1999.5)` devuelve `"$ 1.999,50"` (cómo se comprueba: unitario `tests/format.test.ts`).
- [ ] `formatCurrency` rechaza `NaN` e `Infinity` con error (cómo se comprueba: unitario `tests/format.test.ts`).

## Casos borde

- Valores no finitos (`NaN`, `Infinity`): lanza `Error("formatCurrency espera un número finito")`.
- Cero: se formatea como `"$ 0,00"`, no falla.

## Fuera de alcance

- Otros idiomas/monedas (solo `es-AR` / ARS).
- Diseño visual (sin Tailwind ni componentes: HTML plano).
- Cualquier otra página o ruta.

## Decisiones técnicas

- Formato con `Intl.NumberFormat("es-AR", ...)` en vez de formateo manual: respeta reglas locales sin código propio.
- Unitario sobre función pura + e2e sobre la página: el unitario cubre bordes barato, el e2e cubre que la página lo muestra.
