from flask import request, jsonify, current_app
import sqlalchemy 
import psycopg2
from app.controllers.verifications import WrongKeyError, WrongOptionError, limitation, verify_keys
from app.models.tasks_model import TaskModel
from app.models.categories_model import CategoriesModel
from app.models.eisenhowers_model import EisenhowerModel


def create_task():
    try:
        session = current_app.db.session
        data = request.get_json()
        verify_keys(data,"task","post")
        option = limitation(data)    
    except WrongKeyError as e:
        return jsonify(e.value), 400
    except WrongOptionError as f:
        return jsonify(f.value), 404
    eisen = session.query(EisenhowerModel).filter_by(eisen_type=option).first()
    

    category = data.pop('categories')
    
    

    data['eisenhower_id'] = eisen.eisenhower_id

    try:
        task = TaskModel(**data)
        
        session.add(task)
        session.commit()
    except (sqlalchemy.exc.IntegrityError ) as er:
        if type(er.orig) == psycopg2.errors.UniqueViolation:
            return jsonify({"error": "Task already exists"}), 409

    for categ in category:
        
        a = session.query(CategoriesModel).filter_by(cat_name=categ['cat_name']).first()        
        if a is None:
            new_cag = CategoriesModel(**categ)
            new_cag.tasks.append(task)
            session.add(new_cag)
            session.commit()
        else:
            a.tasks.append(task)
            t = dict(a)
            session.query(CategoriesModel).filter_by(cat_name=categ['cat_name']).update(t)
            session.commit()
    
    resp = dict(task)
    resp['eisenhower_classification'] = eisen.eisen_type
    resp['category'] = category
    
    del resp['importance']
    del resp['urgency']

    return jsonify(resp), 201


def update_tasks(task_id):
    try:
        session = current_app.db.session
        data = request.get_json()
        verify_keys(data,"task","patch")
        limitation(data, "patch")
    except WrongKeyError as e:
        return jsonify(e.value), 400
    except WrongOptionError as f:
        return jsonify(f.value), 404

    try:
        old = TaskModel.query.get(task_id)
        resp = dict(old)
        resp.update(data)

        updated = session.query(TaskModel).filter_by(task_id=task_id).update(resp)
        session.commit()  
    except TypeError as e:
        return jsonify({"error": "Task not found"}), 404
    
    new_updated = session.query(TaskModel).filter_by(task_id=task_id).first()

    new_resp = dict(new_updated)
    
    new_eisen = limitation(new_resp)

    new_date = session.query(EisenhowerModel).filter_by(eisen_type=new_eisen).first()

    session.query(TaskModel).filter_by(task_id=task_id).update({"eisenhower_id": new_date.eisenhower_id})
    session.commit()
    
    new_resp['eisenhower_classification'] = new_date.eisen_type
    del new_resp['importance']
    del new_resp['urgency']
    return jsonify(new_resp), 200



def delete_task(task_id):
    session = current_app.db.session
    task = TaskModel.query.get(task_id)
    if task is None:
        return jsonify({"error": "TaskCategory not found"}), 404
    session.delete(task)
    session.commit()
    return jsonify({"message": "Task deleted"}), 204