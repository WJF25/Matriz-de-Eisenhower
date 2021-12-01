from flask import request, jsonify, current_app
from app.models.categories_model import CategoriesModel



def create_category():
    session = current_app.db.session
    #normalizar os dados com .title()
    data = request.get_json()
    category = CategoriesModel(**data)
    session.add(category)
    session.commit()
    return jsonify(category), 201


def update_category_by_id(category_id):
    session = current_app.db.session
    data = request.get_json()
    category = session.query(CategoriesModel).filter_by(category_id=category_id).update(data)   
    
    session.commit()

    category = session.query(CategoriesModel).filter_by(category_id=category_id).first()    
    return jsonify(category), 200



def delete_category_by_id(category_id):
    session = current_app.db.session
    category = session.query(CategoriesModel).get_or_404(category_id)
    session.delete(category)
    session.commit()
    return jsonify(category), 204