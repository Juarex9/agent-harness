# Spec: mapa de rutas sensibles y skill de issues

- **Estado**: aprobada
- **Fecha**: 2026-10-02
- **Autor**: plan "Mapa e issues" confirmado por el usuario

## Contexto y problema

El harness dice que el agente no toca secretos ni se sale del alcance, pero eso solo está escrito. Un diff puede cambiar `.env` o auth sin que ningún comando lo marque. "Issue aparte" queda como frase en `progress/` y los otros worktrees no lo ven.

Hace falta un mapa por proyecto que un script pueda leer, y una forma de abrir un issue de GitHub real, recién cuando el usuario lo confirma.

## Comportamiento esperado

### Mapa

1. Cada proyecto tiene `docs/mapa-agentes.json` con la sección `sensibles` (`tipo` + `rutas`).
2. El revisor corre `skills/check-map/check_map.py` sobre los archivos del cambio.
3. Si un archivo coincide con una ruta sensible, el script sale `2` e imprime el tipo y el archivo. El líder tiene que haber consultado al usuario; si `progress/` no lo dice, el revisor rechaza.
4. `.env` y `.env.local` son sensibles en cualquier carpeta. `.env.example` no.
5. El script no ejecuta comandos escritos dentro del JSON.

### Issues

1. Un hallazgo fuera de alcance se abre con la skill `crear-issue`.
2. El script arma el borrador y sale `0` sin llamar a `gh`, salvo que reciba `--confirmar`.
3. Con `--confirmar`, crea el issue con `gh issue create`. Los labels tienen que existir ya en el repo (`gh label list --json name`). Si no existen, no crea nada.
4. El número queda en `progress/current.md` como `Issue: #n`.
5. Si `gh` no está autenticado, el repo no es de GitHub o el tracker es Linear, no se inventa otra API: se deja escrito en `progress/` y se frena.

## Criterios de aceptación

- [x] `python3 skills/check-map/test_check_map.py` pasa: acierto en `.env` anidado, no acierto en un archivo normal, `.env.example` no es sensible, JSON inválido sale `1`, mapa ausente sale `1`.
- [x] Un glob con `**` coincide con archivos adentro de esa carpeta y no con el resto del repo (mismo test).
- [x] `python3 skills/crear-issue/test_crear_issue.py` pasa: el borrador incluye título y cuerpo; sin `--confirmar` no se llama a `gh`; con `--confirmar` y un label inexistente no se llama a `gh issue create`.
- [x] `docs/mapa.md` y `docs/progress-format.md` describen el formato. El revisor y el líder mencionan el mapa y `crear-issue`.
- [x] Las plantillas (`template/`, `template-python/`, `template-mern/`, `example/`) traen un mapa mínimo de secretos.

## Casos borde

- Mapa ausente o JSON inválido: sale `1` y no se trata como "todo bien".
- `sensibles` vacío: sale `0`.
- Patrón sin `/`: matchea ese nombre en cualquier carpeta. `*` no cruza `/`. `**` sí.
- Sin archivos de argumento: se leen los del `git status --porcelain`. Si git falla, sale `1`.
- Labels pedidos que no están en el repo: sale `1` y no se crea el issue.
- `gh label list` o `gh issue create` fallan: sale `1` y se muestra el error. No se reintenta por otra vía.
- Issue tracker Linear: la skill no llama al script con `--confirmar`.

## Fuera de alcance

- Épicas, sub-issues, dependencias "Blocked by", workflow de desbloqueo.
- Taxonomía de labels (`tipo:`, `area:`) y formularios en `.github/`.
- Correr el mapa en el CI de las plantillas.
- Ejecutar lint o tests desde el JSON del mapa.
- API de Linear.
- "¿Qué puedo hacer ahora?" (issues sin bloqueantes).

## Decisiones técnicas

- El mapa vive en el repo porque las rutas son de ese proyecto. El script vive en `skills/` porque `install.sh` ya enlaza esa carpeta a `~/.agents/skills/` (ruta ya usada por el harness, no una ruta nueva de Cursor/OpenCode).
- Un solo `check` sigue siendo lint y tests. El mapa es un gate aparte, corrido por el revisor.
- Crear el issue exige `--confirmar` en el script, no solo una frase en la skill: sin el flag, el código no llama a `gh`.
- Comandos de GitHub CLI tomados de su manual: `gh issue list --search` (https://cli.github.com/manual/gh_issue_list), `gh issue create --title --body --label` (https://cli.github.com/manual/gh_issue_create), `gh label list --json name` (https://cli.github.com/manual/gh_label_list).

## Dependencias

- `gh` autenticado en la máquina donde se cree un issue de verdad. Los tests no lo necesitan.
- Plan "Mapa e issues" confirmado (esta spec).

## Estimación y slices

- Slice 1: mapa, script, tests, docs y el enganche en roles y plantillas.
- Slice 2: skill `crear-issue`, script con `--confirmar`, tests y el campo `Issue` en `progress/`.
