# Instrucciones globales (machine-wide)

Quién soy y cómo trabajo, en cualquier proyecto.

- Desarrollador junior (Ingeniería Informática) + freelance. Stack: Python, SQL, MERN, Next.js.
- Flujo: leer `AGENTS.md` → `init.sh` → `progress/` → una tarea a la vez → tests de comportamiento real → `check` en verde → actualizar `progress/`.
- Tarea no trivial sin spec aprobada: no se implementa. La tarea en `progress/` apunta a su spec.
- Nada está terminado sin `check` en verde y aprobación escrita del revisor.
- No tocar secretos ni `.env`; no hacer push ni deploy sin que lo pidan.
- Español claro, cambios chicos, explicar el porqué.

## Memoria (engram)

Los archivos del proyecto son la fuente de verdad (`progress/`, `specs/` en git). Engram es el índice entre sesiones: qué se decidió, dónde está, cómo recuperarlo.

- **Al empezar** (o tras una compactación): `mem_search` con keywords de la tarea + releer `progress/current.md`. El estado se reconstruye desde archivos + engram, nunca desde la memoria del chat.
- **Al terminar algo importante**: `mem_save` inmediato (decisión, bug con causa, descubrimiento no obvio, convención). Formato: Qué / Por qué / Dónde / Aprendido.
- **Specs**: al aprobarse una spec, snapshot en engram (`topic_key: specs/<feature>`, `capture_prompt: false`). El archivo manda; engram sirve para encontrarla y recuperarla (ver `docs/specs.md`).
- **Al cerrar**: `progress/` al día + resumen guardado. Sin eso, la sesión no existió.

> Instalación: OpenCode lo lee vía symlink a `~/.config/opencode/AGENTS.md` (lo hace `install.sh`).
> Cursor (User Rules) y Muse (user rules): copiar este contenido a mano, ver `README.md`.
