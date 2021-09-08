from api import Resource, reqparse, auth, db, g
from api.models.author import AuthorModel
from api.models.quote import QuoteModel
from api.schemas.quote import quote_schema, quotes_schema


class QuoteResource(Resource):
    def get(self, author_id=None, quote_id=None):
        """
        Обрабатываем GET запросы
        :param id: id цитаты
        :return: http-response("текст ответа", статус)
        """
        if author_id is None and quote_id is None:
            quotes = QuoteModel.query.all()
            return quotes_schema.dump(quotes), 200
        author = AuthorModel.query.get(author_id)
        if quote_id is None:
            quotes = author.quotes.all()
            return quotes_schema.dump(quotes), 200
        quote = QuoteModel.query.get(quote_id)
        if quote is not None:
            return quote_schema.dump(quote), 200
        return {"Error": "Quote not found"}, 404

    @auth.login_required
    def post(self, author_id):
        parser = reqparse.RequestParser()
        parser.add_argument("quote", required=True)
        quote_data = parser.parse_args()
        author = AuthorModel.query.get(author_id)
        if author:
            quote = QuoteModel(author, quote_data["quote"])
            db.session.add(quote)
            db.session.commit()
            return quote_schema.dump(quote), 201
        return {"Error": f"Author id={author_id} not found"}, 404

    def put(self, author_id=None, quote_id=None):
        if author_id is None or quote_id is None:
            return {"Error": f"'author_id' or/and 'quote_id' is missing"}, 400
        quote = QuoteModel.query.get(quote_id)
        if not quote:
            return {"Error": f"Quote id={quote_id} not found"}, 404
        if author_id != quote_schema.dump(quote)["author"]["id"]:
            return {"Error": f"Quote id={quote_id} not found in quotes of author with id={author_id}"}, 404
        parser = reqparse.RequestParser()
        parser.add_argument("quote")
        new_data = parser.parse_args()
        quote.quote = new_data["quote"]
        db.session.commit()
        return quote_schema.dump(quote), 200

    def delete(self, author_id=None, quote_id=None):
        if author_id is None or quote_id is None:
            return {"Error": f"'author_id' or/and 'quote_id' is missing"}, 400
        quote = QuoteModel.query.get(quote_id)
        if quote is None:
            return f"Quote with id {quote_id} not found", 404
        if author_id != quote_schema.dump(quote)["author"]["id"]:
            return {"Error": f"Quote id={quote_id} not found in quotes of author with id={author_id}"}, 404
        db.session.delete(quote)
        db.session.commit()
        return quote_schema.dump(quote), 200
