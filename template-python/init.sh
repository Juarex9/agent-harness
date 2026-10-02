#!/usr/bin/env bash
#
# init.sh — verifica que el entorno esté sano antes de empezar a trabajar.
# Si falta el entorno, intenta crearlo (venv local + make install).
# Si algo falla, el agente NO debe empezar: arregla el entorno primero.

set -euo pipefail

fail() { echo "init.sh: FALTA: $1" >&2; exit 1; }
ok()   { echo "init.sh: ok: $1"; }

command -v python3 >/dev/null || fail "python3 no instalado (se necesita 3.11+)"
python3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)" \
  || fail "python es muy viejo, se necesita 3.11+"
ok "python $(python3 --version)"

if [ ! -x .venv/bin/python ]; then
  echo "init.sh: creando .venv e instalando dependencias..."
  (command -v uv >/dev/null && uv venv && uv pip install -e ".[dev]") \
    || make install \
    || fail "no se pudo crear el entorno (¿hay red para pip?)"
fi
ok "entorno .venv presente"

for f in pyproject.toml Makefile; do
  [ -f "$f" ] || fail "falta archivo requerido: $f"
done
ok "archivos requeridos presentes"

[ -f .env ] || echo "init.sh: aviso: no hay .env (copiá .env.example si la app lo necesita)"

echo "init.sh: corriendo 'make check'..."
make check || fail "'make check' en rojo: arreglá los chequeos antes de trabajar"
ok "entorno sano, podés empezar"
