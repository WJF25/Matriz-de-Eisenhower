from flask import request, jsonify, current_app
from app.controllers.verifications import limitation, verify_keys
from app.models.tasks_model import TaskModel
from app.models.categories_model import CategoriesModel
from app.models.eisenhowers_model import EisenhowerModel


def create_task():
    session = current_app.db.session
    data = request.get_json()
    option = limitation(data)
    eisen = session.query(EisenhowerModel).filter_by(eisen_type=option).first()
    

    category = data.pop('categories')
    
    for categ in category:
        
        a = session.query(CategoriesModel).filter_by(cat_name=categ['cat_name']).first()
        
        if a is None:
            session.add(CategoriesModel(**categ))
            session.commit()

    data['eisenhower_id'] = eisen.eisenhower_id
    task = TaskModel(**data)
    session.add(task)
    session.commit()
    resp = dict(task)
    resp['eisenhower_classification'] = eisen.eisen_type
    resp['category'] = category
    
    del resp['importance']
    del resp['urgency']

    return jsonify(resp), 201


def update_tasks(task_id):
    session = current_app.db.session
    data = request.get_json()
    verify_keys(data,"task","patch")
    limitation(data, "patch")
    old = TaskModel.query.get(task_id)

    resp = dict(old)
    resp.update(data)
    updated = session.query(TaskModel).filter_by(task_id=task_id).update(resp)
    session.commit()  
    
    new_updated = session.query(TaskModel).filter_by(task_id=task_id).first()

    new_resp = dict(new_updated)
    
    new_eisen = limitation(new_resp)

    new_date = session.query(EisenhowerModel).filter_by(eisen_type=new_eisen).first()

    new_resp['eisenhower_classification'] = new_date.eisen_type
    del new_resp['importance']
    del new_resp['urgency']
    return jsonify(new_resp), 200



def delete_task(task_id):
    session = current_app.db.session
    task = TaskModel.query.get_or_404(task_id)
    session.delete(task)
    session.commit()
    return jsonify({"message": "Task deleted"}), 204