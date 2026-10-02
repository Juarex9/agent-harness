# Mapa de rutas sensibles

Cada proyecto del harness tiene `docs/mapa-agentes.json`. Dice qué archivos no se cambian sin consultar al usuario. El script que lo lee es la skill `check-map` (`skills/check-map/check_map.py`, instalada en `~/.agents/skills/check-map/`).

El mapa vive en el repo porque las rutas son de ese proyecto. El script vive en la máquina porque es el mismo para todos.

## Formato

```json
{
  "_ayuda": "Rutas que el agente no cambia sin consultar. Ver docs/mapa.md.",
  "sensibles": [
    {"tipo": "secretos", "rutas": [".env", ".env.local"]}
  ]
}
```

- `sensibles`: lista de reglas. Cada una tiene `tipo` (texto) y `rutas` (lista de globs).
- Un patrón **sin** `/` matchea ese nombre en cualquier carpeta: `.env` coincide con `.env` y con `server/.env`. No coincide con `.env.example`.
- `*` no cruza `/`. `**` sí: `app/api/auth/**` coincide con `app/api/auth/route.ts` y no con `app/page.tsx`.
- Cuando el proyecto sume auth, pagos o schema, se agrega una regla con las rutas reales. No dejes globs de ejemplo que no existan.

## Códigos de salida

| Código | Significado |
|---|---|
| `0` | Ningún archivo del cambio coincide |
| `2` | Coincide. Hay que haber consultado al usuario y dejarlo en `progress/` |
| `1` | Falta el mapa, el JSON es inválido o `git status` falló |

Sin argumentos, el script mira `git status --porcelain`. Con rutas como argumentos, mira solo esas.

El CI de las plantillas no corre este script: en GitHub Actions no está `~/.agents/skills/`. Lo corre el revisor, igual que corre `check`.
