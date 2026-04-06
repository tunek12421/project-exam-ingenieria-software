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
    const titleInput = document.getElementById('input-title');
    const descInput = document.getElementById('input-description');
    const title = titleInput.value.trim();
    const description = descInput.value.trim();

    if (!title) {
        alert('El titulo no puede estar vacio');
        return;
    }

    try {
        await ApiService.createTask(title, description);
        titleInput.value = '';
        descInput.value = '';
        toggleForm();
        showNotification('Tarea creada correctamente');
        loadTasks();
    } catch (error) {
        alert(error.message);
    }
}

async function handleCompleteTask(taskId) {
    try {
        await ApiService.completeTask(taskId);
        showNotification('Tarea completada');
        loadTasks();
    } catch (error) {
        alert('Error al completar la tarea');
    }
}

async function handleDeleteTask(taskId) {
    if (!confirm('Eliminar esta tarea?')) return;
    try {
        await ApiService.deleteTask(taskId);
        showNotification('Tarea eliminada');
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

function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 2500);
}
