from  app.configs.database import db
from dataclasses import dataclass

@dataclass
class TaskModel(db.Model):
    __tablename__ = 'tasks'

    task_id: int
    name: str
    description: str
    duration: int
    importance: int
    urgency: int
    


    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(200))
    duration = db.Column(db.Integer)
    importance = db.Column(db.Integer)
    urgency = db.Column(db.Integer)
    eisenhower_id = db.Column(db.Integer, db.ForeignKey('eisenhowers.eisenhower_id'), nullable=False)


    def __iter__(self):
        yield 'task_id', self.task_id
        yield 'name', self.name
        yield 'description', self.description
        yield 'duration', self.duration
        yield 'importance', self.importance
        yield 'urgency', self.urgency
        
   
    