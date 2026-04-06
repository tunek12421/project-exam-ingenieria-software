from backend.src.config.database import get_database_connection
from backend.src.models.task_model import Task


class TaskRepository:
    """Capa de acceso a datos para las tareas."""

    _BASE_SELECT = "SELECT id, title, description, is_completed, created_at FROM tasks"

    def find_all(self):
        """Obtiene todas las tareas ordenadas por fecha de creacion."""
        with get_database_connection() as connection:
            cursor = connection.execute(
                f"{self._BASE_SELECT} ORDER BY created_at DESC"
            )
            return [Task.from_row(row) for row in cursor.fetchall()]

    def find_pending(self):
        """Obtiene solo las tareas pendientes (no completadas)."""
        with get_database_connection() as connection:
            cursor = connection.execute(
                f"{self._BASE_SELECT} WHERE is_completed = 0 ORDER BY created_at DESC"
            )
            return [Task.from_row(row) for row in cursor.fetchall()]

    def find_by_id(self, task_id):
        """Busca una tarea por su ID."""
        with get_database_connection() as connection:
            cursor = connection.execute(
                f"{self._BASE_SELECT} WHERE id = ?", (task_id,)
            )
            row = cursor.fetchone()
            return Task.from_row(row) if row else None

    def create(self, task):
        """Inserta una nueva tarea en la base de datos."""
        with get_database_connection() as connection:
            cursor = connection.execute(
                "INSERT INTO tasks (title, description, is_completed) VALUES (?, ?, ?)",
                (task.title, task.description, int(task.is_completed))
            )
            connection.commit()
            task.id = cursor.lastrowid
            return task

    def update_status(self, task_id, is_completed):
        """Actualiza el estado de completado de una tarea."""
        with get_database_connection() as connection:
            connection.execute(
                "UPDATE tasks SET is_completed = ? WHERE id = ?",
                (int(is_completed), task_id)
            )
            connection.commit()

    def delete(self, task_id):
        """Elimina una tarea por su ID."""
        with get_database_connection() as connection:
            connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            connection.commit()
