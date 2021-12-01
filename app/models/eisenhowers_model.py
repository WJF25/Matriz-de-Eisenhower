from app.configs.database import db
from dataclasses import dataclass


class EisenhowerModel(db.Model):
    __tablename__ = "eisenhowers"

    eisenhower_id = db.Column(db.Integer, primary_key=True)
    eisen_type = db.Column(db.String(100))


    def __repr__(self):
        return "<Eisenhower(eisonhower_id='%s', eisen_type='%s')>" % (self.eisenhower_id, self.eisen_type)