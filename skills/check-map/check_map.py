#!/usr/bin/env python3
"""Marca si un cambio toca rutas de docs/mapa-agentes.json.

Sale 0 si ninguna ruta sensible coincide.
Sale 2 si coincide (imprime tipo y archivo).
Sale 1 si falta el mapa, el JSON es inválido o git status falla.

No ejecuta comandos escritos en el JSON.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

MAPA = Path("docs") / "mapa-agentes.json"


def glob_a_regex(patron: str) -> re.Pattern[str]:
    """Convierte un glob de ruta a regex. `*` no cruza `/`. `**` sí."""
    partes: list[str] = ["^"]
    i = 0
    while i < len(patron):
        if patron.startswith("**/", i):
            partes.append("(?:.*/)?")
            i += 3
            continue
        if patron.startswith("**", i):
            partes.append(".*")
            i += 2
            continue
        caracter = patron[i]
        if caracter == "*":
            partes.append("[^/]*")
        elif caracter == "?":
            partes.append("[^/]")
        else:
            partes.append(re.escape(caracter))
        i += 1
    partes.append("$")
    return re.compile("".join(partes))


def coincide(ruta: str, patron: str) -> bool:
    ruta = ruta.replace("\\", "/").lstrip("./")
    patron = patron.replace("\\", "/")
    if "/" not in patron:
        patron = "**/" + patron
    return glob_a_regex(patron).fullmatch(ruta) is not None


def cargar_sensibles(raiz: Path) -> tuple[list[tuple[str, list[str]]] | None, str | None]:
    ruta = raiz / MAPA
    if not ruta.is_file():
        return None, f"no hay {MAPA.as_posix()}"
    try:
        data = json.loads(ruta.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None, f"{MAPA.as_posix()} no es JSON válido"
    if not isinstance(data, dict):
        return None, f"{MAPA.as_posix()} no es un objeto"
    reglas = data.get("sensibles", [])
    if not isinstance(reglas, list):
        return None, f"{MAPA.as_posix()}: 'sensibles' no es una lista"
    cargadas: list[tuple[str, list[str]]] = []
    for regla in reglas:
        if not isinstance(regla, dict):
            return None, f"{MAPA.as_posix()}: una entrada de 'sensibles' no es un objeto"
        tipo = regla.get("tipo")
        rutas = regla.get("rutas")
        if not isinstance(tipo, str) or not tipo:
            return None, f"{MAPA.as_posix()}: falta 'tipo'"
        if not isinstance(rutas, list) or not all(isinstance(r, str) for r in rutas):
            return None, f"{MAPA.as_posix()}: 'rutas' de {tipo} no es una lista de textos"
        cargadas.append((tipo, rutas))
    return cargadas, None


def archivos_del_status(raiz: Path) -> tuple[list[str] | None, str | None]:
    proc = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=raiz,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        detalle = proc.stderr.strip() or "git status falló"
        return None, detalle
    archivos: list[str] = []
    for linea in proc.stdout.splitlines():
        if len(linea) < 4:
            continue
        ruta = linea[3:]
        if " -> " in ruta:
            ruta = ruta.split(" -> ", 1)[1]
        if len(ruta) >= 2 and ruta[0] == '"' and ruta[-1] == '"':
            ruta = ruta[1:-1]
        archivos.append(ruta)
    return archivos, None


def revisar(raiz: Path, archivos: list[str] | None) -> tuple[int, str]:
    reglas, error = cargar_sensibles(raiz)
    if error:
        return 1, error
    assert reglas is not None
    if archivos is None:
        archivos, error = archivos_del_status(raiz)
        if error:
            return 1, error
        assert archivos is not None
    hallazgos: list[str] = []
    for archivo in archivos:
        for tipo, rutas in reglas:
            if any(coincide(archivo, patron) for patron in rutas):
                hallazgos.append(f"sensible: {tipo}\n  {archivo}")
                break
    if not hallazgos:
        return 0, "sin rutas sensibles"
    return 2, "\n".join(hallazgos)


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    raiz = Path.cwd()
    archivos: list[str] = []
    i = 0
    while i < len(args):
        if args[i] == "--raiz":
            if i + 1 >= len(args):
                print("falta el valor de --raiz", file=sys.stderr)
                return 1
            raiz = Path(args[i + 1])
            i += 2
            continue
        if args[i].startswith("-"):
            print(f"argumento desconocido: {args[i]}", file=sys.stderr)
            return 1
        archivos.append(args[i])
        i += 1
    codigo, texto = revisar(raiz, archivos if archivos else None)
    print(texto)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
