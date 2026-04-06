# Task List - Sistema de Gestion de Tareas

Aplicacion web para la gestion de tareas internas de un equipo de trabajo.

## Tecnologias utilizadas

- **Backend:** Python 3 con Flask
- **Frontend:** HTML5, CSS3, JavaScript vanilla
- **Base de datos:** SQLite
- **Pruebas:** unittest (Python)

## Estructura del proyecto

```
project-exam/
├── backend/
│   ├── src/
│   │   ├── config/         # Configuracion de base de datos
│   │   ├── controllers/    # Controladores (endpoints REST)
│   │   ├── services/       # Logica de negocio
│   │   ├── models/         # Modelos de datos
│   │   ├── repositories/   # Acceso a datos (queries SQL)
│   │   └── routes/
│   ├── tests/              # Pruebas unitarias
│   └── main.py             # Punto de entrada del servidor
├── frontend/
│   ├── src/
│   │   ├── components/     # Componentes reutilizables (task_card)
│   │   ├── pages/          # Logica de paginas (main)
│   │   ├── services/       # Comunicacion con la API
│   │   └── assets/         # Estilos CSS
│   └── index.html
├── database/
│   ├── schema.sql          # Esquema de la base de datos
│   └── seed.sql            # Datos iniciales
├── docs/
│   └── architecture.md     # Documentacion arquitectonica
└── tests/
    └── integration/        # Pruebas de integracion
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
| `config/database.py` | Conexion y configuracion de SQLite |
| `models/task_model.py` | Modelo de datos Task con serializacion |
| `repositories/task_repository.py` | CRUD a nivel de base de datos |
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

1. **Separacion en capas:** El codigo se organizo en Controller → Service → Repository → Model, eliminando logica mezclada.
2. **Nombres claros y descriptivos:** Se usaron nombres como `find_pending()`, `create_task()`, `_validate_title()` en lugar de nombres genericos.
3. **Validaciones extraidas:** La validacion del titulo se extrajo a un metodo privado `_validate_title()` en el servicio, separando la logica de validacion de la logica de creacion.

## Funcionalidad implementada (Actividad 4)

- Registrar nueva tarea (con titulo y descripcion)
- Listar todas las tareas
- Filtrar tareas pendientes
- Marcar tarea como completada
- Eliminar tarea
- Validacion de datos vacios

## Como ejecutar

```bash
# Instalar dependencias
pip install flask

# Ejecutar el servidor
cd project-exam
python -m backend.src.main
```

El servidor inicia en `http://localhost:5000`

## Como ejecutar las pruebas

```bash
# Pruebas unitarias
python -m pytest backend/tests/ -v

# Pruebas de integracion
python -m pytest tests/integration/ -v

# Todas las pruebas
python -m pytest -v
```
