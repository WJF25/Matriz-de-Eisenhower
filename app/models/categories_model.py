from app.configs.database import db
from app.models.tasks_categories_table import tasks_categories_table
from dataclasses import dataclass


@dataclass
class CategoriesModel(db.Model):
    __tablename__ = 'categories'

    category_id: int
    cat_name: str
    cat_description: str   

    category_id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(100), nullable=False, unique=True)
    cat_description = db.Column(db.String(200))

    tasks = db.relationship('TaskModel', secondary=tasks_categories_table, backref="categories")