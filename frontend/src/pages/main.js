let currentFilter = 'all';

document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
});

async function loadTasks() {
    const taskList = document.getElementById('task-list');
    try {
        const tasks = await ApiService.fetchTasks(currentFilter);
        taskList.innerHTML = '';
        if (tasks.length === 0) {
            taskList.innerHTML = '<div class="empty-state">No hay tareas para mostrar</div>';
            return;
        }
        tasks.forEach(task => {
            taskList.appendChild(createTaskCard(task));
        });
    } catch (error) {
        taskList.innerHTML = '<div class="empty-state">Error al cargar las tareas</div>';
    }
}

function toggleForm() {
    const form = document.getElementById('task-form');
    form.classList.toggle('hidden');
    if (!form.classList.contains('hidden')) {
        document.getElementById('input-title').focus();
    }
}

async function handleCreateTask(event) {
    event.preventDefault();
    const title = document.getElementById('input-title').value;
    const description = document.getElementById('input-description').value;
    try {
        await ApiService.createTask(title, description);
        document.getElementById('input-title').value = '';
        document.getElementById('input-description').value = '';
        toggleForm();
        loadTasks();
    } catch (error) {
        alert(error.message);
    }
}

async function handleCompleteTask(taskId) {
    try {
        await ApiService.completeTask(taskId);
        loadTasks();
    } catch (error) {
        alert('Error al completar la tarea');
    }
}

async function handleDeleteTask(taskId) {
    if (!confirm('¿Eliminar esta tarea?')) return;
    try {
        await ApiService.deleteTask(taskId);
        loadTasks();
    } catch (error) {
        alert('Error al eliminar la tarea');
    }
}

function filterTasks(filter, button) {
    currentFilter = filter;
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');
    loadTasks();
}
