from flask import request, jsonify, current_app
import sqlalchemy 
import psycopg2
from app.models.categories_model import CategoriesModel
from app.controllers.verifications import WrongKeyError, limitation, verify_keys
from sqlalchemy import asc, desc



def create_category():
    try:
        session = current_app.db.session
        data = request.get_json()
        verify_keys(data, "category")
        category = CategoriesModel(**data)
        session.add(category)
        session.commit()

        response = dict(category)    
        del response['tasks']

        return jsonify(response), 201
    except (sqlalchemy.exc.IntegrityError ) as e:
        if type(e.orig) == psycopg2.errors.UniqueViolation:
            return jsonify({"error": "Category already exists"}), 409
    except WrongKeyError as f:   
            return jsonify(f.value), 400


def update_category_by_id(category_id):
    try:
        session = current_app.db.session
        data = request.get_json()
        verify_keys(data, "category", "patch")
        category = session.query(CategoriesModel).filter_by(id=category_id).update(data)   
        
        session.commit()

        category = session.query(CategoriesModel).filter_by(id=category_id).first()
        if category is None:
            return jsonify({"error": "Category not found"}), 404
        response = dict(category)    
        del response['tasks']        
        return jsonify(response), 200
    except (sqlalchemy.exc.IntegrityError ) as e:
        if type(e.orig) == psycopg2.errors.UniqueViolation:
            return jsonify({"error": "Category already exists"}), 409
    except WrongKeyError as f:   
            return jsonify(f.value), 400



def delete_category_by_id(category_id):
    
    session = current_app.db.session
    category = session.query(CategoriesModel).get(category_id)
    if category is None:
        return jsonify({"error": "Category not found"}), 404
    session.delete(category)
    session.commit()
    
    return jsonify(category), 204
    


def get_categories():
    session = current_app.db.session

    param: dict = dict(request.args)

    if param.get('order_by', None) == 'tasks':
        return jsonify({"error": "It's not possible order by tasks in categories"}), 400

    if param:
        q_options = {
            "asc": asc(getattr(CategoriesModel, param.get('order_by', 'id'))),
            "dsc": desc(getattr(CategoriesModel, param.get('order_by', 'id')))        
        }
        categories = session.query(CategoriesModel).order_by(q_options.get(param.get('dir', 'asc'))).all()
        
        response = [dict(category) for category in categories]
        for i in response:
            i['tasks'] = [dict(task) for task in i['tasks']]
            if len(i['tasks']) > 0:
                for j in i['tasks']:
                    eisen = limitation(j)
                    del j['duration'], j['importance'], j['urgency']
                    j['priority'] = eisen       
        return jsonify(response), 200
    else:
        categories = session.query(CategoriesModel).all()
            
        response = [dict(category) for category in categories]
        for i in response:
            i['tasks'] = [dict(task) for task in i['tasks']]
            if len(i['tasks']) > 0:
                for j in i['tasks']:
                    eisen = limitation(j)
                    del j['duration'], j['importance'], j['urgency']
                    j['priority'] = eisen
        
        return jsonify(response), 200


def get_catg_by_id(category_id):
    session = current_app.db.session
    category = session.query(CategoriesModel).get(category_id)
    if category is None:
        return jsonify({"error": "Category not found"}), 404

    response = dict(category)

    response['tasks'] = [dict(task) for task in response['tasks']]

    if len(response['tasks']) > 0:
        for i in response['tasks']:
            eisen = limitation(i)
            del i['duration'], i['importance'], i['urgency']
            i['priority'] = eisen
    return jsonify(response), 200