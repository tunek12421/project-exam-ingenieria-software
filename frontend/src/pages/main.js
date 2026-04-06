const expandedLists = new Set();
const openSubtaskForms = new Set();

document.addEventListener('DOMContentLoaded', () => {
    loadTaskLists();
});

async function loadTaskLists() {
    const container = document.getElementById('task-lists-container');
    try {
        const lists = await ApiService.fetchTaskLists();
        container.innerHTML = '';
        if (lists.length === 0) {
            container.innerHTML = '<div class="empty-state">No hay listas de tareas. Crea una con + New</div>';
            return;
        }
        lists.forEach(list => {
            container.appendChild(createTaskListCard(list));
            // Restaurar paneles abiertos
            if (expandedLists.has(list.id)) {
                document.getElementById(`subtasks-${list.id}`).classList.add('open');
                const btn = document.querySelector(`#list-${list.id} .btn-expand`);
                if (btn) btn.classList.add('expanded');
            }
            if (openSubtaskForms.has(list.id)) {
                document.getElementById(`add-subtask-${list.id}`).classList.add('open');
            }
        });
    } catch (error) {
        container.innerHTML = '<div class="empty-state">Error al cargar las listas</div>';
    }
}

// --- List Form ---
function toggleListForm() {
    const form = document.getElementById('list-form');
    form.classList.toggle('hidden');
    if (!form.classList.contains('hidden')) {
        document.getElementById('input-list-title').focus();
    }
}

async function handleCreateList(event) {
    event.preventDefault();
    const titleInput = document.getElementById('input-list-title');
    const descInput = document.getElementById('input-list-desc');
    const title = titleInput.value.trim();
    const description = descInput.value.trim();

    if (!title) {
        alert('El titulo no puede estar vacio');
        return;
    }

    try {
        await ApiService.createTaskList(title, description);
        titleInput.value = '';
        descInput.value = '';
        toggleListForm();
        showNotification('Lista creada');
        loadTaskLists();
    } catch (error) {
        alert(error.message);
    }
}

async function handleDeleteList(listId) {
    if (!confirm('Eliminar esta lista y todas sus subtareas?')) return;
    try {
        await ApiService.deleteTaskList(listId);
        expandedLists.delete(listId);
        openSubtaskForms.delete(listId);
        showNotification('Lista eliminada');
        loadTaskLists();
    } catch (error) {
        alert('Error al eliminar la lista');
    }
}

// --- Expand / Collapse ---
function toggleExpand(listId, button) {
    const panel = document.getElementById(`subtasks-${listId}`);
    panel.classList.toggle('open');
    button.classList.toggle('expanded');

    if (expandedLists.has(listId)) {
        expandedLists.delete(listId);
    } else {
        expandedLists.add(listId);
    }
}

// --- Subtasks ---
function toggleAddSubtask(listId) {
    const form = document.getElementById(`add-subtask-${listId}`);
    form.classList.toggle('open');

    if (openSubtaskForms.has(listId)) {
        openSubtaskForms.delete(listId);
    } else {
        openSubtaskForms.add(listId);
        document.getElementById(`input-subtask-${listId}`).focus();
    }
}

async function handleAddSubtask(listId) {
    const input = document.getElementById(`input-subtask-${listId}`);
    const title = input.value.trim();
    if (!title) {
        alert('El nombre de la subtarea no puede estar vacio');
        return;
    }

    try {
        await ApiService.addSubtask(listId, title);
        input.value = '';
        openSubtaskForms.delete(listId);
        showNotification('Subtarea agregada');
        loadTaskLists();
    } catch (error) {
        alert(error.message);
    }
}

async function handleToggleSubtask(subtaskId) {
    try {
        await ApiService.toggleSubtask(subtaskId);
        loadTaskLists();
    } catch (error) {
        alert('Error al cambiar estado de la subtarea');
    }
}

async function handleDeleteSubtask(subtaskId) {
    try {
        await ApiService.deleteSubtask(subtaskId);
        showNotification('Subtarea eliminada');
        loadTaskLists();
    } catch (error) {
        alert('Error al eliminar la subtarea');
    }
}

// --- Notification ---
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 2500);
}
