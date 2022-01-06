from flask import Blueprint
from app.controllers.categories_controller import create_category, update_category_by_id, delete_category_by_id, get_categories, get_catg_by_id


bp = Blueprint('categories', __name__, url_prefix='/category')

bp.post("")(create_category)
bp.patch("/<int:category_id>")(update_category_by_id)
bp.delete("/<int:category_id>")(delete_category_by_id)
bp.get("")(get_categories)
bp.get("/<int:category_id>")(get_catg_by_id)