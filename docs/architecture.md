# Arquitectura del Sistema - Task List

## Diagrama de capas

```
┌─────────────────────────────────┐
│       Frontend (HTML/JS/CSS)    │  Capa de Presentacion
│   components / pages / services │
└──────────────┬──────────────────┘
               │ HTTP REST (JSON)
┌──────────────▼──────────────────┐
│     Controllers (Flask Routes)  │  Capa de Controladores
│       task_controller.py        │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│     Services (Business Logic)   │  Capa de Servicios
│       task_service.py           │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│   Repositories (Data Access)    │  Capa de Acceso a Datos
│     task_repository.py          │
└──────────────┬──────────────────┘
               │ SQL
┌──────────────▼──────────────────┐
│        SQLite Database          │  Capa de Persistencia
│          tasks.db               │
└─────────────────────────────────┘
```

## Patron arquitectonico

Se aplica el patron **Repository** para separar la logica de acceso a datos de la logica de negocio. Cada capa tiene una responsabilidad unica y se comunica solo con la capa inmediatamente inferior.

## Flujo de una peticion

1. El usuario interactua con el **Frontend** (clic en boton, enviar formulario).
2. El frontend invoca al **ApiService** que realiza una peticion HTTP al backend.
3. El **Controller** recibe la peticion, extrae los datos y llama al **Service**.
4. El **Service** aplica validaciones y reglas de negocio, luego llama al **Repository**.
5. El **Repository** ejecuta la consulta SQL contra **SQLite** y retorna el resultado.
6. La respuesta sube por las capas hasta el frontend, que actualiza la interfaz.
