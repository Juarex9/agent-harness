#!/usr/bin/env python3
"""Abre un PR draft en el harness. Sin --confirmar no toca git ni gh.

No llama a `gh pr merge`.
https://cli.github.com/manual/gh_pr_create
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

MAX_LINEAS = 120
INVARIANTES = (
    ("skills/crear-issue/crear_issue.py", "if not confirmar"),
    ("skills/check-map/check_map.py", "return 2"),
    ("agents/reviewer.md", "check-map"),
    ("agents/reviewer.md", "crear-issue"),
)

Comando = Callable[[Sequence[str]], subprocess.CompletedProcess[str]]


def raiz_harness() -> Path:
    """skills/mejorar-skills/ → repo. resolve() sigue el symlink de ~/.agents/skills/."""
    return Path(__file__).resolve().parents[2]


@dataclass
class EstadoGit:
    porcelain: str = ""
    rama: str = "main"
    commits_delante: int = 0
    archivos_del_diff: list[str] = field(default_factory=list)
    skills_tocadas: dict[str, str] = field(default_factory=dict)
    textos: dict[str, str] = field(default_factory=dict)
    remote: str = "git@github.com:Juarex9/agent-harness.git"


def repo_de_url(url: str) -> str | None:
    limpio = url.strip()
    if limpio.endswith(".git"):
        limpio = limpio[:-4]
    if limpio.startswith("git@github.com:"):
        return limpio.split(":", 1)[1]
    marca = "github.com/"
    if marca in limpio:
        return limpio.split(marca, 1)[1]
    return None


def armar_cuerpo(patrones: str, preguntas: str, descartado: str) -> str:
    return (
        "## Patrones encontrados\n"
        f"{patrones.strip()}\n\n"
        "## Preguntas para el equipo\n"
        f"{preguntas.strip()}\n\n"
        "## Descartado\n"
        f"{descartado.strip()}\n"
    )


def _git(raiz: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(raiz), *args], capture_output=True, text=True, check=False
    )


def cargar_estado(raiz: Path) -> tuple[EstadoGit | None, str | None]:
    porcelain = _git(raiz, "status", "--porcelain")
    if porcelain.returncode != 0:
        return None, (porcelain.stderr or "git status falló").strip()
    rama = _git(raiz, "rev-parse", "--abbrev-ref", "HEAD")
    if rama.returncode != 0:
        return None, (rama.stderr or "git rev-parse falló").strip()
    delante = _git(raiz, "rev-list", "--count", "origin/main..HEAD")
    if delante.returncode != 0:
        return None, "no está origin/main en el harness"
    nombres = _git(raiz, "diff", "--name-only", "origin/main...HEAD")
    if nombres.returncode != 0:
        return None, (nombres.stderr or "git diff falló").strip()
    archivos = [linea for linea in (nombres.stdout or "").splitlines() if linea]
    skills: dict[str, str] = {}
    for archivo in archivos:
        if archivo.endswith("SKILL.md"):
            ruta = raiz / archivo
            skills[archivo] = ruta.read_text(encoding="utf-8") if ruta.is_file() else ""
    textos: dict[str, str] = {}
    for archivo, _aguja in INVARIANTES:
        ruta = raiz / archivo
        textos[archivo] = ruta.read_text(encoding="utf-8") if ruta.is_file() else ""
    remote = _git(raiz, "remote", "get-url", "origin")
    if remote.returncode != 0:
        return None, "el harness no tiene remote origin"
    try:
        commits = int((delante.stdout or "0").strip() or "0")
    except ValueError:
        return None, "git rev-list no devolvió un número"
    return (
        EstadoGit(
            porcelain=porcelain.stdout or "",
            rama=(rama.stdout or "").strip(),
            commits_delante=commits,
            archivos_del_diff=archivos,
            skills_tocadas=skills,
            textos=textos,
            remote=(remote.stdout or "").strip(),
        ),
        None,
    )


def evaluar(
    titulo: str,
    patrones: str,
    preguntas: str,
    descartado: str,
    confirmar: bool,
    estado: EstadoGit,
    fecha: str,
) -> tuple[int, str, list[list[str]]]:
    cuerpo = armar_cuerpo(patrones, preguntas, descartado)
    if not confirmar:
        return 0, f"título: {titulo}\n\n{cuerpo}", []
    if estado.porcelain.strip():
        return 1, "el checkout del harness tiene cambios sin commitear", []
    rama = f"mejorar-skills/{fecha}"
    if estado.rama != rama:
        if estado.commits_delante != 0:
            return 1, "hay commits fuera de origin/main en otra rama", []
        return (
            1,
            f"rama {rama} creada desde origin/main. Commiteá el ajuste y volvé a correr con --confirmar.",
            [["git", "switch", "-c", rama, "origin/main"]],
        )
    for archivo, texto in estado.skills_tocadas.items():
        if len(texto.splitlines()) > MAX_LINEAS:
            return 1, f"{archivo} supera {MAX_LINEAS} líneas", []
    for archivo, aguja in INVARIANTES:
        if aguja not in estado.textos.get(archivo, ""):
            return 1, f"falta el invariante {aguja!r} en {archivo}", []
    if not estado.archivos_del_diff:
        return 1, "no hay cambios contra origin/main", []
    repo = repo_de_url(estado.remote)
    if not repo:
        return 1, f"remote origin no es un repo de GitHub: {estado.remote}", []
    comandos = [
        ["git", "push", "-u", "origin", "HEAD"],
        [
            "gh",
            "pr",
            "create",
            "--draft",
            "--base",
            "main",
            "--title",
            titulo,
            "--body",
            cuerpo,
            "-R",
            repo,
        ],
    ]
    return 0, cuerpo, comandos


def _correr(raiz: Path, cmd: list[str]) -> subprocess.CompletedProcess[str]:
    if cmd[0] == "git":
        return subprocess.run(
            ["git", "-C", str(raiz), *cmd[1:]],
            capture_output=True,
            text=True,
            check=False,
        )
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="PR draft para ajustar skills del harness.")
    parser.add_argument("--titulo", required=True)
    parser.add_argument("--patrones", required=True)
    parser.add_argument("--preguntas", default="(ninguna)")
    parser.add_argument("--descartado", default="(ninguno)")
    parser.add_argument("--confirmar", action="store_true")
    parser.add_argument("--fecha", default=date.today().isoformat())
    args = parser.parse_args(argv)
    raiz = raiz_harness()
    estado, error = cargar_estado(raiz)
    if estado is None:
        print(error or "no se pudo leer el harness", file=sys.stderr)
        return 1
    codigo, texto, comandos = evaluar(
        args.titulo,
        args.patrones,
        args.preguntas,
        args.descartado,
        args.confirmar,
        estado,
        args.fecha,
    )
    for cmd in comandos:
        if codigo != 0 and cmd[:2] != ["git", "switch"]:
            continue
        hecho = _correr(raiz, cmd)
        if hecho.returncode != 0:
            detalle = (hecho.stderr or hecho.stdout or "comando falló").strip()
            print(detalle, file=sys.stderr)
            return 1
        if cmd[0] == "gh":
            print(hecho.stdout, end="" if (hecho.stdout or "").endswith("\n") else "\n")
    print(texto, end="" if texto.endswith("\n") else "\n")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
