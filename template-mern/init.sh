#!/usr/bin/env bash
#
# init.sh — verifica que el entorno esté sano antes de empezar a trabajar.
# Si algo falla, el agente NO debe empezar: arregla el entorno primero.

set -euo pipefail

fail() { echo "init.sh: FALTA: $1" >&2; exit 1; }
ok()   { echo "init.sh: ok: $1"; }

command -v node >/dev/null || fail "node no instalado (se necesita Node 20+)"
node -e "process.exit(Number(process.versions.node.split('.')[0]) < 20 ? 1 : 0)" \
  || fail "node es muy viejo, se necesita Node 20+"
ok "node $(node --version)"

[ -d node_modules ] || fail "falta node_modules: corré 'npm ci' desde la raíz"
ok "dependencias instaladas"

for f in package.json server/server.js client/src/main.jsx playwright.config.js; do
  [ -f "$f" ] || fail "falta archivo requerido: $f"
done
ok "archivos requeridos presentes"

[ -f server/.env ] || echo "init.sh: aviso: no hay server/.env (copiá server/.env.example si la app lo necesita)"

echo "init.sh: corriendo 'npm run check'..."
npm run check --silent || fail "'npm run check' en rojo: arreglá los chequeos antes de trabajar"
ok "entorno sano, podés empezar"
