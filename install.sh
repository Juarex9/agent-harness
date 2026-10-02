#!/usr/bin/env bash
#
# install.sh — instala la configuración global del harness (estilo dotfiles).
#
#   ./install.sh --dry-run   muestra lo que haría sin cambiar nada
#   ./install.sh             crea symlinks (con backup de lo existente)
#
# Idempotente: correrlo dos veces no cambia nada la segunda vez.
# Solo usa rutas verificadas en documentación oficial (ver README.md).
# No pisa configuración existente: hace backup a <destino>.bak-<fecha>.

set -euo pipefail

HARNESS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DRY_RUN=0

usage() {
  sed -n '2,10p' "$0"
  exit 0
}

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    -h | --help) usage ;;
    *) echo "error: argumento desconocido: $arg (usá --dry-run)" >&2; exit 1 ;;
  esac
done

log()  { echo "$1"; }
run()  { if [ "$DRY_RUN" -eq 1 ]; then echo "[dry-run] $*"; else "$@"; fi; }

# link <origen> <destino>: crea symlink, con backup si el destino ya existe.
link() {
  local src="$1" dst="$2"
  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
    log "ok (ya instalado): $dst"
    return 0
  fi
  if [ -e "$dst" ] || [ -L "$dst" ]; then
    local bak="$dst.bak-$(date +%Y%m%d-%H%M%S)"
    log "backup: $dst -> $bak"
    run mv "$dst" "$bak"
  fi
  log "link: $dst -> $src"
  run mkdir -p "$(dirname "$dst")"
  run ln -s "$src" "$dst"
}

log "== agent-harness: roles (agentes) =="
for role in "$HARNESS_DIR"/agents/*.md "$HARNESS_DIR"/agents/specialists/*.md; do
  [ -e "$role" ] || continue
  name="$(basename "$role")"
  link "$role" "$HOME/.cursor/agents/$name"          # Cursor CLI
  link "$role" "$HOME/.config/opencode/agents/$name" # OpenCode
  # Muse: sin directorio global de agentes documentado; el líder usa estos
  # archivos como texto del encargo al subagente (ver README.md).
done

log "== agent-harness: skills (destino único, lo leen los 3) =="
for skill in "$HARNESS_DIR"/skills/*/; do
  [ -d "$skill" ] || continue
  name="$(basename "$skill")"
  link "$skill" "$HOME/.agents/skills/$name"         # Cursor + OpenCode + Muse
done

log "== agent-harness: instrucciones globales =="
link "$HARNESS_DIR/instructions/global.md" "$HOME/.config/opencode/AGENTS.md" # OpenCode
# Cursor (User Rules) y Muse (user rules): paso manual, ver README.md.

log ""
log "Listo. Pasos manuales restantes (ver README.md y docs/orca.md):"
echo "  1. Cursor: copiar instructions/global.md como User Rules (Customize -> Rules)."
echo "  2. Muse: revisar settings.json (MCP, hooks) sin pisar lo existente."
echo "  3. Orca: MCP compartidos, hooks de worktree, skills y permisos seguros."
