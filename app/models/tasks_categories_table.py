from app.configs.database import db


tasks_categories_table = db.Table('tasks_categories',
    db.Column('task_category_id', db.Integer, primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.task_id')),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.category_id'))
    )
