from api import Resource, reqparse, db
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema


class UserResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        parser.add_argument("role")
        user_data = parser.parse_args()
        user = UserModel(user_data["username"], user_data["password"], user_data["role"])
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201

    def get(self, user_id=None):
        if user_id is None:
            users = UserModel.query.all()
            return users_schema.dump(users), 200
        user = UserModel.query.get(user_id)
        if not user:
            return f"User id={user_id} not found", 404
        return user_schema.dump(user), 200
