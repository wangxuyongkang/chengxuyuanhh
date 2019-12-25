from app import db
from .BaseModels import BaseModel

class hero_lol(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100), nullable=False, default='') # 主图
    name = db.Column(db.String(20), nullable=False, default='')
