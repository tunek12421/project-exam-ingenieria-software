from backend.src.config.database import get_database_connection
from backend.src.models.task_model import TaskList, Subtask


class TaskRepository:
    """Capa de acceso a datos para listas de tareas y subtareas."""

    _LIST_SELECT = "SELECT id, title, description, created_at FROM task_lists"
    _SUBTASK_SELECT = "SELECT id, task_list_id, title, is_completed, created_at FROM subtasks"

    # --- Task Lists ---

    def find_all_lists(self):
        """Obtiene todas las listas de tareas con sus subtareas."""
        with get_database_connection() as conn:
            cursor = conn.execute(f"{self._LIST_SELECT} ORDER BY created_at DESC")
            task_lists = [TaskList.from_row(row) for row in cursor.fetchall()]
            for task_list in task_lists:
                task_list.subtasks = self._find_subtasks_by_list_id(conn, task_list.id)
            return task_lists

    def find_list_by_id(self, list_id):
        """Busca una lista de tareas por su ID con sus subtareas."""
        with get_database_connection() as conn:
            cursor = conn.execute(f"{self._LIST_SELECT} WHERE id = ?", (list_id,))
            row = cursor.fetchone()
            if not row:
                return None
            task_list = TaskList.from_row(row)
            task_list.subtasks = self._find_subtasks_by_list_id(conn, list_id)
            return task_list

    def create_list(self, task_list):
        """Crea una nueva lista de tareas."""
        with get_database_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO task_lists (title, description) VALUES (?, ?)",
                (task_list.title, task_list.description)
            )
            conn.commit()
            task_list.id = cursor.lastrowid
            return task_list

    def delete_list(self, list_id):
        """Elimina una lista de tareas y sus subtareas (CASCADE)."""
        with get_database_connection() as conn:
            conn.execute("DELETE FROM task_lists WHERE id = ?", (list_id,))
            conn.commit()

    # --- Subtasks ---

    def _find_subtasks_by_list_id(self, conn, list_id):
        """Obtiene las subtareas de una lista (usa conexion existente)."""
        cursor = conn.execute(
            f"{self._SUBTASK_SELECT} WHERE task_list_id = ? ORDER BY created_at ASC",
            (list_id,)
        )
        return [Subtask.from_row(row) for row in cursor.fetchall()]

    def find_subtask_by_id(self, subtask_id):
        """Busca una subtarea por su ID."""
        with get_database_connection() as conn:
            cursor = conn.execute(
                f"{self._SUBTASK_SELECT} WHERE id = ?", (subtask_id,)
            )
            row = cursor.fetchone()
            return Subtask.from_row(row) if row else None

    def create_subtask(self, subtask):
        """Crea una nueva subtarea dentro de una lista."""
        with get_database_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO subtasks (task_list_id, title, is_completed) VALUES (?, ?, ?)",
                (subtask.task_list_id, subtask.title, int(subtask.is_completed))
            )
            conn.commit()
            subtask.id = cursor.lastrowid
            return subtask

    def toggle_subtask(self, subtask_id, is_completed):
        """Cambia el estado de completado de una subtarea."""
        with get_database_connection() as conn:
            conn.execute(
                "UPDATE subtasks SET is_completed = ? WHERE id = ?",
                (int(is_completed), subtask_id)
            )
            conn.commit()

    def delete_subtask(self, subtask_id):
        """Elimina una subtarea."""
        with get_database_connection() as conn:
            conn.execute("DELETE FROM subtasks WHERE id = ?", (subtask_id,))
            conn.commit()
