from backend.src.config.database import get_database_connection
from backend.src.models.task_model import Task


class TaskRepository:
    """Capa de acceso a datos para las tareas."""

    def find_all(self):
        """Obtiene todas las tareas ordenadas por fecha de creacion."""
        connection = get_database_connection()
        cursor = connection.execute(
            "SELECT id, title, description, is_completed, created_at FROM tasks ORDER BY created_at DESC"
        )
        tasks = [Task.from_row(row) for row in cursor.fetchall()]
        connection.close()
        return tasks

    def find_pending(self):
        """Obtiene solo las tareas pendientes (no completadas)."""
        connection = get_database_connection()
        cursor = connection.execute(
            "SELECT id, title, description, is_completed, created_at FROM tasks WHERE is_completed = 0 ORDER BY created_at DESC"
        )
        tasks = [Task.from_row(row) for row in cursor.fetchall()]
        connection.close()
        return tasks

    def find_by_id(self, task_id):
        """Busca una tarea por su ID."""
        connection = get_database_connection()
        cursor = connection.execute(
            "SELECT id, title, description, is_completed, created_at FROM tasks WHERE id = ?",
            (task_id,)
        )
        row = cursor.fetchone()
        connection.close()
        if row:
            return Task.from_row(row)
        return None

    def create(self, task):
        """Inserta una nueva tarea en la base de datos."""
        connection = get_database_connection()
        cursor = connection.execute(
            "INSERT INTO tasks (title, description, is_completed) VALUES (?, ?, ?)",
            (task.title, task.description, int(task.is_completed))
        )
        connection.commit()
        task.id = cursor.lastrowid
        connection.close()
        return task

    def update_status(self, task_id, is_completed):
        """Actualiza el estado de completado de una tarea."""
        connection = get_database_connection()
        connection.execute(
            "UPDATE tasks SET is_completed = ? WHERE id = ?",
            (int(is_completed), task_id)
        )
        connection.commit()
        connection.close()

    def delete(self, task_id):
        """Elimina una tarea por su ID."""
        connection = get_database_connection()
        connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        connection.commit()
        connection.close()
