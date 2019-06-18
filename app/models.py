from app import db
from sqlalchemy.dialects.postgresql import ARRAY


class test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer)