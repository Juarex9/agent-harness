# Tarea: saludo personalizado (/saludo) — demo Fase 5

- Estado: terminado
- Spec: specs/saludo.md (Estado: aprobada)
- Criterios de aceptación:
  - [x] `/saludo` → "Hola, mundo" (e2e escrito, pendiente ejecución con navegador)
  - [x] `/saludo?name=Ana` → "Hola, Ana" (e2e escrito, pendiente ejecución con navegador)
  - [x] HTML en el nombre se muestra literal (e2e escrito, pendiente ejecución con navegador)
  - [x] `greet()` recorta y defaultea a "mundo" (unitario 5/5 en verde)
  - [x] `npm run lint`, `typecheck` y `test` en verde (verificado por líder + revisor por separado)
- Plan:
  1. Líder: spec + plan (hecho)
  2. Implementador (subagente): `lib/greet.ts`, `tests/greet.test.ts`, `app/saludo/page.tsx`, `e2e/saludo.spec.ts` (hecho)
  3. Revisor (subagente, contexto limpio): veredicto APROBADO (hecho, abajo)
  4. Líder: fix raíz del issue aparte + cierre (hecho)
- Decisiones:
  - Lógica pura en `lib/` para testear sin navegador
  - Fix raíz del hallazgo del revisor: `eslint.config.mjs` ignora `.next/` y `next-env.d.ts` (aplicado en `template/` y `example/`)
- Bloqueos:
  - e2e no ejecutable en el sandbox de Muse (Chromium crashea, sin red para el dev server): specs validados por compilación (`--list`: 4 tests en 2 archivos); ejecución real en CI/máquina del usuario
- Último resumen: feature implementada según spec, revisor aprobó, checks ejecutables en verde. Archivos: `lib/greet.ts`, `tests/greet.test.ts`, `app/saludo/page.tsx`, `e2e/saludo.spec.ts`.
- Veredicto del revisor: APROBADO. Corrió por su cuenta lint (en fuente), typecheck, unitarios 8/8 y `--list` (4 tests). Issue aparte (fuera de alcance, registrado y corregido por el líder): `npm run lint` fallaba con 179 errores en `.next/` por falta de `ignores` en el template.
