from app import db
from sqlalchemy.dialects.postgresql import ARRAY


class Teleusers(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Tags = db.Column(ARRAY(db.Text))
    Tunels = db.Column(ARRAY(db.Integer))
    TunelsLevel = db.Column(ARRAY(db.Integer))
    LastAct = db.Column(db.Integer)