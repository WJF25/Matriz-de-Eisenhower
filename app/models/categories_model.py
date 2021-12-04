from app.configs.database import db
from app.models.tasks_categories_table import tasks_categories_table
from dataclasses import dataclass


@dataclass
class CategoriesModel(db.Model):
    __tablename__ = 'categories'

    id: int
    name: str
    description: str
    tasks: list

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(200))

    tasks = db.relationship('TaskModel', secondary=tasks_categories_table, backref="categories")

    def __iter__(self):
        yield 'id', self.id
        yield 'name', self.name
        yield 'description', self.description
        yield 'tasks', self.tasks