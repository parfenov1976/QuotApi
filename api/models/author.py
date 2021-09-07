from api import db


class AuthorModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    surname = db.Column(db.String(32), server_default="Unknown")
    quotes = db.relationship('QuoteModel', backref='author', lazy='dynamic')

    def __init__(self, name):
        self.name = name
