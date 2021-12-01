from flask import Blueprint
from app.controllers.tasks_controller import create_task, update_tasks, delete_task

bp = Blueprint('tasks', __name__, url_prefix='/task')

bp.post("")(create_task)
bp.patch("/<int:task_id>")(update_tasks)
bp.delete("/<int:task_id>")(delete_task)