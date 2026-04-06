const API_BASE_URL = '/api';

const ApiService = {
    // --- Task Lists ---
    async fetchTaskLists() {
        const response = await fetch(`${API_BASE_URL}/task-lists`);
        if (!response.ok) throw new Error('Error al obtener listas');
        return response.json();
    },

    async createTaskList(title, description) {
        const response = await fetch(`${API_BASE_URL}/task-lists`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, description })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Error al crear lista');
        return data;
    },

    async deleteTaskList(listId) {
        const response = await fetch(`${API_BASE_URL}/task-lists/${listId}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Error al eliminar lista');
        return response.json();
    },

    // --- Subtasks ---
    async addSubtask(listId, title) {
        const response = await fetch(`${API_BASE_URL}/task-lists/${listId}/subtasks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Error al crear subtarea');
        return data;
    },

    async toggleSubtask(subtaskId) {
        const response = await fetch(`${API_BASE_URL}/subtasks/${subtaskId}/toggle`, {
            method: 'PATCH'
        });
        if (!response.ok) throw new Error('Error al cambiar estado');
        return response.json();
    },

    async deleteSubtask(subtaskId) {
        const response = await fetch(`${API_BASE_URL}/subtasks/${subtaskId}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Error al eliminar subtarea');
        return response.json();
    }
};
