#!/usr/bin/env python3
"""Comenta una retro. Crea y fija el issue solo con --confirmar.

https://cli.github.com/manual/gh_issue_comment
https://cli.github.com/manual/gh_issue_pin
https://cli.github.com/manual/gh_issue_create
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections.abc import Callable, Sequence

from senales import TITULO, _ejecutar, _error

Comando = Callable[[Sequence[str]], subprocess.CompletedProcess[str]]

CUERPO_ISSUE = (
    "Acá se acumulan las retros del flujo con agentes, una por revisión cerrada.\n"
    "`mejorar-skills` las lee y propone ajustes a las skills en un PR draft del harness.\n"
    "No cerrar este issue.\n"
)


def _numero(stdout: str) -> str | None:
    match = re.search(r"/issues/(\d+)\s*$", stdout.strip())
    return match.group(1) if match else None


def _buscar(runner: Comando) -> tuple[str | None, int | None, str | None]:
    repo = runner(["gh", "repo", "view", "--json", "nameWithOwner"])
    if repo.returncode != 0:
        return None, None, _error(repo, "gh repo view falló")
    try:
        nombre = json.loads(repo.stdout or "{}")["nameWithOwner"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return None, None, "gh repo view no devolvió el repo"
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
        return None, None, _error(issues, "gh issue list falló")
    try:
        lista = json.loads(issues.stdout or "[]")
    except json.JSONDecodeError:
        return None, None, "gh issue list no devolvió JSON"
    numero = next(
        (item["number"] for item in lista if item.get("title") == TITULO),
        None,
    )
    return nombre, numero, None


def enviar(
    cuerpo: str,
    confirmar: bool,
    runner: Comando = _ejecutar,
) -> tuple[int, str]:
    nombre, numero, error = _buscar(runner)
    if error:
        return 1, error
    assert nombre is not None
    if numero is None and not confirmar:
        borrador = f"título: {TITULO}\n\n{CUERPO_ISSUE}\nretro:\n{cuerpo.rstrip()}\n"
        return 0, borrador
    if numero is None:
        creado = runner(
            [
                "gh",
                "issue",
                "create",
                "--title",
                TITULO,
                "--body",
                CUERPO_ISSUE,
                "-R",
                nombre,
            ]
        )
        if creado.returncode != 0:
            return 1, _error(creado, "gh issue create falló")
        numero_texto = _numero(creado.stdout or "")
        if not numero_texto:
            return 1, "gh issue create no devolvió la URL del issue"
        fijado = runner(["gh", "issue", "pin", numero_texto, "-R", nombre])
        if fijado.returncode != 0:
            return 1, _error(fijado, "gh issue pin falló")
        numero = int(numero_texto)
    comentario = runner(
        ["gh", "issue", "comment", str(numero), "--body", cuerpo, "-R", nombre]
    )
    if comentario.returncode != 0:
        return 1, _error(comentario, "gh issue comment falló")
    return 0, f"retro en {nombre}#{numero}\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Publica una retro del flujo con agentes.")
    parser.add_argument("--cuerpo", required=True)
    parser.add_argument("--confirmar", action="store_true")
    args = parser.parse_args(argv)
    codigo, texto = enviar(args.cuerpo, args.confirmar)
    print(texto, end="" if texto.endswith("\n") else "\n")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
