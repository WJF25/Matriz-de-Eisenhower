from app.configs.database import db
from dataclasses import dataclass


class EisenhowerModel(db.Model):
    __tablename__ = "eisenhowers"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))


    def __repr__(self):
        return "<Eisenhower(id='%s', type='%s')>" % (self.id, self.type)