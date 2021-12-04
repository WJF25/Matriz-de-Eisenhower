from flask import request, jsonify, current_app
import sqlalchemy 
import psycopg2
from app.models.categories_model import CategoriesModel
from app.controllers.verifications import WrongKeyError, limitation, verify_keys



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
    categories = session.query(CategoriesModel).all()
    response = [dict(category) for category in categories]
    for i in range(len(response)):
        response[i]['tasks'] = [dict(g) for g in response[i]['tasks']]
        if len(response[i]['tasks']) > 0:
            for j in range(len(response[i]['tasks'])):
                eisen = limitation(response[i]['tasks'][j])
                del response[i]['tasks'][j]['duration']
                del response[i]['tasks'][j]['importance']
                del response[i]['tasks'][j]['urgency']
                response[i]['tasks'][j]['priority'] = eisen       

    
    return jsonify(response), 200