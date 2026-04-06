import unittest
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.src.main import create_app


class TestTaskAPIIntegration(unittest.TestCase):
    """Pruebas de integracion para los endpoints de la API de tareas."""

    def setUp(self):
        """Configura la aplicacion de prueba con una base de datos temporal."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_create_and_list_tasks(self):
        """Verifica el flujo completo: crear una tarea y luego listarla."""
        response = self.client.post('/api/tasks',
            data=json.dumps({"title": "Tarea integracion", "description": "Test"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], "Tarea integracion")
        self.assertFalse(data['is_completed'])

        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        tasks = json.loads(response.data)
        self.assertTrue(any(t['title'] == "Tarea integracion" for t in tasks))

    def test_create_task_without_title_returns_400(self):
        """Verifica que crear una tarea sin titulo retorna error 400."""
        response = self.client.post('/api/tasks',
            data=json.dumps({"title": "", "description": "Sin titulo"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_complete_task_flow(self):
        """Verifica el flujo de crear y luego completar una tarea."""
        response = self.client.post('/api/tasks',
            data=json.dumps({"title": "Tarea para completar"}),
            content_type='application/json'
        )
        task_id = json.loads(response.data)['id']

        response = self.client.patch(f'/api/tasks/{task_id}/complete')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['is_completed'])

    def test_delete_nonexistent_task_returns_404(self):
        """Verifica que eliminar una tarea inexistente retorna 404."""
        response = self.client.delete('/api/tasks/99999')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
