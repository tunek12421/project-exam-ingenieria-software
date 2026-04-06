from backend.src.config.database import TITLE_MAX_LENGTH
from backend.src.models.task_model import Task
from backend.src.repositories.task_repository import TaskRepository


class ValidationError(Exception):
    """Error lanzado cuando los datos de entrada no son validos."""
    pass


class TaskNotFoundError(Exception):
    """Error lanzado cuando no se encuentra una tarea."""
    pass


class TaskService:
    """Capa de logica de negocio para la gestion de tareas."""

    def __init__(self, repository=None):
        self.repository = repository or TaskRepository()

    def get_all_tasks(self):
        """Retorna todas las tareas."""
        return self.repository.find_all()

    def get_pending_tasks(self):
        """Retorna solo las tareas pendientes."""
        return self.repository.find_pending()

    def create_task(self, title, description=""):
        """Crea una nueva tarea validando los datos de entrada."""
        title = self._validate_title(title)
        description = description.strip() if description else ""

        task = Task(title=title, description=description)
        return self.repository.create(task)

    def complete_task(self, task_id):
        """Marca una tarea como completada."""
        task = self._find_task_or_raise(task_id)
        self.repository.update_status(task_id, True)
        task.is_completed = True
        return task

    def delete_task(self, task_id):
        """Elimina una tarea por su ID."""
        self._find_task_or_raise(task_id)
        self.repository.delete(task_id)

    def _find_task_or_raise(self, task_id):
        """Busca una tarea o lanza TaskNotFoundError si no existe."""
        task = self.repository.find_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"No se encontro la tarea con ID {task_id}")
        return task

    def _validate_title(self, title):
        """Valida que el titulo no este vacio ni sea demasiado largo."""
        if not title or not title.strip():
            raise ValidationError("El titulo de la tarea no puede estar vacio")
        title = title.strip()
        if len(title) > TITLE_MAX_LENGTH:
            raise ValidationError(f"El titulo no puede exceder {TITLE_MAX_LENGTH} caracteres")
        return title
