# Capa B: configuración en Orca

Lo que se configura en Orca y no en los agentes. Es guía, no se automatiza (Orca no expone una forma soportada de hacerlo por script).

## 1. Servidores MCP compartidos

Settings → Integrations → MCP. Viven en Orca para que todos los worktrees los usen. El MCP específico de cada agente sigue en sus archivos (`~/.cursor/mcp.json`, `opencode.json`, `mcp_servers` de Muse).

## 2. Hooks de creación de worktree (por repo)

Settings → Repository → Hooks. Comandos que corren tras crear cada worktree, por ejemplo:

```bash
# instalar dependencias (ajustar por stack)
npm ci
# restaurar secretos locales (nunca commiteados)
if [ -f "$ORCA_ROOT_PATH/.env" ]; then cp "$ORCA_ROOT_PATH/.env" "$ORCA_WORKSPACE_NAME/.env"; fi
# verificar que el entorno quedó sano
./init.sh
```

Por qué: si `init.sh` falla acá, el agente no empieza a trabajar sobre un entorno roto.

## 3. Skills

```bash
npx skills add https://github.com/stablyai/orca --skill orca-cli --global
npx skills add https://github.com/stablyai/orca --skill orchestration --global
npx skills add https://github.com/stablyai/orca --skill computer-use --global
```

Se instalan en los directorios de skills de cada agente y en la carpeta compartida `.agents/skills`. Ver [skills registry & MCP](https://www.onorca.dev/docs/cli/skills).

## 4. Argumentos de lanzamiento y propuesta segura

⚠️ **Default de Orca (verificado en [Supported agents](https://www.onorca.dev/docs/agents/supported)):** Orca pre-rellena el flag de bypass de permisos de cada agente (`--dangerously-skip-permissions` en Claude, `--dangerously-bypass-approvals-and-sandbox` en Codex, `--yolo` en Cursor/Gemini/Copilot, etc.). La idea es que el worktree es descartable, pero eso deja sin defensa la máquina host, los secretos y los remotos (un agente puede pushear o filtrar un `.env` sin preguntar).

**Propuesta segura** (Settings → Agents):

1. Quitar los flags de bypass por defecto → cada comando con efectos vuelve a pedir confirmación.
2. Explorador y subagentes de lectura en modo restringido/solo-lectura.
3. Push, deploy y tocar `.env`/secretos: siempre con confirmación (además de prohibido en `AGENTS.md`).
4. Sandbox activado; `--yolo` solo en contenedores desechables, nunca en tu máquina con credenciales reales.

**Qué cambia**: lo reversible (leer, editar, correr tests) fluye sin fricción; lo irreversible (publicar, borrar, exponer secretos) pide confirmación. El worktree sigue siendo aislamiento barato, pero deja de ser la única defensa.
