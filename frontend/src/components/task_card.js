function createProgressCircle(progress) {
    const radius = 22;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (progress / 100) * circumference;

    return `
        <div class="progress-circle">
            <svg viewBox="0 0 52 52">
                <circle class="bg" cx="26" cy="26" r="${radius}"/>
                <circle class="fg" cx="26" cy="26" r="${radius}"
                    stroke-dasharray="${circumference}"
                    stroke-dashoffset="${offset}"/>
            </svg>
            <span class="progress-text">${progress}%</span>
        </div>
    `;
}

function createSubtaskItem(subtask) {
    const completedClass = subtask.is_completed ? 'completed' : '';
    const checkmark = subtask.is_completed ? '&#10003;' : '';

    return `
        <div class="subtask-item ${completedClass}">
            <div class="subtask-checkbox" onclick="handleToggleSubtask(${subtask.id})">
                ${checkmark}
            </div>
            <span class="subtask-title">${escapeHtml(subtask.title)}</span>
            <button class="subtask-delete" onclick="handleDeleteSubtask(${subtask.id})">&#128465;</button>
        </div>
    `;
}

function createTaskListCard(taskList) {
    const card = document.createElement('div');
    card.className = 'task-list-card';
    card.id = `list-${taskList.id}`;

    const subtasksHtml = taskList.subtasks.length > 0
        ? taskList.subtasks.map(s => createSubtaskItem(s)).join('')
        : '<div class="subtasks-empty">No hay subtareas</div>';

    card.innerHTML = `
        <div class="task-list-header">
            ${createProgressCircle(taskList.progress)}
            <div class="task-list-info">
                <div class="task-list-title">${escapeHtml(taskList.title)}</div>
                ${taskList.description ? `<div class="task-list-desc">${escapeHtml(taskList.description)}</div>` : ''}
            </div>
            <div class="task-list-actions">
                <button class="btn-icon btn-delete" onclick="handleDeleteList(${taskList.id})" title="Eliminar lista">&#128465;</button>
                <button class="btn-icon btn-expand" onclick="toggleExpand(${taskList.id}, this)" title="Expandir">&#8744;&#8744;</button>
                <button class="btn-icon btn-add-subtask" onclick="toggleAddSubtask(${taskList.id})" title="Agregar subtarea">+</button>
            </div>
        </div>
        <div class="subtasks-panel" id="subtasks-${taskList.id}">
            ${subtasksHtml}
        </div>
        <div class="add-subtask-inline" id="add-subtask-${taskList.id}">
            <input type="text" id="input-subtask-${taskList.id}" placeholder="Nombre de la subtarea" maxlength="200"
                onkeydown="if(event.key==='Enter'){handleAddSubtask(${taskList.id});event.preventDefault();}">
            <button class="btn-save" onclick="handleAddSubtask(${taskList.id})">Agregar</button>
        </div>
    `;

    return card;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
