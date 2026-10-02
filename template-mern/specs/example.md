# Spec: saludo por API (ejemplo)

- **Estado**: aprobada
- **Fecha**: 2026-09-27
- **Autor**: harness (spec de ejemplo de la plantilla)

## Contexto y problema

La plantilla necesita un endpoint mínimo que demuestre el contrato del harness en un stack cliente+servidor: comportamiento testeable con supertest del lado server y helper puro del lado client.

## Comportamiento esperado

`GET /api/saludo?name=X` devuelve `{ "saludo": "Hola, X" }`. Sin `name`, vacío o solo espacios devuelve `{ "saludo": "Hola, mundo" }`. El nombre viaja tal cual en el JSON; escapar al mostrar es trabajo del client. `GET /api/health` devuelve `{ "status": "ok" }`.

## Criterios de aceptación

- [ ] `/api/saludo` → `{ "saludo": "Hola, mundo" }` (cómo se comprueba: supertest `server/tests/api.test.js`).
- [ ] `/api/saludo?name=Ana` → `{ "saludo": "Hola, Ana" }` (cómo se comprueba: supertest).
- [ ] Nombre con HTML viaja literal en el JSON (cómo se comprueba: supertest con texto exacto).
- [ ] `saludoUrl()` construye la URL con codificación correcta (cómo se comprueba: unitario `client/src/lib/api.test.js`).
- [ ] La home del client muestra el título (cómo se comprueba: e2e `e2e/home.spec.js`).

## Casos borde

- `name` repetido: se usa el primero. Vacío/espacios: equivale a ausente.
- Caracteres especiales: `URLSearchParams` los codifica del lado client.

## Fuera de alcance

- MongoDB (plantilla stateless; el cableado es por proyecto).
- Integración client→API en e2e, autenticación, otros endpoints.

## Decisiones técnicas

- Lógica de saludo duplicada a propósito (server `greet.js` + client `api.js`): cada lado se testea sin levantar el otro.
- Supertest sin levantar puerto: los tests de API no necesitan red.
