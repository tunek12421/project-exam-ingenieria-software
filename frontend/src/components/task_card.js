function createTaskCard(task) {
    const card = document.createElement('div');
    card.className = `task-card ${task.is_completed ? 'completed' : ''}`;
    card.innerHTML = `
        <div class="task-checkbox" onclick="handleCompleteTask(${task.id})">
            ${task.is_completed ? '&#10003;' : ''}
        </div>
        <div class="task-info">
            <div class="task-title">${escapeHtml(task.title)}</div>
            ${task.description ? `<div class="task-description">${escapeHtml(task.description)}</div>` : ''}
        </div>
        <button class="task-delete" onclick="handleDeleteTask(${task.id})">&#128465;</button>
    `;
    return card;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
