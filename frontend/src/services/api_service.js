const API_BASE_URL = '/api';

const ApiService = {
    async fetchTasks(filter = 'all') {
        const response = await fetch(`${API_BASE_URL}/tasks?filter=${filter}`);
        if (!response.ok) throw new Error('Error al obtener tareas');
        return response.json();
    },

    async createTask(title, description) {
        const response = await fetch(`${API_BASE_URL}/tasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, description })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Error al crear tarea');
        return data;
    },

    async completeTask(taskId) {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/complete`, {
            method: 'PATCH'
        });
        if (!response.ok) throw new Error('Error al completar tarea');
        return response.json();
    },

    async deleteTask(taskId) {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Error al eliminar tarea');
        return response.json();
    }
};
