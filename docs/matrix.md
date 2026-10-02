# Orquestación matricial

Cada implementador trabaja en una celda: recibe el **qué** del líder y cumple el **cómo** de los estándares.

## Los dos ejes

- **Eje de proyecto (el qué)**: un líder por tarea/feature (= un worktree en Orca). Alcance, plan, delegación, decisión de entrega. Vive en cada proyecto (`progress/`, `specs/`).
- **Eje funcional (el cómo)**: estándares que valen en todos los proyectos. Viven en este repo (`agents/`, `skills/`, `specs/spec-template.md`).

## Implementación incremental

- **Base**: líder + implementador + **un revisor general** (`agents/reviewer.md`).
- **Especialistas** en `agents/specialists/` (hoy: seguridad, testing; a futuro: frontend, base de datos), cada uno con sus reglas y checklist. Nuevos especialistas se agregan cuando un área falle seguido.

## Activación (control de costo)

El líder activa especialistas solo si la tarea lo justifica:

| Si la tarea toca... | Activar |
|---|---|
| Auth, secretos, pagos, datos sensibles, dependencias nuevas | seguridad |
| Lógica con ramas/casos borde importantes | testing |
| Componentes, accesibilidad | frontend |
| Migraciones, índices, consultas | base de datos |

## Desempate

1. Los estándares funcionales son **restricciones duras**: si un especialista rechaza, no se entrega y el líder no puede saltearlo.
2. El líder decide el **alcance**: pedido fuera de la tarea → issue aparte, no bloqueo.
3. Después de **2–3 rondas** sin acuerdo: se frena y se consulta al usuario.

## Salida escrita

Cada revisor/especialista deja en `progress/`: veredicto (aprobado/rechazado), motivos concretos (archivo y línea) y comandos verificados. El líder no depende de su memoria de contexto.
