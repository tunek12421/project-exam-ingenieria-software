import unittest
from unittest.mock import MagicMock
from backend.src.services.task_service import TaskService, ValidationError, TaskNotFoundError
from backend.src.models.task_model import Task


class TestTaskService(unittest.TestCase):
    """Pruebas unitarias para la capa de servicio de tareas."""

    def setUp(self):
        """Configura un repositorio mock antes de cada prueba."""
        self.mock_repository = MagicMock()
        self.service = TaskService(repository=self.mock_repository)

    def test_create_task_with_valid_data(self):
        """Verifica que se crea una tarea correctamente con datos validos."""
        self.mock_repository.create.return_value = Task(
            id=1, title="Tarea de prueba", description="Descripcion"
        )
        task = self.service.create_task("Tarea de prueba", "Descripcion")

        self.assertEqual(task.title, "Tarea de prueba")
        self.assertEqual(task.id, 1)
        self.mock_repository.create.assert_called_once()

    def test_create_task_with_empty_title_raises_error(self):
        """Verifica que no se puede crear una tarea sin titulo."""
        with self.assertRaises(ValidationError) as context:
            self.service.create_task("", "Descripcion")
        self.assertIn("vacio", str(context.exception))

    def test_create_task_with_whitespace_title_raises_error(self):
        """Verifica que un titulo con solo espacios es rechazado."""
        with self.assertRaises(ValidationError):
            self.service.create_task("   ", "Descripcion")

    def test_create_task_with_long_title_raises_error(self):
        """Verifica que un titulo mayor a 200 caracteres es rechazado."""
        long_title = "A" * 201
        with self.assertRaises(ValidationError) as context:
            self.service.create_task(long_title)
        self.assertIn("200 caracteres", str(context.exception))

    def test_complete_task_success(self):
        """Verifica que se puede completar una tarea existente."""
        existing_task = Task(id=1, title="Tarea", is_completed=False)
        self.mock_repository.find_by_id.return_value = existing_task

        result = self.service.complete_task(1)

        self.assertTrue(result.is_completed)
        self.mock_repository.update_status.assert_called_once_with(1, True)

    def test_complete_nonexistent_task_raises_error(self):
        """Verifica que completar una tarea inexistente lanza error."""
        self.mock_repository.find_by_id.return_value = None

        with self.assertRaises(TaskNotFoundError):
            self.service.complete_task(999)

    def test_delete_nonexistent_task_raises_error(self):
        """Verifica que eliminar una tarea inexistente lanza error."""
        self.mock_repository.find_by_id.return_value = None

        with self.assertRaises(TaskNotFoundError):
            self.service.delete_task(999)

    def test_get_all_tasks(self):
        """Verifica que se obtienen todas las tareas."""
        self.mock_repository.find_all.return_value = [
            Task(id=1, title="Tarea 1"),
            Task(id=2, title="Tarea 2")
        ]
        tasks = self.service.get_all_tasks()

        self.assertEqual(len(tasks), 2)
        self.mock_repository.find_all.assert_called_once()


if __name__ == '__main__':
    unittest.main()
