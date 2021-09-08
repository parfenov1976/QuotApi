from api import db
from api.models.author import AuthorModel


class QuoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(AuthorModel.id))
    quote = db.Column(db.String(255), unique=False)
    rate = db.Column(db.Integer, server_default='0')

    def __init__(self, author: AuthorModel, quote: str, rating=0):
        self.author_id = author.id
        self.quote = quote
        self.rate = rating
