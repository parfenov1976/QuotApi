from api import Resource, reqparse, db
from api.models.author import AuthorModel
from api.schemas.author import author_schema, authors_schema


class AuthorResource(Resource):
    def get(self, author_id=None):
        if author_id is None:
            authors = AuthorModel.query.all()
            return authors_schema.dump(authors), 200

        author = AuthorModel.query.get(author_id)
        if author:
            return f"Author id={author_id} not found", 404

        return author_schema.dump(author), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        author_data = parser.parse_args()
        author = AuthorModel(author_data["name"])
        db.session.add(author)
        db.session.commit()
        return author_schema.dump(author), 201

    def put(self, author_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        author_data = parser.parse_args()
        author = AuthorModel.query.get(author_id)
        if author is None:
            author = AuthorModel(author_data["name"])
            db.session.add(author)
            db.session.commit()
            return author_schema.dump(author), 201
        author.name = author_data["name"]
        db.session.commit()
        return author_schema.dump(author), 200
