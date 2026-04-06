# Task List - Sistema de Gestion de Tareas

Aplicacion web para gestionar tareas con subtareas, progreso visual y checklist tipo Trello.

**Repositorio:** https://github.com/tunek12421/project-exam-ingenieria-software
**Rama:** `examen-enrique-lujan`

## Tecnologias

- **Backend:** Python 3 + Flask
- **Frontend:** HTML5, CSS3, JavaScript vanilla
- **BD:** SQLite
- **Pruebas:** unittest + pytest (21 tests)
- **Contenedores:** Docker + Docker Compose

## Estructura

```
project-exam/
├── backend/
│   ├── src/
│   │   ├── config/         # Conexion BD (context manager) + constantes
│   │   ├── controllers/    # Endpoints REST
│   │   ├── services/       # Logica de negocio y validaciones
│   │   ├── models/         # Modelos TaskList y Subtask
│   │   └── repositories/   # Acceso a datos SQL
│   └── tests/              # 15 pruebas unitarias
├── frontend/
│   ├── src/
│   │   ├── components/     # Tarjeta de tarea con timeline
│   │   ├── pages/          # Logica principal + estado de paneles
│   │   ├── services/       # Cliente API
│   │   └── assets/         # CSS (progreso circular, timeline, toast)
│   └── index.html
├── database/
│   ├── schema.sql          # Tablas task_lists y subtasks (FK CASCADE)
│   └── seed.sql            # Datos iniciales
├── docs/architecture.md
├── tests/integration/      # 6 pruebas de integracion
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Arquitectura (Actividad 2)

**Arquitectura por capas:**

Frontend (HTML/JS) → Controllers → Services → Repositories → SQLite

| Modulo | Responsabilidad |
|--------|----------------|
| `config/database.py` | Conexion SQLite con context manager + TITLE_MAX_LENGTH |
| `models/task_model.py` | Modelos TaskList (con progreso) y Subtask |
| `repositories/task_repository.py` | CRUD con _BASE_SELECT (DRY) |
| `services/task_service.py` | Validaciones y reglas de negocio |
| `controllers/task_controller.py` | 6 endpoints REST |
| `frontend/src/components/` | Tarjeta con circulo de progreso y timeline |

**Mejoras propuestas:** migraciones Alembic, autenticacion JWT, middleware de errores, migrar a Vue/React.

## Refactorizacion (Actividad 3)

| Code Smell | Solucion |
|-----------|----------|
| Conexiones BD sin cierre seguro | Context manager `@contextmanager` |
| Query SQL repetida 3 veces | Constante `_BASE_SELECT` |
| Import datetime sin usar | Eliminado |
| Magic number 200 | Constante `TITLE_MAX_LENGTH` |
| Validacion duplicada en service | Metodo `_find_list_or_raise()` |
| Sin validacion en frontend | `trim()` + check vacio |
| Sin feedback de exito | Notificaciones toast |
| Paneles se cerraban al toggle | Estado preservado con `Set` |
| Request sin JSON daba 415 | `get_json(silent=True)` retorna 400 |

## Funcionalidad (Actividad 4)

- Crear tareas con titulo y descripcion
- Agregar subtareas dentro de cada tarea (checklist)
- Marcar y desmarcar subtareas (toggle)
- Circulo de progreso SVG segun % completado
- Expandir/colapsar subtareas con timeline (linea + dots)
- Eliminar tareas (cascade) y subtareas
- Validacion de campos vacios (front y back)
- Notificaciones toast
- Estado de paneles se preserva al interactuar

### Endpoints API

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | `/api/task-lists` | Listar tareas con subtareas y progreso |
| POST | `/api/task-lists` | Crear tarea |
| DELETE | `/api/task-lists/<id>` | Eliminar tarea (cascade) |
| POST | `/api/task-lists/<id>/subtasks` | Agregar subtarea |
| PATCH | `/api/subtasks/<id>/toggle` | Marcar/desmarcar subtarea |
| DELETE | `/api/subtasks/<id>` | Eliminar subtarea |

## Pruebas (Actividad 5)

**21 pruebas** (15 unitarias + 6 integracion). Todas pasan.

**Unitarias:** crear lista, titulo vacio/espacios/largo, eliminar lista, agregar subtarea, toggle on/off, subtarea inexistente, obtener listas, progreso 0%/25%/100%.

**Integracion:** crear y listar, error 400, progreso con subtareas, toggle check/uncheck, cascade delete, error 404.

## Como ejecutar

```bash
# Con Docker
docker compose up --build

# Sin Docker
pip install -r requirements.txt
python3 -m backend.src.main
```

Servidor en `http://localhost:5000`

## Pruebas

```bash
python3 -m pytest -v
```
