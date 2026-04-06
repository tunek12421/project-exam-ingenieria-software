# Task List - Sistema de Gestion de Tareas

Aplicacion web para la gestion de tareas internas de un equipo de trabajo.

**Repositorio:** https://github.com/tunek12421/project-exam-ingenieria-software
**Rama:** `examen-final`

## Tecnologias utilizadas

- **Backend:** Python 3 con Flask
- **Frontend:** HTML5, CSS3, JavaScript vanilla
- **Base de datos:** SQLite
- **Pruebas:** unittest + pytest (12 tests)
- **Contenedores:** Docker + Docker Compose

## Estructura del proyecto

```
project-exam/
├── backend/
│   ├── src/
│   │   ├── config/         # Configuracion de BD + constantes (context manager)
│   │   ├── controllers/    # Endpoints REST (Flask Blueprints)
│   │   ├── services/       # Logica de negocio y validaciones
│   │   ├── models/         # Modelo de datos Task
│   │   ├── repositories/   # Acceso a datos (queries SQL con _BASE_SELECT)
│   │   └── routes/
│   ├── tests/              # Pruebas unitarias (8 tests)
│   └── main.py             # Punto de entrada del servidor
├── frontend/
│   ├── src/
│   │   ├── components/     # Componentes reutilizables (task_card)
│   │   ├── pages/          # Logica de paginas (main + notificaciones)
│   │   ├── services/       # Cliente HTTP para consumir la API
│   │   └── assets/         # Estilos CSS + animaciones
│   └── index.html
├── database/
│   ├── schema.sql          # Esquema de la base de datos
│   └── seed.sql            # Datos iniciales
├── docs/
│   └── architecture.md     # Documentacion arquitectonica
├── tests/
│   └── integration/        # Pruebas de integracion (4 tests)
├── Dockerfile              # Imagen Python 3.12-slim
├── docker-compose.yml      # Orquestacion con volumen persistente
├── requirements.txt        # Dependencias (Flask)
├── .gitignore
├── .dockerignore
└── README.md
```

## Analisis Arquitectonico (Actividad 2)

### 1. Tipo de arquitectura

El proyecto implementa una **arquitectura por capas (Layered Architecture)** con separacion clara de responsabilidades:

- **Capa de presentacion (Frontend):** Interfaz de usuario con HTML/CSS/JS que se comunica con el backend via API REST.
- **Capa de controladores:** Recibe las peticiones HTTP y delega al servicio correspondiente.
- **Capa de servicios (Logica de negocio):** Contiene las reglas de negocio y validaciones.
- **Capa de repositorios (Acceso a datos):** Encapsula las consultas a la base de datos.
- **Capa de modelos:** Define las entidades del dominio.

### 2. Modulos y componentes identificados

| Modulo | Responsabilidad |
|--------|----------------|
| `config/database.py` | Conexion SQLite con context manager + constante TITLE_MAX_LENGTH |
| `models/task_model.py` | Modelo de datos Task con serializacion y deserializacion |
| `repositories/task_repository.py` | CRUD a nivel de base de datos con _BASE_SELECT |
| `services/task_service.py` | Validaciones y logica de negocio |
| `controllers/task_controller.py` | Endpoints REST de la API |
| `frontend/src/services/` | Cliente HTTP para consumir la API |
| `frontend/src/components/` | Componentes visuales reutilizables |

### 3. Mejoras arquitectonicas propuestas

1. **Inyeccion de dependencias formal:** Usar un contenedor de DI para desacoplar las capas (actualmente se hace manualmente en el constructor del servicio).
2. **Migraciones de base de datos:** Implementar un sistema de migraciones (ej. Alembic) en lugar de ejecutar schema.sql directamente.
3. **Manejo centralizado de errores:** Crear un middleware de errores en Flask para unificar las respuestas de error.
4. **Autenticacion y autorizacion:** Agregar JWT o sesiones para proteger los endpoints.
5. **Framework frontend:** Migrar a un framework como Vue.js o React para mejor mantenibilidad a medida que crezca la aplicacion.

## Refactorizacion realizada (Actividad 3)

### Code smells identificados y corregidos

| Code Smell | Problema | Solucion |
|-----------|----------|----------|
| Resource Leak | Conexiones BD sin try/finally | Context manager `@contextmanager` en `get_database_connection()` |
| SQL duplicado | Misma query SELECT en 3 metodos | Constante de clase `_BASE_SELECT` (principio DRY) |
| Import sin usar | `from datetime import datetime` en task_model.py | Eliminado |
| Magic number | `200` hardcodeado para longitud de titulo | Constante `TITLE_MAX_LENGTH` en config |
| Codigo duplicado | Validacion de tarea existente repetida en service | Metodo `_find_task_or_raise()` |
| Sin validacion frontend | Datos enviados sin validar | `trim()` + check vacio antes de enviar |
| Sin feedback UX | Solo alertas de error | Notificaciones toast con animacion CSS |

## Funcionalidad implementada (Actividad 4)

- Registrar nueva tarea (con titulo y descripcion)
- Listar todas las tareas
- Filtrar tareas pendientes
- Marcar tarea como completada
- Eliminar tarea con confirmacion
- Validacion de datos vacios (backend y frontend)
- Notificaciones visuales de exito

### Endpoints API REST

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | `/api/tasks` | Listar todas las tareas |
| GET | `/api/tasks?filter=pending` | Listar tareas pendientes |
| POST | `/api/tasks` | Crear nueva tarea |
| PATCH | `/api/tasks/<id>/complete` | Marcar como completada |
| DELETE | `/api/tasks/<id>` | Eliminar tarea |

## Pruebas de software (Actividad 5)

**12 pruebas automatizadas** (8 unitarias + 4 de integracion). Todas pasan correctamente.

### Pruebas unitarias (backend/tests/test_task_service.py)
- Crear tarea con datos validos
- Titulo vacio lanza ValidationError
- Titulo con solo espacios es rechazado
- Titulo mayor a 200 caracteres es rechazado
- Completar tarea existente
- Completar tarea inexistente lanza error
- Eliminar tarea inexistente lanza error
- Obtener todas las tareas

### Pruebas de integracion (tests/integration/test_api_integration.py)
- Flujo completo: crear tarea y verificar en listado
- Crear sin titulo retorna error 400
- Crear y luego completar una tarea
- Eliminar inexistente retorna 404

## Como ejecutar

### Con Docker (recomendado)
```bash
docker compose up --build
```
El servidor inicia en `http://localhost:5000`

### Sin Docker
```bash
pip install -r requirements.txt
python3 -m backend.src.main
```

## Como ejecutar las pruebas

```bash
# Todas las pruebas
python3 -m pytest -v

# Solo unitarias
python3 -m pytest backend/tests/ -v

# Solo integracion
python3 -m pytest tests/integration/ -v
```
