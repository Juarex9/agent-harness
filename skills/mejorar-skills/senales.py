#!/usr/bin/env python3
"""Junta retros, fallas de CI y reverts. Solo lee. No crea issues ni PRs.

Manuales:
https://cli.github.com/manual/gh_run_list
https://cli.github.com/manual/gh_repo_view
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from collections.abc import Callable, Sequence

TITULO = "Retros del flujo con agentes"
MARCA = "<!-- mejorar-skills: consolidado -->"

Comando = Callable[[Sequence[str]], subprocess.CompletedProcess[str]]


def _ejecutar(cmd: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(cmd), capture_output=True, text=True, check=False)


def jsons(texto: str) -> list[object]:
    decodificador = json.JSONDecoder()
    indice = 0
    salida: list[object] = []
    while indice < len(texto):
        while indice < len(texto) and texto[indice].isspace():
            indice += 1
        if indice >= len(texto):
            break
        valor, indice = decodificador.raw_decode(texto, indice)
        salida.append(valor)
    return salida


def retros_nuevas(comentarios: Sequence[dict], marca: str = MARCA) -> list[dict]:
    ultima = -1
    for indice, comentario in enumerate(comentarios):
        if marca in (comentario.get("body") or ""):
            ultima = indice
    return list(comentarios[ultima + 1 :])


def fallas_de_agentes(
    runs: Sequence[dict], rama_defecto: str, desde: str
) -> dict[str, list[dict]]:
    grupos: dict[str, list[dict]] = defaultdict(list)
    for run in runs:
        rama = run.get("headBranch") or ""
        cuando = run.get("createdAt") or ""
        if rama == rama_defecto or cuando < desde:
            continue
        grupos[run.get("workflowName") or "(sin workflow)"].append(run)
    return dict(grupos)


def _texto_retros(comentarios: Sequence[dict]) -> str:
    nuevas = retros_nuevas(comentarios)
    if not nuevas:
        return "_Ninguna desde la última consolidación._\n"
    bloques: list[str] = []
    for comentario in nuevas:
        usuario = (comentario.get("user") or {}).get("login") or "?"
        fecha = (comentario.get("created_at") or "")[:10]
        url = comentario.get("html_url") or ""
        bloques.append(
            f"### {fecha} · @{usuario} · {url}\n{comentario.get('body') or ''}\n"
        )
    return "\n".join(bloques)


def _texto_fallas(grupos: dict[str, list[dict]]) -> str:
    if not grupos:
        return "_Ninguna._\n"
    lineas: list[str] = []
    ordenados = sorted(grupos.items(), key=lambda item: -len(item[1]))
    for workflow, runs in ordenados:
        ramas = sorted({run.get("headBranch") or "" for run in runs})
        ejemplo = runs[0]
        lineas.append(
            f"- **{workflow}**: {len(runs)} falla(s) en {len(ramas)} rama(s). "
            f"Ejemplo: {ejemplo.get('headBranch')} — {ejemplo.get('displayTitle')} "
            f"({ejemplo.get('url')})"
        )
    return "\n".join(lineas) + "\n"


def armar_informe(
    comentarios: Sequence[dict] | None,
    grupos: dict[str, list[dict]],
    reverts: str,
    dias: int,
    sin_issue: bool,
) -> str:
    if sin_issue:
        bloque_retros = f'_No existe el issue "{TITULO}"._\n'
    else:
        bloque_retros = _texto_retros(comentarios or [])
    reverts = reverts.strip() or "_Ninguno._"
    return (
        "# Señales para mejorar las skills\n\n"
        "## Retros nuevas\n"
        f"{bloque_retros}\n"
        f"## Fallas de CI fuera de la rama por defecto (últimos {dias} días)\n"
        f"{_texto_fallas(grupos)}\n"
        f"## Reverts (últimos {dias} días)\n"
        f"{reverts}\n"
    )


def _error(proc: subprocess.CompletedProcess[str], mensaje: str) -> str:
    return (proc.stderr or proc.stdout or mensaje).strip() or mensaje


def juntar(
    dias: int = 30,
    desde: str | None = None,
    runner: Comando = _ejecutar,
    git: Comando | None = None,
) -> tuple[int, str]:
    if desde is None:
        fecha = runner(["date", "-u", "-d", f"{dias} days ago", "+%Y-%m-%dT%H:%M:%SZ"])
        if fecha.returncode != 0:
            return 1, _error(fecha, "date falló")
        desde = (fecha.stdout or "").strip()
    repo = runner(["gh", "repo", "view", "--json", "nameWithOwner,defaultBranchRef"])
    if repo.returncode != 0:
        return 1, _error(repo, "gh repo view falló")
    try:
        datos = json.loads(repo.stdout or "{}")
        nombre = datos["nameWithOwner"]
        rama_defecto = datos["defaultBranchRef"]["name"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return 1, "gh repo view no devolvió el repo ni la rama por defecto"
    if not rama_defecto:
        return 1, "el repo no tiene rama por defecto"

    issues = runner(
        [
            "gh",
            "issue",
            "list",
            "--state",
            "open",
            "--limit",
            "20",
            "--search",
            f'"{TITULO}" in:title',
            "--json",
            "number,title",
        ]
    )
    if issues.returncode != 0:
        return 1, _error(issues, "gh issue list falló")
    try:
        lista = json.loads(issues.stdout or "[]")
    except json.JSONDecodeError:
        return 1, "gh issue list no devolvió JSON"
    numero = next(
        (item["number"] for item in lista if item.get("title") == TITULO),
        None,
    )
    comentarios: list[dict] | None = None
    sin_issue = numero is None
    if numero is not None:
        crudos = runner(
            ["gh", "api", "--paginate", f"repos/{nombre}/issues/{numero}/comments"]
        )
        if crudos.returncode != 0:
            return 1, _error(crudos, "gh api comments falló")
        try:
            parseados = jsons(crudos.stdout or "[]")
        except json.JSONDecodeError:
            return 1, "los comentarios del issue no son JSON"
        comentarios = []
        for bloque in parseados:
            if isinstance(bloque, list):
                comentarios.extend(item for item in bloque if isinstance(item, dict))
            elif isinstance(bloque, dict):
                comentarios.append(bloque)

    runs = runner(
        [
            "gh",
            "run",
            "list",
            "--status",
            "failure",
            "--limit",
            "100",
            "--json",
            "headBranch,workflowName,displayTitle,createdAt,url",
        ]
    )
    if runs.returncode != 0:
        return 1, _error(runs, "gh run list falló")
    try:
        lista_runs = json.loads(runs.stdout or "[]")
    except json.JSONDecodeError:
        return 1, "gh run list no devolvió JSON"
    grupos = fallas_de_agentes(lista_runs, rama_defecto, desde)

    log = (git or _ejecutar)(
        [
            "git",
            "log",
            f"--since={dias} days ago",
            "-i",
            "--grep=revert",
            "--format=- %h %s",
        ]
    )
    reverts = log.stdout or "" if log.returncode == 0 else ""
    return 0, armar_informe(comentarios, grupos, reverts, dias, sin_issue)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Señales para mejorar las skills. Solo lee.")
    parser.add_argument("dias", nargs="?", type=int, default=30)
    parser.add_argument("--desde", default=None, help="ISO-8601; si falta, se calcula con date.")
    args = parser.parse_args(argv)
    codigo, texto = juntar(args.dias, args.desde)
    print(texto, end="" if texto.endswith("\n") else "\n")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
