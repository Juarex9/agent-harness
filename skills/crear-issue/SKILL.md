---
name: crear-issue
description: Abre un issue de GitHub para un hallazgo fuera de alcance. Muestra el borrador y solo lo crea cuando el usuario lo confirma.
---

# crear-issue

"Issue aparte" es un issue de verdad, con número en `progress/current.md`. El estado global vive ahí; el worktree no lo ve hasta el merge.

## Cuándo frenar

No llames al script con `--confirmar` si pasa alguna de estas:

- El tracker del proyecto es Linear.
- `gh auth status` falla.
- El repo no está en GitHub.

Dejalo escrito en `progress/` como `Issue: N/A — <motivo>` y no inventes otra API.

## Pasos

1. Buscá duplicados con el comando oficial ([manual](https://cli.github.com/manual/gh_issue_list)):

```bash
gh issue list --search "<palabras del hallazgo>" --state open --limit 10
```

Si ya existe, usá ese número. No abras otro.

2. Mirá los labels que ya existen ([manual](https://cli.github.com/manual/gh_label_list)). No inventes nombres ni pidas crear labels:

```bash
gh label list --json name --limit 200
```

3. Mostrá el borrador, sin crear nada:

```bash
python3 ~/.agents/skills/crear-issue/crear_issue.py \
  --titulo "el título en imperativo" \
  --cuerpo "qué pasa, por qué queda fuera de esta tarea"
```

En el repo del harness, si no corriste `install.sh`: `python3 skills/crear-issue/crear_issue.py` con los mismos flags.

4. Recién cuando el usuario confirme, repetí el comando con `--confirmar` y, si aplica, `--label` por cada label que ya exista. El script rechaza un label que no esté en el repo y en ese caso no llama a `gh issue create` ([manual](https://cli.github.com/manual/gh_issue_create)).

5. Copiá `Issue: #n` a `progress/current.md` (skill `update-progress`). Fusioná con lo que ya está; no reescribas el archivo.
