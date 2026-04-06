from flask import Blueprint, request, jsonify
from backend.src.services.task_service import TaskService, ValidationError, TaskNotFoundError

task_blueprint = Blueprint('tasks', __name__)
task_service = TaskService()


@task_blueprint.route('/tasks', methods=['GET'])
def get_tasks():
    """Endpoint para obtener todas las tareas."""
    filter_type = request.args.get('filter', 'all')
    if filter_type == 'pending':
        tasks = task_service.get_pending_tasks()
    else:
        tasks = task_service.get_all_tasks()
    return jsonify([task.to_dict() for task in tasks]), 200


@task_blueprint.route('/tasks', methods=['POST'])
def create_task():
    """Endpoint para crear una nueva tarea."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Se requiere un cuerpo JSON"}), 400
    try:
        task = task_service.create_task(
            title=data.get('title', ''),
            description=data.get('description', '')
        )
        return jsonify(task.to_dict()), 201
    except ValidationError as error:
        return jsonify({"error": str(error)}), 400


@task_blueprint.route('/tasks/<int:task_id>/complete', methods=['PATCH'])
def complete_task(task_id):
    """Endpoint para marcar una tarea como completada."""
    try:
        task = task_service.complete_task(task_id)
        return jsonify(task.to_dict()), 200
    except TaskNotFoundError as error:
        return jsonify({"error": str(error)}), 404


@task_blueprint.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Endpoint para eliminar una tarea."""
    try:
        task_service.delete_task(task_id)
        return jsonify({"message": "Tarea eliminada correctamente"}), 200
    except TaskNotFoundError as error:
        return jsonify({"error": str(error)}), 404
