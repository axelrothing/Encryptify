from . import db

class Encryption_Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    shift = db.Column(db.Integer)




