from app import db
from sqlalchemy.dialects.postgresql import ARRAY


class teleusers(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Tags = db.Column(ARRAY(db.Text))
    Tunels = db.Column(ARRAY(db.Integer))
    TunelsLevel = db.Column(ARRAY(db.Integer))
    LastAct = db.Column(db.Integer)

class messages(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Text = db.Column(db.Text)
    Attach = db.Column(db.Text)
    ButtonText = db.Column(db.Text)
    TagAdd = db.Column(ARRAY(db.Text))
    TagRem = db.Column(ARRAY(db.Text))
    Img = db.Column(db.Text)

class product(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    MessageId = db.Column(db.Integer)
    ProductName = db.Column(db.Text)
    DownloadLink = db.Column(db.Text)
    FileIdTelega = db.Column(db.Text)
    Img = db.Column(db.Text)