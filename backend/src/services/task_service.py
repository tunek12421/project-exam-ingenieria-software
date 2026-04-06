from backend.src.config.database import TITLE_MAX_LENGTH
from backend.src.models.task_model import TaskList, Subtask
from backend.src.repositories.task_repository import TaskRepository


class ValidationError(Exception):
    """Error lanzado cuando los datos de entrada no son validos."""
    pass


class TaskNotFoundError(Exception):
    """Error lanzado cuando no se encuentra una tarea o subtarea."""
    pass


class TaskService:
    """Capa de logica de negocio para la gestion de listas de tareas y subtareas."""

    def __init__(self, repository=None):
        self.repository = repository or TaskRepository()

    # --- Task Lists ---

    def get_all_lists(self):
        """Retorna todas las listas de tareas con subtareas y progreso."""
        return self.repository.find_all_lists()

    def create_list(self, title, description=""):
        """Crea una nueva lista de tareas."""
        title = self._validate_title(title)
        description = description.strip() if description else ""
        task_list = TaskList(title=title, description=description)
        return self.repository.create_list(task_list)

    def delete_list(self, list_id):
        """Elimina una lista de tareas."""
        self._find_list_or_raise(list_id)
        self.repository.delete_list(list_id)

    # --- Subtasks ---

    def add_subtask(self, list_id, title):
        """Agrega una subtarea a una lista existente."""
        self._find_list_or_raise(list_id)
        title = self._validate_title(title)
        subtask = Subtask(task_list_id=list_id, title=title)
        return self.repository.create_subtask(subtask)

    def toggle_subtask(self, subtask_id):
        """Alterna el estado completado/pendiente de una subtarea."""
        subtask = self._find_subtask_or_raise(subtask_id)
        new_status = not subtask.is_completed
        self.repository.toggle_subtask(subtask_id, new_status)
        subtask.is_completed = new_status
        return subtask

    def delete_subtask(self, subtask_id):
        """Elimina una subtarea."""
        self._find_subtask_or_raise(subtask_id)
        self.repository.delete_subtask(subtask_id)

    # --- Helpers ---

    def _find_list_or_raise(self, list_id):
        """Busca una lista o lanza error si no existe."""
        task_list = self.repository.find_list_by_id(list_id)
        if not task_list:
            raise TaskNotFoundError(f"No se encontro la lista con ID {list_id}")
        return task_list

    def _find_subtask_or_raise(self, subtask_id):
        """Busca una subtarea o lanza error si no existe."""
        subtask = self.repository.find_subtask_by_id(subtask_id)
        if not subtask:
            raise TaskNotFoundError(f"No se encontro la subtarea con ID {subtask_id}")
        return subtask

    def _validate_title(self, title):
        """Valida que el titulo no este vacio ni sea demasiado largo."""
        if not title or not title.strip():
            raise ValidationError("El titulo no puede estar vacio")
        title = title.strip()
        if len(title) > TITLE_MAX_LENGTH:
            raise ValidationError(f"El titulo no puede exceder {TITLE_MAX_LENGTH} caracteres")
        return title
