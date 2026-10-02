# Spec: saludo personalizado (/saludo)

- **Estado**: aprobada (aprobada con el "dale, pasemos a fase 5"; en flujo real la aprueba el usuario antes de implementar)
- **Fecha**: 2026-09-27
- **Autor**: líder (demo Fase 5)

## Contexto y problema

La plantilla necesita una segunda feature mínima que demuestre el flujo completo con spec: una página que saluda por nombre. Es no trivial (nueva ruta + comportamiento visible), así que lleva spec.

## Comportamiento esperado

`GET /saludo?name=X` muestra un título `Hola, X`. Sin `name`, con valor vacío o solo espacios, muestra `Hola, mundo`. El nombre con espacios se recorta. HTML en el nombre se muestra como texto literal (React lo escapa por defecto).

## Criterios de aceptación

- [ ] `/saludo` sin `name` muestra "Hola, mundo" (cómo se comprueba: e2e `e2e/saludo.spec.ts`).
- [ ] `/saludo?name=Ana` muestra "Hola, Ana" (cómo se comprueba: e2e).
- [ ] `name="<b>Ana</b>"` se ve como texto literal, sin HTML inyectado (cómo se comprueba: e2e con texto exacto).
- [ ] `greet("  Ana  ")` devuelve `"Hola, Ana"` (cómo se comprueba: unitario `tests/greet.test.ts`).
- [ ] `greet(undefined)` y `greet("   ")` devuelven `"Hola, mundo"` (cómo se comprueba: unitario).

## Casos borde

- `name` muy largo o con unicode: se muestra tal cual, sin truncar.
- `name` repetido (`?name=A&name=B`): se usa el primero.
- `name` con solo espacios: equivale a ausente → "Hola, mundo".

## Fuera de alcance

- Otros idiomas (solo español), diseño/estilos más allá del layout existente.
- Otras rutas, persistencia, validación con mensajes de error (el fallback a "mundo" es el comportamiento).

## Decisiones técnicas

- Lógica en `lib/greet.ts` (función pura): testeable sin navegador; el e2e cubre que la página la usa.
- Página como server component de Next 15 (`searchParams` es `Promise`: usar `await`).
- Sin sanitización manual: React escapa por defecto; el e2e lo demuestra con el caso `<b>`.
