# Brief: construir mi harness de IA para desarrollo

> Este documento es un encargo para un agente de programación. Leelo entero antes de empezar.
> Trabajá por fases y pedime confirmación al terminar cada una.

## 1. Quién soy y cómo trabajo

- Soy desarrollador de software junior, estudio Ingeniería Informática y trabajo como freelance con proyectos de distintos clientes.
- Mi stack es Python, SQL, MERN (MongoDB, Express, React, Node) y Next.js.
- Uso agentes de programación por terminal: **Cursor CLI** y **OpenCode** (también Muse; verificá cómo se configura antes de asumir nada).
- Uso **Orca** como ADE (entorno de desarrollo para agentes). Orca corre varios agentes en paralelo, cada uno en su propio git worktree (una copia aislada del repo con su rama, su terminal y su navegador). Orca **no** guarda la configuración de los agentes: lanza el programa de cada agente, que lee sus propios archivos (`AGENTS.md`, su carpeta de config global, etc.).

## 2. Qué es el harness y qué objetivo tiene

El harness es todo el entorno que rodea al modelo para que trabaje de forma confiable. Tiene cuatro piezas:

1. **Contexto**: instrucciones y documentación que el agente lee (`AGENTS.md`, reglas, arquitectura, convenciones).
2. **Herramientas**: comandos y scripts que el agente puede ejecutar (chequeos, seed de datos, MCP).
3. **Memoria**: archivos de estado fuera de la ventana de contexto (tarea actual, progreso, historial).
4. **Verificación**: código que comprueba el trabajo (tests, linter, typecheck, hooks, CI).

Principios que tiene que respetar el diseño:

- **Simple primero.** Pocas herramientas y bien elegidas. No sumar skills, MCPs o reglas "por las dudas": más complejidad suele empeorar el resultado.
- **El texto orienta, el código obliga.** Toda regla importante tiene que tener un chequeo ejecutable que la haga cumplir (hook, script o CI).
- **Demostrar, no afirmar.** Ninguna tarea está terminada porque el agente lo diga, sino cuando los chequeos pasan.
- **Contexto chico.** Guardar el estado en archivos para poder abrir sesiones nuevas sin perder información, y delegar en subagentes con contexto limpio.
- **Portable entre agentes y modelos.** Nada atado a una sola herramienta si existe una alternativa estándar (por ejemplo `AGENTS.md`).

## 3. Arquitectura: tres capas

### Capa A: repo global del harness (`agent-harness`)
Un repo propio, independiente de cualquier proyecto, con lo que es mío y no depende del código de un cliente:

- Instrucciones globales de cómo trabajo (flujo, estilo, definición de "terminado").
- Definiciones de agentes con roles:
  - **Líder**: lee la tarea, planifica, delega y decide cuándo algo está terminado.
  - **Implementador**: escribe el código y los tests de la tarea.
  - **Revisor**: corre los chequeos, controla arquitectura y convenciones, aprueba o rechaza con feedback concreto.
  - **Explorador** (opcional): investiga el código o documentación sin modificar nada.
- Comandos y skills reutilizables (pocos al principio).
- Plantilla base para proyectos (ver capa C).
- Un script `install.sh` que cree enlaces simbólicos desde este repo hacia las carpetas de configuración global de cada agente, estilo dotfiles. Tiene que ser idempotente, no pisar configuración existente sin hacer backup y tener un modo `--dry-run`.

### Capa B: configuración en Orca
Lo que se configura en Orca y no en los agentes (documentalo en el repo global como guía, no lo automatices si no hay forma soportada):

- Servidores MCP compartidos (Settings, Integrations, MCP).
- Hooks de creación de worktree por repo (Settings, Repository, Hooks): instalar dependencias, restaurar `.env`, correr `init.sh`.
- Skills instaladas con `npx skills add` (global o local; Orca usa también la carpeta compartida `.agents/skills`).
- Argumentos de lanzamiento de cada agente (Settings, Agents). **Importante:** Orca lanza los agentes con permisos totalmente abiertos por defecto. Proponeme una configuración más segura y explicame qué cambia.

### Capa C: capa fina en cada proyecto
Lo que depende del código de cada proyecto y por eso vive en su repo:

- `AGENTS.md` corto: cómo levantar el proyecto, qué comando lo valida, particularidades, qué no tocar.
- Tests (Vitest o Jest para Node/Next, pytest para Python, Playwright para end-to-end).
- Linter, formatter y typecheck configurados.
- Script `init.sh`: verifica que el entorno esté sano (dependencias, archivos requeridos, tests en verde). Si algo falla, el agente no debe empezar a trabajar.
- CI en GitHub Actions que corre los mismos chequeos en cada PR.
- Carpeta `progress/` con la memoria de la tarea dentro de ese worktree (`current.md` e historial).

## 4. El contrato entre el harness global y cada proyecto

Para que el harness global funcione con cualquier proyecto, todo proyecto tiene que cumplir esta interfaz mínima:

| Elemento | Requisito |
|---|---|
| `AGENTS.md` | En la raíz del repo |
| `npm run check` (o `make check` en Python) | Corre lint, typecheck y tests, y sale con código distinto de 0 si algo falla |
| `init.sh` | Deja el entorno listo o explica qué falta |
| `progress/` | Existe y sigue el formato definido por el harness global |

El revisor global siempre corre `check`; cada proyecto decide qué hace adentro.

## 5. Memoria y tareas con worktrees en paralelo

Cada worktree tiene su propia copia de `progress/`, así que dos agentes en paralelo no ven lo que escribe el otro hasta que se mergea. Por eso:

- `progress/` guarda solo la memoria **de la tarea** de ese worktree.
- El estado global (qué está hecho y qué falta) vive en **issues de GitHub o Linear**, que todos los agentes pueden leer (Orca se integra con ambos).

Proponeme el formato de `progress/current.md` y del historial.

## 6. Orquestación matricial de agentes

Quiero organizar los agentes como una empresa con estructura matricial, donde cada agente que ejecuta responde a dos ejes:

- **Eje de proyecto (el qué):** un agente **líder por tarea o feature**, que en Orca corresponde a un worktree. Define el alcance, planifica, delega y decide cuándo la tarea está lista para entregar.
- **Eje funcional (el cómo):** agentes **especialistas** que no pertenecen a ninguna tarea y aplican los mismos estándares en todos los proyectos. Por ejemplo:
  - revisor de **seguridad** (autenticación, secretos, validación de entradas, dependencias),
  - revisor de **testing** (que los tests prueben comportamiento real y cubran los casos importantes),
  - revisor de **frontend** (convenciones de React/Next, accesibilidad),
  - revisor de **base de datos** (migraciones, índices, consultas).
- **Ejecutores:** los implementadores trabajan en una celda de la matriz: reciben el qué del líder y tienen que cumplir el cómo de cada especialista.

Dónde vive cada eje:

- Los especialistas funcionales se definen en el **repo global del harness** (capa A), cada uno con sus reglas y su checklist, para reutilizarlos en todos los clientes.
- El líder y las tareas viven en **cada proyecto y worktree** (capa C).

Reglas de desempate (tienen que quedar escritas y, cuando se pueda, reforzadas por chequeos):

1. Los estándares funcionales son **restricciones duras**: si un especialista rechaza, la tarea no se entrega y el líder no puede saltearlo.
2. El líder decide el **alcance**: un especialista no puede pedir cambios ajenos a la tarea; si detecta algo fuera de alcance, lo registra como issue aparte.
3. Si después de **2 o 3 rondas** no hay acuerdo, se frena y se me consulta.

Control de costo:

- El líder activa especialistas **solo cuando la tarea lo justifica** (seguridad si toca auth, pagos o datos sensibles; base de datos si hay migraciones), no en todas las tareas.
- Empezar con **un solo revisor general** y separar especialistas cuando un área falle seguido.
- Cada especialista entrega su resultado por escrito en `progress/` (aprobado o rechazado, con motivos concretos), para que el líder no dependa de lo que recuerde en su contexto.

Implementalo de forma incremental: primero líder, implementador y revisor general; los especialistas se agregan en una fase posterior.

## 7. Reglas mínimas para el `AGENTS.md` base

- Antes de empezar: leer `AGENTS.md`, correr `init.sh` y leer `progress/`.
- Una tarea a la vez, con criterios de aceptación claros.
- Toda feature o cambio lleva tests que prueban comportamiento real (no solo que algo existe).
- No marcar nada como terminado sin `check` en verde.
- No tocar secretos, `.env`, ni hacer push o deploy sin que yo lo pida.
- Al terminar: actualizar `progress/` y dejar un resumen del cambio.

## 8. Fases de trabajo

1. **Investigación (sin escribir código).** Verificá en la documentación oficial, con links:
   - qué ubicaciones de configuración global y por proyecto leen Cursor CLI, OpenCode y Muse (instrucciones, agentes, comandos, skills, MCP, hooks);
   - si soportan `AGENTS.md` y subagentes;
   - qué soporta Orca (hooks de worktree, MCP, skills, argumentos de lanzamiento).
   No asumas rutas de memoria: si algo no está documentado, decímelo.
2. **Diseño.** Proponé la estructura del repo global y de la plantilla de proyecto, con un árbol de carpetas y una línea explicando cada archivo. Esperá mi aprobación.
3. **Repo global.** Crealo con instrucciones, agentes, `install.sh` (con `--dry-run`) y un README.
4. **Plantilla de proyecto Next.js.** `AGENTS.md`, tests configurados (unitarios y un e2e de ejemplo), lint, typecheck, `check`, `init.sh`, `progress/` y CI.
5. **Prueba real.** Usá la plantilla en un proyecto de ejemplo, implementá una feature chica siguiendo el flujo completo (líder, implementador, revisor) y mostrame que `check` y el CI pasan.
6. **Especialistas funcionales.** Agregá al repo global al menos el revisor de seguridad y el de testing, con las reglas de activación y desempate de la sección 6, y probalos en el proyecto de ejemplo.
7. **Después:** variante de la plantilla para Python (pytest, ruff, mypy o similar) y para MERN.

## 9. Criterios de aceptación

- Puedo clonar el repo global en otra máquina, correr `install.sh` y tener la misma configuración en Cursor CLI y OpenCode.
- Cualquier agente abierto desde Orca en un proyecto de la plantilla lee las reglas, corre `init.sh` y usa `check` sin que yo se lo explique.
- Si un test falla, el flujo no permite dar la tarea por terminada (hook o CI lo bloquean).
- En un conflicto entre el líder y un especialista, se aplican las reglas de desempate y, si no se resuelve, el flujo frena y me consulta.
- Todo está documentado en un README que un junior pueda seguir.
- Nada de configuración inventada: cada ruta u opción tiene su fuente en la documentación.

## 10. Cómo quiero que me respondas

- En español, con explicaciones claras: estoy aprendiendo, así que decime el porqué de cada decisión.
- Cambios chicos y revisables, uno por fase.
- Si algo es ambiguo o una herramienta no soporta lo que pido, frená y preguntame en vez de improvisar.
