from flask import Blueprint, request, jsonify
from backend.src.services.task_service import TaskService, ValidationError, TaskNotFoundError

task_blueprint = Blueprint('tasks', __name__)
task_service = TaskService()


@task_blueprint.route('/task-lists', methods=['GET'])
def get_task_lists():
    """Obtiene todas las listas de tareas con subtareas y progreso."""
    task_lists = task_service.get_all_lists()
    return jsonify([tl.to_dict() for tl in task_lists]), 200


@task_blueprint.route('/task-lists', methods=['POST'])
def create_task_list():
    """Crea una nueva lista de tareas."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Se requiere un cuerpo JSON"}), 400
    try:
        task_list = task_service.create_list(
            title=data.get('title', ''),
            description=data.get('description', '')
        )
        return jsonify(task_list.to_dict()), 201
    except ValidationError as error:
        return jsonify({"error": str(error)}), 400


@task_blueprint.route('/task-lists/<int:list_id>', methods=['DELETE'])
def delete_task_list(list_id):
    """Elimina una lista de tareas y sus subtareas."""
    try:
        task_service.delete_list(list_id)
        return jsonify({"message": "Lista eliminada correctamente"}), 200
    except TaskNotFoundError as error:
        return jsonify({"error": str(error)}), 404


@task_blueprint.route('/task-lists/<int:list_id>/subtasks', methods=['POST'])
def add_subtask(list_id):
    """Agrega una subtarea a una lista."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Se requiere un cuerpo JSON"}), 400
    try:
        subtask = task_service.add_subtask(
            list_id=list_id,
            title=data.get('title', '')
        )
        return jsonify(subtask.to_dict()), 201
    except ValidationError as error:
        return jsonify({"error": str(error)}), 400
    except TaskNotFoundError as error:
        return jsonify({"error": str(error)}), 404


@task_blueprint.route('/subtasks/<int:subtask_id>/toggle', methods=['PATCH'])
def toggle_subtask(subtask_id):
    """Alterna el estado de una subtarea (completada/pendiente)."""
    try:
        subtask = task_service.toggle_subtask(subtask_id)
        return jsonify(subtask.to_dict()), 200
    except TaskNotFoundError as error:
        return jsonify({"error": str(error)}), 404


@task_blueprint.route('/subtasks/<int:subtask_id>', methods=['DELETE'])
def delete_subtask(subtask_id):
    """Elimina una subtarea."""
    try:
        task_service.delete_subtask(subtask_id)
        return jsonify({"message": "Subtarea eliminada correctamente"}), 200
    except TaskNotFoundError as error:
        return jsonify({"error": str(error)}), 404
