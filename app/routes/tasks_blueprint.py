from flask import Blueprint
from app.controllers.tasks_controller import create_task, update_tasks, delete_task, get_tasks, get_task_by_id, get_task_by_name_or_descrip

bp = Blueprint('tasks', __name__, url_prefix='/task')

bp.post("")(create_task)
bp.patch("/<int:task_id>")(update_tasks)
bp.delete("/<int:task_id>")(delete_task)
bp.get("")(get_tasks)
bp.get("/<int:task_id>")(get_task_by_id)
bp.get("/<string:name_or_descrip>")(get_task_by_name_or_descrip)