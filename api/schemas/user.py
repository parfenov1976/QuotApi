from api import ma
from api.models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        # fields = ["id", "username"] # перечисление выводимых полей
        exclude = ["password_hash"] # перечисление исключаемых из вывода полей


user_schema = UserSchema()
users_schema = UserSchema(many=True)
