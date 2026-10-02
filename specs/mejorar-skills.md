# Spec: mejorar skills con el uso

- **Estado**: aprobada
- **Fecha**: 2026-10-02
- **Autor**: plan "Mejorar skills" confirmado por el usuario

## Contexto y problema

Las skills del harness solo cambian cuando alguien lo pide en el chat. No hay un registro de desvíos ni de fallas de CI, y un ajuste improvisado tiende a sacar los controles que frenan al agente.

Hace falta juntar retros y señales del proyecto en curso, y proponer el cambio en un PR del repo del harness. Una persona decide. El script no mergea y no afloja controles.

## Comportamiento esperado

1. `senales.py`, parado en un proyecto, imprime retros nuevas del issue abierto `Retros del flujo con agentes` (después de `<!-- mejorar-skills: consolidado -->`), fallas de CI que no sean de la rama por defecto, y reverts. Solo lee.
2. `retro.py` comenta en ese issue. Si no existe, sin `--confirmar` imprime el borrador y no llama a `gh issue create`. Con `--confirmar` lo crea y lo fija.
3. `abrir_pr.py` sin `--confirmar` imprime el cuerpo del PR y no toca git ni `gh`. Con `--confirmar`, si el checkout del harness está sucio, sale `1`. Crea la rama `mejorar-skills/AAAA-MM-DD` desde `origin/main` cuando todavía no hay commits propios. Rechaza el diff si un `SKILL.md` tocado pasa de 120 líneas o si falta un invariante. Si pasa, hace push y `gh pr create --draft --base main` contra el repo del harness. No llama a `gh pr merge`.
4. El revisor, al cerrar, deja una retro corta.

Invariantes que el diff no puede borrar:

- `if not confirmar` en `skills/crear-issue/crear_issue.py`
- `return 2` en `skills/check-map/check_map.py`
- `check-map` y `crear-issue` en `agents/reviewer.md`

## Criterios de aceptación

- [x] `python3 skills/mejorar-skills/test_mejorar_skills.py` pasa.
- [x] Sin `--confirmar` no se llama a `gh issue create` ni a `gh pr create`.
- [x] Un `SKILL.md` de más de 120 líneas, o un invariante ausente, no llega al push.
- [x] Las fallas de CI de la rama por defecto no entran; las demás se agrupan por workflow.
- [x] `skills/mejorar-skills/SKILL.md` tiene como máximo 120 líneas. El README y el revisor mencionan la skill.

## Casos borde

- `gh` sin autenticar o repo que no es de GitHub: sale `1`. No se inventa una API de Linear.
- Issue de retros ausente y sin `--confirmar`: sale `0` con el borrador.
- Checkout del harness sucio, o commits en una rama que no es `mejorar-skills/fecha`: sale `1`, sin push.
- Diff vacío contra `origin/main`: sale `1`, sin push. La rama puede quedar creada para commitear el ajuste y volver a correr.
- Comentar un issue de retros que ya existe no pide otra confirmación.

## Fuera de alcance

- Programar la corrida (lunes u Orca).
- Mergear el PR.
- Juntar retros de todos los repos en una sola pasada.
- Prefijo de rama `claude/`.
- Cambiar labels o el `check` de las plantillas.

## Decisiones técnicas

- Las señales se leen del proyecto en el que estás (`cwd`). El PR se abre en el checkout del harness, resuelto con `Path(__file__).resolve()`, porque las skills viven ahí y `install.sh` las enlaza a `~/.agents/skills/`.
- Confirmar una vez la creación del issue de retros alcanza para los comentarios siguientes.
- Comandos de GitHub CLI: `gh run list` (https://cli.github.com/manual/gh_run_list), `gh repo view --json defaultBranchRef` (https://cli.github.com/manual/gh_repo_view), `gh issue comment` (https://cli.github.com/manual/gh_issue_comment), `gh issue pin` (https://cli.github.com/manual/gh_issue_pin), `gh pr create --draft` (https://cli.github.com/manual/gh_pr_create).

## Dependencias

- `gh` autenticado y `origin/main` en el harness para publicar un PR de verdad. Los tests no lo necesitan.
- Plan "Mejorar skills" confirmado (esta spec).

## Estimación y slices

- Slice 1: `senales.py`, `retro.py` y tests.
- Slice 2: `abrir_pr.py`, reglas de la skill, revisor, workflow y README.
