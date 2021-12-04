from app.configs.database import db


tasks_categories_table = db.Table('tasks_categories',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
    )
