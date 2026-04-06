import unittest
from unittest.mock import MagicMock
from backend.src.services.task_service import TaskService, ValidationError, TaskNotFoundError
from backend.src.models.task_model import TaskList, Subtask


class TestTaskService(unittest.TestCase):
    """Pruebas unitarias para la capa de servicio de listas de tareas."""

    def setUp(self):
        self.mock_repository = MagicMock()
        self.service = TaskService(repository=self.mock_repository)

    # --- Task Lists ---

    def test_create_list_with_valid_data(self):
        """Verifica que se crea una lista correctamente con datos validos."""
        self.mock_repository.create_list.return_value = TaskList(
            id=1, title="Lista de prueba", description="Descripcion"
        )
        result = self.service.create_list("Lista de prueba", "Descripcion")
        self.assertEqual(result.title, "Lista de prueba")
        self.assertEqual(result.id, 1)
        self.mock_repository.create_list.assert_called_once()

    def test_create_list_with_empty_title_raises_error(self):
        """Verifica que no se puede crear una lista sin titulo."""
        with self.assertRaises(ValidationError) as ctx:
            self.service.create_list("", "Descripcion")
        self.assertIn("vacio", str(ctx.exception))

    def test_create_list_with_whitespace_title_raises_error(self):
        """Verifica que un titulo con solo espacios es rechazado."""
        with self.assertRaises(ValidationError):
            self.service.create_list("   ")

    def test_create_list_with_long_title_raises_error(self):
        """Verifica que un titulo mayor a 200 caracteres es rechazado."""
        with self.assertRaises(ValidationError) as ctx:
            self.service.create_list("A" * 201)
        self.assertIn("200", str(ctx.exception))

    def test_delete_list_success(self):
        """Verifica que se puede eliminar una lista existente."""
        self.mock_repository.find_list_by_id.return_value = TaskList(id=1, title="Test")
        self.service.delete_list(1)
        self.mock_repository.delete_list.assert_called_once_with(1)

    def test_delete_nonexistent_list_raises_error(self):
        """Verifica que eliminar una lista inexistente lanza error."""
        self.mock_repository.find_list_by_id.return_value = None
        with self.assertRaises(TaskNotFoundError):
            self.service.delete_list(999)

    # --- Subtasks ---

    def test_add_subtask_to_existing_list(self):
        """Verifica que se puede agregar una subtarea a una lista existente."""
        self.mock_repository.find_list_by_id.return_value = TaskList(id=1, title="Test")
        self.mock_repository.create_subtask.return_value = Subtask(
            id=1, task_list_id=1, title="Subtarea"
        )
        result = self.service.add_subtask(1, "Subtarea")
        self.assertEqual(result.title, "Subtarea")
        self.assertEqual(result.task_list_id, 1)

    def test_add_subtask_to_nonexistent_list_raises_error(self):
        """Verifica que agregar subtarea a lista inexistente lanza error."""
        self.mock_repository.find_list_by_id.return_value = None
        with self.assertRaises(TaskNotFoundError):
            self.service.add_subtask(999, "Subtarea")

    def test_toggle_subtask_from_pending_to_completed(self):
        """Verifica que se puede marcar una subtarea como completada."""
        self.mock_repository.find_subtask_by_id.return_value = Subtask(
            id=1, task_list_id=1, title="Sub", is_completed=False
        )
        result = self.service.toggle_subtask(1)
        self.assertTrue(result.is_completed)
        self.mock_repository.toggle_subtask.assert_called_once_with(1, True)

    def test_toggle_subtask_from_completed_to_pending(self):
        """Verifica que se puede desmarcar una subtarea completada (destiquear)."""
        self.mock_repository.find_subtask_by_id.return_value = Subtask(
            id=1, task_list_id=1, title="Sub", is_completed=True
        )
        result = self.service.toggle_subtask(1)
        self.assertFalse(result.is_completed)
        self.mock_repository.toggle_subtask.assert_called_once_with(1, False)

    def test_toggle_nonexistent_subtask_raises_error(self):
        """Verifica que toggle en subtarea inexistente lanza error."""
        self.mock_repository.find_subtask_by_id.return_value = None
        with self.assertRaises(TaskNotFoundError):
            self.service.toggle_subtask(999)

    def test_get_all_lists(self):
        """Verifica que se obtienen todas las listas."""
        self.mock_repository.find_all_lists.return_value = [
            TaskList(id=1, title="Lista 1"),
            TaskList(id=2, title="Lista 2")
        ]
        lists = self.service.get_all_lists()
        self.assertEqual(len(lists), 2)
        self.mock_repository.find_all_lists.assert_called_once()


class TestTaskListProgress(unittest.TestCase):
    """Pruebas para el calculo de progreso de una lista."""

    def test_progress_with_no_subtasks(self):
        """Lista sin subtareas tiene 0% de progreso."""
        task_list = TaskList(id=1, title="Test", subtasks=[])
        self.assertEqual(task_list.progress, 0)

    def test_progress_with_all_completed(self):
        """Lista con todas las subtareas completadas tiene 100%."""
        task_list = TaskList(id=1, title="Test", subtasks=[
            Subtask(id=1, title="A", is_completed=True),
            Subtask(id=2, title="B", is_completed=True),
        ])
        self.assertEqual(task_list.progress, 100)

    def test_progress_with_partial_completion(self):
        """Lista con 1 de 4 completadas tiene 25%."""
        task_list = TaskList(id=1, title="Test", subtasks=[
            Subtask(id=1, title="A", is_completed=True),
            Subtask(id=2, title="B", is_completed=False),
            Subtask(id=3, title="C", is_completed=False),
            Subtask(id=4, title="D", is_completed=False),
        ])
        self.assertEqual(task_list.progress, 25)


if __name__ == '__main__':
    unittest.main()
