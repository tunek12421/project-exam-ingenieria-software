import unittest
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.src.main import create_app


class TestTaskListAPIIntegration(unittest.TestCase):
    """Pruebas de integracion para la API de listas de tareas y subtareas."""

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def _create_list(self, title="Test List", description="Desc"):
        response = self.client.post('/api/task-lists',
            data=json.dumps({"title": title, "description": description}),
            content_type='application/json'
        )
        return json.loads(response.data)

    def test_create_and_list_task_lists(self):
        """Verifica crear una lista y obtenerla en el listado."""
        data = self._create_list("Mi lista")
        self.assertEqual(data['title'], "Mi lista")
        self.assertEqual(data['progress'], 0)

        response = self.client.get('/api/task-lists')
        self.assertEqual(response.status_code, 200)
        lists = json.loads(response.data)
        self.assertTrue(any(l['title'] == "Mi lista" for l in lists))

    def test_create_list_without_title_returns_400(self):
        """Crear lista sin titulo retorna error 400."""
        response = self.client.post('/api/task-lists',
            data=json.dumps({"title": ""}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_add_subtask_and_verify_progress(self):
        """Agregar subtareas y verificar calculo de progreso."""
        task_list = self._create_list("Lista con subtareas")
        list_id = task_list['id']

        self.client.post(f'/api/task-lists/{list_id}/subtasks',
            data=json.dumps({"title": "Subtarea 1"}),
            content_type='application/json'
        )
        self.client.post(f'/api/task-lists/{list_id}/subtasks',
            data=json.dumps({"title": "Subtarea 2"}),
            content_type='application/json'
        )

        response = self.client.get('/api/task-lists')
        lists = json.loads(response.data)
        target = next(l for l in lists if l['id'] == list_id)
        self.assertEqual(len(target['subtasks']), 2)
        self.assertEqual(target['progress'], 0)

    def test_toggle_subtask_check_and_uncheck(self):
        """Verificar que se puede marcar y desmarcar una subtarea (toggle)."""
        task_list = self._create_list("Toggle test")
        list_id = task_list['id']

        resp = self.client.post(f'/api/task-lists/{list_id}/subtasks',
            data=json.dumps({"title": "Toggle subtask"}),
            content_type='application/json'
        )
        subtask = json.loads(resp.data)
        subtask_id = subtask['id']
        self.assertFalse(subtask['is_completed'])

        # Marcar como completada
        resp = self.client.patch(f'/api/subtasks/{subtask_id}/toggle')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertTrue(data['is_completed'])

        # Desmarcar (destiquear)
        resp = self.client.patch(f'/api/subtasks/{subtask_id}/toggle')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertFalse(data['is_completed'])

    def test_delete_list_cascades_subtasks(self):
        """Verificar que eliminar lista elimina sus subtareas."""
        task_list = self._create_list("Para eliminar")
        list_id = task_list['id']

        self.client.post(f'/api/task-lists/{list_id}/subtasks',
            data=json.dumps({"title": "Sub"}),
            content_type='application/json'
        )

        response = self.client.delete(f'/api/task-lists/{list_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_nonexistent_list_returns_404(self):
        """Eliminar lista inexistente retorna 404."""
        response = self.client.delete('/api/task-lists/99999')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
