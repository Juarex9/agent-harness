#!/usr/bin/env python3
"""Arma el borrador de un issue y, solo con --confirmar, lo crea con gh.

Sin --confirmar imprime el borrador y sale 0, sin llamar a gh.
Con --confirmar llama a `gh issue create`. Si se piden labels, antes
corre `gh label list --json name` y no crea nada si alguno no existe.

Manuales:
https://cli.github.com/manual/gh_issue_create
https://cli.github.com/manual/gh_label_list
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections.abc import Callable, Sequence

Comando = Callable[[list[str]], subprocess.CompletedProcess[str]]


def armar_borrador(titulo: str, cuerpo: str, labels: Sequence[str]) -> str:
    lineas = [f"título: {titulo}", "", cuerpo]
    if labels:
        lineas.extend(["", "labels: " + ", ".join(labels)])
    return "\n".join(lineas).rstrip() + "\n"


def _ejecutar(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def _labels_existentes(runner: Comando) -> tuple[set[str] | None, str | None]:
    proc = runner(["gh", "label", "list", "--json", "name", "--limit", "200"])
    if proc.returncode != 0:
        detalle = (proc.stderr or proc.stdout).strip() or "gh label list falló"
        return None, detalle
    try:
        data = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError:
        return None, "gh label list no devolvió JSON"
    if not isinstance(data, list):
        return None, "gh label list no devolvió una lista"
    nombres: set[str] = set()
    for item in data:
        if isinstance(item, dict) and isinstance(item.get("name"), str):
            nombres.add(item["name"])
    return nombres, None


def _numero(stdout: str) -> str | None:
    match = re.search(r"/issues/(\d+)\s*$", stdout.strip())
    if not match:
        return None
    return match.group(1)


def crear(
    titulo: str,
    cuerpo: str,
    labels: Sequence[str],
    confirmar: bool,
    runner: Comando = _ejecutar,
) -> tuple[int, str]:
    borrador = armar_borrador(titulo, cuerpo, labels)
    if not confirmar:
        return 0, borrador
    if labels:
        existentes, error = _labels_existentes(runner)
        if error:
            return 1, error
        assert existentes is not None
        faltan = [label for label in labels if label not in existentes]
        if faltan:
            return 1, "labels que no existen en el repo: " + ", ".join(faltan)
    cmd = ["gh", "issue", "create", "--title", titulo, "--body", cuerpo]
    for label in labels:
        cmd.extend(["--label", label])
    proc = runner(cmd)
    if proc.returncode != 0:
        detalle = (proc.stderr or proc.stdout).strip() or "gh issue create falló"
        return 1, detalle
    url = (proc.stdout or "").strip()
    numero = _numero(url)
    if numero:
        return 0, f"Issue: #{numero}\n{url}\n"
    return 0, (url + "\n") if url else "issue creado\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Borrador o creación de un issue de GitHub.")
    parser.add_argument("--titulo", required=True)
    parser.add_argument("--cuerpo", required=True)
    parser.add_argument("--label", action="append", default=[])
    parser.add_argument("--confirmar", action="store_true")
    args = parser.parse_args(argv)
    codigo, texto = crear(args.titulo, args.cuerpo, args.label, args.confirmar)
    print(texto, end="" if texto.endswith("\n") else "\n")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
