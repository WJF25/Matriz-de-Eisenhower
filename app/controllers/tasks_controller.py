from flask import request, jsonify, current_app
import sqlalchemy 
import psycopg2
from app.controllers.verifications import WrongKeyError, WrongOptionError, limitation, verify_keys
from app.models.tasks_model import TaskModel
from app.models.categories_model import CategoriesModel
from app.models.eisenhowers_model import EisenhowerModel
from app.models.tasks_categories_table import tasks_categories_table
from sqlalchemy import asc, desc


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
    eisen = session.query(EisenhowerModel).filter_by(type=option).first()
    

    category = data.pop('categories')
    
    

    data['eisenhower_id'] = eisen.id if eisen.id else 1

    try:
        task = TaskModel(**data)
        
        session.add(task)
        session.commit()
    except (sqlalchemy.exc.IntegrityError ) as er:
        if type(er.orig) == psycopg2.errors.UniqueViolation:
            return jsonify({"error": "Task already exists"}), 409

    for categ in category:
        
        a = session.query(CategoriesModel).filter_by(name=categ['name']).first()
        
        if a is None:
            new_cag = CategoriesModel(**categ)
            new_cag.tasks.append(task)
            session.add(new_cag)
            session.commit()
        else:
            
            a.tasks.append(task)
            session.add(a)            
            session.commit()
        
            
    
    resp = dict(task)
    resp['eisenhower_classification'] = eisen.type
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

        if data.get('categories', None):
            categories = data.pop('categories')
            
            for categ in categories:
                category: CategoriesModel = session.query(CategoriesModel).filter_by(name=categ['name']).first()
                if category is None:
                    new_cag = CategoriesModel(**categ)
                    new_cag.tasks.append(old)
                    session.add(new_cag)
                    session.commit()
                else:                    
                        
                    category.tasks.append(old)
                    session.add(category)
                    session.commit()
                
        resp.update(data)
        

        updated = session.query(TaskModel).filter_by(id=task_id).update(resp)
        session.commit()  
    except TypeError as e:
        print(str(e))
        return jsonify({"error": "Task not found"}), 404
    
    new_updated = session.query(TaskModel).filter_by(id=task_id).first()

    new_resp = dict(new_updated)
    
    new_eisen = limitation(new_resp)

    new_date = session.query(EisenhowerModel).filter_by(type=new_eisen).first()

    session.query(TaskModel).filter_by(id=task_id).update({"eisenhower_id": new_date.id})
    session.commit()
    
    new_resp['eisenhower_classification'] = new_date.type
    del new_resp['importance']
    del new_resp['urgency']
    tasky_id = tasks_categories_table.columns.get('task_id')
    category_task = CategoriesModel.query.select_from(tasks_categories_table).join(CategoriesModel).filter(tasky_id == task_id).all()
    new_category = [dict(category) for category in category_task]
    new_resp['categories'] = [category for category in new_category if category.pop('tasks', None)]
    return jsonify(new_resp), 200



def delete_task(task_id):
    session = current_app.db.session
    task = TaskModel.query.get(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    session.delete(task)
    session.commit()
    return jsonify({"message": "Task deleted"}), 204


def get_tasks():
    session = current_app.db.session

    param: dict = dict(request.args)

    if param.get("order_by", None) == 'categories':
        return jsonify({"error": "Impossible order by categories in tasks"}), 400
    

    if param:
        q_options = {
                "asc": asc(getattr(TaskModel, param.get('order_by', 'id'))),
                "dsc": desc(getattr(TaskModel, param.get('order_by', 'id')))        
            }
        all_tasks = session.query(TaskModel).order_by(q_options.get(param.get('dir', 'asc'))).all()
        resp = [dict(task) for task in all_tasks]
        for task in resp:
            option = limitation(task)
            eisen = session.query(EisenhowerModel).filter_by(type=option).first()
            tasky_id = tasks_categories_table.columns.get('task_id')
            category_task = CategoriesModel.query.select_from(tasks_categories_table).join(CategoriesModel).filter(tasky_id == task['id']).all()
            new_category = [dict(category) for category in category_task]
            task['eisenhower_classification'] = eisen.type
            task['categories'] = [category for category in new_category if category.pop('tasks', None)]
        
        return jsonify(resp), 200
    else:
        all_tasks = session.query(TaskModel).all()
        resp = [dict(task) for task in all_tasks]
        for task in resp:
            option = limitation(task)
            eisen = session.query(EisenhowerModel).filter_by(type=option).first()
            tasky_id = tasks_categories_table.columns.get('task_id')
            category_task = CategoriesModel.query.select_from(tasks_categories_table).join(CategoriesModel).filter(tasky_id == task['id']).all()
            new_category = [dict(category) for category in category_task]
            task['eisenhower_classification'] = eisen.type
            task['categories'] = [category for category in new_category if category.pop('tasks', None)]
        return jsonify(resp), 200


def get_task_by_id(task_id):
    session = current_app.db.session
    task = session.query(TaskModel).get(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    response = dict(task)
    option = limitation(response)
    eisen = session.query(EisenhowerModel).filter_by(type=option).first()
    tasky_id = tasks_categories_table.columns.get('task_id')
    category_task = CategoriesModel.query.select_from(tasks_categories_table).join(CategoriesModel).filter(tasky_id == task_id).all()
    new_category = [dict(category) for category in category_task]
    response['eisenhower_classification'] = eisen.type
    response['categories'] = [category for category in new_category if category.pop('tasks', None)]
    
    return jsonify(response), 200


def get_task_by_name_or_descrip(name_or_descrip):
    session = current_app.db.session
    param: dict = dict(request.args)
    try:
        task = session.query(TaskModel).filter(getattr(TaskModel, name_or_descrip).ilike('%' + str(param.get('text')) + '%')).all()
        if len(task) == 0:
            return jsonify({"error": f"No such text found on {name_or_descrip}"}), 404

        response = [dict(task) for task in task]
        for task in response:
            option = limitation(task)
            eisen = session.query(EisenhowerModel).filter_by(type=option).first()
            tasky_id = tasks_categories_table.columns.get('task_id')
            category_task = CategoriesModel.query.select_from(tasks_categories_table).join(CategoriesModel).filter(tasky_id == task['id']).all()
            new_category = [dict(category) for category in category_task]
            task['eisenhower_classification'] = eisen.type
            task['categories'] = [category for category in new_category if category.pop('tasks', None)]
        return jsonify(response), 200
    except AttributeError as e:
        return jsonify({"error": "Allowed to search is name or description"}), 400

    