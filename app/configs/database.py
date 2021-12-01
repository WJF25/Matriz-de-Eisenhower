from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app: Flask):
    db.init_app(app)
    app.db = db

    from app.models.categories_model import CategoriesModel
    from app.models.eisenhowers_model import EisenhowerModel
    from app.models.tasks_categories_table import tasks_categories_table
    from app.models.tasks_model import TaskModel